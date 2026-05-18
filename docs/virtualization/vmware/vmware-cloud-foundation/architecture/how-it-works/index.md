# VCF — How It Works

```
VCF Bring-Up and Lifecycle Flow
┌──────────────────────────────────────────────────────┐
│  Cloud Builder (bring-up tool)                       │
│  reads deployment parameter workbook                 │
└──────────────────────┬───────────────────────────────┘
                       │ deploys
                       ▼
┌──────────────────────────────────────────────────────┐
│  SDDC Manager (management domain)                    │
│                                                      │
│  ┌──────────┐  ┌────────────┐  ┌──────────────────┐ │
│  │ vCenter  │  │ NSX Mgr    │  │  vSAN datastore  │ │
│  │ (mgmt)   │  │ 3-node     │  │  (mgmt VMs)      │ │
│  └──────────┘  └────────────┘  └──────────────────┘ │
└─────────┬────────────────────────────────────────────┘
          │ LCM orchestrates upgrades in BOM order
          ▼
┌─────────────────────────────────────────────────────┐
│  Upgrade Sequence                                    │
│  SDDC Manager → vCenter → ESXi → NSX → vSAN FW     │
│                                                      │
│  1. Download bundle from depot                       │
│  2. Run Precheck (DNS, NTP, certs, vSAN, passwords) │
│  3. Resolve WARN/ERROR items                         │
│  4. Schedule window → SDDC Manager applies BOM      │
│  5. Post-upgrade validation                          │
└─────────────────────────────────────────────────────┘
          │ manages new workload domains
          ▼
┌─────────────────────────────────────────────────────┐
│  Workload Domain Provisioning                        │
│  Commission hosts → Create domain → SDDC Manager   │
│  deploys dedicated vCenter, NSX, vSAN as a unit     │
└─────────────────────────────────────────────────────┘
```

## SDDC Manager

SDDC Manager is the central orchestrator for VCF. It manages the entire lifecycle of all components — deployment, upgrades, password rotation, certificate management, and inventory — across every workload domain.

| Function | Description |
|---|---|
| Workload domain provisioning | Deploys vCenter, NSX, and vSAN as a validated unit |
| Lifecycle Management (LCM) | Orchestrates upgrades across the full BOM stack |
| Password management | Rotates credentials on all managed accounts on schedule |
| Certificate management | Issues and renews certificates for all components via VMCA or third-party CA |
| Network pool management | Allocates IP ranges for VMkernel adapters during host commissioning |
| Inventory | Single pane of glass for all domains, hosts, and components |
| Precheck | Validates DNS, NTP, certificates, vSAN health, and password status before upgrades |

---

## Deployment Domains

### Management Domain

The Management Domain hosts VCF's own management stack. It is always the first domain deployed and must be healthy before workload domains can be created.

| Component | Role |
|---|---|
| SDDC Manager | VCF orchestration plane |
| vCenter (management) | Manages management domain ESXi hosts |
| NSX Manager cluster | Provides overlay networking for the management domain |
| vSAN | Storage for management VMs |

Minimum 4 ESXi hosts. Management components (SDDC Manager, vCenter VMs, NSX Manager VMs) all run within this domain.

### VI Workload Domain

VI (Virtual Infrastructure) Workload Domains host general-purpose vSphere workloads. Each domain has its own vCenter and NSX instance, managed by SDDC Manager.

- Isolated failure domain from other workload domains
- Independent vSAN cluster(s) per domain
- NSX instance scoped to the domain (or shared via NSX Federation)
- Up to 15 workload domains per SDDC Manager instance

### VVF Workload Domain (Tanzu)

VVF (VMware vSphere Foundation) Workload Domains add Tanzu Kubernetes Grid Supervisor to a VI domain, enabling containerised workloads alongside VMs.

---

## Bill of Materials (BOM)

The BOM defines the validated, interoperable versions of all components for a given VCF release. You cannot mix component versions outside the BOM.

| Component | Example (VCF 5.1) |
|---|---|
| ESXi | 8.0 U2 |
| vCenter | 8.0 U2 |
| NSX | 4.1.x |
| vSAN | Embedded in ESXi |
| SDDC Manager | 5.1.x |

Check the BOM before any upgrade: **SDDC Manager → Lifecycle Management → Release Notes**.

---

## Lifecycle Management (LCM)

LCM is the upgrade engine. SDDC Manager downloads bundles from the depot (online or offline), validates compatibility, runs prechecks, and orchestrates rolling upgrades across the stack.

### Upgrade Flow

