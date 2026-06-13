#!/usr/bin/env python3
"""
Add "## See also" cross-reference sections to pages that have natural companions.

Each rule maps a source page path pattern to a list of related links.
Links use relative paths from the source page's directory.

Usage:
    python3 scripts/add_see_also.py --dry-run
    python3 scripts/add_see_also.py
"""

import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
DRY  = '--dry-run' in sys.argv

SEE_ALSO_RE = re.compile(r'^## See also', re.MULTILINE)

# ── Cross-reference map ───────────────────────────────────────────────────────
# Format: (source_path_pattern, [(link_text, abs_doc_path), ...])
# abs_doc_path is relative to docs/
XREF_MAP = [
    # vSAN troubleshooting ↔ vSAN cluster health internals
    ('virtualization/vmware/vsan/troubleshooting/common-issues', [
        ('vSAN Cluster Health — Internals', 'virtualization/vmware/internals/vsan-cluster-health/'),
        ('vSAN — Operations', 'virtualization/vmware/vsan/operations/'),
        ('Scenarios — vSAN Disk Failure', 'virtualization/vmware/topics/scenarios/vsan-disk-component-failure/'),
    ]),

    # NSX troubleshooting ↔ NSX data plane internals
    ('virtualization/vmware/nsx/troubleshooting/common-issues', [
        ('NSX Data Plane — Internals', 'virtualization/vmware/internals/nsx-data-plane/'),
        ('NSX — Operations', 'virtualization/vmware/nsx/operations/'),
        ('Scenarios — NSX Connectivity Broken', 'virtualization/vmware/topics/scenarios/nsx-connectivity-broken/'),
    ]),

    # vCenter troubleshooting ↔ internals
    ('virtualization/vmware/vcenter/troubleshooting/common-issues', [
        ('vCenter HA — Internals', 'virtualization/vmware/internals/vcha-internals/'),
        ('Certificate Chain — Internals', 'virtualization/vmware/internals/certificate-chain/'),
        ('Scenarios — vCenter Down', 'virtualization/vmware/topics/scenarios/vcenter-down/'),
    ]),

    # ESXi troubleshooting ↔ cluster services
    ('virtualization/vmware/esxi/troubleshooting/common-issues', [
        ('Cluster Services — Internals', 'virtualization/vmware/internals/cluster-services/'),
        ('HA Deep Dive — Internals', 'virtualization/vmware/internals/ha-deep-dive/'),
        ('Scenarios — ESXi Host Disconnected', 'virtualization/vmware/topics/scenarios/esxi-host-disconnected/'),
    ]),

    # Certificate rotation runbook ↔ internals + scenario
    ('virtualization/vmware/operations/runbooks/certificate-rotation', [
        ('Certificate Chain — Internals', 'virtualization/vmware/internals/certificate-chain/'),
        ('Scenarios — Certificate Expiry and Rotation', 'virtualization/vmware/topics/scenarios/certificate-expiry-rotation/'),
        ('vCenter — Security', 'virtualization/vmware/vcenter/security/'),
    ]),

    # NSX DFW scenario ↔ internals
    ('virtualization/vmware/topics/scenarios/nsx-dfw-blocking', [
        ('NSX Data Plane — Internals', 'virtualization/vmware/internals/nsx-data-plane/'),
        ('NSX Microsegmentation Rollout — Scenario', 'virtualization/vmware/topics/scenarios/nsx-microsegmentation-rollout/'),
        ('NSX — Operations', 'virtualization/vmware/nsx/operations/'),
    ]),

    # NSX microsegmentation rollout ↔ DFW scenario + internals
    ('virtualization/vmware/topics/scenarios/nsx-microsegmentation-rollout', [
        ('NSX Data Plane — Internals', 'virtualization/vmware/internals/nsx-data-plane/'),
        ('Scenarios — NSX DFW Blocking', 'virtualization/vmware/topics/scenarios/nsx-dfw-blocking-application-traffic/'),
        ('NSX — Deploy', 'virtualization/vmware/nsx/deploy/'),
    ]),

    # vSAN encryption ↔ internals + security
    ('virtualization/vmware/topics/scenarios/enable-vsan-encryption', [
        ('vSAN Cluster Health — Internals', 'virtualization/vmware/internals/vsan-cluster-health/'),
        ('vSAN — Security', 'virtualization/vmware/vsan/security/'),
        ('vSAN — Operations', 'virtualization/vmware/vsan/operations/'),
    ]),

    # DRS mechanics ↔ HA and cluster services
    ('virtualization/vmware/internals/drs-mechanics', [
        ('HA Deep Dive — Internals', 'virtualization/vmware/internals/ha-deep-dive/'),
        ('Cluster Services — Internals', 'virtualization/vmware/internals/cluster-services/'),
        ('Resource Management — Internals', 'virtualization/vmware/internals/vsphere-resource-management/'),
    ]),

    # HA deep dive ↔ DRS + cluster services
    ('virtualization/vmware/internals/ha-deep-dive', [
        ('DRS Mechanics — Internals', 'virtualization/vmware/internals/drs-mechanics/'),
        ('Cluster Services — Internals', 'virtualization/vmware/internals/cluster-services/'),
        ('Scenarios — VM Inaccessible / HA Failover', 'virtualization/vmware/topics/scenarios/vm-inaccessible-ha-failover/'),
    ]),

    # vCenter HA internals ↔ scenario + operations
    ('virtualization/vmware/internals/vcha-internals', [
        ('Scenarios — vCenter HA Failover', 'virtualization/vmware/topics/scenarios/vcenter-ha-failover/'),
        ('vCenter — Operations', 'virtualization/vmware/vcenter/operations/'),
        ('HA Deep Dive — Internals', 'virtualization/vmware/internals/ha-deep-dive/'),
    ]),

    # DR test scenario ↔ SRM + vSR operations
    ('virtualization/vmware/topics/scenarios/dr-test-planned-failover', [
        ('SRM — Operations', 'virtualization/vmware/srm/operations/'),
        ('vSphere Replication — Operations', 'virtualization/vmware/vsphere-replication/operations/'),
        ('Scenarios — SRM RPO Violation', 'virtualization/vmware/topics/scenarios/srm-replication-lag-rpo-violation/'),
    ]),

    # vCenter backup runbook ↔ operations + scenario
    ('virtualization/vmware/operations/runbooks/vcenter-backup', [
        ('vCenter — Operations', 'virtualization/vmware/vcenter/operations/'),
        ('Scenarios — vCenter Down', 'virtualization/vmware/topics/scenarios/vcenter-down/'),
        ('VMware Morning Health Check', 'virtualization/vmware/operations/morning-health-check/'),
    ]),

    # Storage APD scenario ↔ vSAN internals + storage internals
    ('virtualization/vmware/topics/scenarios/storage-apd', [
        ('vSphere Storage — Internals', 'virtualization/vmware/internals/vsphere-storage/'),
        ('vSAN Cluster Health — Internals', 'virtualization/vmware/internals/vsan-cluster-health/'),
        ('Scenarios — vSAN Disk Failure', 'virtualization/vmware/topics/scenarios/vsan-disk-component-failure/'),
    ]),

    # Morning health check ↔ product operations pages
    ('virtualization/vmware/operations/morning-health-check', [
        ('VMware Operations — Runbooks', 'virtualization/vmware/operations/runbooks/'),
        ('Scenarios — Cross-product Playbooks', 'virtualization/vmware/topics/scenarios/'),
        ('vSAN Cluster Health — Internals', 'virtualization/vmware/internals/vsan-cluster-health/'),
    ]),

    # Veeam operations ↔ backup runbooks
    ('backup/veeam/operations', [
        ('Backup — DR Operations', 'backup/dr-operations/'),
        ('VMware — Operations Runbooks', 'virtualization/vmware/operations/runbooks/'),
    ]),

    # NSX networking internals ↔ NSX deploy + DRS
    ('virtualization/vmware/internals/vsphere-networking-internals', [
        ('NSX Data Plane — Internals', 'virtualization/vmware/internals/nsx-data-plane/'),
        ('vSphere Networking — Internals', 'virtualization/vmware/internals/vsphere-networking/'),
        ('NSX — Architecture', 'virtualization/vmware/nsx/architecture/'),
    ]),
]


