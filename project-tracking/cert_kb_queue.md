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
- [x] automation/terraform
  - Audit (2026-11-24): KB has 5 top-level sections (architecture, deploy, operations,
    security, troubleshooting) plus learning-path, FAQ, release notes, known issues
    (27 pages, ~6,550 lines; *Applies to: Terraform 1.x*). Strongly ops-focused. Strong
    on: core workflow (init/plan -out/apply), remote backends and state locking
    (S3 backend, `force-unlock`), CLI state surgery (`state list/show/mv/rm/pull/push`),
    `terraform import` CLI, workspaces, `.terraform.lock.hcl` and `required_providers`,
    drift detection, TF_LOG diagnostics, tfvars, OIDC and static-analysis scanners
    (tflint/checkov/tfsec), Sentinel mentioned in hardening/escalation. Thin or missing
    on the language: zero mentions of `for_each`, `dynamic` blocks, `count.index`/
    `each.key`, provider `alias`, config-driven `import {}`/`removed {}`/`check {}`
    blocks, `precondition`/`postcondition`, `terraform test`, `templatefile`,
    `-replace`, ephemeral values, Terraform MCP server, HCP Terraform run tasks;
    `moved {}`, variable `validation`, `lifecycle`, `depends_on`, HCL functions,
    `terraform_remote_state`/`tfe_outputs`, and dynamic provider credentials get one to
    four passing mentions each.
  - Cert research (2026-11-24): Real, named, published certs exist. HashiCorp offers
    Terraform certifications "at three levels" (per its certifications overview page):
    **Foundation: Terraform Associate (004)**, 1 hr, multiple choice, online proctored,
    tests Terraform 1.12, $70.50, expires after 2 yrs. 8 domains: IaC concepts;
    Terraform fundamentals (providers, state); core workflow (init/validate/plan/apply/
    destroy/fmt); configuration (resource vs data, references, variables/outputs,
    complex types, expressions/functions, dependencies, custom conditions, sensitive
    data/Vault); modules (sourcing, variable scope, usage, versioning); state (local
    backend, locking, remote backend, drift); maintenance (import, inspect state with
    the CLI, verbose logging); HCP Terraform (runs, collaboration/governance,
    workspaces/projects, CLI integration). New vs 003: `depends_on`/
    `create_before_destroy`, custom conditions, ephemeral values/write-only arguments,
    projects.
    Sources (primary, vendor, verified via direct fetch): https://developer.hashicorp.com/certifications/terraform-associate
    and https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-review-004
    **Mid tier: Terraform Infrastructure Engineer Professional (002)**, 90 min,
    multiple choice, tests Terraform 1.15, $200, expires after 2 yrs. 40 objectives in
    7 domains, no published weightings: scalable configuration design (incl. tracing
    `for_each`, predicting function output, advanced configs, providers, using the
    Terraform MCP server with AI coding agents); state & backend operations (remote
    state, drift, dependency chains before upgrades, upgrading Terraform across
    environments); lifecycle operations (plan/apply/import, multi-environment,
    troubleshooting, provider/module versions); CI/CD & automation (pipelines,
    deployment strategies, dynamic provider credentials, `.tfvars`/`auto.tfvars`
    precedence); security & governance (secrets, rotation, pipeline identities,
    policy rules, risky-change mitigation); modules & registry (when to refactor,
    module contract, registry, `terraform test` unit tests); HCP Terraform/Enterprise
    operations (usage/cost tracking, multi-env, workspace version upgrades, policy as
    code in CI/CD).
    Sources (primary, verified via direct fetch): https://developer.hashicorp.com/certifications/terraform-infrastructure-engineer-professional
    and https://developer.hashicorp.com/terraform/tutorials/certification-infra-professional/cert-pro-review
    **Top tier (target bar): Terraform Authoring & Operations Advanced**: lab-based
    scenarios plus multiple choice, 4 hrs, AWS or Azure version (same credential),
    $295 with a free retake, expires after 2 yrs, needs production experience. Its
    cert page still says it tests **Terraform 1.6**, older than the other two. 6
    domains: resource lifecycle (`init`/`plan`/`apply`/`destroy` and their options,
    state incl. import and drift); dynamic configuration (validation, data sources,
    HCL functions, meta-arguments, complex-typed variables/outputs, sensitive
    data/Vault); collaborative workflows (version constraints, remote state,
    automation, sharing data across configurations/workspaces); modules (create, use,
    refactor/version, refactor existing config into modules); providers (plugin
    architecture, aliasing/versioning/sourcing/upgrades, authentication,
    troubleshooting); HCP Terraform (run workflow, workspaces/access, provider
    credentials, policy as code; this domain is multiple choice only).
    Sources (primary, verified via direct fetch): https://developer.hashicorp.com/certifications/terraform-advanced
    and https://developer.hashicorp.com/terraform/tutorials/pro-cert/adv-review
    Overview: https://developer.hashicorp.com/certifications
    Rationale: Advanced is the highest-tier and hands-on bar, so it is the target.
    Because it pins Terraform 1.6, Phase B should also cover the newer Associate 004 /
    Professional 002 topics (custom conditions, ephemeral/write-only, `terraform test`,
    MCP server) so the KB doesn't freeze at 1.6.
  - Gap vs blueprint: the KB covers the operational side well (lifecycle CLI, remote
    state/locking, CLI state inspection, drift, TF_LOG troubleshooting, OIDC). The big
    gap is the authoring side, which carries the most weight in all three exams:
    meta-arguments (`for_each`, `dynamic` blocks, `lifecycle`, `depends_on`; `count =`
    appears in just one example),
    HCL functions and expressions, provider aliasing, variable validation and custom
    conditions, config-driven `import`/`moved`/`removed` refactoring, module authoring
    and refactoring config into modules, `terraform test`, sharing data across
    configurations (`terraform_remote_state`/`tfe_outputs`), HCP Terraform
    runs/run tasks/dynamic provider credentials/policy as code, ephemeral values, and
    the Terraform MCP server. Flagged for Phase B; it probably needs a new
    "language/authoring" subsection.
  - site_audit (2026-11-24): 70/70 clean (full run, ~14 min, no exceptions triggered).
    This run only edited this queue file.

