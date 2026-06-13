#!/usr/bin/env python3
"""
KB site audit — 18 checks.

Usage:
    python3 scripts/site_audit.py          # run all checks, print summary
    python3 scripts/site_audit.py --full   # include full issue lists (no truncation)
"""

import os, re, sys, xml.etree.ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
ASSETS = os.path.join(DOCS, 'assets')
FULL = '--full' in sys.argv

results = {}


def check(n, name):
    results[n] = {'name': name, 'issues': []}
    return results[n]['issues']


def warn(issues, msg):
    issues.append(msg)


def all_md():
    for root, dirs, files in os.walk(DOCS):
        dirs[:] = sorted([d for d in dirs if not d.startswith('.')])
        for f in sorted(files):
            if f.endswith('.md'):
                yield os.path.join(root, f)


# ── Check 1: Cards vs filesystem ─────────────────────────────────────────────
# Directories that are intentionally card-free (asset, PWA, navigation-only)
CARDLESS_DIRS = {
    'learning-path',        # navigation page — appears via auto-nav, no card needed
    'offline',              # MkDocs offline plugin output dir
    'stats',                # MkDocs stats plugin output dir
    'images',               # personal/blog images — not KB content
    'icons',                # PWA icons (apple-touch-icon, icon-192, etc.)
    'overrides', 'stylesheets', 'assets', 'javascripts',
}

issues = check(1, 'Cards vs filesystem (orphans)')
for root, dirs, files in os.walk(DOCS):
    if 'index.md' not in files:
        continue
    parent_content = open(os.path.join(root, 'index.md')).read()
    for d in sorted(dirs):
        if d.startswith('.') or d in CARDLESS_DIRS:
            continue
        if not os.path.exists(os.path.join(root, d, 'index.md')):
            continue
        if f'href="{d}/"' not in parent_content:
            rel = os.path.relpath(root, DOCS)
            warn(issues, f'{rel}/index.md: no card for subdir "{d}/"')

# ── Check 2: Site-map links ───────────────────────────────────────────────────
issues = check(2, 'Site-map links')
smap = os.path.join(DOCS, 'site-map.md')
if os.path.exists(smap):
    smap_dir = os.path.dirname(smap)
    for i, line in enumerate(open(smap).readlines(), 1):
        m = re.search(r'\]\(([^)]+)\)', line)
        if not m:
            continue
        href = m.group(1)
        if href.startswith('http') or href.startswith('#'):
            continue
        target = os.path.normpath(os.path.join(smap_dir, href.rstrip('/')))
        if not os.path.exists(target) and not os.path.exists(target + '/index.md') and not os.path.exists(target + '.md'):
            warn(issues, f'site-map.md:{i}: broken link "{href}"')

# ── Check 3: Stale kb-summaries ───────────────────────────────────────────────
issues = check(3, 'Stale kb-summaries')
STALE_PATTERNS = [
    r'^[A-Z][A-Za-z\s]+ — [A-Z][a-z]+ (reference|overview|guide)\.$',
    r'^This section covers',
    r'^Coming soon',
]
for path in all_md():
    text = open(path).read()
    m = re.search(r'<div class="kb-summary">\s*([^\n<]{0,80})\s*</div>', text, re.DOTALL)
    if m:
        body = m.group(1).strip()
        for pat in STALE_PATTERNS:
            if re.match(pat, body, re.IGNORECASE):
                rel = os.path.relpath(path, REPO)
                warn(issues, f'{rel}: stale summary: "{body[:60]}"')

# ── Check 4: Home page descriptions ───────────────────────────────────────────
issues = check(4, 'Home page descriptions')
home = os.path.join(DOCS, 'index.md')
if os.path.exists(home):
    for s in re.findall(r'<span>([^<]{0,200})</span>', open(home).read()):
        if len(s.strip()) < 10:
            warn(issues, f'index.md: short/empty span: "{s.strip()}"')

# ── Check 5: Broken SVG references ────────────────────────────────────────────
issues = check(5, 'Broken SVG references')
for path in all_md():
    text = open(path).read()
    for m in re.finditer(r'(?:!\[.*?\]\(|<img[^>]+src=")([^)"]+\.svg)', text):
        svg_ref = m.group(1)
        if svg_ref.startswith('http'):
            continue
        svg_path = os.path.normpath(os.path.join(os.path.dirname(path), svg_ref))
        if not os.path.exists(svg_path):
            rel = os.path.relpath(path, REPO)
            warn(issues, f'{rel}: broken SVG ref "{svg_ref}"')

