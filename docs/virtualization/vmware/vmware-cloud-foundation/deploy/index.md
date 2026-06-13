---
tags:
  - deployment
  - vcf
  - vmware
---
# VMware Cloud Foundation — Deploy

<div class="kb-summary">
End-to-end deployment guide for VMware Cloud Foundation (VCF) bringup. Covers hardware validation, Cloud Builder OVA deployment, bringup JSON spec preparation, management domain deployment, SDDC Manager commissioning, and first workload domain creation.

*Applies to: VCF 4.x / 5.x*
</div>

```text
┌─────────────────────────────────────── VCF — Deployment Phases ───────────────────────────────────────┐
│                                                                                                       │
│  Six phases from bare-metal validation to an operational VCF management domain with first workload    │
│  domain. Each phase has a clear exit criterion. Do not proceed until current phase validates clean.   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌──────────────────────────────┐  ┌──────────────────────────────┐ │
│   │  Phase 1: Pre-Deploy        │  │  Phase 2: Cloud Builder      │  │  Phase 3: Bringup Wizard     │ │
│   │  HCL verification (VCF)     │  │  Deploy Cloud Builder OVA    │  │  Import bringup JSON spec    │ │
│   │  DNS for all components     │  │  Set management IP/FQDN      │  │  Run prerequisite validation │ │
│   │  VLANs on ToR switches      │  │  Access Cloud Builder UI     │  │  Fix all WARN/ERROR items    │ │
│   │  ESXi on ≥4 HCL hosts       │  │  Upload bringup JSON spec    │  │  Start bringup (2–4 hours)   │ │
│   └─────────────────────────────┘  └──────────────────────────────┘  └──────────────────────────────┘ │
│                                                                                                       │
│                ▼                                 ▼                                 ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌──────────────────────────────┐  ┌──────────────────────────────┐ │
│   │  Phase 4: SDDC Manager      │  │  Phase 5: Workload Domain    │  │  Phase 6: Validation         │ │
│   │  Login and health check     │  │  Commission additional hosts │  │  SOS health tool: all green  │ │
│   │  Rotate default passwords   │  │  Network pools configured    │  │  Licences entered            │ │
│   │  Enter VCF licences         │  │  Create VI workload domain   │  │  Certs replaced (CA-signed)  │ │
│   │  Configure SDDC backup      │  │  Verify domain deploys clean │  │  Backup verified             │ │
│   └─────────────────────────────┘  └──────────────────────────────┘  └──────────────────────────────┘ │
│                                                                                                       │
│  Physical Infrastructure: ≥4 HCL-validated rack servers · 25 GbE ToR switches · OOB management        │
│  (iDRAC/iLO) · management/vSAN/vMotion/NSX TEP VLANs pre-configured on switches.                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cloud Builder  = Day-0 VCF deployment appliance; reads JSON spec; deploys management domain          │
│  SDDC Manager   = VCF lifecycle orchestration engine; manages all components post-bringup             │
│  Management domain= first VCF domain; runs SDDC Manager, vCenter, NSX Manager 3-node cluster, vSAN    │
│  Workload domain= tenant vSphere+vSAN+NSX cluster; created via SDDC Manager after bringup             │
│  BOM            = Bill of Materials; VCF version-pinned component versions (cannot mix)               │
│  SOS            = SDDC Operations Support; VCF health-check and log bundle CLI tool                   │
│  Network pool   = IP range pre-allocated in SDDC Manager for VMkernel port commissioning              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access:** vCenter Administrator role and SSH access to VCSA/ESXi hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Phase 1 — Pre-Deployment Checks

**Exit criterion:** All hosts HCL-verified, DNS entries created, VLANs configured on switches, and ESXi installed with management connectivity confirmed.

### Hardware Validation (VCF HCL)

All servers must appear on the [VCF Compatibility Guide](https://www.vmware.com/resources/compatibility/vcf). Check:

| Component | Requirement |
|---|---|
| Server model | Listed on VCF HCL for target VCF version |
| NIC model and firmware | HCL-listed; 25 GbE minimum for vSAN |
| SSD/NVMe drives | HCL-listed; separate cache and capacity tiers for vSAN OSA |
| BIOS version | Must meet VCF minimum (check HCL entry) |
| RAM | ≥512 GB per host recommended for management domain |

Minimum host count: **4 hosts** for management domain. Additional hosts for workload domains.

### DNS Pre-Creation

All FQDNs must exist in DNS before bringup starts. Cloud Builder validates DNS and aborts on failure.

| Component | Example FQDN |
|---|---|
| Cloud Builder | cloud-builder.example.local |
| SDDC Manager | sddc-manager.example.local |
| vCenter (mgmt) | vcenter-mgmt.example.local |
| NSX Manager node 1 | nsx-mgr-01.example.local |
| NSX Manager node 2 | nsx-mgr-02.example.local |
| NSX Manager node 3 | nsx-mgr-03.example.local |
| NSX VIP | nsx-vip.example.local |
| ESXi host 1–4 | esxi-mgmt-01–04.example.local |

```bash
# Verify all DNS entries resolve from the management network
for fqdn in sddc-manager.example.local vcenter-mgmt.example.local nsx-mgr-01.example.local esxi-mgmt-01.example.local; do
  echo -n "$fqdn: "; nslookup $fqdn | grep -E "Address" | tail -1
