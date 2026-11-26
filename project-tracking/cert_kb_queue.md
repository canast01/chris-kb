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
- [x] cloud/azure
  - Audit (2026-11-25): 125 pages, ~37,200 lines (the biggest cloud section): architecture,
    compute, storage, networking, identity, governance, security, monitoring, backup-dr,
    cost, deploy, operations, cli-reference, troubleshooting, learning path. "Applies to"
    is written 5 ways (119 say just "Azure"). Strong on RBAC (63 pages), Entra ID (37),
    storage accounts (43), NSGs (32), Key Vault (32), Azure Monitor/Log Analytics (28/27),
    Recovery Services/Backup vaults (23), AKS (23), App Service (22), ExpressRoute (17),
    management groups (17), Azure Policy/Private Endpoint/Load Balancer (15 each). No
    exam-blueprint content.
  - Cert research (2026-11-25): Microsoft has a full role-based ladder, so this section
    needs a chosen target. Target: **Exam AZ-104: Microsoft Azure Administrator**, which
    earns **Microsoft Certified: Azure Administrator Associate**. It matches this KB's
    implement/manage/monitor focus. Format (Microsoft Learn, verified via the official
    study guide and exam-duration pages): pass 700 (scale to 1,000); associate role-based
    exams are 100 min (120 min seat), or 120/140 min if labs are included, and Microsoft
    does not say which exams have labs; "most exams typically contain between 40-60
    questions"; certification renews every 12 months via a free online assessment. Price
    varies by country (not verified here). Skills measured as of **April 17, 2026**
    (current version; the change log shows only minor edits from the prior version):
    **Manage Azure identities and governance (20-25%)**: Entra users and groups (licenses,
    external users, SSPR); access to Azure resources (built-in roles, scopes, interpreting
    assignments); subscriptions and governance (Azure Policy, resource locks, tags,
    resource groups, subscriptions, cost alerts/budgets/Advisor, management groups).
    **Implement and manage storage (15-20%)**: storage access (firewalls and VNets, SAS,
    stored access policies, access keys, identity-based access for Azure Files); storage
    accounts (redundancy, object replication, encryption, Storage Explorer and AzCopy);
    Azure Files and Blob (file shares, containers, tiers, soft delete, Files snapshots,
    lifecycle management, versioning).
    **Deploy and manage Azure compute resources (20-25%)**: ARM/Bicep (interpret, modify,
    deploy, export, convert); VMs (encryption at host, move across RG/sub/region, sizes,
    disks, zones and availability sets, VM Scale Sets); containers (ACR, ACI, Container
    Apps, sizing and scaling); App Service (plans, scaling, TLS/certs, custom DNS, backup,
    networking, deployment slots).
    **Implement and manage virtual networking (15-20%)**: VNets/subnets, peering, public
    IPs, UDRs, troubleshoot connectivity; NSGs and ASGs, effective security rules, Bastion,
    service endpoints, private endpoints; Azure DNS, internal/public load balancer,
    troubleshoot load balancing.
    **Monitor and maintain Azure resources (10-15%)**: metrics, log settings, log queries,
    alert rules/action groups/alert processing rules, Monitor Insights, Network Watcher
    and Connection Monitor; Recovery Services vault, Backup vault, backup policies,
    backup/restore, Site Recovery config and failover, backup reports and alerts.
    Next tier up, for later: AZ-305 (Azure Solutions Architect Expert), which requires
    AZ-104.
    Sources (primary, vendor): https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-104
    https://learn.microsoft.com/en-us/credentials/certifications/azure-administrator/
    https://learn.microsoft.com/en-us/credentials/support/exam-duration-exam-experience
    Target bar: the AZ-104 skills measured above.
  - Gap vs blueprint (pages mentioning each term, out of 125): Zero coverage: AzCopy,
    Storage Explorer, object replication, stored access policies, encryption at host,
    App Service deployment slots, Container Apps. Thin: ARM/Bicep (4; the whole ARM/Bicep
    skill group is a real gap: interpret/modify/export/convert), external users/B2B (2),
    Entra licensing (2), SAS (6), storage firewalls (2), Azure Files (9), availability
    sets/zones (7 each), ACI (2), application security groups (1), Bastion (2),
    Connection Monitor (1), alert processing rules (1), Monitor Insights (3), effective
    rules/routes (5), UDRs (7). Phase B should add an ARM/Bicep page (read, modify,
    deploy, export, decompile), a storage data-tools and data-protection page (AzCopy,
    Storage Explorer, SAS vs stored access policy, object replication, versioning, soft
    delete), a containers page (ACR/ACI/Container Apps), App Service slots/TLS/custom
    domains, VM placement and moves (zones vs sets, encryption at host, move RG/sub/
    region), and fill Bastion/ASG/Connection Monitor/alert processing rules into the
    existing networking and monitoring pages.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered cloud/azure and
    compute/linux since neither touched docs/). This item only edited this queue file.

### Compute
- [x] compute/linux
  - Audit (2026-11-25): 34 pages, ~12,900 lines (mysql/ and postgresql/ sub-sections
    excluded; they have their own queue items): architecture, deploy, operations,
    security, troubleshooting, directory-integration, learning path. Written
    distro-neutral: "RHEL / Ubuntu LTS" (15 pages), "RHEL 8.x/9.x, Ubuntu 22.04/24.04"
    (6). **No page mentions RHEL 10.** Strong on systemd (31), dnf/yum (26), sudo (25),
    kernel (25), journalctl (19), SELinux concepts (16). Operationally focused; no
    exam-blueprint content.
  - Cert research (2026-11-25): Target: **Red Hat Certified System Administrator (RHCSA),
    exam EX200**, the standard vendor Linux admin cert. Per the official exam page
    (redhat.com, fetched 2026-11-25): "based on Red Hat Enterprise Linux 10";
    performance-based (hands-on tasks on live systems; configs "must persist after reboot
    without intervention"); no internet; product docs available. Prep: RH124 + RH134, or
    RH199 Rapid Track. Next step up: RHCE (EX294, Ansible; see automation/ansible).
    Duration, passing score and price are not on the exam page (not verified here). Red
    Hat's FAQ says the May 2026 framework changes did not change exam content,
    objectives, price or proctoring. A community thread says the RHEL 9 vs 10 version is
    chosen at scheduling (unofficial).
    Objectives (10 groups, 70 bullets, official page, paraphrased): **(1) essential
    tools** (shell syntax, redirection, grep/regex, SSH, switching users, tar/gzip/bzip2,
    editing files, file ops, hard/soft links, ugo/rwx, man/info/usr-share-doc);
    **(2) software** (RPM repos and packages, **Flatpak** repos and packages);
    **(3) simple shell scripts** (if/test/[], loops, $1.., command output);
    **(4) operate running systems** (boot/reboot/shutdown, boot into targets, interrupt
    boot to gain access, find and kill heavy processes, scheduling priority, **tuning
    profiles**, logs and journals, persistent journal, network services, secure file
    transfer); **(5) local storage** (GPT partitions, PVs/VGs/LVs, mount by UUID/label,
    non-destructive add of partitions/LVs/swap); **(6) file systems** (VFAT/ext4/XFS,
    NFS, autofs, extend LVs, fix permission problems); **(7) deploy/maintain** (at, cron,
    systemd timers, services at boot, default target, time client, packages from CDN/
    remote repo/local file, bootloader); **(8) networking** (IPv4/IPv6, hostname
    resolution, services at boot, firewalld); **(9) users and groups** (users, password
    aging, groups, privileged access); **(10) security** (firewalld, default
    permissions/umask, SSH keys, SELinux modes, contexts, restore contexts, port labels,
    booleans). Note: containers/podman are not in the RHEL 10 objectives.
    Secondary, distro-neutral, noted for the Ubuntu side: **LFCS** (Linux Foundation):
    online proctored performance-based, 2 h, valid 2 yrs, $445; domains Operations
    Deployment 25%, Networking 25%, Storage 20%, Essential Commands 20%, Users and
    Groups 10%; no distro named.
    Sources: https://www.redhat.com/en/services/training/ex200-red-hat-certified-system-administrator-rhcsa-exam
    https://www.redhat.com/en/services/training-and-certification/faq
    https://training.linuxfoundation.org/certification/linux-foundation-certified-sysadmin-lfcs/
    Target bar: the EX200 (RHEL 10) objectives above.
  - Gap vs blueprint (pages mentioning each term, out of 34): Zero coverage: RHEL 10,
    Flatpak, tuned/tuning profiles, `at` scheduling, VFAT, ACLs (setfacl), SELinux port
    labels, VDO (no longer in objectives, fine). Thin: systemd timers (1), autofs (1),
    semanage/restorecon (1), SELinux booleans (1), shell scripting (1 page with a bash
    script tutorial angle), podman (1, not needed), GPT partitioning (2), umask (2),
    IPv6 (2), man/usr-share-doc (2), NFS client (6), firewalld (9), nmcli (7). Phase B
    should do a RHEL 10 pass first, then add: shell scripting fundamentals, a storage
    lab page (GPT -> PV/VG/LV -> fs -> fstab by UUID -> extend -> swap), SELinux
    hands-on (contexts, restorecon, semanage port, booleans), scheduling (at/cron/
    timers), boot targets and root password recovery, software (dnf repos + Flatpak),
    tuned, and an exam-style "persist across reboot" checklist on each task page.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered cloud/azure and
    compute/linux since neither touched docs/). This item only edited this queue file.