# ── Check 6: Orphaned directories (no index.md) ───────────────────────────────
# Asset/tooling dirs that legitimately have no index.md
NO_INDEX_OK = {'assets', 'javascripts', 'stylesheets', 'overrides', 'images', 'icons', 'offline', 'stats'}
issues = check(6, 'Orphaned directories')
for root, dirs, files in os.walk(DOCS):
    rel = os.path.relpath(root, DOCS)
    if rel == '.':
        continue
    top = rel.split(os.sep)[0]
    if top in NO_INDEX_OK:
        continue
    if 'index.md' not in files:
        warn(issues, f'{rel}: directory has no index.md')

# ── Check 7: Broken diagrams (box-drawing outside fences) ────────────────────
issues = check(7, 'Broken diagrams')
for path in all_md():
    lines = open(path).readlines()
    in_fence = False
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            in_fence = not in_fence
        if not in_fence and ('┌' in line or '│' in line or '└' in line):
            rel = os.path.relpath(path, REPO)
            warn(issues, f'{rel}:{i}: box-drawing char outside fence')

# ── Check 8: Dead card hrefs ──────────────────────────────────────────────────
issues = check(8, 'Dead card hrefs')
for path in all_md():
    content = open(path).read()
    page_dir = os.path.dirname(path)
    for m in re.finditer(r'href="([^"]+/)"', content):
        href = m.group(1)
        if href.startswith('http') or href.startswith('mailto'):
            continue
        target = os.path.join(page_dir, href)
        if not os.path.isdir(target):
            rel = os.path.relpath(path, REPO)
            warn(issues, f'{rel}: dead href="{href}"')

# ── Check 9: Diagram after kb-grid ───────────────────────────────────────────
issues = check(9, 'Diagram after kb-grid')
for path in all_md():
    content = open(path).read()
    grid_pos = content.find('<div class="kb-grid')
    if grid_pos == -1:
        continue
    after = content[grid_pos:]
    fence_m = re.search(r'^```text\n(?:[^\n]*\n)*?.*?[┌│└]', after, re.MULTILINE)
    if fence_m:
        rel = os.path.relpath(path, REPO)
        warn(issues, f'{rel}: ASCII diagram fence after kb-grid')

# ── Check 10: Missing kb-summary ─────────────────────────────────────────────
KNOWN_NO_SUMMARY = {'docs/index.md', 'docs/tags.md'}
issues = check(10, 'Missing kb-summary')
for path in all_md():
    if os.path.relpath(path, REPO) in KNOWN_NO_SUMMARY:
        continue
    content = open(path).read()
    if '<div class="kb-grid' in content and 'kb-summary' not in content:
        rel = os.path.relpath(path, REPO)
        warn(issues, f'{rel}: has kb-grid but no kb-summary')

# ── Check 11: Nav entries to missing files ────────────────────────────────────
issues = check(11, 'Nav entries to missing files')
mkdocs_yml = os.path.join(REPO, 'mkdocs.yml')
if os.path.exists(mkdocs_yml):
    for i, line in enumerate(open(mkdocs_yml).readlines(), 1):
        m = re.search(r':\s+(.+\.md)\s*$', line)
        if m:
            nav_path = os.path.join(REPO, 'docs', m.group(1).strip())
            if not os.path.exists(nav_path):
                warn(issues, f'mkdocs.yml:{i}: nav points to missing file "{m.group(1).strip()}"')

# ── Check 12: Missing H1 ─────────────────────────────────────────────────────
issues = check(12, 'Missing H1')
for path in all_md():
    if os.path.relpath(path, REPO) in KNOWN_NO_SUMMARY:
        continue
    content = open(path).read()
    if not re.search(r'^# .+', content, re.MULTILINE):
        rel = os.path.relpath(path, REPO)
        warn(issues, f'{rel}: no H1 heading')

# ── Check 13: Stub/empty pages ────────────────────────────────────────────────
KNOWN_STUB_OK = {'docs/tags.md'}
issues = check(13, 'Stub/empty pages')
for path in all_md():
    if os.path.relpath(path, REPO) in KNOWN_STUB_OK:
        continue
    lines = open(path).readlines()
    if len(lines) < 15:
        content = ''.join(lines)
        # architecture/index.md pages with SVG overviews are intentionally ~13L
        if path.endswith('architecture/index.md') and '![' in content:
            continue
        rel = os.path.relpath(path, REPO)
        warn(issues, f'{rel}: only {len(lines)} lines')

# ── Check 14: Diagram alignment ───────────────────────────────────────────────
issues = check(14, 'Diagram alignment')
for path in all_md():
    lines = open(path).readlines()
    in_fence = False
    fence_lines = []
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith('```text'):
            in_fence = True; fence_lines = []; continue
        if in_fence and s.startswith('```'):
            in_fence = False
            top = next(
                (l for l in fence_lines if not l[0].startswith(' ') and l[0].strip().startswith('┌')),
                None
            )
            if top and len(top[0].rstrip('\n')) != 105:
                rel = os.path.relpath(path, REPO)
                warn(issues, f'{rel}:{top[1]}: outer box width={len(top[0].rstrip())} (expected 105)')
            fence_lines = []
            continue
        if in_fence:
            fence_lines.append((line, i))

