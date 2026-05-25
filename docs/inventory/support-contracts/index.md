# Support Contract Tracking

Maintain visibility of vendor support agreements to ensure infrastructure components remain covered and renewals are actioned before expiry.

```text
┌──────────────────────────────────────────────────────────────┐
│                     Contract Register                        │
│  Vendor │ Product │ SLA Tier │ Expiry │ Renewal Owner        │
└─────────────────────────────┬────────────────────────────────┘
                              │
         ┌────────────────────┼───────────────────┐
         ▼                    ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐
│  >120 days out  │  │  90 days out    │  │  <30 days out      │
│                 │  │                 │  │                    │
│ Review scope    │  │ Request quote   │  │ Submit PO          │
│ add/remove CIs  │  │ route to proc.  │  │ confirm coverage   │
└─────────────────┘  └────────┬────────┘  └──────────────────┘
                              │                   │
                              ▼                   ▼
                    ┌──────────────────┐  ┌──────────────────┐
                    │  Approve quote   │  │  New contract    │
                    │  (management)    │  │  active → update │
                    └──────────────────┘  │  register        │
                                          └──────────────────┘
```

## Contract Register — Key Fields

| Field | Description |
|---|---|
| Vendor | Company providing support |
| Product / CI | Specific hardware or software covered |
| Contract type | Hardware support / software maintenance / SaaS subscription |
| Contract number | Vendor reference |
| Start date | Coverage begins |
| Expiry date | Coverage ends |
| SLA tier | Standard / Premium / 24×7 / NBD |
| Annual cost | For budget forecasting |
| Renewal owner | Who must action renewal |
| Vendor TAM / CSM | Technical Account Manager contact |
| Support portal URL | Where to raise cases |

## Expiry Monitoring

### Contracts Expiring Within 90 Days

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

## Support Tier Reference

| Tier | Response Time | Hours | Typical Use |
|---|---|---|---|
| 24×7 Critical | < 1 hour | 24×7×365 | Production storage, network core, DR systems |
| 24×7 Standard | < 4 hours | 24×7×365 | Production compute, databases |
| Business hours | Next business day | Mon–Fri 9–5 | Dev/test, non-critical systems |
| Self-service | No SLA | Online portal | Internal tooling, low-risk systems |

## Opening a Support Case

```bash
# Generic: note the following before calling/opening a ticket:
# - Contract number / serial number
# - Product version and build
# - Affected hostname(s) and IPs
# - Symptoms: what is failing and since when
# - Logs: collect before calling (see platform-specific runbooks)

# NetApp — collect AutoSupport bundle
system node autosupport invoke -type all -message "Opening case XXXXX"

# VMware — collect vm-support bundle
vm-support -w /tmp -b

# Cisco TAC — collect 'show tech-support' output
# (varies by device — run before opening case)
```

## Warranty / Support Status Checks

```bash
# Dell hardware — using Dell TechDirect API or iDRAC
racadm getsvctag   # get service tag from iDRAC

# Check warranty on Dell support site (requires service tag)
curl -s "https://apidirect.dell.com/Contracts/v2/contracts?servicetag=<tag>" \
  -H "X-BAPI-Key: <api-key>" | jq '.contracts[] | {entitlement:.entitlementType,end:.endDate}'

# HPE iLO — show contract info
# HPSUM or OneView shows warranty; or use:
# curl https://warranty.hpe.com/CountryLanguageStore/wc/country/<country>/language/EN/contract/serial/<serial>
```

## Renewal Process

```text
120 days out → Identify contracts expiring < 90 days; review scope (add/remove CIs)
90 days out  → Request renewal quote from vendor; route to procurement
60 days out  → Quote approved by management; PO raised
30 days out  → PO submitted to vendor; confirmation received
Day 0        → New contract active; update contract register; confirm portal access
```

## Support Contract Checklist

- [ ] All production systems have active support coverage
- [ ] No contracts expired without renewal
- [ ] Contracts expiring within 90 days have renewal in progress
- [ ] Vendor portal credentials are current (not tied to departed staff)
- [ ] Hardware serial numbers match contract CIs (no uncovered devices)
- [ ] Support tier is appropriate for each system's criticality
- [ ] Budget line item confirmed for next renewal cycle

## Escalation Contacts

| Vendor | Escalation Path |
|---|---|
| Microsoft | Azure Unified Support: `aka.ms/supportrequest`; Premier escalation via TAM |
| AWS | Support console → Severity A; Account Manager for major issues |
| VMware (Broadcom) | My VMware portal → Support Request; TAM for severity 1 |
| NetApp | NetApp Support Site; call 1-888-4-NETAPP for P1 |
| Pure Storage | `support.purestorage.com`; call hotline for P1 |
| Cisco | `tools.cisco.com/ServiceRequestTool`; TAC call for P1/P2 |
