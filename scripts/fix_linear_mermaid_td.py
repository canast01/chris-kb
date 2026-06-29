#!/usr/bin/env python3
"""Replace narrow vertical Mermaid flowchart TD/TB diagrams with D2 direction:right.

Strategy:
  1. Pages that already have a D2 direction:right block → just remove the Mermaid TD.
  2. Pages with Mermaid TD only → convert the Mermaid to an equivalent D2 right block.
"""

import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs')

# Matches a complete ```mermaid ... ``` block that contains a linear TD/LR graph
MERMAID_BLOCK = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
LINEAR_TD_PAT = re.compile(r'^(flowchart|graph)\s+(TD|TB|LR|RL)\b', re.MULTILINE)
D2_RIGHT_PAT  = re.compile(r'```d2\n.*?direction:\s*right', re.DOTALL)


def parse_mermaid_to_d2(blk):
    """Convert a linear Mermaid TD block to a D2 direction:right block."""
    lines = blk.splitlines()
    nodes = {}   # id → label
    edges = []   # (from, to)

    for line in lines:
        line = line.strip()
        if not line or line.startswith('%%') or re.match(r'^(flowchart|graph)\b', line):
            continue
        # Skip classDef and class lines
        if line.startswith('classDef') or line.startswith('class '):
            continue
        # Skip style lines
        if line.startswith('style '):
            continue

        # Edge chains: a --> b --> c  or  a & b --> c
        # First extract chained -->
        if '-->' in line or '---' in line:
            # Replace style attributes like | label |
            stripped = re.sub(r'\|[^|]*\|', '', line)
            # Split on --> or ---
            parts = re.split(r'-->|---', stripped)
            # Each part may be a node ID or "id[label]" or "id(label)"
            part_ids = []
            for part in parts:
                part = part.strip()
                # Handle & grouping: "a & b"
                for sub in re.split(r'\s*&\s*', part):
                    sub = sub.strip()
                    if not sub:
                        continue
                    # Extract id and label
                    m_label = re.match(r'([A-Za-z0-9_-]+)\s*[\[\({"\']+(.+?)[\]\)"\']+', sub)
                    if m_label:
                        nid, label = m_label.group(1), m_label.group(2)
                        # Strip <br/> or <br> tags
                        label = re.sub(r'<br\s*/?>\\?n?', ' · ', label, flags=re.IGNORECASE)
                        nodes[nid] = label.strip()
                        part_ids.append(nid)
                    else:
                        # Bare id
                        nid = sub
                        if re.match(r'^[A-Za-z0-9_-]+$', nid):
                            nodes.setdefault(nid, nid)
                            part_ids.append(nid)
            # Build edges from the chain
            for i in range(len(part_ids) - 1):
                edges.append((part_ids[i], part_ids[i + 1]))
            continue

        # Standalone node definition: id[Label] or id(Label) or id{"Label"}
        m_node = re.match(r'^([A-Za-z0-9_-]+)\s*[\[\({"\']+(.+?)[\]\)"\']+\s*$', line)
        if m_node:
            nid, label = m_node.group(1), m_node.group(2)
            label = re.sub(r'<br\s*/?>\\?n?', ' · ', label, flags=re.IGNORECASE)
            nodes[nid] = label.strip()

    if not nodes:
        return None

    out = ['```d2', 'direction: right', '']
    # Deduplicate: use seen order from edges then any remaining nodes
    seen = []
    for frm, to in edges:
        for nid in (frm, to):
            if nid not in seen:
                seen.append(nid)
    for nid in nodes:
        if nid not in seen:
            seen.append(nid)

    # Emit node definitions
    for nid in seen:
        label = nodes.get(nid, nid)
        # Sanitize label
        label = label.replace('"', "'")
        # Determine shape
        if '✓' in label or 'Verify' in label.lower() or 'Done' in label.lower():
            shape = 'oval'
        elif nid in ('Plan', 'plan', 'Start', 'start'):
            shape = 'oval'
        else:
            shape = 'rectangle'
        safe_nid = re.sub(r'[^a-zA-Z0-9_]', '_', nid)
        out.append(f'{safe_nid}: "{label}" {{shape: {shape}}}')
    out.append('')

    # Emit edges (deduplicated)
    seen_edges = set()
    for frm, to in edges:
        safe_frm = re.sub(r'[^a-zA-Z0-9_]', '_', frm)
        safe_to  = re.sub(r'[^a-zA-Z0-9_]', '_', to)
        key = (safe_frm, safe_to)
        if key not in seen_edges:
            out.append(f'{safe_frm} -> {safe_to}')
            seen_edges.add(key)
    out.append('```')
    return '\n'.join(out)


def is_linear_mermaid(blk):
    return bool(LINEAR_TD_PAT.search(blk)) and 'subgraph' not in blk


removed = 0
converted = 0
skipped = 0

for root, dirs, files in os.walk(DOCS):
    dirs[:] = sorted([d for d in dirs if not d.startswith('.')])
    for fname in sorted(files):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(root, fname)
        txt = open(path, errors='replace').read()

        # Check if page has any linear Mermaid TD
        has_linear = any(is_linear_mermaid(b) for b in MERMAID_BLOCK.findall(txt))
        if not has_linear:
            continue

        has_d2_right = bool(D2_RIGHT_PAT.search(txt))
        new_txt = txt

        if has_d2_right:
            # Just remove the Mermaid TD block(s) — D2 right already exists
            def remove_if_linear(m):
                blk = m.group(1)
                if is_linear_mermaid(blk):
                    return ''
                return m.group(0)
            new_txt = MERMAID_BLOCK.sub(remove_if_linear, new_txt)
            if new_txt != txt:
                removed += 1
        else:
            # Replace Mermaid TD block with D2 right conversion
            def convert_or_keep(m):
                blk = m.group(1)
                if not is_linear_mermaid(blk):
                    return m.group(0)
                d2 = parse_mermaid_to_d2(blk)
                if d2:
                    return d2
                return m.group(0)  # parse failed, keep original
            new_txt = MERMAID_BLOCK.sub(convert_or_keep, new_txt)
            if new_txt != txt:
                converted += 1
            else:
                skipped += 1

        if new_txt != txt:
            # Clean up double-blank lines left by removed blocks
            new_txt = re.sub(r'\n{3,}', '\n\n', new_txt)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_txt)

print(f'Removed Mermaid TD (D2 already present): {removed}')
print(f'Converted Mermaid TD → D2 right:         {converted}')
print(f'Skipped (parse failed):                   {skipped}')
print(f'Total modified:                           {removed + converted}')
