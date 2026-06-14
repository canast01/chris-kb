---
tags:
  - terraform
  - automation
  - networking
  - firewall
  - ports
  - iac
---
# Terraform — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Terraform and Terraform Enterprise (TFE). Terraform CLI is a client tool with no listening ports. The relevant rules are outbound from the execution environment to provider APIs, and inbound to TFE when self-hosted.

*Applies to: Terraform CLI 1.x / Terraform Enterprise / HCP Terraform*
</div>

```text
┌──────────────────────────── Terraform — Network Traffic Zones ────────────────────────────────────────┐
│                                                                                                       │
│  CI/CD / DevOps Zone          TFE (self-hosted)               Provider APIs                           │
│  ──────────────────           ────────────────                ─────────────                           │
│  Operators  ──443──► TFE      TFE ──443──► Provider APIs      vCenter, NSX, NetApp, etc. ──443        │
│  Pipelines  ──443──► TFE      TFE ──22──► provisioner targets AWS/Azure/GCP ──443                     │
│                                                                                                       │
│  Standalone CLI: no inbound ports — all connections are outbound from where terraform is executed     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- Standalone Terraform CLI has no listening ports — open only outbound rules from where `terraform apply` runs
- Terraform Enterprise (TFE) is a self-hosted server that needs inbound 443 from operators and CI/CD systems
- Provisioner connections (for `remote-exec`, `file` provisioner) use SSH (22) or WinRM (5986) from TFE or the runner
- All provider plugins connect outbound from the execution host to the provider's API endpoint on 443

---

## Inbound — Admin to Terraform Enterprise (Self-Hosted)

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | Operators, CI/CD pipelines (GitHub, GitLab, Jenkins) | TFE web UI and REST API; VCS webhook receiver |
| 80 | TCP | Clients | HTTP — redirects to 443 |
| 22 | TCP | Jump hosts | TFE OS management (SSH) |

---

## TFE Cluster Internal (Active/Active)

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 443 | TCP | TFE nodes | Inter-node API |
| 8201 | TCP | TFE nodes | Vault HA cluster (if bundled Vault) |
| 5432 | TCP | TFE → PostgreSQL | TFE database (external PostgreSQL) |

---

## Terraform (CLI or TFE) to Provider APIs

All Terraform provider calls are HTTPS outbound to the provider's API endpoint.

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | *.amazonaws.com | AWS provider |
| 443 | TCP | management.azure.com | Azure provider |
| 443 | TCP | *.googleapis.com | GCP provider |
| 443 | TCP | vCenter FQDN | vSphere provider (vCenter API) |
| 443 | TCP | NSX Manager | NSX provider |
| 443 | TCP | NetApp ONTAP cluster mgmt | NetApp ONTAP provider |
| 443 | TCP | Pure FlashArray mgmt | Pure Storage provider |
| 443 | TCP | Vault/HCP Vault | Vault provider for secrets |
| 443 | TCP | GitHub/GitLab | GitHub/GitLab provider |

---

## Terraform Provisioners (remote-exec, file)

When using `remote-exec` or `file` provisioners to configure resources after creation:

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 22 | TCP | TFE / Terraform runner | Newly provisioned Linux VMs | SSH — post-creation configuration |
| 5986 | TCP | TFE / Terraform runner | Newly provisioned Windows VMs | WinRM HTTPS — post-creation configuration |

---

## Outbound — TFE to External Services

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | releases.hashicorp.com, registry.terraform.io | Provider plugin downloads, Terraform CLI updates |
| 443 | TCP | HCP API (app.terraform.io) | HCP Terraform remote state, remote operations |
| 443 | TCP | VCS providers (github.com, gitlab.com) | Webhook delivery, repository access for runs |
| 25 | TCP | SMTP relay | Email notifications |

---

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Operators / CI/CD | TFE | 443 | UI, API, and VCS webhook receiver |
| TFE / Terraform runner | vCenter, AWS, Azure, GCP, etc. | 443 | All provider API calls |
| TFE / runner | Linux provisioned VMs | 22 | remote-exec provisioner |
| TFE / runner | Windows provisioned VMs | 5986 | WinRM provisioner |
| TFE | releases.hashicorp.com | 443 | Provider downloads |
| TFE | VCS (GitHub, GitLab) | 443 | Run triggers, repo access |

---

## Verify

```bash
# From Terraform runner — test vCenter provider endpoint
curl -sk -o /dev/null -w "%{http_code}" https://<vcenter-fqdn>/rest/com/vmware/cis/session

# From Terraform runner — test AWS API endpoint
curl -sk -o /dev/null -w "%{http_code}" https://sts.amazonaws.com/

# From Terraform runner — test TFE API (if using remote backend)
curl -sk -o /dev/null -w "%{http_code}" https://<tfe-hostname>/api/v2/ping

# From Terraform runner — test SSH to a VM that was just created
nc -zv <new-vm-ip> 22

# Simple connectivity test for any provider
terraform plan -var 'test=true' 2>&1 | grep -i "error\|warning\|failed\|timeout" || echo "Plan succeeded"
```

---

## See also

- [Terraform — Architecture](how-it-works/)
- [Terraform — Deploy](../deploy/)
- [Terraform — Operations](../operations/)
- [Ansible — Ports](../../ansible/architecture/ports/)
