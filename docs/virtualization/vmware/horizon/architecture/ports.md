---
tags:
  - horizon
  - vdi
  - networking
  - firewall
  - ports
  - blast
  - pcoip
---
# Horizon — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for VMware Horizon. Covers client-to-Connection Server, display protocol traffic (Blast Extreme and PCoIP), USB/CDR redirection, Connection Server cluster and inter-pod, and Horizon infrastructure to vCenter/Active Directory.

*Applies to: Horizon 8 (2111+) / Horizon 2312+*
</div>

```text
┌───────────────────────── Horizon — Network Traffic Zones ─────────────────────────────────────────────┐
│                                                                                                       │
│  Client Zone                  DMZ (UAG/GSS)              Internal Network                             │
│  ─────────────               ────────────                ────────────────                             │
│  Horizon Client ──443───────► Unified Access  ──443─────► Connection Server                           │
│  (any device)   ──22443 UDP──► Gateway (UAG)  ──22443 UDP──► Horizon Agent (VMs)                      │
│                  ──4172 UDP──►                ──4172 UDP──► Horizon Agent (VMs)                       │
│                                                                                                       │
│  Without UAG (internal clients only):                                                                 │
│  Horizon Client ──443──► Connection Server ──22443/4172──► Horizon Agent (desktop/RDSH VMs)           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- In most deployments, external clients connect to the Unified Access Gateway (UAG) in the DMZ — not directly to Connection Servers
- If using UAG, open ports in two stages: client → UAG (external firewall) and UAG → Connection Server/Agents (internal firewall)
- PCoIP is UDP 4172 — TCP 4172 is used as a fallback only; UDP 4172 should be the primary rule
- Blast Extreme (22443) is the recommended display protocol for Horizon 7+ and is preferred over PCoIP for most deployments
- USB redirection (32111) and CDR/MMR (9427) are optional — disable if the security policy does not permit peripheral redirection

---

## Inbound — Horizon Client to Unified Access Gateway (UAG) — External Firewall

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | Horizon clients | UAG external IP | HTTPS — session authentication and XMLAPI tunnelling |
| 8443 | TCP | Horizon clients | UAG external IP | Blast Extreme alternate HTTPS port (fallback for 443-blocked environments) |
| 22443 | TCP/UDP | Horizon clients | UAG external IP | Blast Extreme display protocol (primary) |
| 4172 | TCP/UDP | Horizon clients | UAG external IP | PCoIP display protocol |
| 9427 | TCP | Horizon clients | UAG external IP | MMR and CDR — multimedia redirection and client drive redirection |
| 32111 | TCP | Horizon clients | UAG external IP | USB device redirection |

---

## UAG to Connection Server — Internal Firewall

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | UAG | Connection Server | Session management and tunnelling (blast secured through CS) |
| 8443 | TCP | UAG | Connection Server | JMS SSL — Horizon message bus |
| 4001 | TCP | UAG | Connection Server | JMS — Horizon message bus (non-SSL, internal use) |
| 22443 | TCP/UDP | UAG | Horizon Agent VMs | Blast Extreme display protocol direct (UAG → VM; bypasses CS for data) |
| 4172 | TCP/UDP | UAG | Horizon Agent VMs | PCoIP direct (UAG → VM) |
| 9427 | TCP | UAG | Horizon Agent VMs | CDR/MMR |
| 32111 | TCP | UAG | Horizon Agent VMs | USB |

---

## Direct (Internal Clients — No UAG)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | Horizon clients | Connection Server | HTTPS — authentication and session |
| 8443 | TCP | Horizon clients | Connection Server | JMS SSL — message bus |
| 22443 | TCP/UDP | Horizon clients | Horizon Agent VMs | Blast Extreme display |
| 4172 | TCP/UDP | Horizon clients | Horizon Agent VMs | PCoIP display |
| 9427 | TCP | Horizon clients | Horizon Agent VMs | CDR/MMR |
| 32111 | TCP | Horizon clients | Horizon Agent VMs | USB |

---

## Connection Server to Horizon Agent (Desktop / RDSH VMs)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 4001 | TCP | Connection Server | Horizon Agent VM | JMS — heartbeat and message bus |
| 4002 | TCP | Connection Server | Horizon Agent VM | JMS SSL |
| 22443 | TCP | Connection Server | Horizon Agent VM | Blast Extreme session setup |
| 3389 | TCP | Connection Server | Horizon Agent VM | RDP (Horizon uses RDP for MMR/CDR in some configurations) |

---

## Connection Server — Infrastructure

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | Connection Server | vCenter Server | vCenter API — VM inventory, power operations, snapshot/linked-clone management |
| 389 | TCP | Connection Server | Active Directory DCs | LDAP — user and group lookup |
| 636 | TCP | Connection Server | Active Directory DCs | LDAPS (recommended) |
| 88 | TCP/UDP | Connection Server | Active Directory DCs | Kerberos (SSO pass-through) |
| 3268 | TCP | Connection Server | Active Directory DCs | Global Catalog |
| 443 | TCP | Connection Server | Composer Server (if using Composer) | View Composer API — linked clone operations |

---

## Connection Server Cluster (Pod — Inter-CS)

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 22389 | TCP | Connection Server ↔ Connection Server | LDAP replication between pod members |
| 22636 | TCP | Connection Server ↔ Connection Server | LDAPS replication (recommended) |
| 4100 | TCP | Connection Server ↔ Connection Server | JMS cluster bus |
| 4101 | TCP | Connection Server ↔ Connection Server | JMS cluster bus SSL |

---

## Cloud Pod Architecture (CPA — Multi-Pod / Multi-Site)

When Horizon CPA links multiple pods:

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 22389 | TCP | Connection Server (pod A) ↔ Connection Server (pod B) | Inter-pod LDAP replication |
| 22636 | TCP | Connection Server (pod A) ↔ Connection Server (pod B) | Inter-pod LDAPS |
| 443 | TCP | Connection Server (pod A) ↔ Connection Server (pod B) | Global Entitlement Layer (GEL) API |

---

## Horizon to Licensing and Updates (Outbound)

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | *.vmware.com, *.broadcom.com | License activation, update check |
| 443 | TCP | ws1.omnissa.com | Horizon license check (post-Broadcom split) |

---

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Horizon clients (external) | UAG (DMZ) | 443, 8443, 22443 TCP/UDP, 4172 TCP/UDP | Main external firewall rules |
| UAG | Connection Server | 443, 8443, 4001 | Internal firewall — UAG to CS |
| UAG | Horizon Agent VMs | 22443 TCP/UDP, 4172 TCP/UDP, 9427, 32111 | Direct data path UAG → VM |
| Horizon clients (internal) | Connection Server | 443, 8443 | Internal client authentication |
| Horizon clients (internal) | Horizon Agent VMs | 22443, 4172 | Display protocol direct |
| Connection Server | vCenter | 443 | VM lifecycle management |
| Connection Server | Active Directory | 389/636, 88 | User authentication |
| CS ↔ CS (cluster) | CS ↔ CS (cluster) | 22389, 22636, 4100, 4101 | Pod replication |

---

## Verify

```bash
# From admin workstation — test Connection Server web
curl -sk -o /dev/null -w "%{http_code}" https://<connection-server-ip>/broker/xml

# From Horizon Client workstation — test Blast port (UDP)
nc -zu <agent-vm-ip> 22443

# From Horizon Client workstation — test PCoIP port (UDP)
nc -zu <agent-vm-ip> 4172

# From Connection Server — test vCenter API
nc -zv <vcenter-ip> 443

# From Connection Server — test AD LDAP
nc -zv <dc-ip> 389
nc -zv <dc-ip> 636

# From UAG — test Connection Server reachability
curl -sk -o /dev/null -w "%{http_code}" https://<connection-server-ip>/broker/xml
```

---

## See also

- [Horizon — Architecture](how-it-works/)
- [Horizon — Deploy](../deploy/)
- [Horizon — Operations](../operations/)
- [Horizon — Troubleshooting](../troubleshooting/)
- [vCenter — Ports](../../vcenter/architecture/ports/)