```
1. Download bundle from depot (or upload from offline file)
2. Run Precheck — validates DNS, NTP, certs, vSAN health, password status
3. Review precheck results — resolve any WARN or ERROR items
4. Schedule upgrade window
5. SDDC Manager upgrades components in BOM order:
   ESXi → vCenter → NSX → vSAN (firmware optional)
6. Post-upgrade validation — SDDC Manager verifies all services healthy
```

### Bundle Management

```bash
# SDDC Manager UI — Lifecycle Management → Bundle Management
# Download latest bundles (requires internet or offline depot)

# Check depot connectivity from SDDC Manager appliance
curl -sk https://depot.vmware.com/PROD2/evo/vmw/index.xml | head -20

# Offline depot: copy bundle .tar files to SDDC Manager
# Administration → Depot Settings → Local Depot
```

### Precheck Validation Points

| Category | What Is Checked |
|---|---|
| DNS | Forward and reverse resolution for all managed FQDNs |
| NTP | Clock skew across all components |
| Certificates | Expiry dates; warns at <30 days |
| vSAN health | Cluster health tests; object compliance |
| Network pools | Available IPs for host commissioning |
| Password rotation | All managed accounts within policy |
| HCL | Hardware compatibility for ESXi hosts |

---

## Password Management

SDDC Manager centrally manages credentials for all components. Passwords rotate on a configurable schedule.

```
SDDC Manager → Security → Password Management
→ Select component → Rotate Password
```

Managed accounts include: vCenter SSO admin, NSX admin, ESXi root, SDDC Manager admin, vSAN iSCSI accounts.

```bash
# API — rotate a single credential
curl -sk -u 'admin@local:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"credentialType": "SSH", "resourceType": "ESXI"}' \
  "https://sddc-manager.corp.local/v1/credentials/rotate"

# Check credential rotation status
curl -sk -u 'admin@local:password' \
  "https://sddc-manager.corp.local/v1/credentials" | python3 -m json.tool
```

---

## Certificate Management

SDDC Manager manages TLS certificates for all components using VMCA (embedded) or a third-party CA.

```
SDDC Manager → Security → Certificate Management
→ View expiry per component → Renew or Replace
```

**Certificate rotation order** (to avoid service disruption):
1. SDDC Manager itself
2. vCenter (Machine SSL + solution certificates)
3. NSX Manager nodes
4. ESXi hosts (via vCenter)

```bash
# Check certificate expiry across all components (API)
curl -sk -u 'admin@local:password' \
  "https://sddc-manager.corp.local/v1/certificates" | \
  python3 -m json.tool | grep -E "expirationDate|resourceFqdn"
```

---

## Network Pools

Network pools pre-allocate IP ranges that SDDC Manager assigns to VMkernel adapters when a new host is commissioned into a workload domain.

| Pool Type | VMkernel Service | Required |
|---|---|---|
| Management | vmk0 | No (uses existing IP) |
| vMotion | vmk1 | Yes |
| vSAN | vmk2 | Yes |
| NSX TEP | vmkX | Yes |

```
SDDC Manager → Network Settings → Network Pools
→ Create pool → specify VLAN, subnet, gateway, IP range
```

Each workload domain references a network pool at provisioning time. Pool exhaustion blocks new host commissioning — monitor available IPs.

---

## Host Commissioning

New hosts are onboarded into SDDC Manager before being assigned to a workload domain.

```
1. Rack and cable host; configure BIOS baseline
2. Install ESXi (or use Auto Deploy)
3. Set management IP, FQDN, DNS — must resolve forward and reverse
4. SDDC Manager → Inventory → Hosts → Commission
   → Provide ESXi IP and root credentials
   → SDDC Manager validates: HCL, SSH, DNS, NTP
5. Host enters "Unassigned" state — available for domain expansion
```

---

## Ports and Logs

| Use | Protocol | Port |
|---|---|---|
| SDDC Manager UI / API | HTTPS | 443 |
| SDDC Manager SSH | TCP | 22 |
| ESXi management | HTTPS | 443 |
| vCenter | HTTPS | 443 |
| NSX Manager | HTTPS | 443 |
| Syslog (TLS) | TCP | 6514 |

**Key SDDC Manager log paths:**

```bash
# SSH to SDDC Manager appliance (vcf user → sudo)
/var/log/vmware/vcf/sddc-manager/vcfops.log     # LCM and orchestration
/var/log/vmware/vcf/sddc-manager/sddc-svc.log   # core SDDC Manager service
/var/log/vmware/vcf/lcm/lcm-debug.log           # Lifecycle Management detail
/var/log/vmware/vcf/domainmanager/dm.log        # Workload domain operations
/var/log/vmware/vcf/commonsvcs/audit.log        # Admin actions and API calls
```
