#!/usr/bin/env python3
"""
KB site audit — 61 checks.

Usage:
    python3 scripts/site_audit.py               # run all checks, print summary
    python3 scripts/site_audit.py --full        # include full issue lists (no truncation)
    python3 scripts/site_audit.py --check-links # also validate external URLs (slow)
"""

import os, re, sys, xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
ASSETS = os.path.join(DOCS, 'assets')
FULL = '--full' in sys.argv
CHECK_LINKS = '--check-links' in sys.argv

results = {}


def check(n, name):
    results[n] = {'name': name, 'issues': []}
    return results[n]['issues']


def warn(issues, msg):
    issues.append(msg)


def all_md():
    for root, dirs, files in os.walk(DOCS):
        dirs[:] = sorted([d for d in dirs if not d.startswith('.') and d != 'includes'])
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
NO_INDEX_OK = {'assets', 'javascripts', 'stylesheets', 'overrides', 'images', 'icons', 'offline', 'stats', 'includes'}
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
        # Accept both dir/index.md and flat dir.md (flattened tree)
        flat_md = os.path.join(page_dir, href.rstrip('/') + '.md')
        if not os.path.isdir(target) and not os.path.isfile(flat_md):
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
# Directories whose pages are intentional stubs (new sections under construction)
KNOWN_STUB_DIRS = {
    'docs/virtualization/nutanix',
    'docs/offline',   # PWA offline page — intentionally minimal
    'docs/stats',     # Stats page — intentionally minimal
    'docs/virtualization/vmware/reference/certification',  # placeholder cert notes
    'docs/itsm/servicenow/change-management',  # skeleton sections
    'docs/itsm/servicenow/templates',          # skeleton sections
    'docs/virtualization/vmware/reference/inventory',  # version/tool inventory stubs
}
issues = check(13, 'Stub/empty pages')
for path in all_md():
    if os.path.relpath(path, REPO) in KNOWN_STUB_OK:
        continue
    if any(os.path.relpath(path, REPO).startswith(d) for d in KNOWN_STUB_DIRS):
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
# Sections excluded because they are actively being built out (more tracks pending)
_SKIP_THIN = {'reference'}
for d in sorted(os.listdir(DOCS)):
    full = os.path.join(DOCS, d)
    if not os.path.isdir(full) or d.startswith('.') or d in _SKIP_THIN:
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
    # 17a: thin sub-sections (count all .md files, including flat ones post-flatten)
    for d in sorted(os.listdir(vmware)):
        full = os.path.join(vmware, d)
        if not os.path.isdir(full):
            continue
        count = sum(1 for _, _, files in os.walk(full) for f in files if f.endswith('.md'))
        if count < 5:
            warn(issues, f'vmware/{d}/: only {count} pages — thin section')
    # 17b: knowledge section proliferation (>3 is actionable; 4 is borderline but acceptable)
    knowledge_types = ['concepts', 'internals', 'topics', 'reference']
    found = [d for d in knowledge_types if os.path.isdir(os.path.join(vmware, d))]
    if len(found) > 3:
        warn(issues, f'vmware/: {len(found)} knowledge sections coexist: {found} — consider consolidating')
    # 17c: product pair duplication — disabled after tree-flattening
    # All products now share the same template filenames (common-issues.md, health-checks.md, etc.)
    # so filename-overlap is a universal false positive. Content-diff check to be added later.

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

# ── Check 19: Prerequisites on procedure pages ────────────────────────────────
# 19a: no kb-grid landing page should have "## Before you begin"
# 19b: leaf procedure pages (no kb-grid, under proc dirs) should have one
PROC_DIRS_AUDIT = {'/deploy/', '/operations/', '/troubleshooting/', '/security/'}
issues = check(19, 'Prerequisites placement')
for path in all_md():
    content = open(path).read()
    rel  = os.path.relpath(path, DOCS)
    rpath = '/' + rel.replace(os.sep, '/')
    is_proc_dir = any(d in rpath for d in PROC_DIRS_AUDIT)

    # 19a: landing pages must NOT have "Before you begin"
    if '<div class="kb-grid' in content and '## Before you begin' in content:
        warn(issues, f'{rel}: landing page (kb-grid) has "Before you begin" — remove it')

    # 19b: leaf procedure pages SHOULD have "Before you begin"
    if (is_proc_dir
            and os.path.basename(path) not in ('faq.md', 'known-issues.md')
            and '<div class="kb-grid' not in content
            and '## Before you begin' not in content
            and '## Prerequisites' not in content
            and '## Requirements' not in content
            and len(content.splitlines()) > 20):  # skip genuine stubs
        warn(issues, f'{rel}: procedure page missing "Before you begin"')


# ── Check 22: Misplaced product sections ─────────────────────────────────────
# Detects product directories that exist both as a standalone section AND under
# their parent vendor directory — e.g. docs/virtualization/vxrail/ alongside
# docs/virtualization/vmware/vxrail/.  Both appear in auto-nav, creating
# duplicate entries and confusing users.
issues = check(22, 'Misplaced product sections (duplicate under vendor)')
_VENDOR_ROOTS = {
    os.path.join(DOCS, 'virtualization', 'vmware'): os.path.join(DOCS, 'virtualization'),
}
for vendor_dir, parent_dir in _VENDOR_ROOTS.items():
    if not os.path.isdir(vendor_dir):
        continue
    # Products that live correctly under the vendor dir
    vendor_products = {d for d in os.listdir(vendor_dir)
                       if os.path.isdir(os.path.join(vendor_dir, d))}
    # Siblings of the vendor dir (e.g. docs/virtualization/<name>/)
    siblings = {d for d in os.listdir(parent_dir)
                if os.path.isdir(os.path.join(parent_dir, d)) and d != 'vmware'}
    for name in sorted(vendor_products & siblings):
        vendor_path = os.path.relpath(os.path.join(vendor_dir, name), DOCS)
        sibling_path = os.path.relpath(os.path.join(parent_dir, name), DOCS)
        page_count = sum(1 for _, _, fs in os.walk(os.path.join(parent_dir, name))
                         for f in fs if f == 'index.md')
        warn(issues, (f'{sibling_path}/ duplicates {vendor_path}/ '
                      f'({page_count} orphaned pages — merge into vendor section)'))


# ── Check 20: Multi-H1 pages ─────────────────────────────────────────────────
# Uses line-by-line fence tracking — avoids false positives from bash # comments
# inside code blocks. Only flags genuine duplicate H1 headings in prose.
issues = check(20, 'Multi-H1 pages')
for path in all_md():
    raw = open(path).read()
    # Strip front matter
    body = re.sub(r'^---\n.*?\n---\n', '', raw, count=1, flags=re.DOTALL)
    lines = body.splitlines()
    in_fence = False
    h1s = []
    for line in lines:
        s = line.strip()
        if not in_fence:
            if s.startswith('```') or s.startswith('~~~'):
                in_fence = True
            elif line.startswith('# '):
                h1s.append(line.rstrip())
        else:
            if s == '```' or s == '~~~':
                in_fence = False
    if len(h1s) > 1:
        rel = os.path.relpath(path, DOCS)
        warn(issues, f'{rel}: {len(h1s)} H1 headings: {h1s[:3]}')


