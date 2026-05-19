# Horizon — Common Issues

```
  Triage Decision Tree
┌─────────────────────────────────────────────────────────────┐
│  Login issue?          Blank screen?       Slow login?       │
│  ┌──────────┐          ┌──────────┐        ┌──────────┐      │
│  │ No deskt.│          │ Agent    │        │ DEM migr.│      │
│  │ sources  │          │ running? │        │ AppStack │      │
│  │   │      │          │   │      │        │ AV scan  │      │
│  │   ▼      │          │   ▼      │        └──────────┘      │
│  │Entitlemnt│          │ Blast/   │                          │
│  │ missing? │          │ PCoIP    │        UAG disconnected? │
│  │Pool full?│          │ port ok? │        ┌──────────┐      │
│  │Desktops  │          │ vGPU     │        │ CS cert  │      │
│  │in ERROR? │          │ driver?  │        │ thumbprt │      │
│  └──────────┘          └──────────┘        │ mismatch │      │
│                                            │ TCP 443  │      │
│  AppStack fails?                           │ UAG→CS?  │      │
│  ┌──────────┐                             └──────────┘      │
│  │ AVM reach│                                                │
│  │ able?    │                                                │
│  │ VMDK     │                                                │
│  │ attached?│                                                │
│  └──────────┘                                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Desktop Stuck in "Provisioning"

**Symptoms:** Desktop pool shows desktops in "Provisioning" state for >10 minutes without progressing

**Causes and resolution:**

1. **Parent VM snapshot issue:** Snapshot taken while VMware Tools not current, or VM was not properly sealed (sysprep not run / customization spec missing)
   ```
   Horizon Console → Inventory → Desktops → [pool] → Edit
   Verify: Customization Spec is assigned and valid (test it in vCenter)
   vCenter → right-click golden image → Guest OS → Customize... → test
   ```

2. **vCenter permission issue:**
   ```powershell
   # Check Connection Server event log for permission errors:
   Get-WinEvent -LogName "VMwareVDMDS" | Where-Object { $_.LevelDisplayName -eq "Error" } | 
     Select-Object -First 20 TimeCreated, Message
   ```
   Fix: verify Horizon service account has required vCenter permissions

3. **Datastore full:** Desktop VM cannot be provisioned
   ```
   vCenter → Datastore → check free space > 10% minimum
   ```

4. **Customization spec fails:** Check vCenter Tasks and Events for the provisioning VM
   ```
   vCenter → Monitor → Tasks — filter by the stuck desktop VM name
   ```

---

## "No Desktop Sources Available"

**Symptoms:** Users get "No desktop sources available" when connecting

1. **Pool is exhausted — all desktops assigned or in use:**
   ```
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
   ```
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
   ```
   DEM Management Console → Monitor → check profile migration queue
   ```

2. **AppStack mount failure (App Volumes):** AppStack VMDK attachment is slow or failing
   ```
   App Volumes Manager → Activity → check for stuck attach operations
   ```

3. **Antivirus scanning user profile on login:** AV exclusions needed
   ```
   Exclude from scanning: %APPDATA%, %USERPROFILE%, DEM config share (\\server\dem-config)
   ```

4. **Network drive mapping slow:** Group Policy login script timing out on drive mapping
   ```
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
   ```
   # From desktop VM:
   Test-NetConnection appvol-mgr.example.local -Port 443
   # Must succeed — if failed, firewall or DNS issue
   ```

2. **VMDK attachment failure in vCenter:** AppStack VMDK is already attached to another VM (from a previous failed detach)
   ```
   App Volumes Manager → AppStacks → [stack] → Assignments → check for stale attachments
   OR: vCenter → locate AppStack VMDK → detach from any VM it's currently attached to
   ```
