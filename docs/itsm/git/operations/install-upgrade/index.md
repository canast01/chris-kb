---
tags:
  - git
  - operations
---
# Git — Install and Upgrade

```bash
# Install from distro repo
sudo apt-get update && sudo apt-get install -y git

# Check installed version
git --version

# Install latest stable via PPA (Ubuntu)
sudo add-apt-repository ppa:git-core/ppa -y
sudo apt-get update
sudo apt-get install -y git

# Upgrade only
sudo apt-get install --only-upgrade git
```

```powershell
# Upgrade via winget
winget upgrade --id Git.Git -e --include-unknown

# Check version
git --version
```
```bash
# 1. Back up
sudo gitlab-backup create CRON=1
sudo cp /etc/gitlab/gitlab-secrets.json /secure/
sudo cp /etc/gitlab/gitlab.rb /secure/

# 2. Update package (Ubuntu/Debian)
curl -s https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.deb.sh | sudo bash
sudo apt-get update
sudo apt-get install -y gitlab-ee=17.0.3-ee.0

# 3. Reconfigure and restart
sudo gitlab-ctl reconfigure
sudo gitlab-ctl restart

# 4. Run post-upgrade checks
sudo gitlab-rake gitlab:check SANITIZE=true
sudo gitlab-rake db:migrate:status | tail -5
curl -sf https://gitlab.example.com/-/readiness?all=1 | jq .
```
```text
15.4 → 15.11.x → 16.0.x → 16.3.x → 16.11.x → 17.1.x
```
```bash
# Stop at each required version, run migrations, verify, then continue

# Upgrade to 15.11 (last minor before 16)
sudo apt-get install -y gitlab-ee=15.11.13-ee.0
sudo gitlab-ctl reconfigure
sudo gitlab-rake db:migrate:status
sudo gitlab-rake gitlab:check SANITIZE=true

# Wait for background migrations to complete before upgrading to 16.0
sudo gitlab-rails runner "Gitlab::Database::BackgroundMigration::BatchedMigration.where(status: [:active, :queued]).count"
# Must return 0 before proceeding

# Upgrade to 16.0
sudo apt-get install -y gitlab-ee=16.0.9-ee.0
# ... repeat for each stop version
```

```text title="Expected output"
Reading package lists... Done
Building dependency tree... Done
Setting up gitlab-ee (15.11.13-ee.0) ...
gitlab Reconfiguring GitLab and installing dependencies. This may take a while.
...
Running migrations for main: succeeded
Status: up to date
Checking GitLab Shell ... OK
Checking GitLab API ... OK
Checking Database Connection ... OK
Checking Database Version ... OK (PostgreSQL 13.11)
Checking Uploads ... OK
0
Reading package lists... Done
Building dependency tree... Done
Setting up gitlab-ee (16.0.9-ee.0) ...
```

!!! warning "Common errors"
    **`dpkg: error processing package gitlab-ee (--configure): dependency problem - will not configure`** — Run `sudo apt-get install -f` to fix broken dependencies before retrying the upgrade.
    **`FATAL: Ident authentication failed for user "gitlab"`** — Ensure PostgreSQL is running with `sudo systemctl restart postgresql` and verify the gitlab database user credentials in `/etc/gitlab/gitlab.rb`.
    **`ActiveRecord::MigrationError: An error has occurred this migration does not permit transactions`** — Check for incomplete batched migrations with `sudo gitlab-rails runner "puts Gitlab::Database::BackgroundMigration::BatchedMigration.incomplete.count"` and wait for them to finish before proceeding.
```bash
# Check for in-progress background migrations (must be 0 before major upgrade)
sudo gitlab-rails runner "
  count = Gitlab::Database::BackgroundMigration::BatchedMigration
            .where(status: [:active, :queued]).count
  puts \"Pending background migrations: #{count}\"
"

# Force-run pending migrations (if needed)
sudo gitlab-rake db:migrate
```
```yaml
# docker-compose.yml (excerpt)
services:
  gitlab:
    image: gitlab/gitlab-ee:17.0.3-ee.0   # pin the version
    ...
```
```bash
# Pull new image
docker compose pull gitlab

# Stop, upgrade, start
docker compose down gitlab
docker compose up -d gitlab

# Check logs
docker compose logs -f gitlab

# Verify
docker exec -it gitlab gitlab-rake gitlab:check SANITIZE=true
```