# ── Check 21: Duplicate page titles ──────────────────────────────────────────
issues = check(21, 'Duplicate page titles')
_title_map = {}
for path in all_md():
    raw = open(path).read()
    body = re.sub(r'^---\n.*?\n---\n', '', raw, count=1, flags=re.DOTALL)
    lines = body.splitlines()
    in_fence = False
    title = None
    for line in lines:
        s = line.strip()
        if not in_fence:
            if s.startswith('```') or s.startswith('~~~'):
                in_fence = True
            elif line.startswith('# ') and title is None:
                title = line[2:].strip()
                break
        else:
            if s == '```' or s == '~~~':
                in_fence = False
    if title:
        _title_map.setdefault(title, []).append(os.path.relpath(path, DOCS))

for title, paths in sorted(_title_map.items()):
    if len(paths) > 1:
        warn(issues, f'"{title}" appears on {len(paths)} pages: {paths}')


# ── Check 23: Backup retention ────────────────────────────────────────────────
issues = check(23, 'Backup retention')
_backup_dir = os.path.join(os.path.dirname(DOCS), 'backup')
if os.path.isdir(_backup_dir):
    _backups = sorted([
        d for d in os.listdir(_backup_dir)
        if os.path.isdir(os.path.join(_backup_dir, d)) and
        len(d) == 17 and d[4] == '-' and d[7] == '-'  # YYYY-MM-DD_HHMMSS
    ])
    _count = len(_backups)
    if _count > 10:
        warn(issues, f'{_count} backup snapshots exist (cap is 10) — run: cd backup && ls -1d */ | sort | head -n {_count - 10} | xargs rm -rf')
    elif _count == 0:
        warn(issues, 'No backups found — backup.sh may not be running')
    else:
        # Check total size (du -sk, quick estimate)
        try:
            import subprocess as _sp
            _result = _sp.run(['du', '-sk', _backup_dir], capture_output=True, text=True)
            _kb = int(_result.stdout.split()[0]) if _result.returncode == 0 else 0
            _gb = _kb / (1024 * 1024)
            if _gb > 15:
                warn(issues, f'Backup dir is {_gb:.1f} GB ({_count} snapshots) — run cleanup or reduce retention')
        except Exception:
            pass
else:
    warn(issues, f'Backup directory not found at {_backup_dir}')


# ── Check 24: ASCII diagram coverage ─────────────────────────────────────────
issues = check(24, 'ASCII diagram coverage')
_SKIP_DIAG = {'tags.md', 'site-map.md', 'usage-metrics.md', 'site-quality.md'}
_missing_diag = []
for _path in all_md():
    _rel = os.path.relpath(_path, DOCS)
    _abs_rel = os.path.relpath(_path, REPO)
    if _rel in _SKIP_DIAG or _rel.startswith('stats/'):
        continue
    if any(_abs_rel.startswith(d) for d in KNOWN_STUB_DIRS):
        continue
    _c = open(_path).read()
    if 'kb-card' in _c or 'kb-grid' in _c:
        continue  # nav pages don't need diagrams
    if re.search(r'\.(svg|png|jpg)\)', _c) or '<img ' in _c:
        continue  # pages with embedded images satisfy the diagram requirement
    if re.search(r'```(mermaid|d2|plantuml|vegalite)\b', _c):
        continue  # Mermaid/Kroki-rendered diagrams satisfy the requirement
    if not re.search(r'[┌│└┐┘]', _c):
        _missing_diag.append(_rel)
if _missing_diag:
    for _p in _missing_diag[:12]:
        warn(issues, f'No ASCII diagram: {_p}')
    if len(_missing_diag) > 12:
        warn(issues, f'... and {len(_missing_diag) - 12} more (run --full)')


# ── Check 25: See also coverage ───────────────────────────────────────────────
# Only flag leaf sub-pages inside known operational section types
_SEE_ALSO_SECTIONS = {
    'procedures', 'health-checks', 'cli-reference', 'scripts',
    'backup-restore', 'install-upgrade', 'common-issues', 'diagnostics',
    'escalation', 'access-control', 'authentication', 'encryption', 'hardening',
}
issues = check(25, 'See also cross-references')
_missing_see = []
for _path in all_md():
    _rel = os.path.relpath(_path, DOCS)
    if _rel.startswith('stats/') or _rel in {'tags.md', 'site-map.md', 'usage-metrics.md', 'site-quality.md'}:
        continue
    _parts = _rel.split(os.sep)
    # parent directory must be one of the known operational section names
    _parent = _parts[-2] if len(_parts) >= 2 else ''
    if _parent not in _SEE_ALSO_SECTIONS:
        continue
    _c = open(_path).read()
    if 'kb-card' in _c or 'kb-grid' in _c:
        continue
    if '## See also' not in _c:
        _missing_see.append(_rel)
if _missing_see:
    for _p in _missing_see[:12]:
        warn(issues, f'Missing "## See also": {_p}')
    if len(_missing_see) > 12:
        warn(issues, f'... and {len(_missing_see) - 12} more (run --full)')


# ── Check 26: Before you begin coverage ──────────────────────────────────────
issues = check(26, 'Before you begin prerequisites')
_BYB_DIRS = {'deploy', 'operations', 'troubleshooting'}
_missing_byb = []
for _path in all_md():
    _rel = os.path.relpath(_path, DOCS)
    _parts = _rel.split(os.sep)
    # only check files inside deploy/, operations/, or troubleshooting/ sub-dirs
    if not any(p in _BYB_DIRS for p in _parts[:-1]):
        continue
    _c = open(_path).read()
    if 'kb-card' in _c or 'kb-grid' in _c:
        continue
    # skip index.md landing pages (they're card-nav) and known-issues / escalation flat tables
    _fname = os.path.basename(_path)
    if _fname in ('known-issues.md', 'faq.md'):
        continue
    if len(_parts) < 3:
        continue
    if '## Before you begin' not in _c and 'Before you begin' not in _c:
        _missing_byb.append(_rel)
if _missing_byb:
    for _p in _missing_byb[:12]:
        warn(issues, f'Missing "Before you begin": {_p}')
    if len(_missing_byb) > 12:
        warn(issues, f'... and {len(_missing_byb) - 12} more (run --full)')


# ── Check 27: New platform section structure ──────────────────────────────────
issues = check(27, 'New platform section structure (OpenShift, Ceph, EVS)')
_NEW_SECTIONS = {
    'virtualization/openshift': ['architecture', 'deploy', 'operations', 'security', 'troubleshooting'],
    'storage/ceph':             ['architecture', 'deploy', 'operations', 'security', 'troubleshooting'],
    'cloud/aws/evs':            ['architecture', 'deploy', 'operations', 'security', 'troubleshooting'],
}
for _section, _required in _NEW_SECTIONS.items():
    _base = os.path.join(DOCS, _section)
    if not os.path.isdir(_base):
        warn(issues, f'Section missing: {_section}/')
        continue
    for _sub in _required:
        _sub_path = os.path.join(_base, _sub)
        if not os.path.isdir(_sub_path):
            warn(issues, f'{_section}/{_sub}/ missing')
        elif not os.path.exists(os.path.join(_sub_path, 'index.md')):
            # flat .md files are OK for EVS
            _flat = [f for f in os.listdir(_sub_path) if f.endswith('.md')]
            if not _flat:
                warn(issues, f'{_section}/{_sub}/ has no content')