done
```

### VLAN Configuration on ToR Switches

| VLAN | Purpose | MTU |
|---|---|---|
| VLAN 10 | Management | 1500 |
| VLAN 20 | vMotion | 9000 |
| VLAN 30 | vSAN | 9000 |
| VLAN 40 | NSX TEP (Geneve encap) | 9000 |

Verify trunk VLANs on all switch ports connected to ESXi hosts before Cloud Builder deployment.

### ESXi Pre-Install on Management Hosts

```bash
# On each management host: install ESXi, set management IP, FQDN, DNS, NTP
# Then verify SSH access
ssh root@esxi-mgmt-01.example.local "esxcli system hostname get"
ssh root@esxi-mgmt-02.example.local "esxcli system hostname get"
ssh root@esxi-mgmt-03.example.local "esxcli system hostname get"
ssh root@esxi-mgmt-04.example.local "esxcli system hostname get"
# All must return correct FQDNs
```

---

## Phase 2 — Cloud Builder Deployment

**Exit criterion:** Cloud Builder OVA deployed and accessible; bringup JSON spec uploaded and validation reports no errors.

### Deploy Cloud Builder OVA

```text
vSphere Client (or ESXi host UI) → Deploy OVF Template
  Source: VMware-Cloud-Builder-<version>.ova

  Step 1: VM name: cloud-builder
  Step 2: Compute resource: management ESXi host
  Step 3: Storage: management datastore (20 GB thin sufficient)
  Step 4: Network: Management portgroup
  Step 5: Customize:
    IP: 10.10.10.10 (planned Cloud Builder IP)
    Netmask: 255.255.255.0
    Gateway: 10.10.10.1
    DNS: 10.10.10.53
    NTP: ntp.example.local
    Admin password: <strong password>
    Root password: <strong password>
  → Deploy
```

### Prepare Bringup JSON Spec

The VCF deployment parameter workbook (Excel) generates the JSON spec. Key sections:

```json
{
  "sddcManagerSpec": {
    "hostname": "sddc-manager",
    "ipAddress": "10.10.10.20",
    "netmask": "255.255.255.0",
    "gateway": "10.10.10.1",
    "domain": "example.local",
    "adminPassword": "<password>",
    "localPassword": "<password>"
  },
  "vcenterSpec": {
    "vcenterIp": "10.10.10.21",
    "vcenterHostname": "vcenter-mgmt",
    "licenseFile": "<vCenter-licence-key>"
  },
  "nsxTSpec": {
    "nsxManagerSpecs": [
      {"hostname": "nsx-mgr-01", "ip": "10.10.10.31"},
      {"hostname": "nsx-mgr-02", "ip": "10.10.10.32"},
      {"hostname": "nsx-mgr-03", "ip": "10.10.10.33"}
    ],
    "vip": "10.10.10.30",
    "vipFqdn": "nsx-vip"
  }
}
```

### Run Prerequisite Validation

```text
Cloud Builder UI: https://cloud-builder.example.local
  Login: admin / <password>
  → Deploy vSphere + SDDC Manager
  → Upload bringup JSON spec (or paste JSON directly)
  → Run validation

  Validation checks:
    ✓ DNS resolution for all FQDNs
    ✓ NTP connectivity from all hosts
    ✓ VLAN reachability (ping tests across VLANs)
    ✓ Password complexity
    ✓ ESXi host connectivity (SSH, NTP sync)
    ✓ vSAN disk eligibility