def find_file(doc_rel: str) -> str | None:
    """Return absolute path for a docs-relative path, or None if not found."""
    candidate = os.path.join(DOCS, doc_rel.rstrip('/'), 'index.md')
    if os.path.exists(candidate):
        return candidate
    candidate2 = os.path.join(DOCS, doc_rel)
    if os.path.exists(candidate2):
        return candidate2
    return None


def relative_link(from_dir: str, to_doc_rel: str) -> str | None:
    """Return a relative URL from from_dir to the doc path."""
    target = find_file(to_doc_rel)
    if not target:
        return None
    target_dir = os.path.dirname(target)
    rel = os.path.relpath(target_dir, from_dir)
    return rel.replace(os.sep, '/') + '/'


def make_see_also(from_dir: str, links: list) -> str:
    items = []
    for text, doc_rel in links:
        href = relative_link(from_dir, doc_rel)
        if href:
            items.append(f'- [{text}]({href})')
    if not items:
        return ''
    return '## See also\n\n' + '\n'.join(items) + '\n'


modified = 0
skipped  = 0

for source_pattern, links in XREF_MAP:
    path = find_file(source_pattern)
    if not path:
        # Try as exact file
        path = os.path.join(DOCS, source_pattern + '.md')
        if not os.path.exists(path):
            skipped += 1
            continue

    content = open(path).read()

    # Skip if already has See also
    if SEE_ALSO_RE.search(content):
        skipped += 1
        continue

    from_dir = os.path.dirname(path)
    block = make_see_also(from_dir, links)
    if not block:
        skipped += 1
        continue

    new_content = content.rstrip('\n') + '\n\n---\n\n' + block
    modified += 1

    rel = os.path.relpath(path, DOCS)
    if DRY:
        print(f'  {rel}')
    else:
        open(path, 'w').write(new_content)

mode = 'DRY RUN — ' if DRY else ''
print(f'\n{mode}{modified} files updated, {skipped} skipped')