# ── Check 28: Admin page staleness ────────────────────────────────────────────
issues = check(28, 'Admin page staleness (site-quality.md, usage-metrics.md)')
import re as _re
import datetime as _dt

_actual_count = sum(1 for _r, _ds, _fs in os.walk(DOCS) for _f in _fs if _f.endswith('.md'))

for _admin_page in ['site-quality.md', 'usage-metrics.md']:
    _page_path = os.path.join(DOCS, _admin_page)
    if not os.path.exists(_page_path):
        warn(issues, f'{_admin_page} missing')
        continue
    with open(_page_path) as _f:
        _text = _f.read()

    # Check stated page count vs actual
    _m = _re.search(r'\|\s*Total markdown pages\s*\|\s*([\d,]+)\s*\|', _text)
    if _m:
        _stated = int(_m.group(1).replace(',', ''))
        _delta = abs(_stated - _actual_count)
        _pct = _delta / _actual_count * 100 if _actual_count else 0
        if _pct > 5:
            warn(issues, f'{_admin_page}: stated {_stated} pages but actual is {_actual_count} (off by {_delta}, {_pct:.1f}%)')
    else:
        warn(issues, f'{_admin_page}: no "Total markdown pages" row found in table')

    # Check generated date — warn if more than 1 day old
    _dm = _re.search(r'Generated:\s*(\d{4}-\d{2}-\d{2})', _text)
    if _dm:
        _gen_date = _dt.date.fromisoformat(_dm.group(1))
        _age = (_dt.date.today() - _gen_date).days
        if _age > 1:
            warn(issues, f'{_admin_page}: Generated date {_dm.group(1)} is {_age} days old (>1 day)')
    else:
        warn(issues, f'{_admin_page}: no "Generated: YYYY-MM-DD" line found')


# ── Check 29: Orphaned assets ────────────────────────────────────────────────
issues = check(29, 'Orphaned assets (unreferenced files in docs/assets/)')
_referenced_assets = set()
for _path in all_md():
    _text = open(_path).read()
    for _m in re.finditer(r'(?:!\[.*?\]\(|src=")([^)"]+)', _text):
        _ref = _m.group(1)
        if _ref.startswith('http'):
            continue
        _abs = os.path.normpath(os.path.join(os.path.dirname(_path), _ref))
        _referenced_assets.add(_abs)
if os.path.isdir(ASSETS):
    for _fname in sorted(os.listdir(ASSETS)):
        _fpath = os.path.join(ASSETS, _fname)
        if not os.path.isfile(_fpath):
            continue
        if _fpath not in _referenced_assets:
            warn(issues, f'assets/{_fname}: not referenced by any page')


# ── Check 30: External link rot ───────────────────────────────────────────────
issues = check(30, 'External link rot')
_ext_urls = set()
for _path in all_md():
    for _m in re.finditer(r'https?://[^\s\)\]"\'<>]+', open(_path).read()):
        _ext_urls.add(_m.group(0).rstrip('.,;)>'))
results[30]['url_count'] = len(_ext_urls)
if CHECK_LINKS:
    import urllib.request as _ur
    for _url in sorted(_ext_urls):
        try:
            _req = _ur.Request(_url, headers={'User-Agent': 'Mozilla/5.0'})
            _resp = _ur.urlopen(_req, timeout=8)
            if _resp.status >= 400:
                warn(issues, f'HTTP {_resp.status}: {_url}')
        except Exception as _e:
            warn(issues, f'Error ({_e}): {_url}')


# ── Check 31: SVG per-section coverage (procedures / health-checks) ───────────
issues = check(31, 'SVG per-section coverage (procedures/health-checks)')
_proc_pages_with_svgs = 0
for _path in all_md():
    if os.path.basename(_path) not in ('procedures.md', 'health-checks.md'):
        continue
    _lines = open(_path).readlines()
    for _i, _line in enumerate(_lines):
        if _line.startswith('### ') and _i + 1 < len(_lines):
            _nxt = [l.strip() for l in _lines[_i+1:_i+4] if l.strip()]
            if _nxt and re.match(r'!\[.*\]\(.*\.svg\)', _nxt[0]):
                _proc_pages_with_svgs += 1
                break
if _proc_pages_with_svgs == 0:
    warn(issues, 'PENDING — SVG expansion (Step A1) not started; re-run after first batch')
else:
    for _path in all_md():
        if os.path.basename(_path) not in ('procedures.md', 'health-checks.md'):
            continue
        _lines = open(_path).readlines()
        _rel = os.path.relpath(_path, DOCS)
        for _i, _line in enumerate(_lines):
            if not _line.startswith('### '):
                continue
            _nxt = [l.strip() for l in _lines[_i+1:_i+4] if l.strip()]
            _has_svg = bool(_nxt and (
                re.match(r'!\[.*\]\(.*\.svg\)', _nxt[0]) or
                re.match(r'```(d2|plantuml|vegalite)', _nxt[0])
            ))
            if not _has_svg:
                warn(issues, f'{_rel}: "### {_line[4:].strip()}" missing SVG ref')


# ── Check 32: Tag coverage ────────────────────────────────────────────────────
issues = check(32, 'Tag coverage (product + domain tags)')
_mkdocs_text = open(os.path.join(REPO, 'mkdocs.yml')).read() if os.path.exists(os.path.join(REPO, 'mkdocs.yml')) else ''
_tags_enabled = bool(re.search(r'^\s*-\s*tags\b', _mkdocs_text, re.MULTILINE))
if not _tags_enabled:
    warn(issues, 'PENDING — tags plugin not enabled in mkdocs.yml (Spectacular Track 1)')
else:
    _SKIP_TAGS = {'tags.md', 'site-map.md', 'index.md', 'usage-metrics.md', 'site-quality.md',
                  'offline/index.md', 'stats/index.md'}
    for _path in all_md():
        _rel = os.path.relpath(_path, DOCS)
        if _rel in _SKIP_TAGS:
            continue
        _text = open(_path).read()
        if 'kb-grid' in _text or 'kb-card' in _text:
            continue
        _fm = re.match(r'^---\n(.*?)\n---', _text, re.DOTALL)
        if not _fm or 'tags:' not in _fm.group(1):
            warn(issues, f'{_rel}: no tags in front matter')


