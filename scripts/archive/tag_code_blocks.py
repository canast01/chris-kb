#!/usr/bin/env python3
"""Tag untagged code fences with inferred language identifiers."""
import glob, re, sys

ASCII_CHARS = set('┌│└┐┘├┤┬┴┼─═║╔╗╚╝╠╣╦╩╬')

BASH_CMDS = re.compile(
    r'\b(sudo|systemctl|journalctl|apt|yum|dnf|rpm|chmod|chown|mkdir|'
    r'kubectl|helm|docker|podman|ansible|terraform|vault|openssl|'
    r'curl|wget|ssh|scp|rsync|tar|gzip|grep|awk|sed|find|xargs|'
    r'ping|nmap|netstat|ss|ip |ifconfig|route|iptables|'
    r'service |mount |umount|lsblk|fdisk|parted|lvs|vgs|pvs|'
    r'esxcli|esxtop|vim-cmd|vdq|vsan|vmkfstools|nsxcli|'
    r'ontap|cluster|vserver|aggr|vol |snap |snapmirror|'
    r'purestorage|purefa|purearray|purehosts|purevolume)\b'
)
PS_PATTERNS = re.compile(
    r'\b(Get-|Set-|New-|Remove-|Start-|Stop-|Restart-|Test-|'
    r'Invoke-|Write-Host|Write-Output|Write-Error|'
    r'Import-Module|Export-|Connect-|Disconnect-)\w',
    re.I
)
PYTHON_PATTERNS = re.compile(
    r'\b(import |from .+ import|def |class |print\(|'
    r'if __name__|return |raise |with open|\.format\(|f\")\b'
)
YAML_PATTERNS = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_\-]*:\s', re.M)
HCL_PATTERNS = re.compile(
    r'^(resource |variable |provider |terraform |data |output |module )'
    r'"[a-z]', re.M
)
SQL_PATTERNS = re.compile(
    r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|GRANT|REVOKE|'
    r'FROM|WHERE|JOIN|GROUP BY|ORDER BY|HAVING)\b', re.I
)
JSON_PATTERN = re.compile(r'^\s*[{\[]')
XML_PATTERN  = re.compile(r'^\s*<[?!a-zA-Z]')
INI_PATTERN  = re.compile(r'^\[[\w\s]+\]$', re.M)


def infer_lang(block_lines):
    """Return a language tag string, or '' to leave untagged."""
    content = [l for l in block_lines if l.strip()]
    if not content:
        return ''

    full_text = ''.join(content)
    first = content[0].lstrip()

    # ASCII box-drawing diagram — leave plain
    if first and first[0] in ASCII_CHARS:
        return ''

    # Shebang
    if first.startswith('#!/bin/bash') or first.startswith('#!/bin/sh'):
        return 'bash'
    if 'python' in first and first.startswith('#!'):
        return 'python'

    # PowerShell
    if PS_PATTERNS.search(full_text):
        return 'powershell'

    # Python
    if PYTHON_PATTERNS.search(full_text):
        return 'python'

    # HCL / Terraform
    if HCL_PATTERNS.search(full_text):
        return 'hcl'

    # SQL
    if SQL_PATTERNS.search(full_text[:500]):
        return 'sql'

    # XML / HTML
    if XML_PATTERN.match(first):
        return 'xml'

    # JSON
    if JSON_PATTERN.match(first):
        return 'json'

    # YAML: key: value structure, no leading spaces on first line
    if (YAML_PATTERNS.search(full_text) and
            not first.startswith(' ') and
            ':' in first and
            not first.startswith('#')):
        return 'yaml'

    # INI-style config
    if INI_PATTERN.search(full_text) and len(content) > 2:
        return 'ini'

    # Bash heuristics
    if (first.startswith('$ ') or
            first.startswith('# ') and BASH_CMDS.search(full_text) or
            BASH_CMDS.search(full_text[:300])):
        return 'bash'

    # Comment-only or separator (---) blocks → text
    if all(l.strip().startswith('#') or l.strip() == '---' or
           not l.strip() for l in content):
        return 'text'

    # Markdown table or formatted text
    if first.startswith('|') or first.startswith('---'):
        return 'text'

    # Multi-line plain text / prose
    avg_line_len = sum(len(l.rstrip()) for l in content) / len(content)
    if avg_line_len > 40 and not any(c in full_text for c in '{}[]()<>'):
        return 'text'

    return ''  # uncertain — leave plain


def process_file(path, dry_run=False):
    with open(path) as f:
        lines = f.readlines()

    new_lines = []
    in_fence = False
    block_lines = []
    fence_start_idx = None
    changed = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not in_fence:
            if stripped == '```':
                in_fence = True
                fence_start_idx = len(new_lines)
                block_lines = []
                new_lines.append(line)  # placeholder
            elif stripped.startswith('```'):
                in_fence = True
                block_lines = []
                new_lines.append(line)
                fence_start_idx = None  # already tagged
            else:
                new_lines.append(line)
        else:
            if stripped == '```':
                in_fence = False
                if fence_start_idx is not None:
                    lang = infer_lang(block_lines)
                    if lang:
                        new_lines[fence_start_idx] = f'```{lang}\n'
                        changed += 1
                fence_start_idx = None
                block_lines = []
                new_lines.append(line)
            else:
                block_lines.append(line)
                new_lines.append(line)
        i += 1

    if changed and not dry_run:
        with open(path, 'w') as f:
            f.writelines(new_lines)

    return changed


def main():
    dry_run = '--dry-run' in sys.argv
    pages = sorted(glob.glob('docs/**/*.md', recursive=True))

    total_files = 0
    total_tags = 0
    for p in pages:
        n = process_file(p, dry_run=dry_run)
        if n:
            total_files += 1
            total_tags += n

    mode = 'DRY RUN' if dry_run else 'APPLIED'
    print(f"[{mode}] Tagged {total_tags} blocks across {total_files} files")


if __name__ == '__main__':
    main()
