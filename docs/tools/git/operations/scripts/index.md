# Git — Operational Scripts


<div class="kb-summary">
Production-ready shell scripts for common Git platform administration tasks. All scripts are designed to run safely in CI/CD pipelines or as scheduled cron jobs.
</div>

---

## Mass Repository Cloner

Clone or update all repositories in a GitHub Organisation or GitLab Group.

```bash
#!/usr/bin/env bash
# clone-org-repos.sh
# Usage:
#   GitHub: PLATFORM=github ORG=myorg GITHUB_TOKEN=xxx ./clone-org-repos.sh
#   GitLab: PLATFORM=gitlab GROUP_ID=12 GITLAB_TOKEN=xxx GITLAB_URL=https://gitlab.example.com ./clone-org-repos.sh
set -euo pipefail

PLATFORM="${PLATFORM:?Set PLATFORM=github or PLATFORM=gitlab}"
DEST_DIR="${DEST_DIR:-$HOME/repos}"
mkdir -p "$DEST_DIR"

clone_or_update() {
  local url="$1"
  local name="$2"
  local dest="$DEST_DIR/$name"

  if [[ -d "$dest/.git" ]]; then
    echo "Updating: $name"
    git -C "$dest" fetch --all --prune --tags --quiet
  elif [[ -d "$dest" ]]; then
    echo "Skipping (non-git dir exists): $dest"
  else
    echo "Cloning: $name"
    git clone --quiet "$url" "$dest"
  fi
}

if [[ "$PLATFORM" == "github" ]]; then
  ORG="${ORG:?Set ORG}"
  PAGE=1
  while :; do
    repos=$(curl -sf \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/orgs/$ORG/repos?per_page=100&page=$PAGE&type=all" | \
      jq -r '.[] | "\(.ssh_url) \(.name)"')
    [[ -z "$repos" ]] && break
    while IFS=' ' read -r url name; do
      clone_or_update "$url" "$name"
    done <<< "$repos"
    ((PAGE++))
  done

elif [[ "$PLATFORM" == "gitlab" ]]; then
  GROUP_ID="${GROUP_ID:?Set GROUP_ID}"
  GITLAB_URL="${GITLAB_URL:-https://gitlab.com}"
  PAGE=1
  while :; do
    repos=$(curl -sf \
      --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
      "$GITLAB_URL/api/v4/groups/$GROUP_ID/projects?include_subgroups=true&per_page=100&page=$PAGE" | \
      jq -r '.[] | "\(.ssh_url_to_repo) \(.path)"')
    [[ -z "$repos" ]] && break
    while IFS=' ' read -r url path; do
      clone_or_update "$url" "$path"
    done <<< "$repos"
    ((PAGE++))
  done
fi

echo "Done. Repositories in: $DEST_DIR"
```
┌────────────────────────────────────── Git — Operations Scripts ───────────────────────────────────────┐
│                                                                                                       │
│  Shell scripts and hooks for automating Git operations: cleanup, audit, and enforcement.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Branch Cleanup Scripts            │  │                Audit Scripts                │   │
│   │        Delete merged branches locally        │  │       List repos without branch prot.       │   │
│   │          Prune remote tracking refs          │  │       Find repos with secrets in hist.      │   │
│   │       Find stale branches: last commit       │  │          Report large files > 50 MB         │   │
│   │           Batch delete via gh CLI            │  │      List contributors + commit counts      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Cleanup scripts run weekly; audit scripts run monthly or on-demand                                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Git Hooks                   │  │             Automation Patterns             │   │
│   │        pre-commit: lint + secret scan        │  │         gh CLI: scripting GitHub API        │   │
│   │       commit-msg: enforce conv. format       │  │        glab CLI: scripting GitLab API       │   │
│   │         pre-push: run tests locally          │  │       Cron: mirror backup sync nightly      │   │
│   │       pre-receive: server enforcement        │  │       GitHub Actions: automate cleanup      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Developer workstations · CI runners · GitHub/GitLab server hooks · cron jobs                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  pre-commit hook  = client-side script run before git commit creates commit                           │
│  commit-msg hook  = validates commit message format; rejects non-conforming                           │
│  pre-push hook    = client-side; runs before push; can block if tests fail                            │
│  pre-receive hook = server-side; enforces policy before refs update                                   │
│  gh CLI           = GitHub official CLI; scriptable access to repos, PRs, issues                      │
│  glab CLI         = GitLab official CLI; mirrors gh functionality for GitLab                          │
│  Stale branch     = branch with last commit > 60 days; candidate for deletion                         │
│  Secret scan      = detect API keys/passwords in diffs before commit                                  │
│  Conv. format     = Conventional Commits: type(scope): subject                                        │
│  Mirror sync      = nightly cron: cd mirror && git remote update                                      │
│  GitHub Actions   = workflow YAML in .github/workflows/ triggered by events                           │
│  Batch delete     = gh api /repos/{owner}/{repo}/branches/{branch} -X DELETE                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

