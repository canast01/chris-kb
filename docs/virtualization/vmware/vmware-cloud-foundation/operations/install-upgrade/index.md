# VCF Operations — Install & Upgrade


<div class="kb-summary">
Install & Upgrade reference covering Async Patches, Upgrade Readiness, Bring-Up.
</div>

VCF Upgrade Flow — SDDC Manager Orchestration
```text
┌─────────────────────────────────────────────────────┐
│  Step 1: Bundle Acquisition                         │
│  depot.vmware.com ──► SDDC Manager bundle store     │
│  (or offline: .tar file ► local depot)              │
└──────────────────────────┬──────────────────────────┘
```
┌───────────────────────────── VMware Cloud Foundation — Install & Upgrade ─────────────────────────────┐
│                                                                                                       │
│  VCF installation uses Cloud Builder to deploy the management domain; upgrades                        │
│  are orchestrated by SDDC Manager LCM using versioned upgrade bundles.                                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Installation Steps              │  │           Pre-Install Requirements          │   │
│   │           Deploy Cloud Builder OVA           │  │           HCL: all hardware listed          │   │
│   │          Complete bringup JSON spec          │  │            DNS: all FQDNs resolve           │   │
│   │        Cloud Builder validates input         │  │            NTP: all hosts synced            │   │
│   │           Deploy mgmt domain (~2h)           │  │          VLANs: created on switches         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  DNS and NTP must be correct before bringup; validation failures abort deployment.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Upgrade Process                │  │              Post-Upgrade Steps             │   │
│   │         Download bundle in SDDC Mgr          │  │             Run VCF health check            │   │
│   │           Run pre-check validation           │  │            Verify all certs valid           │   │
│   │           Apply: mgmt domain first           │  │              Check vSAN health              │   │
│   │        Then apply to workload domains        │  │             Validate NSX routing            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Bringup needs 4+ identical bare-metal servers; upgrade temporarily increases                         │
│  host resource usage during patching; maintain 30% vSAN free space.                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cloud Builder = OVA appliance; validates spec and deploys management domain                          │
│  Bringup       = initial VCF deployment process; ~2h for management domain                            │
│  JSON spec     = configuration file for Cloud Builder; all IP/FQDN values                             │
│  SDDC Manager  = takes over from Cloud Builder post-bringup                                           │
│  LCM           = Lifecycle Manager in SDDC Mgr; manages all upgrades                                  │
│  Bundle        = versioned upgrade package; downloaded from VMware depot                              │
│  Pre-check     = automated readiness validation; must pass before upgrade                             │
│  Mgmt domain first= always upgrade management domain before workload domains                          │
│  VCF version   = e.g., VCF 5.2; all components versioned together                                     │
│  HCL           = Hardware Compatibility List; VCF-specific server/NIC list                            │
│  VLAN scheme   = mgmt/vSAN/vMotion/uplink VLANs defined in spec                                       │
│  Depot         = VMware online update repository; SDDC Mgr downloads from                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
                           │ all checks pass
                           ▼
```text
┌─────────────────────────────────────────────────────┐
│  Step 3: Upgrade Sequence (BOM order, no skipping)  │
│                                                     │
│  ① SDDC Manager (always first)                      │
│         │                                           │
│         ▼                                           │
│  ② vCenter (management domain, then workload)       │
│         │                                           │
│         ▼                                           │
│  ③ ESXi hosts (rolling, cluster by cluster)         │
│         │                                           │
│         ▼                                           │
│  ④ NSX-T Manager cluster → Edge clusters            │
│         │                                           │
│         ▼                                           │
│  ⑤ vSAN firmware/driver (HCL-validated)             │
└──────────────────────────┬──────────────────────────┘
```
                           │
                           ▼
```text
```
┌─────────────────────────────────────────────────────┐
│  Step 4: Post-Upgrade Validation                    │
│  All domains green · services healthy · no alarms   │
└─────────────────────────────────────────────────────┘
```text
┌───────────────────────────── VMware Cloud Foundation — Install & Upgrade ─────────────────────────────┐
│                                                                                                       │
│  VCF installation uses Cloud Builder to deploy the management domain; upgrades                        │
│  are orchestrated by SDDC Manager LCM using versioned upgrade bundles.                                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Installation Steps              │  │           Pre-Install Requirements          │   │
│   │           Deploy Cloud Builder OVA           │  │           HCL: all hardware listed          │   │
│   │          Complete bringup JSON spec          │  │            DNS: all FQDNs resolve           │   │
│   │        Cloud Builder validates input         │  │            NTP: all hosts synced            │   │
│   │           Deploy mgmt domain (~2h)           │  │          VLANs: created on switches         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  DNS and NTP must be correct before bringup; validation failures abort deployment.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Upgrade Process                │  │              Post-Upgrade Steps             │   │
│   │         Download bundle in SDDC Mgr          │  │             Run VCF health check            │   │
│   │           Run pre-check validation           │  │            Verify all certs valid           │   │
│   │           Apply: mgmt domain first           │  │              Check vSAN health              │   │
│   │        Then apply to workload domains        │  │             Validate NSX routing            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Bringup needs 4+ identical bare-metal servers; upgrade temporarily increases                         │
│  host resource usage during patching; maintain 30% vSAN free space.                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cloud Builder = OVA appliance; validates spec and deploys management domain                          │
│  Bringup       = initial VCF deployment process; ~2h for management domain                            │
│  JSON spec     = configuration file for Cloud Builder; all IP/FQDN values                             │
│  SDDC Manager  = takes over from Cloud Builder post-bringup                                           │
│  LCM           = Lifecycle Manager in SDDC Mgr; manages all upgrades                                  │
│  Bundle        = versioned upgrade package; downloaded from VMware depot                              │
│  Pre-check     = automated readiness validation; must pass before upgrade                             │
│  Mgmt domain first= always upgrade management domain before workload domains                          │
│  VCF version   = e.g., VCF 5.2; all components versioned together                                     │
│  HCL           = Hardware Compatibility List; VCF-specific server/NIC list                            │
│  VLAN scheme   = mgmt/vSAN/vMotion/uplink VLANs defined in spec                                       │
│  Depot         = VMware online update repository; SDDC Mgr downloads from                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### SDDC Manager Pre-Check Execution

```bash
# Run pre-check for a workload domain upgrade
curl -sk -X POST -u admin:<password> \
  https://localhost/v1/upgrades \
  -H "Content-Type: application/json" \
  -d '{
    "resourceType": "DOMAIN",
    "resourceId": "<domain-id>",
    "bundleId": "<bundle-id>",
    "requestType": "PRECHECK"
  }'

