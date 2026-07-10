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
- [x] automation/github-actions
  - Audit (2026-07-09): KB has 5 top-level sections (architecture, deploy, operations,
    security, troubleshooting) plus a learning-path guide. Content covers: runner specs
    and execution model, concurrency/artifacts/platform limits (architecture); reusable
    workflows, composite actions, action version pinning, caching, matrix strategy
    (design-standards); basic pipeline setup and self-hosted runner registration (deploy);
    workflow/build/publish procedures and CLI reference (operations); hardening, access
    control, authentication (PAT/token), encryption/secrets masking (security); known
    issues, diagnostics, escalation (troubleshooting). No dedicated content yet on
    authoring/publishing custom actions (JS/Docker/composite action.yml metadata,
    Marketplace publishing), OIDC cloud federation detail, or enterprise-scale governance
    (org policies, IP allow lists, artifact attestations/SLSA provenance).
  - Cert research (2026-07-09): Real, named, published cert exists — **GitHub Actions
    Certification (exam GH-200)**, an official GitHub certification administered via
    Microsoft Learn / Pearson VUE (confirmed on GitHub's own docs.github.com
    certifications page). Intermediate level, 100 minutes, proctored. Skills measured as
    of January 2026, five domains: Author and manage workflows (20–25%) — triggers/events,
    workflow_dispatch inputs, workflow_call, jobs/steps/conditionals, service containers,
    matrix strategy, YAML anchors/aliases, contexts, expressions, caching, artifacts,
    GITHUB_STEP_SUMMARY; Consume and troubleshoot workflows (15–20%) — diagnosing failed
    runs, matrix expansion analysis, starter vs reusable workflows vs composite actions;
    Author and maintain actions (15–20%) — action types (JS/Docker/composite), metadata,
    Marketplace distribution, versioning; Manage GitHub Actions for the enterprise
    (20–25%) — org policies, runner groups/IP allow lists, encrypted secrets/variables at
    org/repo/env scope; Secure and optimize automation (10–15%) — environment protections,
    script-injection mitigation, GITHUB_TOKEN lifecycle, OIDC federation, SHA pinning,
    artifact attestations/SLSA, caching/retention for cost.
    Source (primary, GitHub's own confirmation): https://docs.github.com/en/get-started/showcase-your-expertise-with-github-certifications/about-github-certifications
    Source (official exam study guide, administered on GitHub's behalf via Microsoft
    Learn/Pearson VUE): https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-200
    Source (official exam page): https://learn.microsoft.com/en-us/credentials/certifications/github-actions/
  - Gap vs blueprint: biggest gap is "Author and maintain actions" (15–20% of exam) —
    KB has no dedicated custom-action-authoring content at all. Also missing: OIDC
    federation walkthrough (mentioned only implicitly), artifact attestations/SLSA
    provenance, enterprise-level org policy/IP allow list detail, YAML anchors/aliases,
    GITHUB_STEP_SUMMARY job summaries. Flagged for Phase B.
- [ ] automation/powershell
- [ ] automation/python
- [ ] automation/terraform

### Backup
- [ ] backup/products/commvault
- [ ] backup/products/netbackup
- [ ] backup/products/veeam

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
