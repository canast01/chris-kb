# Superna Eyeglass — Scripts

Automation scripts for Eyeglass cover SyncIQ health checking, RPO compliance reporting, automated pre-failover validation, and post-failover validation using the Eyeglass REST API. Scripts are typically written in Python or Bash and executed from a management jump host with network access to both the Eyeglass appliance and the PowerScale clusters.

| Script | Language | Purpose |
|---|---|---|
| `synciq-health-check.py` | Python | Query Eyeglass REST API for all policy states; alert on failures |
| `rpo-compliance-report.py` | Python | Export RPO compliance per SyncIQ policy with lag metrics |
| `pre-failover-validation.sh` | Bash | Run automated pre-failover checks: DR readiness score, DNS, quotas |
| `post-failover-validation.py` | Python | Validate shares accessible, quotas applied, DNS resolved at DR site |

**Example: pre-failover validation (Bash)**

```bash
#!/bin/bash
EYEGLASS_HOST="eyeglass-dr.example.com"
API_TOKEN="$EYEGLASS_API_TOKEN"

# Check DR readiness score
score=$(curl -sk -H "Authorization: Bearer $API_TOKEN" \
  "https://$EYEGLASS_HOST/api/v1/dr/readiness" | jq '.score')

if [ "$score" -lt 100 ]; then
  echo "ERROR: DR readiness score is $score — failover blocked."
  exit 1
fi
echo "DR readiness score: $score — proceeding."
```