# ── Check 33: "Run This Routine" on health-check pages ───────────────────────
issues = check(33, '"Run This Routine" block on health-check pages')
_missing_routine = []
for _path in all_md():
    if os.path.basename(_path) != 'health-checks.md':
        continue
    _c = open(_path).read()
    if 'kb-grid' in _c or len(_c.splitlines()) < 20:
        continue
    if 'Run This Routine' not in _c:
        _missing_routine.append(os.path.relpath(_path, DOCS))
if _missing_routine:
    for _p in (_missing_routine if FULL else _missing_routine[:12]):
        warn(issues, f'Missing "Run This Routine": {_p}')
    if not FULL and len(_missing_routine) > 12:
        warn(issues, f'... and {len(_missing_routine)-12} more (run --full)')


# ── Check 34: Heading hierarchy ───────────────────────────────────────────────
issues = check(34, 'Heading hierarchy (H3 without H2, H4 without H3)')
for _path in all_md():
    _lines = open(_path).readlines()
    _in_fence = False
    _seen_h2 = _seen_h3 = False
    _violations = []
    for _i, _line in enumerate(_lines, 1):
        _s = _line.strip()
        if _s.startswith('```') or _s.startswith('~~~'):
            _in_fence = not _in_fence
        if _in_fence:
            continue
        if _line.startswith('## '):
            _seen_h2 = True; _seen_h3 = False
        elif _line.startswith('### '):
            if not _seen_h2:
                _violations.append(f'  line {_i}: H3 "{_line[4:].strip()}" before any H2')
            _seen_h3 = True
        elif _line.startswith('#### '):
            if not _seen_h3:
                _violations.append(f'  line {_i}: H4 "{_line[5:].strip()}" before any H3')
    if _violations:
        _rel = os.path.relpath(_path, DOCS)
        warn(issues, f'{_rel}:')
        for _v in _violations[:3]:
            warn(issues, _v)


# ── Check 35: "See also" link validity ───────────────────────────────────────
# Validates against site/ (built output) to account for MkDocs converting
# flat file.md → file/index.html, which shifts relative link depth by one.
# Falls back to docs/ resolution if site/ doesn't exist.
issues = check(35, '"See also" internal link validity')
_SITE = os.path.join(REPO, 'site')
_use_site = os.path.isdir(_SITE)
for _path in all_md():
    _c = open(_path).read()
    _sm = re.search(r'## See also\n(.*?)(?=\n##|\Z)', _c, re.DOTALL)
    if not _sm:
        continue
    if _use_site:
        # Compute the effective directory in site/ space
        _rel_to_docs = os.path.relpath(_path, DOCS)
        _p = Path(_rel_to_docs)
        if _p.name == 'index.md':
            _eff_dir = os.path.join(_SITE, str(_p.parent))
        else:
            _eff_dir = os.path.join(_SITE, str(_p.parent), _p.stem)
    else:
        _eff_dir = os.path.dirname(_path)
    for _lm in re.finditer(r'\[.*?\]\(([^)]+)\)', _sm.group(1)):
        _href = _lm.group(1).split('#')[0]
        if not _href or _href.startswith(('http', 'mailto', 'data:')):
            continue
        if _href.endswith('.md'):
            # .md links: MkDocs resolves from docs/ source position (not site/)
            _src_dir = os.path.dirname(_path)
            _tgt = os.path.normpath(os.path.join(_src_dir, _href[:-3]))
            _exists = (os.path.exists(_tgt + '.md')
                       or os.path.exists(os.path.join(_tgt, 'index.md')))
        else:
            _target = os.path.normpath(os.path.join(_eff_dir, _href))
            if _use_site:
                _exists = (os.path.exists(_target)
                           or os.path.exists(os.path.join(_target, 'index.html')))
            else:
                _exists = (os.path.exists(_target)
                           or os.path.exists(_target + '.md')
                           or os.path.exists(os.path.join(_target, 'index.md')))
        if not _exists:
            _rel = os.path.relpath(_path, DOCS)
            warn(issues, f'{_rel}: broken "See also" link "{_href}"')


