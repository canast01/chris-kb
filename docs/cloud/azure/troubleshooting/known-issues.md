---
tags:
  - troubleshooting
  - azure
  - cloud
  - known-issues
---
# Microsoft Azure — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Azure bugs, error codes, and workarounds covering ARM, VM provisioning, networking, and Entra ID.

*Applies to: Azure IaaS/PaaS — ARM, VMs, VNet, AKS*
</div>

```text
┌───────────────────────────────────── Cloud Azure Troubleshooting ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                          Azure: Cloud Azure Troubleshooting platform                          │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                   Management: Cloud Azure Troubleshooting management console                  │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Cloud Azure Troubleshooting infrastructure · management network · monitoring             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Troubleshooting platform overview and core concepts               │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Azure errors appear in the portal → Activity Log and in the resource-level Diagnose and solve problems blade.
- `az <resource> show` and `az monitor activity-log list` for CLI diagnostics.
- Check `status.azure.com` for service health incidents before deep troubleshooting.

## ARM / Provisioning

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `QuotaExceeded` during VM deployment | All | Subscription vCPU quota reached for VM family in region | Request quota increase via Portal → Subscriptions → Usage + quotas | N/A |
| `AllocationFailed` for VM size | All | No capacity for requested VM size in region/zone | Try different size, different availability zone, or different region | N/A |
| `ResourceGroupIsNotEmpty` deletion failure | All | Resources still exist in resource group | Delete all child resources first; use `az resource list -g <rg>` to find remaining resources | N/A |

## Entra ID (Azure AD)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `AADSTS70011: Invalid scope` | All | Incorrect OAuth2 scope in token request | Verify scope format: `api://<app-id>/.default` or `https://management.azure.com/.default` | N/A |
| `Conditional Access policy blocking sign-in` | All | Device compliance or MFA policy not satisfied | Complete MFA; enroll device in Intune; contact Azure AD admin for policy exemption | N/A |
| Service principal authentication failing after secret rotation | All | Old client secret cached by application | Update application config with new client secret; restart application | N/A |

## Networking

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| NSG rule change not applying to existing traffic | All | NSG changes apply immediately to new connections; existing sessions use connection tracking | Reconnect sessions to pick up updated NSG rules | N/A |
| `Cannot delete subnet — delegated to service` | All | Subnet delegated to PaaS service (App Service, Container Instances) | Remove service delegation or delete delegated service first | N/A |

## AKS

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| AKS node `NotReady` after upgrade | AKS | Node pool upgrade timed out; node in degraded state | Cordon node; drain; delete node — node pool auto-replaces | N/A |
| `Failed to pull image` from ACR | AKS | AKS cluster identity lacks `AcrPull` role on ACR | Assign role: `az role assignment create --role AcrPull --assignee <aks-identity> --scope <acr-id>` | N/A |

## See also

- [Azure — Common Issues](common-issues.md)
- [AWS — Known Issues](../../aws/troubleshooting/known-issues/)
- [Active Directory — Known Issues](../../../compute/windows-server/active-directory/troubleshooting/known-issues/)
