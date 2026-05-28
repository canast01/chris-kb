# Change Management


```
┌────────────────────────────────────────── Change Management ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Change management: structured process to control IT changes and minimise risk         │   │
│   │           Types: Standard (pre-approved), Normal (CAB review), Emergency (expedited)          │   │
│   │         ITIL framework: RFC → assessment → approval → implementation → review → close         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    RFC raised → assessed → CAB reviewed → approved → scheduled → executed → closed                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Standard Change       │  │        Normal Change        │  │       Emergency Change      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │         Pre-approved        │  │          CAB review         │  │       ECAB or on-call       │   │
│   │           Low risk          │  │       Risk assessment       │  │         P1 fix only         │   │
│   │     Documented template     │  │       Backout plan req      │  │      Retrospective req      │   │
│   │        No CAB needed        │  │       Scheduled window      │  │        Immediate exec       │   │
│   │        e.g. patching        │  │         e.g. upgrade        │  │         e.g. P1 fix         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   │      Phase       │     Activity     │       Owner       │     Artefact     │       Gate       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │      Raise       │   RFC creation   │     Requestor     │     RFC form     │   Completeness   │   │
│   │      Assess      │  Risk + impact   │     Change mgr    │   Risk matrix    │    Assessment    │   │
│   │     Approve      │     CAB vote     │        CAB        │   Approval rec   │ Approved status  │   │
│   │      Close       │    PIR/review    │     Change mgr    │   Closure note   │   Success/fail   │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    RFC    = Request for Change; formal document describing the change and its rationale               │
│    CAB    = Change Advisory Board; reviews normal changes; approves or rejects                        │
│    ECAB   = Emergency CAB; subset of CAB for expedited emergency change approval                      │
│    PIR    = Post-Implementation Review; assesses whether change met objectives                        │
│    Backout= Rollback plan; must be documented before every normal/emergency change                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="change-approval/"><strong>Change Approval</strong><span>CAB submission, risk assessment, approval workflow, and sign-off requirements.</span></a>
<a class="kb-card" href="change-communication/"><strong>Change Communication</strong><span>Stakeholder notification templates, downtime announcements, and post-change updates.</span></a>
<a class="kb-card" href="change-request/"><strong>Change Request</strong><span>Change request form, required fields, categorisation, and submission checklist.</span></a>
<a class="kb-card" href="change-validation/"><strong>Change Validation</strong><span>Pre-change and post-change validation steps, success criteria, and rollback triggers.</span></a>
<a class="kb-card" href="deployment-procedure/"><strong>Deployment Procedure</strong><span>Step-by-step deployment execution, sequencing, checkpoints, and sign-off.</span></a>
<a class="kb-card" href="emergency-change/"><strong>Emergency Change</strong><span>Emergency change authorisation, expedited approval, and retrospective documentation.</span></a>
<a class="kb-card" href="release-management/"><strong>Release Management</strong><span>Release packaging, scheduling, dependency mapping, and go/no-go criteria.</span></a>
</div>
