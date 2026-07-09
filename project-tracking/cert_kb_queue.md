# Certification-Grade KB — Daily Queue

Not part of the published site (excluded from mkdocs nav / not in `docs/`). This is the
working task queue for `[[project-certification-grade-kb]]` in Claude's memory system.

**Daily workflow for whoever picks up the next item** (per user instruction 2026-07-09):
1. Audit current state relevant to this item.
2. Prechecks — validate assumptions before doing the work.
3. Do ONE trial/item from the list below.
4. Test it for errors.
5. Commit it.
6. Run the full `site_audit.py` — 100%.
7. If clean: proceed to mark this item done, stop for the day.
8. If a bug is found: add a permanent check for it to `site_audit.py`, script the fix,
   fix it, re-audit, THEN mark this item done, stop for the day.
9. Do not start a second queue item in the same run — one per day, bounded token usage.

Check off `[x]` as items complete. Leave a one-line result note after each.

## Phase A — cert-blueprint research (one section per day)

For each: does a real, named, published certification exam exist for this product? If
yes — name it, find its official objectives/blueprint. If no — define the fallback
"expert-level" bar (vendor's own official training curriculum, or a well-regarded
community standard). Research via WebSearch, verify, don't assume from memory.

### Automation
- [x] automation/ansible
  - Audit (2026-07-09): KB has 5 top-level sections (architecture, deploy, operations,
    security, troubleshooting) plus a learning-path guide. Content is operationally
    focused (AWX/AAP admin, playbook ops, RBAC, troubleshooting) — no exam-blueprint-style
    content yet (no dedicated collections/EE authoring deep-dive, no Git-workflow-for-
    playbooks page, no filters/plugins/lookup-plugin reference).
  - Cert research (2026-07-09): Real, named, published cert exists — **Red Hat Certified
    Specialist in Developing Automation with Ansible Automation Platform (EX374)**, based
    on Ansible Automation Platform 2.5, counts toward RHCA. Official objectives (verified
    via direct fetch of the vendor page): Git repo management for playbooks; inventory
    variable structuring (host/group vars, special vars, dynamic overrides); task
    execution control (privilege escalation, selective task runs); filters/lookup/query
    plugins for external data and networking-variable manipulation; task delegation
    (`delegate_to`, fact delegation); content collections (create/install/publish);
    execution environments (build/run/upload/use in controller); advanced inventories &
    credentials (dynamic inventory from IdM/DB, machine & source-control credentials);
    automation controller operation (run playbooks, pull from Git/hub, run in an EE).
    Source (primary, vendor): https://www.redhat.com/en/services/training/red-hat-certified-specialist-developing-automation-ansible-automation-platform-exam?section=objectives
  - Gap vs blueprint: KB's `operations/` and `security/` cover controller RBAC/creds
    reasonably well already; missing dedicated coverage of collections authoring, EE
    build/publish workflow, and lookup/filter plugin usage — flagged for Phase B.
- [ ] automation/github-actions
- [ ] automation/powershell
- [ ] automation/python
- [ ] automation/terraform

### Backup
- [ ] backup/commvault
- [ ] backup/netbackup
- [ ] backup/veeam

### Cloud
- [ ] cloud/aws
- [ ] cloud/aws/evs
- [ ] cloud/azure

### Compute
- [ ] compute/linux
- [ ] compute/linux/mysql
- [ ] compute/linux/postgresql
- [ ] compute/windows-server
- [ ] compute/windows-server/active-directory
- [ ] compute/windows-server/sql-server

### ITSM
- [ ] itsm/confluence
- [ ] itsm/git
- [ ] itsm/jira
- [ ] itsm/servicenow

### SAN
- [ ] san/brocade/fabric-os
- [ ] san/brocade/sannav
- [ ] san/cisco/cisco-dcnm
- [ ] san/cisco/mds
- [ ] san/cisco/nexus-dashboard

### Security
- [ ] security/certificates
- [ ] security/cyberark
- [ ] security/venafi

### Storage — Ceph
- [ ] storage/ceph

### Storage — Dell
- [ ] storage/dell/apex-storage-as-a-service
- [ ] storage/dell/cloudiq
- [ ] storage/dell/cod
- [ ] storage/dell/data-domain
- [ ] storage/dell/dell-aiops
- [ ] storage/dell/ecs
- [ ] storage/dell/fod
- [ ] storage/dell/powermax
- [ ] storage/dell/powerpath
- [ ] storage/dell/powerscale
- [ ] storage/dell/powerstore
- [ ] storage/dell/recoverpoint
- [ ] storage/dell/srdf-a
- [ ] storage/dell/srdf-s
- [ ] storage/dell/unity
- [ ] storage/dell/vplex

### Storage — NetApp
- [ ] storage/netapp/insightiq
- [ ] storage/netapp/keystone
- [ ] storage/netapp/ontap
- [ ] storage/netapp/snapcenter
- [ ] storage/netapp/snapmirror
- [ ] storage/netapp/superna-eyeglass

### Storage — Pure
- [ ] storage/pure/evergreen
- [ ] storage/pure/evergreen-one
- [ ] storage/pure/flasharray
- [ ] storage/pure/flashblade
- [ ] storage/pure/pure1

### Virtualization
- [ ] virtualization/openshift
- [ ] virtualization/vmware/aria-automation
- [ ] virtualization/vmware/aria-operations
- [ ] virtualization/vmware/aria-operations-for-logs
- [ ] virtualization/vmware/aria-operations-for-networks
- [ ] virtualization/vmware/aria-suite-lifecycle
- [ ] virtualization/vmware/esxi
- [ ] virtualization/vmware/horizon
- [ ] virtualization/vmware/nsx
- [ ] virtualization/vmware/powercli
- [ ] virtualization/vmware/srm
- [ ] virtualization/vmware/tanzu
- [ ] virtualization/vmware/topics
- [ ] virtualization/vmware/vcenter
- [ ] virtualization/vmware/vmware-cloud-foundation
- [ ] virtualization/vmware/vsan
- [ ] virtualization/vmware/vsphere-replication
- [ ] virtualization/vmware/vxrail

## Phase B+ (not queued yet)

Gap analysis, content fill, practice questions, labs, tutorials, etc. — queued once
Phase A is far enough along to know what's actually being targeted per section. Don't
jump ahead of Phase A.
