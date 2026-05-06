# Aria Suite Lifecycle Scripts

Automation scripts for LCM target three primary use cases: pre-upgrade validation (confirming disk space, certificate validity, and product health before initiating an upgrade), certificate expiry monitoring (scanning all Locker entries and alerting when within a configurable threshold), and scheduled health checks via the LCM REST API. Scripts use the LCM API base URL `https://<lcm-fqdn>/lcm/lcmservice/api/v2` with Basic or token authentication.

**Certificate expiry monitor (Bash):**
```bash
#!/usr/bin/env bash
# Usage: ./cert-expiry-check.sh <lcm-fqdn> <username> <password> <warn-days>
LCM=$1; USER=$2; PASS=$3; WARN=${4:-30}
TOKEN=$(curl -sk -X POST "https://$LCM/lcm/authz/api/v2/login" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$USER\",\"password\":\"$PASS\"}" | jq -r '.token')
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://$LCM/lcm/locker/api/v2/certificates" | \
  jq --argjson w "$WARN" \
  '.certificates[] | select((.daysToExpiry|tonumber) <= $w) | "\(.alias): \(.daysToExpiry) days"'
```

**Pre-upgrade disk check (Bash):**
```bash
#!/usr/bin/env bash
# Run on LCM appliance as root before any upgrade
for mount in / /data /tmp; do
  used=$(df -h "$mount" | awk 'NR==2{print $5}' | tr -d '%')
  echo "$mount: ${used}% used"
  [[ $used -ge 80 ]] && echo "  WARNING: $mount exceeds 80% — free space before upgrading"
done
```