# Retrieve pre-check results
curl -sk -u admin:<password> \
  https://localhost/v1/upgrades/<precheck-id> \
  | python3 -m json.tool

# Check SDDC Manager logs for pre-check detail
tail -200 /var/log/vmware/vcf/sddc-manager/vcf-sddc-manager.log | grep -i "precheck"
```

### Compatibility Matrix Verification

VCF BOM (Bill of Materials) defines the exact component versions per VCF release:

| VCF Version | vCenter | ESXi | NSX | SDDC Manager |
|---|---|---|---|---|
| 5.2 | 8.0 U3 | 8.0 U3 | 4.1.2 | 5.2 |
| 5.1 | 8.0 U2 | 8.0 U2 | 4.1.1 | 5.1 |
| 4.5.2 | 7.0 U3p | 7.0 U3p | 3.2.3 | 4.5.2 |
| 4.4 | 7.0 U3f | 7.0 U3f | 3.2.1 | 4.4 |

```bash
# Check current component versions in SDDC Manager
curl -sk -u admin:<password> \
  https://localhost/v1/system/inventory/components \
  | python3 -m json.tool

# Verify NSX version compatibility
curl -sk -u admin:<password> \
  https://localhost/v1/nsxt-clusters \
  | python3 -m json.tool | grep -E "version|id"
```

### Snapshot and Backup Verification

```bash
# Verify SDDC Manager backup is current
curl -sk -u admin:<password> \
  https://localhost/v1/backups/tasks \
  | python3 -m json.tool | grep -E "status|completionTimestamp" | head -20

# Trigger an on-demand SDDC Manager backup
curl -sk -X POST -u admin:<password> \
  https://localhost/v1/backups \
  -H "Content-Type: application/json" \
  -d '{"elements": [{"resourceType": "SDDC_MANAGER"}]}'

# Check for existing VM snapshots that must be removed pre-upgrade
curl -sk -u admin:<password> \
  https://localhost/v1/system/inventory/snapshots \
  | python3 -m json.tool
```

### Network and Firewall Pre-Checks

Required network connectivity for VCF upgrade operations:

| Source | Destination | Port | Purpose |
|---|---|---|---|
| SDDC Manager | depot.vmware.com | 443 | Bundle download |
| SDDC Manager | All ESXi hosts | 443, 22 | Upgrade orchestration |
| SDDC Manager | vCenter | 443 | vSphere operations |
| SDDC Manager | NSX Manager | 443 | NSX upgrade |
| All ESXi hosts | NFS mount | 2049 | Bundle staging |

```bash
# Test connectivity from SDDC Manager to VMware depot
curl -sk -o /dev/null -w "%{http_code}" https://depot.vmware.com

# Test vCenter reachability
curl -sk -o /dev/null -w "%{http_code}" https://<vcenter-fqdn>/sdk

# Test NSX Manager reachability
curl -sk -o /dev/null -w "%{http_code}" https://<nsx-manager-fqdn>/api/v1/node
```

---

## Bring-Up

VCF bring-up planning, prerequisites, validation, and early lifecycle notes.

### Daily Checks

| Check | Command | Notes |
|---|---|---|
| Review active alarms. |  |  |
| Check recent failed tasks. |  |  |
| Confirm service health. |  |  |
| Confirm capacity and performance are normal. |  |  |
| Check recent changes. |  |  |

### Health Commands

```bash
# Add environment-specific commands here
```

### Common Issues

- Failed or stuck tasks.
- Certificate, DNS, or authentication issues.
- Capacity pressure.
- Service health warnings.
- Version mismatch after maintenance.
- Monitoring gaps.

### Operational Tasks

| Task | Command |
|---|---|
| Review alarms and events. |  |
| Confirm ownership and support notes. |  |
| Validate dependencies. |  |
| Document changes. |  |
| Confirm monitoring coverage. |  |

### Best Practices

| Recommendation | Detail |
|---|---|
| Keep naming consistent. | Keep naming consistent. |
| Keep versions aligned. | Keep versions aligned. |
| Avoid unsupported version combinations. | Avoid unsupported version combinations. |
| Document exceptions. | Document exceptions. |
| Validate after every change. | Validate after every change. |
