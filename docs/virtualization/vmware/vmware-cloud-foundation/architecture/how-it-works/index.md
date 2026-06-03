# VMware Cloud Foundation — How It Works

```text
┌─────────────────────────────── VMware Cloud Foundation — How It Works ────────────────────────────────┐
│                                                                                                       │
│  VCF bundles vSphere, vSAN, NSX, and Aria into a single SDDC stack; SDDC Manager                      │
│  automates lifecycle, domain creation, and cluster expansion.                                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 SDDC Manager                 │  │                 Domain Model                │   │
│   │           Lifecycle management hub           │  │         Management domain: ops stack        │   │
│   │         Deploys vCenter + NSX + vSAN         │  │           Workload domains: tenant          │   │
│   │            Certificate management            │  │           VI domain: vSphere+vSAN           │   │
│   │        Password rotation: all stacks         │  │          NSX: shared or per-domain          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SDDC Manager orchestrates all operations; management domain deploys first.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Bring-Up Process               │  │              Cluster Expansion              │   │
│   │        Cloud Builder: initial deploy         │  │               Add host to pool              │   │
│   │            Validates HW readiness            │  │           SDDC Mgr: expand cluster          │   │
│   │          Deploys mgmt domain stack           │  │            Create workload domain           │   │
│   │         JSON spec: all config values         │  │            Hosts: from free pool            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  VCF requires VMware-compatible servers on the VCF HCL; minimum 4 hosts for                           │
│  management domain; 25GbE+ network with defined VLAN layout.                                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SDDC Manager  = VCF automation and lifecycle engine; manages all components                          │
│  Cloud Builder = initial deployment tool; validates and bootstraps VCF                                │
│  Management domain= first domain; runs SDDC Mgr, vCenter, NSX, vSAN                                   │
│  Workload domain= tenant cluster; separate vCenter + NSX per domain                                   │
│  VI domain     = vSphere+vSAN workload domain; most common type                                       │
│  NSX shared    = single NSX manager serves multiple workload domains                                  │
│  Free pool     = unallocated hosts available for domain creation                                      │
│  JSON spec     = configuration file passed to Cloud Builder for bringup                               │
│  Bring-up      = process to deploy management domain from scratch                                     │
│  HCL           = Hardware Compatibility List; VCF-specific list                                       │
│  vLCM          = vSphere Lifecycle Manager; manages ESXi patching in VCF                              │
│  SDDC          = Software-Defined Data Center; the overall VCF platform                               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────── VMware Cloud Foundation — How It Works ────────────────────────────────┐
│                                                                                                       │
│  VCF bundles vSphere, vSAN, NSX, and Aria into a single SDDC stack; SDDC Manager                      │
│  automates lifecycle, domain creation, and cluster expansion.                                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 SDDC Manager                 │  │                 Domain Model                │   │
│   │           Lifecycle management hub           │  │         Management domain: ops stack        │   │
│   │         Deploys vCenter + NSX + vSAN         │  │           Workload domains: tenant          │   │
│   │            Certificate management            │  │           VI domain: vSphere+vSAN           │   │
│   │        Password rotation: all stacks         │  │          NSX: shared or per-domain          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SDDC Manager orchestrates all operations; management domain deploys first.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Bring-Up Process               │  │              Cluster Expansion              │   │
│   │        Cloud Builder: initial deploy         │  │               Add host to pool              │   │
│   │            Validates HW readiness            │  │           SDDC Mgr: expand cluster          │   │
│   │          Deploys mgmt domain stack           │  │            Create workload domain           │   │
│   │         JSON spec: all config values         │  │            Hosts: from free pool            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  VCF requires VMware-compatible servers on the VCF HCL; minimum 4 hosts for                           │
│  management domain; 25GbE+ network with defined VLAN layout.                                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SDDC Manager  = VCF automation and lifecycle engine; manages all components                          │
│  Cloud Builder = initial deployment tool; validates and bootstraps VCF                                │
│  Management domain= first domain; runs SDDC Mgr, vCenter, NSX, vSAN                                   │
│  Workload domain= tenant cluster; separate vCenter + NSX per domain                                   │
│  VI domain     = vSphere+vSAN workload domain; most common type                                       │
│  NSX shared    = single NSX manager serves multiple workload domains                                  │
│  Free pool     = unallocated hosts available for domain creation                                      │
│  JSON spec     = configuration file passed to Cloud Builder for bringup                               │
│  Bring-up      = process to deploy management domain from scratch                                     │
│  HCL           = Hardware Compatibility List; VCF-specific list                                       │
│  vLCM          = vSphere Lifecycle Manager; manages ESXi patching in VCF                              │
│  SDDC          = Software-Defined Data Center; the overall VCF platform                               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────────────────────┐
│  Upgrade Sequence                                                                                     │
│  SDDC Manager → vCenter → ESXi → NSX → vSAN FW                                                        │
│                                                                                                       │
│  1. Download bundle from depot                                                                        │
│  2. Run Precheck (DNS, NTP, certs, vSAN, passwords)                                                   │
│  3. Resolve WARN/ERROR items                                                                          │
│  4. Schedule window → SDDC Manager applies BOM                                                        │
│  5. Post-upgrade validation                                                                           │
└─────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────────────────────┐
│  Workload Domain Provisioning                                                                         │
│  Commission hosts → Create domain → SDDC Manager                                                      │
│  deploys dedicated vCenter, NSX, vSAN as a unit                                                       │
└─────────────────────────────────────────────────────┘
```

