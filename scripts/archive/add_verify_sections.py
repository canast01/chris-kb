#!/usr/bin/env python3
"""
Add a "## Verify" section at the end of procedure pages that lack one.
Content is product/type-aware.

Usage:
    python3 scripts/add_verify_sections.py --dry-run
    python3 scripts/add_verify_sections.py
"""

import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
DRY  = '--dry-run' in sys.argv

PROC_DIRS = {'/deploy/', '/operations/', '/troubleshooting/'}
VERIFY_RE = re.compile(r'^## Verify|^## Validation|^## Confirm|^## Check your work', re.MULTILINE)


def verify_for(rel: str) -> str:
    path = '/' + rel.replace(os.sep, '/')

    is_deploy    = '/deploy/'          in path
    is_ops       = '/operations/'      in path
    is_trouble   = '/troubleshooting/' in path

    # ── Product detection ────────────────────────────────────────────────────
    is_vcenter = '/vcenter/'  in path
    is_esxi    = '/esxi/'     in path
    is_vsan    = '/vsan/'     in path
    is_nsx     = '/nsx/'      in path
    is_vmware  = '/vmware/'   in path or any([is_vcenter, is_esxi, is_vsan, is_nsx])
    is_linux   = '/linux/'    in path
    is_windows = '/windows/'  in path
    is_storage = '/storage/'  in path or '/san/' in path
    is_backup  = '/backup/'   in path or '/veeam/' in path or '/commvault/' in path

    # ── Deploy verify ────────────────────────────────────────────────────────
    if is_deploy:
        if is_vcenter:
            return """\
## Verify

- **vSphere Client:** log in at `https://<vcenter-fqdn>/ui` — inventory loads and all hosts show Connected
- **Alarms:** Home → Alarms — no critical alarms present after deployment
- **Services:** `service-control --status --all` — all services show RUNNING
- **Backup:** VAMI → Backup — schedule active, first backup completes successfully
"""
        if is_vsan:
            return """\
## Verify

- **Skyline Health:** Cluster → Monitor → vSAN → Skyline Health — all checks green
- **Disk groups:** Cluster → Configure → vSAN → Disk Management — all disk groups Healthy
- **Object compliance:** Cluster → Monitor → vSAN → Virtual Objects — all Compliant
- **Performance service:** Cluster → Monitor → vSAN → Performance — graphs populating within 5 min
"""
        if is_nsx:
            return """\
## Verify

- **Manager cluster:** NSX UI → System → Overview — all nodes Active, cluster Stable
- **Transport nodes:** Fabric → Nodes → Host Transport Nodes — all nodes Configured/Success
- **Edge cluster:** Fabric → Nodes → Edge Transport Nodes — all edges Up
- **Connectivity test:** NSX UI → Tools → Traceflow — send a packet between two VMs on different segments
"""
        if is_esxi:
            return """\
## Verify

- **Host connected:** vSphere Client → host status shows Connected (green)
- **NTP sync:** `esxcli system time get` — time within 5 seconds of authoritative source
- **Network:** `esxcli network ip interface list` — vmk0 (management) shows Up
- **SSH disabled:** `esxcli system ssh get` — Policy: off (re-enable only when needed)
"""
        if is_vmware:
            return """\
## Verify

- **vSphere Client:** confirm the component is visible and shows a healthy status
- **Alarms:** Home → Alarms — no new critical alarms after deployment
- **Logs:** review vmware.log / recent events for any errors in the first 5 minutes
"""
        if is_linux:
            return """\
## Verify

```bash
systemctl status <service-name>   # Active: running
journalctl -u <service-name> -n 20 --no-pager  # no ERROR lines
ss -tlnp | grep <port>            # service listening on expected port
```
"""
        if is_storage:
            return """\
## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window
"""
        # Generic deploy
        return """\
## Verify

- Confirm the service or component is running and reachable
- Check management UI for any errors or warnings
- Run a basic functional test (login, read, write) to confirm end-to-end operation
"""

    # ── Operations verify ────────────────────────────────────────────────────
    if is_ops:
        if is_vmware:
            return """\
## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
"""
        if is_backup:
            return """\
## Verify

- **Job status:** confirm backup job completed with status Success (not Warning)
- **Recovery test:** restore a single file or VM from the new backup to confirm restorability
- **Retention:** verify old recovery points are expiring per the configured retention policy
"""
        # Generic ops
        return """\
## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
"""

    # ── Troubleshooting verify ────────────────────────────────────────────────
    if is_trouble:
        if is_vmware:
            return """\
## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
"""
        # Generic troubleshoot
        return """\
## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
"""

    return ''


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

        if not any(d in rpath for d in PROC_DIRS):
            skipped += 1
            continue

        content = open(path).read()

        # Skip landing pages
        if '<div class="kb-grid' in content:
            skipped += 1
            continue

        # Skip if already has a verify/validation section
        if VERIFY_RE.search(content):
            skipped += 1
            continue

        block = verify_for(rel)
        if not block:
            skipped += 1
            continue

        new_content = content.rstrip('\n') + '\n\n---\n\n' + block
        modified += 1

        if DRY:
            print(f'  {rel}')
        else:
            open(path, 'w').write(new_content)

mode = 'DRY RUN — ' if DRY else ''
print(f'\n{mode}{modified} files updated, {skipped} skipped')
