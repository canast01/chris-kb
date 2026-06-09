# vCenter — Deploy

<div class="kb-summary">
End-to-end deployment guide for VMware vCenter Server Appliance (VCSA). Covers pre-deployment DNS/NTP checks, Stage 1 OVA deployment, Stage 2 SSO and network configuration, Active Directory integration, host inventory build, and post-deployment hardening.
</div>

```text
┌───────────────────────────────────── vCenter — Deployment Phases ─────────────────────────────────────┐
│                                                                                                       │
│  Six phases from DNS record creation to a hardened, production-ready vCenter. Each phase has a        │
│  clear exit criterion. Do not proceed until the current phase validates clean.                        │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌──────────────────────────────┐  ┌──────────────────────────────┐ │
│   │  Phase 1: Pre-Deploy        │  │  Phase 2: VCSA Stage 1       │  │  Phase 3: VCSA Stage 2       │ │
│   │  DNS A + PTR for VCSA FQDN  │  │  Mount ISO on jump host      │  │  Connect to :5480 wizard     │ │
│   │  NTP sources confirmed      │  │  Run vcsa-ui-installer       │  │  Set NTP + SSH + SSO domain  │ │
│   │  Target datastore free space│  │  Size: tiny/small/medium/    │  │  Set SSO admin password      │ │
│   │  AD service account ready   │  │  large/x-large selected      │  │  Wait for services to start  │ │
│   └─────────────────────────────┘  └──────────────────────────────┘  └──────────────────────────────┘ │
│                                                                                                       │
│                ▼                                 ▼                                 ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌──────────────────────────────┐  ┌──────────────────────────────┐ │
│   │  Phase 4: AD Integration    │  │  Phase 5: Inventory Build    │  │  Phase 6: Post-Deploy        │ │
│   │  Add AD identity source     │  │  Create datacenter + cluster │  │  File-based backup schedule  │ │
│   │  LDAP service account bind  │  │  Add ESXi hosts to cluster   │  │  Certificate replace (VMCA)  │ │
│   │  Assign AD groups to roles  │  │  Create dvSwitch + port grps │  │  Skyline Health: green       │ │
│   │  Verify AD login            │  │  Assign licences to hosts    │  │  Syslog/SNMP forwarding      │ │
│   └─────────────────────────────┘  └──────────────────────────────┘  └──────────────────────────────┘ │
│                                                                                                       │
│  Physical Infrastructure: Target ESXi host with sufficient free CPU, RAM, and datastore capacity      │
│  for selected VCSA size tier. Management network with reachability from all target ESXi hosts.        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VCSA         = vCenter Server Appliance; Photon OS VM running vpxd, SSO, and embedded PostgreSQL     │
│  vpxd         = core vCenter daemon; crash or restart brings management plane down                    │
│  SSO domain   = identity namespace (vsphere.local or custom); set once at Stage 2                     │
│  VAMI         = VM Appliance Management Interface; HTTPS management at port 5480                      │
│  VMCA         = VMware Certificate Authority; embedded CA; issues certs for all vCenter services      │
│  ELM          = Enhanced Linked Mode; joins multiple vCenters to share a single inventory view        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1 — Pre-Deployment Checks

**Exit criterion:** DNS, NTP, datastore space, and credentials verified. No blockers outstanding.

### DNS Validation

```bash
# Forward lookup — VCSA FQDN must resolve before deployment
nslookup vcenter.example.local
# Expected: returns planned VCSA IP

# Reverse lookup — PTR record required for SSO certificate issuance
nslookup <planned-VCSA-IP>
# Expected: returns vcenter.example.local

# Verify from target ESXi host
ssh root@esxi-01.example.local
nslookup vcenter.example.local
# Must resolve from every ESXi host that will be managed
```

### NTP Validation

```bash
# Verify NTP on the target ESXi host
esxcli system ntp get
esxcli system ntp stats
# Both NTP sources should show synchronized
```

### Datastore Space Check

| VCSA Size | Max Hosts | Max VMs | Required Disk |
|---|---|---|---|
| Tiny (lab) | 10 | 100 | 415 GB |
| Small | 100 | 1,000 | 480 GB |
| Medium | 400 | 4,000 | 700 GB |
| Large | 1,000 | 10,000 | 1,065 GB |
| X-Large | 2,000 | 35,000 | 1,805 GB |

### AD Service Account

Confirm the AD bind account is available before Stage 2:
- CN: `svc-vcenter` (example)
- Permissions: read access to Users and Groups OUs (no write needed)
- Password: meets complexity requirements (8+ chars, upper, lower, digit, special)

---

## Phase 2 — VCSA Deployment: Stage 1

**Exit criterion:** VCSA VM powered on, OS booted, and Stage 2 web wizard accessible at `https://<VCSA-IP>:5480`.

