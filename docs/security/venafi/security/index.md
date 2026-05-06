# Venafi Security

Venafi RBAC is managed through built-in roles: Policy Master (full policy tree control), Certificate Manager (issue, renew, revoke within assigned folders), and Approver (approve or reject certificate requests without issuing). Least-privilege role assignment should be enforced, with service account permissions scoped to specific policy folders only.

All certificate lifecycle events are captured in the Venafi audit log and should be forwarded to a SIEM via the Log Server. HSM integration protects the CA private keys and Venafi service credentials. API keys must be rotated on a defined schedule and immediately upon personnel change.

| Control | Detail |
|---|---|
| RBAC roles | Policy Master, Certificate Manager, Approver — scoped to policy folders |
| Audit log | All lifecycle events logged; forward to SIEM via Log Server |
| HSM integration | Private key protection for CA trust anchors and Venafi credentials |
| Certificate pinning | Policy enforcement for pinned certificate use cases |
| Separation of duties | CA trust anchor management separated from day-to-day certificate operations |
| API key rotation | Rotate on schedule and on personnel change; store in secrets manager |
| Admin account review | Quarterly review of Venafi admin and service accounts |
