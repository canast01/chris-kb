#!/usr/bin/env python3
"""
add_command_output.py — Add example output + common errors to bash blocks site-wide.

For every bash block NOT already followed by a non-bash code fence:
  1. Extract the commands
  2. Call Claude Haiku to generate:
       - Realistic expected output (5-15 lines)
       - 2-3 most common errors with one-line fix steps
  3. Insert immediately after the closing fence:
       ```text title="Expected output"
       <output>
       ```
       !!! warning "Common errors"
           **`<error>`** — <fix>

Usage:
  python3 scripts/add_command_output.py --section docs/virtualization/vmware/esxi
  python3 scripts/add_command_output.py --section docs/virtualization/vmware/esxi --dry-run
  python3 scripts/add_command_output.py --file docs/virtualization/vmware/esxi/operations/health-checks.md --dry-run
  python3 scripts/add_command_output.py --section docs/virtualization --limit 20
  python3 scripts/add_command_output.py --section docs/virtualization --resume

Options:
  --section DIR    Process all .md files under DIR
  --file FILE      Process a single file
  --dry-run        Print what would be inserted; do not write files
  --limit N        Stop after processing N bash blocks total (0=unlimited)
  --model MODEL    Anthropic model (default: claude-haiku-4-5-20251001)
  --delay SECS     Seconds between API calls (default: 0.3)
  --resume         Skip files already marked done in command_output_manifest.json
"""

import argparse
import glob
import json
import os
import re
import sys
import time

import anthropic

MANIFEST_PATH = 'scripts/command_output_manifest.json'

BASH_OPEN   = re.compile(r'^```bash\b', re.MULTILINE)
FENCE_CLOSE = re.compile(r'^```\s*$', re.MULTILINE)

SILENT_PREFIXES = ('reboot', 'shutdown', 'poweroff', 'halt')

SYSTEM_PROMPT = """You are a technical writer for an IT infrastructure knowledge base.
Given a bash code block from a documentation page, generate:
1. Realistic expected terminal output (5-15 lines). Use real-looking values — hostnames, IPs, build numbers, UUIDs.
   If the block contains multiple commands, show consolidated output in the order the commands run.
   If a command truly produces no output (e.g. setting a config silently), write: (no output — command completes silently)
2. The 2-3 most common errors an admin would actually see, each with a one-sentence fix.

Format your response EXACTLY as:
---OUTPUT---
<realistic terminal output here>
---ERRORS---
**`<exact error message>`** — <one-sentence fix>
**`<exact error message>`** — <one-sentence fix>

Rules:
- Keep output realistic: truncate long lists to 5-8 representative lines then add "..."
- Error messages should be exact shell/CLI error text, not descriptions
- Fix steps must be actionable in one sentence
- Do NOT add any text outside the ---OUTPUT--- and ---ERRORS--- sections
- If there are no meaningful errors possible (e.g. read-only query), write: (no common errors)"""


def build_user_prompt(block: str, file_path: str) -> str:
    parts = file_path.replace('docs/', '').split('/')
    context = ' > '.join(parts[:4]) if len(parts) >= 4 else file_path
    return f"File: {context}\n\nBash block:\n{block}\n\nGenerate expected output and common errors."


def extract_bash_blocks(text: str):
    results = []
    pos = 0
    while True:
        m_open = BASH_OPEN.search(text, pos)
        if not m_open:
            break
        m_close = FENCE_CLOSE.search(text, m_open.end())
        if not m_close:
            break
        start = m_open.start()
        end   = m_close.end()
        results.append((start, end, text[start:end]))
        pos = end
    return results


def already_has_output(text: str, bash_end: int) -> bool:
    after = text[bash_end:bash_end + 300].lstrip('\n ')
    return after.startswith('```') and not after.startswith('```bash')


def is_silent_block(block: str) -> bool:
    lines = [l.strip() for l in block.splitlines() if l.strip() and not l.startswith('```')]
    code_lines = [l for l in lines if l and not l.startswith('#')]
    if not code_lines:
        return True
    return all(any(l.startswith(p) for p in SILENT_PREFIXES) for l in code_lines)


def call_claude(block: str, file_path: str, model: str) -> tuple[str, str]:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        system=SYSTEM_PROMPT,
        messages=[{'role': 'user', 'content': build_user_prompt(block, file_path)}],
        temperature=0.3,
        max_tokens=600,
    )
    raw = response.content[0].text.strip()
    out_m = re.search(r'---OUTPUT---\s*(.*?)(?=---ERRORS---|$)', raw, re.DOTALL)
    err_m = re.search(r'---ERRORS---\s*(.*?)$', raw, re.DOTALL)
    output_text = out_m.group(1).strip() if out_m else '(output unavailable)'
    errors_text = err_m.group(1).strip() if err_m else '(no common errors)'
    return output_text, errors_text