### Mount ISO and Run Installer

```bash
# On a Windows/Linux/macOS jump host:
# Mount the VCSA ISO

# Launch the UI installer:
# Windows: <ISO>\vcsa-ui-installer\win32\installer.exe
# Linux:   <ISO>/vcsa-ui-installer/lin64/installer
# macOS:   <ISO>/vcsa-ui-installer/mac/installer.app
```

### Stage 1 Deployment Steps

```text
Select: Deploy vCenter Server

  Step 1: Select deployment type
    → vCenter Server with Embedded PSC (standard for new deployments)

  Step 2: Appliance deployment target
    ESXi host/cluster: esxi-01.example.local
    HTTPS port: 443
    Username: root  /  Password: <ESXi root password>
    Accept host thumbprint: Yes

  Step 3: VM configuration
    VM name: vcenter-prod
    Set root password: <strong password>

  Step 4: Deployment size
    Select size: Medium (for 400 hosts / 4,000 VMs)
    Storage size: Default (expand later if needed)

  Step 5: Select datastore
    Datastore: <management datastore>
    Enable thin disk mode: Yes (recommended for lab/dev; No for production)

  Step 6: Network settings
    Network: VM Network (management portgroup)
    IP version: IPv4
    IP assignment: Static
    IP address: <planned VCSA IP>
    Subnet mask: 255.255.255.0
    Default gateway: <gateway>
    DNS servers: <DNS1>, <DNS2>
    Common gateway: <gateway>
    FQDN: vcenter.example.local
    HTTP port: 80
    HTTPS port: 443

  Step 7: Review and finish → Stage 1 deploys (~15 minutes)
```

### Verify Stage 1 Complete

```bash
# Wait for VCSA VM to appear in target ESXi host inventory
# Power state should be: Powered On

# Test VAMI reachability (Stage 2 wizard)
curl -sk https://<VCSA-IP>:5480 | grep -i "getting started"
# Or open https://<VCSA-IP>:5480 in a browser
```

---

## Phase 3 — VCSA Configuration: Stage 2

**Exit criterion:** vCenter services started; vSphere Client accessible at `https://<VCSA-FQDN>/ui`.

### Stage 2 Configuration Wizard

```text
Open browser: https://vcenter.example.local:5480
  Login: root / <password from Stage 1>
  Click: Set Up

  Step 1: Appliance configuration
    NTP server 1: ntp1.example.local
    NTP server 2: ntp2.example.local
    Enable SSH: Yes (disable after deployment; needed for initial setup)

  Step 2: SSO configuration
    SSO domain name: vsphere.local  (or use custom domain; cannot be changed post-deploy)
    SSO site name: Default-First-Site
    SSO password: <strong password — 8+ chars, upper, lower, digit, special>

  Step 3: CEIP participation
    → Deselect (or as per org policy)

  Step 4: Review and complete
    → Finish — Stage 2 takes ~10 minutes; services start automatically
```

### Verify vCenter Services

```bash
# SSH to VCSA (as root)
ssh root@vcenter.example.local

# Verify all core services running
service-control --status --all | grep -E "STOPPED|FAILED"
# Expected: no output (all services running)

# Confirm vpxd is healthy
service-control --status vpxd
# Expected: Running

# Check disk usage
df -h
# No partition should be > 80%

# Verify vSphere Client reachable
curl -sk https://vcenter.example.local/ui | grep -i "vsphere"
```

---

## Phase 4 — Active Directory Integration

**Exit criterion:** AD identity source added; AD groups mapped to vCenter roles; AD user login verified.

### Add AD Identity Source

```text
vSphere Client → Administration → Single Sign On → Configuration → Identity Sources
  → Add

  Type: Active Directory over LDAP
  Name: example.local
  Base DN for users: CN=Users,DC=example,DC=local
  Base DN for groups: CN=Users,DC=example,DC=local
  Domain name: example.local
  Domain alias: EXAMPLE
  Primary URL: ldap://ad1.example.local:389  (or ldaps://ad1.example.local:636)
  Username: EXAMPLE\svc-vcenter  (bind account)
  Password: <svc-vcenter password>
  → Add
```

### Assign AD Groups to vCenter Roles

```text
vSphere Client → Administration → Access Control → Global Permissions
  → Add

  Permission 1 (vSphere admins):
    User/Group: EXAMPLE\vSphere-Admins
    Role: Administrator
    Propagate to children: Yes

  Permission 2 (read-only):
    User/Group: EXAMPLE\vSphere-ReadOnly
    Role: Read-Only
    Propagate to children: Yes
```

### Verify AD Authentication

