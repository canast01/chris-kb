# VMware Certificate Inventory


<div class="kb-summary">
| Product | FQDN | Certificate Type | Issuer | Expiration | Owner | Last Renewed | Next Review | |---|---|---|---|---|---|---|---| | vCenter | vcenter.domain.local | Machine SSL | VMCA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD | | vCenter | vcenter.domain.local | STS | 
</div>

| Product | FQDN | Certificate Type | Issuer | Expiration | Owner | Last Renewed | Next Review |
|---|---|---|---|---|---|---|---|
| vCenter | vcenter.domain.local | Machine SSL | VMCA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| vCenter | vcenter.domain.local | STS | Self-signed | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| NSX Manager | nsx.domain.local | API/UI | Custom CA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| Aria Operations | aria-ops.domain.local | Endpoint | Custom CA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| Aria Logs | aria-logs.domain.local | Endpoint | Custom CA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| VxRail Manager | vxrail.domain.local | UI/API | Self-signed | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |

## Replacement Method Notes

- **VMCA-issued** — replace via vSphere Client or VAMI
- **Custom CA** — generate CSR, submit to CA, import signed cert
- **Self-signed** — replace via product UI or CLI

## Tracking Notes

- Review all expiration dates monthly
- Flag anything expiring within 60 days
