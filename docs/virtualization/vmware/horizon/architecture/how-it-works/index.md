# Horizon — How It Works


<div class="kb-summary">
How It Works reference covering Component Overview, Connection Flow, Blast Extreme vs PCoIP, Session Broker Role, Security Server Deprecation and 1 more sections.
</div>

## Component Overview

VMware Horizon is a broker-based VDI and published application delivery platform. The core components and their relationships:

| Component | Role | Location |
|---|---|---|
| Connection Server | Session broker, authenticates users, assigns desktops | Windows Server, domain-joined |
| Unified Access Gateway (UAG) | Reverse proxy for external access, terminates Blast/PCoIP | DMZ, Linux appliance |
| vCenter Server | VM lifecycle management (provision, power, snapshot) | Management network |
| Active Directory | User authentication, group policy, entitlement groups | Existing infrastructure |
| Horizon Agent | In-guest component enabling remoting protocols and redirection | Each desktop VM or RDS host |
| Horizon Client | End-user client connecting to desktops | Endpoint (Windows, macOS, Linux, mobile, HTML5) |
| App Volumes Manager | Application layering — attaches AppStacks (VMDKs) at login | Windows Server + SQL DB |
| DEM (Dynamic Environment Manager) | User environment management — policies, profile migration, drive maps | Windows Server, GPO-driven |
| Composer (deprecated) | Linked-clone pool management | Replaced by Instant Clone Engine |

### Component Interaction Diagram (text)

```text
[User Endpoint]
     |
  Horizon Client
     |
  (external)     (internal)
     |                |
  [UAG - DMZ]    [Connection Server]
     |                |
     +----> [Connection Server] <----> [Active Directory]
                    |
              [vCenter Server]
                    |
         +----------+-----------+
         |                      |
   [ESXi Hosts]          [App Volumes Mgr]
   [Desktop VMs]               |
   [Horizon Agent]       [AppStack VMDKs]
         |
   [DEM Config Share] <-- GPO applies DEM Agent
```
┌──────────────────────────────────── VMware Horizon — How It Works ────────────────────────────────────┐
│                                                                                                       │
│  Horizon delivers virtualised desktops and apps via Connection Servers that broker                    │
│  sessions between clients and desktop pools or RDS farms.                                             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Session Broker Layer             │  │             Desktop & App Layer             │   │
│   │          Connection Server: broker           │  │             Instant clone pools             │   │
│   │             Authenticates via AD             │  │        Full clone pools (persistent)        │   │
│   │          Selects resource from pool          │  │            RDS: App/Desktop farms           │   │
│   │         Blast Extreme: display prot          │  │               GPUs: vGPU pools              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Connection Server brokers AD auth then hands session to pool agent on target VM.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Client Layer                 │  │            Unified Access Gateway           │   │
│   │          Horizon Client: native app          │  │            UAG: DMZ reverse proxy           │   │
│   │             HTML Access: browser             │  │            Offloads external auth           │   │
│   │            Blast TCP/UDP 8443/443            │  │          SAML to Connection Server          │   │
│   │            PCoIP: legacy protocol            │  │         Dual NIC: internal+external         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Connection Servers run as Windows VMs; desktop VMs run on ESXi hosts with vSAN                       │
│  or NFS storage; UAG VMs sit in DMZ with dual-NIC on separate networks.                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Connection Server= Windows Server VM; Horizon broker and management                                  │
│  Instant clone   = desktop provisioned in seconds from parent snapshot                                │
│  Full clone      = independent persistent VM; slow to provision                                       │
│  RDS             = Remote Desktop Services; server-based desktop/app                                  │
│  UAG             = Unified Access Gateway; replaces Security Server                                   │
│  Blast Extreme   = VMware display protocol; lower latency than PCoIP                                  │
│  PCoIP           = PC over IP; legacy display protocol; UDP-based                                     │
│  HTML Access     = browser-based Horizon client; uses WebSocket                                       │
│  SAML            = assertion from UAG to Connection Server for auth                                   │
│  vGPU            = NVIDIA GPU partition shared across desktop VMs                                     │
│  Pool            = collection of desktops with same policy                                            │
│  Farm            = collection of RDS hosts for app/desktop delivery                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