```text title="Expected output"
Pulling gitlab
latest: Pulling from gitlab/gitlab-ee
sha256:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6: Pull complete
Status: Downloaded newer image for gitlab/gitlab-ee:latest

Stopping gitlab ... done
Removing gitlab ... done
Creating gitlab ... done

gitlab  | 2024-01-15 14:32:18.456 UTC [1] LOG:  database system is ready to accept connections
gitlab  | 2024-01-15 14:32:45.123 UTC [892] LOG:  connection authorized: user=gitlab database=gitlabhq_production
gitlab  | 2024-01-15 14:33:12.789 UTC [1245] LOG:  autovacuum launcher started
gitlab  | Puma started in cluster mode with 3 processes
gitlab  | 2024-01-15 14:33:28.456 UTC INFO: GitLab is ready

Checking GitLab installation ...
Checking GitLab Shell ... Installed
Checking GitLab API ... OK
Checking GitLab Workers ... 4 workers
Checking Database Connection ... Connected
Checking Database Version ... PostgreSQL 13.8
Checking Uploads ... OK
Checking LFS Objects ... OK
Checking Artifacts ... OK
Checking Pages ... OK

GitLab check passed.
```

!!! warning "Common errors"
    **`Error response from daemon: container gitlab is not running`** — Verify the container started successfully with `docker compose ps` and check logs with `docker compose logs gitlab` for startup errors.
    **`FATAL: remaining connection slots are reserved for non-replication superuser connections`** — Wait 2-3 minutes for the database to fully initialize before running the check, or increase `max_connections` in the PostgreSQL configuration.
    **`Errno::ECONNREFUSED — Connection refused`** — Ensure GitLab has fully started by waiting for the "GitLab is ready" message in logs before running the rake check command.
```bash
# Add / update GitLab Helm repo
helm repo add gitlab https://charts.gitlab.io
helm repo update

# Check current deployed chart version
helm list -n gitlab

# Upgrade (always review values diff first)
helm diff upgrade gitlab gitlab/gitlab \
  --namespace gitlab \
  --version 8.0.3 \
  -f values.yaml

helm upgrade gitlab gitlab/gitlab \
  --namespace gitlab \
  --version 8.0.3 \
  -f values.yaml \
  --timeout 600s \
  --wait

# Monitor rollout
kubectl rollout status deployment/gitlab-webservice -n gitlab
kubectl rollout status deployment/gitlab-sidekiq-all-in-1-v2 -n gitlab
```

```text title="Expected output"
"gitlab" has been added to your repositories
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "gitlab" chart repository
Update Complete. ⎈ Happy Helming!⎈

NAME    NAMESPACE   REVISION    UPDATED                     STATUS      CHART           APP VERSION
gitlab  gitlab      12          2024-01-15 14:32:18.123456  deployed    gitlab-7.9.2    16.7.1

diff --git a/gitlab/templates/webservice-deployment.yaml b/gitlab/templates/webservice-deployment.yaml
index 3a4b5c2..8f7e9d1 100644
--- a/gitlab/templates/webservice-deployment.yaml
+++ b/gitlab/templates/webservice-deployment.yaml
@@ -12,7 +12,7 @@ spec:
       containers:
       - name: webservice
-        image: registry.gitlab.com/gitlab-org/build/cng/gitlab-webservice:v16.7.1
+        image: registry.gitlab.com/gitlab-org/build/cng/gitlab-webservice:v16.8.0
         resources:
           requests:
             memory: "2Gi"

Release "gitlab" has been upgraded. Happy Helming!
NAME: gitlab
NAMESPACE: gitlab
STATUS: deployed
REVISION: 13
CHART: gitlab:8.0.3
APP VERSION: 16.8.0

deployment.apps/gitlab-webservice is rolling out
Waiting for deployment spec update to be observed...
Waiting for rollout to finish: 1 old replicas pending termination...
deployment "gitlab-webservice" successfully rolled out
deployment "gitlab-sidekiq-all-in-1-v2" successfully rolled out
```

!!! warning "Common errors"
    **`Error: release not found`** — Ensure the release name "gitlab" matches your existing deployment with `helm list -n gitlab`.
    **`Error: timed out waiting for the condition`** — Increase the `--timeout` value (e.g., `--timeout 1200s`) or check pod logs with `kubectl logs -n gitlab <pod-name>` for blocking issues.
    **`Error: UPGRADE FAILED: values don't meet the requirements of the schema`** — Validate your `values.yaml` against the chart schema by running `helm template gitlab gitlab/gitlab -f values.yaml` to identify schema violations.
```bash
# 1. Enable maintenance mode
curl -X POST \
  -H "Authorization: Bearer $GHES_TOKEN" \
  "https://github.example.com/api/v3/maintenance" \
  -d '{"maintenance": {"enabled": true, "message": "Upgrading to 3.13"}}'

# 2. Verify maintenance mode is active
curl -s "https://github.example.com/api/v3/maintenance" \
  -H "Authorization: Bearer $GHES_TOKEN" | jq .

# 3. Take snapshot backup
/opt/github-backup-utils/bin/ghe-backup
```

