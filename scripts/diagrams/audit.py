#!/usr/bin/env python3
"""
Diagram audit: find duplicate keys and map warning strings to their source files.
Run from repo root: python3 scripts/diagrams/audit.py
"""
import re, os, subprocess, collections

DIAG_DIR = 'scripts/diagrams'

# ── Duplicate key detection ─────────────────────────────────────────────────
print("── Duplicate keys ──")
key_to_entries = collections.defaultdict(list)
for fname in sorted(os.listdir(DIAG_DIR)):
    if not fname.endswith('.py') or fname.startswith('_'):
        continue
    path = os.path.join(DIAG_DIR, fname)
    content = open(path).read()
    for m in re.finditer(r"@kb_diagram\s*\(\s*\n?\s*'([^']+)'\s*,\s*\n?\s*'([^']+)'", content):
        key, fpath = m.group(1), m.group(2)
        lineno = content[:m.start()].count('\n') + 1
        key_to_entries[key].append((fname, lineno, fpath))

dups = {k: v for k, v in key_to_entries.items() if len(v) > 1}
if dups:
    for key, entries in sorted(dups.items()):
        print(f"  DUP '{key}':")
        for fname, lineno, fpath in entries:
            print(f"    {fname}:{lineno}  →  {fpath}")
else:
    print("  None found")

# ── Warning extraction ──────────────────────────────────────────────────────
print("\n── Warnings by file ──")
result = subprocess.run(['python3', 'scripts/ascii_diagram_gen.py', '--check'],
                        capture_output=True, text=True)
output = result.stdout + result.stderr

warn_pattern = re.compile(r"WARN (?:bMid|txt_row|sections\[\d+\]): truncated.*?: '(.+)'")
warnings = set()
for line in output.split('\n'):
    m = warn_pattern.search(line)
    if m:
        warnings.add(m.group(1))

print(f"  {len(warnings)} unique warning strings\n")
for fname in sorted(os.listdir(DIAG_DIR)):
    if not fname.endswith('.py') or fname.startswith('_'):
        continue
    path = os.path.join(DIAG_DIR, fname)
    content = open(path).read()
    hits = [(len(w), w) for w in warnings if w in content]
    if hits:
        print(f"  {fname} ({len(hits)} warnings):")
        for length, text in sorted(hits, reverse=True):
            print(f"    [{length}] {text}")