---

## Commit Activity Report

Generates a per-author commit activity report across one or all repositories.

```bash
#!/usr/bin/env bash
# commit-activity-report.sh
# Usage: REPO_PATH=. SINCE="30 days ago" ./commit-activity-report.sh
set -euo pipefail

REPO_PATH="${REPO_PATH:-.}"
SINCE="${SINCE:-30 days ago}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"   # text | csv

echo "Commit activity report — since: $SINCE"
echo "Repository: $(realpath $REPO_PATH)"
echo "Generated: $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "==="

if [[ "$OUTPUT_FORMAT" == "csv" ]]; then
  echo "author_name,author_email,commits,files_changed,insertions,deletions"
fi

git -C "$REPO_PATH" log \
  --since="$SINCE" \
  --format="%an|%ae" | \
  sort | uniq | \
while IFS='|' read -r name email; do
  stats=$(git -C "$REPO_PATH" log \
    --author="$email" \
    --since="$SINCE" \
    --numstat \
    --format="" | \
    awk 'NF==3 {ins+=$1; del+=$2; files++} END {print files, ins, del}')

  commits=$(git -C "$REPO_PATH" rev-list \
    --author="$email" \
    --since="$SINCE" \
    --count HEAD)

  files=$(echo "$stats" | awk '{print $1}')
  ins=$(echo "$stats" | awk '{print $2}')
  del=$(echo "$stats" | awk '{print $3}')

  if [[ "$OUTPUT_FORMAT" == "csv" ]]; then
    echo "\"$name\",\"$email\",$commits,$files,$ins,$del"
  else
    printf "%-30s %-35s commits=%-4s files=%-5s +%-6s -%-6s\n" \
      "$name" "$email" "$commits" "$files" "$ins" "$del"
  fi
done | sort -t'=' -k2 -rn

echo ""
echo "Total commits: $(git -C "$REPO_PATH" rev-list --since="$SINCE" --count HEAD)"
```

---

## Org-Wide Secret Scanner

Scans all repositories in a directory for accidentally committed secrets using pattern matching. Complements tools like `truffleHog` and `gitleaks` with a lightweight local option.

```bash
#!/usr/bin/env bash
# scan-secrets.sh
# Usage: REPOS_DIR=/backup/git SINCE="90 days ago" ./scan-secrets.sh
set -euo pipefail

REPOS_DIR="${REPOS_DIR:?Set REPOS_DIR}"
SINCE="${SINCE:-90 days ago}"
REPORT_FILE="/tmp/secret-scan-$(date +%Y%m%d-%H%M%S).txt"
FINDINGS=0

# Patterns to match (extend as needed)
PATTERNS=(
  'AKIA[0-9A-Z]{16}'                          # AWS Access Key ID
  'aws_secret_access_key\s*=\s*\S+'           # AWS Secret Key
  '-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY'   # Private keys
  'ghp_[A-Za-z0-9]{36}'                       # GitHub PAT
  'glpat-[A-Za-z0-9_-]{20}'                   # GitLab PAT
  'password\s*[:=]\s*["\047]\S+'              # Generic passwords
  'api[_-]?key\s*[:=]\s*["\047][A-Za-z0-9]{20,}' # API keys
  'Bearer\s+[A-Za-z0-9\-._~+/]+=*'           # Bearer tokens (caution: high noise)
)

PATTERN_REGEX=$(IFS='|'; echo "${PATTERNS[*]}")

echo "Secret scan started: $(date -u)"
echo "Repos dir: $REPOS_DIR"
echo "Scanning commits since: $SINCE"
echo "Report: $REPORT_FILE"
echo ""

{
  echo "# Secret Scan Report"
  echo "# Generated: $(date -u)"
  echo "# Repos: $REPOS_DIR"
  echo ""
} > "$REPORT_FILE"

find "$REPOS_DIR" -maxdepth 2 -name "*.git" -type d | sort | \
while read -r repo; do
  repo_name=$(basename "$repo" .git)
  matches=$(git -C "$repo" log \
    --since="$SINCE" \
    --all \
    -p \
    --no-merges \
    -G "$PATTERN_REGEX" 2>/dev/null | \
    grep -E "$PATTERN_REGEX" | \
    grep -v "^Binary" || true)

  if [[ -n "$matches" ]]; then
    echo "[FINDING] $repo_name"
    {
      echo "## $repo_name"
      echo '```'
      echo "$matches"
      echo '```'
      echo ""
    } >> "$REPORT_FILE"
    ((FINDINGS++)) || true
  else
    echo "[CLEAN]   $repo_name"
  fi
