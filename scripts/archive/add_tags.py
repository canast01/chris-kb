#!/usr/bin/env python3
"""
Add front-matter tags to KB pages based on directory path.

Usage:
    python3 scripts/add_tags.py --dry-run   # preview changes
    python3 scripts/add_tags.py             # apply changes
"""

import os, re, sys

REPO  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS  = os.path.join(REPO, 'docs')
DRY   = '--dry-run' in sys.argv

# ── Tag rules: (path_segment, tag) ──────────────────────────────────────────
# Rules are evaluated in order; all matching rules are applied.
# Path segment match is case-insensitive substring of the relative path from docs/.

AREA_RULES = [
    # Products
    ('vmware',                      'vmware'),
    ('vcenter',                     'vcenter'),
    ('esxi',                        'esxi'),
    ('vsan',                        'vsan'),
    ('nsx',                         'nsx'),
    ('vmware-cloud-foundation',     'vcf'),
    ('vxrail',                      'vxrail'),
    ('aria-operations/',            'aria-operations'),
    ('aria-operations-for-logs',    'aria-logs'),
    ('aria-operations-for-networks','aria-networks'),
    ('aria-automation',             'aria-automation'),
    ('aria-suite-lifecycle',        'aria-lcm'),
    ('horizon',                     'horizon'),
    ('srm',                         'srm'),
    ('vsphere-replication',         'vsphere-replication'),
    ('tanzu',                       'tanzu'),
    ('powercli',                    'powercli'),
    # Cloud / Compute
    ('cloud/aws',                   'aws'),
    ('cloud/azure',                 'azure'),
    ('cloud/gcp',                   'gcp'),
    ('compute/linux',               'linux'),
    ('compute/windows',             'windows'),
    # Automation
    ('automation/ansible',          'ansible'),
    ('automation/terraform',        'terraform'),
    ('automation/powershell',       'powershell'),
    ('automation/python',           'python'),
    ('automation/github-actions',   'github-actions'),
    # Backup
    ('backup/veeam',                'veeam'),
    ('backup/commvault',            'commvault'),
    ('backup/netbackup',            'netbackup'),
    ('backup/dr-operations',        'dr'),
    # ITSM
    ('itsm/jira',                   'jira'),
    ('itsm/servicenow',             'servicenow'),
    ('itsm/confluence',             'confluence'),
    ('itsm/git',                    'git'),
    # Storage / Networking / Security
    ('storage/ceph',                'ceph'),
    ('storage/dell',                'dell'),
    ('storage/netapp',              'netapp'),
    ('storage/pure',                'pure'),
    ('/san/',                       'san'),
    ('/networking/',                'networking'),
    ('/security/',                  'security'),
    # Content type
    ('/architecture/',              'architecture'),
    ('/deploy/',                    'deployment'),
    ('/operations/',                'operations'),
    ('/troubleshooting/',           'troubleshooting'),
    ('/security/',                  'security'),
    ('/reference/',                 'reference'),
    ('/internals/',                 'internals'),
    ('/learning-path/',             'learning-path'),
    ('/scenarios/',                 'scenarios'),
    ('/certifications/',            'certifications'),
    # Version — applied where product + content type already set a good context
    ('vcenter',                     'vsphere-8'),
    ('esxi',                        'vsphere-8'),
    ('vsan',                        'vsphere-8'),
    ('nsx',                         'nsx-4'),
]

FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)
TAGS_RE        = re.compile(r'^tags:\s*\n((?:  - [^\n]+\n)+)', re.MULTILINE)


def compute_tags(rel: str) -> list[str]:
    """Return sorted, deduped list of tags for a given rel path."""
    tags = set()
    path = '/' + rel.replace(os.sep, '/')
    for segment, tag in AREA_RULES:
        if segment in path:
            tags.add(tag)
    return sorted(tags)


def has_frontmatter(content: str) -> bool:
    return content.startswith('---\n')


def get_existing_tags(content: str) -> list[str]:
    m = FRONTMATTER_RE.match(content)
    if not m:
        return []
    fm = m.group(1)
    tm = TAGS_RE.search(fm)
    if not tm:
        return []
    return [line.strip().lstrip('- ') for line in tm.group(1).splitlines()]


def apply_tags(path: str, tags: list[str]) -> bool:
    """Return True if file was (or would be) modified."""
    content = open(path).read()
    existing = get_existing_tags(content)
    merged   = sorted(set(existing) | set(tags))
    if merged == sorted(existing):
        return False  # nothing new to add

    tags_block = 'tags:\n' + ''.join(f'  - {t}\n' for t in merged)

    if has_frontmatter(content):
        m = FRONTMATTER_RE.match(content)
        fm_body = m.group(1)
        rest    = content[m.end():]
        # Replace or insert tags: block inside existing front matter
        if TAGS_RE.search(fm_body):
            new_fm = TAGS_RE.sub(tags_block, fm_body)
        else:
            new_fm = fm_body.rstrip('\n') + '\n' + tags_block.rstrip('\n')
        new_content = f'---\n{new_fm}\n---\n{rest}'
    else:
        new_content = f'---\n{tags_block}---\n{content}'

    if not DRY:
        open(path, 'w').write(new_content)
    return True


modified = 0
skipped  = 0
for root, dirs, files in os.walk(DOCS):
    dirs[:] = sorted([d for d in dirs if not d.startswith('.')])
    for fname in sorted(files):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(root, fname)
        rel  = os.path.relpath(path, DOCS)
        tags = compute_tags(rel)
        if not tags:
            skipped += 1
            continue
        changed = apply_tags(path, tags)
        if changed:
            modified += 1
            if DRY:
                print(f'  {rel}: {tags}')

mode = 'DRY RUN — ' if DRY else ''
print(f'\n{mode}{modified} files updated, {skipped} files had no matching tags')
