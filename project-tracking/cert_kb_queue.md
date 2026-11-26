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
- [x] san/cisco/nexus-dashboard
  - Audit (2026-11-25): 31 pages, 5,275 lines, 6 subdirs (architecture, deploy,
    operations, security, troubleshooting, learning-path) + index + release-notes.
    "Applies to:" 15x "Cisco MDS / NX-OS", 12x "Cisco MDS · Nexus", 3x "Nexus
    Dashboard 3.x" (/NDFC 12.x /NDI 6.x), 1 none. Version mentions top out at ND 3.2
    and NDFC 12.2.2; ZERO pages mention ND 4.x (current line, see below). Whole
    section is one major release stale: ND 4.1.1 (GA Aug 2025) unified Fabric
    Controller + Orchestrator + Insights into a single product, no per-service
    install/upgrade; KB still teaches "install NDFC/NDI as apps on ND 3.x".
    Factual errors / stale claims found:
    - release-notes.md: table stops at 3.2 "2024-Q3"; all links are "#"; quarter
      dates not verified against Cisco; no 4.1/4.2/4.3 rows; Applies-to says MDS/NX-OS.
    - operations/faq.md:20 "ND 3.1.x with NDFC 12.2.x is the current recommendation"
      and "cluster of 3 or 5 nodes": stale (4.x; 4.1 added 1-node/3-node pND
      ND-NODE-G5S/G5L; 4.3.1 deprecates 3-node vND large and 5-node vND app
      deployments for greenfield). ND 3.0/3.1/3.2 EoS/EoL notice posted 26-Aug-2026.
    - troubleshooting/escalation.md:102 sample output "Nexus Dashboard Fabric
      Controller 2.1.4" (NDFC versions are 12.x) plus "Multi-Site Orchestrator 3.2.1"
      running alongside NDO 3.5.2 (MSO-renamed-to-NDO co-residency: not verified).
    - troubleshooting/common-issues.md:180-183 sample "dcnm 14.1.1" and "ndfc 14.1.1"
      as separate ND apps, plus "ise 3.2.1" as an ND app: invented (no DCNM/NDFC 14.x;
      ISE-as-ND-app not verified, believed wrong). operations/common-issues.md:42 node version
      "14.1.2.1" also invented.
    - Inconsistent sample versions across pages (ND CLI v2.3.1.1a, v2.3.1.4a,
      v3.2.1.4a; ND 3.1.1/3.1.2/3.2.1.1a; NDFC 12.1.3/12.2.1/12.2.2; NDI 6.2.1/6.3.1).
    - deploy/index.md:234 sends readers to "the Cisco DCNM deployment guide" for NDFC
      fabric creation (DCNM past LDoS 2026-04-30).
    - `acs ...` CLI (acs system ntp, acs backup remote, acs upgrade start --version,
      acs network test, acs system resources) used on ~17 pages: not verified against
      Cisco docs; Phase B must check each verb against the ND CLI reference.
  - Cert research (2026-11-25): No Nexus-Dashboard or SAN-specific Cisco cert exists
    (300-625 DCSAN retired 2023-04-19, per coordinator). Nexus Dashboard is named
    explicitly in DCCOR v1.2, DCID v1.2 and DCIT v1.2 blueprints (verified via PDF):
    - 350-601 DCCOR v1.2 (120 min): 1.9 infra monitoring incl. "Cisco Nexus
      Dashboard"; 1.10 network assurance / streaming telemetry; 1.11 "Describe the
      capabilities and features of Nexus Dashboard"; 3.4 storage monitoring with
      SPAN and Nexus Dashboard; 3.1 FC (FCID, zoning, FCNS, NPV/NPIV, VSAN) as the
      SAN fabric content ND manages; 3.3 software updates (disruptive/non, EPLD);
      4.2.d evaluate Nexus Dashboard as automation/orchestration tech.
    - 300-610 DCID v1.2 (90 min; 35 Net/25 Compute/20 Storage/20 Automation): 1.7.c
      centralized management and monitoring such as Nexus Dashboard; 4.4 evaluate
      automatic network deployment using Nexus Dashboard.
    - 300-615 DCIT v1.2 (90 min; 25/25/15 Storage/15 Automation/20 Mgmt&Ops): 5.2
      troubleshoot integration of centralized mgmt such as Nexus Dashboard and
      Intersight; 5.1 firmware upgrades/interoperability; 3.1-3.2 FC troubleshooting
      (buffer-credit starvation, NPV/NPIV, VSAN, FCID, zoning); 5.3 AAA/RBAC,
      fabric binding, MACsec.
    Current product: Nexus Dashboard 4.3.1 (4.3.1.175, available 2026-08-22) is the
    highest release on cisco.com; 4.2.1 (RN 2026-03-12), 4.1.1g (2025-08-13). From
    4.1.1 the platform and services are "unified into a single product"; upgrade
    paths are from ND 3.2.2 or 4.1.1. Standalone NDFC RN list tops at 12.2.1 on the
    series page (later 12.2.x patch numbers not verified).
    Sources (primary, vendor):
    https://learningcontent.cisco.com/documents/marketing/exam-topics/350-601-DCCOR-v1.2.pdf
    https://learningcontent.cisco.com/documents/marketing/exam-topics/300-610-DCID-v1.2.pdf
    https://learningcontent.cisco.com/documents/marketing/exam-topics/300-615-DCIT-v1.2.pdf
    https://www.cisco.com/c/en/us/support/data-center-analytics/nexus-dashboard/series.html
    https://www.cisco.com/c/en/us/td/docs/dcn/nd/4x/release-notes/cisco-nexus-dashboard-release-notes-431.pdf
    https://www.cisco.com/c/en/us/td/docs/dcn/nd/4x/release-notes/cisco-nexus-dashboard-release-notes-411.pdf
    Target bar: 350-601 DCCOR v1.2 ND objectives (1.9-1.11, 3.4, 4.2.d) + DCIT 5.2 +
    DCID 1.7.c/4.4, taught on Nexus Dashboard 4.x (4.3.1) unified, with 3.2 as legacy.
  - Gap vs blueprint (pages mentioning each term, out of 31): Zero coverage: ND 4.x /
    unified product (0), NPV/NPIV (0), FCID/FCNS (0), buffer credits (0), Ansible (0),
    Terraform (0), MACsec/fabric binding (0). Thin: POAP 1, Intersight 1, Connected
    TAC/tech-support 1, ISSU/EPLD/image mgmt 1, SAN Insights/Analytics 2, VXLAN EVPN 2,
    device-alias 3, templates 4, persistent IP/data vs mgmt network 4, SAN fabric 5,
    VSAN 5, RBAC 5, zoning 6, SPAN 6, NetFlow/flow telemetry 6, NDO 6. Adequate:
    telemetry 14, NDFC 17, Insights 20, backup 19, anomaly/assurance 10, REST API 8,
    AAA 8 (MDS 31 is inflated by Applies-to lines; ~9 pages discuss MDS in body).
    Phase B should: (1) rebase the section on ND 4.3.1 unified (single install,
    unified RBAC/6 roles, unified fabric types, 1/3-node pND G5, vND cluster
    types + 4.3.1 deprecations, upgrade from 3.2.2/4.1.1) with 3.x as legacy +
    EoL note; (2) rewrite release-notes.md with real 3.0-4.3.1 rows and links;
    (3) fix the invented versions (NDFC 2.1.4, dcnm/ndfc 14.1.1, ise-as-app, MSO+NDO)
    and normalise samples; (4) verify every `acs` verb against Cisco docs; (5) add SAN
    workflow pages on ND (SAN fabric create, zoning/device-alias, VSAN, NPV/NPIV
    visibility, SAN Insights, buffer-credit/slow-drain views) mapped to DCCOR 3.1/3.4
    and DCIT 3.1-3.2; (6) add automation page (ND REST API, Ansible collections (names not verified),
    Terraform, POAP) for DCCOR 4.2.d/DCID 4.4; (7) add DCIT-5.2-style integration
    troubleshooting (ND<->switch discovery, Intersight/Connected TAC); (8) fix
    Applies-to lines to "Nexus Dashboard 4.x (3.2 legacy)".
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered these 8 items, none
    touched docs/). Queue file only.

### Security
- [x] security/certificates
  - Audit (2026-11-25): 29 pages, 5,103 lines; no product subdirs (Venafi/CyberArk live
    under security/products/ and are separate queue items). Subdirs architecture/
    (how-it-works, integrations, design-standards, ports), deploy/pki-deployment,
    learning-path/, operations/ (backup-restore, certificate-trust, cli-reference,
    health-checks, install-upgrade, procedures, scripts, faq), security/ (access-control,
    authentication, encryption, hardening), troubleshooting/ (common-issues, diagnostics,
    escalation, known-issues), release-notes. Biggest: procedures 603, diagnostics 535,
    backup-restore 445, cli-reference 364. "Applies to": 6 lines -- 2x "All products
    (Security)", 1x "Windows Server 2019 / 2022 CA role", 1x "Microsoft ADCS, Let's
    Encrypt, general TLS/PKI", 1x "Microsoft ADCS / Venafi TPP / Let's Encrypt / ACME",
    1x "Linux (RHEL/Ubuntu) / Windows Server / OpenSSL 3.x / ADCS". Version mentions:
    Windows Server 2022 (2), 2019 (1), 2008 R2 (1, template compatibility), OpenSSL 3
    (1), TLS 1.3 (7), TLS 1.2 (1). Scope is enterprise/internal PKI ops: ADCS two/three-
    tier hierarchy, CDP/AIA, CRL/OCSP, auto-enrollment, openssl/certutil/keytool, ACME/
    Let's Encrypt, Venafi TPP API. Strengths: CRL 24 pages, ADCS 21, chain/intermediate
    17, OCSP 14, ACME 14, PEM/DER 14, X.509 13, autoenrollment 12, CSR 11, SAN 11,
    CDP/AIA 11, HSM 11, Let's Encrypt 11; 24/29 pages carry a diagram. No exam content.
    Factual errors spotted: (1) operations/faq.md:28 says public TLS max is "397 days
    (browser requirement since 2020)" -- wrong since 2026-03-15 (CA/B BR: 200 days now,
    100 days from 2027-03-15, 47 days from 2029-03-15, ballot SC081). (2) release-
    notes.md:24 claims "2024-Q4 -- 90-day max validity enforcement" -- no such rule
    exists; the whole version table (2022-2024 rows, links to "#") looks invented and
    should be replaced with a real WebPKI-rules timeline (SC063 OCSP-optional 2024-03-15,
    SC081 schedule). (3) troubleshooting/diagnostics/index.md:138-141 sample shows a
    Let's Encrypt "R3"-issued wildcard with "247 days remaining" -- impossible: LE
    certs are 90 days (or 6-day opt-in). (4) operations/faq.md "How do I check the
    current Certificate Management version?" answer is a cert-dates command (nonsense
    Q/A from a template). (5) learning-path/health-checks lean on OCSP; BR now makes
    OCSP optional for public CAs and requires CRLs -- revocation pages should say so.
  - Cert research (2026-11-25): No vendor-neutral exam is PKI-specialist; no current
    Microsoft exam covers AD CS. Verified AZ-802 "Administering Windows Server" study
    guide (successor to AZ-800/801): 7 domains (AD DS 20-25%, hybrid 10-15%, VMs 10-15%,
    networking 10-15%, storage 15-20%, secure WS 10-15%, monitor/troubleshoot 15-20%)
    with zero AD CS/PKI/certificate objectives -- not a fit. Exam anchor chosen:
    CompTIA Security+ SY0-801 (V8). Verified on comptia.org V8 page: launched November
    17, 2026; max 90 questions (MCQ + performance-based); 90 minutes; pass 750 on
    100-900; English; retirement "estimated 3 years after launch"; SY0-701 (V7, launched
    2023-11-07) retires June 11, 2027 (English) / Aug 13, 2027 (JA/PT/ES/TH). Domains
    (objectives PDF "Document Version 2.0"): 1.0 General Security Concepts 16%, 2.0
    Threats/Vulns/Attacks 24%, 3.0 Security Architecture 19%, 4.0 Security Operations
    27%, 5.0 Program Mgmt & Oversight 14%. PKI lives in obj. 1.3 "Explain the importance
    of using appropriate cryptographic solutions": PKI (public key, private key, key
    escrow); Certificates (CAs, CRLs, OCSP, self-signed, third-party, root of trust, CSR
    generation, wildcard); Encryption (protocols, symmetric, asymmetric, levels full-disk/
    partition/file/volume/database/record, transport, key exchange, algorithms, key
    length); digital signatures; salting; tools; obfuscation; hashing algorithms. Also
    4.1 lists code signing and 802.1X. V8 objectives do NOT list HSM, TPM, OCSP stapling,
    pinning or certificate transparency. Security+ is therefore a floor, far below the
    KB's ADCS depth. DigiCert "Digital Trust Professional" (3 free self-paced courses:
    DNS/PKI/TLS Fundamentals, no exam stated) and "Digital Trust Solutions Engineer"
    (4 product Technical Professional certs, proctored) are vendor-product credentials,
    not chosen. Keyfactor/Sectigo person-certifications: not verified (none found in
    search). (ISC)2 CISSP crypto domain: not verified (not fetched).
    Expert-depth fallback bar (verified): CA/Browser Forum TLS Baseline Requirements
    v2.3.1 (dated 4-Oct-2026): RFC 3647 structure (naming, identity/domain validation
    3.2.2, CAA, lifecycle ch.4 incl. revocation reasons/CRL/OCSP, key sizes 6.1.5 incl.
    P-256/P-384/P-521); validity schedule 398 -> 200 days (2026-03-15) -> 100 days
    (2027-03-15) -> 47 days (2029-03-15) with matching DCV-reuse cuts (SC081, adopted
    2025-04-11); SC063 made OCSP optional and CRLs mandatory (effective 2024-03-15).
    NIST SP 800-57 Part 1 Rev. 5 (May 2020; page shows no superseding notice): key
    management lifecycle, cryptoperiods, key states, protection. Microsoft AD CS docs
    (CA roles, web enrollment, Online Responder, NDES, TPM key attestation, CEP/CES,
    ML-DSA post-quantum signing support) for the internal-PKI depth.
    Sources (primary, vendor):
    https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-802
    https://www.comptia.org/en/certifications/security/
    https://www.comptia.org/en/certifications/security/v7/
    https://www.comptia.org/en/certifications/security/v8/
    https://lecbyo.files.cmp.optimizely.com/download/77f3bd3223ac11f180820e495f189928
    https://www.digicert.com/digital-trust-certification
    https://raw.githubusercontent.com/cabforum/servercert/main/docs/BR.md
    https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
    https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/active-directory-certificate-services-overview
    https://letsencrypt.org/docs/faq/
    Target bar: Security+ SY0-801 obj. 1.3 fully covered as the floor, plus expert depth
    = CA/B BR v2.3.1 lifecycle/validity rules + NIST SP 800-57 Pt1 r5 key management +
    full AD CS role-service coverage (incl. NDES/CEP/CES, key archival, PQC).
  - Gap vs blueprint (pages mentioning each term, out of 29): Zero coverage: CAA,
    S/MIME, post-quantum/ML-DSA, ADCS attack paths (ESC1-ESC16/Certipy), name
    constraints, CLM as a discipline, cryptoperiod, key exchange/ECDHE/forward secrecy,
    salting, RFC 5280, ACME Renewal Info (ARI), SSH certificates, the 200/100/47-day
    WebPKI schedule (the 2 "47 days" hits are sample output). Thin: CEP/CES 1, key
    archival/recovery 1, key escrow 1, self-signed 1, TPM 1, CP/CPS 1, delta CRL 1,
    RFC 8555 1, NDES/SCEP 2, DV/OV/EV 2, JKS 2, digital signatures 2, TLS 1.3 2,
    PKINIT/smart card 2, CA/B Forum BR 3, NIST 3, ECC/ECDSA 3, cert-manager 3, symmetric/
    AES 3, root of trust 3, key usage/EKU 4, certbot 4, PKCS#12 4, wildcard 4, Vault 4,
    CRL reason codes 4, CT logs 5, mTLS 5, code signing 5, key ceremony 5.
    Phase B should: (1) fix the 5 factual errors above (FAQ 397-day claim, invented
    release-notes table, impossible LE sample, nonsense version Q/A, OCSP-optional
    note); (2) add a WebPKI rules page: BR structure, DV/OV/EV, CAA, CT, SC081 validity/
    DCV-reuse schedule, SC063 CRL-vs-OCSP, and the automation implications (ACME, ARI,
    6-day LE certs); (3) add crypto-fundamentals page mapped to Sec+ 1.3: symmetric vs
    asymmetric, key exchange/ECDHE/PFS, hashing/salting, digital signatures, key length,
    encryption levels, key escrow, self-signed vs third-party, root of trust; (4) add
    NIST SP 800-57 key-management page (key states, cryptoperiods, HSM/TPM protection,
    archival/recovery, compromise handling); (5) deepen ADCS: CEP/CES, NDES/SCEP, key
    archival/KRA, CP/CPS, name constraints, template security and ESC attack-path
    hardening, PKINIT/smart-card logon, ML-DSA PQC; (6) add S/MIME, SSH-certificate and
    code-signing coverage; (7) add a Security+ obj.-1.3-mapped exam-prep page with
    practice questions plus a BR/800-57 expert self-check.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered these 8 items, none
    touched docs/). Queue file only.