### Backup
- [x] backup/products/commvault
  - Audit (2026-11-24): 27 pages, ~2,950 lines in the standard 5 sections plus a
    learning path. Content is CommCell-era and on-prem: CommServe/MediaAgent
    topology, storage policies (36 mentions), subclients, DDB health, CV_DIAG, ports,
    escalation. No exam-blueprint content yet.
  - Cert research (2026-11-24): Real, named certifications exist, but **Commvault
    publishes no exam objectives or blueprint**. The program was rebuilt in 2026 (blog
    dated 2026-05-11) into four "Commvault Cloud" tiers on Readiverse Academy:
    **Practitioner** ("foundational platform and resilience knowledge"; needs the
    Commvault Cloud Administrator - 2026 course and exam plus Cyber Resilience - 2026
    and one workload course), **Specialist** ("expanded operational and security
    depth"), **Professional** ("advanced recovery and workload expertise", including
    Cloud Rewind or Cleanroom Recovery coursework), and **Expert** ("full cloud
    engineering and resilience leadership": Cloud Engineer coursework, two Advanced
    Feature courses with assessments, Cloud Rewind, Cleanroom Recovery). Tiers are
    earned by coursework, hands-on labs and validated assessments. No question count,
    duration, passing score or validity is published. Expert launched around Sep 2026,
    and badges were still being issued in Nov 2026. "There is no direct progression"
    from the old tracks. The old Professional/Engineer/Expert certs (with Command
    Center and CommCell Console tracks) stay valid but reach end of life as their
    releases retire. "Commvault Certified Engineer - 2027" (launched 08 Oct 2026) is
    still in the catalog.
    Sources (verified via direct fetch): https://www.commvault.com/blogs/introducing-new-readiverse-courses-and-certification-programs
    https://community.commvault.com/readiverse-academy-60/new-readiverse-academy-certification-tiers-are-here-11844
    https://community.commvault.com/readiverse-academy-60/readiverse-academy-customer-course-catalog-10789
    Not readable: readiverse.commvault.com (JavaScript/login portal), and the
    commvault.com/download-pdf/40151 "data sheet" (a design file, no content).
  - **Fallback bar (no published blueprint):** use Commvault's own official
    curriculum. Target the **Commvault Cloud Expert** tier and the courses its tiers
    are built from in the customer catalog: Cloud Administrator - 2026, Cyber
    Resilience - 2026, Core Security, MediaAgent Advanced, Indexing Advanced, Working
    with Support, Cloud Rewind, Cleanroom Recovery, Threat Scan, Risk Analysis, Auto
    Recovery, workload courses (VMware, M365, Entra ID/AD, Kubernetes, SQL/Oracle,
    Salesforce, Clumio, cloud VMs) and Storage Accelerator.
  - Gap vs bar: the KB is built on the legacy CommCell/storage-policy model, while
    the 2026 curriculum is built on Command Center and plans. Content with zero
    coverage: cyber-resilience features (Threat Scan, Risk Analysis, Cleanroom
    Recovery, Cloud Rewind, Auto Recovery), SaaS workloads (M365, Salesforce,
    Clumio), Storage Accelerator and Arlie. Barely covered: Kubernetes (1 mention),
    Entra ID/AD, Oracle/SQL agents, KMS, immutability/air gap, multi-tenancy. Phase B
    should first reframe procedures from storage policies to plans, then add a
    "cyber resilience" subsection and per-workload protection pages. Recheck
    Readiverse (logged in) for real objectives before Phase B starts.
  - site_audit (2026-11-24): 70/70 clean (full run, no exceptions). This run only
    edited this queue file.
