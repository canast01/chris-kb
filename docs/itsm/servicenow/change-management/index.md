# ServiceNow — Change Management

<div class="kb-summary">
ServiceNow change management procedures — change request lifecycle, CAB process, standard changes, and post-implementation review.
</div>

```text
┌─────────────────────────────────── ServiceNow — Change Management ────────────────────────────────────┐
│                                                                                                       │
│   Change types: Standard (pre-approved), Normal (CAB review), Emergency (expedited approval)          │
│   CAB: Change Advisory Board; reviews Normal changes; meets on schedule (typically weekly)            │
│   Risk matrix: scored by impact × likelihood; drives approval path and required documentation         │
│   PIR: Post-Implementation Review; mandatory for all Normal and Emergency changes                     │
│                                                                                                       │
│   Change lifecycle                                                                                    │
│   Raise RFC    Create change record; fill required fields; attach backout plan + test steps           │
│   Categorise   Standard (auto-approve) / Normal (CAB) / Emergency (e-CAB or ECAB)                     │
│   Risk assess  Score impact + likelihood; attach mitigation plan for Medium and above                 │
│   Approve      Standard: auto; Normal: CAB vote; Emergency: CAB Chair + 2 approvers minimum           │
│   Implement    Follow deployment procedure; go/no-go gate before execution window                     │
│   Validate     Post-change testing per validation checklist; sign-off by change owner                 │
│   Close        Classify outcome (Successful / Unsuccessful / Partial); schedule PIR if required       │
│                                                                                                       │
│   Standard change catalogue                                                                           │
│   Pre-approved for low-risk repeatable tasks; no CAB review required                                  │
│   Examples: OS patch within approved window, SSL cert renewal, AD group modification                  │
│   New templates added by CAB after initial approval; annual review of existing templates              │
│                                                                                                       │
│   Emergency change process                                                                            │
│   CAB override when production impact is active and delay is not acceptable                           │
│   Minimum approvers: ECAB Chair + 2 (e.g. Technical Lead + Service Owner)                             │
│   Post-implementation: retrospective RFC raised within 24h; PIR within 5 business days                │
│                                                                                                       │
│   Key terms:                                                                                          │
│   RFC          = Request for Change; the ServiceNow change record                                     │
│   CAB          = Change Advisory Board; weekly meeting to approve Normal changes                      │
│   ECAB         = Emergency CAB; subset of CAB; can convene within 30 min for P1 changes               │
│   PIR          = Post-Implementation Review; lessons learned after significant changes                │
│   backout plan = documented rollback steps; must be approved before change is authorised              │
│   go/no-go     = decision gate before execution; based on environment health and readiness criteria   │
│   change freeze= period where no changes are allowed (e.g. business-critical periods, holidays)       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="change-request/"><strong>Change Request (RFC)</strong><span>RFC creation, required fields, and submission workflow in ServiceNow.</span></a>
<a class="kb-card" href="change-approval/"><strong>Change Approval</strong><span>Approval requirements by change type — standard, normal, and emergency CAB paths.</span></a>
<a class="kb-card" href="change-communication/"><strong>Change Communication</strong><span>Stakeholder notification plan and communication templates for each change phase.</span></a>
<a class="kb-card" href="risk/"><strong>Risk Assessment</strong><span>Change risk scoring matrix — impact, likelihood, and mitigation requirements.</span></a>
<a class="kb-card" href="backout-plan/"><strong>Backout Plan</strong><span>Backout criteria, rollback decision tree, and plan template for every change.</span></a>
<a class="kb-card" href="deployment-procedure/"><strong>Deployment Procedure</strong><span>Deployment execution steps, go/no-go gates, and implementation checklist.</span></a>
<a class="kb-card" href="change-validation/"><strong>Change Validation</strong><span>Post-change validation steps, testing criteria, and sign-off requirements.</span></a>
<a class="kb-card" href="closeout/"><strong>Change Closeout</strong><span>Closeout checklist, outcome classification, and PIR scheduling.</span></a>
<a class="kb-card" href="procedures/"><strong>Procedures</strong><span>Change request lifecycle and full CAB procedures reference.</span></a>
<a class="kb-card" href="standard-changes/"><strong>Standard Changes</strong><span>Pre-approved standard change catalogue and registration process.</span></a>
<a class="kb-card" href="emergency-changes/"><strong>Emergency Changes</strong><span>Emergency change catalogue — pre-approved expedited changes.</span></a>
<a class="kb-card" href="emergency-change/"><strong>Emergency Change Procedure</strong><span>Emergency change execution procedure — CAB override, approvals during implementation.</span></a>
<a class="kb-card" href="release-management/"><strong>Release Management</strong><span>Release planning, scheduling, coordination, and go-live gate criteria.</span></a>

</div>
