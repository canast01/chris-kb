---
tags:
  - git
  - operations
---
# Git — Operations Scripts

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


```text title="Expected output"
Cloning: api-service
Cloning: web-frontend
Updating: infrastructure
Cloning: data-pipeline
Updating: auth-service
Cloning: mobile-app
Cloning: documentation
Updating: monitoring-tools
Done. Repositories in: /home/devops/repos
```

!!! warning "Common errors"
    **`curl: (22) The requested URL returned error: 401 Unauthorized`** — Verify that GITHUB_TOKEN or GITLAB_TOKEN environment variable is set and has valid API permissions.
    **`jq: parse error: Invalid numeric literal at line 1 column 10`** — Ensure the API endpoint URL and authentication header names are correct for your platform version.
    **`fatal: could not read Username for 'git@github.com': No such file or directory`** — Configure SSH keys for git authentication or use HTTPS clone URLs instead of SSH URLs.
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

```text title="Expected output"
Secret scan started: 2024-01-15T14:32:47Z
Repos dir: /backup/git
Scanning commits since: 90 days ago
Report: /tmp/secret-scan-20240115-143247.txt

[CLEAN]   infrastructure-core
[FINDING] deployment-automation
[CLEAN]   monitoring-stack
[FINDING] legacy-config-repo
[CLEAN]   terraform-modules
[CLEAN]   ansible-playbooks

Scan complete. Findings: 2
Report written to: /tmp/secret-scan-20240115-143247.txt
```

!!! warning "Common errors"
    **`fatal: not a git repository (or any of the parent directories): .git`** — Ensure all subdirectories in `$REPOS_DIR` are valid bare Git repositories with `.git` directories at the expected depth.
    **`Set REPOS_DIR`** — Export the `REPOS_DIR` environment variable before running the script (e.g., `export REPOS_DIR=/backup/git`).
    **`grep: Invalid regular expression`** — Escape special regex characters in the `PATTERNS` array or use `grep -F` for literal string matching instead of regex patterns.
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

```text title="Expected output"
[OK 200]   myorg/api-service hook 12847291 -> https://webhook.internal.io/github/push
[OK 200]   myorg/web-frontend hook 12847292 -> https://webhook.internal.io/github/push
[OK 200]   myorg/data-pipeline hook 12847293 -> https://events.company.net/ingest
[FAIL 000] myorg/legacy-app hook 12847294 -> https://webhook.old-server.local/receive
[OK 404]   myorg/docs hook 12847295 -> https://webhook.internal.io/github/deprecated
[OK 200]   myorg/infra-config hook 12847296 -> https://webhook.internal.io/github/push

Webhook health check: 6 total, 1 failures
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host: api.github.com`** — Verify network connectivity and DNS resolution; check if a corporate proxy or firewall is blocking GitHub API access.
    **`jq: parse error: Invalid JSON text at line 1`** — Ensure the GITHUB_TOKEN or GITLAB_TOKEN is valid and has appropriate API scopes (repo:read_hook or api).
    **`[FAIL 000] ... hook ... -> https://webhook.internal.io/...`** — Verify the webhook endpoint is reachable from the CI/CD runner's network, check firewall rules, and confirm the target service is running.
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

```d2
direction: down

verify: "Verify" {shape: rectangle}

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

- [Git — Procedures](../procedures/)
- [Git — CLI Reference](../cli-reference/)
- [Git — Health Checks](../health-checks/)
