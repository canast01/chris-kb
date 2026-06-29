---
tags:
  - git
  - operations
---
# Git — Health Checks

```bash
# Basic integrity check
git fsck

# Full check — also verifies pack files and reachability of all objects
git fsck --full --strict

# Check a bare/mirror repository
git -C /backup/repo.git fsck --full

# Common output messages:
# "dangling commit <sha>"    — commit exists but no ref points to it (may be from force-push)
# "dangling blob <sha>"      — orphaned blob, usually from git add then reset
# "missing blob <sha>"       — CORRUPTION — object referenced but missing from disk
# "broken link from tree"    — CORRUPTION — tree references a missing object
```

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
run_this_routine: "Run This Routine" {shape: rectangle}
verify: "Verify" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> run_this_routine
run_this_routine -> verify
verify -> generate_report
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **Git service status** — On a GitLab server run `sudo gitlab-ctl status`; on a Gitea server run `systemctl status gitea`; on Bitbucket Server run `systemctl status bitbucket`; all component services (puma, gitaly, sidekiq, postgresql, nginx) must show `run:` status; any stopped service requires immediate investigation.
2. **Web UI accessible** — Run `curl -sk -o /dev/null -w "%{http_code}" https://<git-server>/api/v4/version` for GitLab or the equivalent health endpoint for your platform; expect HTTP `200`; a non-200 or connection refused response indicates the web tier is down.
3. **Runner status** — Run `gitlab-runner status` on each CI runner host; all registered runners must show `Service is running`; also verify runners appear as `online` in **GitLab Admin → CI/CD → Runners**; offline runners will cause pipelines to queue indefinitely.
4. **Backup recency** — Check the backup destination configured in `/etc/gitlab/gitlab.rb` (key: `gitlab_rails['backup_path']`); run `ls -lht /var/opt/gitlab/backups/*.tar | head -5` and confirm the most recent backup file timestamp is within the last 24 hours; a missing recent backup means the next data loss event will have no recovery point.
5. **Disk space** — Run `df -h /var/opt/gitlab` and `df -h /var/opt/gitlab/git-data`; alert if either volume exceeds 80%; also run the top-20 largest repositories check: `du -sh /var/opt/gitlab/git-data/repositories/*/*/*.git 2>/dev/null | sort -rh | head -20` to identify unexpected growth.
6. **Database size** — Run `sudo gitlab-psql -c "SELECT pg_size_pretty(pg_database_size('gitlabhq_production'));"` and compare against the previous week; rapid database growth (more than 10% week-over-week) should be investigated for runaway audit log or CI artifact storage.
7. **Background jobs (Sidekiq)** — Navigate to **GitLab Admin → Monitoring → Background Jobs**; review the Sidekiq queue depths — all queues should be draining; a persistently growing queue (especially `default` or `mailers`) indicates Sidekiq is unable to keep up and jobs are at risk of being dropped.

```bash
# Set auto-gc thresholds in repo config
git config gc.auto 6700             # loose object threshold (0 = disable auto-gc)
git config gc.autoPackLimit 50      # number of packs before repacking
git config gc.pruneExpire "14 days" # how old objects must be before pruning
git config pack.compression 9       # max compression
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`error: key does not contain a section: gc.auto`** — Ensure you are in a valid git repository directory (run `git rev-parse --git-dir` to verify).
    **`error: Permission denied`** — Run the commands with appropriate permissions or use `--global` flag if configuring user-level settings instead of repo-level.
```bash
BASE="https://gitlab.example.com"

# Basic liveness probe (no auth required)
curl -sf "$BASE/-/health" && echo "UP"

# Readiness — checks all service dependencies
curl -sf "$BASE/-/readiness"

# Full metrics (Prometheus format)
curl -sf "$BASE/-/metrics" | grep -E "^(gitlab_|ruby_|rails_)"

# Database connectivity check
curl -sf "$BASE/-/readiness?all=1" | jq '.db_check'

# Gitaly connectivity check
curl -sf "$BASE/-/readiness?all=1" | jq '.gitaly_check'
```
```json
{
  "master_check": [{"status": "ok"}],
  "db_check":     [{"status": "ok"}],
  "cache_check":  [{"status": "ok"}],
  "gitaly_check": [{"status": "ok"}],
  "queues_check": [{"status": "ok"}]
}
```
```bash
# GitLab component status via gitlab-ctl
sudo gitlab-ctl status

# Check individual service logs
sudo gitlab-ctl tail puma
sudo gitlab-ctl tail gitaly
sudo gitlab-ctl tail sidekiq
sudo gitlab-ctl tail postgresql

