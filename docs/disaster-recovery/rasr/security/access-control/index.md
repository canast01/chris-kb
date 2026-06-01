# RASR — Access Control

Access control for RASR recovery operations, recovery media, snapshot management roles, and least-privilege principles.

## Access Control Boundaries

RASR access control spans several layers:

| Layer | What is Protected | Control Mechanism |
|---|---|---|
| Array management plane | Snapshot creation, RASR policy configuration | RBAC roles in Unisphere / iDRAC |
| Recovery media | Bootable USB, ISO, PXE image | Physical access control, UEFI password |
| Recovery initiation | Triggering a RASR restore | Change management + PAM workflow |
| Recovered system | Post-restore OS access | Standard OS access controls |
| Audit logs | Recovery session records | Immutable log storage, restricted read |

## Storage Array RBAC

### Dell EMC Unity — Role Assignments

Dell EMC Unity (and similar arrays) provide predefined roles. Assign the minimum role needed.

| Role | Capabilities | Who Should Have It |
|---|---|---|
| Administrator | Full array management | DR team lead, storage architects |
| Recovery Manager | Initiate restores, access snapshots | DR operators |
| Storage Operator | Create/manage LUNs, snapshots | Storage operations team |
| VM Administrator | Manage VM-related storage | Virtualisation team |
| Operator | Read-only monitoring | NOC, monitoring tools |
| Read Only | View-only access | Auditors, helpdesk |

```bash
# uemcli — list users and roles
uemcli /user show -detail

# Create a user with Recovery Manager role
uemcli /user create -name svc-rasr-operator -type local -role recovery_manager -passwd "InitialPass!"

# Assign an LDAP group to a role
uemcli /sys/auth/ldapgroup create -name "CORP\\DR-Operators" -role recovery_manager

# View LDAP group role assignments
uemcli /sys/auth/ldapgroup show
```
┌──────────────────────────────────────── RASR — Access Control ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 RASR — RBAC and Access Control                                │   │
│   │      Auth: Vault operator role; 2-person integrity for unlock; AD integration for PPDM UI     │   │
│   │             Principle of least privilege: each role gets only required permissions            │   │
│   │              Service accounts: dedicated, non-interactive; rotation every 90 days             │   │
│   │               Emergency break-glass: documented, monitored, time-limited access               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   │       Role       │   Access Level   │    Typical User   │   Review Freq    │    Granted By    │   │
│   │      Admin       │ Full config/ops  │   Sr Backup Eng   │    Quarterly     │  Security team   │   │
│   │     Operator     │ Start/stop jobs  │     Backup Eng    │    Quarterly     │    Team lead     │   │
│   │     Monitor      │  Read-only view  │      NOC / L1     │    Quarterly     │    Team lead     │   │
│   │   Service Acct   │  API / headless  │     Automation    │   Per rotation   │  Security team   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts     │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest       │
│  Vault         = isolated, air-gapped storage appliance receiving periodic replication copies         │
│  Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies      │
│  CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures        │
│  PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery      │
│  Air Gap       = physical or logical network isolation preventing attacker lateral movement to        │
│  Delta Set     = incremental changed blocks replicated from production to vault each cycle            │
│  Clean Room    = isolated recovery environment: separate vCenter, network, and workstations           │
│  Recovery Point= specific vault snapshot timestamp from which clean recovery is performed             │
│  Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac       │
│  Journal       = write-order-consistent journal on vault enabling point-in-time recovery              │
│  Scan Report   = CyberSense output: clean/suspect classification per file and block                   │
│  Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept                    │
│  RTO           = Recovery Time Objective; time from failover decision to restored service             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

## Recovery Media Access Control

### Physical Access Procedure

Recovery USBs and ISOs must follow a strict custody chain to prevent unauthorised use.

```text
Standard Operating Procedure — RASR Recovery Media:

1. Media is stored in a locked DR cabinet; key held by DR manager
2. Access logged in the DR cabinet access register (name, date/time, reason)
3. Media is checked out under a change record number
4. Single-use principle: media is verified clean (virus scan) after return
5. Media vault inventory reviewed monthly against CMDB records
6. Retired or corrupted media securely destroyed (physical shred or cryptographic wipe)
```

### UEFI Boot Order Lock

Prevent unauthorised boot from recovery media by locking the boot order:

```yaml
UEFI Configuration:
- BIOS Setup Password:   Required to change boot order
- Default boot order:    Internal HDD only
- USB Boot:              Disabled by default; enabled one-time via iDRAC console
- Secure Boot:           Enabled; RASR media must be Secure Boot signed
- PXE Boot:              Allowed only from management VLAN (firewall controlled)
```

