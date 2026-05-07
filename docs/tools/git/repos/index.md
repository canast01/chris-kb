# Git Repos

Clone, remote management, fetch, pull, push, submodules, and bare repositories.

## Cloning

```bash
# Standard clone
git clone https://github.com/org/repo.git

# Clone into a specific directory
git clone https://github.com/org/repo.git my-local-name

# Shallow clone (last N commits only — faster for CI)
git clone --depth 1 https://github.com/org/repo.git

# Clone a specific branch
git clone -b release/v2.4.0 --single-branch https://github.com/org/repo.git

# Clone with all submodules initialised
git clone --recurse-submodules https://github.com/org/repo.git

# Clone via SSH
git clone git@github.com:org/repo.git
```

## Remote Management

```bash
# List remotes with URLs
git remote -v

# Add a remote
git remote add upstream https://github.com/upstream/repo.git

# Change a remote URL (e.g., HTTPS to SSH)
git remote set-url origin git@github.com:org/repo.git

# Rename a remote
git remote rename origin old-origin

# Remove a remote
git remote remove upstream

# Inspect a remote
git remote show origin
```

| Remote Operation | Command |
|----------------|---------|
| List remotes | `git remote -v` |
| Add remote | `git remote add <name> <url>` |
| Change URL | `git remote set-url <name> <url>` |
| Remove | `git remote remove <name>` |
| Inspect | `git remote show <name>` |

## Fetch, Pull, and Push

```bash
# Fetch all remotes without merging
git fetch --all --prune

# Fetch a specific remote
git fetch origin

# Pull with rebase instead of merge (cleaner history)
git pull --rebase origin main

# Push current branch to same-named remote branch
git push origin HEAD

# Push and set upstream in one step
git push -u origin feature/my-branch

# Force-push (use with extreme caution — only on personal branches)
git push --force-with-lease origin feature/my-branch

# Delete remote branch
git push origin --delete feature/old-branch
```

Always prefer `--force-with-lease` over `--force` — it refuses to overwrite if the remote has new commits you have not seen.

## Submodules

```bash
# Add a submodule
git submodule add https://github.com/org/shared-lib.git libs/shared-lib

# Initialise and update after cloning
git submodule update --init --recursive

# Update all submodules to latest remote commits
git submodule update --remote --merge

# Run a command in all submodules
git submodule foreach 'git pull origin main'

# Remove a submodule
git submodule deinit -f libs/shared-lib
rm -rf .git/modules/libs/shared-lib
git rm -f libs/shared-lib
```

## Bare Repositories

Bare repos contain only the git objects — no working tree. Used as central remotes or for automation.

```bash
# Create a bare repo
git init --bare /srv/git/myrepo.git

# Clone into a bare repo (mirror)
git clone --mirror https://github.com/org/repo.git myrepo.git

# Push to a local bare repo
git remote add local /srv/git/myrepo.git
git push local main

# Update a mirror repo
cd myrepo.git && git remote update
```

| Repo Type | Working Tree | Use Case |
|-----------|-------------|----------|
| Standard | Yes | Local development |
| Bare | No | Central remote, CI server |
| Mirror | No | Full backup including all refs |
| Shallow | Partial history | Fast CI clone |
