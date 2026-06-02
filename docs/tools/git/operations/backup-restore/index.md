# Git — Backup & Restore


<div class="kb-summary">
This page covers repository backup strategies, platform-level backup procedures, and restore procedures for both individual repositories and full platform instances.
</div>

---

## Backup Strategy Overview

| Strategy | Scope | RPO | Complexity |
|----------|-------|-----|------------|
| `git clone --mirror` | Single repository | Minutes | Low |
| Bare repo rsync | Single/batch repos | Minutes | Low |
| GitLab backup rake task | Full instance | Hours | Medium |
| GitLab Geo | Full instance | Seconds | High |
| GHES snapshot | Full appliance | Minutes | Medium |
| Object storage sync (LFS/artifacts) | Blobs only | Minutes | Low |

---

## Repository Mirroring with `git clone --mirror`

A mirror clone includes all refs (branches, tags, notes, stash) and is the most complete single-repo backup method.

```bash
# Initial mirror clone
git clone --mirror https://github.com/org/repo.git /backup/repo.git

# Update an existing mirror (run on schedule)
cd /backup/repo.git
git remote update --prune

# Verify the mirror is complete
git fsck --full
git count-objects -vH
```
┌────────────────────────────────────── Git — Backup and Restore ───────────────────────────────────────┐
│                                                                                                       │
│  Git backup strategies: mirror clones, bundle exports, and recovery from history.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Mirror Clone Backup              │  │                Bundle Export                │   │
│   │           git clone --mirror <url>           │  │     git bundle create repo.bundle --all     │   │
│   │         Includes all refs + objects          │  │        Single file; portable offline        │   │
│   │          Update: git remote update           │  │        Restore: git clone repo.bundle       │   │
│   │         Schedule via cron to NAS/S3          │  │          Use for air-gap or DR copy         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Mirror backup preserves all refs; bundle is portable for offline/air-gap use                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Restore / Recovery              │  │               History Recovery              │   │
│   │      Restore from mirror: push --mirror      │  │        git reflog: find lost commits        │   │
│   │        Restore from bundle: git clone        │  │       git fsck: find dangling objects       │   │
│   │        Verify: git fsck after restore        │  │        git cherry-pick <sha>: recover       │   │
│   │       Point DNS/webhook to new remote        │  │        git reset --hard <sha>: rewind       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub/GitLab server · backup NAS or S3 bucket · DR Git server · cron jobs                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  git clone --mirror= clones bare repo with all refs; differs from --bare (no refspec)                 │
│  git remote update = re-fetches all remotes; updates mirror without re-cloning                        │
│  git bundle        = exports all commits/refs into portable binary file                               │
│  Air-gap           = isolated network; bundle is only transfer mechanism                              │
│  push --mirror     = pushes all refs from local mirror to new remote; used in restore                 │
│  git reflog        = per-ref log of all pointer movements; survives reset                             │
│  git fsck          = verifies object store integrity; finds dangling commits                          │
│  Dangling object   = commit/blob not reachable from any ref; recoverable via fsck                     │
│  Cherry-pick       = applies diff of specific commit to current branch                                │
│  reset --hard      = moves HEAD and index to commit; discards working tree                            │
│  DR server         = disaster-recovery Git host; receives nightly mirror push                         │
│  Webhook           = must be updated to point to restored remote URL                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## GitLab Instance Backup

### Backup with `gitlab-backup`

```bash
# Create a full backup (stops writes briefly for consistency)
sudo gitlab-backup create

# Backup to a custom directory
sudo gitlab-backup create BACKUP=custom_label STRATEGY=copy

# Backup output location (Omnibus default)
ls -lh /var/opt/gitlab/backups/
# Example: 1715000000_2024_05_06_16.11.0_gitlab_backup.tar

# Exclude specific data to speed up backup
sudo gitlab-backup create SKIP=artifacts,lfs,uploads,registry
```

The backup archive contains:

| Component | Included |
|-----------|----------|
| PostgreSQL database dump | Yes |
| Git repositories | Yes |
| Wiki repositories | Yes |
| CI/CD artifacts | Optional (`SKIP=artifacts`) |
| LFS objects | Optional (`SKIP=lfs`) |
| Container registry | No (backup separately) |
| GitLab configuration (`/etc/gitlab/`) | **No — backup manually** |

```bash
# Always backup configuration separately — it contains secrets
sudo tar -czf /secure/gitlab-config-$(date +%Y%m%d).tar.gz \
  /etc/gitlab/gitlab.rb \
  /etc/gitlab/gitlab-secrets.json
```

### Scheduled GitLab Backup (Cron)

```bash
# /etc/cron.d/gitlab-backup
0 2 * * * root /opt/gitlab/bin/gitlab-backup create CRON=1 2>&1 | tee -a /var/log/gitlab-backup.log

# Cleanup old backups (keep 7 days)
# /etc/gitlab/gitlab.rb:
# gitlab_rails['backup_keep_time'] = 604800   # seconds = 7 days
```

### Backup to S3

