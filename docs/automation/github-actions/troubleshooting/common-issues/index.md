# GitHub Actions — Common Issues


<div class="kb-summary">
> Part of the [GitHub Actions Troubleshooting](../index.md) reference.
</div>

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
