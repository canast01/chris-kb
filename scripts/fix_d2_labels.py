#!/usr/bin/env python3
"""Wrap D2 node labels longer than 55 chars per line by inserting \\n breaks."""
import re, os, sys, textwrap

DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs'))
WRAP = 50   # target wrap width (leave headroom below 55-char limit)

_D2_BLOCK   = re.compile(r'(```d2\n)(.*?)(\n```)', re.DOTALL)
_NODE_LABEL = re.compile(r'^(\w[\w_.-]*\s*:\s*")([^"]+)(")', re.MULTILINE)


def wrap_label(text, width=WRAP):
    """Word-wrap a label at `width` chars using D2's \\n line-break syntax."""
    # Already has \n breaks — check per-segment
    segments = text.split('\\n')
    result = []
    for seg in segments:
        if len(seg) <= 55:
            result.append(seg)
        else:
            # textwrap at `width`; join pieces with \n
            wrapped = textwrap.wrap(seg, width=width, break_long_words=False)
            if not wrapped:
                wrapped = [seg]
            result.append('\\n'.join(wrapped))
    return '\\n'.join(result)


def fix_block(block_body):
    changed = False

    def replace_label(m):
        nonlocal changed
        prefix, label, suffix = m.group(1), m.group(2), m.group(3)
        max_line = max(len(ln) for ln in label.split('\\n'))
        if max_line <= 55:
            return m.group(0)
        new_label = wrap_label(label)
        if new_label != label:
            changed = True
        return prefix + new_label + suffix

    new_body = _NODE_LABEL.sub(replace_label, block_body)
    return new_body, changed


def process_file(path, dry_run=False):
    text = open(path, errors='replace').read()
    if '```d2' not in text:
        return False

    file_changed = False

    def replace_block(m):
        nonlocal file_changed
        open_tag, body, close_tag = m.group(1), m.group(2), m.group(3)
        new_body, changed = fix_block(body)
        if changed:
            file_changed = True
        return open_tag + new_body + close_tag

    new_text = _D2_BLOCK.sub(replace_block, text)

    if file_changed and not dry_run:
        with open(path, 'w') as fh:
            fh.write(new_text)

    return file_changed


if __name__ == '__main__':
    dry_run = '--dry-run' in sys.argv
    fixed = 0
    for root, dirs, files in os.walk(DOCS):
        dirs.sort()
        for f in sorted(files):
            if not f.endswith('.md'):
                continue
            path = os.path.join(root, f)
            if process_file(path, dry_run=dry_run):
                rel = os.path.relpath(path, DOCS)
                print(f'  fixed: {rel}')
                fixed += 1
    print(f'\n{"Would fix" if dry_run else "Fixed"} {fixed} files')