```text
┌─────────────────────────────── VMware Cloud Foundation — How It Works ────────────────────────────────┐
│                                                                                                       │
│  VCF bundles vSphere, vSAN, NSX, and Aria into a single SDDC stack; SDDC Manager                      │
│  automates lifecycle, domain creation, and cluster expansion.                                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 SDDC Manager                 │  │                 Domain Model                │   │
│   │           Lifecycle management hub           │  │         Management domain: ops stack        │   │
│   │         Deploys vCenter + NSX + vSAN         │  │           Workload domains: tenant          │   │
│   │            Certificate management            │  │           VI domain: vSphere+vSAN           │   │
│   │        Password rotation: all stacks         │  │          NSX: shared or per-domain          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SDDC Manager orchestrates all operations; management domain deploys first.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Bring-Up Process               │  │              Cluster Expansion              │   │
│   │        Cloud Builder: initial deploy         │  │               Add host to pool              │   │
│   │            Validates HW readiness            │  │           SDDC Mgr: expand cluster          │   │
│   │          Deploys mgmt domain stack           │  │            Create workload domain           │   │
│   │         JSON spec: all config values         │  │            Hosts: from free pool            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  VCF requires VMware-compatible servers on the VCF HCL; minimum 4 hosts for                           │
│  management domain; 25GbE+ network with defined VLAN layout.                                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SDDC Manager  = VCF automation and lifecycle engine; manages all components                          │
│  Cloud Builder = initial deployment tool; validates and bootstraps VCF                                │
│  Management domain= first domain; runs SDDC Mgr, vCenter, NSX, vSAN                                   │
│  Workload domain= tenant cluster; separate vCenter + NSX per domain                                   │
│  VI domain     = vSphere+vSAN workload domain; most common type                                       │
│  NSX shared    = single NSX manager serves multiple workload domains                                  │
│  Free pool     = unallocated hosts available for domain creation                                      │
│  JSON spec     = configuration file passed to Cloud Builder for bringup                               │
│  Bring-up      = process to deploy management domain from scratch                                     │
│  HCL           = Hardware Compatibility List; VCF-specific list                                       │
│  vLCM          = vSphere Lifecycle Manager; manages ESXi patching in VCF                              │
│  SDDC          = Software-Defined Data Center; the overall VCF platform                               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
SDDC Manager → Security → Password Management
→ Select component → Rotate Password
```
```bash
## API — rotate a single credential
curl -sk -u 'admin@local:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"credentialType": "SSH", "resourceType": "ESXI"}' \
  "https://sddc-manager.example.local/v1/credentials/rotate"

## Check credential rotation status
curl -sk -u 'admin@local:password' \
  "https://sddc-manager.example.local/v1/credentials" | python3 -m json.tool
```
```text
SDDC Manager → Security → Certificate Management
→ View expiry per component → Renew or Replace
```
```bash
## Check certificate expiry across all components (API)
curl -sk -u 'admin@local:password' \
  "https://sddc-manager.example.local/v1/certificates" | \
  python3 -m json.tool | grep -E "expirationDate|resourceFqdn"
```
```text
SDDC Manager → Network Settings → Network Pools
→ Create pool → specify VLAN, subnet, gateway, IP range
```
```text
1. Rack and cable host; configure BIOS baseline
2. Install ESXi (or use Auto Deploy)
3. Set management IP, FQDN, DNS — must resolve forward and reverse
4. SDDC Manager → Inventory → Hosts → Commission
   → Provide ESXi IP and root credentials
   → SDDC Manager validates: HCL, SSH, DNS, NTP
5. Host enters "Unassigned" state — available for domain expansion
```
```bash
## SSH to SDDC Manager appliance (vcf user → sudo)
/var/log/vmware/vcf/sddc-manager/vcfops.log     # LCM and orchestration
/var/log/vmware/vcf/sddc-manager/sddc-svc.log   # core SDDC Manager service
/var/log/vmware/vcf/lcm/lcm-debug.log           # Lifecycle Management detail
/var/log/vmware/vcf/domainmanager/dm.log        # Workload domain operations
/var/log/vmware/vcf/commonsvcs/audit.log        # Admin actions and API calls
```