```bash
# Test AD login by opening vSphere Client in an incognito window:
# https://vcenter.example.local/ui
# Login: EXAMPLE\<your-AD-account>@example.local / <AD password>
# Should land in vSphere Client successfully

# Remove default Administrator@vsphere.local global permissions
# after confirming AD admin group has access
```

---

## Phase 5 — Inventory Build

**Exit criterion:** Datacenter, cluster, and dvSwitch created; all ESXi hosts added and connected; licences assigned.

### Create Datacenter and Cluster

```text
vSphere Client → right-click vCenter root → New Datacenter
  Name: DC-London (or per site naming)

Right-click Datacenter → New Cluster
  Name: Cluster-01
  DRS: Enable (Fully Automated)
  vSphere HA: Enable
  vSAN: Do not enable here (enable via vSAN workflow)
```

### Add ESXi Hosts

```text
Right-click Cluster-01 → Add Hosts
  For each host:
    Hostname/IP: esxi-01.example.local
    Username: root
    Password: <ESXi root password>
    Accept thumbprint: Yes
  → Add all hosts in one operation
```

### Create Distributed Switch

```bash
# vSphere Client → Datacenter → Actions → Distributed Switch → New Distributed Switch
# Name: vDS-Prod
# Version: match ESXi version
# Uplinks: 2
# Default port group: uncheck (create named groups)
```

### Add Hosts to dvSwitch and Create Port Groups

```text
dvSwitch → Actions → Add and Manage Hosts
  → Add hosts → assign vmnic uplinks

Create port groups:
  PG-Management:  VLAN 10
  PG-vMotion:     VLAN 20
  PG-vSAN:        VLAN 30 (if vSAN in scope)
  PG-VM-Prod:     VLAN 100
```

### Assign Licences

```text
vSphere Client → Administration → Licensing → Licenses
  → Add licence keys (vSphere, vSAN, NSX as applicable)

  Assign vSphere licence to cluster
  Assign vSphere licence to each host
```

---

## Phase 6 — Post-Deployment Hardening and Validation

**Exit criterion:** Backup scheduled, certificates valid, Skyline Health green, alarms configured, syslog forwarding active.

### Configure File-Based Backup

```text
VAMI: https://vcenter.example.local:5480
  → Backup → Configure
    Protocol: SCP (or SFTP / HTTP)
    Server: backup.example.local
    Port: 22
    Directory: /vcenter-backups
    Username: vcenter-backup
    Password: <password>
    Schedule: Daily at 02:00
    Retain: 7 backups
    → Save
```

### Replace MACHINE_SSL_CERT (If Required)

```bash
# SSH to VCSA as root
ssh root@vcenter.example.local

# Check current certificate expiry and issuer
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT --text \
  | grep -E "Alias|Issuer|Not After"

# If CA-signed cert required, use certificate-manager:
/usr/lib/vmware-vmcad/certificate-manager
# Option 1: Replace MACHINE_SSL_CERT with custom certificate
# Follow prompts; provide signed cert, private key, and CA chain
```

### Configure Alarm Definitions

```text
vSphere Client → [cluster] → Configure → Alarm Definitions
  Add alarms:
    - Host connection failure  → email + trigger HA
    - Datastore usage > 80%   → email
    - vSAN health degraded     → email (if vSAN deployed)
    - VCSA certificate expiry  → email at 60-day mark
```

### Verify Skyline Health

```bash
# SSH to VCSA
ssh root@vcenter.example.local

# Run health check
/usr/lib/vmware-vmafd/bin/vmafd-cli get-ls-location --server-name localhost
service-control --status --all | grep -v "Running"
# Expected: all services Running; no STOPPED items
```

### Configure Syslog Forwarding

```text
vSphere Client → [vCenter] → Configure → Advanced Settings
  config.log.outputToSyslog: true
  config.log.syslog.address: udp://syslog.example.local:514
```

### Post-Deployment Checklist

| Item | Check |
|---|---|
| DNS | VCSA FQDN resolves forward and reverse |
| NTP | VCSA time drift < 500 ms from ESXi hosts |
| SSO domain | vsphere.local (or custom) configured and login working |
| AD identity source | AD groups log in via vSphere Client |
| ESXi hosts | All hosts Connected in cluster |
| Distributed switch | All hosts migrated to dvSwitch |
| Licences | No licence warnings in vCenter |
| File-based backup | Backup job created and first backup completed |
| MACHINE_SSL_CERT | Valid CA-signed or VMCA cert; not expiring within 30 days |
| Skyline Health | All categories green |
| Alarms | Host disconnect, datastore full, cert expiry alarms active |
| Syslog | vCenter events forwarding to syslog server |
| SSH | SSH disabled on VCSA after setup complete |
