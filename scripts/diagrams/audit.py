#!/usr/bin/env python3
"""
Diagram audit: duplicates, orphaned registrations, missing pages, over-width strings.
Run from repo root: python3 scripts/diagrams/audit.py [--section <prefix>]

  --section virtualization   show missing pages only under docs/virtualization/
"""
import re, os, sys, subprocess, collections

DIAG_DIR = 'scripts/diagrams'
DOCS_DIR = 'docs'

section_filter = None
if '--section' in sys.argv:
    idx = sys.argv.index('--section')
    if idx + 1 < len(sys.argv):
        section_filter = sys.argv[idx + 1].strip('/')

# ── Duplicate key detection ─────────────────────────────────────────────────
print("── Duplicate keys ──")
key_to_entries = collections.defaultdict(list)
registered_files = {}   # key -> filepath (for orphan check)
for fname in sorted(os.listdir(DIAG_DIR)):
    if not fname.endswith('.py') or fname.startswith('_'):
        continue
    path = os.path.join(DIAG_DIR, fname)
    content = open(path).read()
    for m in re.finditer(r"@kb_diagram\s*\(\s*\n?\s*'([^']+)'\s*,\s*\n?\s*'([^']+)'", content):
        key, fpath = m.group(1), m.group(2)
        lineno = content[:m.start()].count('\n') + 1
        key_to_entries[key].append((fname, lineno, fpath))
        registered_files[key] = fpath

dups = {k: v for k, v in key_to_entries.items() if len(v) > 1}
if dups:
    for key, entries in sorted(dups.items()):
        print(f"  DUP '{key}':")
        for fname, lineno, fpath in entries:
            print(f"    {fname}:{lineno}  →  {fpath}")
else:
    print("  None found")

# ── Orphaned registrations ──────────────────────────────────────────────────
print("\n── Orphaned registrations (target file missing) ──")
orphans = [(k, f) for k, f in registered_files.items() if not os.path.exists(f)]
if orphans:
    for key, fpath in sorted(orphans):
        print(f"  '{key}'  →  {fpath}")
else:
    print("  None found")

# ── Pages missing a diagram ─────────────────────────────────────────────────
print("\n── Pages missing a diagram ──")
registered_paths = set(registered_files.values())
all_index_files = []
for dirpath, _, filenames in os.walk(DOCS_DIR):
    for fn in filenames:
        if fn == 'index.md':
            all_index_files.append(os.path.join(dirpath, fn).lstrip('./'))

missing = sorted(p for p in all_index_files if p not in registered_paths)
if section_filter:
    missing = [p for p in missing if p.startswith(f'docs/{section_filter}/')]

# Group by top-level section
by_section = collections.defaultdict(list)
for p in missing:
    parts = p.split('/')
    section = parts[1] if len(parts) > 2 else '(root)'
    by_section[section].append(p)

print(f"  {len(missing)} pages have no registered diagram"
      + (f" (filtered: docs/{section_filter}/)" if section_filter else ""))
for section in sorted(by_section):
    print(f"  {section}: {len(by_section[section])}")

if section_filter and missing:
    print()
    for p in missing:
        print(f"    {p}")

# ── Over-width strings (now raises ValueError — check for any residual) ──────
print("\n── Over-width strings (via --check) ──")
result = subprocess.run(['python3', 'scripts/ascii_diagram_gen.py', '--check'],
                        capture_output=True, text=True)
output = result.stdout + result.stderr

warn_pattern = re.compile(r"WARN (?:bMid|txt_row|sections\[\d+\]): truncated.*?: '(.+)'")
warnings = set()
for line in output.split('\n'):
    m = warn_pattern.search(line)
    if m:
        warnings.add(m.group(1))

if warnings:
    print(f"  {len(warnings)} unique over-width strings:\n")
    for fname in sorted(os.listdir(DIAG_DIR)):
        if not fname.endswith('.py') or fname.startswith('_'):
            continue
        content = open(os.path.join(DIAG_DIR, fname)).read()
        hits = [(len(w), w) for w in warnings if w in content]
        if hits:
            print(f"  {fname} ({len(hits)}):")
            for length, text in sorted(hits, reverse=True):
                print(f"    [{length}] {text}")
else:
    print("  None found")