- [x] backup/products/netbackup
  - Audit (2026-11-25): 27 pages, ~4,160 lines in the standard 5 sections plus a
    learning path. It is strong on classic operations: three-tier topology, ports,
    MSDP (73 mentions), catalog backup/recovery, bpexpdate, VxUL logs, nbsu, error
    codes, DD Boost. It is branded Veritas throughout (0 mentions of Cohesity, which
    has owned NetBackup since Dec 2024). No exam-blueprint content yet.
  - Cert research (2026-11-25): A real, named, published cert exists: **Cohesity
    Certified Protection Professional - NetBackup, exam COH-284** (the URL slug still
    says vcs-284). 105 min, $200, 65% pass mark, valid 2 yrs, retake every 14 days,
    no prerequisites, proctored onsite or remote, 9 months' experience recommended.
    Recommended courses: NetBackup 11.0: Administration (5 days) and NetBackup 10.0:
    Advanced Administration (5 days). A sibling exam, **CCPP - NetBackup and NetBackup
    Appliances** (COH-285), is the superset. There is no Expert/Architect NetBackup
    tier. Cohesity's top tier is Security Specialist (CCSS), which covers Cohesity's
    own platform, not NetBackup.
    Domains (official prep guide 1000108-001-EN, dated 9-2025):
    **S1 Configure (31%)**: primary/media/client host properties incl. security
    certificates; disk, cloud storage and storage unit groups; backup policies and
    protection plans; synthetic backups, TIR, multiple data streams, checkpoint
    restart, disk staging, SLPs, AIR, Isolated Recovery Environment, Accelerator;
    dedup options (media-server and client-side dedup, optimized duplication, KMS,
    MSDP Cloud, WORM, Universal Shares, Snapshot Manager, storage servers); catalog
    backup config.
    **S2 Monitor and Maintain (36%)**: image management (verify, expire, import,
    manual duplicate); disk and cloud storage management; reports; job control
    (prioritize, cancel, suspend, resume, restart, retry); restores; security (RBAC,
    host ID certs); updates via VxUpdate; Anomaly and Malware Detection.
    **S3 Tune (10%)**: analyze, optimize and tune NetBackup.
    **S4 Troubleshoot (23%)**: status codes and job details; devices and media, plus
    primary/media/client connectivity; DR issues incl. catalog recovery.
    The experience list also covers appliances (CLISH, Appliance Web Console, AMS),
    NetBackup for VMware and Snapshot Manager. The sample questions show how deep it
    goes: exact paths (anomaly_detection folder), SLP defaults
    (SLP.MIN_SIZE_PER_REPLICATION_JOB), client-side dedup attribute combinations,
    stream math, status 96/2111, frozen tapes via bptm, default RBAC roles.
    Sources (primary, read in a real browser because cohesity.com returns 403 to
    plain fetches): https://www.cohesity.com/academy/certification/exam-vcs-284/
    https://www.cohesity.com/content/dam/cohesity/resource-assets/datasheets/ccpp-netbackup-certification-exam-preparation-guide-en.pdf
    https://www.cohesity.com/academy/certification/
    Target bar: COH-284 domains, plus the COH-285 appliance extras (CLISH, AMS).
  - Gap vs blueprint: the catalog, MSDP, logs and status-code basics are covered.
    Zero coverage: protection plans, synthetic backups, TIR, multiple data streams
    (and the stream/job math), checkpoint restart, disk staging, IRE, client-side
    dedup, optimized duplication, WORM/immutability, Universal Shares, Snapshot
    Manager, bpduplicate/manual duplication, VxUpdate, Anomaly Detection, CLISH, Smart
    Meter, deployment policies. Thin (1-3 mentions): host properties, SLPs (1!),
    storage unit groups, RBAC, malware scan, multiplexing, VMware transport modes,
    tuning (buffers), Accelerator, KMS, volume pools/scratch, tape daemons
    (bptm/vmd/ltid). Phase B should rebrand Veritas to Cohesity, and add a
    "policies and SLPs" deep-dive (S1 is the core), a job-control and image-management
    page, a security page (RBAC, certs, anomaly/malware, WORM, IRE), a tuning page and
    an appliances page.
  - site_audit (2026-11-25): 70/70 clean (full run, no exceptions). This run only
    edited this queue file.