```

```bash
# Resolve all WARN items before proceeding
# ERROR items block bringup; WARN items may proceed but investigate each
# Common issues: DNS PTR missing, NTP unreachable, ESXi NTP not synced
```

---

## Phase 3 — Management Domain Bringup

**Exit criterion:** Bringup completes; SDDC Manager UI accessible and management domain shows Operational.

### Start Bringup

```text
Cloud Builder UI → Validate → Proceed to Deploy → Confirm

  Bringup sequence (automated, 2–4 hours):
    ① Configure ESXi hosts: networking, NTP, DNS
    ② Deploy vCenter VCSA
    ③ Create management cluster in vCenter
    ④ Configure vSAN disk groups on management hosts
    ⑤ Deploy NSX Manager 3-node cluster
    ⑥ Configure NSX: T0/T1 gateways, TEP IPs, edge transport nodes
    ⑦ Deploy SDDC Manager appliance
    ⑧ Register all components with SDDC Manager
```

### Monitor Bringup Progress

```text
Cloud Builder UI → Deployment Status

  Progress bar shows current step
  Click each step for detailed logs
  Full log: Cloud Builder VM → /var/log/vcf/bringup/
```

```bash
# SSH to Cloud Builder if UI is unresponsive
ssh admin@cloud-builder.example.local
tail -f /var/log/vcf/bringup/vcf-bringup.log
```

### Verify Bringup Complete

```bash
# Access SDDC Manager after bringup
# https://sddc-manager.example.local
# Login: admin@local / <password from JSON spec>

# Check management domain status
curl -sk -u 'admin@local:<password>' \
  https://sddc-manager.example.local/v1/domains \
  | python3 -m json.tool | grep -E '"name"|"status"'
# Expected: "MANAGEMENT" domain status "ACTIVE"
```

---

## Phase 4 — SDDC Manager Initial Configuration

**Exit criterion:** All default passwords rotated, licences entered, backup configured, certificates staged.

### Rotate Default Passwords

```bash
# SDDC Manager → Security → Password Management
# Rotate passwords for: vCenter SSO, NSX admin, ESXi root, SDDC Manager admin

# Via API: rotate all ESXi root passwords
curl -sk -X POST -u 'admin@local:<password>' \
  -H "Content-Type: application/json" \
  -d '{"credentialType":"SSH","resourceType":"ESXI"}' \
  https://sddc-manager.example.local/v1/credentials/rotate

# Monitor rotation task status
curl -sk -u 'admin@local:<password>' \
  https://sddc-manager.example.local/v1/tasks \
  | python3 -m json.tool | grep -E '"type"|"status"' | head -20
```

### Enter Licences

```text
SDDC Manager → Administration → Licensing
  → Add licence keys:
    vSphere (per host)
    vSAN (per host)
    NSX (per core or CPU)
    VCF (per core — if applicable)
```

### Configure SDDC Manager Backup

```text
SDDC Manager → Administration → Backup and Restore
  Protocol: SCP
  Server: backup.example.local
  Port: 22
  Directory: /vcf-backups
  Username: vcf-backup
  Passphrase: <encryption passphrase — store securely>
  Schedule: Daily at 03:00
  → Save
```

### Verify Certificate Status

```bash
# Check all component cert expiry
curl -sk -u 'admin@local:<password>' \
  https://sddc-manager.example.local/v1/certificates \
  | python3 -m json.tool | grep -E "expirationDate|resourceFqdn"