# Gitaly health via gRPC
/opt/gitlab/embedded/bin/grpc_health_probe \
  -addr=unix:///var/opt/gitlab/gitaly/gitaly.socket
```

```text title="Expected output"
run: alertmanager: (pid 12847) 45s; run
run: gitaly: (pid 12934) 38s; run
run: gitlab-exporter: (pid 12856) 44s; run
run: gitlab-workhorse: (pid 12923) 40s; run
run: logrotate: (pid 12891) 2s; run
run: nginx: (pid 12912) 41s; run
run: node-exporter: (pid 12867) 43s; run
run: postgres-exporter: (pid 12878) 42s; run
run: postgresql: (pid 12801) 56s; run
run: puma: (pid 12945) 32s; run
run: redis: (pid 12822) 54s; run
run: sidekiq: (pid 12956) 25s; run
run: sshd: (pid 12834) 50s; run

==> /var/log/gitlab/puma/puma_stdout.log <==
2024-01-15T09:23:47.123Z Puma starting in cluster mode...
2024-01-15T09:23:48.456Z * Workers: 4
2024-01-15T09:23:49.789Z * Threads: 4/4

==> /var/log/gitlab/gitaly/current <==
time="2024-01-15T09:23:50.234Z" level=info msg="starting gitaly" version=16.7.0

==> /var/log/gitlab/sidekiq/current <==
2024-01-15T09:23:51.567Z INFO: Sidekiq 7.0.8 starting in cluster mode with 5 concurrency

==> /var/log/gitlab/postgresql/current <==
2024-01-15 09:23:52.890 UTC [12801] LOG: database system is ready to accept connections

status: SERVING
```

!!! warning "Common errors"
    **`Error: No such file or directory @ rb_sysopen - /var/opt/gitlab/gitaly/gitaly.socket`** — Ensure Gitaly service is running with `sudo gitlab-ctl restart gitaly` and verify the socket path exists.
    **`sudo: gitlab-ctl: command not found`** — Install GitLab using the official omnibus package or verify `/opt/gitlab/bin` is in your PATH.
    **`permission denied while trying to connect to the Docker daemon`** — Run the command with proper sudo privileges or add your user to the docker group if using containerized GitLab.
```bash
GHES="github.example.com"

# Maintenance status
curl -sf "https://$GHES/api/v3/maintenance" \
  -H "Authorization: Bearer $GHES_TOKEN" | jq .

# System health check
ssh -p 122 admin@$GHES "ghe-check-disk-usage"
ssh -p 122 admin@$GHES "ghe-config-check"
ssh -p 122 admin@$GHES "ghe-repl-status"     # HA replication status

# GHES Management Console status
curl -sf "https://$GHES:8443/setup/api/check-disk-usage" \
  -u "api_key:$MANAGEMENT_CONSOLE_PASSWORD"