- [x] backup/products/veeam
  - Audit (2026-11-25): 28 pages, ~3,360 lines in the standard 5 sections plus a
    learning path, release notes and FAQ. Pages say "Applies to: Veeam Backup &
    Replication 12.x" (1 mention of v13). It is strong on VBR VMware basics: deploy
    walkthrough (proxies, transport modes, repos, first job), SOBR/capacity tier,
    S3 Object Lock and the hardened Linux repo, SureBackup/virtual labs, Instant VM
    Recovery, CBT reset, logs and support bundle, escalation. No exam-blueprint
    content yet. The release-notes table has dates that look wrong (it lists 12.1 as
    2024-Q1 and 11.0 as 2021-Q2; 12.1 shipped Dec 2023 and v11 shipped Feb 2021).
    Re-verify those dates in Phase B.
  - Cert research (2026-11-25): A real, named, published cert exists: **Veeam
    Certified Engineer Plus (VMCE+) v13**. The exam spec says it "aligns to Veeam
    Data Platform 13 capabilities" and covers VBR, Veeam ONE and Veeam Recovery
    Orchestrator. Veeam's FAQ says the old VMCE (v12) and VMCA are retired. A
    community announcement says VMCE+ was released 2026-06-01. Format: 100
    multiple-choice items, all scored; 150 min (+30 min for non-native English
    speakers); scaled score 300-900 with a 724 pass mark; English (US) only; taken
    through Pearson Professional Assessments at a test center or online. Credentials
    do not expire. Retakes wait 24 h after the 1st fail and 14 days after attempts
    2-4, with a 12-month wait after attempts 5 and 9. You must first complete 3
    courses: VBR: Configure, Manage and Recover; Veeam Data Platform: Monitor,
    Manage, Analyze (Veeam ONE); and Veeam Data Platform: Scale, Automate, Secure
    (Recovery Orchestrator). The spec recommends 2+ years of hands-on experience.
    The next tier up is **Veeam Certified Security Expert (VMCSE)**, which needs
    VMCE+ plus the Enterprise Data Security course. The vendor page still says
    "coming soon" and one community thread claims a pass, so its status is
    unconfirmed and it is not the target here.
    Domains (official exam spec PDF, dated 5.20.2026; blueprint from a JTA by Alpine
    Testing Solutions):
    **Fundamentals, Strategy, and Design (14%)**: RPO/RTO, transport modes, ports,
    permission requirements; workload protection requirements; design to business
    requirements.
    **Deployment, Configuration, and Security (20%)**: hardened backup
    infrastructure; deploy components; initial security config; initial system
    config; secure, reliable backup infrastructure.
    **Data Protection and Maintenance (26%)**: VM backup and replication jobs;
    NAS/unstructured data and offsite copies; physical workloads, cloud machines,
    enterprise plug-ins; plan and maintain infrastructure; platform maintenance.
    **Recovery and Verification (15%)**: perform and validate restores; app-item
    restores with Veeam Explorer; SureBackup.
    **Analytics, Monitoring, and Observability (13%)**: monitor and resolve backup
    ops; environment health and remediation; reports; dashboards and alarms (Veeam
    ONE).
    **Orchestration and DR (10%)**: configure Recovery Orchestrator; recovery plans;
    Orchestrator reports; DataLabs verification.
    The weights in Veeam's own PDF add up to 98%, not 100%. That is copied exactly,
    not a typo here.
    Sources (primary, vendor): https://www.veeam.com/veeam_certified_engineer_plus_v13_exam_guide_ds.pdf
    https://www.veeam.com/vmce-certification.html
    https://www.veeam.com/support/training/vmce-training-faq.html
    Target bar: the VMCE+ v13 domains above.
  - Gap vs blueprint: The KB is pinned to 12.x, but the exam is v13. Phase B needs a
    v13 pass first (the Linux software appliance, what changed). Zero coverage:
    Veeam Recovery Orchestrator (1 passing mention), recovery plans, Orchestrator
    reports, NAS/unstructured backup (3 mentions), M365 and enterprise plug-ins
    (Oracle RMAN/SAP), backup chain formats (forever forward / reverse incremental /
    GFS, 1 mention), compact/defrag maintenance, Four-Eyes authorization, Secure
    Restore / malware detection (1 mention), the gateway server, and Cloud Connect.
    Thin: Veeam ONE dashboards (2) and reports, physical/agent workloads, cloud
    machines, Veeam Explorer (5), permissions (1), mount server (1), WAN
    accelerators (2), Archive Tier (1), CDP (3). Phase B should add a "backup
    methods and job settings" deep-dive (D3 is the biggest), a Veeam ONE
    monitoring and reporting page, a Recovery Orchestrator/DataLabs page, a
    NAS/agents/plug-ins page, and fold Four-Eyes, MFA, malware detection and Secure
    Restore into security.
  - site_audit (2026-11-25): 70/70 clean (full run, no exceptions). This run only
    edited this queue file.

