#!/usr/bin/env python3
"""
Add MkDocs Material admonition warnings to procedure pages for
destructive or service-interrupting operations.

Inserts a !!! warning block after the "Before you begin" section
(or after the kb-summary if no prereqs section exists) on pages
that match known destructive operation patterns.

Usage:
    python3 scripts/add_risk_warnings.py --dry-run
    python3 scripts/add_risk_warnings.py
"""

import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
DRY  = '--dry-run' in sys.argv

# ── Destructive operation patterns → warning text ─────────────────────────────
# Each rule: (path_substring, warning_title, warning_body)
# Rules use TWO qualifiers: (required_segment, also_required, title, body)
# Both segments must appear in the path for the rule to match.
# Use '' as the second segment to match on the first alone.
RULES = [
    # VMware certificate rotation runbooks only
    ('certificate-rotation',  '',       'Service interruption',
     'Certificate rotation restarts vCenter SSO and platform services. '
     'All vSphere Client sessions will disconnect. '
     'Allow 15–30 minutes and schedule a maintenance window.'),

    # vSAN encryption (scenario page)
    ('enable-vsan-encryption', '',      'Full data rebuild required',
     'Enabling or disabling vSAN encryption triggers a full data migration across all disk groups. '
     'This can take hours on large clusters. Do not proceed without confirming available capacity '
     'and a tested rollback snapshot of vCenter.'),

    # VMware ESXi/cluster host upgrade only
    ('vmware', '/operations/install-upgrade', 'Host enters maintenance mode',
     'ESXi remediation puts hosts into maintenance mode, triggering DRS evacuation. '
     'Confirm DRS is Fully Automated and HA admission control is satisfied before starting.'),

    # vCenter backup runbook
    ('vcenter-backup',         '',      'vCenter downtime',
     'Restoring vCenter from backup replaces the running instance. '
     'The environment will be unmanaged for the duration of the restore (typically 20–60 minutes).'),

    # NSX deploy
    ('nsx/deploy',             '',      'DFW enforcement change',
     'Deploying or reconfiguring NSX affects distributed firewall policy across all hosts. '
     'Validate in monitor mode before enforcing. A misconfigured rule can block application traffic immediately.'),

    # Storage vMotion scenario
    ('storage-vmotion',        '',      'Increased I/O load',
     'Storage vMotion generates sustained read/write I/O on both source and destination datastores. '
     'Run during a low-traffic window and monitor vSAN resync latency throughout.'),

    # DR failover scenario
    ('dr-test-planned-failover', '',    'Production traffic cutover',
     'Executing a planned failover transfers production traffic to the recovery site. '
     'Confirm all replication groups are synchronised (RPO = 0) and stakeholders are notified before starting.'),

    # SDDC Manager upgrade scenario
    ('vcf-sddc-manager-upgrade', '',    'Full SDDC management plane downtime',
     'SDDC Manager upgrade pauses all lifecycle management operations for the duration. '
     'No new workloads, patches, or expansions can be applied until the upgrade completes.'),

    # Host profile remediation scenario
    ('host-profile-compliance', '',     'Hosts reboot during remediation',
     'Applying a host profile that changes kernel parameters or drivers requires a host reboot. '
     'Ensure DRS can evacuate each host before remediation begins.'),

    # vSAN deploy (disk claim)
    ('vsan/deploy',             '',     'Disk claim is destructive',
     'Claiming disks for vSAN **erases all existing data** on those disks. '
     'Confirm disk selection before proceeding — this action cannot be undone.'),
]

WARNING_RE  = re.compile(r'^!!! (warning|danger)', re.MULTILINE)
PREREQ_RE   = re.compile(r'^## Before you begin', re.MULTILINE)
SUMMARY_END = re.compile(r'</div>\n', re.MULTILINE)
H2_RE       = re.compile(r'^## ', re.MULTILINE)


def make_warning(title: str, body: str) -> str:
    return f'\n!!! warning "{title}"\n    {body}\n'


def insert_after_prereqs(content: str, block: str) -> str:
    """Insert block after the 'Before you begin' section (after its --- separator)."""
    # Find end of Before you begin section (next ---)
    m_prereq = PREREQ_RE.search(content)
    if m_prereq:
        # Find the --- that closes the prereqs block
        sep = content.find('\n---\n', m_prereq.end())
        if sep != -1:
            pos = sep + 5  # after the ---\n
            return content[:pos] + block + content[pos:]

    # Fallback: insert before first H2
    m_h2 = H2_RE.search(content)
    if m_h2:
        return content[:m_h2.start()] + block + content[m_h2.start():]

    return content + block


modified = 0
skipped  = 0

for root, dirs, files in os.walk(DOCS):
    dirs[:] = sorted([d for d in dirs if not d.startswith('.')])
    for fname in sorted(files):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(root, fname)
        rel  = os.path.relpath(path, DOCS)
        rpath = '/' + rel.replace(os.sep, '/')

        content = open(path).read()

        # Skip landing pages (kb-grid nav pages — warnings belong on procedure pages only)
        if '<div class="kb-grid' in content:
            skipped += 1
            continue

        # Skip if already has a warning admonition
        if WARNING_RE.search(content):
            skipped += 1
            continue

        # Find matching rule (both segments must be present in path)
        matched = None
        for seg1, seg2, title, body in RULES:
            if seg1 in rpath and (not seg2 or seg2 in rpath):
                matched = (title, body)
                break

        if not matched:
            skipped += 1
            continue

        title, body = matched
        block = make_warning(title, body)
        new_content = insert_after_prereqs(content, block)

        if new_content == content:
            skipped += 1
            continue

        modified += 1
        if DRY:
            print(f'  {rel}: "{title}"')
        else:
            open(path, 'w').write(new_content)

mode = 'DRY RUN — ' if DRY else ''
print(f'\n{mode}{modified} files updated, {skipped} skipped')
