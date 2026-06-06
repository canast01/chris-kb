# Git — Common Issues

```bash
# See which files are conflicted
git status
# "both modified:   src/config.go"

# Show the conflict markers in a file
git diff

# Use a 3-way diff tool
git mergetool
```
```text
┌───────────────────────────────────────── Git — Common Issues ─────────────────────────────────────────┐
│                                                                                                       │
│  Common Git problems: detached HEAD, wrong commits, line endings, and submodule errors.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Detached HEAD                 │  │             Wrong Branch Commit             │   │
│   │          Cause: git checkout <sha>           │  │          Save: git stash or branch          │   │
│   │          Fix: git checkout <branch>          │  │        Move: git cherry-pick + reset        │   │
│   │        Keep work: git checkout -b new        │  │          Undo pushed: revert commit         │   │
│   │       HEAD moves on checkout / switch        │  │         Undo local: git reset HEAD~1        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Revert for pushed commits (safe); reset for local-only commits (destructive)                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Line Ending Issues              │  │               Submodule Errors              │   │
│   │          core.autocrlf: true (Win)           │  │     Update: git submodule update --init     │   │
│   │       core.autocrlf: input (Unix/Mac)        │  │       Detached: cd sub && git checkout      │   │
│   │        .gitattributes: text=auto eol         │  │        Wrong URL: .gitmodules update        │   │
│   │       Normalize: git add --renormalize       │  │        Remove: git rm --cached <path>       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Developer workstation · OS (CRLF vs LF) · Git remote · submodule repos                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Detached HEAD   = HEAD points to commit, not branch; commits not saved to branch                     │
│  git revert      = creates new commit that undoes a previous commit; safe for shared                  │
│  git reset HEAD~1= undo last commit; --soft keeps changes staged, --hard discards                     │
│  CRLF            = Windows line ending (\r\n); causes diffs across OS boundaries                      │
│  core.autocrlf   = convert CRLF↔LF on checkout/commit; "true" on Windows                              │
│  .gitattributes  = per-path line ending rules; text=auto normalises to LF in repo                     │
│  add --renormalize= re-stages all files with correct line endings after attr change                   │
│  Submodule       = embedded Git repo; tracked as commit SHA in parent repo                            │
│  update --init   = clone submodule if missing and check out pinned commit                             │
│  .gitmodules     = file listing submodule paths and remote URLs                                       │
│  git rm --cached = removes file/submodule from index without deleting from disk                       │
│  cherry-pick     = apply specific commit to current branch; use to move work                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Enable rerere (re-use recorded resolution)
git config --global rerere.enabled true

# After resolving, rerere records the resolution automatically
# Future identical conflicts are resolved automatically
git rerere
```
```bash
git status
# HEAD detached at a1b2c3d

git log --oneline -5
```
```bash
# Return to wherever you were before
git switch -
# or
git checkout -
```
```bash
# Create a new branch at the current (detached) commit
git switch -c feature/save-my-work

# Or attach to an existing branch (only if no new commits were made)
git switch main
```
```bash
# Return to main, discarding any uncommitted detached-HEAD changes
git switch main
# Any commits made in detached HEAD state are now unreachable (dangling)
# They will be garbage collected after ~2 weeks
```
```yaml
! [rejected] main -> main (non-fast-forward)
error: failed to push some refs to 'origin'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart.
```
```bash
# Fetch and rebase your commits on top of remote
git pull --rebase origin main

# Resolve any conflicts that arise during rebase
# Then push
git push origin main
```
```bash
git pull origin main        # creates a merge commit
git push origin main
```
```bash
# WARNING: rewrites remote history — never use on shared/protected branches
git push --force-with-lease origin feature/my-branch
# --force-with-lease is safer than --force: fails if someone else pushed since your last fetch
```
```bash
# Via API — enable branch protection
curl -X POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/projects/:id/protected_branches" \
  --data 'name=main&push_access_level=0&merge_access_level=40&allow_force_push=false'
```
```text
remote: error: File large-binary.bin is 150.00 MB; this exceeds GitHub's file size limit of 100.00 MB.
remote: error: GH001: Large files detected. You may want to try Git Large File Storage.
```
```bash
# Undo the last commit, keep changes staged
git reset --soft HEAD~1

# Remove the large file from staging
git rm --cached path/to/large-binary.bin
echo "path/to/large-binary.bin" >> .gitignore
git add .gitignore

git commit -m "Remove large binary; add to .gitignore"
```
```bash
# Using git-filter-repo (recommended over BFG for complex cases)
pip install git-filter-repo
git filter-repo --invert-paths --path path/to/large-binary.bin

# Force push to all remotes (coordinate with team first)
git push --force-with-lease origin main

# --- OR --- using BFG Repo Cleaner (faster for simple cases)
bfg --delete-files large-binary.bin
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force origin main
```
```bash
# Install LFS
git lfs install

# Track the file pattern
git lfs track "*.bin"
git lfs track "*.zip"
git add .gitattributes

# Migrate existing history (all branches)
git lfs migrate import --include="*.bin" --everything

git push --force-with-lease origin main
```
```text
remote: HTTP Basic: Access denied
fatal: Authentication failed for 'https://gitlab.example.com/org/repo.git'
```
```bash
# Check which credential store is active
git config --global credential.helper

# List cached credentials (macOS Keychain)
git credential-osxkeychain erase <<EOF
protocol=https
host=github.com
EOF

# Test authentication
curl -sf -u username:TOKEN https://api.github.com/user | jq .login
```
```bash
# macOS — remove cached entry and let Git re-prompt
git credential-osxkeychain erase <<EOF
protocol=https
host=github.com
EOF
git fetch   # will prompt for new credentials

# Linux (libsecret / GNOME keyring)
git config --global credential.helper libsecret

# Linux (store in plain file — not recommended for production)
git config --global credential.helper store
# Credentials stored in ~/.git-credentials

# Use a new PAT in the URL directly (temporary)
git remote set-url origin https://oauth2:NEW_TOKEN@gitlab.example.com/org/repo.git

# Git Credential Manager (cross-platform)
git credential-manager-core erase
```
```bash
# Verify new token works
curl -H "Authorization: Bearer $NEW_TOKEN" https://api.github.com/user | jq .login

# Update remote URL with new token (use credential store instead when possible)
git remote set-url origin https://github.com/org/repo.git
git config --global credential.helper osxkeychain   # or manager-core
```
```text
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
```
```bash
# Test SSH connection with verbose output
ssh -vT git@github.com
ssh -vT git@gitlab.example.com

# Check which key is being offered
ssh-add -l

# Check known_hosts
ssh-keygen -F github.com
```
```bash
# Start agent if not running
eval "$(ssh-agent -s)"

# Add key
ssh-add ~/.ssh/id_ed25519

# Verify
ssh-add -l

# Persist across reboots (macOS)
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```
```bash
# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub via API
curl -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/keys \
  -d "{\"title\":\"$(hostname)\",\"key\":\"$(cat ~/.ssh/id_ed25519.pub)\"}"

# Add to GitLab via API
curl -X POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/user/keys" \
  --data "title=$(hostname)&key=$(cat ~/.ssh/id_ed25519.pub)"
```
```bash
# ~/.ssh/config
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github
    IdentitiesOnly yes

Host gitlab.example.com
    HostName gitlab.example.com
    User git
    IdentityFile ~/.ssh/id_ed25519_gitlab
    IdentitiesOnly yes
    Port 22
```
```text
error: Server does not allow request for unadvertised object
fatal: remote error: upload-pack: not our ref
```
```bash
# Initialise and clone all submodules recursively
git submodule update --init --recursive

# Clone with submodules from the start
git clone --recurse-submodules https://github.com/org/repo.git
```
```bash
# Check submodule status
git submodule status

# Update all submodules to the commit recorded in the parent repo
git submodule update --recursive

# Update submodule to remote HEAD (use with caution — changes the pinned commit)
git submodule update --remote --merge

# Force-reset a submodule to its recorded commit
git submodule foreach git reset --hard
git submodule update --recursive
```
```bash
# Check what changed
git submodule foreach git status
git submodule foreach git diff

# Fix file mode differences
git submodule foreach git config core.fileMode false

# Reset silently modified submodule
git submodule foreach git checkout -- .
```
```bash
# Proper removal — three steps required
git submodule deinit -f path/to/submodule
git rm -f path/to/submodule
rm -rf .git/modules/path/to/submodule
git commit -m "Remove submodule path/to/submodule"
```
```bash
# Show full config (effective, merged from all scopes)
git config --list --show-origin

# Show all remotes
git remote -v

# Show current branch tracking info
git branch -vv

# Show reflog (last 20 operations — useful for recovery)
git reflog -20

# Show what changed between local and remote
git fetch origin
git log origin/main..HEAD --oneline    # commits you have, remote doesn't
git log HEAD..origin/main --oneline    # commits remote has, you don't
git diff origin/main...HEAD            # diff of diverged changes
```
