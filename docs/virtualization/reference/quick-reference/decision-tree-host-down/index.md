# Decision Tree: Host Down


<div class="kb-summary">
Use this when a vSphere host shows `Not Responding` or `Disconnected` in vCenter.
</div>

```text
                    Host: Not Responding / Disconnected
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Ping mgmt IP?      │
                    └─────────────────────┘
                    No ▼              Yes ▼
          ┌──────────────────┐   ┌──────────────────────┐
          │ Check switch/    │   │  SSH to host?        │
          │ iDRAC powered on │   └──────────────────────┘
          └──────────────────┘   No ▼              Yes ▼
                              ┌───────────────┐  ┌──────────────────┐
                              │ Restart agents│  │ Check hostd/vpxa │
                              │ via iDRAC     │  │ status + restart  │
                              │ console       │  └──────────────────┘
                              └───────────────┘          │
                                                         ▼
                                              ┌────────────────────┐
                                              │ PSOD on iDRAC      │
                                              │ console?           │
                                              │ → Cold restart     │
                                              │ → VMware SR bundle │
                                              └────────────────────┘
```
## Step 1 — Can You Ping the Host Management IP?

```bash
ping -c 4 <esxi-management-ip>
```

**No response:**
→ Check physical network switch — port enabled? VLAN correct?
→ Check iDRAC/iLO — is the host powered on?
→ If iDRAC unreachable: escalate to data centre for physical check

**Response received** → proceed to Step 2

## Step 2 — Can You SSH to the Host?

```bash
ssh root@<esxi-management-ip>
```

**SSH fails:**
→ vSphere management agents may be down
→ Try restarting from iDRAC console: `services.sh restart`
→ Or ESXi Direct Console UI (DCUI) → Restart Management Agents

**SSH succeeds** → proceed to Step 3

## Step 3 — Check Management Agent Status

```bash
# On the ESXi host via SSH
/etc/init.d/hostd status
/etc/init.d/vpxa status

# Restart if stopped
/etc/init.d/hostd restart
/etc/init.d/vpxa restart

# Check logs for errors
tail -100 /var/log/hostd.log | grep -E "Error|WARN"
tail -100 /var/log/vpxa.log | grep -E "Error|WARN"
```

After restart: wait 2–3 minutes and check if vCenter shows the host as Connected.

## Step 4 — PSOD (Purple Screen of Death)?

Check via iDRAC console if the host shows a PSOD:
- Note the exact error text (take a photo or screenshot)
- Perform a cold restart via iDRAC
- Submit a support bundle to VMware (KB2072908 procedure)

## Step 5 — Host Reconnects but VMs Are Missing?

Check for maintenance mode or an accidental disconnect event:
```powershell
# Via vCenter PowerCLI
Get-VMHost -Name <host> | Select-Object Name, ConnectionState, PowerState
Get-VMHost -Name <host> | Get-VM | Select-Object Name, PowerState
```

If VMs were migrated by DRS during the disconnect: check the DRS history for migration events.

## Step 6 — Hardware Issues?

```bash
# Check hardware health from ESXi shell
esxcli hardware memory get
esxcli hardware cpu list
esxcli storage core device list

# Check SMART data for disk issues
esxcli storage core device smart get -d <device_id>
```

Review iDRAC/iLO system event log for hardware faults.

## Escalation

If none of the above resolves the issue within 30 minutes:
1. Open a VMware/Broadcom SR with host diagnostics bundle
2. Escalate to hardware vendor (Dell, HPE) if iDRAC shows hardware faults
3. Notify application owners if VMs are impacted and HA has not recovered them
