#!/usr/bin/env python3
"""Fix broken relative .md links site-wide.

Strategies applied (in order):
  1. /index.md → .md  (file lives at peer level, not in sub-dir)
  2. ../../tools/ → ../../itsm/  (ITSM tools relocated)
  3. Remove lines whose link target simply doesn't exist anywhere
"""
import re, os, sys

DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs'))

_MD_LINK = re.compile(r'\[([^\]]+)\]\(([^)]+\.md[^)]*)\)')


def resolve(base_dir, rel_link):
    """Return absolute path of rel_link from base_dir, or None if outside DOCS."""
    abs_path = os.path.normpath(os.path.join(base_dir, rel_link))
    if abs_path.startswith(DOCS):
        return abs_path
    return None


def fix_link(base_dir, link_target):
    """
    Try to find a working alternative for a broken link_target.
    Returns the fixed target string, or None if no fix found.
    """
    # Strip anchor
    anchor = ''
    if '#' in link_target:
        link_target, anchor = link_target.split('#', 1)
        anchor = '#' + anchor

    # Strategy 1: replace /index.md suffix with .md
    if link_target.endswith('/index.md'):
        candidate = link_target[:-len('/index.md')] + '.md'
        abs_c = resolve(base_dir, candidate)
        if abs_c and os.path.isfile(abs_c):
            return candidate + anchor

    # Strategy 2: tools/ → itsm/
    if '/tools/' in link_target:
        candidate = link_target.replace('/tools/', '/itsm/')
        abs_c = resolve(base_dir, candidate)
        if abs_c and os.path.isfile(abs_c):
            return candidate + anchor
        # also try flat variant of that
        if candidate.endswith('/index.md'):
            flat = candidate[:-len('/index.md')] + '.md'
            abs_f = resolve(base_dir, flat)
            if abs_f and os.path.isfile(abs_f):
                return flat + anchor

    return None


def process_file(path, dry_run=False):
    text = open(path, errors='replace').read()
    base_dir = os.path.dirname(path)
    new_text = text
    changed = False
    removed_lines = []

    lines = text.split('\n')
    new_lines = []
    for line in lines:
        new_line = line
        for m in _MD_LINK.finditer(line):
            link_target = m.group(2)
            # Skip http links, anchors, absolute paths
            if link_target.startswith('http') or link_target.startswith('#') or link_target.startswith('/'):
                continue
            # Strip anchor for file check
            file_part = link_target.split('#')[0]
            abs_target = resolve(base_dir, file_part)
            if abs_target and os.path.isfile(abs_target):
                continue  # link is valid
            # Broken — try to fix
            fixed = fix_link(base_dir, link_target)
            if fixed:
                new_line = new_line.replace(f']({link_target})', f']({fixed})', 1)
                changed = True
            else:
                # No fix found — remove the entire bullet if it's a list item
                stripped = line.strip()
                if stripped.startswith('- ') or stripped.startswith('* '):
                    new_line = None  # mark for removal
                # else leave the line unchanged (don't break prose)
                break

        if new_line is None:
            removed_lines.append(line)
        else:
            new_lines.append(new_line)

    if removed_lines:
        changed = True

    if changed:
        new_text = '\n'.join(new_lines)
        rel = os.path.relpath(path, DOCS)
        if dry_run:
            print(f'  would fix: {rel} (removed {len(removed_lines)} line(s))')
        else:
            with open(path, 'w') as fh:
                fh.write(new_text)
            print(f'  fixed: {rel}')

    return changed


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
                fixed += 1
    print(f'\n{"Would fix" if dry_run else "Fixed"} {fixed} files')