done

echo ""
echo "Scan complete. Findings: $FINDINGS"
echo "Report written to: $REPORT_FILE"

[[ $FINDINGS -gt 0 ]] && exit 1 || exit 0
```

**Note:** For production use, replace or augment with [`gitleaks`](https://github.com/gitleaks/gitleaks) or [`truffleHog`](https://github.com/trufflesecurity/trufflehog) for more accurate pattern matching and lower false-positive rates.

---

## Webhook Health Checker

Verifies that all configured webhooks on a GitLab group or GitHub org are reachable and returning expected HTTP responses.

```bash
#!/usr/bin/env bash
# webhook-health.sh
# Usage: PLATFORM=github ORG=myorg GITHUB_TOKEN=xxx ./webhook-health.sh
set -euo pipefail

PLATFORM="${PLATFORM:?Set PLATFORM=github or PLATFORM=gitlab}"
TIMEOUT=10
FAILURES=0
TOTAL=0

check_url() {
  local url="$1"
  local code
  code=$(curl -sf -o /dev/null -w "%{http_code}" \
    --max-time "$TIMEOUT" \
    --connect-timeout 5 \
    "$url" 2>/dev/null || echo "000")
  echo "$code"
}

if [[ "$PLATFORM" == "github" ]]; then
  ORG="${ORG:?Set ORG}"
  PAGE=1
  while :; do
    repos=$(curl -sf \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/orgs/$ORG/repos?per_page=100&page=$PAGE" | \
      jq -r '.[].name')
    [[ -z "$repos" ]] && break

    while read -r repo; do
      hooks=$(curl -sf \
        -H "Authorization: Bearer $GITHUB_TOKEN" \
        "https://api.github.com/repos/$ORG/$repo/hooks" | \
        jq -r '.[] | "\(.id) \(.config.url // "no-url") \(.active)"')

      while IFS=' ' read -r id url active; do
        [[ "$url" == "no-url" || -z "$url" ]] && continue
        ((TOTAL++)) || true
        code=$(check_url "$url")
        if [[ "$code" =~ ^(200|204|201|301|302|307|308|404|405)$ ]]; then
          printf "[OK %s]   %s/%s hook %s -> %s\n" "$code" "$ORG" "$repo" "$id" "$url"
        else
          printf "[FAIL %s] %s/%s hook %s -> %s\n" "$code" "$ORG" "$repo" "$id" "$url"
          ((FAILURES++)) || true
        fi
      done <<< "$hooks"
    done <<< "$repos"
    ((PAGE++))
  done

elif [[ "$PLATFORM" == "gitlab" ]]; then
  GITLAB_URL="${GITLAB_URL:-https://gitlab.com}"
  GROUP_ID="${GROUP_ID:?Set GROUP_ID}"

  hooks=$(curl -sf \
    --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB_URL/api/v4/groups/$GROUP_ID/hooks" | \
    jq -r '.[] | "\(.id) \(.url) \(.push_events)"')

  while IFS=' ' read -r id url push; do
    ((TOTAL++)) || true
    code=$(check_url "$url")
    if [[ "$code" =~ ^(200|204|201|301|302|307|308|404|405)$ ]]; then
      printf "[OK %s]   Group hook %s -> %s\n" "$code" "$id" "$url"
    else
      printf "[FAIL %s] Group hook %s -> %s\n" "$code" "$id" "$url"
      ((FAILURES++)) || true
    fi
  done <<< "$hooks"
fi

echo ""
echo "Webhook health check: $TOTAL total, $FAILURES failures"
[[ $FAILURES -gt 0 ]] && exit 1 || exit 0
```

---

## LFS Storage Audit

Reports LFS object sizes, identifies large objects, and checks for orphaned LFS pointers.

```bash
#!/usr/bin/env bash
# lfs-audit.sh
# Usage: REPO_PATH=/path/to/repo ./lfs-audit.sh
set -euo pipefail

REPO_PATH="${REPO_PATH:-.}"
TOP_N="${TOP_N:-20}"

echo "LFS Storage Audit"
echo "Repository: $(realpath $REPO_PATH)"
echo "Generated:  $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "==="

# Check LFS is initialised
if ! git -C "$REPO_PATH" lfs status &>/dev/null; then
  echo "LFS not initialised in this repository."
  exit 0
fi

echo ""
echo "## LFS Objects — Top $TOP_N by Size"
echo ""
git -C "$REPO_PATH" lfs ls-files --size --all 2>/dev/null | \
  awk '{print $NF, $0}' | \
  sort -rh | \
  head -"$TOP_N" | \
  awk '{$1=""; print NR". "$0}' | \
  sed 's/  */ /g'

echo ""
echo "## LFS Storage Summary"
total_bytes=$(git -C "$REPO_PATH" lfs ls-files --size --all 2>/dev/null | \
  awk '{
    match($NF, /([0-9.]+) ([KMGT]?B)/, a)
    size = a[1]
    unit = a[2]
    if (unit == "KB") size *= 1024
    else if (unit == "MB") size *= 1048576
    else if (unit == "GB") size *= 1073741824
    else if (unit == "TB") size *= 1099511627776
    total += size
  } END {print total}')

echo "Total LFS tracked bytes: $(numfmt --to=iec-i --suffix=B $total_bytes 2>/dev/null || echo "${total_bytes} bytes")"
echo "LFS object count: $(git -C "$REPO_PATH" lfs ls-files --all 2>/dev/null | wc -l)"

echo ""
echo "## LFS Tracked File Extensions"
git -C "$REPO_PATH" lfs track 2>/dev/null | grep -v "^Listing" || echo "(none configured)"

echo ""
echo "## Stale LFS Pointers (in history, object may not exist locally)"
git -C "$REPO_PATH" lfs fsck --pointers 2>&1 || true

echo ""
echo "## .gitattributes LFS Configuration"
if [[ -f "$REPO_PATH/.gitattributes" ]]; then
  grep "filter=lfs" "$REPO_PATH/.gitattributes" || echo "(no LFS attributes defined)"
else
  echo ".gitattributes not found"
fi
```

---

## Script Reference Summary

| Script | Purpose | Key Inputs | Safe to Run in Prod |
|--------|---------|------------|---------------------|
| `clone-org-repos.sh` | Clone/update all org repos | `PLATFORM`, `ORG/GROUP_ID`, token | Yes |
| `clean-stale-branches.sh` | Find/delete inactive branches | `REPO_PATH`, `STALE_DAYS` | Yes (DRY_RUN=true default) |
| `commit-activity-report.sh` | Per-author commit stats | `REPO_PATH`, `SINCE` | Yes (read-only) |
| `scan-secrets.sh` | Pattern-match secrets in history | `REPOS_DIR`, `SINCE` | Yes (read-only) |
| `webhook-health.sh` | Check webhook endpoint reachability | `PLATFORM`, `ORG/GROUP_ID`, token | Yes (read-only) |
| `lfs-audit.sh` | LFS object sizes and health | `REPO_PATH` | Yes (read-only) |

> All scripts respect `set -euo pipefail`. Set `DRY_RUN=true` on destructive operations before production use.
