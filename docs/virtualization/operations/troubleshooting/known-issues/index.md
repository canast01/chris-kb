# Known Issues and Fix Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│                  KNOWN ISSUE LOOKUP PATTERN                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
   ┌───────────────────────▼──────────────────────────────────┐
   │  SYMPTOM                                                 │
   │  Host disconnected │ Login failure │ vSAN degraded       │
   │  PSOD │ Datastore inaccessible │ Service failed          │
   └───────────────────────┬──────────────────────────────────┘
                           │
   ┌───────────────────────▼──────────────────────────────────┐
   │  KB ARTICLE LOOKUP                                       │
   │  Match symptom ► VMware KB / internal known-issue entry  │
   └───────────────────────┬──────────────────────────────────┘
                           │
   ┌───────────────────────▼──────────────────────────────────┐
   │  WORKAROUND / FIX STEPS                                  │
   │  Apply documented commands or config change              │
   └───────────────────────┬──────────────────────────────────┘
                           │
   ┌───────────────────────▼──────────────────────────────────┐
   │  FIX VERSION                                             │
   │  Confirm patch / build that resolves permanently         │
   │  Schedule upgrade if fix version not yet applied         │
   └──────────────────────────────────────────────────────────┘
```

Structured troubleshooting entries for common VMware/vSAN operational issues. Each entry includes specific diagnostic commands, relevant error messages or event IDs, and concrete fix steps.

---

## 1. Host Disconnected from vCenter

### Symptoms

- Host shows **Not Responding** or **Disconnected** in vCenter Hosts and Clusters view.
- vCenter event log: `Lost connection to host <hostname>` (event ID `vim.event.HostDisconnectedEvent`).
- VMs on the host may show grayed out or inaccessible in the inventory.

### Diagnostics

| Check | Command | Expected Result |
|---|---|---|
| Ping management VMkernel | `ping <host-mgmt-ip>` from vCenter appliance | Response within < 5 ms; no loss |
| DNS resolution (forward) | `nslookup <hostname>` from vCenter appliance | Resolves to correct management IP |
| DNS resolution (reverse) | `nslookup <mgmt-ip>` | Resolves back to the correct FQDN |
| SSH to host | `ssh root@<hostname>` | Successful login |
| hostd service status | From host SSH: `service.sh status` | `hostd` and `vpxa` show `Running` |
| vpxa log (vCenter agent) | From host: `tail -100 /var/log/vpxa.log` | Look for `Connection refused` or SSL errors |
| vCenter connectivity from host | From host: `nc -zv <vcenter-ip> 443` | `Connection succeeded` |

### Fix Steps

1. Confirm management network reachability — if no ping, check physical NIC, VLAN, and upstream switch port.
2. If reachable, restart management agents from the DCUI or SSH:
   ```bash
   # From host SSH
   /etc/init.d/hostd restart
   /etc/init.d/vpxa restart
   ```
3. If DNS is the issue, fix `/etc/resolv.conf` on the host and confirm `nscd` is running:
   ```bash
   cat /etc/resolv.conf
   /etc/init.d/nscd restart
   ```
4. If SSL certificate mismatch is in `vpxa.log`, reconnect the host from vCenter:
   - Right-click host → **Connection** → **Disconnect**, wait 30 s, then **Reconnect**.
5. If the host still fails to reconnect, remove and re-add it to vCenter (last resort — ensure no VMs are running on it first).

---

## 2. vSAN Capacity Warning

### Symptoms

- vSAN health alert: **vSAN datastore usage** with a yellow or red badge.
- Alarm: `vSAN datastore is running out of disk space`.
- Capacity dashboard shows used > 70% (warning) or > 80% (critical).

### Diagnostics

| Check | Command | Expected Result |
|---|---|---|
| Capacity summary | `Get-VsanSpaceUsage -Cluster <name>` | Free capacity > 30% |
| Per-object breakdown | `esxcli vsan debug object list \| grep -i "size"` | No single object unexpectedly large |
| Resync bytes | `esxcli vsan debug resync list` | Empty; resync adds temporary capacity pressure |
| Snapshots consuming space | `Get-VM \| Get-Snapshot \| Sort-Object SizeMB -Descending \| Select-Object -First 20` | No large orphaned snapshots |
| Dedup savings | `Get-VsanSpaceEfficiencyUsage -Cluster <name>` | Dedup ratio and savings report |

### Fix Steps

1. **Immediate:** Delete stale VM snapshots that are consuming hidden capacity:
   ```powershell
   Get-VM | Get-Snapshot | Where-Object { $_.Created -lt (Get-Date).AddDays(-3) } | Remove-Snapshot -Confirm:$false
   ```
2. If a large resync is in progress, wait for it to complete before taking action — do not add hosts or make policy changes mid-resync:
   ```bash
   watch -n 10 'esxcli vsan debug resync list'
   ```
3. If capacity is genuinely exhausted, defer any maintenance window that would trigger additional resync.
4. If running an erasure coding policy (RAID-5/6), consider whether switching lower-priority VMs to RAID-1 temporarily frees space (RAID-5 uses 1.33× vs RAID-1 at 2×).
5. Long-term remediation: add a disk group to an existing host or expand the cluster.

---

## 3. vCenter Login Failure

### Symptoms

- Login page returns: `503 Service Unavailable` or `An error occurred while connecting to the server`.
- SSO login fails with: `Error: The request failed because the server is not currently available`.
- Event log may show: `com.vmware.sso.PrincipalNotFound` or `com.vmware.sso.InvalidCredentials`.

### Diagnostics

| Check | Command | Expected Result |
|---|---|---|
| VAMI service health | Browse to `https://<vcsa-fqdn>:5480` → Monitor | All services show green |
| SSO service status | SSH to VCSA: `service-control --status vmware-sso` | `Running` |
| All service status | `service-control --status --all` | All services `Running` |
| SSO certificate expiry | `for store in MACHINE_SSL_CERT trusted-roots; do /usr/lib/vmware-vmafd/bin/vecs-cli entry list --store $store --text; done \| grep -A2 "Not After"` | No certificates expired |
| STS signing cert | `/usr/lib/vmware-vmafd/bin/dir-cli user find-by-name --account administrator --domain vsphere.local` | Returns user info without error |
| Auth log | `tail -200 /var/log/vmware/sso/vmware-sts-idmd.log` | Look for `LDAP`, `certificate`, or `bind` errors |