```bash
# Racadm — disable USB boot at BIOS level
racadm bios set BootSeq="HardDisk.List.1-1"

# Enable one-time USB boot (authorised recovery session only)
racadm set iDRAC.ServerBoot.BootOnce 1
racadm set iDRAC.ServerBoot.FirstBootDevice USB

# This change requires iDRAC Operator credentials — enforcing authorisation
```

## Snapshot Access Control

RASR operates on storage snapshots. Access to snapshot data must be restricted.

### Snapshot Visibility

```bash
# Unity — list snapshots and their access settings
uemcli /prot/snap show -detail

# Restrict snapshot access (set snap to not be accessible as a production clone)
# Snapshots should not be writable or accessible except during recovery operations
uemcli /prot/snap modify -id snap_001 -descr "RASR snap - restricted"

# Assign snapshot management only to the recovery service account
# Via Unity LDAP group role: recovery_manager role can access snapshots
```

### Network Access to Snapshot Data

```yaml
Snapshot data paths must be isolated:
- Recovery LUNs presented only to the DR recovery host (not production hosts)
- iSCSI or FC zoning restricts which initiators can see recovery targets
- VLAN segmentation: recovery traffic on isolated DR VLAN
- No direct access from application VLANs to recovery storage paths
```

```bash
# Verify FC zone — recovery host should only see DR storage ports
# (Brocade switch example)
zoneshow "DR-Recovery-Zone"

# Verify iSCSI access list (Unity)
uemcli /net/iscsi/node show
```

## Least Privilege for Automated RASR Operations

Automated recovery scripts and scheduled validation tasks should use the minimum required access.

```yaml
Automated RASR service account policy:
- Account: svc-rasr-prod, svc-rasr-uat (one per environment)
- Array role: Operator (read snapshots, initiate restore) — not Administrator
- iDRAC role: Read Only (monitoring only; human operator handles boot)
- Credential storage: PAM vault (CyberArk / HashiCorp Vault) — never in config files
- Network access: management VLAN only, specific source IP restrictions where possible
- Log forwarding: all API actions forwarded to SIEM
```

```bash
# Restrict svc-rasr-prod to management VLAN source IPs on the array firewall
# (Array CLI concept — implementation varies by platform)
uemcli /net/acl create -host 10.10.20.0/24 -access allow

# Service account used for API calls only — verify no interactive sessions
last svc-rasr-prod | head -5   # Should show no interactive SSH sessions
```

## Change Management Gate

All RASR recovery initiations must be gated by an approved change record. This is an administrative access control.

| Stage | Requirement |
|---|---|
| Recovery requested | Change ticket raised with system name, snapshot target, reason |
| Technical review | Storage or DR engineer reviews snapshot integrity |
| Approval | System owner + DR manager approve the change |
| Authorisation to proceed | Change status = "Approved" before any recovery action |
| Recovery execution | Operator initiates recovery; change record updated with start time |
| Completion | Change record closed with result; snapshot inventory updated |

```yaml
ServiceNow change record fields for RASR:
- Assignment Group: DR Operations
- Category: Recovery
- Risk: High
- Implementation Notes: snapshot ID, target system, expected RTO
- Approval chain: system_owner + dr_manager
```

## Separation of Duties

| Action | Who Can Do It |
|---|---|
| Request a recovery | Any authorised user (raises change) |
| Approve a recovery | System owner or DR manager (not the requester) |
| Execute the recovery | DR operator (not the approver) |
| Verify the recovery | Application owner (separate from DR team) |
| Close the change record | Change manager |

## Access Control Audit

```bash
# Array — review who has access to recovery-related roles
uemcli /user show -detail | grep -E "Name:|Role:"
uemcli /sys/auth/ldapgroup show

# iDRAC — review role assignments
racadm get iDRAC.Users

# Check who accessed the recovery USB (physical log audit)
# Review DR cabinet access register for the last 90 days

# Review change records for unapproved recoveries
# ServiceNow: query Changes where category=Recovery AND approval_state != approved
```

```powershell
# Review recent privileged access to array management (from SIEM / event log)
# On management workstation:
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4648} -MaxEvents 50 |
  Where-Object {$_.Message -like "*unisphere*" -or $_.Message -like "*iDRAC*"} |
  Select-Object TimeCreated, Message
```

## Quick Reference

| Topic | Control / Command |
|---|---|
| Array user roles | `uemcli /user show -detail` |
| Array LDAP group roles | `uemcli /sys/auth/ldapgroup show` |
| iDRAC role assignments | `racadm get iDRAC.LDAPRoleGroup` |
| One-time boot authorisation | `racadm set iDRAC.ServerBoot.BootOnce 1` (requires credentials) |
| Snapshot access listing | `uemcli /prot/snap show -detail` |
| Service account in vault | CyberArk / HashiCorp Vault — `svc-rasr-<env>` |
| Change record gate | Change status must be "Approved" before execution |
| Media access log | Physical DR cabinet register |
