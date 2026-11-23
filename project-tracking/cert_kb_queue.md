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
- [x] automation/powershell
  - Audit (2026-11-23): KB has 5 top-level sections (architecture, deploy, operations,
    security, troubleshooting) plus learning-path, FAQ, release notes, known issues
    (27 pages, ~3,950 lines). Strong on: PS 7 vs 5.1 engine/runspaces/modules
    (architecture); WinRM/SSH remoting and ports; PowerCLI + AD/disk integrations;
    error handling, trace/transcript/script-block-logging diagnostics; module manifest
    creation + PSGallery publishing; scheduled tasks; JEA/execution policy/hardening;
    approved verbs and basic Pester (design-standards). Thin or missing: CIM sessions
    (`New-CimSession`), providers/PSDrives, background jobs (`Start-Job`/`Receive-Job`/
    `Start-ThreadJob`), pipeline parameter binding (ByValue/ByPropertyName), Microsoft
    Graph / Exchange Online / Az module administration (zero coverage), PowerShell
    classes, PSResourceGet, PSScriptAnalyzer as a lint gate.
  - Cert research (2026-11-23): **No formal cert.** Microsoft has no PowerShell-specific
    certification exam; PowerShell is only tested incidentally inside role exams
    (e.g. AZ-800/AZ-801 → AZ-802 Windows Server, MS-102 Microsoft 365).
    **Fallback: Microsoft's official instructor-led course AZ-040T00-A "Automate
    Administration with PowerShell"** (Advanced, 5 days, Windows Server/Administrator
    role, page updated 2025-12-04, no exam attached; the vendor page lists none).
    Its 11 modules in order: get started with Windows PowerShell; system administration
    tasks; the pipeline; providers & PowerShell drives; CIM/WMI; variables, arrays &
    hash tables; create & modify scripts; administer remote computers; manage cloud
    (Azure) resources; manage Microsoft 365 services; background jobs & scheduled jobs.
    Source (primary, vendor, verified via direct fetch): https://learn.microsoft.com/en-us/training/courses/az-040t00
    Supplementary bar for the authoring/craft side that AZ-040 doesn't cover (advanced
    functions, module layout, naming, error-handling, docs): Microsoft's own cmdlet
    development guidelines + the community PoshCode "PowerShell Practice and Style"
    guide (unofficial but the widely cited community standard, ~2.4k GitHub stars).
    Sources: https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/strongly-encouraged-development-guidelines
    and https://github.com/PoshCode/PowerShellPracticeAndStyle
  - Gap vs fallback bar: biggest gaps are AZ-040's cloud modules (Az for Azure
    resources, Microsoft Graph/Exchange Online for M365 — zero KB coverage), plus
    providers/PSDrives, CIM sessions, background jobs, and pipeline binding mechanics.
    Craft side: no PowerShell classes coverage; PSScriptAnalyzer/CI lint gate and
    PSResourceGet only mentioned in passing (one page each). Flagged for Phase B.
  - site_audit (2026-11-23): 59/65 clean. This run only edited this queue file
    (outside `docs/`), so none of the failures are from it. Besides Check 59's known soft
    heuristic, 5 checks fail and all predate this run: Check 6 (docs/goals,
    docs/goals-overview, docs/p, docs/p/bnl1n2i8 have no index.md; created 01:53, before
    this run), Check 35 (2,521 "See also" links flagged, e.g.
    `architecture/ports.md` → `../how-it-works/`; possibly the checker misresolving
    non-index pages, needs a look), Check 45 (vxrail cluster-software-stack.md missing
    *Applies to:*), Check 64 (confluence common-issues prose block), Check 65 (6 SVG
    vertical-overflow/occlusion; run scripts/svg_vertical_bugs_fix.py). Left for a
    dedicated fix session, not fixed here per the one-item rule.