**Customization at fork:** A post-customization script (`horizon-customization.ps1` or sysprep alternative) runs in each child VM immediately after the fork to:
- Set a unique hostname (based on naming pattern defined in pool)
- Join domain (using Instant Clone Domain Join — a cached machine account)
- Remove previous user's profile data if persistent profile not in use

### Full Clone Pools

Full Clone pools provision independent VMs from a vCenter template. Each VM is a complete, independent copy.

- Suitable for persistent desktops where users expect to "own" their VM
- Higher storage consumption — no shared base disk
- Slower provisioning (full VM deploy from template)
- VM persists across sessions; user data survives logoff
- Managed via vCenter snapshot for OS-level updates (manual or automated maintenance)

### RDS Published Applications and Desktops

RDS (Remote Desktop Services) Farms host Windows Server (with Desktop Experience or not) with Horizon Agent in RDS mode. Multiple users share a single Windows Server OS instance.

- **Published Applications:** Individual apps (e.g., Internet Explorer, legacy apps) streamed to client
- **Published Desktops:** Full RDS desktop session
- Multiple RDS hosts form a **Farm**; a Farm backs a **Published Application Pool** or **Published Desktop Pool**
- Load balancing across farm members is handled by Connection Server

| Feature | Instant Clone Pool | Full Clone Pool | RDS Farm |
|---|---|---|---|
| Isolation | Per-user VM | Per-user VM | Shared OS, per-session |
| State | Stateless (default) | Persistent | Stateless |
| Provisioning speed | Seconds | Minutes | N/A (persistent hosts) |
| Storage efficiency | High (shared base) | Low | Highest (many users per VM) |
| User persona | Task/knowledge worker | Power user, persistent | Published app, high-density |

---

## Connection Flow

### Internal Client (LAN)

```text
1. User opens Horizon Client → enters Connection Server FQDN
2. Horizon Client → HTTPS (443) → Connection Server
3. Connection Server authenticates user against AD (Kerberos/LDAP)
4. Connection Server checks entitlements (AD group → pool mapping)
5. Connection Server selects an available desktop (or provisions new Instant Clone)
6. Connection Server instructs vCenter to power on / assign VM
7. Connection Server returns IP/FQDN + session ticket to client
8. Client establishes Blast Extreme (TCP 8443 / UDP 8443) or PCoIP (TCP 4172 / UDP 4172) directly to VM
9. Horizon Agent in VM validates ticket, establishes session
```

### External Client via UAG

```text
1. User opens Horizon Client → enters UAG external FQDN
2. Horizon Client → HTTPS (443) → UAG (DMZ)
3. UAG forwards authentication request → Connection Server (internal, 443)
4. Authentication + entitlement check on Connection Server
5. Connection Server returns session ticket to UAG
6. UAG returns connection details to client
7. Client establishes Blast Extreme (TCP 8443 / UDP 8443) → UAG
8. UAG proxies display protocol traffic → Horizon Agent in VM
   (UAG acts as a Blast/PCoIP proxy — client never directly reaches internal VM)
```

**Ports summary:**

| Port | Protocol | Purpose |
|---|---|---|
| 443 | TCP | HTTPS — client to Connection Server or UAG |
| 8443 | TCP/UDP | Blast Extreme (primary) |
| 4172 | TCP/UDP | PCoIP |
| 22443 | TCP/UDP | Blast Extreme (alternative, used via UAG) |
| 32111 | TCP | USB redirection (client to agent) |
| 9427 | TCP | MMR (Multimedia Redirection) and CDR (Client Drive Redirection) |

---

## Blast Extreme vs PCoIP