- [x] compute/linux/mysql
  - Audit (2026-11-25): 27 pages, ~4,160 lines: architecture, deploy, operations,
    security, troubleshooting, learning path, release notes. Mostly written for "MySQL
    8.0" (20 mentions) with MariaDB 10.x folded in (6 pages); "Applies to" is written 7
    ways (15 say just "RHEL / Ubuntu LTS"). Only 1 mention of 8.4 LTS. Strong-ish on
    InnoDB (19), replication (17), binlog (12), users/GRANT (11), TLS (11), upgrades
    (11), slow query log and Performance Schema (9 each). No exam-blueprint content.
  - Cert research (2026-11-25): **The old target is gone.** Exam 1Z0-908 (MySQL 8.0
    Database Administrator, OCP) retired 2026-11-16; its MyLearn page now returns "We
    couldn't find the exam ... may already be retired" (checked in a rendered browser,
    2026-11-25). Current target: **Exam 1Z0-918: MySQL Database Administration
    Professional** (Oracle MyLearn page, rendered and read 2026-11-25): proctored online,
    multiple choice, 120 min, 70 questions, passing score 60 (percent, by Oracle's usual
    convention; the page shows just "60"). The page does not name a MySQL version or a
    formal credential title and gives no domain weights; price not shown (Oracle Exam
    Subscription is ~$245 per a secondary source, unverified). Audience: DBAs, sysadmins,
    DB engineers, support and ops. Exam topics (verbatim headings, official page):
    **(1) Understanding MySQL Architecture, Storage, and InnoDB Fundamentals**:
    architecture, connectivity and storage fundamentals; InnoDB storage structures and
    memory usage.
    **(2) Managing MySQL Server Installation, Startup, Configuration, Upgrade, and
    Multiple Server Instances**: install/initialize/maintain; runtime behavior and
    multiple instances.
    **(3) Administering MySQL Security, Authentication, Authorization, Encryption, and
    Firewall Controls**: identities, authentication and access control; secure server,
    host and connection environments; advanced data protection and threat prevention.
    **(4) Monitoring MySQL Activity, Analysing Operations, and Maintaining Stability**:
    monitor, audit and analyze activity; performance, capacity and stability.
    **(5) Optimizing MySQL Queries Through Analysis, Indexing, and Statistics**: query
    processing analysis; index design and index statistics.
    **(6) Managing MySQL Backup and Recovery Methods, Tools, and Strategies**: plan and
    evaluate backup strategy; implement backup and recovery with the right tools.
    **(7) Managing MySQL High Availability Using Replication, Monitoring, InnoDB
    Cluster, and Recovery**: configure/manage/monitor replication; replication and HA
    concepts; implement and recover InnoDB Cluster.
    Other current MySQL exams (secondary source only, not targets): 1Z0-909 developer,
    1Z0-922 Implementation Associate.
    Sources: https://mylearn.oracle.com/ou/exam/mysql-database-administration-professional-1z0-918/51871/164064/275183
    (client-side rendered: WebFetch returns an empty shell; use a real browser)
    https://mylearn.oracle.com/ou/exam/mysql-80-database-administrator-1z0-908/51871/110678/170386 (now "not found")
    Lead only: https://dailydebian.com/blogs/it-certification-news/mysql-certification-2026-1z0-908-1z0-918-1z0-909
    Target bar: the 1Z0-918 topics above, on MySQL 8.4 LTS (Oracle names no version;
    8.4 is the current LTS, so Phase B should verify against 8.4 docs).
  - Gap vs blueprint (pages mentioning each term, out of 27): Zero coverage: multiple
    server instances, MySQL Enterprise Firewall, histograms/ANALYZE TABLE (index
    statistics), EXPLAIN ANALYZE/optimizer trace, data masking, connection control,
    InnoDB ClusterSet, SET PERSIST, data dictionary. Thin: redo/undo logs (3 each),
    InnoDB Cluster (3), MySQL Router/Shell (3 each), Group Replication (4), roles (4),
    sys schema (4), audit (4; Enterprise Audit 2), EXPLAIN (5), GTID (5), keyring/TDE
    (1), clone plugin (1), MySQL Enterprise Backup (2), partitioning (1). Phase B
    should: pick 8.4 LTS as the baseline and split MariaDB out (it diverges on
    auth, replication and clustering); add an InnoDB internals page (buffer pool, redo/
    undo, doublewrite, tablespaces); a query-optimization page (EXPLAIN/EXPLAIN ANALYZE,
    index design, histograms); an Enterprise security page (Firewall, Audit, TDE/
    keyring, masking, connection control, password validation); an InnoDB Cluster /
    ClusterSet / Router / Shell lab; a backup-strategy page (mysqldump vs MEB vs clone
    vs snapshots, PITR with binlogs); multiple-instance operation.
  - site_audit (2026-11-25): 70/70 clean (full run). This item only edited this queue file.
- [x] compute/linux/postgresql
  - Audit (2026-11-25): 27 pages, ~3,880 lines: architecture, deploy, operations,
    security, troubleshooting, learning path, release notes. Versions are mostly 14-16
    (PostgreSQL 15 x16, 14 x9, 16 x6, 17 x2; **no PostgreSQL 18**); "Applies to" written
    6 ways. Reasonable on pg_hba (15 pages), psql (15), WAL (14), postgresql.conf (13),
    autovacuum and pg_stat_activity (10 each). No exam-blueprint content.
  - Cert research (2026-11-25): The PostgreSQL project has no official certification.
    The vendor certs for community PostgreSQL are EDB's. Per the EDB Certification
    Exams Catalog (rendered and read 2026-11-25): **EDB Essentials for PostgreSQL**
    ("fundamental knowledge to maintain and manage a PostgreSQL server and related
    applications in a production environment"), versions **v18**, v16, v14; and **EDB
    Advanced for PostgreSQL** ("advanced responsibilities for maintaining and managing
    PostgreSQL servers"), v18, v16. Also listed, not targets: EDB Postgres AI Database
    Essentials/Advanced (EPAS, Oracle-compatible; v18/17/15), HA Essentials v6,
    WarehousePG v7, CloudNativePG v1.25. **Format and objectives are not public**: the
    catalog gives none, and exam detail pages are inside EDB's LMS behind an account
    login (training.enterprisedb.com redirects to EDB login). Third-party figures (60-80
    questions, 90 min, 70%) describe other/older exams and are NOT used here.
    Target: **EDB Essentials for PostgreSQL v18**, with EDB Advanced for PostgreSQL v18
    as the expert bar. Since the official objectives are login-gated, the published
    standard used as the blueprint is the **PostgreSQL 18 manual, Part III "Server
    Administration"** (chapters, verified at postgresql.org/docs/18/admin.html):
    16 Installation from Binaries; 17 Installation from Source; 18 Server Setup and
    Operation; 19 Server Configuration; 20 Client Authentication; 21 Database Roles;
    22 Managing Databases; 23 Localization; 24 Routine Database Maintenance Tasks;
    25 Backup and Restore; 26 High Availability, Load Balancing, and Replication;
    27 Monitoring Database Activity; 28 Reliability and the WAL; 29 Logical
    Replication; 30 JIT (31 Regression Tests: out of scope for admins).
    Sources: https://www.enterprisedb.com/training/certification-exams
    https://www.postgresql.org/docs/18/admin.html
    Target bar: PG 18 Part III chapters 16-30 (+ ops tooling the KB already uses:
    Patroni, pgBackRest, PgBouncer). If the user has an EDB account, the real exam
    objectives can replace this in Phase B.
  - Gap vs blueprint (pages mentioning each term, out of 27): Zero coverage: PostgreSQL
    18 (and its new features), SCRAM auth, localization/collations, JIT. Thin: EXPLAIN
    (3), MVCC (3), pg_stat_statements (3), row-level security (1), initdb/pg_ctl (4
    each), pg_upgrade (4), Patroni (4), work_mem (4), streaming/logical replication and
    replication slots (5 each), tablespaces and partitioning (5 each), roles/GRANT (6),
    checkpoint (6). Phase B should: do a PG 18 pass and drop pre-14 references; add a
    roles and privileges page (role attributes, GRANT/default privileges, RLS, SCRAM,
    pg_hba method order); an MVCC/VACUUM internals page (xmin/xmax, wraparound,
    freezing, autovacuum tuning); a query-tuning page (EXPLAIN ANALYZE, index types,
    pg_stat_statements); a replication lab (physical streaming + slots, logical
    publication/subscription, failover with Patroni); a backup lab (pg_dump/restore vs
    pg_basebackup vs pgBackRest, PITR with WAL archiving); an upgrade page (pg_upgrade,
    logical-replication upgrades).
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered the 12 items done
    this evening from postgresql to mds, since none touched docs/). Queue file only.
- [x] compute/windows-server
  - Audit (2026-11-25): 28 pages, ~6,080 lines (active-directory/ and sql-server/
    excluded; they have their own queue items): architecture, deploy, operations,
    security, troubleshooting, learning path, release notes. 23 pages say "Windows Server
    2019 / 2022"; **Windows Server 2025 appears once**. Strong on event logs and Windows
    Update/WSUS (16 each), DNS (15), SMB (10), Windows Firewall and Kerberos (8 each).
    Operations/troubleshooting focused; no exam-blueprint content.
  - Cert research (2026-11-25): **The old target is gone.** AZ-800 (Administering
    Windows Server Hybrid Core Infrastructure) was retired 2026-09-30 per its own study
    guide banner on Microsoft Learn; third-party coverage says AZ-801 retired the same
    day and both were replaced by one exam. Microsoft Learn confirms the successor: the
    credential page is now **Microsoft Certified: Windows Server Administrator
    Associate** (renamed; "Hybrid" dropped; last updated 01/21/2026) and its practice
    assessment link is aka.ms/AZ802-PA. Target: **Exam AZ-802: Administering Windows
    Server** (official study guide, fetched 2026-11-25). Pass 700; associate exams are
    100 min (120 with labs); renews yearly via free assessment. No product version is
    named; Windows Server 2025 is current (OSConfig, SMB over QUIC, hotpatch-era
    features in the outline imply it).
    Skills at a glance: **AD DS 20-25%** (DCs on-prem and in Azure, RODCs and RODC
    account security, FSMO; trusts, sites, replication; users/groups/service accounts;
    Group Policy and preferences). **Hybrid management 10-15%** (Windows Admin Center
    on-prem and in Azure portal; PowerShell remoting with double-hop and JEA; SSH; RDP;
    Azure Arc servers, Arc device configuration, VM extensions on non-Azure machines,
    Azure Update Manager, Automation runbooks). **VMs 10-15%** (Hyper-V: enhanced
    session, PowerShell Direct/SSH Direct, nested virtualization, memory, integration
    services, device assignment, GPU partitioning, checkpoints, HA, VHDs, network
    adapter, NIC teaming, virtual switch, **Hyper-V Replica**; Azure VMs: storage,
    resize/VMSS, sets/zones, JIT and Bastion, networking). **Networking 10-15%** (AD-
    integrated DNS, zones/records, forwarding/conditional forwarding, hybrid name
    resolution, DNS policies, DNSSEC; DHCP role, scopes, reservations, DHCP HA, IP
    troubleshooting). **Storage and file services 15-20%** (Azure Files, File Sync,
    DFS -> File Sync and share -> Azure Files migration; share access, FSRM, DFS, SMB
    over QUIC, SMB settings; disks/volumes, Storage Spaces, **Storage Spaces Direct**,
    Storage Replica, dedup, SMB Direct, Storage QoS, NTFS/ReFS, iSCSI, BitLocker and
    encrypted-volume recovery). **Secure Windows Server 10-15%** (NEW vs AZ-800: exploit
    protection, App Control for Windows, Credential Guard, SmartScreen, GPO hardening,
    OSConfig baselines, Windows LAPS, Defender for Servers, Windows Firewall/IPsec rules;
    AD DS: password policies, Entra Password Protection, Protected Users, DC hardening,
    delegation, auth protocols). **Monitor and troubleshoot 15-20%** (NEW: PerfMon, data
    collector sets, WAC alerts, System Insights, event logs, Azure Monitor DCRs, alerts,
    VM Insights; troubleshoot connectivity, name resolution, Windows Update, time
    service, performance, VM/Arc extensions, disk encryption, storage; AD Recycle Bin,
    DSRM, SYSVOL recovery, AD replication, Kerberos, secure channel).
    Dropped vs AZ-800: containers, guarded fabric/shielded VMs, IPAM, Remote Access/
    NPS/WAP/Azure Relay/Entra App Proxy, Entra Connect/Cloud Sync/Domain Services.
    Sources (primary, vendor): https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-802
    https://learn.microsoft.com/en-us/credentials/certifications/windows-server-hybrid-administrator/ (old URL; page now titled Windows Server Administrator Associate)
    https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-800 (retirement banner)
    Target bar: the AZ-802 skills above. AD DS (20-25%) and "Secure AD DS" /
    "Troubleshoot AD" overlap compute/windows-server/active-directory; that item should
    reuse AZ-802 for its AD objectives and the two sections should cross-link.
  - Gap vs blueprint (pages mentioning each term, out of 28): Zero coverage: Azure
    Automation runbooks, nested virtualization, PowerShell Direct, GPU partitioning,
    Hyper-V checkpoints, Hyper-V Replica, NIC teaming/SET, DNSSEC, DNS policies, DHCP
    failover, Azure File Sync, FSRM, SMB over QUIC, Storage Replica, Data
    Deduplication, ReFS, Defender for Servers, System Insights, VM Insights/DCRs,
    Failover Clustering. Thin: Windows Server 2025 (1), Windows Admin Center (2), JEA
    (1), double-hop (1), Azure Arc (1), Update Manager (1), DHCP (1), DFS (1), App
    Control (1), Storage Spaces Direct (2), data collector sets (2), Hyper-V (5).
    Phase B: do a Windows Server 2025 pass; add a Hyper-V section (VM config, replica,
    HA/clustering, networking/SET); a file and storage services section (FSRM, DFS,
    SMB over QUIC, Storage Spaces/S2D, Storage Replica, dedup, ReFS, Azure File Sync);
    a DNS/DHCP page (policies, DNSSEC, DHCP failover); a hybrid management page (WAC,
    remoting/JEA/double-hop, Arc, Update Manager, runbooks); a monitoring page (PerfMon/
    DCS, System Insights, Azure Monitor DCRs, VM Insights); expand security into the
    AZ-802 OS-hardening list.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered the 12 items done
    this evening from postgresql to mds, since none touched docs/). Queue file only.