- [x] security/products/cyberark
  - Audit (2026-11-25): 27 pages, 3,885 lines, 21 subdirs (architecture/{how-it-works,
    integrations,design-standards}, deploy, learning-path, operations/{backup-restore,
    cli-reference,health-checks,install-upgrade,procedures,scripts}, security/
    {access-control,authentication,encryption,hardening}, troubleshooting/{common-issues,
    diagnostics,escalation}). Largest: backup-restore 403, cli-reference 335,
    diagnostics 308; 7 pages <=50 lines. "Applies to:" 20x "CyberArk PAM", 2x "PAS
    12.x", plus singletons "PAS / Privilege Cloud 13.x+", "PAM 13.x+", "PAM 12.x/13.x",
    "PAM (Self-Hosted) 12.x/13.x", "PAM - Vault, PVWA, CPM, PSM" (inconsistent; old
    "PAS" name). Scope is clearly SELF-HOSTED PAM: Vault 24/27, PVWA 24, CPM 21, PSM 20,
    PrivateArk 9, PACLI 4, dbparm.ini 3, DR Vault 14; Privilege Cloud only 3 pages.
    Versions: 13.2 (8, escalation/PACLI samples), 14.2/14.0/13.0/12.6 (release-notes
    only); 10.x hits are IP addresses. Suspect factual errors: release-notes.md table
    ("14.2 - PAM360 integration improvements" - PAM360 is not a CyberArk product name;
    "14.0 - CORA AI launch"; "12.6 - Conjur Cloud GA"; all links "#") looks fabricated -
    not verified against vendor release notes (docs.cyberark.com URL tried returned 404).
    operations/faq.md "CyberArk v13.x (Privilege Cloud)" - Privilege Cloud is SaaS, not
    versioned that way (not verified). No page mentions the 2026 rebrand to Palo Alto
    Networks "Idira" or the certification program change.
  - Cert research (2026-11-25): The CyberArk certification program (Defender PAM-DEF,
    Sentry PAM-SEN, Guardian, etc.) was RETIRED effective 2026-11-10 and moved into the
    Palo Alto Networks certification program at Pearson (registration freeze 11-11..
    11-23; PANW portal reopened 11-24). cyberark.com cert URLs now redirect to
    paloaltonetworks.com/idira; product is "Idira (formerly CyberArk)". Current PANW
    Idira PAM certs: PAM Self-Hosted Analyst, PAM Self-Hosted Engineer, PAM SaaS
    Engineer (all "Specialist" level). TARGET: Palo Alto Networks Certified Privileged
    Access Manager Self-Hosted Engineer (deploy/install/configure/harden, HA focus) -
    matches the KB's self-hosted Vault/PVWA/CPM/PSM scope; companion: PAM Self-Hosted
    Analyst (day-to-day ops). Engineer blueprint (datasheet NOV2026, sums 100%):
    1 CPM 15% | 2 PAM Solution Integration (MFA/PKI/RADIUS/SAML auth; NTP, SMTP, LDAP,
    Syslog/SIEM) 20% | 3 Performance & Load Tuning (Safe/PSM recording retention;
    interval, concurrency, AllowedSafes) 11% | 4 PSM Install/Deploy/Hardening (sizing,
    recording storage, SIA, HTML5 Gateway) 15% | 5 PSM for SSH (maintenance users, MFA
    caching) 10% | 6 Web Access UI (PVWA) deploy, hardening, LB, REST API 13% | 7 Vault
    install/deploy/hardening 16%. Analyst blueprint (sums 100%): Account Onboarding 18 |
    Application Mgmt 10 | Maintenance & Troubleshooting 10 | Password Config & Mgmt 25 |
    Security & Audit 17 | Session Mgmt Config 10 | User Mgmt (Vendor PAM/Remote Access)
    10. Format: Specialist-level price $250 USD (may vary by country); English only, +30
    min ESL extension; multiple choice, matching, ordering items; scaled passing score
    860 of 300-1000 (all PANW exams); valid 2 years, recertify by retaking in the 6
    months before expiry; legacy CyberArk vouchers accepted. Question count and
    duration: not verified (not on page/datasheet/FAQ/handbook). Legacy-to-new exam
    equivalency (e.g., PAM-SEN -> SH Engineer): not verified - Pearson says "will be
    published shortly". Engineer prep ILT: "Idira PAM Self-Hosted Install and Configure".
    Sources (primary, vendor): https://www.pearsonvue.com/us/en/cyberark.html ;
    https://www.cyberark.com/services-support/technical-education/cyberark-certification/
    (redirects to paloaltonetworks.com/idira) ;
    https://www.paloaltonetworks.com/services/education/certification ;
    https://www.paloaltonetworks.com/services/education/palo-alto-networks-pam-sh-engineer
    ; .../palo-alto-networks-pam-sh-analyst ; .../palo-alto-networks-pam-saas-engineer ;
    https://www.paloaltonetworks.com/content/dam/pan/en_US/assets/pdf/datasheets/
    education/pam-sh-engineer-datasheet.pdf ; .../pam-sh-analyst-datasheet.pdf ;
    .../certification-faq.pdf ;
    https://www.paloaltonetworks.com/content/dam/pan/en_US/assets/pdf/ebooks/
    panw-certification-handbook.pdf ; https://www.pearsonvue.com/us/en/paloaltonetworks.html
    Target bar: pass PANW Certified PAM Self-Hosted Engineer (7 domains, 860/1000), with
    Analyst-blueprint ops topics covered as the foundation layer.
  - Gap vs blueprint (pages mentioning each term, out of 27): Zero coverage: HTML5
    Gateway 0, Secure Infrastructure Access/SIA 0, MFA caching 0, PSMP maintenance users
    0, Distributed Vaults 0, logon account 0, time-of-use restrictions 0, loosely
    connected devices 0, Remote Access/Vendor PAM 0, Secrets Hub 0, PTA 0, Idira
    rebrand/new cert program 0. Thin: Privilege Cloud 3, PSM for SSH 6, Master Policy 5,
    reconcile 5, dual control/split workflow 4, onboarding rules/bulk upload/pending
    accounts 4, discovery 1, Plugin Generator/connection components 5, SAML 1, PKI 2,
    NTP 2, SMTP 2, load balancing 2, sizing/storage requirements 2, interval/
    concurrency/AllowedSafes 4, Marketplace platforms 2, SSH keys 3, recording Safe 1,
    live monitoring/termination 2, System Health 3, Secure Tunnel/connectors 3.
    Reasonable: Vault 24, PVWA 24, CPM 21, PSM 20, Platform 20, Safe 19, recording 15,
    LDAP 15, DR 14, REST API 11, hardening 10, PrivateArk 9.
    Phase B should: (1) fix/replace the fabricated release-notes table and normalise
    "Applies to:" to "Idira (formerly CyberArk) PAM Self-Hosted 14.x" after verifying
    current versions; add rebrand note; (2) add per-domain pages for the Engineer
    blueprint: CPM sizing/placement/install/hardening; PSM sizing + recording-storage
    math, PSM post-install, HTML5 Gateway, SIA; PSMP install, maintenance users, MFA
    caching; PVWA install, hardening, load balancing, REST API; Vault install +
    post-install hardening; auth integration (MFA, PKI, RADIUS, SAML) and NTP/SMTP/
    Syslog/SIEM; performance tuning (retention, CPM Interval/MaxConcurrent/AllowedSafes);
    (3) cover Analyst ops topics: discovery + onboarding rules/bulk upload, Master Policy
    workflows (dual control, exclusive/one-time, split workflow, time-of-use), platform
    management (duplication, linked logon/reconcile accounts, usages, loosely connected,
    Marketplace), recording Safes, reports, Vendor PAM; (4) expand the 7 sub-50-line
    pages; (5) add a cert page with blueprint mapping, $250, 860/1000, 2-yr validity.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered these 8 items, none
    touched docs/). Queue file only.
