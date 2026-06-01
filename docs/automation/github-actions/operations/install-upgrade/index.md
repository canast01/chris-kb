# GitHub Actions — Install & Upgrade


<div class="kb-summary">
> Part of the [GitHub Actions Operations](../index.md) reference.
</div>

---

## Self-Hosted Runner Upgrade Procedure

Self-hosted runners do not auto-update by default (unlike GitHub-hosted runners). Follow this procedure for each upgrade cycle.

### 1. Check the current runner version

On each runner host, check the installed version:

```bash
cd /opt/actions-runner   # or wherever the runner is installed
./config.sh --version
```
┌───────────────────────────────── GitHub Actions — Install & Upgrade ──────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  GitHub Actions is a hosted service — no server-side installation; manage self-hosted runners │   │
│   │    Self-hosted runner install: download from GitHub, configure, register, run as OS service   │   │
│   │   Runner updates: GitHub-hosted auto-update weekly; self-hosted manual or auto-update policy  │   │
│   │        ARC (Actions Runner Controller): Kubernetes-based auto-scaling runner deployment       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Self-Hosted Runner Setup           │  │            ARC Setup (Kubernetes)           │   │
│   │       1. Settings → Actions → Runners        │  │          helm install arc oci://...         │   │
│   │          2. Download runner package          │  │      kubectl apply -f runnerdeployment      │   │
│   │         3. ./config.sh --url --token         │  │          Set minRunners/maxRunners          │   │
│   │           4. sudo ./svc.sh install           │  │           Configure runner labels           │   │
│   │            5. sudo ./svc.sh start            │  │           Verify runners register           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ARC             = Actions Runner Controller; Kubernetes operator managing ephemeral runner pods│   │
│   │  Runner version  = must be within 30 days of latest; GitHub stops routing jobs to old runners │   │
│   │     Ephemeral     = --ephemeral flag: runner deregisters after each job; clean env per run    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Confirm the runner appears as **Idle** in the GitHub repository or organisation runner list (Settings > Actions > Runners).

### 5. Validate with a test workflow

Trigger a lightweight test workflow targeting the upgraded runner before routing production jobs to it:

```yaml
on: workflow_dispatch
jobs:
  validate:
    runs-on: [self-hosted, <runner-label>]
    steps:
      - run: echo "Runner version check"
      - run: cat /opt/actions-runner/.runner
```

Confirm the job completes successfully and the correct runner version is reported in the job log.

---

## Version Pinning for Actions

Pin third-party actions to a specific commit SHA rather than a mutable tag to prevent supply-chain substitution:

| Pattern | Risk | Recommendation |
|---|---|---|
| `uses: actions/checkout@main` | Pulls whatever is on `main` at run time — changes without notice | Do not use |
| `uses: actions/checkout@v4` | Tag can be force-pushed to a different commit | Acceptable for first-party GitHub actions (actions/*); avoid for third-party |
| `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` | Pinned to a specific commit SHA | Preferred for all third-party actions |

Use [Dependabot](https://docs.github.com/en/code-security/dependabot) or [Renovate](https://docs.renovatebot.com/) to automate SHA pin updates.

---

## Runner Group Management

| Task | Location | Notes |
|---|---|---|
| Create a runner group | Org Settings > Actions > Runner groups | Scope runner groups to specific repositories or all repositories |
| Move a runner to a group | Org Settings > Actions > Runners > Edit | A runner can belong to only one group |
| Restrict a group to selected repos | Runner group > Edit > Repository access | Use this to segregate production and development runners |
| Set group policies | Runner group > Edit > Workflow access | Control whether public repository workflows can use the group |

---

## Upgrade Validation Checklist

| Check | Pass Criteria |
|---|---|
| Runner service status | `active (running)` in systemctl output |
| Runner registration | Runner shows as **Idle** in GitHub Settings > Actions > Runners |
| Runner version | Reported version matches target upgrade version |
| Test workflow | Workflow dispatched to runner completes without errors |
| Job labels | Runner labels are preserved (check `.runner` file or GitHub UI) |
| No orphaned processes | No `Runner.Worker` or `Runner.Listener` processes from the old version still running |

---

## Rollback Procedure

If the upgraded runner fails validation:

1. Stop the runner service: `sudo systemctl stop actions.runner.<org>-<name>.service`
2. Re-extract the previous runner tarball over the installation directory (keep the existing `.credentials` and `.runner` files — do not overwrite them).
3. Restart the service: `sudo systemctl start actions.runner.<org>-<name>.service`
4. Validate the runner shows Idle in the GitHub UI before routing jobs back to it.
5. File an issue against the runner upgrade noting the failure and the version combination.

Keep the previous runner tarball on the host until the upgraded version has been validated in production for at least one full release cycle.
