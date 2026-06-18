#!/usr/bin/env python3
"""
Add a "## Before you begin" section to procedure pages that don't already have one.
Inserts after the kb-summary+diagram block, before the first H2.

Usage:
    python3 scripts/add_prerequisites.py --dry-run
    python3 scripts/add_prerequisites.py
"""

import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
DRY  = '--dry-run' in sys.argv

PROC_DIRS = {'/deploy/', '/operations/', '/troubleshooting/', '/security/'}

# Pages that already have a prerequisites section or are index/landing pages
SKIP_RE = re.compile(
    r'^## (Prerequisites|Before you begin|Requirements|Prereq)',
    re.MULTILINE | re.IGNORECASE
)

# ── Product-specific prerequisite content ──────────────────────────────────
def prereqs_for(rel: str) -> str:
    path = '/' + rel.replace(os.sep, '/')

    # ── Content type ────────────────────────────────────────────────────────
    is_deploy    = '/deploy/'        in path
    is_ops       = '/operations/'    in path
    is_trouble   = '/troubleshooting/' in path
    is_security  = '/security/'      in path

    # ── Product detection ────────────────────────────────────────────────────
    is_vmware = any(p in path for p in [
        '/vmware/', '/vcenter/', '/esxi/', '/vsan/', '/nsx/', '/vxrail/',
        '/vmware-cloud-foundation/', '/aria-', '/horizon/', '/srm/',
        '/vsphere-replication/', '/tanzu/', '/powercli/',
    ])
    is_linux   = '/compute/linux'    in path
    is_windows = '/compute/windows'  in path
    is_storage = any(p in path for p in ['/storage/', '/san/', '/netapp/', '/ceph/', '/pure/', '/dell/'])
    is_network = '/networking/'      in path
    is_backup  = '/backup/'          in path or '/veeam/' in path or '/commvault/' in path
    is_ansible = '/ansible/'         in path
    is_tf      = '/terraform/'       in path

    # ── Access line ──────────────────────────────────────────────────────────
    if is_vmware and is_deploy:
        access = '- **Access:** vCenter Administrator role and SSH access to VCSA/ESXi hosts'
    elif is_vmware and is_ops:
        access = '- **Access:** vCenter read-only minimum; Administrator role for remediation steps'
    elif is_vmware and is_trouble:
        access = '- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access'
    elif is_vmware:
        access = '- **Access:** vCenter Administrator role'
    elif is_linux:
        access = '- **Access:** root or sudo-capable account on target hosts'
    elif is_windows:
        access = '- **Access:** Local Administrator or Domain Admin on target hosts'
    elif is_storage:
        access = '- **Access:** Storage admin credentials (cluster admin or equivalent)'
    elif is_network:
        access = '- **Access:** Network admin credentials; console or SSH to devices'
    elif is_backup:
        access = '- **Access:** Backup admin role on backup server; target system credentials'
    elif is_ansible:
        access = '- **Access:** SSH key or service account with sudo on managed hosts; Ansible control node'
    elif is_tf:
        access = '- **Access:** Provider credentials configured (`terraform login` or env vars)'
    else:
        access = '- **Access:** Admin credentials on all affected systems'

    # ── Content-type-specific bullet sets ────────────────────────────────────
    if is_deploy:
        specific = """\
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available"""

    elif is_ops:
        specific = """\
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion"""

    elif is_trouble:
        specific = """\
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed"""

    elif is_security:
        specific = """\
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible"""

    else:
        specific = """\
- **Environment:** confirm all dependencies are running before starting
- **Logging:** record command output for audit and rollback purposes"""

    return f"""## Before you begin

{access}
{specific}

---

"""


# ── Insertion logic ───────────────────────────────────────────────────────────
FENCE_RE   = re.compile(r'```[\s\S]+?```\n', re.MULTILINE)
SUMMARY_RE = re.compile(r'<div class="kb-summary">[\s\S]+?</div>\n', re.MULTILINE)
H2_RE      = re.compile(r'^## ', re.MULTILINE)


def insert_prereqs(content: str, block: str) -> str:
    """Insert block before the first H2, after diagram/summary."""
    m = H2_RE.search(content)
    if m:
        return content[:m.start()] + block + content[m.start():]
    # No H2 — append at end
    return content.rstrip('\n') + '\n\n' + block


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

        # Only procedure-type directories
        if not any(d in rpath for d in PROC_DIRS):
            skipped += 1
            continue

        content = open(path).read()

        # Skip landing pages (contain kb-grid cards — these are nav pages, not procedures)
        if '<div class="kb-grid' in content:
            skipped += 1
            continue

        # Skip if already has prereqs
        if SKIP_RE.search(content):
            skipped += 1
            continue

        block = prereqs_for(rel)
        new_content = insert_prereqs(content, block)

        if new_content == content:
            skipped += 1
            continue

        modified += 1
        if DRY:
            print(f'  {rel}')
        else:
            open(path, 'w').write(new_content)

mode = 'DRY RUN — ' if DRY else ''
print(f'\n{mode}{modified} files updated, {skipped} skipped')