# ── Check 15: Redundancy ──────────────────────────────────────────────────────
issues = check(15, 'Redundancy / structural overlap')
for d in sorted(os.listdir(DOCS)):
    full = os.path.join(DOCS, d)
    if not os.path.isdir(full) or d.startswith('.'):
        continue
    count = sum(1 for _, _, files in os.walk(full) for f in files if f == 'index.md')
    if 1 < count < 5:
        warn(issues, f'docs/{d}/: only {count} pages — potential thin/redundant section')

# ── Check 16: SVG XML validity ────────────────────────────────────────────────
issues = check(16, 'SVG XML validity')
if os.path.isdir(ASSETS):
    svg_count = 0
    for fname in sorted(os.listdir(ASSETS)):
        if not fname.endswith('.svg'):
            continue
        svg_count += 1
        path = os.path.join(ASSETS, fname)
        try:
            ET.fromstring(open(path, errors='replace').read())
        except ET.ParseError as e:
            warn(issues, f'assets/{fname}: {e}')
    results[16]['svg_count'] = svg_count

# ── Check 17: VMware section consolidation ────────────────────────────────────
issues = check(17, 'VMware section consolidation')
vmware = os.path.join(DOCS, 'virtualization', 'vmware')
if os.path.isdir(vmware):
    # 17a: thin sub-sections
    for d in sorted(os.listdir(vmware)):
        full = os.path.join(vmware, d)
        if not os.path.isdir(full):
            continue
        count = sum(1 for _, _, files in os.walk(full) for f in files if f == 'index.md')
        if count < 5:
            warn(issues, f'vmware/{d}/: only {count} pages — thin section')
    # 17b: knowledge section proliferation (>3 is actionable; 4 is borderline but acceptable)
    knowledge_types = ['concepts', 'internals', 'topics', 'reference']
    found = [d for d in knowledge_types if os.path.isdir(os.path.join(vmware, d))]
    if len(found) > 3:
        warn(issues, f'vmware/: {len(found)} knowledge sections coexist: {found} — consider consolidating')
    # 17c: product pair duplication (srm vs vsphere-replication)
    srm_files = set(f for _,_,files in os.walk(os.path.join(vmware,'srm')) for f in files if f.endswith('.md'))
    vrep_files = set(f for _,_,files in os.walk(os.path.join(vmware,'vsphere-replication')) for f in files if f.endswith('.md'))
    overlap = srm_files & vrep_files
    if len(overlap) > 3:
        warn(issues, f'srm/ and vsphere-replication/ share {len(overlap)} file names — check for content duplication')

# ── Check 18: Mermaid node contrast ──────────────────────────────────────────
issues = check(18, 'Mermaid node contrast (light mode)')
def lum(hex_color):
    h = hex_color.lstrip('#')
    if len(h) == 3: h = ''.join(c*2 for c in h)
    if len(h) != 6: return 0
    r, g, b = int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255
    def lin(v): return v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4
    return 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b)

light_fills = {}
for path in all_md():
    text = open(path).read()
    for m in re.finditer(r'classDef\s+\w+\s+fill:(#[0-9a-fA-F]{3,6})', text):
        hx = m.group(1)
        if lum(hx) > 0.25:
            rel = os.path.relpath(path, REPO)
            light_fills.setdefault(hx, []).append(rel)
for hx, paths in light_fills.items():
    warn(issues, f'Light fill {hx} (lum={lum(hx):.3f}) in {len(paths)} files — white text forced, invisible in light mode')
    for p in paths[:2]:
        warn(issues, f'  e.g. {p}')
    if len(paths) > 2:
        warn(issues, f'  ... and {len(paths)-2} more')

# ── Report ────────────────────────────────────────────────────────────────────
print('\n' + '='*70)
print('KB SITE AUDIT REPORT')
print('='*70 + '\n')

clean = 0
for n in sorted(results):
    r = results[n]
    issues = r['issues']
    extra = ''
    if n == 16 and 'svg_count' in r:
        extra = f' — {r["svg_count"]} SVGs checked'
    status = f'✅ Clean{extra}' if not issues else f'❌ {len(issues)} issue(s)'
    print(f'Check {n:2d}: {r["name"]}')
    print(f'         {status}')
    if issues:
        limit = None if FULL else 12
        for issue in issues[:limit]:
            print(f'         {issue}')
        if limit and len(issues) > limit:
            print(f'         ... and {len(issues)-limit} more (run --full to see all)')
    print()
    if not issues:
        clean += 1

print('='*70)
print(f'SUMMARY: {clean}/{len(results)} checks clean')
print('='*70 + '\n')
sys.exit(0 if clean == len(results) else 1)