```ruby
# /etc/gitlab/gitlab.rb
gitlab_rails['backup_upload_connection'] = {
  'provider'              => 'AWS',
  'region'               => 'eu-west-1',
  'aws_access_key_id'    => ENV['AWS_ACCESS_KEY_ID'],
  'aws_secret_access_key' => ENV['AWS_SECRET_ACCESS_KEY'],
}
gitlab_rails['backup_upload_remote_directory'] = 'my-gitlab-backups'
gitlab_rails['backup_multipart_chunk_size']    = 104857600   # 100 MB
```

---

## GitHub Repository Archive

### Single Repository Archive (GitHub API)

```bash
# Request an archive (GitHub generates a tarball of source at HEAD)
curl -L \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/ORG/REPO/tarball/main" \
  -o repo-backup.tar.gz

# Full git history — use mirror clone instead
git clone --mirror git@github.com:ORG/REPO.git repo.git
```

### GitHub Enterprise — Backup Utilities

GitHub provides the open-source `github-backup-utils` for GHES:

```bash
# Install
git clone https://github.com/github/backup-utils.git /opt/github-backup-utils
cp /opt/github-backup-utils/backup.config-example /etc/github-backup/backup.config

# /etc/github-backup/backup.config
GHE_HOSTNAME="github.example.com"
GHE_DATA_DIR="/backup/ghes"
GHE_EXTRA_USER_DISK_REQUIRED_PERCENTAGE=50

# Run backup
/opt/github-backup-utils/bin/ghe-backup

# Verify backup
/opt/github-backup-utils/bin/ghe-backup-verify
```

Backup schedule (recommended):

```bash
# /etc/cron.d/ghes-backup
0 */4 * * * root /opt/github-backup-utils/bin/ghe-backup >> /var/log/ghes-backup.log 2>&1
```

---

## Restore Procedures

### Restore a Single Repository from Mirror

```bash
# Option 1: Push mirror to a new remote
cd /backup/repo.git
git remote set-url origin https://github.com/org/new-repo.git
git push --mirror

# Option 2: Clone from the mirror locally
git clone /backup/repo.git ~/restored-repo
```

### Restore GitLab Instance

```bash
# 1. Ensure GitLab version matches the backup version
sudo gitlab-rake gitlab:env:info | grep "GitLab information"

# 2. Stop services that use the database
sudo gitlab-ctl stop puma
sudo gitlab-ctl stop sidekiq

# 3. Restore (replace timestamp with actual backup filename prefix)
sudo gitlab-backup restore BACKUP=1715000000_2024_05_06_16.11.0

# 4. Restore configuration files (must be done BEFORE restore if secrets differ)
sudo tar -xzf /secure/gitlab-config-20240506.tar.gz -C /

# 5. Reconfigure and restart
sudo gitlab-ctl reconfigure
sudo gitlab-ctl restart

# 6. Verify
sudo gitlab-rake gitlab:check SANITIZE=true
sudo gitlab-rake gitlab:doctor:secrets
```

### Restore GitHub Enterprise from Backup Utils

```bash
# Restore to a fresh GHES appliance (same version)
/opt/github-backup-utils/bin/ghe-restore github-new.example.com

# Restore specific snapshot
/opt/github-backup-utils/bin/ghe-restore -s /backup/ghes/20240506T020000 github-new.example.com
```

---

## Bare Repo Backup

A bare clone contains only the `.git` contents without a working tree. Suitable for scripted batch backups.

```bash
# Create bare backup
git clone --bare https://github.com/org/repo.git /backup/repo.git

# Bundle into a single file (portable, can be sent via email/SCP)
git -C /backup/repo.git bundle create /backup/repo.bundle --all

# Verify the bundle
git bundle verify /backup/repo.bundle

# Clone from bundle
git clone /backup/repo.bundle ~/restored-repo
git -C ~/restored-repo remote set-url origin https://github.com/org/repo.git
git -C ~/restored-repo fetch origin
```

---

## Backup Verification Steps

Always validate backups after creation. A backup that cannot be restored is not a backup.

```bash
#!/usr/bin/env bash
# verify-backup.sh
set -euo pipefail

BACKUP_PATH="${1:?Usage: $0 <path-to-repo.git>}"

echo "[1/4] Checking object database integrity..."
git -C "$BACKUP_PATH" fsck --full --strict

echo "[2/4] Counting objects..."
git -C "$BACKUP_PATH" count-objects -vH

echo "[3/4] Verifying pack files..."
for pack in "$BACKUP_PATH"/objects/pack/*.idx; do
  git -C "$BACKUP_PATH" verify-pack -v "$pack" > /dev/null && echo "OK: $pack"
done

echo "[4/4] Listing refs..."
git -C "$BACKUP_PATH" show-ref | head -20

echo "Verification complete for: $BACKUP_PATH"
```

### Verification Checklist

| Check | Command | Expected Result |
|-------|---------|-----------------|
| Object integrity | `git fsck --full` | No errors or broken links |
| Ref count | `git show-ref \| wc -l` | Matches source repository |
| Commit count | `git rev-list --count --all` | Matches source |
| Pack files valid | `git verify-pack -v *.idx` | No checksum errors |
| Latest commit accessible | `git log -1` | Shows expected HEAD commit |
| Tags present | `git tag -l \| wc -l` | Matches source repository |
