#!/usr/bin/env python3
"""
Auto-tag untagged fenced code blocks in docs/**/*.md.

Usage:
    python3 scripts/tag-code-blocks.py            # apply tags in place
    python3 scripts/tag-code-blocks.py --dry-run  # preview counts only
"""
import glob
import re
import sys
from collections import defaultdict
from pathlib import Path


def detect_language(lines):
    if not lines:
        return 'text'
    text = '\n'.join(lines)
    if not text.strip():
        return 'text'

    # PowerShell — Verb-Noun cmdlets are highly distinctive
    if re.search(
        r'\b(?:Get|Set|New|Remove|Start|Stop|Invoke|Write|Read|Test|Connect|Disconnect'
        r'|Add|Clear|Copy|Move|Select|Where|Sort|Format|Export|Import|Out'
        r'|ConvertTo|ConvertFrom|Register|Unregister|Enable|Disable|Update|Repair'
        r'|Restore|Reset|Publish|Suspend|Resume|Unlock|Wait|Watch)-\w+',
        text,
    ):
        return 'powershell'
    if re.search(
        r'param\s*\('
        r'|\[Parameter\b'
        r'|\[CmdletBinding\b'
        r'|\[string\]\s*\$'
        r'|\[int\]\s*\$'
        r'|\[bool\]\s*\$'
        r'|\$ErrorActionPreference'
        r'|\$PSCmdlet'
        r'|\$_\b'
        r'|\bforeach\s*\(\s*\$',
        text,
    ):
        return 'powershell'

    # Python
    if re.search(r'^\s*(?:def |class |import |from \w+ import |async def )', text, re.M):
        return 'python'
    if re.search(r'#!/usr/bin/env python|if __name__\s*==', text):
        return 'python'

    # YAML
    if re.search(r'^(?:apiVersion|kind|metadata|spec|namespace|replicas|selector):\s', text, re.M):
        return 'yaml'
    if re.search(r'^---\s*$', text, re.M) and re.search(r'^\w[\w.-]*:\s', text, re.M):
        return 'yaml'

    # JSON
    ts = text.strip()
    if ts[:1] in ('{', '[') and re.search(r'"[^"]+"\s*:', text):
        return 'json'

    # HCL / Terraform
    if re.search(r'\b(?:resource|variable|module|provider|terraform|output|data)\s+"', text):
        return 'hcl'

    # INI / config
    if (re.search(r'^\[[\w\s./-]+\]\s*$', text, re.M)
            and re.search(r'^[\w./][\w./-]*\s*=\s*.+', text, re.M)):
        return 'ini'

    # XML
    if re.search(r'<[a-zA-Z][\w]*[^>]*/?>.*</[\w]+>', text, re.S):
        return 'xml'

    # Bash / shell — explicit indicators
    if re.search(r'#!/(?:bin|usr/bin/env)\s*(?:ba)?sh', text):
        return 'bash'
    if re.search(r'^\s*(?:sudo |apt-get |apt |yum |dnf |brew |pip3? |npm |gem )', text, re.M):
        return 'bash'
    if re.search(r'^\s*(?:systemctl |journalctl |service )', text, re.M):
        return 'bash'
    if re.search(r'^\s*(?:chmod |chown |chgrp |mkdir |rm |cp |mv )', text, re.M):
        return 'bash'
    if re.search(r'\$\([^)]+\)|if \[\[|if \[ |for \w+ in |while \[', text):
        return 'bash'
    if re.search(r'^\s*(?:curl |wget |ssh |scp |rsync |tar |docker |kubectl )', text, re.M):
        return 'bash'
    if re.search(r'^\s*(?:cat |echo |grep |awk |sed |find |ls -|ps |df |du )', text, re.M):
        return 'bash'
    if re.search(r'^\s*(?:git |python3? |pip3? |node |npm |mkdocs |ansible )', text, re.M):
        return 'bash'

    return 'text'


def process_file(path):
    raw = path.read_text(encoding='utf-8', errors='replace')
    lines = raw.splitlines(keepends=True)

    out = []
    changes = []

    in_fence = False
    fence_marks = None
    fence_tagged = False
    fence_content = []
    fence_out_idx = None
    fence_orig_line = None

    for _lineno, line in enumerate(lines, start=1):
        s = line.rstrip('\n\r').strip()

        if not in_fence:
            m = re.match(r'^(`{3,}|~{3,})(.*)', s)
            if m:
                marks = m.group(1)
                rest = m.group(2).strip()
                in_fence = True
                fence_marks = marks
                fence_tagged = bool(rest)
                fence_content = []
                if fence_tagged:
                    out.append(line)
                else:
                    fence_out_idx = len(out)
                    fence_orig_line = line
                    out.append(None)
            else:
                out.append(line)
        else:
            if s == fence_marks:
                in_fence = False
                if not fence_tagged:
                    lang = detect_language(fence_content)
                    m2 = re.match(r'^(\s*)(`{3,}|~{3,})', fence_orig_line)
                    if m2:
                        ws, fmarks = m2.group(1), m2.group(2)
                    else:
                        ws, fmarks = '', fence_marks
                    eol_pos = len(fence_orig_line.rstrip('\n\r'))
                    eol = fence_orig_line[eol_pos:]
                    out[fence_out_idx] = ws + fmarks + lang + eol
                    changes.append((fence_out_idx + 1, lang))
                fence_content = []
                out.append(line)
            else:
                if not fence_tagged:
                    fence_content.append(line.rstrip('\n\r'))
                out.append(line)

    # Unclosed fence — restore placeholder with original line (no tagging)
    if in_fence and not fence_tagged and fence_out_idx is not None and out[fence_out_idx] is None:
        out[fence_out_idx] = fence_orig_line

    return ''.join(out), changes


def main():
    dry_run = '--dry-run' in sys.argv

    md_files = sorted(glob.glob('docs/**/*.md', recursive=True))
    total_blocks = 0
    total_files = 0
    lang_counts = defaultdict(int)

    for md in md_files:
        p = Path(md)
        new_content, changes = process_file(p)
        if changes:
            total_blocks += len(changes)
            total_files += 1
            for _, lang in changes:
                lang_counts[lang] += 1
            if not dry_run:
                p.write_text(new_content, encoding='utf-8')

    print(f'Tagged {total_blocks} blocks across {total_files} files')
    print()
    for lang, cnt in sorted(lang_counts.items(), key=lambda x: -x[1]):
        pct = cnt / total_blocks * 100 if total_blocks else 0
        print(f'  {lang:<15}  {cnt:>5}  ({pct:.0f}%)')

    if dry_run:
        print('\n(dry-run — no files written)')


if __name__ == '__main__':
    main()