### Fix Steps

1. If SSO is not running, restart it:
   ```bash
   service-control --stop --all
   service-control --start --all
   ```
2. If a specific service is failed, restart it individually and check its log:
   ```bash
   service-control --restart vmware-sso
   tail -f /var/log/vmware/sso/vmware-sts-idmd.log
   ```
3. If certificates are expired, use the Certificate Manager to reissue:
   ```bash
   /usr/lib/vmware-vmca/bin/certificate-manager
   # Choose option 3 (Replace Machine SSL certificate) or option 6 (Fix all certificates)
   ```
4. If the SSO administrator password is locked, unlock it via VCSA shell:
   ```bash
   /usr/lib/vmware-vmafd/bin/dir-cli user modify --account administrator --domain vsphere.local --password-never-expires true
   ```
5. If identity source (AD) is unreachable, verify DNS and connectivity to the domain controller from the VCSA:
   ```bash
   nslookup <domain-controller-fqdn>
   ldapsearch -H ldap://<dc-ip> -x -b "dc=corp,dc=local"
   ```

---

## 4. vSAN Object Inaccessible

### Symptoms

- VM shows **Invalid** or **Inaccessible** in the vCenter inventory.
- vSAN health alert: **vSAN object health** shows objects in `Degraded` or `Absent` state.
- Error on VM power-on: `Failed to lock the file` or `Unable to access file since it is locked`.

### Diagnostics

| Check | Command | Expected Result |
|---|---|---|
| Object health summary | `Get-VsanObject -Cluster <name> \| Where-Object { $_.HealthState -ne "healthy" }` | Empty for healthy cluster |
| CLOM object list | `esxcli vsan debug object list \| grep -Ev "healthy\|complyState"` | No inaccessible or degraded objects |
| Resync queue | `esxcli vsan debug resync list` | Shows bytes remaining and ETA |
| Component owners | `esxcli vsan debug object list \| grep -A5 "<object-uuid>"` | All components have live owners |
| vSAN disk health | `esxcli vsan storage list \| grep -i "operational"` | All disks show `Operational State: ok` |
| Host contributing to object | `esxcli vsan debug object list \| grep "host"` | No component on a disconnected host |

### Fix Steps

1. If a host is down (causing components to be absent), bring the host back online first. vSAN CLOM will automatically begin repair after the **Object Repair Delay** timer expires (default: 60 minutes).

2. To monitor resync progress:
   ```bash
   # From any host SSH — watch resync clear
   watch -n 30 'esxcli vsan debug resync list'
   ```

3. If the object remains inaccessible after the host recovers, force a resync via CLOM:
   ```bash
   # From host SSH — trigger CLOM to re-evaluate object placement
   esxcli vsan debug object reconfigure --object-uuid <uuid> --policy "<storage-policy-XML>"
   ```

4. If a disk group is permanently lost and components are unrecoverable, you can attempt to evacuate or reconstruct using RVC (Ruby vSphere Console):
   ```bash
   # List inaccessible objects
   vsan.check_state -r /datacenter/host/<cluster>
   # Force rebuild (use with caution)
   vsan.obj_status_report -r /datacenter/host/<cluster>
   ```

5. If the object cannot be recovered, restore the VM from backup. Do not attempt to delete and re-register inaccessible VM disk files without confirming CLOM has fully given up on reconstruction.

---

## 5. vCenter Appliance Service Failure (VAMI)

### Symptoms

- vCenter UI unreachable or partially functional; some tabs return errors.
- VAMI health page (`https://<vcsa>:5480`) shows one or more services in **Stopped** or **Failed** state.
- SSH to VCSA shows high load or a specific service in a crash loop in `journalctl`.

### Diagnostics

