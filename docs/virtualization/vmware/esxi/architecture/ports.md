---
tags:
  - esxi
  - networking
  - firewall
  - ports
  - vsphere
  - vsphere-7
  - vsphere-8
---
# ESXi — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for VMware ESXi hosts. Covers management, VM console, vMotion, Fault Tolerance, storage, and NSX overlay traffic. Use this when building firewall change requests for host onboarding or network re-segmentation.

*Applies to: ESXi 7.x / 8.x*
</div>

```text
┌──────────────────────────────── ESXi — Network Traffic Zones ─────────────────────────────────────────┐
│                                                                                                       │
│  Management Zone          ESXi Host VMkernels                  Storage / Overlay Zone                 │
│  ────────────────          ─────────────────────                ─────────────────────                 │
│  vCenter    ──902/443──► Management vmk0 ──8000──► vMotion vmk  3260──► iSCSI SAN                     │
│  Admin SSH  ──22───────►                 ──2233──► FT vmk       2049──► NFS                           │
│  VMRC       ──903───────►                ──6081 UDP─► NSX TEP   4420──► NVMe-oF/TCP                   │
│  Backup     ──902───────►                                                                             │
│                                                                                                       │
│  Each traffic type uses a dedicated VMkernel adapter on its own VLAN — never share vMotion with mgmt  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- ESXi has a built-in stateful firewall managed by `esxcli network firewall`; port table below reflects permitted directions from ESXi's perspective
- Each VMkernel adapter (management, vMotion, vSAN, FT, NSX TEP) should be on a dedicated VLAN
- Firewall rules between ESXi hosts (vMotion, FT, vSAN) are typically on a trusted internal network with no perimeter firewall — document any L3 boundary explicitly in the CR

---

## Inbound — Management Traffic to ESXi

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | vCenter Server | vCenter → ESXi HTTPS API (host management) |
| 902 | TCP | vCenter Server | vmware-authd — required for vCenter to manage the host |
| 902 | TCP | Backup proxies | VADP — vStorage API for Data Protection |
| 903 | TCP | Admin workstations | VM Remote Console (VMRC) |
| 22 | TCP | Jump hosts | SSH — disable in production unless actively needed |
| 161 | UDP | Monitoring systems | SNMP polling |
| 5988 | TCP | IPMI/monitoring | CIM/WBEM (hardware monitoring — read-only) |
| 5989 | TCP | IPMI/monitoring | CIM/WBEM over HTTPS |
| 80 | TCP | Clients | HTTP — redirects to 443 |

---

## Outbound — ESXi to Infrastructure

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 123 | UDP | NTP servers | Time synchronisation |
| 514 | UDP/TCP | Syslog server | Log forwarding |
| 162 | UDP | SNMP trap receiver | SNMP traps |
| 443 | TCP | vCenter Server | Host → vCenter (reverse agent channel, vSAN witness, etc.) |

---

## vMotion (ESXi to ESXi)

vMotion traffic moves live VMs between hosts. Must traverse the vMotion VMkernel network, not the management network.

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 8000 | TCP | ESXi hosts (vMotion VMkernel) | vMotion — VM memory and state transfer |

---

## Fault Tolerance (ESXi to ESXi)

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 2233 | TCP | ESXi hosts (FT VMkernel) | FT logging — continuous synchronisation between primary and secondary VMs |

---

## vSAN Traffic (ESXi to ESXi)

vSAN requires a dedicated VMkernel adapter. If vSAN traffic crosses L3 (stretched cluster, witness), open these ports on intervening firewalls.

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 12345 | UDP | vSAN VMkernel adapters | CMMDS — cluster membership and metadata |
| 12346 | UDP | vSAN VMkernel adapters | CMMDS — unicast heartbeat |
| 2233 | TCP | vSAN VMkernel adapters | RDT — Reliable Datagram Transport (vSAN I/O) |

See [vSAN — Ports](../../vsan/architecture/ports/) for witness appliance and stretched cluster port requirements.

---

## NSX Overlay (ESXi as Transport Node)

When ESXi hosts participate in NSX-T as transport nodes, TEP (Tunnel Endpoint) traffic uses:

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 6081 | UDP | TEP VMkernel to TEP VMkernel | Geneve encapsulation — overlay network traffic |

TEP VMkernel adapters must be on a routed network (or same L2) that reaches other TEPs and NSX Edge TEPs.

---

## Storage Protocols

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 3260 | TCP | ESXi iSCSI VMkernel | iSCSI target (SAN) | iSCSI block storage |
| 2049 | TCP | ESXi NFS VMkernel | NAS server | NFS v3/v4 datastore |
| 111 | TCP/UDP | ESXi NFS VMkernel | NAS server | rpcbind (NFS portmapper) |
| 4420 | TCP | ESXi NVMe VMkernel | NVMe-oF/TCP target | NVMe over TCP (ESXi 7.0+) |

---

## vSphere Replication

| Port | Protocol | Source/Destination | Purpose |
|---|---|---|---|
| 31031 | TCP | vSphere Replication appliance → ESXi | Replication data transfer |
| 44046 | TCP | ESXi host → vSphere Replication | Replication incoming port (secondary site) |

---

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| vCenter | ESXi hosts | 902, 443 | Core management — required everywhere |
| Admin clients | ESXi | 903, 22 | VMRC and SSH — jump host only |
| Backup proxies | ESXi | 902 | VADP for backup |
| ESXi hosts | ESXi hosts (vMotion) | 8000 | Dedicated VLAN, typically no firewall |
| ESXi hosts | ESXi hosts (FT) | 2233 | Dedicated VLAN |
| ESXi hosts | ESXi hosts (vSAN) | 12345 UDP, 12346 UDP, 2233 TCP | Dedicated VLAN; add to CR if L3 |
| ESXi TEP | ESXi/Edge TEP | 6081 UDP | NSX overlay; all transport nodes |
| ESXi iSCSI vmk | iSCSI SAN | 3260 | Per iSCSI VLAN |
| ESXi NFS vmk | NAS | 2049, 111 | Per NFS VLAN |

---

## Verify

```bash
# From vCenter or jump host — test management ports on ESXi host
nc -zv esxi01.corp.local 443
nc -zv esxi01.corp.local 902

# From ESXi SSH — test NTP
esxcli network ip connection list | grep 123
ntpq -p

# From ESXi SSH — view ESXi firewall rules
esxcli network firewall get
esxcli network firewall ruleset list

# From ESXi SSH — test iSCSI target reachability
esxcli iscsi networkportal list
nc -zv <iscsi-target-ip> 3260

# From ESXi SSH — test vMotion connectivity
vmkping -I vmk1 <destination-esxi-vmk1-ip>
```

---

## See also

- [vCenter — Ports](../../vcenter/architecture/ports/)
- [vSAN — Ports](../../vsan/architecture/ports/)
- [NSX — Ports](../../nsx/architecture/ports/)
- [ESXi — Architecture](how-it-works/)
- [ESXi — Deploy](../../esxi/deploy/)
