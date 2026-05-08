# Venafi — Access Control

Least-privilege role assignment should be enforced, with service account permissions scoped to specific policy folders only. Separation of duties separates CA trust anchor management from day-to-day certificate operations.

| Control | Detail |
|---|---|
| RBAC roles | Policy Master, Certificate Manager, Approver — scoped to policy folders |
| Separation of duties | CA trust anchor management separated from day-to-day certificate operations |
| Admin account review | Quarterly review of Venafi admin and service accounts |