def format_insertion(output_text: str, errors_text: str) -> str:
    parts = [f'\n\n```text title="Expected output"\n{output_text}\n```']
    if errors_text and errors_text != '(no common errors)':
        indented = '\n'.join(f'    {line}' for line in errors_text.splitlines())
        parts.append(f'\n\n!!! warning "Common errors"\n{indented}')
    return ''.join(parts)


def load_manifest() -> dict:
    if os.path.exists(MANIFEST_PATH):
        return json.load(open(MANIFEST_PATH))
    return {}


def save_manifest(manifest: dict):
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(manifest, f, indent=2)


def mark_file_done(manifest: dict, file_path: str):
    for sec_data in manifest.get('sections', {}).values():
        for entry in sec_data.get('files', []):
            if entry['file'] == file_path:
                entry['done'] = True
                return


def is_file_done(manifest: dict, file_path: str) -> bool:
    for sec_data in manifest.get('sections', {}).values():
        for entry in sec_data.get('files', []):
            if entry['file'] == file_path and entry.get('done'):
                return True
    return False


def process_file(path: str, dry_run: bool, model: str, delay: float,
                 limit_counter: list, limit: int) -> int:
    text = open(path, encoding='utf-8', errors='replace').read()
    blocks = extract_bash_blocks(text)
    if not blocks:
        return 0

    insertions = []
    augmented  = 0

    for start, end, block in blocks:
        if limit > 0 and limit_counter[0] >= limit:
            break
        if already_has_output(text, end):
            continue
        if is_silent_block(block):
            continue

        try:
            output_text, errors_text = call_claude(block, path, model)
        except Exception as e:
            print(f'  [ERROR] {path}: {e}', file=sys.stderr)
            continue

        insertion = format_insertion(output_text, errors_text)
        insertions.append((end, insertion))
        limit_counter[0] += 1
        augmented += 1

        if dry_run:
            print(f'\n{"─"*70}')
            print(f'FILE: {path}')
            print(f'BLOCK (first 200 chars):\n{block[:200]}{"..." if len(block)>200 else ""}')
            print(f'WOULD INSERT:{insertion}')

        if delay > 0:
            time.sleep(delay)

    if not dry_run and insertions:
        for insert_pos, insertion_text in sorted(insertions, key=lambda x: -x[0]):
            text = text[:insert_pos] + insertion_text + text[insert_pos:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)

    return augmented


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--section', help='Directory to process recursively')
    group.add_argument('--file',    help='Single file to process')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--resume',  action='store_true', help='Skip files marked done in manifest')
    parser.add_argument('--limit',   type=int, default=0)
    parser.add_argument('--model',   default='claude-haiku-4-5-20251001')
    parser.add_argument('--delay',   type=float, default=0.3)
    args = parser.parse_args()

    if args.file:
        files = [args.file]
    else:
        files = sorted(glob.glob(os.path.join(args.section, '**', '*.md'), recursive=True))

    if not files:
        print('No .md files found.')
        sys.exit(1)

    manifest = load_manifest() if args.resume else {}
    mode = 'DRY-RUN' if args.dry_run else 'LIVE'
    print(f'[add_command_output] {mode} | {len(files)} files | model={args.model} | limit={args.limit or "∞"} | resume={args.resume}')

    total_augmented = 0
    limit_counter   = [0]
    files_skipped   = 0

    for path in files:
        if limit > 0 and limit_counter[0] >= (limit := args.limit):
            break
        if args.resume and is_file_done(manifest, path):
            files_skipped += 1
            continue

        n = process_file(path, args.dry_run, args.model, args.delay, limit_counter, args.limit)

        if n:
            print(f'  {"[DRY]" if args.dry_run else "[OK] "} {path} — {n} block(s)')
            total_augmented += n
            if not args.dry_run and args.resume:
                mark_file_done(manifest, path)
                save_manifest(manifest)

    if args.resume and files_skipped:
        print(f'  (skipped {files_skipped} already-done files via --resume)')

    print(f'\n✓ Done. {total_augmented} block(s) {"would be " if args.dry_run else ""}augmented.')
    if not args.dry_run and total_augmented:
        print('Run: python3 scripts/site_audit.py && mkdocs build -q')


if __name__ == '__main__':
    main()
