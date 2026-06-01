# Venafi — Authentication


<div class="kb-summary">
Venafi RBAC is managed through built-in roles: Policy Master (full policy tree control), Certificate Manager (issue, renew, revoke within assigned folders), and Approver (approve or reject certificate requests without issuing).
</div>

 API keys must be rotated on a defined schedule and immediately upon personnel change.

| Control | Detail |
|---|---|
| RBAC roles | Policy Master, Certificate Manager, Approver — scoped to policy folders |
| API key rotation | Rotate on schedule and on personnel change; store in secrets manager |
| Admin account review | Quarterly review of Venafi admin and service accounts |