| Check | Command | Expected Result |
|---|---|---|
| All service status | `service-control --status --all` | All `Running` |
| Failed units | `systemctl --failed` | Empty list |
| Service logs | `journalctl -u vmware-<service> --since "1 hour ago"` | No repeated crash/restart loops |
| Disk space on VCSA | `df -h` | All partitions < 80% used |
| `/storage/log` usage | `df -h /storage/log` | < 85% — log partition full causes service failures |
| vPostgres DB | `service-control --status vpostgres` | `Running` — DB failure cascades to all services |

### Fix Steps

1. Identify the failed service and attempt a targeted restart:
   ```bash
   service-control --restart vmware-vpxd
   # or for vPostgres:
   service-control --restart vpostgres
   ```

2. If the log partition is full (common cause), archive and truncate large logs:
   ```bash
   df -h /storage/log
   # Find large files
   find /storage/log -name "*.log" -size +500M
   # Truncate (do not delete — open file handles)
   > /storage/log/vmware/vpxd/vpxd.log
   ```

3. If the database is corrupted or `vpostgres` will not start:
   ```bash
   # Check PostgreSQL logs
   tail -200 /var/log/vmware/vpostgres/postgresql.log
   # Attempt DB recovery
   service-control --stop vmware-vpxd
   /opt/vmware/vpostgres/current/bin/pg_resetwal -f /storage/db/vpostgres
   service-control --start vpostgres
   service-control --start vmware-vpxd
   ```

4. If a full service restart is required:
   ```bash
   service-control --stop --all
   service-control --start --all
   ```

5. If VAMI itself is inaccessible, the appliance management UI service can be restarted via SSH:
   ```bash
   systemctl restart vami-lighttp
   ```

---

## 6. ESXi Host PSOD / Purple Screen of Death

### Symptoms

- Host displays a purple diagnostic screen with a stack trace — referred to as a PSOD (Purple Screen of Death) or `vmkernel` panic.
- Host becomes unreachable; all VMs on the host are lost until the host reboots and HA restarts them.
- vCenter event: `Host <hostname> has lost network connectivity` followed by `HA agent on <hostname> is unreachable`.

### Diagnostics

Collect data before rebooting whenever possible. If the PSOD screen is accessible, photograph the full trace — particularly the `#PF Exception` or `BUG:` line and the top 5 frames of the backtrace.

| Check | Command / Location | What to Look For |
|---|---|---|
| vmkernel log (post-reboot) | `/var/log/vmkernel.log` | Panic message, `PCPU`, `BUG:`, driver module name |
| Core dump location | `/var/core/` or `/scratch/` — `ls -lh /var/core/` | `.dumpfile` or `.zdump` present after reboot |
| vmkernel panic summary | `vsish -e get /system/bootconfig/bootstart` | Boot timestamp; correlate with panic time |
| Driver/module at fault | `grep -i "panic\|BUG\|ASSERT" /var/log/vmkernel.log \| tail -50` | Module name in parentheses, e.g., `(ixgbe)` |
| Hardware error | `/var/log/vmksummary.log` | MCE (Machine Check Exception) entries |
| ESXi version and patch level | `vmware -v` | Confirm against known PSOD KB articles |
| Core dump analysis | Upload `.zdump` to VMware Support or use `vmss2core` | Full stack trace with symbol resolution |

### Fix Steps

1. **Immediate:** If VMs were running on the host, confirm HA has restarted them on other hosts:
   ```powershell
   Get-VM | Where-Object { $_.Host.Name -ne "<failed-host>" } | Select-Object Name, Host
   # Check recent HA events
   Get-VIEvent -MaxSamples 500 | Where-Object { $_ -is [VMware.Vim.VmFailoverSucceededEvent] }
   ```

2. Collect core dump before rebooting (if host is still reachable via SSH):
   ```bash
   ls -lh /var/core/
   # Copy dump off-host
   scp /var/core/*.zdump <backup-host>:/tmp/
   ```

3. After reboot, check vmkernel log for the panic cause and module:
   ```bash
   grep -B5 -A20 "PCPU" /var/log/vmkernel.log | head -100
   ```

4. **When to reboot immediately vs. escalate:**
   - **Reboot immediately:** PSOD caused by a known driver bug with a patch available (confirm in VMware KB); no data integrity concern (vSAN resync will recover objects).
   - **Escalate first:** PSOD shows MCE (hardware fault) — indicates failing CPU, RAM, or PCIe bus; rebooting may mask data corruption. Open a hardware vendor ticket before returning the host to production.
   - **Escalate first:** Repeated PSOD (> 2 in 7 days) on the same host — pattern indicates hardware failure or persistent driver/firmware issue.

5. After root cause is identified:
   - For driver bugs: apply the relevant VIB update:
     ```bash
     esxcli software vib update -v <vib-path>
     reboot
     ```
   - For firmware bugs: update via vendor tooling (HPE SUM, Dell SUU, Lenovo UpdateXpress) before returning the host to the cluster.
   - For hardware failure: replace the faulty component (DIMM, NIC, HBA) and run memory/hardware diagnostics (e.g., Memtest, vendor diagnostics) before re-adding to cluster.
