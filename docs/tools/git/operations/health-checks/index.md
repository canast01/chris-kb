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
```text
┌───────────────────────────────────────── Git — Health Checks ─────────────────────────────────────────┐
│                                                                                                       │
│  Regular health checks for repositories: object integrity, size, stale refs, and CI status.           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Repository Integrity             │  │             Size and Performance            │   │
│   │         git fsck: no errors expected         │  │       git count-objects -vH: pack size      │   │
│   │       git gc --auto: run periodically        │  │         Large files: git lfs status         │   │
│   │        Verify remotes: git remote -v         │  │          Clone time: < 30 s target          │   │
│   │        Backup age: last mirror < 24 h        │  │        .git/objects: run gc if large        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Integrity and size checks prevent clone degradation; stale refs waste bandwidth                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Stale Ref Cleanup               │  │              CI Pipeline Health             │   │
│   │       Merged branches: delete after PR       │  │         Success rate: > 95 % on main        │   │
│   │       Remote prune: git fetch --prune        │  │        Build time: monitor for drift        │   │
│   │       Stale PRs: weekly review cadence       │  │         Test coverage: no regression        │   │
│   │        Orphaned tags: audit quarterly        │  │        Dependency alerts: Dependabot        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub/GitLab · mirror backup storage · CI runner · Dependabot alerts                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  git fsck         = file system consistency check; verifies object store                              │
│  git gc           = garbage collection; repacks loose objects into pack files                         │
│  count-objects    = shows loose object count and pack file sizes                                      │
│  git fetch --prune= removes remote-tracking refs deleted from remote                                  │
│  Pack file        = compressed bundle of objects; single file for many objects                        │
│  Stale PR         = open pull request with no activity for > 14 days                                  │
│  Orphaned tag     = tag pointing to commit on a deleted or unreachable branch                         │
│  Clone time       = time to git clone full repo; indicator of repo bloat                              │
│  Dependabot       = GitHub bot that opens PRs for dependency security updates                         │
│  Success rate     = % of CI runs on main passing; below 95 % warrants investigation                   │
│  Mirror age       = time since last backup sync; alert if > 24 hours                                  │
│  Build time drift = CI duration creeping up; indicates test suite growth or slowness                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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