```text title="Expected output"
{"maintenance":{"enabled":true,"message":"Upgrading to 3.13","scheduled_time":null}}
{"maintenance":{"enabled":true,"message":"Upgrading to 3.13","scheduled_time":null},"status":"active"}
Starting backup of github.example.com (192.168.1.42)...
Backup started at 2024-01-15T14:32:18Z
Backing up Git repositories... [████████████████░░] 87%
Backing up MySQL database...
Backing up Redis data...
Backup completed successfully in 12m 43s
Snapshot ID: backup-20240115-143218-abc123def456
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host: github.example.com`** — Verify DNS resolution and network connectivity to the GitHub Enterprise Server hostname.
    **`{"message":"Bad credentials","documentation_url":"https://docs.github.com/rest"}`** — Ensure `$GHES_TOKEN` is set to a valid personal access token with admin:enterprise scope.
    **`ghe-backup: command not found`** — Confirm backup-utils is installed at `/opt/github-backup-utils/` and the PATH includes its bin directory.
```bash
# Upload upgrade package to appliance
scp -P 122 ghes-3.13.0.pkg admin@github.example.com:

# Apply via SSH
ssh -p 122 admin@github.example.com
ghe-upgrade /home/admin/ghes-3.13.0.pkg

# Monitor progress (takes 15–45 minutes)
# The appliance reboots automatically during upgrade

# After reboot — disable maintenance mode
curl -X POST \
  -H "Authorization: Bearer $GHES_TOKEN" \
  "https://github.example.com/api/v3/maintenance" \
  -d '{"maintenance": {"enabled": false}}'

# Verify version
curl -s "https://github.example.com/api/v3/meta" \
  -H "Authorization: Bearer $GHES_TOKEN" | jq .installed_version
```

```text title="Expected output"
ghes-3.13.0.pkg                                    100%  892MB   45.2MB/s   00:19

GitHub Enterprise Server upgrade initiated
Verifying package integrity... OK
Stopping services... OK
Backing up configuration... OK
Extracting upgrade package... OK
Running pre-flight checks... OK
Applying upgrade... OK
Running migrations... OK
Starting services... OK
Appliance will reboot in 30 seconds...

Connection to github.example.com closed by remote host.
Connection to github.example.com closed.

(Waiting 5–10 minutes for appliance to come online...)

{"status":"ok"}

"3.13.0"
```

!!! warning "Common errors"
    **`scp: command not found`** — Install OpenSSH client tools or use `brew install openssh` on macOS.
    **`ghe-upgrade: command not found`** — SSH directly into the appliance as root or a user with sudo privileges; the command is only available in the GHES shell environment.
    **`curl: (7) Failed to connect to github.example.com port 443: Connection refused`** — Wait 2–3 minutes after the appliance reboots for services to fully initialize before retrying the API call.
```bash
# 1. Upgrade replica
ssh -p 122 admin@github-replica.example.com "ghe-upgrade /home/admin/ghes-3.13.0.pkg"

# 2. Failover to replica (replica becomes primary)
ssh -p 122 admin@github-replica.example.com "ghe-repl-promote"

# 3. Upgrade old primary (now replica)
ssh -p 122 admin@github-primary.example.com "ghe-upgrade /home/admin/ghes-3.13.0.pkg"

# 4. Re-establish replication
ssh -p 122 admin@github-primary.example.com "ghe-repl-setup github-replica.example.com"
ssh -p 122 admin@github-primary.example.com "ghe-repl-start"

# 5. Verify replication
ssh -p 122 admin@github-primary.example.com "ghe-repl-status"
```

```text title="Expected output"
Starting upgrade on replica: github-replica.example.com
Upgrading GitHub Enterprise Server 3.12.5 → 3.13.0
[████████████████████████████] 100%
Upgrade completed successfully. Restarting services...
Services started. Replica is ready.

Promoting replica to primary...
Replication stopped.
Replica promoted to primary role.
Primary failover completed at 2024-01-15 14:32:18 UTC

Starting upgrade on primary: github-primary.example.com
Upgrading GitHub Enterprise Server 3.12.5 → 3.13.0
[████████████████████████████] 100%
Upgrade completed successfully. Restarting services...

Configuring replication to github-replica.example.com...
Replication configured. UUID: a7f3c2e1-9b4d-47e8-b1a2-5d8f6c9e2b3a
Replication started successfully.

Replication Status:
  Appliance Hostname: github-primary.example.com
  Replication Role: primary
  Replication Status: HEALTHY
  Last Sync: 2024-01-15 14:35:42 UTC
  Replica UUID: a7f3c2e1-9b4d-47e8-b1a2-5d8f6c9e2b3a
```