- [x] compute/windows-server/active-directory
  - Audit (2026-11-25): 27 pages, ~4,700 lines: the standard 5 sections, learning path,
    release notes. All pages say "Windows Server 2019 / 2022" (written 4 ways); Windows
    Server 2025 appears once (no AD 2025 functional level, dMSA, 32k pages, etc.). This
    is a solid operational section: Kerberos (19), GPO (17), repadmin (15), FSMO (14),
    sites (13), dcdiag/delegation/SYSVOL-authoritative restore (12 each), DFSR (11),
    schema (10), LDAPS/signing and secure channel (9 each). No exam-blueprint content.
  - Cert research (2026-11-25): There is no AD-only certification. On-prem AD DS is
    examined inside **AZ-802: Administering Windows Server** (full research under
    compute/windows-server above; AZ-800/801 retired 2026-09-30). Target: the AD-related
    AZ-802 objectives: **Deploy and manage AD DS (20-25%)**: DCs on-prem and in Azure,
    RODCs and RODC account security, FSMO manage/troubleshoot; trusts, sites,
    replication; users/groups incl. multi-domain/forest, service accounts; Group Policy
    and preferences. **Secure AD DS** (part of 10-15%): password policies, Entra
    Password Protection for AD DS, Protected Users, DC hardening and access restriction,
    user-account and built-in admin group security options, AD delegation, auth
    protocols and methods. **Troubleshoot AD** (part of 15-20%): AD Recycle Bin, DSRM
    database recovery, SYSVOL recovery, AD replication, on-prem AD, Kerberos and auth,
    secure channel and computer account trust. Plus DNS integrated with AD DS (networking
    domain).
    Hybrid identity (Entra Connect Sync, Cloud Sync, PHS/PTA, seamless SSO, Connect
    Health) was dropped from the Windows Server exam and now lives in **SC-300:
    Microsoft Identity and Access Administrator** (skills measured as of 2026-10-28,
    verified on Microsoft Learn); use SC-300's hybrid-identity group as the bar for any
    AD-to-Entra content here.
    Sources: https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-802
    https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/sc-300
    Target bar: the AZ-802 AD objectives above (+ SC-300 hybrid identity subsection).
  - Gap vs blueprint (pages mentioning each term, out of 27): Zero coverage: Password
    Replication Policy (RODC account security), selective authentication/SID filtering,
    gMSA/dMSA service accounts, Group Policy Preferences, Entra Password Protection,
    Kerberos constrained/resource-based delegation. Thin: Windows Server 2025 (1),
    Entra Connect/Cloud Sync (1), RODC (2), DSRM (2), site links/bridgeheads (2), WMI
    filters/loopback (2), DCs in Azure (3), AdminSDHolder (5), trusts (6), Recycle Bin
    (6), NTLM (6), tiered admin model/PAW (6), Protected Users (6). Phase B: Server
    2025 AD pass (2025 DFL/FFL, dMSA, LDAP/Kerberos changes); add an RODC page (PRP,
    credential caching, admin role separation); a service accounts page (gMSA, dMSA,
    sMSA); a trusts page (types, selective auth, SID filtering, quarantine); GP
    Preferences + filtering; DC-in-Azure design; a hybrid identity page aligned to
    SC-300 (Connect Sync vs Cloud Sync, PHS/PTA/SSO); expand the recovery page into a
    lab (Recycle Bin, DSRM, authoritative/non-authoritative SYSVOL restore).
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered the 12 items done
    this evening from postgresql to mds, since none touched docs/). Queue file only.
- [x] compute/windows-server/sql-server
  - Audit (2026-11-25): 27 pages, 3,295 lines; 6 subdirs (architecture 5, deploy 1,
    learning-path 1, operations 8, security 5, troubleshooting 5) + index.md and
    release-notes.md. All 27 pages carry an "Applies to:" line, but 15 of them say
    "Windows Server 2019 / 2022" (the OS, not SQL); 10 say SQL Server 2019 / 2022; 2 say
    "Windows Server 2022 · SQL Server". Version mentions: SQL Server 2019 x12, 2022 x7,
    2016 x2; SQL Server 2025 x0. Strengths: DMVs (sys.dm_*, 15 pages), SQL Server Agent/msdb
    (9), blocking (9), tempdb (9), Always On availability groups (8), Query Store (6),
    index maintenance (5), MAXDOP/max server memory (5), patching/CUs (5), TDE (4), log
    shipping (4), dbatools/SqlServer module (4). The longest pages are diagnostics (362
    lines), health-checks (360) and escalation (338). The exam/certif matches (4 pages)
    are about TLS/TDE certificates, not exams. No exam-blueprint content.
  - Cert research (2026-11-25): Target exam: DP-300 "Administering Microsoft Azure SQL
    Solutions", which leads to Microsoft Certified: Azure Database Administrator Associate
    (Intermediate). Checked by fetching the Learn study guide and the certification page.
    It is LIVE: the study guide has no retirement banner, and DP-300 is not listed under
    "Exams scheduled to retire" or "Recently retired exams" on the Learn retirement page
    (that page does list AZ-800/801 as retired 2026-09-30). The skills outline was
    refreshed "as of October 27, 2026" (the change log shows only a Minor change, to data
    at rest/in transit security). Format: pass score 700. Renewal every 12 months via a
    free online assessment. Microsoft's general exam-duration page gives 100 min for
    associate/expert exams without labs (120 min if they may contain labs) and "typically
    40-60 questions". DP-300's own question count, duration and price: not verified (the
    exam page redirects to the certification page, which doesn't show them). The audience
    profile explicitly includes "SQL Server on-premises" next to Azure SQL DB, SQL MI and
    SQL Server on Azure VMs.
    Domains: (1) Plan and implement data platform resources 15-20%: recommend an offering;
    automated deployment; Azure Arc-enabled SQL; Azure SQL DB in Fabric; plan/configure
    table partitioning and sharding; deploy hybrid SQL Server; patch hybrid/IaaS;
    configure SQL DB/MI/SQL VM for scale and performance; data compression; migration
    strategy (online/offline, to Azure, between Azure SQL services, MI database copy/move,
    troubleshoot migration). (2) Implement a secure environment 20-25%: Microsoft Entra ID
    auth for SQL DB/MI/SQL Server; security principals; least privilege; graphical
    and T-SQL permission management; troubleshoot authN/authZ; TDE; object-level
    encryption; server/DB firewall rules; Always Encrypted (incl. secure enclaves); private
    link/service endpoints; data classification; server/database audit; change data
    tracking; dynamic data masking; ledger; row-level security. (3) Monitor, configure,
    and optimize database resources 20-25%: performance baseline; metric sources; database
    watcher; Extended Events; Query Store; session blocking; DMVs; index changes; query
    construct changes; execution plans; Intelligent Insights; index and statistics
    maintenance; integrity checks; automatic tuning; server settings; Resource Governor;
    database-scoped configuration; compute/storage scaling; IQP use cases. (4) Configure
    and manage automation of tasks 15-20%: SQL Server Agent job schedules, alerts and
    notifications, troubleshooting; ARM/Bicep, Azure PowerShell and Azure CLI deployment;
    elastic jobs; Azure task automation, alerts and troubleshooting. (5) Plan and configure
    HA/DR 20-25%: HA/DR strategy from RPO/RTO; hybrid and Azure HA/DR evaluation; HA/DR test
    plan; backup/restore strategy; native and T-SQL backup/restore; point-in-time restore;
    long-term retention; backup to/restore from cloud storage (URL); active
    geo-replication; failover groups; AGs on MI and Azure VMs; FCIs on Azure VMs; log
    shipping; monitor/troubleshoot HA/DR.
    Fit: partial. About half of the objectives are engine-level and apply directly to
    on-prem SQL Server (Agent, DMVs, Query Store, XE, backup/restore, AGs, log shipping,
    TDE/AE/RLS/DDM, audit, Resource Governor). The rest are Azure-only (MI, SQL DB,
    elastic jobs, geo-replication, ARM/CLI, Entra, firewall rules, Fabric). Microsoft
    currently offers no on-prem-only SQL Server certification. On Learn I found only
    DP-300 and one adjacent Applied Skills credential, "Migrate SQL Server workloads to
    Azure SQL Database" (live page; it covers assessing/migrating instance- and
    database-scoped objects). That Applied Skills credential is the secondary/next-tier
    option. No vendor-neutral or on-prem SQL Server exam was found or verified.
    Sources (primary, vendor):
    https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/dp-300
    https://learn.microsoft.com/en-us/credentials/certifications/azure-database-administrator-associate/
    https://learn.microsoft.com/en-us/credentials/certifications/exams/dp-300/
    https://learn.microsoft.com/en-us/credentials/support/retired-certification-exams
    https://learn.microsoft.com/en-us/credentials/support/exam-duration-exam-experience
    https://learn.microsoft.com/en-us/credentials/applied-skills/migrate-sql-workloads-azure-sql-database/
    Target bar: DP-300 (skills as of 2026-10-27), weighted toward its on-prem/engine
    objectives, with the Azure-only objectives covered as hybrid/migration context.
  - Gap vs blueprint (pages mentioning each term, out of 27): Zero coverage: Entra ID
    auth, Always Encrypted secure enclaves, dynamic data masking, ledger, data
    classification, change data capture/tracking, backup to URL/cloud storage,
    geo-replication/failover groups, automatic tuning, Resource Governor,
    database-scoped configuration, IQP, table partitioning, data compression, sharding,
    elastic jobs, ARM/Bicep, Azure CLI/Az.Sql, migration tooling (DMS/DMA/Azure Migrate),
    Azure Arc-enabled SQL, Azure SQL MI, Azure SQL Database, SQL Server on Azure VMs,
    Fabric, SQL Server 2025. Thin: Extended Events 1, row-level security 1, RPO/RTO 1,
    contained DB/AG 1, FCI 2, point-in-time restore 2, execution plans 2, statistics
    maintenance 2, baseline 2, CHECKDB 3, Always Encrypted 3, audit 3, BACKUP DATABASE 3,
    Kerberos/SPN 3, TDE 4, log shipping 4. Solid: DMVs 15, Agent 9, blocking 9, AGs 8,
    Query Store 6, index maintenance 5. Phase B should: (1) add an exam-objective map page
    under learning-path tagging each DP-300 objective as on-prem/hybrid/Azure-only, with
    links; (2) deepen engine topics: XE sessions, perf baseline, execution plans, stats,
    Resource Governor, DB-scoped config, IQP, automatic tuning, partitioning and
    compression; (3) build out security compliance: Always Encrypted (+enclaves), RLS,
    DDM, ledger, classification, server/database audit, CDC/change tracking, and Entra
    auth for SQL Server 2022 (Arc); (4) round out HA/DR: an RPO/RTO decision page, FCI,
    log shipping, PITR walkthrough, backup to URL, contained AGs, HA/DR test plan; (5) add
    a hybrid/Azure sub-section (Arc-enabled SQL, MI/SQL DB/SQL VM offering choice,
    migration with DMS/Azure Migrate, geo-replication/failover groups, elastic jobs,
    ARM/Bicep/CLI deployment); (6) fix the "Applies to" lines (15 name the OS only) and
    add SQL Server 2025 coverage.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered the 12 items done
    this evening from postgresql to mds, since none touched docs/). Queue file only.