### Cloud
- [x] cloud/aws
  - Audit (2026-11-25): 109 pages, ~17,600 lines (EVS sub-section excluded; it has its
    own queue item). Sections: architecture, compute, storage, networking, identity,
    security, governance, monitoring, backup, cost, deploy, operations, cli-reference,
    troubleshooting, plus a learning path, FAQ and release notes. Pages say "Applies to:
    AWS". It is strong on the infra-admin core: VPC/subnets/route tables/NAT/IGW/SGs/
    NACLs/endpoints/flow logs/Route 53/ELB, IAM (roles, policies, cross-account, access
    keys, Identity Center 7 pages, SCPs 12), KMS/Secrets Manager/ACM/GuardDuty/Security
    Hub/Inspector, S3 + lifecycle, EBS snapshots, and a deep cost section (Budgets,
    Cost Explorer, RIs, Savings Plans, tags, anomaly detection). There is no database
    sub-section and no application-integration sub-section. No exam-blueprint content.
  - Cert research (2026-11-25): AWS has a full cert ladder, so this section needs a
    chosen target. Target: **AWS Certified Solutions Architect - Associate (SAA-C03)**,
    AWS's canonical infra-design cert and the usual first associate exam. AWS has not
    announced a successor; the official guide on docs.aws.amazon.com is still SAA-C03.
    Format (official guide + cert page): 65 questions (50 scored + 15 unscored, not
    identified); multiple choice (1 of 4) and multiple response (2+ of 5+); 130 min;
    scaled score 100-1,000, 720 to pass, compensatory scoring, no guessing penalty;
    150 USD; valid 3 years; ~1 year hands-on AWS design experience recommended.
    Domains (official guide, "% of scored content"):
    **D1 Design Secure Architectures (30%)**: 1.1 secure access to AWS resources;
    1.2 secure workloads and applications; 1.3 data security controls.
    **D2 Design Resilient Architectures (26%)**: 2.1 scalable and loosely coupled
    architectures; 2.2 highly available and/or fault-tolerant architectures.
    **D3 Design High-Performing Architectures (24%)**: 3.1 storage; 3.2 elastic
    compute; 3.3 databases; 3.4 network architectures; 3.5 data ingestion and
    transformation.
    **D4 Design Cost-Optimized Architectures (20%)**: 4.1 storage; 4.2 compute;
    4.3 database; 4.4 network.
    The guide publishes a non-exhaustive in-scope service list (~130 services across
    analytics, app integration, compute, containers, database, migration, networking,
    security, storage, serverless, ML).
    Secondary target, noted for later: **AWS Certified CloudOps Engineer - Associate
    (SOA-C03)**, the renamed SysOps Administrator exam. Its domains (Monitoring/Logging/
    Remediation 22%, Reliability & BC 22%, Deployment/Provisioning/Automation 22%,
    Security & Compliance 16%, Networking & Content Delivery 18%) fit this KB's ops
    focus closely. It uses the same 50+15 question, 720-pass format. Phase B should
    cover SAA-C03 first; most SOA-C03 gaps are a subset of it plus CloudFormation/SSM
    automation depth.
    Sources (primary, vendor): https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03.html
    https://aws.amazon.com/certification/certified-solutions-architect-associate/
    https://docs.aws.amazon.com/aws-certification/latest/sysops-administrator-associate-03/sysops-administrator-associate-03.html
    Target bar: the SAA-C03 domains above.
  - Gap vs blueprint (pages mentioning each term, out of 109): Zero coverage: Step
    Functions, Global Accelerator, Cognito, Shield, CloudHSM, Storage Gateway,
    DataSync, Snow Family, DMS, Athena, Redshift, Spot Instances, placement groups,
    pilot light / warm standby DR strategies, Compute Optimizer. Thin: Well-Architected
    (1), RPO/RTO (1), SQS (2), SNS (3), EventBridge (3), API Gateway (1), Kinesis (3),
    ElastiCache (1), Aurora (4), DynamoDB (7), read replicas (2), Multi-AZ (5),
    CloudFront (5), WAF (2), PrivateLink (1), Site-to-Site VPN (2), Direct Connect (4),
    Auto Scaling (6), Fargate (2), FSx (4), Glacier (4), Macie (1), Cost and Usage
    Report (1). D1 is mostly covered; D2-D4 are the big gaps because the KB is written
    for operating existing infra, not choosing between services. Phase B should add a
    databases sub-section (RDS/Aurora/DynamoDB/ElastiCache, Multi-AZ vs read replicas),
    an application-integration page (SQS/SNS/EventBridge/Step Functions/API Gateway/
    Kinesis), a resilience & DR-strategies page (backup-restore -> pilot light -> warm
    standby -> multi-site, RPO/RTO, Route 53 failover, Global Accelerator), EC2
    purchasing/placement (Spot, placement groups, Auto Scaling policies), edge security
    (CloudFront, WAF, Shield), hybrid storage/migration (Storage Gateway, DataSync, Snow,
    DMS, Transfer Family), a storage-class/cost decision page, and a Well-Architected
    framing on the learning path.
  - site_audit (2026-11-25): 70/70 clean (full run). This item only edited this queue file.