!!! warning "Common errors"
    **`ghe-upgrade: command not found`** — Verify the upgrade package path is correct and the file exists on the target appliance with `ssh -p 122 admin@github-replica.example.com "ls -la /home/admin/ghes-3.13.0.pkg"`.
    **`Replication failed: Connection refused on github-replica.example.com:122`** — Ensure network connectivity between appliances and that SSH port 122 is open; test with `ssh -p 122 admin@github-replica.example.com "echo ok"`.
    **`ghe-repl-status: Replication Status: UNHEALTHY`** — Run `ghe-repl-start` on the primary and check logs with `ghe-support-bundle` to diagnose sync failures.
```bash
# 1. Stop GitLab
sudo gitlab-ctl stop

# 2. Install previous package version
sudo apt-get install -y gitlab-ee=<previous-version>

# 3. Restore database from backup
sudo gitlab-backup restore BACKUP=<timestamp_label>

# 4. Restore configuration
sudo cp /secure/gitlab-secrets.json /etc/gitlab/
sudo cp /secure/gitlab.rb /etc/gitlab/

# 5. Reconfigure and restart
sudo gitlab-ctl reconfigure
sudo gitlab-ctl restart

# 6. Verify
sudo gitlab-rake gitlab:check SANITIZE=true
```

```text title="Expected output"
ok: run: alertmanager: (pid 12847) 0s
ok: run: gitaly: (pid 12851) 1s
ok: run: gitlab-workhorse: (pid 12849) 0s
ok: run: logrotate: (pid 12853) 1s
ok: run: nginx: (pid 12850) 0s
ok: run: postgres: (pid 12848) 0s
ok: run: redis: (pid 12852) 0s
ok: run: sidekiq: (pid 12854) 2s
Setting up gitlab-ee (14.10.5-ee.0) ...
Restoring database from backup 1687432891_2023_06_21_14.10.5-ee_gitlab_backup.tar...
Unpacking backup...
Restoring database...
[DONE]
Restoring uploads...
[DONE]
Restoring repositories...
[DONE]
gitlab-secrets.json restored to /etc/gitlab/
gitlab.rb restored to /etc/gitlab/
Running reconfigure...
gitlab Reconfigured!
ok: run: alertmanager: (pid 12901) 0s
ok: run: gitaly: (pid 12905) 1s
ok: run: gitlab-workhorse: (pid 12903) 0s
ok: run: nginx: (pid 12904) 0s
ok: run: postgres: (pid 12902) 0s
ok: run: redis: (pid 12906) 0s
ok: run: sidekiq: (pid 12907) 2s
Checking GitLab Shell ... ok
Checking Gitaly ... ok
Checking Postgres ... ok
Checking Redis ... ok
Checking RabbitMQ ... ok
Checking Elasticsearch ... ok
Checking GitLab API ... ok
Checking GitLab includes API ... ok
Checking GitLab Shell API ... ok
System information
System uptime ... 45 days
Active users ... 287
```

!!! warning "Common errors"
    **`BACKUP=<timestamp_label> does not exist`** — Verify the backup filename exists in /var/opt/gitlab/backups/ using `ls -la /var/opt/gitlab/backups/` and use the correct timestamp.
    **`FATAL: permission denied for database "gitlabhq_production"`** — Ensure the postgres user has proper permissions by running `sudo gitlab-ctl reconfigure` before restore, or check that the backup was created from the same GitLab version.
    **`ERROR: pg_restore: [archiver] unsupported version number in file header`** — Confirm the backup file is not corrupted and matches the target GitLab version; download a fresh backup if necessary.
```bash
# GHES supports rollback to previous upgrade package if within the same minor version
ssh -p 122 admin@github.example.com "ghe-upgrade --allow-downgrade /home/admin/ghes-3.12.5.pkg"

# For major version rollback — restore from backup-utils snapshot
/opt/github-backup-utils/bin/ghe-restore -s /backup/ghes/<snapshot-dir> github-restored.example.com
```
```d2
direction: right

ASSESS: "ASSESS" {shape: rectangle}
TUNE: "Tune config\nAdjust resources" {shape: rectangle}
ROLLBACK: "ROLLBACK" {shape: rectangle}
PKG: "Reinstall previous\npackage version" {shape: rectangle}
RESTORE: "Full restore\nfrom pre-upgrade backup" {shape: rectangle}
VERIFY: "Run gitlab:check\nVerify endpoints" {shape: rectangle}
DONE: "Service Restored" {shape: rectangle}
ESCALATE: "Escalate to Vendor Support" {shape: rectangle}
START: "Post-Upgrade Failure Detected" {shape: rectangle}

ASSESS -> TUNE
ROLLBACK -> PKG
ROLLBACK -> RESTORE
PKG -> VERIFY
RESTORE -> VERIFY
VERIFY -> DONE
VERIFY -> ESCALATE
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Git — Deploy](../../deploy/)