### ITSM
- [x] itsm/confluence
  - Audit (2026-11-25): 27 pages, 6,658 lines; subdirs architecture/{design-standards,
    how-it-works,integrations}, deploy, learning-path, operations/{backup-restore,
    cli-reference,health-checks,install-upgrade,procedures,scripts}, security/{access-control,
    authentication,encryption,hardening}, troubleshooting/{common-issues,diagnostics,
    escalation}. "Applies to:" on 17 pages (12 "Cloud / Data Center", 2 "Data Center 8.x",
    2 bare "Confluence", 1 "Data Center / Cloud"); versions named: 7.19 (x3), 8.0, 8.5, 8.8,
    8.9. Despite the Cloud labels the content is Data Center/self-managed: only 5 pages
    mention Cloud outside the Applies-to line, and those mostly in passing. Strengths are DC
    ops: backup/restore 16 pages, database (PostgreSQL/Oracle) 16, REST API 15,
    SAML/SSO/LDAP/Crowd 15, cluster/Hazelcast 14, JVM heap 12, server.xml/
    confluence.cfg.xml 12, reverse proxy 6, Synchrony 3. Hits for "automation" are
    REST-API/script automation; 0 pages cover Confluence Automation rules. No
    exam-blueprint content.
  - Cert research (2026-11-25): Target exam ACP-220 Confluence Administration for Cloud
    (Atlassian Certified Professional, role-based). The name, code and topics come from
    the certification page's embedded page data and its linked "ACP-220 Confluence
    Administration for Cloud Exam Topics" PDF (V1 July 2025). The visible "full exam
    details" panel is collapsed/JS-rendered, so WebFetch returned only a summary line.
    Format from the same page data: 61 questions, 180 minutes, pass = 41 correct, $249 +
    tax, proctored online, valid 24 months. Renewal mechanics beyond "valid for 24
    months": not verified. Status: active. No retirement notice on the page, and the
    certifications catalog lists only the Cloud slug. There is no Confluence Data Center
    certification. Atlassian's certification team (Ree Kent, community article) announced
    retirement of the two Jira DC certs in Sept 2025 and the shift of the catalog to Cloud.
    Retirement of the old ACP-200 Confluence DC/Server exam: not verified from a primary
    page (search snippets only). Domains (as published, sum 99%):
    1 Access and permissions 21%: app admin vs org admin vs space admin; anonymous access;
      guest and licence requests through org/user-access admins; unlicensed guests in one
      space; public links; space permissions (view, delete own, create, restrict, export,
      admin, add pages); copy, recover and restore default permissions; page restrictions
      and inheritance; moves across spaces; include page/excerpt permissions; admin key
      (Premium/Enterprise); additive group permissions.
    2 Site configuration 13%: landing page/company hub; date/time formats; attachment size
      and count limits; default language; recommendation email; email sending domain;
      templates vs blueprints; Create from Template macro; enable/disable global
      blueprints.
    3 Security and data management 11%: hide external links from search engines; global
      permissions (create space, personal space); default permissions for new spaces;
      public links in new spaces; analytics-tab access; macro usage; space reports;
      import/export, backup, archive, delete and restore (spaces and site backups);
      application links at site and space level; application navigator.
    4 Look and feel 8%: logos and colour schemes; themes; site header and footer; PDF
      export format; space logo; site banner; featured/promoted space templates; space
      layout and PDF export.
    5 Space setup and general settings 15%: create from template; permission options;
      space key and icon; categories and home page; content status; avatars; related-page
      suggestions; space features (blogs, automation, analytics, calendars, content
      manager, smart links, databases, whiteboards, folders, shortcuts, apps); content
      manager bulk actions; transfer ownership from deactivated accounts; auto-conversion
      to new editor; export as CSV/HTML/XML/PDF; move pages across spaces.
    6 Content administration 13%: restore from trash to the space root, then move back;
      folders; reorder (Add + View permissions); move branches; attachments list and
      labels; archive vs delete vs purge; effect of deletion on links and macros; hidden,
      archived and restricted page lists; labels for search; undefined links; pages
      outside the home hierarchy.
    7 Automation rules 11%: recommend rules (e.g. child pages on folder creation; label ->
      AI summary); import/export rules; smart buttons; triggers, conditions, actions and
      branch rules; single-space vs multi-space scope; audit log and the log action;
      transfer rule ownership; rule actor permissions; usage limits.
    8 Monitor site performance 7%: Mission Control and Analytics (view trends, spikes,
      guest access, pages without owners, top searches); audit log filtering by date,
      user, event and keyword; audit retention setting.
    The official prep collection also lists a Rovo summarisation course and an 8-lesson
    "certification prep resources" course whose lessons match the 8 domains.
    Mismatch: the exam is Cloud-only, and the KB is DC-focused.
    Sources (primary, vendor):
    https://community.atlassian.com/learning/certifications/confluence-admin-certification
    (also fetched raw with curl to read the embedded examTopics/examSpecifics data);
    https://assets.ctfassets.net/xkfunaz6zr9g/2Cli2MYrFDSsLDNG5VsZi0/c81e75cd5951f2c895745ce2a4103676/CandL-ACP-220_Confluence_Administration_for_Cloud_Exam_Topics-030625-165125.pdf;
    https://learning.atlassian.com/learning/certifications/confluence-admin-certification;
    https://community.atlassian.com/learning/landing/certification-detail/confluence-admin-certification;
    https://community.atlassian.com/learning/collection/certification-prep/confluence-administrator-for-cloud-prep;
    https://community.atlassian.com/learning/course/confluence-administration-certification-prep-resources;
    https://community.atlassian.com/learning/certifications;
    https://community.atlassian.com/forums/Training-Certification-articles/Data-Center-certifications-are-being-retired-in-the-coming/ba-p/2974579
    Target bar: ACP-220 Confluence Administration for Cloud (8 domains, V1 July 2025
    topics), with the existing DC ops content kept as a separate "Data Center operations"
    layer.
  - Gap vs blueprint (pages mentioning each term, out of 27): Zero coverage: org/app/site
    admin roles 0, public links 0, admin key 0, default space permissions 0, landing
    page/company hub 0, application navigator 0, look and feel/themes/colour scheme 0,
    site header/footer/banner 0, content manager 0, content status 0,
    whiteboards/databases/folders 0, editor conversion 0, undefined links 0, Confluence
    Automation rules 0, smart buttons 0, rule actor/usage limits 0, Mission Control 0,
    macro usage 0, space reports 0, Rovo/AI summary 0. Thin: blueprints 1, include
    page/excerpt 1, attachment size 1, PDF export layout 1, page ownership 1, anonymous
    access 2, guest access 2, global permissions 2, analytics 2, space/page archiving 2,
    page/space templates 2, space admin 3, page restrictions 3, application links 3, trash
    4, labels 5, audit log 5 (mostly DC log files, not Cloud audit log), space permissions
    6. Broad generic hits (export 13, backup 16, notification 10) are DC/admin-CLI
    context, not the Cloud admin UI. Phase B should: (1) decide scope: add Cloud admin
    pages alongside the DC ops content and fix the "Cloud / Data Center" Applies-to labels
    to match each page's real scope; (2) write a Cloud permissions model page (org vs app
    vs space admin, guests, anonymous, public links, additive permissions, restriction
    inheritance, admin key, recovering space permissions) for the 21% domain; (3) add
    pages on site configuration and look and feel (landing page/hub, limits, language,
    email, templates vs blueprints, themes, header/footer, banner, PDF export); (4) add
    space setup and content administration (space features, content manager, content
    status, folders/whiteboards/databases, trash/archive/restore flows, undefined links,
    missing pages); (5) add a Confluence Automation page (triggers, conditions, actions,
    branches, smart buttons, scope, actor, audit log, usage limits); (6) add Mission
    Control/Analytics and the Cloud audit log; (7) add a learning-path mapping of the
    ACP-220 objectives to KB pages, with exam facts (61 Q / 180 min / 41 correct / $249 /
    24 months).
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered the 12 items done
    this evening from postgresql to mds, since none touched docs/). Queue file only.