```

```text title="Expected output"
{
  "status": "normal",
  "scheduled_maintenance": false,
  "maintenance_scheduled_for": null
}
Disk usage: 67.3% (402 GB of 598 GB)
Config check passed
Replication Status
  Role: primary
  Enabled: yes
  Primary: github.example.com
  Secondary: github-replica.example.com
  Last sync: 2024-01-15T09:47:22Z
  Lag: 0.12s
  Last check: 2024-01-15T09:48:15Z
{
  "status": "ok",
  "disk_usage_percent": 67.3,
  "disk_available_gb": 196
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl commands or import the GHES certificate into your CA bundle.
    **`Permission denied (publickey).`** — Verify `$GHES_TOKEN` and `$MANAGEMENT_CONSOLE_PASSWORD` are set, and that your SSH key is authorized on the GHES instance.
    **`ghe-repl-status: command not found`** — Confirm GHES has HA replication enabled; this command only exists on replicated instances.
```bash
# Size of a single repository
du -sh /var/opt/gitlab/git-data/repositories/group/project.git

# Top 20 largest repositories
du -sh /var/opt/gitlab/git-data/repositories/*/*/*.git 2>/dev/null | \
  sort -rh | head -20

# Objects breakdown per repo
git -C /path/to/repo.git count-objects -vH

# Find large objects in git history
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {print substr($0,6)}' | \
  sort -k2 -rn | \
  numfmt --field=1 --to=iec-i | \
  head -20

# LFS objects disk usage
git lfs ls-files --size | sort -k2 -rh | head -20
```

```text title="Expected output"
2.8G	/var/opt/gitlab/git-data/repositories/group/project.git
1.2G	/var/opt/gitlab/git-data/repositories/platform/api-service.git
980M	/var/opt/gitlab/git-data/repositories/platform/web-ui.git
756M	/var/opt/gitlab/git-data/repositories/legacy/monolith.git
645M	/var/opt/gitlab/git-data/repositories/infra/terraform.git
512M	/var/opt/gitlab/git-data/repositories/data/warehouse.git
...

count-objects: 15847 objects, 2.3 GiB
in-pack: 14923 objects, 2.1 GiB
packs: 8
size-pack: 2.2 GiB
prune-packable: 0
garbage: 0
size-garbage: 0

a7f2c9e1 refs/heads/main:docs/archive.tar.gz 512M
b3e4d2f5 refs/heads/feature:models/dataset.pkl 384M
c1a9f8b2 refs/tags/v2.1.0:vendor/dependencies.zip 256M
d6e5c3a9 refs/heads/develop:build/artifacts.tar 192M
e2f1a4c7 refs/heads/main:cache/embeddings.bin 128M
...

Locking file list...
a1b2c3d4e5f6 (512 MB) path/to/model.h5
f6e5d4c3b2a1 (384 MB) path/to/dataset.csv
...
```

!!! warning "Common errors"
    **`fatal: not a git repository (or any of the parent directories): .git`** — Verify the repository path exists and is a valid git directory with `ls -la /path/to/repo.git/HEAD`.
    **`du: cannot access '/var/opt/gitlab/git-data/repositories/*/*/*.git': No such file or directory`** — Confirm GitLab repositories directory structure matches your installation path using `ls -la /var/opt/gitlab/git-data/repositories/`.
    **`command not found: numfmt`** — Install GNU coreutils with `apt-get install coreutils` (Debian/Ubuntu) or `yum install coreutils` (RHEL/CentOS).
```bash
# GitLab disk usage summary
sudo gitlab-rake gitlab:storage:list_hashed 2>/dev/null | tail -5

# Top projects by storage (GitLab API)
curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/projects?order_by=last_activity_at&per_page=100" | \
  jq -r '.[] | "\(.statistics.repository_size | . / 1048576 | floor)MB \(.path_with_namespace)"' | \
  sort -rn | head -20

# Filesystem usage
df -h /var/opt/gitlab
df -h /var/opt/gitlab/git-data

# Alert thresholds (add to monitoring)
# Warning:  >75% of git-data partition
# Critical: >90% of git-data partition
```

```text title="Expected output"
Hashed storage: 1247 projects migrated
Hashed storage: 2 projects pending migration
Hashed storage: 0 projects failed migration

5432MB platform/backend
4891MB infrastructure/terraform-modules
3156MB data-science/ml-pipeline
2847MB devops/ansible-playbooks
2103MB security/compliance-scanner
1876MB platform/api-gateway
1654MB infrastructure/kubernetes-config
1523MB devops/monitoring-stack
1401MB platform/documentation
1289MB data-science/datasets
...

Filesystem     Size  Used Avail Use% Mounted on
/dev/sda3      500G  387G  113G  78% /var/opt/gitlab
Filesystem     Size  Used Avail Use% Mounted on
/dev/sdb1      2.0T  1.6T  398G  80% /var/opt/gitlab/git-data
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host name`** — Verify the GitLab hostname is correct and DNS is resolving; check `/etc/hosts` or network connectivity to `gitlab.example.com`.
    **`jq: parse error: Cannot index number with string "statistics"`** — Ensure the API token has sufficient permissions and the GitLab instance is responding with valid JSON; test with `curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "https://gitlab.example.com/api/v4/user"` first.
    **`df: '/var/opt/gitlab/git-data': No such file or directory`** — Confirm the git-data mount point exists and is mounted; run `mount | grep git-data` to verify the filesystem is attached.
```bash
# On the Geo Primary — check replication status
sudo gitlab-rake geo:status

# Example output:
# Name                          | URL                              | Status    | Repositories  | Wikis  | LFS  | Attachments
# Geo-DR-Site                   | https://gitlab-dr.example.com   | Healthy   | 98.7%         | 99.1%  | 100% | 97.3%

# On the Geo Secondary — detailed status
sudo gitlab-rake geo:check

# Via API (from Primary)
curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/geo_nodes/status" | \
  jq '.[] | {name: .name, healthy: .healthy, repositories_synced_count, repositories_failed_count, last_event_timestamp}'

# Check replication lag via PostgreSQL
sudo gitlab-psql -c "
SELECT
  now() - pg_last_xact_replay_timestamp() AS replication_lag,
  pg_is_in_recovery() AS is_secondary;
"

# Geo replication lag alert: > 5 minutes is warning, > 15 minutes is critical
```

```text title="Expected output"
sudo gitlab-rake geo:status
Name                          | URL                              | Status    | Repositories  | Wikis  | LFS  | Attachments
Geo-DR-Site                   | https://gitlab-dr.example.com   | Healthy   | 98.7%         | 99.1%  | 100% | 97.3%

sudo gitlab-rake geo:check
GitLab Geo check Finished
Checking Geo ...
  Geo is available ... yes
  Database replication lag ... 0 seconds
  Repositories synced ... 2847/2851
  Wikis synced ... 2847/2851
  LFS objects synced ... 1203/1203
  Attachments synced ... 5421/5421

curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "https://gitlab.example.com/api/v4/geo_nodes/status" | jq '.[] | {name: .name, healthy: .healthy, repositories_synced_count, repositories_failed_count, last_event_timestamp}'
{
  "name": "Geo-DR-Site",
  "healthy": true,
  "repositories_synced_count": 2847,
  "repositories_failed_count": 4,
  "last_event_timestamp": "2024-01-15T14:32:18.456Z"
}

sudo gitlab-psql -c "SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag, pg_is_in_recovery() AS is_secondary;"
 replication_lag | is_secondary
-----------------+--------------
 00:00:02.341    | t
(1 row)
```

!!! warning "Common errors"
    **`PRIVATE-TOKEN header not provided or invalid`** — Verify the `$GITLAB_TOKEN` environment variable is set and contains a valid Personal Access Token with `api` scope.
    **`could not translate host name "gitlab-dr.example.com" to address`** — Confirm the secondary site's hostname is resolvable and network connectivity exists from the primary to the secondary.
    **`pg_is_in_recovery() returned 'f' on secondary node`** — Verify the secondary database is in recovery mode and replication is configured correctly in `postgresql.conf`.
```bash
#!/usr/bin/env bash
# gitlab-health-check.sh
set -euo pipefail

GITLAB_URL="https://gitlab.example.com"
GITLAB_TOKEN="${GITLAB_TOKEN:?Set GITLAB_TOKEN}"
ALERT_EMAIL="ops@example.com"
FAILURES=()

check() {
  local name="$1"; local cmd="$2"; local expected="$3"
  result=$(eval "$cmd" 2>&1) || true
  if echo "$result" | grep -q "$expected"; then
    echo "[OK]   $name"
  else
    echo "[FAIL] $name — got: $result"
    FAILURES+=("$name")
  fi
}

check "Readiness" \
  "curl -sf '$GITLAB_URL/-/readiness?all=1'" \
  '"status":"ok"'

check "Disk <75%" \
  "df /var/opt/gitlab/git-data | awk 'NR==2{print \$5}' | tr -d '%'" \
  "^[0-7][0-9]$"

check "Gitaly socket" \
  "/opt/gitlab/embedded/bin/grpc_health_probe -addr=unix:///var/opt/gitlab/gitaly/gitaly.socket" \
  "SERVING"

check "Backup recent" \
  "find /var/opt/gitlab/backups -name '*.tar' -mtime -1 | wc -l" \
  "^[1-9]"

if [[ ${#FAILURES[@]} -gt 0 ]]; then
  echo "FAILURES: ${FAILURES[*]}" | mail -s "[ALERT] GitLab health check failed" "$ALERT_EMAIL"
  exit 1
fi

echo "All health checks passed."
```


```text title="Expected output"
[OK]   Readiness
[OK]   Disk <75%
[OK]   Gitaly socket
[OK]   Backup recent
All health checks passed.
```

!!! warning "Common errors"
    **`GITLAB_TOKEN: parameter null or not set`** — Export the GITLAB_TOKEN environment variable before running the script: `export GITLAB_TOKEN="your-token"`.
    **`[FAIL] Readiness — got: curl: (7) Failed to connect to gitlab.example.com port 443`** — Verify GitLab URL is correct and the host is reachable; check firewall rules and DNS resolution with `nslookup gitlab.example.com`.
    **`[FAIL] Gitaly socket — got: Failed to connect to the server`** — Ensure Gitaly service is running with `sudo gitlab-ctl status gitaly` and the socket path `/var/opt/gitlab/gitaly/gitaly.socket` exists.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Git — Procedures](../procedures/)
- [Git — CLI Reference](../cli-reference/)
- [Git — Common Issues](../../troubleshooting/common-issues/)