| Feature | Blast Extreme | PCoIP |
|---|---|---|
| Protocol basis | H.264 / H.265 / VP9 video codec over WebRTC-like transport | Proprietary VMware/Teradici codec |
| Transport | TCP 8443 or UDP 8443 (adaptive) | TCP 4172 + UDP 4172 |
| HTML5 browser client support | Yes (Horizon HTML Access) | No |
| Codec hardware acceleration | Yes (server-side and client-side GPU acceleration) | Limited |
| Bandwidth adaptability | Excellent — adapts to available bandwidth | Good |
| Latency sensitivity | Lower latency on UDP path | Higher latency than Blast UDP |
| 3D/OpenGL workloads | Supported with vGPU | Supported with vGPU |
| Recommended for | All new deployments | Legacy or where Teradici zero clients are in use |
| Encryption | AES-128 or AES-256 (configurable via GPO) | AES-128 via TLS |

**Blast Extreme adaptive transport:** When UDP 8443 is available, Blast uses UDP for lower latency. When UDP is blocked (e.g., strict firewalls), it falls back to TCP 8443 automatically. Configure via GPO: `VMware Blast > Enable H264 Encoding`, `Enable UDP`.

---

## Session Broker Role

The Connection Server is a stateful session broker. It maintains:

- **Session database** (stored in ADAM/AD LDS — a local LDAP instance on each Connection Server)
- **Pool and entitlement configuration**
- **vCenter connection state** — Connection Server polls vCenter for VM state
- **Persistent disk assignments** (for Full Clone and linked-clone pools with persistent disks)

Multiple Connection Servers in a pod **replicate** their ADAM database to each other automatically (AD LDS replication). A load balancer (hardware LB or DNS round-robin) distributes client connections across Connection Servers.

**Pod size limits:**
- Maximum 7 Connection Servers per pod
- Maximum 2,000 concurrent sessions per Connection Server (sizing guideline — actual depends on hardware)
- Maximum ~10,000 desktops per pod (recommended)

---

## Security Server Deprecation

The **Security Server** (an older reverse proxy component that ran on Windows, paired with a Connection Server) is deprecated as of Horizon 7.x and removed in later releases. **UAG (Unified Access Gateway)** is the supported replacement for all external access scenarios.

Differences:

| | Security Server (deprecated) | UAG |
|---|---|---|
| OS | Windows Server | Linux appliance (OVA) |
| Pairing | 1:1 with a Connection Server | Many:many (any UAG can reach any Connection Server) |
| Authentication | Forwarded to Connection Server | Can terminate RADIUS/SAML locally |
| Updates | Windows patching | OVA re-deploy or in-place upgrade |
| Scalability | Limited | Scale-out via load balancer |
| Smart card/cert auth | Limited | Full support |

---

## Instant Clone Technology Detail

### Parent VM Lifecycle

The parent VM is kept running at all times (idle, logged off). When a new desktop is requested:

1. `vmFork` API call to ESXi forks the parent VM at the memory and disk level
2. Child VM gets a unique UUID and MAC address
3. Post-customization script runs (hostname, domain join via pre-staged machine account)
4. VM appears as available in pool within ~30 seconds

### Customization Specifications

Instant Clone pools do **not** use traditional vCenter customization specs (sysprep). Instead, they use a **ClonePrep** process:

- A **domain-join account** is configured in the pool settings (must have rights to create/reset computer accounts in the OU)
- Computer accounts are pre-staged or created at clone time
- ClonePrep runs a PowerShell script in the guest post-fork

**ClonePrep log location (in guest):** `C:\Windows\Temp\vmware-viewcomposer-ga-new-*.log`

### Replica and Parent VM Naming

Horizon names these automatically:

```yaml
Replica:  <pool-name>-replica-<timestamp>
Parent:   <pool-name>-parent-<timestamp>
Desktop:  <naming-pattern>-{n}   (e.g., WIN10-{n} → WIN10-001, WIN10-002)
```

The replica and parent VMs consume resources on the ESXi host and datastore — size golden image appropriately and plan for replica storage overhead (one replica per datastore per pool).
