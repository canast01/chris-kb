#!/usr/bin/env python3
"""
KB site audit — 37 checks.

Usage:
    python3 scripts/site_audit.py               # run all checks, print summary
    python3 scripts/site_audit.py --full        # include full issue lists (no truncation)
    python3 scripts/site_audit.py --check-links # also validate external URLs (slow)
"""

import os, re, sys, xml.etree.ElementTree as ET

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
    if _rel in _SKIP_DIAG or _rel.startswith('stats/'):
        continue
    _c = open(_path).read()
    if 'kb-card' in _c or 'kb-grid' in _c:
        continue  # nav pages don't need diagrams
    if re.search(r'\.(svg|png|jpg)\)', _c) or '<img ' in _c:
        continue  # pages with embedded images satisfy the diagram requirement
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
            _has_svg = bool(_nxt and re.match(r'!\[.*\]\(.*\.svg\)', _nxt[0]))
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
issues = check(35, '"See also" internal link validity')
for _path in all_md():
    _c = open(_path).read()
    _sm = re.search(r'## See also\n(.*?)(?=\n##|\Z)', _c, re.DOTALL)
    if not _sm:
        continue
    _page_dir = os.path.dirname(_path)
    for _lm in re.finditer(r'\[.*?\]\(([^)]+)\)', _sm.group(1)):
        _href = _lm.group(1).split('#')[0]
        if not _href or _href.startswith('http') or _href.startswith('mailto'):
            continue
        _target = os.path.normpath(os.path.join(_page_dir, _href))
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
    return anchors

issues = check(36, 'Anchor fragment validity (internal #links)')
_anchor_cache = {}
for _path in all_md():
    _c = open(_path).read()
    _page_dir = os.path.dirname(_path)
    for _lm in re.finditer(r'\[.*?\]\(([^)#"]+)#([^)"]+)\)', _c):
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
