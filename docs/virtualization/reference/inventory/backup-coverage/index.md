# VMware Backup Coverage Inventory

| VM Name | Application Owner | Criticality | Backup Policy | Schedule | Retention | Last Successful | Last Restore Test | Notes |
|---|---|---|---|---|---|---|---|---|
| vcenter-prod-01 | infra-team | Critical | File-based (VAMI) | Daily | 7 copies | YYYY-MM-DD | YYYY-MM-DD | — |
| app-prod-01 | app-team | Critical | Daily image | Daily | 30 days | YYYY-MM-DD | YYYY-MM-DD | App-aware |
| app-dev-01 | app-team | Standard | Weekly image | Weekly | 14 days | YYYY-MM-DD | Never | — |

## Coverage Review

- Review backup coverage monthly
- Confirm no critical VMs are unprotected
- Confirm retention meets business or compliance requirements