- [x] security/products/venafi
  - Audit (2026-11-25): 26 pages, 3,523 lines, 20 subdirs (architecture/{design-
    standards,how-it-works,integrations}, operations/{backup-restore,cli-reference,
    health-checks,install-upgrade,procedures,scripts}, security/{access-control,
    authentication,encryption,hardening}, troubleshooting/{common-issues,diagnostics,
    escalation}, learning-path). "Applies to:" tally: 21 "Venafi TLS Protect",
    2 "Venafi Trust Protection Platform", 1 "TPP 22.x+", 1 "TPP 22.x / 23.x",
    1 "TLS Protect (TPP) on Windows Server". KB is SELF-HOSTED TPP (Windows/IIS/SQL,
    policy tree, engines); SaaS appears only as side mentions (VaaS 14 hits, "TLS
    Protect Cloud" 8). Versions: TPP 22.x (8 hits), 23.4 (1); release-notes table
    stops at 24.3 with placeholder "#" links. Zero use of current names (Trust
    Protection Foundation, Certificate Manager - Self-Hosted, Palo Alto Networks);
    the 9 "CyberArk" hits are about CyberArk PAM vaulting break-glass creds, not the
    rebrand. Suspected errors: (1) security/authentication + access-control describe
    "built-in roles: Policy Master, Certificate Manager, Approver" (6 "Policy Master"
    hits) - the 26.2 doc TOC shows a "Master Admin" role plus object-level
    permissions and no "Policy Master" topic; verify and rewrite in Phase B.
    (2) release-notes.md version summaries (e.g. "23.2 - machine identity firewall",
    "24.3 - TLS Protect Cloud improvements" on a TPP page) not verified against
    vendor release notes; look generated. (3) Version table is ~5 releases stale.
  - Cert research (2026-11-25): NO current certification exists for this product.
    Naming chain (verified): Venafi Trust Protection Platform / TLS Protect ->
    CyberArk Certificate Manager, Self-Hosted -> Palo Alto Networks "Trust
    Protection Foundation" (26.2 readme: "This product was formerly named Venafi
    Trust Protection Platform"; docs versions 25.1, 25.3, 26.1, 26.2). Certificate
    Manager - Self-Hosted, SSH Manager and Code Sign Manager (ex-CodeSign Protect)
    are products on that foundation. SaaS line (Venafi TLS Protect Cloud/VaaS ->
    CyberArk Certificate Manager SaaS) is now "Next-Gen Trust Security (NGTS)".
    CyberArk brand itself is now "Idira by Palo Alto Networks" (cyberark.com
    certification/training URLs redirect to paloaltonetworks.com/idira). PANW
    certification catalog lists 23 certs (PAM SH Analyst/Engineer, PAM SaaS, EPM,
    IAM, NetSec, Cortex, etc.) - none for certificate/machine identity. PANW ILT
    catalog Idira courses are PAM SH Admin, PAM SH Install & Configure, PAM SaaS,
    EPM only - no Certificate Manager course. Legacy Venafi training site
    (university.venafi.com) no longer resolves. Fallback bar = official 26.2 doc
    set chapter list (extracted from the docs' MadCap TOC data file).
    Sources (primary, vendor):
    https://docs.paloaltonetworks.com/trust-protection-foundation/Docs/26.2/TopNav/Content/Release-Documents/Readme.php
    https://docs.paloaltonetworks.com/trust-protection-foundation/Docs/26.2/TopNav/Data/Tocs/TopNav_TOC_for_products.js
    https://docs.paloaltonetworks.com/trust-protection-foundation/Docs/26.2/TopNav/Data/Tocs/TopNav_TOC_for_products_Chunk0.js
    https://docs.paloaltonetworks.com/trust-protection-foundation/
    https://www.paloaltonetworks.com/network-security/next-gen-trust-security/certificate-manager
    https://www.paloaltonetworks.com/services/education/certification
    https://www.paloaltonetworks.com/services/education/ilt
    https://www.cyberark.com/certification/ (-> paloaltonetworks.com/idira)
    https://www.cyberark.com/services-support/training (-> paloaltonetworks.com/idira)
    https://training.cyberark.com/ (-> learn.paloaltonetworks.com, JS-only)
    Target bar: No exam - expert bar = Trust Protection Foundation 26.2 docs:
    Platform (Install/Upgrade, Administration, Server Agent, Reporting, Log Server,
    Macro guides) + Certificate Manager (Certificate Management Guide 16 chapters,
    CA & Hosting Platform Integration Guide, Troubleshooting) + REST APIs (Auth
    REST, Web SDK).
  - Gap vs blueprint (pages mentioning each term, out of 26): Zero coverage:
    onboard discovery, EST enrollment, application/device objects, system
    encryption keys (software/HSM key storage), custom fields, credential objects,
    macros, Venafi Support Console (VSC), Venafi Operational Certificate (server
    agent client auth), Trust Protection Foundation/Certificate Manager -
    Self-Hosted naming. Thin: SCEP 1, ACME 3, work/client groups 1, dashboards 1,
    SSO/SAML 1, lost certs/root trust 1, Auth REST/OAuth tokens 2, disaster
    recovery 2, adaptable drivers 2, HSM 4, network discovery 5, server agent 7,
    provisioning/installation 7. Adequate: policy folders 19, workflow/approval 15,
    Web SDK/REST 15, MS ADCS 13, public CAs 13, engines 13, reports 10, vcert 9,
    validation 8, CA templates 7, log server/notifications 7. Phase B should:
    rename to "Palo Alto Networks Trust Protection Foundation / Certificate Manager
    - Self-Hosted (formerly Venafi TPP)" with 26.x Applies-to; rebuild release-notes
    from 25.1-26.2 readmes (+ deprecated features page); verify/fix the RBAC model
    (Master Admin + object permissions vs "Policy Master"); add pages for
    discovery (network + onboard), enrollment protocols (SCEP/EST/ACME), app
    objects + certificate installation/drivers, system encryption keys + HSM,
    Server Agent (VOC, client groups, work), custom fields + credentials, Auth
    REST tokens/API integrations, DR operations, VSC, macros/notification rules.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered these 8 items, none
    touched docs/). Queue file only.

### Storage — Ceph
- [x] storage/products/ceph
  - Audit (2026-11-25): 27 pages, 9,669 lines, 22 subdirs (architecture/{how-it-works,
    integrations,design-standards}, deploy, learning-path, operations/{procedures,
    backup-restore,health-checks,install-upgrade,scripts,cli-reference}, security/
    {encryption,hardening,access-control,authentication}, troubleshooting/{diagnostics,
    escalation,common-issues}). "Applies to:" tally: Ceph Reef / Squid x17, "Red Hat
    Ceph Storage · Upstream Ceph" x6, Ceph 18.x (Reef) x2, Reef/Squid x1, Reef/Quincy
    x1. Version mentions: Reef 34, Quincy 37, Squid 21, Octopus 10, Pacific 12,
    Nautilus 5, RHCS 5/6/7 x1 each; Tentacle 0, Umbrella 0, RHCS 8/9 0, "IBM Storage
    Ceph" 0. Focus is upstream cephadm (cephadm on 20/27 pages) with light RHCS nods.
    Factual errors spotted:
    (1) operations/install-upgrade/index.md version table calls Squid 19 "Current
    development, EOL TBD" and Reef 18 "Current stable (LTS)". Per docs.ceph.com,
    Reef is now an archived release, Squid is near EOL (est. 2026-12-02), and
    Tentacle 20 (20.2.5) and Umbrella 21 (21.2.0, 2026-10-28) are the active
    releases. Neither is in the table.
    (2) The same page says "Pacific -> Reef requires an intermediate Quincy upgrade".
    Not verified this session; upstream's skip-one-release upgrade rule should be
    checked before this line is kept.
    (3) deploy/index.md says "Reef = current stable" but the curl fetches cephadm from
    the quincy branch, which is both stale and inconsistent.
    (4) release-notes.md tops out at 18.2 Reef. Its Released dates and "RGW multi-site
    active-active" as a Reef headline look doubtful (multisite predates Reef), and all
    links are placeholders (#).
    (5) troubleshooting/escalation/index.md calls RHCS 6 (Quincy) and RHCS 7 (Reef)
    "current; full support", but RHCS 8 and 9 exist and docs.redhat.com now defaults
    to RHCS 9 (9.1/9.2 docs are PDF only).
  - Cert research (2026-11-25): The candidate EX260 (Red Hat Certified Specialist in
    Ceph Cloud Storage) is RETIRED. The redhat.com EX260 URL now redirects to
    /retired-ex260-... titled "Retired - Red Hat Certified Specialist in Ceph Cloud
    Storage exam". That page still shows the full objective list, a 3-hour
    performance-based format and CL260 as prep. No retirement date is shown (not
    verified). The CL260 and CL261 English pages return 404. The certification page
    (rhcs-ceph-cloud-storage) still lists the skills and EX260 without a retired
    label. The Credly retired-badges collection lists only the older "Specialist in
    Ceph Storage Administration" (EX125), not Ceph Cloud Storage.
    RHCS version EX260 is based on: not verified. The page only says "most recent
    product version available" and the CL261 page that would state it is 404.
    May 2026 framework: the RH T&C FAQ says there are no changes to exam content,
    objectives, recommended training, price or proctoring. That statement covers
    live exams only and is moot for EX260, which is retired.
    Product ownership: Red Hat Ceph Storage still exists (lifecycle page lists
    RHCS 7/8/9, each with 36 months of Production Support). Engineering is IBM's:
    RHCS 9.0 release notes use IBMCEPH-* bug IDs and mention "upgrade to Tentacle",
    which implies RHCS 9 is Tentacle-based (not stated outright).
    IBM replacement credential: "IBM Storage Ceph Administrator" Credly badge,
    Intermediate level, earned by completing IBM DLP course SSCH1DG (IBM Storage Ceph
    Workshop: 3 days self-paced, 14-day labs, graded quizzes). It is a course badge,
    not a proctored exam. IBM's launch blog (2025-10-21) calls the Red Hat Ceph course
    "now-retired". SSCH1DG agenda: cephadm deploy and expand, dashboard, CLI and
    service specs, pools, OSDs and device classes, CephX, RGW, RBD + NVMe, CephFS,
    data protection and CRUSH, tune and troubleshoot, OpenStack/OpenShift
    integration.
    Upstream: Umbrella 21 (21.2.0, released 2026-10-28, est. EOL 2028-06-01),
    Tentacle 20 (20.2.5, est. EOL 2027-06-01), Squid 19 (19.2.7, est. EOL
    2026-12-02). Reef, Quincy and Pacific are archived.
    Sources (primary, vendor):
    https://www.redhat.com/en/services/training/ex260-red-hat-certified-specialist-in-ceph-cloud-storage-exam
    (redirects to the retired- URL),
    https://www.redhat.com/en/services/training/retired-ex260-red-hat-certified-specialist-in-ceph-cloud-storage-exam,
    https://www.redhat.com/en/services/certification/rhcs-ceph-cloud-storage,
    https://www.redhat.com/en/services/training/cl261-cloud-storage-with-red-hat-ceph-storage-with-exam
    (404), https://www.redhat.com/en/services/training/cloud-storage-red-hat-ceph-storage-cl260
    (404), https://www.redhat.com/en/services/training-and-certification/faq,
    https://www.redhat.com/en/blog/validate-targeted-expertise-major-updates-red-hat-certification,
    https://www.credly.com/organizations/red-hat-inc/collections/retired-red-hat-certifications/badge_templates(.json),
    https://www.credly.com/org/ibm/badge/ibm-storage-ceph-administrator,
    https://community.ibm.com/community/user/blogs/upendra-rajan/2025/10/21/ceph-training-from-ibm,
    https://access.redhat.com/support/policy/updates/ceph-storage,
    https://docs.redhat.com/en/documentation/red_hat_ceph_storage (-> /9),
    https://docs.redhat.com/en/documentation/red_hat_ceph_storage/9/html-single/9.0_release_notes/index,
    https://docs.ceph.com/en/latest/releases/
    Target bar: There is no live proctored Ceph exam. Use the last published EX260
    objective list as the task blueprint, modernised to cephadm/orchestrator on
    Tentacle 20 / RHCS 9 / IBM Storage Ceph, and add the SSCH1DG topics (service
    specs, device classes, NVMe-oF, OpenShift). A reader should be able to do every
    EX260 task hands-on from the KB.
  - Gap vs blueprint (pages mentioning each term, out of 27): Zero coverage: pg-upmap/
    balancer 0, NVMe-oF/iSCSI gateway 0, cephfs-mirror 0, stretch mode 0, mClock 0,
    RGW debug logging (debug_rgw) 0, RGW TLS/in-transit encryption (rgw_frontends ssl)
    0, persistent CephFS mount via fstab 0, IBM Storage Ceph 0, Tentacle/Umbrella 0.
    Thin: EC profile 1, device classes 1, rbd-mirror 1 (no pool vs image mode, no
    status), RBD export/import(-diff) 2, RBD clone/snap protect 2, rbd map 2,
    osd_memory_target 2, public/cluster network 2, Grafana 2, service specs 3,
    CephFS snapshots 3, ceph crash 3, alertmanager 3, RADOS namespaces 4, ceph-volume
    4, CRUSH rules 4, recovery tuning (osd_max_backfills etc.) 4, s3cmd/awscli 4,
    Swift CLI/subusers 4, ganesha/NFS 5, multisite 5, erasure 5, OpenStack
    Glance/Cinder 5, deep-scrub 5, pg autoscaler 6, quotas 6. Solid: OSD 26, PGs 23,
    RGW 23, RBD 22, MON quorum 21, cephadm 20, CephFS 19, MDS 16, upgrade 16,
    orchestrator 15, health 14, CRUSH 12, cephx 12, pools 12, S3 12.
    Phase B should:
    (a) fix the version table, release notes, the deploy cephadm URL and the RHCS
    escalation lines to Tentacle/Umbrella and RHCS 8/9, and add an RHCS / IBM
    Storage Ceph <-> upstream mapping, citing sources;
    (b) write one hands-on lab per EX260 objective group: restricted cephx clients
    (pool/namespace caps); EC profile + pool + upload; RBD create/map/snap/clone/
    export-diff/import-diff; one-way rbd-mirror in pool and image mode + status;
    RGW deploy, multisite, S3 and Swift users, NFS export of buckets, in-transit TLS;
    CephFS create, fstab mount, quotas, snapshots; CRUSH bucket hierarchy + rules
    + pg-upmap/balancer; full/nearfull ratios; scrub, recovery and memory tuning;
    debug_rgw; Glance/Cinder RBD backends;
    (c) add SSCH1DG-era topics: service specs, device classes, NVMe-oF gateway,
    stretch mode, mClock, cephfs-mirror and ODF/Rook integration;
    (d) record that EX260 is retired and point readers to the IBM SSCH1DG badge as
    the current vendor credential.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered these 8 items, none
    touched docs/). Queue file only.

### Storage — Dell
- [x] storage/products/dell/apex-storage-as-a-service
  - Audit (2026-11-25): 26 pages, 4,215 lines, 5 subdirs (architecture, operations,
    security, troubleshooting, learning-path) + index + release-notes. Content is
    skewed: scripts.md 1,354 + cli-reference.md 661 + diagnostics.md 449 +
    escalation.md 357 = 67% of lines; 12 pages are <60 lines. "Applies to:" 21x
    "APEX Storage-as-a-Service", 2x "Dell EMC Storage" (stale brand), 2x "Dell APEX
    Block/File/Object Storage", 1x "(block storage)". Names used: APEX Console (19
    pages), CloudIQ (18), PowerStore (15), PowerFlex (12), PowerScale (10), PowerMax
    (2); "APEX Data Storage Services" (Dell's documented name) appears on 0 pages.
    FLAGS: (1) CloudIQ is presented as current; Dell support now calls it "Dell AIOps
    (formerly CloudIQ)" / "APEX AIOps" (0 KB pages say AIOps). (2) release-notes.md
    lists invented-looking versions ("Apex STaaS 2024.3 PowerMax NVMe tier", "2022.3
    PowerScale object tier") with "[Release Notes](#)" dead links; ADSS is a
    service, not a versioned product - not verifiable, treat as fabricated. (3)
    cli-reference/scripts assert api.dell.com OAuth2 token URL + console.dell.com +
    cloudiq.apis.dell.com REST paths - not verified against any Dell API doc. (4)
    Section ignores the public-cloud line (APEX Block/File Storage for AWS/Azure,
    APEX Navigator for Multicloud Storage): 0 pages.
  - Cert research (2026-11-25): NO current Dell Proven Professional exam covers APEX
    storage-as-a-service. Dell Learning "Certification and Badges" page (fetched,
    82 exam codes) lists only APEX Cloud Platform achievements (D-AX-DY-A-00 Azure,
    D-AX-RH-A-00 OpenShift) - compute/HCI, not storage; no APEX Data Storage
    Services / APEX Console / APEX Block or File Storage exam. Feb-2024 exam
    transformation PDF: zero "APEX" hits. Nearest adjacencies checked: D-CS-DS-23
    Cloud Services Design (vendor-neutral cloud strategy; 7 domains, 0 APEX
    mentions) - not a fit; D-PWF-OE-00 PowerFlex Operate (11/26/24) has one
    objective "Describe PowerFlex with APEX" + APEX AIOps Observability - too thin.
    Product status: dell.com/support manuals still publish "Dell APEX Data Storage
    Services" (Roles & Responsibilities for Customer-managed / Dell-managed
    deployments; Remote Access Planning for Dell-managed On-Prem and Colocation) with
    APEX Console + CloudIQ tasks and no EOL notice (revision dates not shown).
    Dell blog 2025-10-22 markets "Dell APEX Infrastructure" (subscription +
    pay-per-use) - storage scope/ADSS relationship not stated. Public cloud: APEX
    Navigator for Multicloud Storage service guide covers APEX Block Storage for AWS
    and APEX File Storage for AWS (US only, 90-day eval); InfoHub Block-for-AWS paper
    says purchasable on AWS Marketplace. NOT VERIFIED: "Flex on Demand" current
    naming and any ADSS rename/retirement (dell.com/dt marketing pages return 403 to
    curl and WebFetch); APEX File Storage for Azure GA (only a Microsoft
    preview-announcement result, not fetched).
    Sources (primary, vendor):
    https://learning.dell.com/content/dell/en-us/home/certification-overview/certificationandbadges.html
    https://learning.dell.com/content/dell/en-us/home/training/apex-training.html
    https://learning.dell.com/content/dam/dell-emc/documents/en-us/Dell%20Technologies%20Proven%20Professional%20Exam%20Updates.pdf
    https://learning.dell.com/content/dam/dell-emc/documents/en-english/D-CS-DS-23_Cloud_Services_Design_Exam.pdf
    https://learning.dell.com/content/dam/dell-emc/documents/en-us/Dell_PowerFlex_Operate_Exam_Description.pdf
    https://www.dell.com/support/manuals/en-us/apex-data-storage-service/roles_response_cust_mgmd_adss_pub/block-storage-activities?guid=guid-657a6276-bae2-4a82-8f73-4f2f9c2f7051&lang=en-us
    https://www.dell.com/support/manuals/en-us/apex-navigator-multi-cloud-storage/apex_nav_multicloud_serviceguide_pub/introduction?guid=guid-9dee03df-6b8a-43f0-96d3-2b99cb7e9e79&lang=en-us
    https://www.dell.com/en-us/infohub/articles/dell-apex-block-storage-for-aws
    https://www.dell.com/support/product-details/en-us/product/cloud-iq/resources/articles
    https://www.dell.com/en-us/blog/transform-your-it-subscription-meets-pay-per-use/
    Target bar: no exam exists - fallback = Dell product doc set: ADSS Roles &
    Responsibilities (Customer- + Dell-managed), ADSS Remote Access Planning (SCG,
    Dell Management Stack, ports/firewall), APEX Navigator for Multicloud Storage
    service guide + InfoHub APEX Block Storage for AWS; underlying-platform depth
    via D-PST-OE-23 PowerStore Operate / D-PWF-OE-01 PowerFlex Operate (both listed).
  - Gap vs blueprint (pages mentioning each term, out of 26): Zero coverage: "Data
    Storage Services" 0, Dell Management Stack 0, virtual gateway 0, AIOps 0, APEX
    Navigator 0, Block/File Storage for AWS/Azure 0, Flex on Demand 0, Terraform 0.
    Thin: customer-managed 2, colocation/Equinix 1, AWS 1, Azure 2, APEX
    Infrastructure 1, replication 4, SAML/SSO 4, MFA 4, firewall 5, Dell-managed 7.
    Adequate: APEX Console 19, CloudIQ 18 (stale name), PowerStore 15, subscription
    14, SCG 13, metering/billing 13, tier 13, PowerFlex 12, snapshot 11, committed
    capacity 10, SLA 10, PowerScale 10, burst 9, responsibilities 9.
    Phase B should: rename to Dell's documented "APEX Data Storage Services" and
    note the "APEX Infrastructure" umbrella (re-verify on dell.com first); replace
    CloudIQ with Dell AIOps (formerly CloudIQ); delete/rebuild release-notes.md
    (no fabricated versions); verify or remove api.dell.com/cloudiq API paths in
    cli-reference+scripts; add Dell- vs customer-managed responsibility matrix
    (block, file, backup target), colocation option, Remote Access Planning (SCG,
    Dell Management Stack, port table); add a public-cloud sub-area (APEX Navigator,
    Block Storage for AWS (PowerFlex-based, per InfoHub), File Storage for AWS,
    90-day eval, US-only); fix "Dell EMC Storage" Applies-to lines; thicken the 12
    sub-60-line pages.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered these 8 items, none
    touched docs/). Queue file only.
- [x] storage/products/dell/cloudiq
  - Audit (2026-11-25): 31 pages, 4,582 lines, 6 subdirs (architecture, deploy,
    learning-path, operations, security, troubleshooting) + index + release-notes.
    "Applies to:" 21 CloudIQ, 7 Dell CloudIQ, 1 Dell CloudIQ SaaS, 1 CloudIQ (SaaS),
    1 CloudIQ / Secure Connect Gateway. Largest: operations/scripts.md (883),
    troubleshooting/escalation.md (459), diagnostics.md (416). RENAMED-PRODUCT FLAG:
    whole section presents "CloudIQ" as the current name; 0 pages mention "Dell
    AIOps", "APEX AIOps" or "Infrastructure Observability". Dell now sells it as
    "Dell AIOps (formerly CloudIQ)" (2024 interim name: APEX AIOps Infrastructure
    Observability). Accuracy flags: release-notes.md version table (2022.4-2024.4)
    has placeholder "(#)" links and is unverified; API examples use 3 different
    base URLs (api.cloudiq.dell.com, cloudiq.apis.dell.com/..., cloudiq.dell.com/
    auth/v1/token) - unverified, likely invented in part. OVERLAP: sibling
    storage/products/dell/dell-aiops (24 pages, 1,772 lines; 21 pages mention
    CloudIQ) covers the same product - Phase B should merge into ONE section
    (dell-aiops as canonical, cloudiq as redirect/"formerly" alias), not build
    two cert-grade sections.
  - Cert research (2026-11-25): NO current Dell Proven Professional exam covers
    CloudIQ/Dell AIOps. Checked 10 exam descriptions via pdftotext - 0 hits for
    "CloudIQ"/"AIOps": D-PST-OE-23 PowerStore Operate, D-PST-DY-23 PowerStore
    Deploy, D-PVM-OE-01 PowerMax Operate v2, D-PVM-DS-01 PowerMax Design v2,
    D-PSC-DY-23 PowerScale Deploy, D-PSC-DS-23 PowerScale Design (its 8%
    monitoring domain names InsightIQ/HealthCheck/SRS, not CloudIQ), D-PSC-MN-23
    (retirement notice), D-MSS-DS-23 Midrange Design, D-CIS-FN-01 Cloud Infra &
    Services Foundations v2; Proven Professional "Exam Updates" (as of 2024-02-05)
    lists no CloudIQ exam. Dell KB 000157827 (mod. 2026-05-04) states CloudIQ
    documentation "is limited to a white paper and on-line help"; no public user
    guide exists. Support manuals page lists only "Dell AIOps Collector Security
    Configuration Guide" (2026-07-14) and "CloudIQ Detailed Review" (2022-05-24).
    Fallback bar = current Dell white paper "Dell AIOps: A Detailed Review"
    (H15691.12, Jan 2026 per search snippet) + Collector Security Config Guide -
    BOTH PDFs returned HTTP 403 to curl and WebFetch, so their TOCs are NOT
    VERIFIED; scope below is from fetched Dell product FAQ + Dell blog only.
    A Dell Demo Center hands-on lab ITD-0511 "Dell AIOps (formerly CloudIQ)" was
    seen only in a search snippet (page requires sign-in) - not verified.
    Sources (primary, vendor): dell.com/en-gb/shop/dell-aiops/sl/aiops (name
    "Dell AIOps (formerly CloudIQ)", ProSupport/ProSupport Plus/ProSupport One
    entitlement, supported products incl. Connectrix/PowerSwitch/VxRail, AIOps
    Assistant, health/anomaly, cyber, sustainability);
    dell.com/support/product-details/en-uk/product/cloud-iq/resources/articles;
    dell.com/support/product-details/en-us/product/cloud-iq/resources/manuals;
    dell.com/support/kbdoc/en-us/000157827; dell.com/en-us/blog/ai-powered-it-
    from-reactive-to-proactive-with-dell-aiops/ (2025-12-15: AIOps Assistant,
    health scores, cyber risk, forecasting incl. SAN optics, carbon, mobile app,
    email digests, APIs/webhooks to Slack/ServiceNow/Ansible/Terraform);
    learning.dell.com exam PDFs listed above (all fetched + pdftotext'd).
    Target bar: no cert exists - expert bar = Dell AIOps Detailed Review
    (H15691.12) feature set + Collector security guide, fetch both before Phase B.
  - Gap vs blueprint (pages mentioning each term, out of 31): Zero coverage:
    Dell AIOps / APEX AIOps / Infrastructure Observability name (0), AIOps
    Assistant/GenAI (0), cybersecurity/vulnerability (0), ransomware (0),
    performance impact analysis (0), health-score categories (0), Connectrix (0),
    PowerSwitch (0), Terraform (0), Report Browser (0), custom reports (0).
    Thin: collector VM 2, misconfiguration 2, sustainability/carbon 2, Slack 2,
    Ansible 2, ProSupport entitlement 2, PowerEdge/OME 3, PowerProtect 3, roles
    3, email digest 3, mobile app 1, VxRail 1. Covered: SCG 14, REST API 15,
    forecast 14, health score 13, webhook 9, SupportAssist/SRS 8, anomaly 6,
    ServiceNow 6. Phase B should: (1) decide merge with dell-aiops and rename to
    "Dell AIOps (formerly CloudIQ)" everywhere; (2) obtain the H15691.12 PDF and
    Collector Security Config Guide (manual download if 403 persists) and rebuild
    against their TOC; (3) add cyber/vulnerability, AIOps Assistant, collector
    (VMware/Connectrix/PowerSwitch), Report Browser/custom reports, RBAC incl.
    DevOps role, sustainability pages; (4) verify or delete the API base URLs and
    the invented release-notes table.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered these 8 items, none
    touched docs/). Queue file only.
- [x] storage/products/dell/cod
  - Audit (2026-11-25): 21 pages, 2,911 lines, 4 subdirs (architecture 5p,
    operations 9p, troubleshooting 5p, learning-path 1p) + index + release-notes.
    Largest: operations/scripts 654, troubleshooting/escalation 433,
    troubleshooting/diagnostics 408, operations/cli-reference 303. Section has
    NO stable identity: "Applies to:" tally = 13x "Cloud for Desktop (COD)",
    4x "Dell Cloud Object Detachment", 2x "Dell PowerMax COD licensing", 1x
    "Dell Cloud on Demand (COD) / PowerMax Cloud on Demand", 1x "Dell PowerMax
    Capacity on Demand (COD)". Body content mostly describes PowerMax/VMAX
    license-gated pre-installed drives activated with a key file via
    SYMCLI/Unisphere (symlmf-style key import, SRP/disk-group capacity), but
    architecture/how-it-works.md also carries an unrelated "Object Storage
    Data Model" (buckets, namespaces, geo-replication) and a "30/90-day
    burst" sequence; FAQ claims PowerStore/Unity CoD licence menus.
    release-notes.md lists invented "COD 2.4-3.2" software versions (COD is
    not a versioned product). Flag for Phase B: mislabeled + partly
    hallucinated content; "Cloud for Desktop" and "Cloud Object Detachment"
    are not Dell storage offerings (no Dell source found for either).
    Overlap: sibling sections storage/products/dell/fod (Flex on Demand) and
    storage/products/dell/apex-storage-as-a-service cover the real Dell
    consumption programs; cod largely duplicates/confuses them.
  - Cert research (2026-11-25): NO current Dell certification covers "Capacity
    on Demand" or any consumption/licensing program. Dell Proven Professional
    catalog (learning.dell.com certification-and-badges, fetched) lists ~80
    exam codes; only APEX items are APEX Cloud Platform implementation
    (Azure/OpenShift), nothing for APEX Flex on Demand / pay-per-use. Nearest
    technical certs are PowerMax: D-PVM-OE-01 PowerMax Operate v2 (75 min
    ~40 Q + 45 min ~8 Q lab; domains: Storage Provisioning 24%, Business
    Continuity Admin 20%, Data Mobility 12%, Monitoring/Workload Planning 10%,
    Local/Remote Replication Concepts 10%, Solutions Enabler 10 10%,
    Unisphere 10 8%, Virtual Env 4%; requirements as of 2024-09-18),
    D-PVM-DS-01 PowerMax Design v2, D-PM-IN-23 Install, D-PM-MN-23
    Maintenance. pdftotext of all four PDFs: zero hits for "licens",
    "entitle", "on demand capacity" -> licensing/COD is not an exam topic.
    Offering status: "PowerMax Capacity on Demand" as a named current Dell
    program NOT VERIFIED (no Dell primary source found; dell.com returns 403
    to automated fetch). Dell's consumption program is now marketed as "Dell
    APEX Infrastructure" pay-per-use: the old en-us flex-on-demand.htm URL
    301-redirects to /dt/apex/subscriptions.htm -> /shop/apex/subscriptions/
    sl/apex-infrastructure (Wayback capture 2026-11-04). That page: "pre-
    deployed buffer capacity", "capped monthly billing at 85% of total
    installed capacity ... Available with Dell Flex on Demand for Storage,
    Data Protection, and VxRail. Dark sites, non-metered deployments ... not
    eligible. 85% billing cap excludes servers"; deployment + support are
    required. This is a COMMERCIAL/FINANCIAL program, not a technical product.
    Sources (primary, vendor):
      https://learning.dell.com/content/dell/en-us/home/certification-overview/certificationandbadges.html
      https://education.dell.com/content/emc/en-us/home/certification-overview.html
      https://learning.dell.com/content/dam/dell-emc/documents/en-us/D-PVM-OE-01-PowerMax_Operate_Exam_Description.pdf
      https://learning.dell.com/content/dam/dell-emc/documents/en-us/ExamDescriptionDellPowerMaxDesignv2ExamD-PVM-DS-01.pdf
      https://learning.dell.com/content/dam/dell-emc/documents/en-us/D-PM-IN-23-Install_PowerMax_Exam.pdf
      https://learning.dell.com/content/dam/dell-emc/documents/en-us/D-PM-MN-23-Maintenance_PowerMax_Exam.pdf
      https://web.archive.org/web/20261104004947id_/https://www.dell.com/en-us/shop/apex/subscriptions/sl/apex-infrastructure
        (archived Dell page; live dell.com 403 to curl/WebFetch)
    Target bar: no cert exists -> expert bar = Dell's own APEX Infrastructure /
    Flex on Demand program terms (commit vs buffer, metering, 85% cap,
    eligibility) + PowerMax licensing/eLicensing (LAC, Solutions Enabler
    license import) at D-PVM-OE-01 operator depth; recommend Phase B merge
    cod into dell/fod rather than build it out.
  - Gap vs blueprint (pages mentioning each term, out of 21): Zero coverage:
    "Flex on Demand" 0, "APEX Infrastructure"/"storage as a service" 0,
    buffer capacity 0, metering 0, pricing 0, data reduction 0. Thin: APEX 1,
    committed/base capacity 1, pay-per-use/consumption 1, billing 1,
    PowerStore 3, Secure Connect Gateway/SRS 2, SRP 5. Heavy (off-target or
    suspect): "Cloud for Desktop" 13, Solutions Enabler/SYMCLI 13, license
    key/file 12, Unisphere 16, PowerMax 16, CloudIQ/AIOps 8, buckets 3.
    Phase B should: (1) decide identity - recommended: retire/merge into
    dell/fod and dell/powermax (licensing), redirect; (2) if kept, retitle as
    "PowerMax licensing & capacity activation" only after a Dell primary
    source confirms the mechanism; (3) delete "Cloud for Desktop"/"Cloud
    Object Detachment" labels, object-storage/bucket section, 30/90-day
    burst claim and fabricated COD 2.4-3.2 release table; (4) verify
    PowerStore/Unity CoD claims or remove; (5) cross-link to APEX
    Infrastructure 85% cap / buffer model in dell/fod.
  - site_audit (2026-11-25): 70/70 clean (full run; one run covered these 8 items, none
    touched docs/). Queue file only.
- [x] storage/products/dell/data-domain
  - Audit (2026-11-25): 27 pages, 10,829 lines; subdirs architecture(5)
    learning-path(1) operations(9) security(5) troubleshooting(5) + index,
    release-notes. "Applies to:" 18x "Data Domain DD OS 7.x", 6x "Dell EMC
    Storage", 1x "DD/PowerProtect DD running DDOS 7.x", 1x "DD OS 7.x / 8.x",
    1x "Data Domain OS 7.x" -- 26/27 pages pinned to the 7.x line; only
    release-notes.md:25 names 8.x (8.1, template table). Product name "PowerProtect
    Data Domain" is still Dell's current name (exam + docs use it), so "Data
    Domain" is fine; "Dell EMC" branding persists (14 lines). Stale/wrong:
    operations/install-upgrade.md:29 "7.13.x Current / Recommended" and :24-30
    matrix (Dell KB 000081247: LTS2026 8.6.1 is Recommended; 7.12 EoSS
    2026-07-31, 7.11 2026-03-31, 7.10.1 2026-04-30; latest feature 8.9.0.0);
    operations/faq.md:20 "DD OS 7.13.x is the current recommendation" (wrong);
    install-upgrade.md:53-56 hardware lifecycle omits DD9910/DD9410/DD6410 (0
    pages mention them); sample output uses DDOS 7.14.1.20 / 7.15.1.x
    (operations/scripts.md:568, cli-reference.md:1236,2139, integrations.md:259,
    hardening.md:431, encryption.md:301) -- no 7.14/7.15 family exists in Dell's
    DDOS versions KB (7.13 -> 8.0), likely invented. Suspect/invented:
    install-upgrade.md:41 "DDVDP protocol", :45 "SISL + DD Boost ... DD
    MediaAgent", :46 "RAIN dedup integration"; encryption.md:117 `system
    enter-maintenance-mode`; release-notes.md:27 "7.12 -- DD3300 platform GA"
    (template table, unverified). learning-path has no cert/exam mapping.
  - Cert research (2026-11-25): Two current Dell Proven Professional exams, both
    listed in Dell's cert catalog: D-PDD-OE-01 "PowerProtect Data Domain Operate"
    (v2) and D-PDD-DY-01 "PowerProtect Data Domain Deploy" (v2); predecessors
    D-PDD-OE-23 / D-PDD-DY-23 (which replaced DES-DD33/DES-DD23 in Nov 2023) are
    no longer in the catalog. No retirement notice found for -01. Both: 90 min,
    50 questions, English/French; passing score and "requirements as of" date
    NOT stated in either PDF (PDF metadata: OE created 2026-04-29, DY
    2026-03-31). OE-01 blueprint: Active Tier Administration 50% (system/support
    settings, access, network interfaces, file system, storage policies, CIFS/
    NFS/DD Boost/VTL, Secure Multitenancy, replication policies, Retention Lock
    on storage units, health/utilization monitoring, upgrades, tuning);
    Integration with Application Software 14%; Cloud Tier Administration 18%
    (config, data movement, tuning); Troubleshooting 18% (backup/restore/
    replication/DR, software+connectivity, capacity+performance). DY-01
    blueprint: Pre-Deployment Check 14% (site requirements, install checklist,
    service tags); Deployment 52% (rack head unit + expansion shelves, shelf
    cabling, network/power, access, mgmt network, backup connectivity, basic
    testing); Post-Deployment 34% (system access, monitoring tools, data
    security features, backup software config, policies); description names
    encryption, multi-tenancy, CIFS/NFS/DD Boost/VTL/NDMP. Recommended training
    incl. DD Management Center Administration (ESDPSD05255), Cloud Tier
    (MR-1WP-DDCTIM), Hardware Installation (MR-1WP-DDHINSTL). Current DDOS
    (Dell KB 000081247, modified 2026-11-04): latest feature release 8.9.0.0
    (2026-08-19); LTS2026 8.6.1.30 Recommended (window 2026-04-14..2028-04-30);
    LTS2025 8.3.1.50 and LTS2024 7.13.1.90 Legacy (to 2027-06-30); 7.13.1 not
    compatible with DD9910/DD9410/DD6410 and newer. Info Hub 000126375 (modified
    2026-08-20) lists docs for DD OS 8.0-8.9.
    Sources (primary, vendor):
    https://learning.dell.com/content/dell/en-us/home/certification-overview/certificationandbadges.html
    https://learning.dell.com/content/dam/dell-emc/documents/en-english/Dell_PowerProtect_Data_Domain_Operate_v2_Exam%20_Description.pdf
    https://learning.dell.com/content/dam/dell-emc/documents/en-us/Dell%20PowerProtect%20Data%20Domain%20Deploy%20v2%20Exam%20Description.pdf
    https://learning.dell.com/content/dell/en-us/home/certification-overview/certificationandbadges/powerprotect-data-domain-operate-2.html
    https://learning.dell.com/content/dell/en-us/home/certification-overview/certificationandbadges/powerprotect-data-domain-deploy.html
    https://learning.dell.com/content/dell/en-us/home/certification-overview/available-exams/powerprotect-dd-operate-.html
    https://learning.dell.com/content/dam/dell-emc/documents/en-us/Dell%20Technologies%20Proven%20Professional%20Exam%20Updates.pdf
    https://www.dell.com/support/kbdoc/en-us/000081247 (via WebFetch)
    https://www.dell.com/support/kbdoc/en-us/000126375 (via WebFetch)
    https://www.dell.com/support/kbdoc/en-us/000420246 (via WebFetch)
    Target bar: pass D-PDD-OE-01 (primary) and D-PDD-DY-01 on DDOS 8.6.1 LTS /
    8.9.
  - Gap vs blueprint (pages mentioning each term, out of 27): Zero coverage:
    Secure Multitenancy/tenant units 0, DDMC (Management Center) 0, ifgroup 0,
    collection replication 0, service tag 0, LTS 0, Cyber Recovery 0, Smart
    Scale 0, DD9910/DD9410/DD6410 0. Thin: Active Tier 2, data movement 1,
    NDMP 2, cabling 1, expansion shelves 4, Retention Lock 7 (compliance/
    governance mode 2 each), KMIP 2, fastcopy 1, DDVE 3, PowerProtect 5, 8.x
    versions ~1 real. Adequate: DD Boost 21, MTree 18, replication 21, NFS 16,
    CIFS 12, storage unit 10, Cloud Tier 9, encryption 10, Veeam 13, upgrade 13,
    cleaning 12, autosupport 6, SNMP 5, AIOps/CloudIQ 5, VTL 7. Phase B should:
    re-baseline all 27 "Applies to:" lines and the install-upgrade version
    matrix to DDOS 8.6.1 LTS2026 / 8.9 (cite KB 000081247); replace invented
    7.14/7.15 sample banners; add a Secure Multitenancy page (tenants, tenant
    units, roles); add DDMC page; add Cloud Tier data-movement policies + tuning
    and Active Tier vs Cloud Tier page; deepen Retention Lock (governance vs
    compliance on storage units/MTrees); add DY-01 hardware deployment page
    (pre-install checklist, service tags, rack/shelf cabling, initial config
    wizard, ifgroups/backup connectivity, NDMP); add replication types
    (collection/MTree/directory) page; map learning-path stages to OE-01/DY-01
    domains with weights; verify or remove DDVDP/SISL/RAIN/enter-maintenance-mode
    claims and update model lifecycle table against Dell docs.
  - site_audit (2026-11-25): 72/72 clean (full run, 72 checks incl. new 71/72; one run
    covered these 7 items). Queue file only.
- [x] storage/products/dell/dell-aiops
  - Audit (2026-11-25): 24 pages, 1,777 lines, 16 subdirs (alerts, architecture[5],
    cli-reference, deploy, design-standards, insights, integration, learning-path,
    lifecycle, operations[2], recommendations, reporting, scripts, security,
    troubleshooting[2], vendor-support). "Applies to:" 16 "Dell AIOps", 2 "Dell
    AIOps / CloudIQ AIOps", 2 stale "Dell EMC Storage" (release-notes.md:8,
    operations/faq.md:10), 4 none (cli-reference, reporting, scripts, troubleshooting
    index). Not in mkdocs nav (auto); linked from dell/index.md:29.
    Overlap with cloudiq (31 pages, 4,587 lines): same product. 21/24 pages here say
    "CloudIQ" and describe AIOps as a separate layer over CloudIQ (e.g. ports.md:22
    "analytics layer built on top of CloudIQ and ESRS telemetry") - wrong: per Dell it is one
    product, renamed. Unique to this section: alerts/insights/recommendations/
    reporting cards + design-standards SLA/tagging policy. cloudiq has the deeper
    ops/security/troubleshooting sub-pages. Recommend dell-aiops as canonical; fold
    cloudiq in and redirect.
    Hollow pages: many headings promised in the kb-summary are missing. recommendations
    (28 lines) has only an issues table. insights has no "Performance Predictions" or
    "Bottleneck Detection" section. lifecycle.md:59 "Check Current SCG Version" is
    empty. operations/index.md:37 "Critical or High Recommendation" is empty.
    troubleshooting/index.md has no issue content. Placeholder d2 "Component
    A/B/C" diagrams: cli-reference:137, reporting:37, scripts:42. deploy.md "Verify"
    (cluster/LUN/replication) is boilerplate that does not fit a SaaS product.
    Invented or wrong content:
    (a) Two conflicting API hosts. `api.cloudiq.dell.com` (cli-reference:23-134,
    scripts:10-11, integration:41) is wrong. `cloudiq.apis.dell.com/cloudiq/rest/v1`
    is the documented base, but the `/aiops/alerts|insights|reports` paths under it
    (alerts:28-35, insights:39, reporting:10-27, troubleshooting:13-19) are not
    verified.
    (b) The API is READ-ONLY per Dell. These POST endpoints and their JSON outputs
    are fabricated: acknowledge/dismiss (alerts:27-38, troubleshooting:18), report
    generation (reporting:9). /anomalies, /audit-logs and capacity
    "days_until_full" are unverified.
    (c) Wrong role names. security:56-60 has Admin/Viewer; learning-path:74 has
    Administrator/Operator/Observer. The real roles are Admin, Advisor, APM
    Admin/Viewer, Cybersecurity Admin/DevOps/Operator/Viewer, DevOps, Resource
    Operator, Standard.
    (d) Stale names: esrs.dell.com and "ESRS telemetry" (ports.md:22,28; SRS was
    removed from the whitepaper in H15691.10); "APEX AIOps"/apex.dell.com as the
    portal (deploy:53-81; the real portal is aiops.dell.com); "Dell EMC";
    "(Isilon)".
    (e) Not in the Dell source: "90 days of telemetry required" (deploy:66,100-105),
    "Settings → Analytics / Predictive Recommendations" (faq:31), anomaly
    "sensitivity Low/Med/High" (design-standards/index:84-91; Dell's only
    sensitivity setting is for ransomware incident detection), PagerDuty/Teams
    channels, "Aria Operations bidirectional" (integration:53), "SAML 2.0"
    (security), SCG UI :9443 (deploy:87, security:84; not checked), API secret
    "90-day" rotation (Dell: client credentials valid 1 year), "Release Notes"
    menu (lifecycle).
    (f) release-notes.md versions 1.0-2.4 are invented: AIOps is SaaS with no
    customer versions (template table, "Unverified").
    (g) deploy.md:65 lists 5 platforms and omits PowerEdge, VxRail, PowerProtect
    DD/DM, PowerVault, SC, XtremIO, Connectrix, PowerSwitch, VMware and APEX cloud.
    Right per Dell: SaaS, Secure Connect Gateway, 5-min alert/performance
    collection, ProSupport entitlement, aiops.dell.com.
  - Cert research (2026-11-25): No Dell Proven Professional exam covers AIOps or
    CloudIQ (reused from the cloudiq Phase A: 10 exam PDFs, 0 hits; not re-checked).
    Fallback bar is now obtained. "Dell AIOps: A Detailed Review" H15691.12, January
    2026, 226 pp, fetched via the Wayback copy dated 2026-07-27 (the live PDF
    returns 403).
    TOC: Executive summary; Overview (requirements/min code table, data collection
    and retention, features, Global Search, AIOps Assistant); Home page; Monitor;
    Manage; Optimize; Reports; Cybersecurity; Storage system / Block / File /
    Storage Group / PowerStore appliance / Node / Quota / Host details; Connectrix
    and PowerSwitch; HCI; Server; Data protection; VMware; Custom Tags;
    Administration (Identity Mgmt/roles/SSO groups, Settings, Customization,
    Integrations: REST API + Webhooks, Licenses); Mobile app; Appx A Enabling AIOps
    at the system; Appx B Security; Appx C Collection frequencies; Appx D Report
    Browser metrics; Appx E PowerEdge features by connection type.
    Key facts from the paper:
    - Health score is 100 minus the worst issue, across 5 categories: Components,
      Configuration, Capacity, Performance, Data Protection.
    - Data retention: 2 years. 5-min data is kept 100 days at system level and 22
      days at object level.
    - Connectivity: Secure Connect Gateway (replaces SRS and SupportAssist
      Enterprise) or Embedded Service Enabler; AIOps Collector vApp for
      VMware/Connectrix/PowerSwitch; OME + CloudIQ plugin or Dell Connectivity
      Client for PowerEdge.
    - REST API is read-only OAuth2: token valid 1 h, credentials 1 yr, DevOps role.
    - Webhooks: 5 event types (Health Issue Change plus 4 cybersecurity types).
    - AIOps Assistant (GenAI, "Powers"). Carbon/energy metrics.
    Lab: Demo Center HOL-0511-01 "APEX AIOps Infrastructure Observability (formerly
    CloudIQ)" (archived 2024-12-04, login needed to launch). Modules: Overview,
    Health, Capacity, Performance Impacts and Anomalies, PowerEdge, VxRail, VMware,
    Cybersecurity, Custom Labels and Reports, Energy/Carbon. ITD-0511 not verified.
    Sources (primary, vendor):
    web.archive.org/web/20260727122522id_/https://www.delltechnologies.com/asset/
    en-us/products/storage/industry-market/dell-aiops-a-detailed-review.pdf ;
    dell.com/community/Developer-Blogs/Start-Guide-to-CloudIQ-REST-API-Using-Postman/
    ba-p/8375121 (Dell dev blog, 2023: base URL, token URL, scope oapi) ;
    web.archive.org/web/20241204191217id_/https://democenter.dell.com/hol/HOLA/
    HOL-0511-01
    Target bar: Operate Dell AIOps end to end at the depth of the Detailed Review
    H15691.12 TOC, plus the HOL-0511 module list and the read-only REST API/webhooks.
  - Gap vs blueprint (pages mentioning each term, out of 24): Zero coverage:
    Cybersecurity/misconfiguration/ransomware (0), AIOps Assistant/GenAI (0),
    Collector (0), carbon/energy (0), mobile app (0), Ansible/Terraform (0), VxRail/
    HCI (0), Dell Security Advisories, Custom Tags (real feature), Report Browser,
    Reclaimable Storage, Workload Contention, SSO groups/Dell Identity/MyService360,
    Trusted Advisor/partner access, Licenses, data retention, PowerEdge firmware
    update jobs. Thin: SCG 12 (mostly wrong model), health score 7 (no 5-category
    model), webhook 4 (no event types or HMAC secret), REST API 9 (wrong host, fake
    writes), OAuth 3, ProSupport 1, PowerFlex 1, PowerSwitch/Connectrix 1, PowerProtect
    2, VMware 4, SupportAssist 3, roles 6 (wrong names).
    Phase B should:
    1. Merge cloudiq into dell-aiops and redirect cloudiq. Fix the "layer on top of
       CloudIQ" model to "CloudIQ → APEX AIOps Infrastructure Observability (Aug
       2024) → Dell AIOps (Oct 2025)".
    2. Delete the POST/write API examples and the api.cloudiq.dell.com host; rebuild
       from developer.dell.com/apis/products/analytics/cloudiq.
    3. Replace the roles, ports (drop esrs) and supported-platform tables with the
       whitepaper tables (min code versions).
    4. Add pages: Cybersecurity (evaluation plans, risk score, ransomware incidents
       for PowerMax/PowerProtect DD), AIOps Assistant, Collector/connectivity per
       product (Appx A), Custom Tags & Reports, Energy/Carbon, Mobile, Administration
       (SSO groups, Advisor access), webhooks with signature verification.
    5. Delete or replace the invented release-notes table, the 90-day and
       sensitivity claims, and the placeholder diagrams. Fill the hollow sections.
  - site_audit (2026-11-25): 72/72 clean (full run, 72 checks incl. new 71/72; one run
    covered these 7 items). Queue file only.
- [x] storage/products/dell/ecs
  - Audit (2026-11-25): 26 pages, 6,899 lines; subdirs architecture/ operations/
    security/ troubleshooting/ learning-path/ + index.md, release-notes.md.
    "Applies to:" 23x "ECS 3.x", 2x "Dell EMC Storage", 1x "Dell ECS 3.x". Version
    mentions: ECS 3.8 (6), 3.9 (4), 3.7/3.6 (2 each), 3.5/3.4 (1 each). ZERO pages
    mention ObjectScale. KB presents ECS as the current product line - STALE: Dell
    rebranded ECS to ObjectScale at 4.0 (Apr 2025); latest is ObjectScale 4.4 (Aug 2026).
    Errors:
    - operations/install-upgrade.md:32 "ECS 3.9.x | 2024 | CloudIQ ... | Active
      (Current)" - no ECS 3.9 exists; Dell release-contents goes 3.8.1 (Apr 2024) ->
      ObjectScale 4.0 (Apr 2025). Same invented 3.9 at architecture/integrations.md:384,
      :386 and architecture/design-standards.md:137 (also "CloudIQ" is now Dell AIOps).
    - operations/install-upgrade.md:29-31 dates wrong: 3.6 = Nov 2020, 3.8 = Dec 2022
      (KB says 2021 / 2023); 3.8.x status "Active" omits the 4.x successor.
    - operations/faq.md:20 "ECS 3.8.x is the current recommendation" - stale (4.x is
      current; 3.8.x is the required upgrade source for 4.0). faq.md:20,23 `ecs version`
      CLI command - not verified, likely invented.
    - release-notes.md:25-29 dates all wrong vs Dell (3.8 "2024-Q2" vs Dec 2022; 3.7
      "2023-Q3" vs Feb 2022; 3.6 "2022-Q4" vs Nov 2020; 3.5 "2022-Q1" vs May 2020; 3.4
      "2021-Q2" vs Sep 2019); feature attributions unverified (table self-flagged).
    - ecscli command syntax (12 pages, e.g. "ecscli namespace list") not verified
      against Dell ECS CLI docs.
  - Cert research (2026-11-25): Dell Proven Professional catalog still lists three
    ECS exams; NO ObjectScale-named exam in the catalog. All three are 2023-vintage
    and were not refreshed for ObjectScale 4.x; no retirement notice found.
    - D-ECS-OE-23 "Dell ECS Operate 2023" (object storage administrator daily ops).
      Products: ECS 3.8, Amazon S3, DD Cloud Tier 6.2, OpenStack, PowerScale
      CloudPools 9.x, NetWorker CloudBoost 9.1. Domains: ECS Overview 22%; ECS
      Administration 39%; ECS Data Client Access 30%; ECS Integrated Solutions 9%.
      90 min. Requirements as of 2023-12-08. Languages English, French.
    - D-ECS-DY-23 "Dell ECS Deploy 2023": Overview 16%; Implementation 36% (site prep,
      core OS install, network separation, software install, initial config, install
      troubleshooting); Administration 22%; Data Client Access 18%; Integrated
      Solutions 8%. ECS 3.8. 90 min. As of 2023-12-08. Replaced DES-1B21 (retired
      2024-01-04). Listed in a separate (possibly partner-gated) catalog block.
    - D-ECS-DS-23 "Dell ECS Design 2023": Platform Architecture, Networking, Data
      Management, Cluster Access, Monitoring & Performance - 20% each. ECS 3.7.
      90 min. As of 2023-02-06.
    Question count / pass score: not stated in PDFs or exam pages - not verified.
    Sources (primary, vendor):
      https://learning.dell.com/content/dell/en-us/home/certification-overview/certificationandbadges.html
      https://learning.dell.com/content/dam/dell-emc/documents/en-us/D-ECS-OE-23-Operate_ECS_Exam.pdf
      https://learning.dell.com/content/dam/dell-emc/documents/en-us/D-ECS-DY-23-Deploy_ECS_Exam.pdf
      https://learning.dell.com/content/dam/dell-emc/documents/en-us/D-ECS-DS-23-Design_ECS_Exam.pdf
      https://learning.dell.com/content/dell/en-us/home/certification-overview/available-exams/ecs-operate.html
      https://learning.dell.com/content/dell/en-us/home/certification-overview/available-exams/ecs-deploy.html
      https://learning.dell.com/content/dell/en-us/home/certification-overview/available-exams/ecs-design.html
      https://learning.dell.com/content/dam/dell-emc/documents/en-us/Dell%20Technologies%20Proven%20Professional%20Exam%20Updates.pdf
      https://www.dell.com/support/kbdoc/en-us/000296965/ecs-rebranding-to-objectscale
      https://www.dell.com/en-us/infohub/articles/dell-objectscale-release-contents
    Target bar: pass D-ECS-OE-23 (primary) + D-ECS-DY-23 Implementation delta, with
    ECS 3.8 exam content kept as-is but the section reframed as ObjectScale 4.x (ECS).
  - Gap vs blueprint (pages mentioning each term, out of 26): Zero coverage:
    ObjectScale/rebrand 0, ARM/access-during-outage 0, GeoDrive 0, DD Cloud Tier 0,
    PowerScale/Isilon CloudPools 0, NetWorker CloudBoost 0, network separation 0,
    node/hardware models (EX300/EX500/EX3000/EX5000/EXF900/XF960) 0, TSO/PSO 0,
    Service Console 0, XOR 0, Dell cert codes 0. Thin: storage pool 3, metering 1,
    D@RE 2, NFS 4, HDFS 4, sizing 3, multi-tenancy 4, ACL 5, load balancer 6, AD/LDAP 7.
    Covered: S3 23, bucket 21, namespace 20, replication group 15, geo/federation 16,
    VDC 15, quota 15, monitoring 15, IAM 14, compliance 14, retention 13, ecscli 12,
    Swift 10, erasure coding 9, object lock 9, CAS 9.
    Phase B should: (1) reframe section as "Dell ObjectScale (formerly ECS)", add
    4.0-4.4 lineage + 3.8.x-only upgrade path (Gen2/Gen3) from KB 000296965; delete
    invented ECS 3.9 rows/sections and fix install-upgrade/faq/release-notes dates;
    (2) write integrated-solutions page (DD Cloud Tier, CloudPools, CloudBoost) - 8-9%
    of OE/DY; (3) add ARM/ADO, TSO/PSO, XOR, storage-pool/VDC/RG data-protection
    deep-dive for Administration 39%; (4) GeoDrive + ecscli + REST API + Swift client
    access verified against Dell docs; (5) Implementation page: site prep, core OS,
    network separation, initial config; (6) design/sizing: node types, LB methods,
    multi-tenancy; (7) a cert-prep page mapping D-ECS-OE/DY/DS-23 objectives to pages.
  - site_audit (2026-11-25): 72/72 clean (full run, 72 checks incl. new 71/72; one run
    covered these 7 items). Queue file only.
- [x] storage/products/dell/fod
  - Audit (2026-11-25): 26 pages, 3,742 lines. Subdirs: architecture/ (5),
    operations/ (8), security/ (5), troubleshooting/ (5), learning-path/ (1),
    plus index.md and release-notes.md. "Applies to:" tags: 20 "Dell FOD",
    2 "Dell EMC Storage", 2 "Dell FOD for PowerStore, PowerMax, Unity",
    1 "Dell Flex on Demand (FoD) / APEX Flex on Demand", 1 "Dell Flex on
    Demand / APEX Flex on Demand". No explicit mkdocs.yml nav entry, so the
    nav is auto-generated.
    IDENTITY SPLIT: the section mixes two different things. One is Flex on
    Demand, the financial consumption program. The other is an invented
    "Features on Demand" licence-key scheme. Pages built on licence keys:
    operations/faq.md (title "Dell Features on Demand"; 90-day trial key,
    :39), architecture/ports.md (license key pull from licensing.dell.com,
    :24), troubleshooting/known-issues.md, learning-path/index.md (all of
    :31-85; trial "typically 30 days", :34, contradicts faq's 90),
    troubleshooting/escalation.md (symlicense install/list/preview .lic,
    :134-377), health-checks.md:26-29, procedures.md:83-170 (symcfg -auth
    activate, symcfg list -fod, with fabricated feature/expiry output
    :121-135), install-upgrade.md:35-74 (symlmf import; fabricated "PowerMax
    FOD Base/Burst Capacity" licence lines; capture says "not verified").
    The metering half also contradicts Dell sources:
    (a) "peak-hour metering, maximum capacity used in any hour" appears at
    how-it-works.md:46, architecture/index.md:46 and cli-reference.md:405.
    Dell says consumed capacity "is measured multiple times per day and the
    daily average is used to calculate the monthly average", and "billed by
    average or actual usage". WRONG.
    (b) The "base/burst ceiling ... over-usage charges or immediate license
    upgrade" model appears at how-it-works.md:44, architecture/index.md:40-44,
    cli-reference.md:277 and procedures.md:50-58. Dell's terms are Committed
    Capacity plus Buffer Capacity, with the 85% billing cap: no charge for
    use above 85% of installed capacity. INVENTED.
    (c) Product scope is given as "PowerMax, PowerStore, PowerScale"
    (index.md, how-it-works.md:50-56), and cli-reference.md:18 says
    "PowerMax/VMAX arrays". Dell lists Storage, Data Protection, and
    HCI/VxRail (plus CI, PowerFlex, and servers per the 2021 blog and 2024
    page). The scope is too narrow, and "Unity" (9 pages) is not verified.
    (d) The CloudIQ/SCG telemetry billing pipeline (how-it-works.md:20,
    integrations.md, encryption.md:33-38) is not verified; Dell says only
    "automated tools installed with your equipment" and APEX console usage
    data. Also unverified: the CloudIQ REST base URL in scripts.md:46,196,320
    and the Unisphere "license_capability: FOD" field in cli-reference.md:186.
    (e) release-notes.md "FOD 2.4-3.2" (:25-29) is FABRICATED, because FoD
    is a payment program with no software versions; delete the table.
    (f) Missing entirely: the 85% cap, commitment thresholds, term lengths,
    dark-site/non-metered ineligibility, revised committed capacity, DFS as
    provider, and the APEX Infrastructure rebrand.
    cod MERGE: fod should be the canonical home. Its correct content is a
    thin layer, but the cod key-activation material duplicates fod's
    invented licence-key half. Merge cod's capacity-activation concept here
    only after rewriting it against the Dell terms, then redirect cod.
    Cross-link apex-storage-as-a-service as the subscription sibling.
  - Cert research (2026-11-25): No Dell Proven Professional exam covers Flex
    on Demand, APEX Infrastructure pay-per-use or consumption programs. I
    reused the sibling-verified catalog (~82 codes; the only APEX exams are
    APEX Cloud Platform for Azure/OpenShift) and did not re-fetch it. FoD is
    a DFS financial program, so no technical exam is expected. Fallback bar:
    the Dell program terms below, verified from Dell-owned pages and DFS
    PDFs.
    Sources (primary, vendor):
    https://web.archive.org/web/20261104004947id_/https://www.dell.com/en-us/shop/apex/subscriptions/sl/apex-infrastructure
    https://web.archive.org/web/20240416081929id_/https://www.dell.com/en-ie/dt/payment-solutions/flexible-consumption/flex-on-demand.htm
    https://web.archive.org/web/20250514142305id_/https://www.dell.com/en-us/blog/cost-assurance-for-unpredictable-it-challenges/
    https://www.delltechnologies.com/content/dam/uwaem/production-design-assets/en/services/Payment-Solutions/19-DFM-0172-DFS-FOD-Flyer-v4.pdf
    https://i.dell.com/sites/csdocuments/Learn_Docs/en/uk/dfs-emea-flex-on-demand-english.pdf
    Target bar: be able to explain and size an APEX Flex on Demand / APEX
    Infrastructure pay-per-use deal end to end. That covers Committed vs
    Buffer Capacity; commit thresholds (storage 40-80%, PowerEdge 70-80%,
    HCI 50-80%); terms (storage 12-60 months, server 36-60 months); the
    metering math (several samples a day, daily average, monthly average);
    the 85% cap (excludes servers; dark-site and non-metered deployments not
    eligible); revised committed capacity; end-of-term options; APEX console
    pre-invoice approval; and product eligibility.
  - Gap vs blueprint (pages mentioning each term, out of 26): Zero coverage:
    "buffer capacity" 0, "buffer" 0, "billing cap" 0, "pay-per-use" 0,
    "APEX Infrastructure" 0, "Dell Financial Services/DFS" 0, "dark site" 0,
    "multiple times per day/daily average" 0, "revised committed" 0,
    VxRail 0. Thin: "committed capacity" 1 (a script sample output line),
    "85%" 1 (an unrelated script warning threshold), Data Protection 1
    (off-topic), PowerFlex 1, "APEX Flex on Demand" 3. Over-weighted or
    wrong: burst 11, licence/activation key 12, symcfg/symlicense/symlmf 8,
    "features on demand" 4, peak 4 (3 of them the false peak-hour claim),
    CloudIQ 14 and SCG 14 (as an unverified billing path). Phase B should:
    (1) delete the Features-on-Demand licence-key material (faq, ports,
    known-issues, learning-path, escalation, procedures:83-170,
    install-upgrade:35-74, health-checks:26-29) and the fabricated
    release-notes table;
    (2) rewrite how-it-works and architecture/index around Committed/Buffer,
    the daily-average metering and the 85% cap, with Dell citations;
    (3) widen product scope to the Dell list;
    (4) replace burst-ceiling procedures and scripts with array-side
    capacity monitoring framed as "estimate buffer usage", clearly labelled
    as not the billing meter;
    (5) add an APEX console usage/pre-invoice review procedure (verify the
    console docs first);
    (6) absorb the rewritten cod content and redirect cod;
    (7) cross-link apex-storage-as-a-service.
  - site_audit (2026-11-25): 72/72 clean (full run, 72 checks incl. new 71/72; one run
    covered these 7 items). Queue file only.
- [x] storage/products/dell/powermax
  - Audit (2026-11-25): 27 pages / 9,335 lines; subdirs architecture(5) deploy(1)
    learning-path(1) operations(8) security(5) troubleshooting(5) + index + release-notes.
    srdf-a/ and srdf-s/ are sibling dirs (storage/products/dell/srdf-a, /srdf-s), separate
    queue items, not under powermax/. "Applies to:" on 26/27 pages: 21x "PowerMax 2500 /
    8500", 2x "Dell PowerMax · VMAX", 2x 2500/8500 + PowerMaxOS 10.x, 1x "PowerMax
    2000/8000, Unisphere 10.x, SE 10.x" (known-issues.md:14, mixes gen-1 HW with 10.x SW).
    Version mentions are thin and partly wrong; no page names 10.2-10.5 or SE 10.x
    pairing; no learning-path/cert/exam-code content at all.
    Invented / wrong content (file:line):
    - release-notes.md:24-28 table invented (tool-generated, flagged unverified): "10.0
      2023-Q3 350F all-NVMe platform" and "10.1 2024-Q3" contradict Dell Info Hub (10.0
      Jul 2022, 10.1 Oct 2023); 9.x rows are not PowerMaxOS versions. Replace with Info
      Hub list 10.0 -> 10.5.
    - operations/faq.md:20 "PowerMaxOS 10.1.x (5978.x)" wrong: exam PDFs list PowerMaxOS
      10 and PowerMaxOS 5978 as distinct releases; also stale (current is 10.5).
    - operations/install-upgrade.md:101-107 EOL table (VMAX 950F, 5977, 5978, SE 9.1 dates)
      unsourced, treat as invented.
    - operations/backup-restore.md:298-300,314,615 `symsnapvx ... set_expiry -hours` does
      not exist; Dell KB 000211289 syntax is `set ttl -delta <t>|-absolute <dt>`. Same
      block suggests legacy `symsnap` as SnapVX fallback.
    - `symsnap list` used as a SnapVX command: troubleshooting/diagnostics.md:71,
      operations/procedures.md:847,850, operations/health-checks.md:51,68,
      troubleshooting/common-issues.md:95 (SnapVX CLI is symsnapvx).
    - known-issues.md:66 `symapid stop; symapid start` and security/encryption.md:327,336
      "symapid" daemon: SE daemons are storapid/storsrvd via `stordaemon` (secondary
      source only, confirm vs SE 10 Install Guide).
    - Suspected invented commands, not verified (SE 10 CLI ref is login-gated):
      `symdf` (escalation.md:68,204,236,364,429; diagnostics.md:68), `symport`
      (cli-reference.md:384-390,452), `symcapacity` (deploy/index.md:399;
      procedures.md:471), `sympools` (procedures.md:666), `symsloprovisioning`
      (procedures.md:743), `symcfg_daemon` (procedures.md:348).
    - architecture/integrations.md:193 sample output "PowerMax OS 9.1" and
      escalation.md:98,100 "SE V9.2.1.0" on a 10.x-scoped page: stale/invented samples.
  - Cert research (2026-11-25): Dell catalog lists 4 PowerMax exams: Operate
    (D-PVM-OE-01), Design (D-PVM-DS-01), Install (D-PM-IN-23), Maintenance (D-PM-MN-23).
    Target = D-PVM-OE-01 Dell PowerMax Operate v2 (KB is admin/ops-focused). PDF
    re-downloaded and read: Part 1 75 min ~40 Q, Part 2 45 min ~8 Q; practice test
    D-PVM-OE-P-01; requirements as of 2024-09-18. Domains: Storage Provisioning 24%
    (models/arch, configs, port mgmt, device mgmt, SL-based provisioning, auto-
    provisioning groups); Business Continuity Admin 20% (SnapVX + TimeFinder Clone ops in
    Unisphere, SRDF ops in Unisphere + SYMCLI); PowerMaxOS 10 Data Mobility 12% (NDM via
    Unisphere, O-MDM via SYMCLI + Unisphere); Monitoring & Workload Planning 10%;
    Local/Remote Replication Concepts 10% (SnapVX snaps vs clones, SRDF topologies);
    Solutions Enabler 10 Implementation 10% (concepts, install/upgrade, gatekeepers,
    daemons); Unisphere for PowerMax 10 8% (install, post-install, navigation, admin);
    Virtual Env 4% (vSphere + VSI, VM monitoring). Products: PowerMaxOS 5978, SE 10,
    Unisphere 10, SnapVX, SRDF, Open Replicator, NDM/O-MDM (2 further bullets clipped in
    PDF text). Secondary: D-PVM-DS-01 Design v2 (as of 2025-04-18): Features 15%, Design
    Resources 15% (PowerSizer, My Work), Upgrades & Migrations 17%, Local/Remote
    Replication 19%, Unisphere 12% (WLP, Data Exclusion, Headroom), SE 7%, PowerMax File
    15% (eNAS + SDNAS); Dell internal/partner audience. Install/Maintenance PDFs not read.
    Current software (Dell Info Hub KB 000189115, modified 2026-11-18): PowerMaxOS
    10.5.0.0 / SE 10.5.0 / Unisphere 10.5.0.0 all Nov 2026; 10.4 Apr 2026; 10.3 Oct 2025;
    10.2 Oct 2024; 10.1 Oct 2023; 10.0 Jul 2022. KB 000297022: SE version must match
    PowerMaxOS version (10.2->10.2, 10.3->10.3). Models: 2500/8500 current, 2000/8000 older.
    Note exam blueprint (2024) predates 10.3-10.5; KB should teach blueprint + flag newer.
    Sources (primary, vendor):
    https://learning.dell.com/content/dell/en-us/home/certification-overview/certificationandbadges.html
    https://learning.dell.com/content/dam/dell-emc/documents/en-us/D-PVM-OE-01-PowerMax_Operate_Exam_Description.pdf
    https://learning.dell.com/content/dam/dell-emc/documents/en-us/ExamDescriptionDellPowerMaxDesignv2ExamD-PVM-DS-01.pdf
    https://www.dell.com/support/kbdoc/en-us/000189115/powermax-info-hub-product-documentation-videos
    https://www.dell.com/support/kbdoc/en-hk/000297022/solutions
    https://www.dell.com/support/kbdoc/000211289/solutions-enabler-unisphere-for-powermax
    Target bar: pass D-PVM-OE-01 (incl. 45-min lab part) on PowerMaxOS 10 / SE 10 /
    Unisphere 10, with the KB current to 10.5.
  - Gap vs blueprint (pages mentioning each term, out of 27): Zero coverage: NDM/Data
    Mobility 0, O-MDM 0, Open Replicator 0, TimeFinder Clone 0, auto-provisioning groups
    (term) 0, VSI 0, "workload planning" 0, Data Exclusion 0, SnapVX TTL/set ttl 0, secure
    snaps 0, snapshot policies 0, SRDF/Metro witness 0, zDP 0, SDNAS/PowerMax File 0,
    PowerSizer 0, exam codes 0. Thin: host I/O limits 1, gatekeeper 1, eNAS 1, VVols 3,
    VASA 2, linked targets 3, cascaded/Star 4, stordaemon/storsrvd 5, data reduction 5,
    eLicensing/license 5, symaccess 6, service level 6, symconfigure 5, NVMe-oF 7,
    SRDF/Metro 8, AIOps/CloudIQ 9. OK: Unisphere 22, masking view 18, storage group 17,
    SRDF group/symrdf 17, symcfg 16, SRDF/S 15, SRDF/A 14, SnapVX 14, SRP 11, REST 11.
    Phase B should: (1) fix every invented item above (set_expiry, symsnap, symapid,
    suspected sym* commands, release-notes table, faq 5978 mapping, EOL table); (2) add a
    Data Mobility page (NDM + O-MDM via Unisphere and SYMCLI, Open Replicator); (3) add
    SnapVX deep-dive (snap vs clone, link modes, TTL, secure snaps, snapshot policies,
    TimeFinder Clone) and SRDF ops lab (modes, Metro + witness, topologies) cross-linked
    to srdf-a/srdf-s items; (4) SE 10 install/upgrade, gatekeepers, daemons
    (storapid/storsrvd/stordaemon), SE-PowerMaxOS version match; (5) Unisphere 10
    install/post-install/admin + Monitoring/Workload Planning/headroom; (6) provisioning
    page on auto-provisioning groups, service levels, host I/O limits, port/device mgmt;
    (7) vSphere/VSI/VVols page; (8) learning-path mapped to D-PVM-OE-01 domains with %s
    and a version note (blueprint 5978/10 vs current 10.5); (9) release-notes from Info Hub.
  - site_audit (2026-11-25): 72/72 clean (full run, 72 checks incl. new 71/72; one run
    covered these 7 items). Queue file only.
- [x] storage/products/dell/powerpath
  - Audit (2026-11-25): 27 pages, 7,839 lines, 5 subdirs (architecture, learning-path,
    operations, security, troubleshooting) + index.md + release-notes.md. "Applies to:"
    22 "PowerPath" (no version), 2 "Dell PowerPath 7.x", 1 each "PP/VE, Linux/Windows
    6.x", "Linux/Windows; PP/VE for ESXi", "Linux/Windows/VMware 6.x". Version mentions
    are all 6.0-6.4 (6.1 x12, 6.2 x14, 6.4 x6); zero pages mention 7.x content or 8.x,
    although Dell's current lines are 8.x (Linux 8.2.1 P01, Windows 8.0 SP2, PP/VE
    8.2 SP1 P01) and PPMA 4.0 SP1. Errors found:
    - learning-path/index.md:36,57,60,67,70-73,84 call PPME "PowerPath Management
      Server"; PPME is PowerPath Migration Enabler (Dell manuals/KB 000054845,
      000059511); the management product is PPMA.
    - troubleshooting/known-issues.md:58 `powermt check_registration -f <license-file>`;
      Dell documents license install via `emcpreg -install` (KB 000021272); emcpreg is
      on 0 pages.
    - troubleshooting/common-issues.md:427, operations/common-issues.md:361,
      operations/cli-reference.md:78,560,741 use `class=symmetrix`; the 8.x CLI ref
      lists class=symm|powermax|unity|powerstore|... (no "symmetrix"). Also sets
      CLAROpt on the Symmetrix class.
    - security/authentication.md:60-63 sample output uses `hsv210..213` device names
      (HP EVA style), not emcpower pseudo devices; fabricated output.
    - release-notes.md:27 "6.2 | 2022-Q4 | NVMe-oF multipath GA": the Linux 6.2 guide
      is dated April 2017; the table is template-generated and wrong.
    - architecture/ports.md: PPMA ports 8443/9988 unsourced; PPMA 4.0 guide has a
      "Port reservation" section that was not readable (not verified either way);
      rpowermt/PP-VE CIM path not covered.
  - Cert research (2026-11-25): No Dell certification centres on PowerPath. The Dell
    catalog (49 exam codes parsed) has no PowerPath exam, and "PowerPath" and
    "multipath" score 0 hits in the 4 storage exam PDFs (PowerMax Operate D-PVM-OE-01,
    Install PowerMax D-PM-IN-23, Operate PowerStore D-PST-OE-23, Design Midrange
    D-MSS-DS-23). Fallback expert bar = Dell's own 8.x documentation set: PowerPath
    Family 8.x Product Guide (rev 4.0, Feb 2024, PP 8.2), PowerPath for Linux 7.5
    Installation & Administration Guide (rev 2.0, Mar 2023), PowerPath Family 8.x
    CLI & System Messages Reference, PPMA 4.0 Install & Config Guide (rev 6.0, Apr
    2026). Current versions on Dell support filters: Linux 8.2.1 P01, Windows 8.0 SP2,
    PP/VE 8.2 SP1 P01, PPMA 4.0 SP1. EOL dates not verified: kbdoc 000185734 lists
    PowerPath only as an affected product, with dates in .xlsx attachments that were
    not read.
    Sources (primary, vendor):
    https://learning.dell.com/content/dell/en-us/home/certification-overview/certificationandbadges.html
    https://learning.dell.com/content/dam/dell-emc/documents/en-us/D-PVM-OE-01-PowerMax_Operate_Exam_Description.pdf
    https://learning.dell.com/content/dam/dell-emc/documents/en-us/D-PM-IN-23-Install_PowerMax_Exam.pdf
    https://learning.dell.com/content/dam/dell-emc/documents/en-us/D-PST-OE-23-Operate_PowerStore_Exam.pdf
    https://learning.dell.com/content/dam/dell-emc/documents/en-english/D-MSS-DS-23-Design_Midrange_Exam.pdf
    https://www.dell.com/support/manuals/en-us/powerpathve-for-vmware/pp_product_guide_8x
    https://www.dell.com/support/manuals/en-us/powerpath-for-linux/pp_pub_core_linux_7x_install_guide/PREFACE?guid=guid-a24035ac-a151-4dd4-8250-7c36954bd28e&lang=en-us
    https://www.dell.com/support/manuals/en-us/powerpath-for-linux/pp_pub_8x_cli_reference/Revision-history?guid=guid-fb2a030c-cd3d-4261-8091-0d451a438dba&lang=en-us
    https://www.dell.com/support/manuals/en-us/powerpath-for-linux/pp_pub_8x_cli_reference/powermt-set-policy?guid=guid-01ab7582-d61c-43d7-a438-a7e16072e1c2&lang=en-us
    https://www.dell.com/support/manuals/en-us/powerpath-management-appliance/pp_ppma_4.0_iag/Revision-history?guid=guid-b3a6c32b-8d6a-4523-bf89-b517420e98df&lang=en-us
    https://www.dell.com/support/product-details/en-us/product/powerpath-for-linux/resources/manuals
    https://www.dell.com/support/product-details/en-us/product/powerpath-for-windows/resources/manuals
    https://www.dell.com/support/product-details/en-us/product/powerpathve-for-vmware/resources/manuals
    https://www.dell.com/support/product-details/en-us/product/powerpath-management-appliance/resources/manuals
    https://www.dell.com/support/product-details/en-us/product/powerpath/resources/articles
    https://www.dell.com/support/kbdoc/en-us/000185734/all-dell-emc-end-of-life-documents?lang=en
    https://www.dell.com/support/kbdoc/en-us/000064623/emc244795-powerpath-ve-served-licensing-cheat-sheet?lang=en
    Target bar: Can install, upgrade (incl. NDU and BFS), license, tune and troubleshoot
    PowerPath 8.x on Linux, Windows and ESXi and manage it via PPMA 4.0 and rpowermt,
    to the depth of the 8.x Product Guide, Linux Install/Admin Guide and CLI Reference.
  - Gap vs blueprint (pages mentioning each term, out of 27): Zero coverage: PowerPath
    8.x (0), rpowermt (0), emcpreg (0), autostandby (0), streamio/si policy (0), boot
    from SAN (0), NDU (0), CLP licensing (0), FPIN (0), SAN latency/path_latency (0),
    LVM filters (0), powermap/pseudo rename (0), PP/VE esxcli/VIB install (0), PPMA
    3.x/4.0 (0), CIM/5989 (0). Thin: PP/VE (6), PPMA (2), NVMe (2), served licensing (4),
    SymmOpt/CLAROpt named (2), least-I/O/blocks (2), host registration (1), flaky path
    (1), Migration Enabler/powermig (1), UEFI Secure Boot/MOK (1), vSphere lifecycle
    (1), MPIO (4). Adequate by count: powermt (20), path states alive/dead (18), powermt
    save/config (18), license wording (18), restore (14), emcpower/pseudo (14), ALUA (9),
    dm-multipath coexistence (9), iSCSI (9), upgrade (15). Phase B should: re-baseline
    all "Applies to:" and samples to 8.x (Linux 8.2.x, Windows 8.0 SPx, PP/VE 8.2 SP1,
    PPMA 4.0); fix the 5 flagged errors; add pages for the 8.x policy set (ad|co|lb|li|
    re|rr|si|so + addon_policy=ca, proto=scsi|nvme), path states incl. autostandby
    (asb:prox, asb:iopf) and proactive port-offline autostandby, emcpreg + CLP/served
    licensing, rpowermt + PP/VE install/NDU via PPMA, Linux BFS (emcpbfs_linux), kernel
    and OS upgrades, NDU, NVMe/TCP + ANA, LVM filters, Secure Boot MOK signing, PowerMax
    features (host registration, flaky path, SAN latency, FPIN), PPMA 4.0 deployment
    (OVA/TBZ-Docker/VHD), certificates and monitoring, and Migration Enabler.
  - site_audit (2026-11-25): 72/72 clean (full run, 72 checks incl. new 71/72; one run
    covered these 7 items). Queue file only.
- [x] storage/products/dell/powerscale
  - Audit (2026-11-25): 27 pages / 11,496 lines; subdirs architecture(5),
    deploy(1), learning-path(1), operations(8), security(5), troubleshooting(5)
    + index.md, release-notes.md. Heavy pages: operations/cli-reference.md
    (2,603), scripts.md (1,265), procedures.md (978), security/authentication.md
    (916). "Applies to:" tally: 26/27 say OneFS/PowerScale "9.x" (6 phrasings,
    20x "PowerScale (Isilon) 9.x"). OneFS version mentions: 9.4.0.0 (8, all in
    sample output), 9.7 (4), 9.4 (3), 9.5 (2), 9.3 (2), 9.6/8.0/8.1/8.2 (1
    each); nothing newer than 9.8. Node models named: F200/F600/F900, H500/H600/
    H700/H7000, A300/A3000 only. Staleness/errors:
    operations/faq.md:20 "OneFS 9.7.x is the current recommendation" (Dell's
    OneFS Info Hubs index now lists 9.16.0.0 as newest); install-upgrade.md:
    28-34 + 69-73 version matrix tops out at "9.7.x/9.8.x Current GA";
    faq.md:20 "Isilon Management Interface (IMI)" is not a OneFS UI name found
    in any source fetched (suspect; OneFS docs say Web Administration);
    operations/cli-reference.md:103,284,322 "PowerScale H500" (Dell hardware
    hub lists it as "Isilon H500"); release-notes.md:25-29 template-invented
    features (e.g. "9.4 - DataAdvantage analytics", "9.7 - SmartFlash NVMe
    tier GA"), all marked "Not yet verified"; architecture/integrations.md:
    5,10,23,47-51 + ports.md:38 + design-standards.md:55,70 + procedures.md:
    102 + health-checks.md:85 still say "CloudIQ" (now Dell AIOps);
    integrations.md:49 conflates `isi cloud accounts create` (CloudPools) with
    AIOps telemetry; security/hardening.md:116 sample error text "Supported
    versions: 1.0, 1.1, 1.3" looks invented. Zero mention of PowerScale for
    Public Cloud / APEX File Storage (AWS/Azure) or of 2024+ nodes (F210/F710/
    F910/PA110/H710/H7100/A310/A3100).
  - Cert research (2026-11-25): Dell catalog now lists exactly three
    PowerScale exams, all re-coded "-01": D-PSC-DY-01 PowerScale Deploy,
    D-PSC-DS-01 PowerScale Design, D-PSC-MN-01 PowerScale Maintenance. No
    PowerScale Operate/Administrator exam exists (other products have Operate
    exams; PowerScale does not). Target = D-PSC-DY-01: its page says it
    validates the ability to "deploy, configure, monitor, and maintain"
    PowerScale; audience includes Storage Administrators; scope named:
    cluster creation, OneFS upgrades, access zones, SmartConnect, SMB/NFS,
    auth providers, SnapshotIQ, SyncIQ, SmartLock, quotas, dedupe, InsightIQ,
    HealthCheck, job engine, CAVA/ICAP antivirus. Domains+weights (DY-01):
    Install Nodes and Create Cluster 14% (front/back-end cabling, create
    cluster, remove/reformat/reimage node); Configure Cluster and Nodes Post
    Installation 62% (cluster config, OneFS upgrades/updates, SmartConnect
    multi-subnet, protocol settings, software modules, auth providers + access
    zones); Monitor and Troubleshoot 12% (performance, install InsightIQ,
    HealthCheck + event/alert notifications, basic troubleshooting, job engine
    best practices); Enable Data Protection 12% (data protection, CAVA/ICAP).
    Languages English/French; delivered by Pearson VUE (centre or OnVUE).
    Format (question count, duration, pass score) and a "requirements as of"
    date are NOT published on the DY-01 page and no DY-01 PDF was found (4 URL
    patterns 404). Predecessor D-PSC-DY-23 PDF (requirements as of 2024-02-21)
    gave 90 min and 8 domains (NAS/PowerScale/OneFS 13%, Foundations for
    Access 17%, Identity Mgmt/Authorization 10%, Client Access 13%, Data
    Protection and Layout 12%, Storage Pools 13%, Data Services 15%,
    Monitoring 7%) on OneFS 8.2 / Gen6 / InsightIQ 3.0; use it only as a
    detail checklist (RBAC vs ZRBAC, ID mapping, FEC/requested-vs-actual
    protection, isi get, neighborhoods/VHS, file filtering, DataIQ, S3).
    DS-01 domains: Discover 14%, Design and Plan 18%, Platform Infrastructure
    36%, Mgmt/Identity/Advanced Apps 24%, Monitor 8%. MN-01: Hardware Concepts,
    Hardware Maintenance (FRU/CRU), Hardware Installation, Implementation, 25%
    each. Product currency: Dell "PowerScale OneFS Info Hubs" (modified
    2026-11-03) lists OneFS 9.16.0.0 as newest (9.7-9.16 hubs); no OneFS 10.
    Dell's "OneFS Current Patches" KB is "no longer maintained". Dell support
    names the cloud offer "PowerScale for Public Cloud (Legacy)" -
    "software-defined, scale-out NAS (based on PowerScale OneFS) as a
    customer-managed offer in AWS and Azure". Hardware hub (modified
    2026-08-21) lists F910, F710, F210, PA110, F900, F600, F200, B100, P100,
    A300/A3000, H700/H7000 plus A310/A3100/H710/H7100 and "Dell PowerEdge
    R7725xd for Software Defined Storage".
    Sources (primary, vendor):
    https://learning.dell.com/content/dell/en-us/home/certification-overview/certificationandbadges.html
    https://learning.dell.com/content/dell/en-us/home/certification-overview/available-exams.html?exam=D-PSC-DY-01
    https://learning.dell.com/content/dell/en-us/home/certification-overview/available-exams.html?exam=D-PSC-DS-01
    https://learning.dell.com/content/dell/en-us/home/certification-overview/available-exams.html?exam=D-PSC-MN-01
    https://learning.dell.com/content/dam/dell-emc/documents/en-us/D-PSC-DY-23%20%20PowerScale%20Deploy.pdf
    https://www.dell.com/support/kbdoc/000152189/powerscale-onefs-info-hubs
    https://www.dell.com/support/kbdoc/en-au/000401512/onefs-9-13-0-0-documentation---powerscale-info-hub
    https://www.dell.com/support/kbdoc/en-ap/000184794/powerscale-onefs-current-patches
    https://www.dell.com/support/kbdoc/en-bg/000198853/hardware-powerscale-info-hub
    https://www.dell.com/support/product-details/en-pg/product/apex-file-storage-public-cloud/resources/articles
    Target bar: pass D-PSC-DY-01 (Deploy, 4 domains, 62% post-install config)
    on OneFS 9.x current (9.16), using DY-23 bullets as the detail checklist.
  - Gap vs blueprint (pages mentioning each term, out of 27): Zero coverage:
    CAVA/ICAP antivirus (a named DY-01 objective), ZRBAC, neighborhoods, inline
    data reduction, DataIQ, file filtering, L3 cache, OneFS simulator,
    FRU/CRU, PowerScale for Public Cloud, 2024+ nodes. Thin: job engine 1,
    SSIP 2, file pool policies 2, SmartDedupe 2, ID mapping 2, isi get 2,
    groupnets 3, InsightIQ 3 (install/discover is a DY-01 objective), RBAC 3,
    SmartLock/WORM 3, upgrades 4, SupportAssist/SRS 4, Gen6/F-series nodes 4,
    CloudPools 6, node pools 7, SmartPools 9, SnapshotIQ 9, protection
    levels/FEC 9. OK: SMB 24, NFS 24, SyncIQ 24, quotas 17, SmartConnect 14,
    access zones 12, AD 11, HealthCheck 11, S3 11, HDFS 11, ACL/POSIX 11.
    Phase B should: (1) add dedicated pages for cluster creation/node
    add-remove-reimage + cabling, OneFS upgrade (rolling/simultaneous/
    parallel, patches, firmware), SmartConnect deep-dive (groupnet/subnet/
    pool, SSIP, multi-subnet DNS delegation), access zones + auth providers +
    ID mapping + RBAC/ZRBAC, job engine (jobs, impact policies, priorities),
    CAVA/ICAP antivirus, SmartLock (enterprise vs compliance), SmartDedupe +
    inline data reduction, InsightIQ install/monitor, HealthCheck + event/
    alert notifications, FEC/protection levels + isi get; (2) refresh version
    matrix/FAQ to 9.16 from the Info Hubs index, replace CloudIQ with Dell
    AIOps, add current hardware list and PowerScale for Public Cloud note;
    (3) purge or source release-notes.md. Overlap: InsightIQ (Dell product)
    currently lives at storage/products/netapp/insightiq (24 pages, 21 mention
    PowerScale/OneFS) - cross-link rather than duplicate; flag misfiling.
  - site_audit (2026-11-25): 72/72 clean (full run, 72 checks incl. new 71/72; one run
    covered these 7 items). Queue file only.
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