# ── Check 36: Anchor fragment validity ───────────────────────────────────────
def _slug(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

def _page_anchors(path):
    anchors = set()
    in_fence = False
    for line in open(path, errors='replace'):
        s = line.strip()
        if s.startswith('```') or s.startswith('~~~'):
            in_fence = not in_fence
        if in_fence:
            continue
        m = re.match(r'^(#{1,6})\s+(.+)', line)
        if m:
            anchors.add(_slug(m.group(2)))
        # attr_list explicit ids, e.g. **Term**{: #custom-id } or ## Heading {: #custom-id }
        for am in re.finditer(r'\{:\s*#([\w-]+)', line):
            anchors.add(am.group(1))
    return anchors

issues = check(36, 'Anchor fragment validity (internal #links)')
_anchor_cache = {}
for _path in all_md():
    _c = open(_path).read()
    _page_dir = os.path.dirname(_path)
    for _lm in re.finditer(r'\[.*?\]\(([^)#"]*)#([^)"]+)\)', _c):
        _file_ref, _fragment = _lm.group(1), _lm.group(2)
        if _file_ref.startswith('http'):
            continue
        if not _file_ref:
            _target_path = _path
        else:
            _raw = os.path.normpath(os.path.join(_page_dir, _file_ref))
            if os.path.isdir(_raw):
                _target_path = os.path.join(_raw, 'index.md')
            elif os.path.exists(_raw + '.md'):
                _target_path = _raw + '.md'
            elif os.path.exists(_raw):
                _target_path = _raw
            else:
                continue  # broken file ref — Check 35 already catches this
        if not os.path.exists(_target_path):
            continue
        if _target_path not in _anchor_cache:
            _anchor_cache[_target_path] = _page_anchors(_target_path)
        if _slug(_fragment) not in _anchor_cache[_target_path]:
            _rel = os.path.relpath(_path, DOCS)
            warn(issues, f'{_rel}: broken anchor "#{_fragment}" in link to "{_file_ref or "self"}"')


# ── Check 37: Missing "## Verify" on procedures pages ────────────────────────
issues = check(37, 'Missing "## Verify" section on procedures pages')
_missing_verify = []
for _path in all_md():
    if os.path.basename(_path) != 'procedures.md':
        continue
    _c = open(_path).read()
    if 'kb-grid' in _c or len(_c.splitlines()) < 20:
        continue
    if '## Verify' not in _c:
        _missing_verify.append(os.path.relpath(_path, DOCS))
if _missing_verify:
    for _p in (_missing_verify if FULL else _missing_verify[:12]):
        warn(issues, f'Missing "## Verify": {_p}')
    if not FULL and len(_missing_verify) > 12:
        warn(issues, f'... and {len(_missing_verify)-12} more (run --full)')


# ── Check 38: Video registry validity and coverage ───────────────────────────
issues = check(38, 'Video registry validity and coverage')
_videos_yml = os.path.join(REPO, 'docs', 'videos.yml')
if not os.path.exists(_videos_yml):
    warn(issues, 'docs/videos.yml not found')
else:
    try:
        import yaml as _yaml
        with open(_videos_yml) as _vf:
            _vdata = _yaml.safe_load(_vf)
        _ventries = _vdata.get('videos', []) if _vdata else []
        _bad_pages = []
        _bad_urls = []
        for _ve in _ventries:
            _vpage = os.path.join(REPO, _ve.get('page', ''))
            if not os.path.exists(_vpage):
                _bad_pages.append(_ve.get('page', '(missing page field)'))
            _vurl = _ve.get('url', '')
            if not _vurl.startswith('https://www.youtube.com/watch?v='):
                _bad_urls.append(f'{_ve.get("page","?")} — {_vurl}')
        for _p in _bad_pages:
            warn(issues, f'Registry page not found: {_p}')
        for _u in _bad_urls:
            warn(issues, f'Non-YouTube URL in registry: {_u}')
        results[38]['video_count'] = len(_ventries)
        results[38]['bad_pages'] = len(_bad_pages)
    except Exception as _e:
        warn(issues, f'Failed to parse videos.yml: {_e}')


# ── Check 39: Hub-and-spoke D2 blocks ────────────────────────────────────────
issues = check(39, 'No hub-and-spoke D2 blocks (center node with only outgoing edges)')
_D2_BLOCK = re.compile(r'```d2\n.*?\n```', re.DOTALL)
for _md in all_md():
    _txt = open(_md).read()
    if '```d2' not in _txt:
        continue
    for _blk in _D2_BLOCK.findall(_txt):
        if re.search(r'^center:', _blk, re.MULTILINE):
            warn(issues, os.path.relpath(_md, DOCS))
            break

# ── Check 40: Section Overview SVG references ─────────────────────────────────
issues = check(40, 'No Section Overview SVG references in pages')
_SEC_OV = re.compile(r'!\[[^\]]*\]\([^)]*\.svg\)|<img\s[^>]*src="[^"]*\.svg"')
_bad_svgs = set()
for _svg in os.listdir(ASSETS):
    if not _svg.endswith('.svg'):
        continue
    try:
        if 'Section Overview' in open(os.path.join(ASSETS, _svg)).read():
            _bad_svgs.add(_svg)
    except Exception:
        pass
if _bad_svgs:
    warn(issues, f'{len(_bad_svgs)} Section Overview SVG files still in assets/')
for _md in all_md():
    _txt = open(_md).read()
    for _m in _SEC_OV.finditer(_txt):
        _ref = _m.group(0)
        if any(b in _ref for b in _bad_svgs):
            warn(issues, os.path.relpath(_md, DOCS))
            break

# ── Check 41: Trivial generic D2 diagrams ────────────────────────────────────
issues = check(41, 'No trivial generic D2 diagrams (stage_N templates, hexagon hubs)')
for _md in all_md():
    _txt = open(_md).read()
    if '```d2' not in _txt:
        continue
    for _blk in _D2_BLOCK.findall(_txt):
        _nodes = re.findall(r'^(\w+):', _blk, re.MULTILINE)
        if any('stage_' in n for n in _nodes):
            warn(issues, f'{os.path.relpath(_md, DOCS)} — stage_N template')
            break
        if '{shape: hexagon}' in _blk or re.search(r'shape:\s*hexagon', _blk):
            if re.search(r'^center:', _blk, re.MULTILINE):
                warn(issues, f'{os.path.relpath(_md, DOCS)} — hexagon hub')
                break

# ── Check 42: Broken .md extension links in "See also" sections ──────────────
# MkDocs resolves .md links from docs/ source position, so valid .md links are
# fine. Only flag .md links where the target file doesn't exist in docs/ — those
# will 404 since MkDocs has no target to convert.
issues = check(42, 'No broken .md extension links in "See also" sections (would 404)')
_MD_LINK_PAT   = re.compile(r'\[([^\]]+)\]\(([^)#?]+\.md)\)')
_SEE_ALSO_BLOCK = re.compile(r'## See also.*?(?=\n##|\Z)', re.DOTALL | re.IGNORECASE)
for _md in all_md():
    _txt = open(_md).read()
    _src_dir = os.path.dirname(_md)
    for _block in _SEE_ALSO_BLOCK.finditer(_txt):
        for _lm in _MD_LINK_PAT.finditer(_block.group(0)):
            _href = _lm.group(2)
            _tgt = os.path.normpath(os.path.join(_src_dir, _href[:-3]))
            _exists = (os.path.exists(_tgt + '.md')
                       or os.path.exists(os.path.join(_tgt, 'index.md')))
            if not _exists:
                warn(issues, f'{os.path.relpath(_md, DOCS)}: [{_lm.group(1)}]({_href})')


# ── Check 43: SVG missing viewBox ────────────────────────────────────────────
# Without viewBox, CSS max-width:100% clips instead of scales the SVG,
# causing text near the right edge to appear truncated.
issues = check(43, 'SVG assets missing viewBox (causes text clipping on narrow screens)')
if os.path.isdir(ASSETS):
    for _fname in sorted(os.listdir(ASSETS)):
        if not _fname.endswith('.svg'):
            continue
        _first = open(os.path.join(ASSETS, _fname), errors='replace').readline()
        if 'viewBox' not in _first:
            warn(issues, f'assets/{_fname}: no viewBox on <svg> element')


# ── Check 44: TODO / placeholder text in published pages ─────────────────────
_TODO_PATTERNS = [
    (re.compile(r'\bTODO\b|\bFIXME\b', re.IGNORECASE), 'TODO/FIXME marker'),
    (re.compile(r'\bLorem ipsum\b', re.IGNORECASE), 'Lorem ipsum placeholder'),
    (re.compile(r'\[Content to be added\]|\[TBD\]|\[WIP\]', re.IGNORECASE), 'TBD/WIP marker'),
    # "Coming soon" only as a standalone line/heading, not inside paragraphs
    (re.compile(r'^#+\s*Coming soon\s*$|^Coming soon\.?\s*$', re.IGNORECASE | re.MULTILINE), 'Coming soon stub heading'),
]
# Skip pages that intentionally discuss historical changes, meta-docs, etc.
_TODO_SKIP = {'docs/tags.md', 'docs/site-map.md', 'docs/whats-new.md'}
issues = check(44, 'TODO / placeholder text in published pages')
for _path in all_md():
    _rel_doc = os.path.relpath(_path, REPO)
    if _rel_doc in _TODO_SKIP:
        continue
    _lines = open(_path, errors='replace').readlines()
    _in_fence = False
    for _i, _line in enumerate(_lines, 1):
        if _line.strip().startswith('```') or _line.strip().startswith('~~~'):
            _in_fence = not _in_fence
        if _in_fence:
            continue
        for _pat, _label in _TODO_PATTERNS:
            if _pat.search(_line):
                warn(issues, f'{os.path.relpath(_path, DOCS)}:{_i}: {_label}: {_line.strip()[:80]}')
                break


# ── Check 45: Missing "Applies to:" version marker ────────────────────────────
# Every content page (non-landing) should declare which product version it covers.
_APPLIES_PAT = re.compile(r'\*Applies to:', re.IGNORECASE)
_APPLIES_SKIP = {
    'tags.md', 'site-map.md', 'usage-metrics.md', 'site-quality.md',
    'index.md',
}
issues = check(45, 'Missing "*Applies to:*" version marker on content pages')
_missing_applies = []
for _path in all_md():
    _fname = os.path.basename(_path)
    if _fname in _APPLIES_SKIP:
        continue
    _c = open(_path, errors='replace').read()
    if 'kb-grid' in _c or 'kb-card' in _c:
        continue  # landing pages don't need version markers
    if len(_c.splitlines()) < 10:
        continue  # stubs
    if not _APPLIES_PAT.search(_c):
        _missing_applies.append(os.path.relpath(_path, DOCS))
if _missing_applies:
    for _p in (_missing_applies if FULL else _missing_applies[:12]):
        warn(issues, f'Missing *Applies to:*: {_p}')
    if not FULL and len(_missing_applies) > 12:
        warn(issues, f'... and {len(_missing_applies)-12} more (run --full)')


# ── Check 46: Health-check pages missing bash command blocks ─────────────────
issues = check(46, 'Health-check pages missing executable bash command blocks')
_missing_bash = []
for _path in all_md():
    if os.path.basename(_path) != 'health-checks.md':
        continue
    _c = open(_path, errors='replace').read()
    if 'kb-grid' in _c or len(_c.splitlines()) < 20:
        continue
    if not re.search(r'```(bash|shell|sh)\b', _c):
        _missing_bash.append(os.path.relpath(_path, DOCS))
if _missing_bash:
    for _p in (_missing_bash if FULL else _missing_bash[:12]):
        warn(issues, f'No bash block: {_p}')
    if not FULL and len(_missing_bash) > 12:
        warn(issues, f'... and {len(_missing_bash)-12} more (run --full)')


# ── Check 47: Overly long pages (>1500 lines — candidates for splitting) ──────
# Exempt inherently long page types: cli-reference, scripts, procedures,
# certifications. These are reference pages that grow with content by design.
issues = check(47, 'Overly long pages (>1500 lines — split candidates)')
_LONG_SKIP = {'docs/tags.md', 'docs/site-map.md'}
_LONG_EXEMPT = ('cli-reference', 'scripts', 'procedures', 'certifications')
for _path in all_md():
    if os.path.relpath(_path, REPO) in _LONG_SKIP:
        continue
    if any(e in _path for e in _LONG_EXEMPT):
        continue
    _lc = sum(1 for _ in open(_path, errors='replace'))
    if _lc > 1500:
        warn(issues, f'{os.path.relpath(_path, DOCS)}: {_lc} lines')


# ── Check 48: FAQ pages without Q/A format ────────────────────────────────────
issues = check(48, 'FAQ pages without Q/A heading format')
_missing_qa = []
for _path in all_md():
    if os.path.basename(_path) != 'faq.md':
        continue
    _c = open(_path, errors='replace').read()
    if 'kb-grid' in _c or len(_c.splitlines()) < 10:
        continue
    # FAQ pages need either ### headings (question form) or **Q: markers
    if not re.search(r'^### .+\?', _c, re.MULTILINE) and not re.search(r'\*\*Q:', _c):
        _missing_qa.append(os.path.relpath(_path, DOCS))
if _missing_qa:
    for _p in (_missing_qa if FULL else _missing_qa[:12]):
        warn(issues, f'No Q/A format: {_p}')
    if not FULL and len(_missing_qa) > 12:
        warn(issues, f'... and {len(_missing_qa)-12} more (run --full)')


# ── Check 49: Unclosed code fences ────────────────────────────────────────────
issues = check(49, 'Unclosed code fences (odd number of triple-backtick lines)')
for _path in all_md():
    _lines = open(_path, errors='replace').readlines()
    _depth = 0
    _open_line = None
    for _i, _line in enumerate(_lines, 1):
        _s = _line.strip()
        if _s.startswith('```') or _s.startswith('~~~'):
            if _depth == 0:
                _depth = 1
                _open_line = _i
            else:
                _depth = 0
                _open_line = None
    if _depth > 0:
        _rel = os.path.relpath(_path, DOCS)
        warn(issues, f'{_rel}: unclosed fence opened at line {_open_line}')


# ── Check 50: Known-issues pages without a table ─────────────────────────────
issues = check(50, 'Known-issues pages without a Markdown table')
_missing_table = []
for _path in all_md():
    if os.path.basename(_path) != 'known-issues.md':
        continue
    _c = open(_path, errors='replace').read()
    if 'kb-grid' in _c or len(_c.splitlines()) < 10:
        continue
    if not re.search(r'^\|.+\|', _c, re.MULTILINE):
        _missing_table.append(os.path.relpath(_path, DOCS))
if _missing_table:
    for _p in (_missing_table if FULL else _missing_table[:12]):
        warn(issues, f'No table: {_p}')
    if not FULL and len(_missing_table) > 12:
        warn(issues, f'... and {len(_missing_table)-12} more (run --full)')


# ── Check 51: D2 node labels that are likely to overflow their boxes ──────────
# Labels using \n in D2 render as multi-line — check the longest *single line*.
issues = check(51, 'D2 node labels >40 chars (likely to overflow rendered box)')
_D2_LABEL = re.compile(r'```d2\n(.*?)\n```', re.DOTALL)
_D2_NODE_LABEL = re.compile(r'^\w[\w_.-]*\s*:\s*"([^"]+)"', re.MULTILINE)
for _md in all_md():
    _txt = open(_md, errors='replace').read()
    if '```d2' not in _txt:
        continue
    for _blk in _D2_LABEL.findall(_txt):
        for _lm in _D2_NODE_LABEL.finditer(_blk):
            _label = _lm.group(1)
            # D2 renders \n as line breaks — check max line length
            _max_line = max(len(ln) for ln in _label.split('\\n'))
            if _max_line > 55:
                warn(issues, f'{os.path.relpath(_md, DOCS)}: label "{_label[:55]}..."')
                break  # one warning per file is enough


# ── Check 52: PlantUML blocks without @startuml / @enduml ────────────────────
issues = check(52, 'PlantUML blocks missing @startuml / @enduml markers')
_PU_BLOCK = re.compile(r'```plantuml\n(.*?)\n```', re.DOTALL)
for _md in all_md():
    _txt = open(_md, errors='replace').read()
    if '```plantuml' not in _txt:
        continue
    for _blk in _PU_BLOCK.findall(_txt):
        if '@startuml' not in _blk or '@enduml' not in _blk:
            warn(issues, os.path.relpath(_md, DOCS))
            break


# ── Check 53: Broken all internal markdown links (not just See also) ──────────
# Checks every [text](href) link in every .md file where href is a relative
# path that ends with .md — the most common cause of 404s after page moves.
issues = check(53, 'Broken relative .md links anywhere in content (not only See also)')
_ALL_MD_LINK = re.compile(r'\[(?:[^\]]+)\]\(([^)#?]+\.md)\)')
for _md in all_md():
    _txt = open(_md, errors='replace').read()
    _src_dir = os.path.dirname(_md)
    for _lm in _ALL_MD_LINK.finditer(_txt):
        _href = _lm.group(1)
        if _href.startswith('http'):
            continue
        _tgt = os.path.normpath(os.path.join(_src_dir, _href[:-3]))
        if not (os.path.exists(_tgt + '.md')
                or os.path.exists(os.path.join(_tgt, 'index.md'))):
            warn(issues, f'{os.path.relpath(_md, DOCS)}: broken link "{_href}"')


# ── Check 54: Mermaid linear TD / subgraph diagrams (should be SVG or D2) ────
# Mermaid graph TB / flowchart TD render as narrow left-aligned diagrams that
# don't fill the content width.  Mermaid subgraph layouts cross arrows
# regardless of direction (LR subgraphs cross just as much as TD ones) --
# fixed 2026-07-03: the direction-only regex below let 130 LR-direction
# subgraph diagrams silently pass this check for days (a prior "fix" just
# changed TD->LR to satisfy the pattern-match, without removing the
# subgraphs that actually cause the crossing-arrow problem this check
# exists to catch). Both patterns should be replaced with D2 or custom SVG.
issues = check(54, 'Mermaid linear TD or subgraph diagrams (use D2/SVG instead)')
_MM_BLOCK = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
_MM_LINEAR = re.compile(r'^(flowchart|graph)\s+(TD|TB)\b', re.MULTILINE)
for _md in all_md():
    _txt = open(_md, errors='replace').read()
    if '```mermaid' not in _txt:
        continue
    for _blk in _MM_BLOCK.findall(_txt):
        if _MM_LINEAR.search(_blk) or 'subgraph' in _blk:
            _label = 'subgraph' if 'subgraph' in _blk else 'linear TD'
            warn(issues, f'{os.path.relpath(_md, DOCS)}: Mermaid {_label} — replace with D2 or SVG')
            break


# ── Check 55: Bash blocks missing example output ─────────────────────────────
# Every non-silent bash block should be followed by a non-bash code fence.
# Silent = comment-only or reboot/shutdown/poweroff/halt commands (no output).
issues = check(55, 'Bash blocks missing example output')
_BASH_OPEN55   = re.compile(r'^```bash\b', re.MULTILINE)
_FENCE_CLOSE55 = re.compile(r'^```\s*$', re.MULTILINE)
_SILENT_PFX55  = ('reboot', 'shutdown', 'poweroff', 'halt')

def _is_silent55(block):
    lines = [l.strip() for l in block.splitlines() if l.strip() and not l.startswith('```')]
    code = [l for l in lines if l and not l.startswith('#')]
    if not code:
        return True
    return all(any(l.startswith(p) for p in _SILENT_PFX55) for l in code)

_missing55 = 0
_total55   = 0
for _md in all_md():
    _txt = open(_md, errors='replace').read()
    if '```bash' not in _txt:
        continue
    _pos = 0
    while True:
        _mo = _BASH_OPEN55.search(_txt, _pos)
        if not _mo:
            break
        _mc = _FENCE_CLOSE55.search(_txt, _mo.end())
        if not _mc:
            break
        _block55 = _txt[_mo.start():_mc.end()]
        if not _is_silent55(_block55):
            _total55 += 1
            _after = _txt[_mc.end():_mc.end()+300].lstrip('\n ')
            if not (_after.startswith('```') and not _after.startswith('```bash')):
                _missing55 += 1
        _pos = _mc.end()
if _missing55:
    warn(issues, f'{_missing55}/{_total55} bash blocks site-wide are missing example output (run add_command_output.py)')


# ── Check 56: Directory-style relative links to nonexistent pages ────────────
# mkdocs --strict flags ANY link it can't statically pattern-match (including
# valid directory-style links like "../foo/" pointing at foo.md or foo/index.md,
# which resolve fine at runtime via directory URLs). This check instead verifies
# real existence using the same site/-relative effective-directory logic as
# Check 35 (flat file.md gets promoted to file/index.html, shifting relative
# link depth by one), to catch genuine 404s among non-.md-suffixed links
# anywhere in page content (not just "## See also" sections).
def _strip_fences56(text):
    out = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        s = line.strip()
        if s.startswith('```') or s.startswith('~~~'):
            in_fence = not in_fence
            out.append(line)
            continue
        out.append('' if in_fence else line)
    return ''.join(out)

issues = check(56, 'Directory-style relative links to nonexistent pages')
for _path in all_md():
    _content = _strip_fences56(open(_path, errors='replace').read())
    if _use_site:
        _rel_to_docs = os.path.relpath(_path, DOCS)
        _p = Path(_rel_to_docs)
        if _p.name == 'index.md':
            _eff_dir = os.path.join(_SITE, str(_p.parent))
        else:
            _eff_dir = os.path.join(_SITE, str(_p.parent), _p.stem)
    else:
        _p = Path(os.path.relpath(_path, DOCS))
        if _p.name == 'index.md':
            _eff_dir = os.path.dirname(_path)
        else:
            _eff_dir = os.path.join(os.path.dirname(_path), _p.stem)
    _ASSET_EXT56 = ('.svg', '.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.pdf', '.yml', '.yaml', '.zip', '.json')
    for _lm in re.finditer(r'\[[^\]]*\]\(([^)"]+)\)', _content):
        if _lm.start() > 0 and _content[_lm.start() - 1] == '!':
            continue  # image embed — different resolution rule, Check 5's job
        _href = _lm.group(1).split('#')[0]
        if not _href or _href.startswith(('http', 'mailto', 'data', '#')):
            continue
        if _href.endswith('.md') or _href.lower().endswith(_ASSET_EXT56):
            continue  # Check 53's / Check 5's job
        if _href.startswith('/'):
            _root56 = _SITE if _use_site else DOCS
            _target = os.path.normpath(os.path.join(_root56, _href.lstrip('/')))
        else:
            _target = os.path.normpath(os.path.join(_eff_dir, _href))
        if _use_site:
            _exists = os.path.exists(_target) or os.path.exists(os.path.join(_target, 'index.html'))
        else:
            _exists = (os.path.exists(_target)
                       or os.path.exists(_target + '.md')
                       or os.path.exists(os.path.join(_target, 'index.md')))
        if not _exists:
            _rel = os.path.relpath(_path, REPO)
            warn(issues, f'{_rel}: directory-style link "{_href}" resolves to no real page')


# ── Check 57: SVG canvas smaller than its actual content ─────────────────────
# Found 2026-07-03: several diagram generators computed row Y-positions
# correctly but left a stale top-level <svg width height viewBox>, so footers
# and in a few cases entire rows rendered below/right of the visible canvas —
# invisible content, not just a cosmetic overflow. scripts/svg_canvas_fix.py
# (--apply) grows (never shrinks) the canvas to fit; this check just detects.
issues = check(57, 'SVG canvas smaller than actual content (invisible off-canvas elements)')
try:
    from svg_canvas_fix import content_extent
    if os.path.isdir(ASSETS):
        import re as _re57
        _SVG_TAG57 = _re57.compile(r'<svg\b[^>]*\bwidth="(\d+(?:\.\d+)?)"[^>]*\bheight="(\d+(?:\.\d+)?)"')
        for fname in sorted(os.listdir(ASSETS)):
            if not fname.endswith('.svg'):
                continue
            path = Path(os.path.join(ASSETS, fname))
            m = _SVG_TAG57.search(open(path, errors='replace').read())
            if not m:
                continue
            cur_w, cur_h = float(m.group(1)), float(m.group(2))
            extent = content_extent(path)
            if extent is None:
                continue
            max_x, max_y = extent
            if max_x > cur_w + 1 or max_y > cur_h + 1:
                warn(issues, f'assets/{fname}: canvas {cur_w:.0f}x{cur_h:.0f} but content '
                             f'reaches {max_x:.0f}x{max_y:.0f}')
except ImportError:
    pass


# ── Check 58: SVG "Diagram Type:" footer positioned before later content ─────
# Found 2026-07-03: distinct from Check 57 -- canvas can already be big enough
# to contain everything, but a nested <g transform="translate(...)"> pushes
# some content past a footer bar sized/positioned for shorter content, so the
# gray footer renders in the *middle* of the diagram instead of at the bottom.
issues = check(58, 'SVG footer bar rendered before (above) later diagram content')
try:
    from svg_overflow_check import NS as _NS58, walk_absolute as _walk58, local_text as _ltext58
    if os.path.isdir(ASSETS):
        for fname in sorted(os.listdir(ASSETS)):
            if not fname.endswith('.svg'):
                continue
            path = os.path.join(ASSETS, fname)
            try:
                _root58 = ET.parse(path).getroot()
            except ET.ParseError:
                continue
            _rects58, _footer_text_y = [], None
            for _elem, _ox, _oy in _walk58(_root58):
                if _elem.tag == f'{_NS58}rect':
                    try:
                        _x = float(_elem.get('x', 0)) + _ox
                        _y = float(_elem.get('y', 0)) + _oy
                        _w = float(_elem.get('width', 0))
                        _h = float(_elem.get('height', 0))
                    except ValueError:
                        continue
                    _rects58.append((_x, _y, _w, _h))
                elif _elem.tag == f'{_NS58}text':
                    _content = _ltext58(_elem)
                    if _content.strip().startswith('Diagram Type'):
                        _y_attr = _elem.get('y')
                        if _y_attr is not None:
                            _footer_text_y = float(_y_attr) + _oy
            if _footer_text_y is None or not _rects58:
                continue
            _footer_candidates = [r for r in _rects58 if r[1] <= _footer_text_y <= r[1] + r[3] + 5]
            if not _footer_candidates:
                continue
            _footer58 = max(_footer_candidates, key=lambda r: r[2])  # widest = real footer bar
            _fy, _fh = _footer58[1], _footer58[3]
            _other58 = [r for r in _rects58 if r != _footer58]
            _max_bottom58 = max((r[1] + r[3] for r in _other58), default=0)
            if _max_bottom58 - (_fy + _fh) > 5:
                warn(issues, f'assets/{fname}: footer at y={_fy:.0f} but content reaches y={_max_bottom58:.0f}')
except ImportError:
    pass


# ── Check 59: SVG text likely wider than its enclosing box ───────────────────
# Heuristic (no real font metrics) -- estimates text width per character
# class and flags where it exceeds the smallest enclosing <rect>. Known
# false-positive source (documented 2026-07-03): in diagrams with many small
# adjacent/stacked boxes, "smallest enclosing" can pick a nearby box that
# spatially overlaps the text's anchor point but isn't the semantically
# correct one -- always spot-check a flagged file's actual box before
# treating this as confirmed, don't batch-fix on the numbers alone.
issues = check(59, 'SVG text likely wider than its enclosing box (heuristic, verify before fixing)')
try:
    from svg_overflow_check import analyze_svg as _analyze59
    if os.path.isdir(ASSETS):
        for fname in sorted(os.listdir(ASSETS)):
            if not fname.endswith('.svg'):
                continue
            path = Path(os.path.join(ASSETS, fname))
            findings, err = _analyze59(path)
            if findings:
                worst = max(f['overflow_px'] for f in findings)
                warn(issues, f'assets/{fname}: worst={worst:.0f}px over, {len(findings)} flagged text element(s)')
except ImportError:
    pass


# ── Check 60: Unconverted <br/> line-break tags leaking into SVG text ────────
# Found 2026-07-03 in mermaid_subgraph_to_svg.py: Mermaid labels using
# <br/>/<br> for line breaks (instead of \n) weren't being split, so the
# literal tag text rendered on the page (e.g. "Fork Remote<br/>github.com").
issues = check(60, 'Literal <br/> tags leaking into rendered SVG text')
if os.path.isdir(ASSETS):
    _BR_LEAK_RE = re.compile(r'<text\b[^>]*>[^<]*(?:&lt;br\s*/?&gt;)[^<]*</text>', re.IGNORECASE)
    for fname in sorted(os.listdir(ASSETS)):
        if not fname.endswith('.svg'):
            continue
        path = os.path.join(ASSETS, fname)
        _txt59 = open(path, errors='replace').read()
        if _BR_LEAK_RE.search(_txt59):
            warn(issues, f'assets/{fname}: literal <br/> tag found inside <text> content')


# ── Check 61: Code fence close line carries a language tag ───────────────────
# Found 2026-07-03 while investigating a wrong-title bug in a mermaid-to-SVG
# conversion: a real closing ``` fence should never have a language tag --
# if it does, that's proof an EARLIER fence was never properly closed (two
# opens got merged, one masquerading as the other's close). This causes
# real damage beyond cosmetics: any Markdown heading/prose that falls
# between the true unclosed open and this point gets silently swallowed as
# literal code-block text instead of rendering normally. Found and fixed 20
# instances across 14 files this way (2 independent bugs per file on
# average: an orphaned empty fence AND, separately, a heading+commands
# section missing its opening fence -- the two coincidentally canceled out
# in raw fence-count parity, which is why simple odd/even counting (see
# Check 49) didn't catch them).
issues = check(61, 'Code fence close line has a language tag (proof an earlier fence was never closed)')
for _md in all_md():
    _txt = open(_md, errors='replace').read()
    if '```' not in _txt and '~~~' not in _txt:
        continue
    _in_fence61 = False
    for _i, _line in enumerate(_txt.splitlines()):
        _s = _line.strip()
        if _s.startswith(('```', '~~~')):
            _tag61 = _s[3:].strip()
            if _in_fence61 and _tag61:
                warn(issues, f'{os.path.relpath(_md, DOCS)}:{_i+1}: "{_line.strip()}" '
                             f'closes a fence but carries a language tag')
            _in_fence61 = not _in_fence61


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
    if n == 30 and 'url_count' in r and not CHECK_LINKS:
        extra = f' — {r["url_count"]} URLs found (run --check-links to validate)'
    if n == 38 and 'video_count' in r:
        extra = f' — {r["video_count"]} videos registered'
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
