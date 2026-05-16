# SRM — Hardening

---

## Restrict SRM Server Network Access

SRM Server should only be reachable from:
- vCenter Servers (both sites) — TCP 443, TCP 9086
- Remote SRM Server — TCP 9086
- Management workstations — TCP 443

```powershell
# Windows firewall rules on SRM Server:
New-NetFirewallRule -Name "SRM-vCenter" -DisplayName "Allow vCenter to SRM" `
  -Direction Inbound -Protocol TCP -LocalPort 443,9086 `
  -RemoteAddress 10.10.10.100  # vCenter IP

New-NetFirewallRule -Name "SRM-RemoteSRM" -DisplayName "Allow Remote SRM" `
  -Direction Inbound -Protocol TCP -LocalPort 9086 `
  -RemoteAddress 10.20.10.101  # Remote SRM Server IP (recovery site)

New-NetFirewallRule -Name "SRM-Mgmt" -DisplayName "Allow Management Hosts" `
  -Direction Inbound -Protocol TCP -LocalPort 443 `
  -RemoteAddress 10.10.10.0/24  # Management subnet
```

---

## Least-Privilege SRA Service Accounts

SRA credentials should have minimum array permissions:

**Pure Storage FlashArray:**
- Create API token with role: `readonly` for SRA discovery
- Create separate API token with role: `array_admin` only for failover operations
- Use the read-only token for normal operations; only use admin token during DR

```bash
# On FlashArray (CLI):
pureapitoken create --name srm-readonly --role readonly
pureapitoken create --name srm-failover --role storage_admin
# Use srm-readonly token in SRA — update to srm-failover only during DR
```

---

## Rotate SRA Credentials

Rotate array credentials in SRM on a regular schedule (quarterly or when personnel changes):

```
1. Create new API token / password on storage array
2. Site Recovery → Storage → Array Pairs → [pair] → Configure Adapter → Update credentials
3. Test: Site Recovery → Storage → Array Pairs → Discover Devices (verify discovery succeeds)
4. Delete old token / change old password on array
5. Repeat for recovery site SRM Server
```

---

## Test Recovery Plans Regularly

Monthly testing is the single most effective hardening measure for DR:

```
Site Recovery → Recovery Plans → [plan] → Test
  Frequency: monthly minimum for critical plans, quarterly for non-critical
  Document: pass/fail, duration, issues found, actions taken
```

An untested recovery plan is not a recovery plan — it's a guess.

---

## Restrict Who Can Execute Recovery

```
vCenter → Administration → Global Permissions
  DR Run Team: Site Recovery Recovery Admin role (can execute plans, cannot configure)
  SRM Admins: Site Recovery Administrator role (can configure and execute)

Process: DR execution requires approval from two DR team members (documented in runbook)
```

---

## Secure Recovery Site Network Design

Test failover uses an "isolated network" — verify it is truly isolated:

```
vCenter (Recovery Site) → Networking → [isolated portgroup] → 
  Verify: no uplinks assigned (isolated portgroup = no physical NIC)
  OR: dedicated VLAN with all-deny firewall rule at switch

If test VMs can ping production IPs, the test network is NOT isolated.
```

---

## Windows Hardening of SRM Server

```powershell
# Disable unused services on SRM Server OS
Stop-Service -Name "RemoteRegistry" -ErrorAction SilentlyContinue
Set-Service -Name "RemoteRegistry" -StartupType Disabled

# Configure NTP
w32tm /config /manualpeerlist:"ntp.corp.local" /syncfromflags:manual /reliable:yes
w32tm /config /update

# Enable Windows Defender or your corporate AV (with exclusions):
# Exclude: C:\Program Files\VMware\VMware vCenter Site Recovery Manager\
```

---

## Audit Recovery Plan Changes

```
vCenter → Monitor → Events
  Filter: "drm" events (all SRM events)
  Alert on: Recovery Plan configuration changes, SRA credential updates

Export weekly audit report:
vCenter → Monitor → Events → Export → filter by "drm"
```

---

## Review and Remove Stale Protection Groups

Quarterly: audit protection groups for VMs that have been decommissioned:

```powershell
$pgs = $srm.ExtensionData.Protection.ListProtectionGroups()
foreach ($pg in $pgs) {
    $vms = $srm.ExtensionData.Protection.ListProtectedVms($pg)
    $vmNames = $vms | Select-Object -ExpandProperty Vm | Select-Object -ExpandProperty Name
    Write-Host "PG: $($pg.Name) — VMs: $($vmNames -join ', ')"
}
# Cross-reference with current VM inventory — remove protection for decommissioned VMs
```
