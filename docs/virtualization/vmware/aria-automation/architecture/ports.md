---
tags:
  - aria-automation
  - vra
  - networking
  - firewall
  - ports
  - vmware
---
# Aria Automation — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for VMware Aria Automation (formerly vRealize Automation). Covers the Aria Automation appliance cluster, inbound API and UI access, outbound connections to vCenter/NSX/cloud endpoints, and the Aria Suite Lifecycle deployment path.

*Applies to: Aria Automation 8.x / 2403+*
</div>

```text
┌─────────────────────── Aria Automation — Network Traffic Zones ───────────────────────────────────────┐
│                                                                                                       │
│  Consumer Zone              Management Zone                    Infrastructure Zone                    │
│  ──────────────             ────────────────                   ────────────────────                   │
│  Users    ──443──► Aria     Aria Automation ──443──► vCenter   Cloud Accounts: AWS/Azure/GCP ──443    │
│  API calls──443──► Automation (cluster)    ──443──► NSX Mgr    Git ──443──► Aria (pipelines/GitOps)   │
│  CI/CD    ──443──►          Aria SaaS      ──443──► vRO        Aria Orchestrator ──443──► targets     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- Aria Automation deploys as a single appliance or 3-node HA cluster; all nodes share the same VIP — open ports to the VIP and all node IPs
- Aria Automation requires outbound HTTPS to every infrastructure endpoint it manages (vCenter, NSX, cloud providers, Git repos)
- If Aria Orchestrator (vRO) is embedded in Aria Automation (default for 8.x), no separate vRO ports are needed; embedded Orchestrator uses Aria's 443 endpoint
- For Aria Suite deployed via Aria Suite Lifecycle Manager, also see [Aria Suite Lifecycle — Ports](../../aria-suite-lifecycle/architecture/ports/)

---

## Inbound — Client to Aria Automation

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | User browsers, REST API clients, CI/CD tools | Aria Automation UI and REST API (Service Broker, Assembler, Pipelines) |
| 443 | TCP | Aria Suite Lifecycle Manager | Deployment, upgrade, and certificate operations |
| 22 | TCP | Jump hosts | SSH — appliance management and troubleshooting |
| 5480 | TCP | Admin workstations | VAMI appliance management |

---

## Inbound — Aria Automation Cluster (Node-to-Node)

For HA clusters, nodes communicate internally:

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 443 | TCP | Cluster nodes | API communication and VIP handling |
| 5671 | TCP | Cluster nodes | RabbitMQ — inter-service messaging |
| 5672 | TCP | Cluster nodes | RabbitMQ (non-TLS, internal) |
| 6672 | TCP | Cluster nodes | Internal cluster bus |

---

## Outbound — Aria Automation to Infrastructure

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | vCenter Server | Cloud account — VM provisioning, snapshot, tagging |
| 443 | TCP | NSX Manager | NSX cloud account — network segment and security group provisioning |
| 443 | TCP | Aria Orchestrator (if external) | Workflow execution |
| 443 | TCP | vRealize Operations / Aria Operations | Cost and performance integration |
| 443 | TCP | NSX Advanced Load Balancer (if configured) | Load balancer provisioning |

---

## Outbound — Cloud Provider Endpoints

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | *.amazonaws.com | AWS cloud account — EC2, S3, IAM, CloudFormation |
| 443 | TCP | management.azure.com, *.azure.com | Azure cloud account — resource provisioning |
| 443 | TCP | *.googleapis.com | GCP cloud account — Compute Engine, GKE |
| 443 | TCP | *.vmc.vmware.com | VMware Cloud on AWS (VMC) endpoint |

---

## Outbound — Source Control and GitOps

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | GitHub, GitLab, Bitbucket endpoints | GitOps-based pipeline source, blueprint repos (HTTPS clone) |
| 22 | TCP | GitHub, GitLab, Bitbucket endpoints | SSH-based Git clone for pipelines |

---

## Outbound — External Services

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | *.vmware.com, *.broadcom.com | License check, plugin downloads |
| 123 | UDP | NTP server | Time synchronisation |
| 514 | UDP/TCP | Syslog server | Log forwarding |
| 25 | TCP | SMTP relay | Email notifications for catalog requests and approvals |
| 389/636 | TCP | Active Directory DCs | LDAP/LDAPS — user authentication and group sync |
| 88 | TCP/UDP | Active Directory DCs | Kerberos |

---

## Aria Automation to Aria Orchestrator (If External/Standalone)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | Aria Automation | vRO Appliance | Workflow execution API |
| 8281 | TCP | Aria Automation | vRO Appliance | vRO REST API (legacy; 8.x uses 443 primarily) |

---

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| User browsers / API clients | Aria Automation VIP | 443 | Main UI and API entry point |
| Aria Automation | vCenter (all accounts) | 443 | VM lifecycle management |
| Aria Automation | NSX Manager | 443 | Network provisioning |
| Aria Automation | Cloud provider APIs | 443 | AWS, Azure, GCP, VMC |
| Aria Automation | Git repos | 443, 22 | Pipeline source code |
| Aria Automation | Active Directory | 389/636, 88 | User authentication |
| Aria Suite LC Manager | Aria Automation | 443, 5480 | Deployment and lifecycle |

---

## Verify

```bash
# From admin workstation — test Aria Automation API
curl -sk -o /dev/null -w "%{http_code}" https://<aria-automation-fqdn>/csp/gateway/am/api/auth/discovery

# From Aria Automation appliance SSH — test vCenter reachability
curl -sk -o /dev/null -w "%{http_code}" https://<vcenter-fqdn>/rest/com/vmware/cis/session

# From Aria Automation appliance SSH — test NSX Manager reachability
curl -sk -o /dev/null -w "%{http_code}" https://<nsx-manager-ip>/api/v1/cluster/status

# From Aria Automation appliance SSH — test AD LDAP
nc -zv <dc-ip> 636

# From Aria Automation appliance SSH — test NTP
ntpq -p

# Test API token generation (quick functional check)
curl -sk -X POST https://<aria-automation-fqdn>/csp/gateway/am/api/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"<user>","password":"<pass>","domain":"<domain>"}' | python3 -m json.tool | grep '"token"'
```

---

## See also

- [Aria Automation — Architecture](how-it-works/)
- [Aria Automation — Deploy](../deploy/)
- [Aria Automation — Operations](../operations/)
- [Aria Suite Lifecycle — Ports](../../aria-suite-lifecycle/architecture/ports.md)
- [vCenter — Ports](../../vcenter/architecture/ports.md)
- [NSX — Ports](../../nsx/architecture/ports.md)
