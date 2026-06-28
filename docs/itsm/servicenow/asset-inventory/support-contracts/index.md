---
tags:
  - servicenow
---
# Inventory — Support Contracts

```bash
# Query contract CSV for near-expiry items
# Columns: Vendor,Product,ContractNumber,ExpiryDate,RenewalOwner,SLATier
awk -F',' 'NR>1 {
  cmd = "date -d \"" $4 "\" +%s"
  cmd | getline expiry; close(cmd)
  days = int((expiry - systime()) / 86400)
  if (days < 90 && days >= 0) printf "EXPIRING: %s | %s | %d days | Owner: %s\n", $1, $2, days, $5
  if (days < 0) printf "EXPIRED: %s | %s | %d days ago | Owner: %s\n", $1, $2, -days, $5
}' support-contracts.csv
```

```text
120 days out → Identify contracts expiring < 90 days; review scope (add/remove CIs)
90 days out  → Request renewal quote from vendor; route to procurement
60 days out  → Quote approved by management; PO raised
30 days out  → PO submitted to vendor; confirmation received
Day 0        → New contract active; update contract register; confirm portal access
```
