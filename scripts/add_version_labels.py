#!/usr/bin/env python3
"""
Add a visible "Applies to:" line at the end of kb-summary blocks
on procedure pages (deploy/, operations/, troubleshooting/, security/).

Usage:
    python3 scripts/add_version_labels.py --dry-run
    python3 scripts/add_version_labels.py
"""

import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
DRY  = '--dry-run' in sys.argv

# Only add to procedure-type pages (not landing pages or architecture)
PROC_DIRS = {'/deploy/', '/operations/', '/troubleshooting/', '/security/'}

# Version label per product path segment
VERSION_MAP = [
    ('vcenter',                 'vSphere 7.x / 8.x'),
    ('esxi',                    'vSphere 7.x / 8.x'),
    ('vsan',                    'vSAN 7.x / 8.x'),
    ('nsx',                     'NSX-T 3.x / NSX 4.x'),
    ('vmware-cloud-foundation', 'VCF 4.x / 5.x'),
    ('vxrail',                  'VxRail 7.x / 8.x'),
    ('aria-operations-for-networks', 'Aria Networks 6.x'),
    ('aria-operations-for-logs',     'Aria Logs 8.x'),
    ('aria-operations/',             'Aria Ops 8.x'),
    ('aria-automation',              'Aria Automation 8.x'),
    ('aria-suite-lifecycle',         'Aria LCM 8.x'),
    ('horizon',                 'Horizon 8.x'),
    ('srm',                     'SRM 8.x / 9.x'),
    ('vsphere-replication',     'vSphere Replication 8.x'),
    ('tanzu',                   'Tanzu 3.x'),
    ('powercli',                'PowerCLI 13.x'),
    # Automation
    ('ansible',                 'Ansible 2.14+'),
    ('terraform',               'Terraform 1.x'),
    # Storage
    ('ceph',                    'Ceph Reef / Squid'),
    ('veeam',                   'Veeam 12.x'),
    ('commvault',               'Commvault 2024.x'),
    ('netbackup',               'NetBackup 10.x'),
    # ITSM
    ('servicenow',              'ServiceNow (Washington / Xanadu)'),
    ('jira',                    'Jira 9.x / Cloud'),
    # Compute
    ('linux',                   'RHEL / Ubuntu LTS'),
    ('windows-server',          'Windows Server 2019 / 2022'),
]

SUMMARY_RE  = re.compile(r'(<div class="kb-summary">)(.*?)(</div>)', re.DOTALL)
APPLIES_RE  = re.compile(r'Applies to:')


def get_version(rel: str) -> str | None:
    path = '/' + rel.replace(os.sep, '/')
    # Only procedure-type pages
    if not any(d in path for d in PROC_DIRS):
        return None
    for segment, label in VERSION_MAP:
        if segment in path:
            return label
    return None


def apply_label(path: str, label: str) -> bool:
    content = open(path).read()
    m = SUMMARY_RE.search(content)
    if not m:
        return False
    body = m.group(2)
    if APPLIES_RE.search(body):
        return False  # already has one

    new_body = body.rstrip() + f'\n\n*Applies to: {label}*\n'
    new_content = content[:m.start()] + m.group(1) + new_body + m.group(3) + content[m.end():]
    if not DRY:
        open(path, 'w').write(new_content)
    return True


modified = 0
for root, dirs, files in os.walk(DOCS):
    dirs[:] = sorted([d for d in dirs if not d.startswith('.')])
    for fname in sorted(files):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(root, fname)
        rel  = os.path.relpath(path, DOCS)
        label = get_version(rel)
        if not label:
            continue
        changed = apply_label(path, label)
        if changed:
            modified += 1
            if DRY:
                print(f'  {rel}: "{label}"')

mode = 'DRY RUN — ' if DRY else ''
print(f'\n{mode}{modified} files updated')
