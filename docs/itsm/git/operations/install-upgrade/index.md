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
