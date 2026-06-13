---
tags:
  - horizon
  - troubleshooting
  - vmware
---
# VMware Horizon — Common Issues

```text
┌─────────────────────────────────── VMware Horizon — Common Issues ────────────────────────────────────┐
│                                                                                                       │
│  Common Horizon issues: black screen, pool provisioning failure, Connection Server                    │
│  error, slow Blast sessions, and UAG certificate errors.                                              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Black Screen Issues              │  │            Provisioning Failures            │   │
│   │           Agent not running on VM            │  │            vCenter: not reachable           │   │
│   │           Blast port 8443 blocked            │  │            Template: no snapshot            │   │
│   │             GPU driver mismatch              │  │          Disk space: datastore full         │   │
│   │           Profile load fails: DEM            │  │          Clone error: check events          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Black screen = Blast connected but agent not ready; check agent services.                            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               CS & UAG Issues                │  │              Performance Issues             │   │
│   │           CS error: check services           │  │             Blast latency >100ms            │   │
│   │         Cert expired: replace on CS          │  │             Check ESXi host CPU             │   │
│   │           UAG: health check fails            │  │          Disk IOPS: vSAN contention         │   │
│   │         AD unreachable: local user?          │  │           Network BW: 1–5Mbps/user          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Most issues: agent not running (black screen), network ports blocked, vCenter                        │
│  unreachable (provisioning), or cert expired (login/UAG); check all four.                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Horizon Agent = service on desktop VM; must be running for session                                   │
│  Blast port 8443= UDP/TCP port for display protocol; must be open                                     │
│  Black screen  = connected session but no display; agent issue                                        │
│  DEM           = Dynamic Environment Manager; profile load at login                                   │
│  UAG health    = REST /rest/healthcheck; returns 200 if healthy                                       │
│  CS services   = VMware Horizon View Connection Server service on Windows                             │
│  Template      = golden image VM must have current snapshot                                           │
│  Clone error   = check vCenter tasks and events for provisioning log                                  │
│  GPU driver    = agent + driver version must match; black screen if not                               │
│  Blast latency = display round-trip; >100ms = degraded user experience                                │
│  IOPS contention= vSAN or NFS storage saturation during peak clone                                    │
│  1–5Mbps/user  = Blast bandwidth per session; plan WAN accordingly                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
   vCenter → Monitor → Tasks — filter by the stuck desktop VM name
   ```

---

## "No Desktop Sources Available"

**Symptoms:** Users get "No desktop sources available" when connecting

1. **Pool is exhausted — all desktops assigned or in use:**
   ```text
   Horizon Console → Inventory → Desktops → [pool]
   Check: Available count — if 0, all desktops are in use or error
   Increase pool size or add headroom
   ```

2. **All desktops in error state:**
   ```powershell
   Get-HVDesktop -PoolName "pool-win10-float" | 
     Group-Object { $_.Base.BasicState } | Select Name, Count
   # If all are ERROR: bulk-delete and let pool reprovision
   Get-HVDesktop -PoolName "pool-win10-float" | 
     Where-Object { $_.Base.BasicState -eq "ERROR" } | 
     Remove-HVDesktop -Confirm:$false
   ```

3. **Entitlement missing:** User is not entitled to the pool
   ```text
   Horizon Console → [pool] → Entitlements → verify user's AD group is listed
   ```

---

## Black Screen After Login

**Symptoms:** User authenticates successfully, session starts, but screen remains black

1. **Horizon Agent not running in the desktop VM:**
   ```powershell
   # From Connection Server:
   $desktop = Get-HVDesktop -VMName "win10-042"
   # Get the VM IP, then check remotely:
   Get-Service -ComputerName <desktop-ip> -Name "VMware Horizon View Agent"
   # If stopped: reset the desktop (reboot)
   Reset-HVMachine -HVMachineName "win10-042"
   ```

2. **Display protocol (Blast/PCoIP) port blocked:** Check NSG or firewall rules between Horizon Client and the UAG/Connection Server

3. **vGPU driver issue (if vGPU pool):** Check vGPU driver status in guest

---

## Slow Login

**Symptoms:** Login takes >60 seconds; users report slow desktop loading

1. **DEM profile migration:** First-time migration of legacy profile to DEM can take minutes — expected behavior
```text
   DEM Management Console → Monitor → check profile migration queue
   ```

2. **AppStack mount failure (App Volumes):** AppStack VMDK attachment is slow or failing
```text
   App Volumes Manager → Activity → check for stuck attach operations
   ```

3. **Antivirus scanning user profile on login:** AV exclusions needed
```sql
   Exclude from scanning: %APPDATA%, %USERPROFILE%, DEM config share (\\server\dem-config)
   ```

4. **Network drive mapping slow:** Group Policy login script timing out on drive mapping
```text
   Enable asynchronous user Group Policy processing to prevent blocking login
   ```

---

## UAG Shows Disconnected from Connection Server

**Symptoms:** UAG Admin UI shows "Connection Server is not connected" or users can authenticate but cannot launch desktops

1. **Certificate mismatch:** Connection Server cert thumbprint in UAG config doesn't match the current CS cert
   ```bash
   # Get current CS cert thumbprint:
   echo | openssl s_client -connect horizon-cs01.example.local:443 2>/dev/null \
     | openssl x509 -fingerprint -sha1 -noout
   # Compare to thumbprint in UAG:
   UAG Admin UI → Edge Service Settings → Horizon → Thumbprint
   # Update if different
   ```

2. **Firewall between UAG and Connection Server:** TCP 443 from UAG backend NIC to Connection Server must be open

---

## App Volumes AppStack Fails to Mount

**Symptoms:** User logs in but application is not available; App Volumes Manager shows failed attachment

1. **App Volumes Manager unreachable from desktop VM:**
```powershell
   # From desktop VM:
   Test-NetConnection appvol-mgr.example.local -Port 443
   # Must succeed — if failed, firewall or DNS issue
   ```

2. **VMDK attachment failure in vCenter:** AppStack VMDK is already attached to another VM (from a previous failed detach)
```sql
   App Volumes Manager → AppStacks → [stack] → Assignments → check for stale attachments
   OR: vCenter → locate AppStack VMDK → detach from any VM it's currently attached to
   ```