- [x] cloud/aws/evs
  - Audit (2026-11-25): 27 pages, ~8,580 lines: architecture (how-it-works, design
    standards, integrations, ports), deploy, operations (procedures, health checks,
    backup-restore, install-upgrade, CLI, scripts, FAQ), security (4 pages),
    troubleshooting (5 pages), learning path, release notes. "Applies to" is written
    5 different ways (normalise in Phase B). The whole section is written for VCF
    5.2.1 on i4i.metal (EVS's GA state). Strong on HCX migration (18 pages), Direct
    Connect/Transit Gateway connectivity (12), NSX/vSAN basics, SDDC Manager.
    **Accuracy bugs found (fix in Phase B):** `operations/install-upgrade.md:290-292`
    lists VCF 5.1, 5.0 and 4.5 as EVS versions; EVS never supported them (GA was
    5.2.1). `troubleshooting/escalation.md:122-125` and `operations/cli-reference.md:
    276-278` show EVS hosts as m5.2xlarge/r5.2xlarge; EVS hosts are bare-metal only.
  - Product state (AWS What's New, verified 2026-11-25): GA 2025-08-05 with VCF 5.2.1
    on i4i.metal in 6 regions, "license portability entitlement" (bring your own VCF
    subscription), on-demand/1-yr/3-yr. 2026-01: VCF and ESX version selection (5.2.2
    added). 2026-07-06: VCF 9.0 and 9.1 supported in all EVS regions; the customer has
    "complete control of the installation, operations, and management", with a
    Solutions-for-EVS GitHub repo. 2026-11-17: r7i.metal-24xl/-48xl for VCF 9.x; these
    have no local NVMe, so EVS added VCF external principal storage (FSx for NetApp
    ONTAP); the EVS Deployment Orchestrator (EDO) automates end-to-end VCF 9.x deploy.
    KB coverage of all of this: zero (no VCF 9, r7i, EDO, licensing portability).
  - Cert research (2026-11-25): **No AWS or Broadcom certification exists for EVS
    itself** (searched AWS What's New, the EVS product page and AWS T&C; nothing found).
    EVS = AWS infrastructure + customer-operated VCF, so the expert bar is the VCF exam.
    Target: **VMware Cloud Foundation 9.0 Administrator (2V0-17.25)**, credential
    **VCP-VCF Administrator**. Format (official Broadcom exam guide, Nov 2026, read in
    full): 60 items, scaled, pass 300, 135-min appointment, proctored via Pearson VUE.
    Recommended courses: VCF: Build, Manage, and Secure; VCF: Automation and Operations.
    MQC: 1 yr IT + 6 months VCF, foundational Kubernetes, DNS/NTP/certs. Sections 1, 3
    and 5 have NO testable objectives; no weightings published. Testable objectives:
    **2.1** Modern private cloud vision; **2.2** compute (vCenter/ESX deploy, clusters,
    VMs); **2.3** storage (vSAN ESA vs OSA, deploy, storage policies, resilience, space
    efficiency); **2.4** networking (VCF networking components, fabrics, connectivity
    and routing, services); **2.5** vSphere Supervisor / VKS. **4.1** deploy and
    configure (deployment models, VCF Network Gateway, workload domains, WLD storage,
    Supervisor); **4.2** manage (Fleet Management, Identity/RBAC, license, certificate,
    password management, vCenter import, lifecycle); **4.3** operations (VCF Operations
    views/reports/dashboards/alerts/policies, logs, Health and Diagnostics, network and
    storage operations, compliance, drift); **4.4** VCF Automation (regions, multi-org
    tenancy, provider networking, content library, org governance, extensibility,
    Supervisor services).
    Sources: https://docs.broadcom.com/doc/vmware-cloud-foundation-administrator-exam-guide
    https://aws.amazon.com/about-aws/whats-new/2025/08/aws-general-availability-amazon-elastic-evs
    https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-evs-vcf9/
    https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-evs-r7i-agent-skill-support/
    Target bar: 2V0-17.25 objectives, plus the AWS-side networking/connectivity
    knowledge from SAA-C03 D1/D3 (see cloud/aws above).
  - Gap vs blueprint: The exam body overlaps almost entirely with
    `virtualization/vmware/products/vmware-cloud-foundation` (its own queue item, same
    target). Phase B for EVS should NOT duplicate that; it should (1) do a VCF 9 pass on
    the EVS pages (versions, r7i + FSx ONTAP external storage, EDO, who installs what,
    licensing portability) and fix the 3 accuracy bugs above; (2) cover the EVS-specific
    delta: VPC/VLAN-subnet underlay, Route Server, host/instance sizing, AWS-side
    shared responsibility; (3) link each 2V0-17.25 objective to the VCF section's
    pages. Zero EVS coverage today of VCF Operations, Fleet Management, VCF Automation,
    Identity Broker; 1 page mentions Supervisor/Kubernetes.
  - site_audit (2026-11-25): 70/70 clean (same full run as cloud/aws; docs/ unchanged by
    either item). The 3 accuracy bugs are content errors for Phase B, not audit-detectable
    structure bugs.
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
