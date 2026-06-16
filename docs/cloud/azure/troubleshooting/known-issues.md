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
┌─────────────────────────────────────────── Microsoft Azure ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        Azure IaaS/PaaS — ARM, VMs, VNet, AKS, Entra ID                        │   │
│   │                         Protocols: HTTPS (Azure Resource Manager API)                         │   │
│   │                   Management: Azure Portal / az CLI / ARM templates / Bicep                   │   │
│   │            ARM template -> Resource Group -> Resource provider -> Deployed resource           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Identity          │  │     Entra ID (Azure AD)     │  │    Tenant-wide directory    │   │
│   │           Compute           │  │           Azure VM          │  │      Scale Sets for HA      │   │
│   │           Network           │  │           VNet/NSG          │  │  Subnet-level segmentation  │   │
│   │             PaaS            │  │      AKS / App Service      │  │   Managed K8s/web hosting   │   │
│   │          Governance         │  │       Subscription/RG       │  │    Quota+policy boundary    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │       ARM        │Deployment engine │       HTTPS       │     Entra ID     │Declarative tmpls │   │
│   │     Entra ID     │Identity provider │     HTTPS/SAML    │   Cond. Access   │   Was Azure AD   │   │
│   │       VNet       │Network isolation │        N/A        │    NSG rules     │Peering supported │   │
│   │       AKS        │   Managed K8s    │       HTTPS       │  Entra ID/RBAC   │Node pools/wkload │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: N/A — Microsoft-managed regions; customer controls logical resources                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ARM            = Azure Resource Manager; deployment/management layer                                 │
│  Resource Group = logical container grouping resources by lifecycle                                   │
│  Entra ID       = Microsoft identity platform, formerly Azure AD                                      │
│  Subscription   = billing+access boundary; quotas apply per subscription                              │
│  NSG            = Network Security Group; stateful firewall on subnets/NICs                           │
│  VNet peering   = private connectivity between two virtual networks                                   │
│  Managed Identity= Entra ID identity auto-assigned to an Azure resource                               │
│  AKS            = Azure Kubernetes Service; managed control plane                                     │
│  Availability Zone= physically separate datacenter within a region                                    │
│  Cond. Access   = Entra ID policy enforcing MFA/device compliance                                     │
│  Service principal= non-human Entra ID identity used by apps/automation                               │
│  ACR            = Azure Container Registry; often paired with AKS                                     │
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