- [x] itsm/git
  - Audit (2026-11-25): 27 pages, 8,935 lines; subdirs architecture/ (how-it-works,
    integrations, design-standards, ports), deploy/, learning-path/, operations/
    (backup-restore, cli-reference, health-checks, install-upgrade, procedures, scripts,
    faq), security/ (access-control, authentication, encryption, hardening),
    troubleshooting/ (common-issues, diagnostics, escalation, known-issues), release-notes.
    "Applies to": 15 lines -- 11x "Git 2.x", 2x "Git", 1x "GitLab 16.x / 17.x
    self-managed; GitHub Enterprise", 1x "GitLab CE/EE 16.x / Bitbucket Data Center 8.x".
    Version mentions: GitLab 16 (7), git version 2.43.0 (3), GHES 3.12.5 (2), Git
    2.28/2.40 (2 each), Git 2.38/2.42/2.44/2.46 (1 each); no GitHub.com/GHEC versioning.
    Scope is plain Git CLI + self-hosted platform ops (GitHub 23 pages, GitLab 21,
    Bitbucket 8, "GitHub Enterprise" 7). Strengths: SSH keys 16 pages, rebase 10, PATs/
    GitHub Apps 9, commit signing/GPG 8, pull requests 8, credential helper 7, fsck 7,
    reflog 6, merge conflicts 6, blob/object model 6, stash 5, branch protection 5;
    17/27 pages carry a diagram. No exam-blueprint content.
  - Cert research (2026-11-25): Git itself has no vendor certification. Target exam:
    GH-900 "GitHub Foundations" (credential: GitHub Foundations, Beginner level, Microsoft
    Learn delivered, maintained by GitHub) -- the only current exam whose objectives
    include core Git. Verified by fetching the MS Learn study guide and certification
    page. Format verified only as: passing score 700; certification page (last updated
    02/19/2026) states GitHub Foundations does not require renewal (follows MS
    fundamentals policy). Question count, duration and price not verified on a GH-900
    page (MS generic page lists 45 min for Fundamentals exams; not GH-900-specific).
    Retirement: GH-900 and GH-100 absent from the MS "Exams scheduled to retire" and
    "Recently retired" tables (fetched 2026-11-25; only AZ-400 in the DevOps space retires
    2027-02-01). Skills as of January 2026 (objectives reworded Jan 2026):
    (1) Understand Git and GitHub basics 25-30%: purpose of version control, Git vs
    GitHub, repos/commits/branches; accounts/orgs/enterprise options, GitHub Flow,
    Markdown, GitHub Desktop/Mobile. (2) Work with GitHub repositories 10-15%: key files
    (README, LICENSE, CONTRIBUTING, CODEOWNERS, SECURITY), templates and branches,
    managing files, insights/stars/metrics/dependency insights, maintenance best
    practice. (3) Collaborate using GitHub 10-15%: issues, PRs, discussions; linking PRs
    to issues, templates/filters/assignments; notifications; Gists, Wikis, Pages.
    (4) Apply modern development practices 10-15%: GitHub Actions; Copilot (agents,
    Agent Mode, multi-model) and Individual/Business/Enterprise plans; Codespaces and dev
    containers; github.dev vs Codespaces. (5) Manage projects with GitHub 5-10%:
    Projects and layouts, labels/milestones/workflows, saved replies/assignees, project
    insights. (6) Privacy, security and administration 10-15%: 2FA and passkeys,
    repo/org roles and permissions, EMUs and org-wide Copilot policy, visibility and
    branch protection rules, org settings/teams/roles. (7) Explore the GitHub community
    5-10%: open source and Sponsors, following users/orgs, Marketplace, InnerSource,
    forks/templates/discoverable repos.
    Secondary: GH-100 "GitHub Enterprise Administrator" study guide (skills as of July
    2026): identities and access 15-20% (EMU vs personal, SAML SSO/2FA, SCIM/team sync,
    IdPs, roles/teams/rulesets); administer enterprise 10-15% (admin vs Support, support
    bundles, branching/review/release standards, GHEC/EMU/data residency/GHES deployment,
    licensing); secure development and compliance 25-30% (policies, audit logging,
    secret scanning, CodeQL, Dependabot, advisories, PATs, rate limits, GitHub/OAuth
    Apps); Actions 20-25% (reusable workflows, Actions policies, runner groups,
    self-hosted vs hosted, IP allow lists/private networking, secrets, external vaults);
    monitor/optimize 10-15% (audit log/API usage, metered usage, license optimization).
    Credential page is titled "GitHub Administration" (last updated 05/04/2026; a
    Microsoft Learn search snippet still showed "(beta)" but the fetched page did not).
    GitLab certifications: not verified -- about.gitlab.com/services/education and
    university.gitlab.com/pages/certifications returned no certification names (JS-
    rendered/empty to the fetcher). Expert-depth fallback for plain Git: Pro Git 2nd
    edition (git-scm.com/book), verified chapters 1-10 + appendices A-C; key bar chapters
    2 Git Basics, 3 Git Branching (incl. 3.6 Rebasing), 4 Git on the Server (protocols,
    SSH keys, Smart HTTP, GitLab), 7 Git Tools (revision selection, stash, signing,
    rewriting history, reset, advanced merging, rerere, bisect, submodules, bundling,
    credential storage), 10 Git Internals (objects, refs, packfiles, refspec, transfer
    protocols, maintenance/data recovery).
    Sources (primary, vendor):
    https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-900
    https://learn.microsoft.com/en-us/credentials/certifications/github-foundations/
    https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-100
    https://learn.microsoft.com/en-us/credentials/certifications/github-administration/
    https://learn.microsoft.com/en-us/credentials/support/retired-certification-exams
    https://git-scm.com/book/en/v2
    Target bar: GH-900 GitHub Foundations (all 7 domains) + Pro Git ch. 2/3/4/7/10 depth for
    the plain-Git CLI pages; GH-100 as optional stretch for the GHES admin pages.
  - Gap vs blueprint (pages mentioning each term, out of 27): Zero coverage: Markdown,
    GitHub Desktop/Mobile, README/LICENSE/CONTRIBUTING files, SECURITY.md, template
    repositories, GitHub issues, Discussions, Gists/Wikis/Pages, Copilot, Codespaces/dev
    containers, github.dev, GitHub Projects, labels/milestones, 2FA, passkeys, EMU,
    Sponsors/Marketplace, InnerSource, forks, self-hosted runners. Thin: GitHub Flow 1,
    notifications 1, repo visibility 1, org roles/teams 1, SAML/SCIM 1, Dependabot/CodeQL
    1, audit log 1, refspec 1, plumbing (cat-file/hash-object/update-ref) 1, sparse/
    partial clone 1, CODEOWNERS 2, bisect 2, hooks 2, secret scanning 3, LFS 3, GitHub
    Actions 4, cherry-pick 4, submodules 4, packfiles/gc 4, branch protection/rulesets 5.
    Phase B should: (1) add a GitHub-platform concepts page set (accounts/orgs/enterprise
    + EMU, GitHub Flow, repo key files incl. CODEOWNERS/SECURITY, templates, forks,
    visibility); (2) add a collaboration page (issues, PR-issue linking, discussions,
    notifications, Gists/Wikis/Pages, Projects/labels/milestones, Markdown); (3) add a
    modern-dev page (Actions basics, Copilot plans/agent mode, Codespaces/dev containers,
    github.dev); (4) extend security/ with 2FA/passkeys, org/repo roles, rulesets,
    SAML/SCIM, secret scanning/push protection, Dependabot/CodeQL; (5) add community/
    InnerSource/Marketplace/Sponsors coverage; (6) deepen plain-Git to Pro Git level:
    internals (plumbing, packfiles, refspec, transfer protocols), bisect, rerere,
    hooks, submodules, partial/sparse clone; (7) add a GH-900 domain-mapped exam-prep
    page with practice questions.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered the 12 items done
    this evening from postgresql to mds, since none touched docs/). Queue file only.
- [x] itsm/jira
  - Audit (2026-11-25): 27 pages, 7,584 lines; subdirs architecture/{design-standards,
    how-it-works,integrations}, deploy, learning-path, operations/{backup-restore,
    cli-reference,health-checks,install-upgrade,procedures,scripts}, security/
    {access-control,authentication,encryption,hardening}, troubleshooting/
    {common-issues,diagnostics,escalation}. 19 "Applies to:" lines on 27 pages (8 have
    none): "Jira 9.x / Cloud" x8, "Jira Cloud / Data Center" x6, "Jira" x2, "Jira Data
    Center 9.x" x1, "Jira DC 9.x / Jira Software 9.x" x1, "Jira 9.x / Data Center" x1.
    Version mentions are self-managed only: Jira Software 9.0/9.4/9.12/9.15/9.17, Jira
    8.20; nothing newer than 9.17, no Cloud release references. Focus is Data Center/self-
    managed ops: cluster/nodes 16p, REST API 16p, upgrade 12p, JVM/heap 10p, LDAP 9p,
    reindex 8p, backup 8p, SAML/SSO 7p, SMTP 7p, dbconfig.xml 2p; large pages are
    procedures (897 lines), cli-reference (811), diagnostics (667), health-checks (549).
    Jira Service Management mentioned on 6p only (incidental). No exam-blueprint
    content (no ACP-/certification references anywhere in the section).
  - Cert research (2026-11-25): Target exam: ACP-120 Jira Administration for Cloud
    (credential: Atlassian Certified Professional). The self-managed match, ACP-100
    Jira Administration for Data Center, is retired: Atlassian's prep/detail pages for
    it now return 404 and old university URLs redirect to the generic learning hub;
    the retirement date (11 Sep 2025, shared with Managing Jira Projects for DC) and a
    June 2026 community reply "all Data Center certifications have been retired" were
    seen only in search snippets of community.atlassian.com pages that fetch as
    JS-rendered empty shells, so the date is not verified by fetch. There is no
    current DC Jira exam, so the KB must pivot toward ACP-120. The ACP-120 detail page
    (fetched) confirms the exam is live, aimed at "Jira admins ... configuring and
    managing Jira Cloud", and says "A new version of this exam will be available in
    January 2027, including new exam topics that will be listed on this page". The
    collapsed "exam specifics" panel was read from the page's embedded data (curl,
    re-checked by the coordinating session 2026-11-25): 60 questions, 180 minutes,
    pass = 38 correct, $249, proctored online, products covered Jira Software Cloud,
    valid 24 months. The page's live "detailed exam topics" link is
    ACP-120_Exam_Topics_V2.pdf, so V2 IS the current topic list until the Jan 2027
    refresh. The V2 PDF (April 2021; automation added 1 June 2021) was fetched and
    read in full. It has eight domains:
    (1) User Features 10-15%: business requirements to JQL; shared filters,
    dashboards, filter subscription outcomes; bulk change results. (2) Configuring
    Global Settings and User Communications 5-10%: general config (look and feel,
    default language, user default settings, system dashboard); attachment options,
    issue links, time tracking. (3) Product and Project Access and Permissions 30-35%:
    Jira Cloud user management; admin privileges; configure and troubleshoot product
    access, groups, roles, project and global permissions; impact of removing or
    suspending access and deleting groups; user default and personal settings;
    issue-level security. (4) General Project Configuration 10-15%: project details and
    sidebar; projects from shared config or templates; versions; components and
    auto-assignment; team-managed features; company- vs team-managed choice. (5) Issue
    Types, Fields and Screens 15-20%: statuses, resolutions, priorities, translations,
    issue types, sub-tasks; issue type config (company-managed); impact of changing or
    moving active issue types and schemes; configure and troubleshoot fields via field
    context, field config (scheme), screens (schemes). (6) Workflows and Automation
    5-10%: workflow config for company-managed projects; troubleshoot workflows;
    configure and troubleshoot automation rules. (7) Notifications and Email 5-10%:
    notifications and events per requirements; troubleshoot notifications; incoming
    mail handler. (8) Administering and Extending Jira 5-10%: configure issue
    collectors; methods for backing up and restoring content. It is not confirmed
    that the 2021 V2 PDF is still the live topic list; recheck in Jan 2027 when the
    new-version topics publish. Secondary options: ACP-420 Managing Jira Service
    Projects for Cloud (JSM; its university pages redirect to the JS-rendered hub,
    so not verified; KB JSM coverage is too thin to target); Managing Jira Projects
    for Cloud (project-admin level, not verified).
    Sources (primary, vendor):
    https://community.atlassian.com/learning/certifications/jira-administration-for-cloud ;
    https://www.atlassian.com/dam/jcr:5719c724-76e1-41f8-8d44-4f3928550465/ACP-120%20Jira%20Administration%20for%20Cloud%20Exam%20Topics%20V2.pdf ;
    https://community.atlassian.com/learning/collection/certification-prep/jira-administration-for-cloud-prep ;
    https://community.atlassian.com/learning/certifications (credential levels only) ;
    https://www.atlassian.com/university/certification/badges/exam-asb-210 (301, then
    302 to the hub; ACP-100 old URL exam-acp-100 behaves the same)
    Target bar: a Jira Cloud admin who has read only this section can pass ACP-120
    (v2 topics), weighted toward permissions/access (30-35%) and
    fields/screens/issue types (15-20%), and is ready for the Jan 2027 refresh.
  - Gap vs blueprint (pages mentioning each term, out of 27): Zero coverage: look and
    feel/default language/user default settings 0, time tracking 0, org/site admin
    roles 0, components + auto-assignment 0, Cloud backup and restore (backup
    manager/site export) 0. Thin: shared filters/filter subscriptions 1, product access
    1, issue-level security 1, suspend/deactivate users 1, team-managed 1,
    company-managed 1, versions/releases 1, issue type schemes 1, priorities 1, field
    context 1, screen schemes 1, notification events 1, issue collector 1, attachment
    settings 1, field configuration 2, workflow scheme 2, incoming mail handler 2,
    issue link types 2, bulk change 3, admin.atlassian.com/user management 3,
    project templates/shared config 3, notification scheme 4. Moderate: JQL 11, groups
    12, permission scheme 9, project roles 6, global permissions 5, dashboards 5,
    automation 5, workflow post functions/validators/conditions 6 (generic word,
    inflated), resolutions 12 (inflated by "resolution" in troubleshooting text). Phase
    B should: (1) relabel the section scope: "Applies to" claims Cloud, but content is
    DC 9.x ops; add Cloud-vs-DC notes and bring DC versions current (nothing past
    9.17 is mentioned); (2) add a Cloud admin
    track: admin.atlassian.com org/site/product admin roles, product access, user
    lifecycle (suspend/remove, group deletion impact), permission and issue security
    schemes with troubleshooting (Permission Helper), at depth for the 30-35% domain;
    (3) add schemes deep-dive pages: issue types and sub-tasks, field context, field
    configuration schemes, screen and issue type screen schemes, migrating active
    schemes; (4) add company- vs team-managed projects, templates and shared config,
    versions, components and auto-assignment; (5) add workflows and Jira automation
    rule configuration and troubleshooting (audit log); (6) add user features: JQL
    scenarios, shared filters and subscriptions, dashboards, bulk change; (7) add
    global settings (look and feel, default language, user defaults, attachments,
    issue linking, time tracking), notification schemes and events, incoming mail
    handlers, issue collectors, Cloud backup and restore; (8) add an ACP-120 blueprint
    map, scenario practice questions per domain, and a recheck note for Jan 2027.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered the 12 items done
    this evening from postgresql to mds, since none touched docs/). Queue file only.