# If CA-signed certs required:
# SDDC Manager → Security → Certificate Management
# → Generate CSR per component → sign with enterprise CA → import signed cert
```

---

## Phase 5 — Workload Domain Creation

**Exit criterion:** First VI workload domain in ACTIVE state in SDDC Manager; dedicated vCenter and NSX deployed.

### Commission Workload Hosts

```bash
# Verify hosts are discoverable from SDDC Manager
# Each host must have: ESXi installed, management IP, FQDN, NTP, DNS set

# SDDC Manager → Inventory → Hosts → Commission
# Provide: ESXi host FQDN, root credentials
# SDDC Manager validates: HCL match, DNS, NTP, SSH connectivity
# Host enters "Unassigned" state when commissioned
```

### Create Network Pool

```text
SDDC Manager → Network Settings → Network Pools → Create
  Name: workload-pool-01
  vMotion VLAN: VLAN 120, subnet 192.168.120.0/24, range .10–.50
  vSAN VLAN:    VLAN 130, subnet 192.168.130.0/24, range .10–.50
  NSX TEP VLAN: VLAN 140, subnet 192.168.140.0/24, range .10–.50
```

### Create Workload Domain

```text
SDDC Manager → Workload Domains → Add Domain

  Step 1: Domain type: VI (vSphere Infrastructure)
  Step 2: Cluster details:
    Domain name: workload-01
    vCenter hostname: vcenter-wld01.example.local
    vCenter IP: 10.10.10.40
  Step 3: Select hosts: choose commissioned hosts from free pool (≥3)
  Step 4: vSAN: enable, select capacity disks
  Step 5: Network pool: workload-pool-01
  Step 6: Review → Create

  Wizard deploys: dedicated vCenter + vSAN cluster + NSX segments
  Duration: ~45 minutes
```

```bash
# Monitor workload domain creation
curl -sk -u 'admin@local:<password>' \
  https://sddc-manager.example.local/v1/domains \
  | python3 -m json.tool | grep -E '"name"|"status"'
```

---

## Phase 6 — End-to-End Validation

**Exit criterion:** All health checks pass. Management and workload domains operational. Hand off to operations.

### Run SOS Health Tool

```bash
# SSH to SDDC Manager
ssh vcf@sddc-manager.example.local

# Run full health check
sudo /opt/vmware/sddc-support/sos --health-check
# All checks should return PASS
# WARN items: document and create follow-up tickets
```

### Verify Management Domain Components

```bash
# Check all component status via SDDC Manager API
curl -sk -u 'admin@local:<password>' \
  https://sddc-manager.example.local/v1/system/inventory/components \
  | python3 -m json.tool | grep -E '"componentType"|"status"'
# Expected: all components ACTIVE

# Verify NSX Manager cluster health
curl -sk -u 'admin@local:<password>' \
  https://sddc-manager.example.local/v1/nsxt-clusters \
  | python3 -m json.tool | grep -E '"status"|"version"'
```

### Verify LCM Bundle Access

```bash
# Confirm SDDC Manager can reach VMware depot
curl -sk -o /dev/null -w "%{http_code}" https://depot.vmware.com
# Expected: 200

# Trigger bundle check
# SDDC Manager → Lifecycle Management → Bundle Management → Check Bundles
```

### Post-Deployment Checklist

| Item | Check |
|---|---|
| Management domain | Status ACTIVE in SDDC Manager |
| Workload domain | Status ACTIVE in SDDC Manager |
| SDDC Manager health | SOS health-check all PASS |
| Licences | All components licenced; no warnings |
| Default passwords | All rotated via SDDC Manager |
| SDDC Manager backup | First backup completed and verified |
| Certificates | No certs expiring within 30 days |
| DNS | All FQDNs resolve forward and reverse |
| NTP | All hosts and appliances time-synced < 5 s drift |
| vSAN health | No degraded or inaccessible objects |
| NSX TEP | Geneve tunnel health all green in NSX UI |
| LCM depot | SDDC Manager can reach depot.vmware.com |
| Syslog | SDDC Manager and components forwarding to syslog |

---

## Verify

- **vSphere Client:** confirm the component is visible and shows a healthy status
- **Alarms:** Home → Alarms — no new critical alarms after deployment
- **Logs:** review vmware.log / recent events for any errors in the first 5 minutes
