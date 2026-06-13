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
┌──────────────────────────────────── Inventory — Support Contracts ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Vendor support contract register: coverage level, expiry dates, escalation contacts      │   │
│   │       Know before an incident: contract number, support level, and how to open a P1 case      │   │
│   │           Renew 90 days before expiry; lapsed support = no access to updates or TAC           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Register Fields                │  │                Support Levels               │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │            Contract / case number            │  │            NBD: next business day           │   │
│   │               Vendor + product               │  │           4h: 4-hour onsite parts           │   │
│   │                Coverage level                │  │             24x7x4: critical SLA            │   │
│   │                 Expiry date                  │  │            Software: patch + TAC            │   │
│   │              TAC contact number              │  │            Premier: named support           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │      Level       │    Parts SLA     │   Support hours   │   Patch access   │     Use case     │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │       NBD        │   Next bus day   │   Business hours  │       Yes        │   Non-critical   │   │
│   │    4h onsite     │     4 hours      │        24x7       │       Yes        │  Business crit   │   │
│   │      24x7x4      │   4h + onsite    │      24x7x365     │       Yes        │   Mission crit   │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    TAC          = Technical Assistance Centre; vendor support portal for raising cases                │
│    NBD          = Next Business Day; parts dispatched by end of next working day                      │
│    EOSL         = End of Service Life; after this date, contract cannot be renewed                    │
│    Case number  = Reference for a support incident; keep for escalation and follow-up                 │
│    SLA breach   = Vendor misses response time; escalate to account manager immediately                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
120 days out → Identify contracts expiring < 90 days; review scope (add/remove CIs)
90 days out  → Request renewal quote from vendor; route to procurement
60 days out  → Quote approved by management; PO raised
30 days out  → PO submitted to vendor; confirmation received
Day 0        → New contract active; update contract register; confirm portal access
```
