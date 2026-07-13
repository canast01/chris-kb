---
tags:
  - reference
description: "| Product | FQDN | Certificate Type | Issuer | Expiration | Owner | Last Renewed | Next Review | |---|---|---|---|---|---|---|---| | vCenter |..."
---
# VMware Certificate Inventory

<div class="kb-summary">
| Product | FQDN | Certificate Type | Issuer | Expiration | Owner | Last Renewed | Next Review | |---|---|---|---|---|---|---|---| | vCenter | vcenter.domain.local | Machine SSL | VMCA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD | | vCenter | vcenter.domain.local | STS |

*Applies to: vSphere 7.x / 8.x*
</div>

| Product | FQDN | Certificate Type | Issuer | Expiration | Owner | Last Renewed | Next Review |
|---|---|---|---|---|---|---|---|
| vCenter | vcenter.domain.local | Machine SSL | VMCA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| vCenter | vcenter.domain.local | STS | Self-signed | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| NSX Manager | nsx.domain.local | API/UI | Custom CA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| Aria Operations | aria-ops.domain.local | Endpoint | Custom CA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| Aria Logs | aria-logs.domain.local | Endpoint | Custom CA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| VxRail Manager | vxrail.domain.local | UI/API | Self-signed | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |

```d2
direction: down

replacement_method_notes: "Replacement Method Notes" {shape: rectangle}
tracking_notes: "Tracking Notes" {shape: rectangle}

replacement_method_notes -> tracking_notes: uses
```

## Replacement Method Notes

- **VMCA-issued** — replace via vSphere Client or VAMI
- **Custom CA** — generate CSR, submit to CA, import signed cert
- **Self-signed** — replace via product UI or CLI

## Tracking Notes

- Review all expiration dates monthly
- Flag anything expiring within 60 days
