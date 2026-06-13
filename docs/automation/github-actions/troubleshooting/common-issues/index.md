---
tags:
  - github-actions
  - troubleshooting
search:
  boost: 1.5
---
# GitHub Actions — Common Issues


<div class="kb-summary">
Part of the [GitHub Actions Troubleshooting](../index.md) reference.

*Applies to: GitHub Actions*
</div>

---

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> B1{Workflow not\ntriggering?}
    S --> B2{Secret not\navailable in step?}
    S --> B3{Artifact upload\nfailed?}
    S --> B4{Runner offline\nor busy?}
    S --> B5{Permission denied\non GITHUB_TOKEN?}
    B1 -->|Yes| D1{on.branches filter\nmatches branch?}
    D1 -->|No| R1[Common Failures\n— adjust on.branches or on.paths filter]
    D1 -->|Yes| R2[Common Failures\n— merge workflow file to default branch]
    B2 -->|Yes| D2{Secret defined at\ncorrect scope?}
    D2 -->|No| R3[Common Failures\n— check repo vs env vs org secret scope]
    D2 -->|Yes| R4[Common Failures\n— verify step can access secrets context]
    B3 -->|Yes| D3{Working directory\ncorrect?}
    D3 -->|No| R5[Common Failures\n— add working-directory: or cd in step]
    D3 -->|Yes| R6[Common Failures\n— check artifact path glob matches files]
    B4 -->|Yes| D4{Runner labels\nmatch runs-on?}
    D4 -->|No| R7[Common Failures\n— fix runs-on label or register runner]
    D4 -->|Yes| R8[Common Failures\n— restart runner service on host]
    B5 -->|Yes| R9[Common Failures\n— add permissions: block with required scopes]
    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6,R7,R8,R9 section
    class B1,B2,B3,B4,B5,D1,D2,D3,D4 decision
    class S start
```

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Common Failures

```mermaid
flowchart TD
    failure(["Workflow failure\nor unexpected behaviour"])
    noTrigger{"Did the workflow\ntrigger at all?"}
    checkPaths["Check on.paths filter\nDoes it match the changed files?"]
    stepFail{"Which step\nfailed?"}
    permErr["Resource not accessible\n→ Add permissions: block to job"]
    ctxErr["Context access invalid\n→ Fix ${{ }} expression syntax"]
    exitErr["Exit code 1\n→ Check step output in logs"]
    secretErr["Secret is empty\n→ Check repo vs env vs org scope"]
    wdErr["No such file\n→ Add working-directory: or cd"]

    failure --> noTrigger
    noTrigger -->|No| checkPaths
    noTrigger -->|Yes| stepFail
    stepFail --> permErr
    stepFail --> ctxErr
    stepFail --> exitErr
    stepFail --> secretErr
    stepFail --> wdErr
```
```text
┌─────────────────────────────────── GitHub Actions — Common Issues ────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                     Most frequent GitHub Actions failures and their fixes                     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Issue: Job queued but never picked up                             │   │
│   │     Cause A: no runner with matching labels → fix: add label to runner or change runs-on:     │   │
│   │    Cause B: all runners busy → fix: scale runner pool or add GitHub-hosted runner fallback    │   │
│   │               Cause C: runner offline → fix: sudo ./svc.sh start on runner host               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                Issue: OIDC token request fails                                │   │
│   │       Cause A: permissions: id-token: write missing → fix: add to workflow permissions:       │   │
│   │      Cause B: cloud trust policy wrong → fix: verify sub claim matches workflow ref/repo      │   │
│   │       Cause C: wrong region/audience → fix: check aws-actions configure-creds parameters      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Issue: Workflow not triggering on push                            │   │
│   │        Cause A: on: branches filter does not match current branch → fix: adjust filter        │   │
│   │       Cause B: workflow file not on default branch → fix: merge to default branch first       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [GitHub Actions — Diagnostics](../diagnostics/)
- [GitHub Actions — Escalation](../escalation/)
- [GitHub Actions — Health Checks](../../operations/health-checks/)