- [x] itsm/servicenow
  - Audit (2026-11-25): 79 pages, 10,624 lines, 12 top-level subdirs (architecture,
    asset-inventory [12 sub], change-management [14 sub], deploy, incident-management
    [5 sub], learning-path, lifecycle [7 sub], maintenance-windows [5 sub], operations
    [6 sub], security [4 sub], templates [4 sub], troubleshooting [3 sub]). "Applies to:"
    on 60 pages: 49 say only "ServiceNow", 10 say Washington (DC)/Xanadu, 1 "SaaS — any
    release". Release-name mentions: Xanadu 18, Washington 10 (+3 "Washington DC"),
    Yokohama 4, Vancouver/Utah/Tokyo 2 each, Zurich 1, Australia 0, so the release
    baseline is about two families behind. Focus is an operator/consumer view of ServiceNow
    as the ITSM tool: generic ITIL process pages (change approval/risk matrix, decommission
    workflows, maintenance windows), REST-API runbooks (operations/procedures 940 lines),
    MID Server/Discovery integration, CMDB. Strengths: CMDB 40 pages, change/CAB/risk 17,
    SLA/OLA 19, MID Server 17, Discovery 14, integration/REST 15, notifications 15,
    upgrade 20, business rules/client scripts 12, import sets 10, ACLs 9. Several stubs
    (templates/*, standard-changes, emergency-changes at 21-23 lines; emergency-change and
    emergency-changes are duplicate dirs). No exam-blueprint content (0 pages mention CSA,
    CIS, or blueprint).
  - Cert research (2026-11-25): Target exam: **ServiceNow Certified System Administrator
    (CSA)**, the platform-admin mainline credential and prerequisite for every CIS path.
    Blueprint: Knowledge Portal article **KB0011554 v11.0 (latest), "Updated January
    2026"**. WebFetch returns an empty JS shell; the coordinating session read it in a
    rendered headless browser on 2026-11-25. Format (verbatim from KB0011554): 90
    minutes; 60 questions; multiple choice (>=3 options) and multiple select (>=4
    options, stated count, no partial credit); one point per question; cut score "not
    publicly shared and is not always 70%"; delivered by **Pearson** (test centre or
    OnVUE online); register then schedule within 90 days; fees non-refundable;
    instructor-led training includes one free attempt. Recommended experience: 3-6
    months maintaining an instance. Recommended training: Welcome to ServiceNow;
    ServiceNow Administration Fundamentals; official practice exams via MeasureUp
    (KB0013408). Domains: **(1) Platform Overview and Navigation 7%** (platform
    overview, capabilities/services, the instance, Next Experience Unified Navigation);
    **(2) Instance Configuration 10%** (installing apps and plugins, personalizing/
    customizing, common UIs); **(3) Configuring Applications for Collaboration 20%**
    (lists/filters/tags, list and form anatomy, form configuration, form templates and
    saving options, advanced form config, task management, Visual Task Boards,
    visualizations/dashboards/Platform Analytics, notifications); **(4) Self Service &
    Automation 20%** (Knowledge Management, Service Catalog, Workflow Studio, Virtual
    Agent); **(5) Database Management and Platform Security 30%** (data schema,
    application/access control, importing data, CMDB and CSDM, Security Center, Shared
    Responsibility Model); **(6) Data Migration and Integration 13%** (UI policies,
    business rules, update sets, scripting). The article does not name the platform
    release the exam is built on; a community MVP post (2025-12-31, not staff) says
    mainline exams moved to Zurich, and a June 2026 community reply (not staff) says
    no Australia cutover date was declared. Release not verified from a vendor page.
    Superseded vendor spec (CSA, San Diego, April 2022) had 5 domains; ignore it.
    Secondary: CIS-ITSM (Implementation Specialist - ITSM). Only the 3Q2017 vendor PDF
    was fetched (prereqs CSA + ITIL; Incident, Problem, Change, CMDB, Knowledge,
    Catalog/Request); its current blueprint was not read. Also relevant later:
    CIS-Data Foundations (CMDB/CSDM) and CIS-Discovery (search titles only).
    Sources (primary, vendor): https://learning.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0011554
    (rendered in a browser; WebFetch gets an empty shell)
    https://www.servicenow.com/community/s/cgfwn76974/attachments/cgfwn76974/developer-forum/714553/1/cis-itsm-blueprint.pdf (CIS-ITSM 3Q2017, superseded)
    Target bar: CSA (KB0011554 v11.0, Jan 2026 domains above); CIS-ITSM process depth
    second; re-baseline "Applies to" once the exam release is confirmed.
  - Gap vs blueprint (pages mentioning each term, out of 79): Zero coverage: CSA/CIS
    exam framing 0, list/filter/breadcrumb/condition builder 0, Virtual Agent 0, Instance
    Security Center/shared responsibility 0, Service Mapping 0. Thin: Next Experience/UI16
    navigation 1, form layout/designer/UI policy 1, tables/dictionary/schema 1, UI actions 1,
    CSDM 1, Problem mgmt 1, request fulfillment/RITM 1, Now Assist/AI 1, workspaces 1,
    IRE 2, knowledge mgmt 2, Service Portal/Employee Center 2, security_admin/elevation 2,
    app scope/studio 2, family release/Upgrade Center 3, record templates 3, users/groups/
    roles 4, update sets 4, Flow Designer 5, branding/system properties 5, service
    catalog/record producer 6. Covered: CMDB 40, upgrade 20, SLA 19, MID 17, change/CAB 17,
    REST/integration 15, notifications 15, Discovery 14, reports/dashboards 13, scripting
    12, import sets 10, ACLs 9. Phase B should: confirm the exam release (KB0010356) and the current
    CIS-ITSM blueprint in a rendered browser;
    add a CSA exam-map page; build platform-admin pages the section lacks entirely
    (navigation/lists/forms/UI policies/UI actions, data schema & dictionary, users/groups/
    roles/elevation, update sets & app scope, Service Catalog + record producers + Flow
    Designer, Knowledge, Service Portal/Employee Center, Virtual Agent, Instance Security
    Center); add Problem and Request Fulfillment pages for CIS-ITSM; add CSDM/IRE depth;
    re-baseline the "Applies to" lines from Washington/Xanadu to the current exam release;
    flesh out or merge the 21-23-line stubs and the duplicate emergency-change dirs.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered the 12 items done
    this evening from postgresql to mds, since none touched docs/). Queue file only.

### SAN
- [x] san/brocade/fabric-os
  - Audit (2026-11-25): 28 pages, 9,283 lines; subdirs architecture/ (5), deploy/ (1),
    learning-path/ (1), operations/ (9), security/ (5), troubleshooting/ (5), plus
    index.md and release-notes.md. "Applies to:" on 27/28 pages, all FOS 9.x (24 say
    "Brocade FOS 9.x"); version mentions are FOS 9.1.0/9.1.1/9.2.x (plus one each
    8.0/8.2.x); zero mentions of FOS 10.x, which Broadcom shipped as v10.0.1 (release
    notes dated 2026-06-25). Strengths: ISL 19 pages, fabric services/name server 16,
    chassis/blades 16, domain ID 15, SNMP/syslog 13, zoning 12, firmware upgrade 12,
    user accounts/RBAC 12, SSH/certificates 12, configupload/download 11, trunking 11,
    LDAP/RADIUS/TACACS+ 11, porterrshow 10, MAPS 8. Largest pages:
    operations/cli-reference.md (1,205), operations/procedures.md (940),
    troubleshooting/diagnostics.md (894). No exam-blueprint content.
  - Cert research (2026-11-25): No proctored certification exists; the legacy
    BCFA/BCFP/BCSD titles appear nowhere on the current Broadcom pages. Broadcom offers
    free, unproctored, open-book "competency exams" through the Broadcom Learning
    Portal. Target is the Brocade SAN Administrator exam. Its FAQ (FAQ-BSA-Rev0926,
    dated 2026-09-22) gives these details: based on Gen 8 and Gen 7 hardware and FOS
    v10.0.0; 60 questions from 19 subject areas; 90 min; pass mark 75% (45/60);
    unlimited retakes; open book; needs 6 months of experience and 19 free prerequisite
    classes (~14 h). The FAQ says verbatim "as a free non-proctored exam, we do not
    classify it as a certification". The 19 classes on the course catalog's exam
    playlist act as the objectives: Intro to FC SANs (FCSAN-101), FC Fundamentals
    (FC-120), Switch Install & Config (INST-122), Transceivers (HWSFP-121), Gen 7
    Switch/Director HW (HWG7S-122/HWG7D-122), Gen 8 Switch/Director HW
    (HWG8S-120/HWG8D-120), TruFOS Certificates (TruFOS-120), Firmware Mgmt (FW-222),
    Switch User Accounts (SEC-221), Zoning (Zone-220), FSPF (FSPF-121), FC Trunking
    (Trunk-120), Virtual Fabrics (VF-122), MAPS (MAPS-122), Traffic Optimizer (TO-122),
    Adaptive Traffic Optimizer (ATO-120), SANnav Mgmt Portal Overview (MPOV-122).
    Next-level and companion exams: (a) SAN Professional exam (FAQ dated 2022-02-04):
    Gen 6/Gen 7 and FOS v9.0.1a; 60 questions from 15 areas; 90 min; 70%; 16 classes
    covering Fabric Notifications, Flow Monitor/IO Insight, FPI, VF implementation,
    FCIP, Long Distance ISLs, MAPS CLI, switch security, SSL, Federated Authentication
    and SSH. Still listed on the exams page but based on older FOS. (b) Gen 8 SAN
    Specialist (FAQ dated 2026-01-26): FOS v10.0; 40 questions; 50 min; 70%; 5 classes
    covering SAN Fabric Intelligence, ATO, Gen 8 HW and Gen 8 (quantum-safe) security.
    (c) SAN Security Specialist exam: 8-class playlist on SSL, federated auth, SSH, user
    accounts, cipher suites and SANnav security. (d) Gen 7 SAN Specialist (Web Tools,
    FOS v9). (e) SANnav Administrator (out of scope, see san/brocade/sannav). The SAN
    Administrator exam playlist includes MPOV-122 (SANnav), which overlaps with the
    sannav item.
    Sources (primary, vendor): https://www.broadcom.com/support/education/brocade ;
      https://www.broadcom.com/support/education/brocade/technical/exams ;
      https://www.broadcom.com/support/education/brocade/courses ;
      https://docs.broadcom.com/doc/bsn-san-admin-exam-faq ;
      https://docs.broadcom.com/doc/bsn-san-professional-exam-faq ;
      https://docs.broadcom.com/doc/gen-8-san-specialist-exam-faq ;
      https://docs.broadcom.com/doc/FOS-1001-RN
    Target bar: Brocade SAN Administrator exam (FOS v10.0.0, Gen 7/Gen 8; 19-class
      playlist), stretched to the SAN Professional and Gen 8 SAN Specialist playlists
      for expert depth.
  - Gap vs blueprint (pages mentioning each term, out of 28): Zero coverage: FOS 10.x,
    Gen 8 hardware (X8/128G), Traffic Optimizer, Adaptive Traffic Optimizer, SAN Fabric
    Intelligence, TruFOS certificates, quantum-safe security, Fabric Notifications/FPIN,
    Access Gateway, Flow Vision/Flow Monitor, IO Insight, Fabric Vision, IP
    extension/VE_Port, EX_Port, target-driven zoning, DPS/aptpolicy, NVMe/FC, Ports on
    Demand. Thin: NPIV 1, traffic isolation/QoS 1, Web Tools 2, peer zoning 2,
    D_Port/ClearLink 2, in-flight encryption 2, REST API 2, FICON 2, cipher config 2, FC
    routing/LSAN 3, FCIP 3, FSPF 4, FC-SP/DH-CHAP 4, DCC/SCC policies 4, slow drain 4,
    virtual fabrics 5, audit log 5, supportsave 5, Gen 7 6, licensing 6, long
    distance/buffer credits 7. Phase B should: move "Applies to" and version content to
    FOS 10.0.x with a 9.x-to-10.x migration note; add a Gen 7/Gen 8 hardware page
    (switches, X7/X8 directors, blades, optics); add pages on TruFOS certificates,
    Traffic Optimizer/ATO, SAN FI, and Fabric Notifications/FPIN/FPI; deepen
    FSPF/trunking/DPS, virtual fabrics, NPIV/Access Gateway, FC routing, long distance
    and FCIP/extension, and Flow Monitor/IO Insight; add a 19-area exam-mapping page and
    practice questions keyed to the SAN Administrator playlist.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered the 12 items done
    this evening from postgresql to mds, since none touched docs/). Queue file only.
- [x] san/brocade/sannav
  - Audit (2026-11-25): 28 pages, 4,384 lines; subdirs architecture, deploy,
    learning-path, operations, security, troubleshooting (+ index, release-notes).
    "Applies to:" on 27 pages, 23 of them say "Brocade FOS 9.x" (a FOS label, not a
    SANnav one); only 4 name SANnav (2.x / 2.3.x / 2.3.x+). Version mentions stop at
    2.2.0-2.3.1; zero mentions of 2.4 or 3.x (current is 3.0.1), podman, sannavcc,
    or Rocky Linux. release-notes.md lists 2.2.0-2.3.1 only, with placeholder "#"
    links. Docker is mentioned on 1 page (operations/faq.md), but 3.0.0 replaced
    Docker with Podman. Strengths: REST API 19 pages, upgrade 18, discovery 17,
    health 17, SNMP 15, certificates 14, events/alarms 13, backup 12, AD/LDAP 11,
    firmware 11; deep troubleshooting (diagnostics 474 lines, escalation 484) and a
    605-line cli-reference. No exam-blueprint content.
  - Cert research (2026-11-25): No proctored SANnav certification exists. The current
    vendor bar is the free, unproctored "Brocade SANnav Administrator Exam" on the
    Broadcom Learning Portal; Broadcom says it covers SANnav installation,
    administration and fundamental features. Format not verified: no exam FAQ found
    (the guessed docs.broadcom.com FAQ URLs return 404). The sibling SAN
    Administrator exam FAQ (2026-09-22) gives 60 Q / 90 min / 75% / open book and
    says Broadcom does not classify these free, unproctored exams as certifications;
    expect the same model, unverified. Legacy BCFA/BCFP are retired (secondary
    sources only). Objectives = the exam's prerequisite course playlist (11
    courses): MPOV-121 Overview, MPIN-222 Installation, MPMI-222 Migration, MPDI-221
    Fabric Discovery, MPUA-222 User Accounts, MPDA-222 Dashboard, MPRP-222 Reports,
    MPTO-222 Browse Topology, MPIV-222 Inventory, MPFM-221 Fault Management,
    MPZO-223 Zoning. Expert bar = the wider "SANnav playlist" (~35 courses):
    adds OVA install/migration (MPOVA-251), Linux essentials (SILE-220), Disaster
    Recovery (MPDR-221), App Backup/Restore (MPAB-220), Switch Backup (MPSB-221),
    Firmware Mgmt (MPFW-221), Config Policy Mgmt (MPCP-221), MAPS (MPMP-220), Flow
    Mgmt (MPFL-220), Performance Monitoring (MPPM-220), NPTC Dashboard (MPNPTC-220),
    Virtual Fabric (MPVF-220), FC-FC Routing (MPFCR-221), FICON (MPFICON-220),
    Extension (MPEX-220), vCenter (MPvC-220), Call Home (MPCH-220), SupportSave
    (MPSS-221), Support Data Collection (MPDC-220), Webhooks (MPWH-220), LDAP
    (SLDAP-220), FOS Cert Mgmt (MPCM-220), Security (MPSEC-222), Scripts
    (MPSC-120), Global View (GVOV-221), v3.0.0 update (PUT-252), REST API
    (REST-330). Current version: SANnav MP v3.0.1 (RN SANnavMP-301-RN-DE-v4,
    2026-09-09). Since 3.0.0 it runs on Podman instead of Docker. The OVA is Rocky
    9.7 with SELinux enforced and is supported on vCenter 9.x. 3.0.1 adds the
    sannavcc command center, OpenLDAP auth, Config Policy Mgmt and TruFOS/POD
    licensing.
    Sources (primary, vendor): https://www.broadcom.com/support/education/brocade ;
    https://www.broadcom.com/support/education/brocade/technical/exams ;
    https://www.broadcom.com/support/education/brocade/courses ;
    https://docs.broadcom.com/doc/sannav-management-portal-v3.0.1-release-notes ;
    https://docs.broadcom.com/doc/bsn-san-admin-exam-faq
    Target bar: Brocade SANnav Administrator Exam (free, unproctored; prerequisite
    playlist of 11 courses) + SANnav playlist topics, against SANnav MP v3.0.1.
  - Gap vs blueprint (pages mentioning each term, out of 28): Zero coverage: SANnav
    3.x/2.4, Podman, sannavcc, Rocky/OVA OS patching, Config Policy Mgmt, Flow
    Mgmt beyond 1 passing mention (Flow Vision 1), IO/Traffic Insights, NPTC/top
    talkers, Virtual Fabric/logical switch, FC-FC Routing, FICON, Extension/FCIP,
    port fencing, FPIN/autonomous SAN, Kafka/streaming telemetry. Thin: Global View
    2, HA/DR 2-3, vCenter 3, webhooks 1, OVA 4, install script 1, MAPS 4,
    licensing 4, restore 5, switch/config backup 2, SupportSave 4, call home 5,
    topology 5, user accounts 2, investigation mode 1, telemetry 3. Adequate:
    discovery 17, upgrade 18, REST 19, SNMP 15, events 13, dashboard 10, zoning 10,
    reports 8, RBAC 8, LDAP 11. Phase B should: (1) re-baseline every page to
    SANnav MP 3.0.1, fixing the 23 "Applies to: Brocade FOS 9.x" labels, the
    release-notes table (add 2.4.0, 3.0.0, 3.0.1 with real links) and the
    Docker-to-Podman architecture; (2) add deploy pages for OVA (Rocky 9.7, SELinux,
    vCenter 9.x, OS-patch tarballs) vs VM/BM install, sannavcc, and migration
    2.x to 3.0.x; (3) add one page per missing playlist topic: Config Policy Mgmt,
    MAPS policies/violations, Flow Mgmt + performance monitoring/NPTC, Virtual
    Fabric, FC-FC routing, FICON, Extension, DR, App vs switch backup, vCenter,
    webhooks, Call Home/SupportSave/data collection, FOS cert mgmt, licensing
    (TruFOS/POD); (4) cover Global View (GVOV-221) on its own page; (5) add a
    learning-path map to the 11 exam-prerequisite courses. Overlap: MAPS, zoning,
    FOS licensing, Virtual Fabric, FCR and Extension concepts belong to
    san/brocade/fabric-os (researched separately). Keep SANnav pages to the
    management workflow and link to fabric-os for the concepts. The SAN Admin exam
    playlist also includes MPOV-122.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered the 12 items done
    this evening from postgresql to mds, since none touched docs/). Queue file only.
- [x] san/cisco/cisco-dcnm
  - Audit (2026-11-25): 28 pages, 4,933 lines; subdirs architecture/ deploy/
    learning-path/ operations/ security/ troubleshooting/ (+ index, release-notes).
    "Applies to:" on 27 pages: 14 "Cisco MDS / NX-OS", 9 "Cisco MDS · Nexus", 4 name
    DCNM 11.x (2 add "/ NDFC 12.x"). Version strings: "DCNM 11" x15, "NDFC 12" x5, and
    single hits for DCNM 11.4, 11.5, 11.5(x), 11.5.4.0, 12.0, 12.1, 12.1.3, 12.2.
    LIFECYCLE IS THE BIGGEST ACCURACY PROBLEM. Cisco EoL notices: DCNM 11.0.x-11.4.x had
    End-of-Sale 2022-10-14 and Last Date of Support 2025-10-31. DCNM 11.5(1)-11.5(4)
    (EoL15194, announced 2023-10-18) had End-of-Sale 2024-04-17, End of SW Maintenance
    2025-04-17, and Last Date of Support 2026-04-30, with migration to NDFC 12.x at no
    extra license. So all of DCNM is now past Last Date of Support. The KB never gives
    these dates; 0/28 pages mention "Last Date of Support"/2026-04-30. Only 2 pages
    mention EoL at all, both vaguely (how-it-works table "EoL announced"; release-notes
    glossary). 26/28 pages read as if DCNM 11.x is a current, supported product, and the
    landing page has no EoL banner. Factual errors: release-notes.md lists
    "DCNM 12.0 2022-Q4 rebrand", "DCNM 12.1 2023-Q3", and "DCNM 12.2 2024-Q2". There
    was no DCNM 12; 12.x is NDFC, and NDFC 12.0.1a's series release date on Cisco's
    support page is 28-Sep-2021. All 5 release-note links are placeholders "(#)".
    security/hardening.md shows "Welcome to Cisco DCNM 12.1.3" (should be NDFC).
    architecture/how-it-works.md says 12.0 was "(2022)" (it was 2021). Strengths:
    escalation (467 lines), CLI reference (541), and diagnostics (591) are substantial;
    SNMP 14/28, upgrade/migrate 14/28, zoning 12/28, backup 12/28, and AAA 9/28 are
    well covered. The DCNM-to-NDFC migration note is present (how-it-works, deploy,
    faq). Overlap: NDFC content belongs in the companion queue item
    san/cisco/nexus-dashboard.
  - Cert research (2026-11-25): No current exam targets DCNM. The SAN-specific exam,
    300-625 DCSAN, is retired: Cisco's retired-exams page gives its last day to test as
    2023-04-19, with no replacement listed. The current CCNP Data Center exams page
    lists core 350-601 DCCOR plus concentrations 300-610 DCID, 300-615 DCIT, 300-620
    DCACI, 300-635 DCNAUTO, and 300-640 DCAI. That page shows no versions and no
    DCSAN. Closest live targets, verified from the official exam-topics PDFs (©2024,
    downloaded and text-extracted):
    - 350-601 DCCOR v1.2: 120 minutes; English and Japanese; US$400 per the cisco.com
      exam page. Domains: Network 25%, Compute 25%, Storage Network 20%, Automation and
      AI 15%, Security 15%. 3.1 Implement Fibre Channel (a switch fabric init, b port
      channels, c FCID, d CFS, e zoning, f FCNS, g device alias, h NPV/NPIV, i VSAN);
      3.2 NFS/iSCSI; 3.3 software updates (disruptive/nondisruptive, EPLD); 3.4
      monitoring with SPAN and Cisco Nexus Dashboard; 5.3 storage security (AAA/RBAC,
      port security, fabric binding); 1.11 Nexus Dashboard capabilities; 4.2.d
      Nexus Dashboard automation.
    - 300-615 DCIT v1.2: 90 minutes. Storage Network 15% covers 3.1 FC physical
      (fabric init, buffer-credit starvation, NPV/NPIV, VSAN) and 3.2 FC services
      (FCID, zoning, device alias, CFS). Management and Operations 20% covers 5.1
      firmware upgrades, 5.2 centralized-management integration such as Nexus
      Dashboard, and 5.6 storage security (AAA/RBAC, port security, fabric binding).
    Neither blueprint names DCNM or NDFC; management is framed as "Cisco Nexus
    Dashboard". Not verified: whether v1.2 is the live version. learningnetwork's
    dccor-exam-topics page is JavaScript-rendered (it returned a CSS-error shell), and
    the cisco.com exam pages state no version.
    Sources (primary, vendor):
    cisco.com/c/en/us/products/collateral/cloud-systems-management/prime-data-center-network-manager/data-center-network-11-5-x-eol.html;
    cisco.com/c/en/us/products/collateral/cloud-systems-management/prime-data-center-network-manager/data-center-network-manager-11-0x-11-4x-eol.html;
    cisco.com/site/us/en/learn/training-certifications/certifications/datacenter/ccnp-data-center/exams-and-training.html;
    cisco.com/site/us/en/learn/training-certifications/exams/retired.html;
    cisco.com/site/us/en/learn/training-certifications/exams/dccor.html;
    cisco.com/c/en/us/training-events/training-certifications/exams/current-list/dccor-300-601.html;
    learningcontent.cisco.com/documents/marketing/exam-topics/350-601-DCCOR-v1.2.pdf;
    learningcontent.cisco.com/documents/marketing/exam-topics/300-615-DCIT-v1.2.pdf;
    cisco.com/c/en/us/support/cloud-systems-management/nexus-dashboard-fabric-controller-12/model.html
    Target bar: DCCOR v1.2 domain 3 + 5.3 and DCIT v1.2 domain 3 + 5.6 storage
    objectives, done on MDS/NX-OS, with DCNM framed as legacy (EoL, past LDoS 2026-04-30)
    and current management pointed at Nexus Dashboard/NDFC (companion item).
  - Gap vs blueprint (pages mentioning each term, out of 28): Zero coverage: NPIV 0,
    NPV 0, FCNS/name server 0, FSPF 0, CFS 0, fabric binding 0, port security 0,
    FC-SP/DHCHAP 0, FCoE 0, EPLD 0, buffer-credit/slow-drain/congestion 0, smart or
    enhanced zoning 0, IVR 0, FICON 0, NVMe 0, SAN Analytics/SAN Insights 0, NDFC SAN
    controller persona 0, DCNM Last Date of Support 0. Thin: FLOGI 1, FCID 1,
    trunking/TE 1, iSCSI/NFS 1, Intersight 1, performance monitor 1, zoneset 2,
    port-channel 2, EoL 2, device-alias 3, Native HA 3, telemetry 3, image
    management 3, license 4, VSAN 7, RBAC 7. Phase B should: (1) add an
    EoL/LDoS admonition to the landing page and every "Applies to" line, citing
    EoL15194 and the 11.0-11.4 notice dates, and fix release-notes.md (remove the
    invented "DCNM 12.x" rows and placeholder links; NDFC 12.0.1a is 2021) plus the
    hardening.md 12.1.3 banner and the how-it-works "(2022)" date. (2) Decide scope with
    san/cisco/nexus-dashboard: keep DCNM as a legacy/migration section (DCNM 11.5 to
    NDFC 12.x migration runbook, inventory/zone/device-alias export) and route
    blueprint learning content to NDFC/MDS pages rather than writing new DCNM content.
    (3) Wherever SAN fundamentals live, cover the DCCOR 3.1 list (fabric init, FCID,
    FCNS, CFS, NPV/NPIV, VSAN, port channels, device alias, zoning), 3.3 EPLD and
    nondisruptive upgrades, 5.3 port security and fabric binding, and DCIT buffer-credit
    starvation troubleshooting.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered the 12 items done
    this evening from postgresql to mds, since none touched docs/). Queue file only.
- [x] san/cisco/mds
  - Audit (2026-11-25): 28 pages, 9,147 lines; subdirs architecture/ (5), deploy/ (1, 754
    lines), learning-path/ (1), operations/ (9, incl. cli-reference 1,256 + scripts 861),
    security/ (5), troubleshooting/ (5), plus index + release-notes. "Applies to" on 28
    lines but generic: 12x "Cisco MDS / NX-OS", 12x "Cisco MDS · Nexus" (mis-scoped), 3x
    "NX-OS 8.x / 9.x" or "9.x"; deploy names 9132T/9148T/9396T + 9706/9710/9718. Only 6
    NX-OS version strings in the whole section (9.2(2), 9.3(1), 9.3(2), 9.4(2), 9.4(3),
    9.4(x)); release-notes.md tops out at 9.4(3) "2024-Q3" with placeholder [Release
    Notes](#) links, current is 9.4(5a) (01-Sep-2026). Strengths: VSAN 25/28 pages, zoning
    22, FLOGI 17, upgrade 15 (install all; ISSU named on 7), trunking 13, domain-id 13,
    AAA 13, FCID 12, SNMP 12, DCNM/NDFC 10, IVR 9. No exam-blueprint content (0 pages
    mention DCSAN, 300-625, DCCOR, 350-601 or CCNP).
  - Cert research (2026-11-25): No current MDS-specific exam. 300-625 DCSAN (Implementing
    Cisco Storage Area Networking) is RETIRED: Cisco retired-exams page lists "300-625
    DCSAN | April 19, 2023 | CCNP Data Center" with no replacement; the CCNP Data Center
    exams page now lists only 350-601 DCCOR core + concentrations 300-610 DCID, 300-615
    DCIT, 300-620 DCACI, 300-635 DCNAUTO, 300-640 DCAI (no SAN concentration). DCSAN
    blueprint PDF on learningcontent.cisco.com returns 403, not used. Target is therefore
    350-601 DCCOR v1.2 (CCNP + CCIE Data Center core): 120 min, English/Japanese, US$400
    (cisco.com exam page; version not stated there). v1.2 blueprint taken from the
    official exam-topics PDF (created 13-Jan-2025); learningnetwork.cisco.com exam-topics
    page is JavaScript-rendered (returned "Sorry to interrupt / CSS Error"), so the
    current version could not be confirmed there; v1.3/v2.0 PDF URLs return 403. No DCCOR
    retirement found. Domains: 1.0 Network 25% (OSPF/MP-BGP/PIM/FHRP, RSTP+/LACP/vPC,
    VXLAN EVPN, ACI, packet flow, NIST cloud models, software updates disruptive/
    nondisruptive/EPLD/patches, config mgmt, monitoring NetFlow/SPAN/Nexus Dashboard,
    streaming telemetry, Nexus Dashboard). 2.0 Compute 25% (UCS rack/blade incl. 2.2.d SAN
    connectivity, FC zoning, VSANs, WWN pools, SAN policies; UCS-X IMM; firmware; backup;
    SPAN/Intersight). 3.0 Storage Network 20% - the MDS-relevant domain: 3.1 Implement
    Fibre Channel (a switch fabric initialization, b port channels, c FCID, d CFS, e
    zoning, f FCNS, g device alias, h NPV and NPIV, i VSAN); 3.2 describe NFS and iSCSI;
    3.3 software updates disruptive/nondisruptive and EPLD; 3.4 monitoring with SPAN and
    Nexus Dashboard. 4.0 Automation and AI 15% (EEM, scheduler, Bash/Guest Shell, NX-API
    JSON/XML, on-box Python; Ansible, Python, POAP, Nexus Dashboard, PowerShell,
    Terraform, Intersight; AI DC networking). 5.0 Security 15% (5.3 storage security: AAA
    and RBAC, port security, fabric binding; plus network/compute security).
    MDS NX-OS: release-notes list tops at 9.4(5a) 01-Sep-2026; "Recommended Releases for
    Cisco MDS 9000 Series Switches" dated 06-Aug-2026 (content not fetched, guessed URL
    404 - recommended release not verified); no 10.x listed.
    Sources (primary, vendor):
    https://www.cisco.com/site/us/en/learn/training-certifications/certifications/datacenter/ccnp-data-center/exams-and-training.html
    https://www.cisco.com/site/us/en/learn/training-certifications/exams/retired.html
    https://www.cisco.com/site/us/en/learn/training-certifications/exams/dccor.html
    https://learningcontent.cisco.com/documents/marketing/exam-topics/350-601-DCCOR-v1.2.pdf
    https://www.cisco.com/c/en/us/support/storage-networking/mds-9000-nx-os-san-os-software/products-release-notes-list.html
    Target bar: Fully answer DCCOR v1.2 domain 3.0 (all 3.1.a-i) and 5.3 on MDS 9.4(x),
    plus the MDS slice of 1.7/1.9/1.10 and 4.1; keep retired-DCSAN depth (IVR, FCIP,
    analytics) as practitioner content, not exam-mapped.
  - Gap vs blueprint (pages mentioning each term, out of 28): Zero coverage: EEM 0,
    scheduler 0, POAP 0, DIRL 0, FPIN 0, FC-NVMe/NVMe 0, autozone 0, peer/target-driven
    zoning 0, exam-blueprint mapping 0. Thin: fabric binding 1, port security 1, EPLD 1,
    congestion 1, slow drain 1, FICON 1, iSCSI 1, NFS 1, Bash/Guest Shell 1, fcalias 1,
    FCIP 2, smart zoning 2, DHCHAP/FC-SP 3, NX-API/Ansible/Python 3, principal switch/
    BF/RCF 4, NPV 4, SAN analytics 4, telemetry 4, Nexus Dashboard 4, NPIV 5, FCoE 5,
    RBAC (term) 5, enhanced zoning 6, CFS 6, SPAN 6, nondisruptive 6, ISSU (term) 7,
    device-alias 8, port-channel 8, FCNS 8. Version drift: only 2 pages mention 9.4;
    release notes stop at 9.4(3). Phase B should: (1) add a DCCOR 3.0/5.3 objective map
    page; (2) write fabric-initialization (principal switch, domain ID, BF/RCF, FCID
    allocation), CFS, FCNS, device-alias (basic/enhanced mode) and NPV/NPIV deep pages;
    (3) storage security page: port security + fabric binding config/verify, AAA/RBAC on
    MDS; (4) software-update page: disruptive vs nondisruptive install all, EPLD upgrade;
    (5) monitoring: SPAN/fcanalyzer, SAN analytics/telemetry, Nexus Dashboard (SAN);
    (6) MDS automation: EEM, scheduler, Bash/Guest Shell, NX-API, on-box Python, POAP;
    (7) modern features: FC-NVMe, DIRL/FPIN congestion/slow drain, smart/auto zoning;
    (8) refresh release-notes to 9.4(5a) and fix "Cisco MDS · Nexus" Applies-to lines.
    Overlap: Nexus Dashboard/DCNM-NDFC SAN items (1.9, 1.11, 3.4, 4.2.d) are shared with
    san/cisco/cisco-dcnm (researched separately); UCS 2.2.d SAN items belong to UCS.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered the 12 items done
    this evening from postgresql to mds, since none touched docs/). Queue file only.
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