- [x] automation/python
  - Audit (2026-11-23): KB has 5 top-level sections (architecture, deploy, operations,
    security, troubleshooting) plus learning-path, FAQ, release notes, known issues
    (27 pages, ~5,530 lines). Strongly ops-focused. Strong on: venv/pyenv install and
    upgrade, dependency pinning, pip-audit; REST/API clients with pagination/retry,
    requests/boto3/paramiko; logging and job design; pytest + pre-commit + ruff/black
    (design-standards); pdb/traceback diagnostics; secrets/Vault, `cryptography`, file
    permissions; pandas/CSV/Excel/Jinja2 reports. Thin or missing on the language itself:
    zero coverage of `yield`, context managers (`with` only in passing, no
    `__enter__`/`contextlib`), dataclasses, closures, `match-case`, properties/
    descriptors, ABCs, metaclasses, `ExceptionGroup`/`except*`, copy/deepcopy,
    pickle/shelve, `sqlite3`, PEP 257 docstrings; generators, decorators, type hints,
    classes/inheritance (only custom exception classes), PEP 8, and XML each get one or
    two passing mentions at most; comprehensions get none.
  - Cert research (2026-11-23): No vendor cert (the PSF does not certify). The
    recognised independent body is the **OpenEDG Python Institute**, whose ladder is
    PCEP → PCAP → PCPP1 → PCPP2. Both of the relevant exams were revised this month,
    so the notes below use the new versions.
    **Target bar: PCPP1-32-102 "Certified Professional Python Programmer: Software
    Development"** (blueprint v1.3, revised 2026-11-06; replaces PCPP1-32-101). 45 Qs,
    72% pass, no formal prerequisite (PCAP-level knowledge recommended). The cert page
    says 65 minutes, but the syllabus FAQ says the final blueprint doesn't set a duration.
    Seven sections: (1) Advanced OOP & core syntax 15% (special methods, function/class
    decorators, class/static methods, properties & descriptors, subclassing built-ins);
    (2) Abstract classes, metaclasses & exception groups 12% (ABCs, metaprogramming,
    exception chaining, `ExceptionGroup`/`except*`); (3) Data modelling, object mechanics
    & type systems 19% (shallow/deep copy, pickle/shelve, CSV/JSON/XML, type hints,
    dataclasses, context managers); (4) Text processing, formatting & security 12%
    (frozenset/frozen dataclasses, regex, advanced formatting, injection risks &
    templating incl. `string.Template`/t-strings); (5) Code development & maintenance 15%
    (PEPs/Zen, PEP 8, PEP 257, linters/formatters, dead code & coverage);
    (6) Services & logging 15% (networking, HTTP, REST, `sqlite3`, application and
    structured logging); (7) Collaborative engineering & AI-assisted development 12%
    (VCS strategy, technical risk, AI-assisted workflows and their governance).
    Source (primary, certifying body, verified via direct fetch): https://pythoninstitute.org/pcpp1-exam-syllabus
    (cert page: https://pythoninstitute.org/pcpp1)
    **Foundation bar: PCAP-31-04 "Certified Associate Python Programmer"** (blueprint
    v1.5, revised 2026-11-02; replaces PCAP-31-03). 42 Qs, 65 min, 72% pass. Six sections:
    modules & packages 12%, exceptions 12%, strings 9.5%, OOP 28.5%, advanced constructs &
    I/O 24% (comprehensions, `match-case`, lambda/map/filter, closures, file I/O,
    `pathlib`), testing/debugging/collaboration/AI assistance 14%.
    Source (primary, verified via direct fetch): https://pythoninstitute.org/pcap-exam-syllabus
  - Gap vs blueprint: the KB covers PCPP1 §6 (HTTP/REST/logging) and parts of §5
    (linters, pytest/coverage) well. §1–§4 are almost entirely missing (decorators,
    descriptors, ABCs/metaclasses, exception groups, dataclasses, type hints, context
    managers, copy semantics, serialization, regex/templating injection safety), as is
    §7 (AI-assisted development governance). On the PCAP side: closures, comprehensions,
    `match-case`, packages/namespaces, inheritance/MRO. Flagged for Phase B; it may
    need a new "language" subsection, since the existing tree is ops-oriented.
  - site_audit (2026-11-23): 67/67 clean (full run, no exceptions triggered). This run
    only edited this queue file.
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
- [ ] security/products/cyberark
- [ ] security/products/venafi

### Storage — Ceph
- [ ] storage/products/ceph

### Storage — Dell
- [ ] storage/products/dell/apex-storage-as-a-service
- [ ] storage/products/dell/cloudiq
- [ ] storage/products/dell/cod
- [ ] storage/products/dell/data-domain
- [ ] storage/products/dell/dell-aiops
- [ ] storage/products/dell/ecs
- [ ] storage/products/dell/fod
- [ ] storage/products/dell/powermax
- [ ] storage/products/dell/powerpath
- [ ] storage/products/dell/powerscale
- [ ] storage/products/dell/powerstore
- [ ] storage/products/dell/recoverpoint
- [ ] storage/products/dell/srdf-a
- [ ] storage/products/dell/srdf-s
- [ ] storage/products/dell/unity
- [ ] storage/products/dell/vplex

### Storage — NetApp
- [ ] storage/products/netapp/insightiq
- [ ] storage/products/netapp/keystone
- [ ] storage/products/netapp/ontap
- [ ] storage/products/netapp/snapcenter
- [ ] storage/products/netapp/snapmirror
- [ ] storage/products/netapp/superna-eyeglass

### Storage — Pure
- [ ] storage/products/pure/evergreen
- [ ] storage/products/pure/evergreen-one
- [ ] storage/products/pure/flasharray
- [ ] storage/products/pure/flashblade
- [ ] storage/products/pure/pure1

### Virtualization
- [ ] virtualization/openshift
- [ ] virtualization/vmware/products/aria-automation
- [ ] virtualization/vmware/products/aria-operations
- [ ] virtualization/vmware/products/aria-operations-for-logs
- [ ] virtualization/vmware/products/aria-operations-for-networks
- [ ] virtualization/vmware/products/aria-suite-lifecycle
- [ ] virtualization/vmware/products/esxi
- [ ] virtualization/vmware/products/horizon
- [ ] virtualization/vmware/products/nsx
- [ ] virtualization/vmware/products/powercli
- [ ] virtualization/vmware/products/srm
- [ ] virtualization/vmware/products/tanzu
- [ ] virtualization/vmware/topics
- [ ] virtualization/vmware/products/vcenter
- [ ] virtualization/vmware/products/vmware-cloud-foundation
- [ ] virtualization/vmware/products/vsan
- [ ] virtualization/vmware/products/vsphere-replication
- [ ] virtualization/vmware/products/vxrail

## Phase B+ (not queued yet)

Gap analysis, content fill, practice questions, labs, tutorials, etc. — queued once
Phase A is far enough along to know what's actually being targeted per section. Don't
jump ahead of Phase A.
