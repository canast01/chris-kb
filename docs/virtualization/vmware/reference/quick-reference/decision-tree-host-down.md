---
tags:
  - reference
description: "Use this when a vSphere host shows Not Responding or Disconnected in vCenter."
---
# Decision Tree: Host Down

<div class="kb-summary">
Use this when a vSphere host shows `Not Responding` or `Disconnected` in vCenter.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
                    Host: Not Responding / Disconnected
                               │
                               ▼
                    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
                    │  Ping mgmt IP?      │
                    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
                    No ▼              Yes ▼
          ┌──────────────────────────────────────────────── ┐   ┌ ────────────────────────────────────────────────┐
          │ Check switch/    │   │  SSH to host?        │
          │ iDRAC powered on │   └──────────────────────┘
          └──────────────────┘   No ▼              Yes ▼
                              ┌──────────────────────────────────────────────── ┐  ┌ ─────────────────────────────────────────────────┐
                              │ Restart agents│  │ Check hostd/vpxa │
                              │ via iDRAC     │  │ status + restart  │
                              │ console       │  └──────────────────┘
                              └───────────────┘          │
                                                         ▼
                                              ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
                                              │ PSOD on iDRAC      │
                                              │ console?           │
                                              │ → Cold restart     │
                                              │ → VMware SR bundle │
                                              └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Step 1 — Can You Ping the Host Management IP?

```bash
ping -c 4 <esxi-management-ip>
```


```text title="Expected output"
PING 172.16.10.42 (172.16.10.42) 56(84) bytes of data.
64 bytes from 172.16.10.42: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 172.16.10.42: icmp_seq=2 ttl=64 time=2.18 ms
64 bytes from 172.16.10.42: icmp_seq=3 ttl=64 time=2.41 ms
64 bytes from 172.16.10.42: icmp_seq=4 ttl=64 time=2.29 ms

--- 172.16.10.42 statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/stddev = 2.18/2.30/2.41/0.09 ms
```

!!! warning "Common errors"
    **`ping: unknown host <esxi-management-ip>`** — Replace the placeholder with the actual ESXi management IP address (e.g., `ping -c 4 172.16.10.42`).
    **`PING <esxi-management-ip> (PING: sendto: Operation not permitted)`** — Verify firewall rules allow ICMP traffic to the ESXi host and check that the management network is reachable from your current network segment.
    **`100% packet loss`** — Confirm the ESXi host is powered on, the management IP is correct, and the network cable is connected to the management vmnic.
**No response:**
→ Check physical network switch — port enabled? VLAN correct?
→ Check iDRAC/iLO — is the host powered on?
→ If iDRAC unreachable: escalate to data centre for physical check

**Response received** → proceed to Step 2

## Step 2 — Can You SSH to the Host?

```bash
ssh root@<esxi-management-ip>
```


```text title="Expected output"
The authenticity of host '192.168.1.42 (192.168.1.42)' can't be established.
ECDSA key fingerprint is SHA256:aBcD1234eFgH5678iJkL9012mNoPqRsT3456uVwXyZ.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.1.42' (ECDSA) to the known_hosts file.
Password: 
Last login: Wed Jan 15 10:23:47 2025 from 192.168.1.100
   VMware ESXi 8.0.1 Build 21495797
   
root@esx-prod-01:~#
```

!!! warning "Common errors"
    **`ssh: Could not resolve hostname <esxi-management-ip>: Name or service not known`** — Replace `<esxi-management-ip>` with the actual ESXi host IP address (e.g., 192.168.1.42).
    **`Permission denied (publickey,password).`** — Verify the root password is correct and the ESXi host has SSH enabled (Configuration > Security Profile > Services > SSH).
    **`ssh: connect to host 192.168.1.42 port 22: Connection refused`** — Enable SSH on the ESXi host via vCenter or DCUI, as the SSH service is disabled by default.
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


```text title="Expected output"
hostd is running.
vpxa is running.
Restarting hostd...
hostd stopped.
hostd started.
Restarting vpxa...
vpxa stopped.
vpxa started.
2024-01-15T09:42:18.123Z [WARN] Connection pool exhausted for vm-123
2024-01-15T09:43:05.456Z [Error] Failed to retrieve datastore inventory: timeout
2024-01-15T09:44:22.789Z [WARN] Memory pressure detected on host esx-prod-04
```

!!! warning "Common errors"
    **`hostd is stopped.`** — Run `/etc/init.d/hostd start` to bring the service online.
    **`/var/log/hostd.log: No such file or directory`** — Verify the ESXi host is accessible via SSH and the log file exists; check `/var/log/` directory contents with `ls -la /var/log/`.
    **`Permission denied`** — Ensure you are logged in as root or have sudo privileges; use `sudo -i` to escalate if needed.
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


```text title="Expected output"
Name   Physical Memory
------  ----------------
System  65536 MB

CPU 0:
  Vendor: Intel
  Hz: 2400000000
  Bus MHz: 100
  Cache Size: 15360 KB
  Cores Per Socket: 8
  Threads Per Socket: 16

Device: naa.60000000000000000000000000000001
  Display Name: Local SSD (naa.60000000000000000000000000000001)
  Size: 476940 MB
  Device Type: SSD
  Multipath Plugin: NMP
  ...

Device: naa.60000000000000000000000000000001
  Overall Health: Good
  Temperature: 35C
  Predictive Failure: No
  Reallocated Sectors: 0
  Power On Hours: 12847
```

!!! warning "Common errors"
    **`Error: Unknown command or namespace esxcli hardware`** — Verify ESXi version supports the hardware namespace (6.5+) and run from ESXi shell, not vCenter.
    **`Error: Could not find device <device_id>`** — Use `esxcli storage core device list` first to get the exact naa device identifier and replace `<device_id>` with the full device name.
Review iDRAC/iLO system event log for hardware faults.

## Escalation

If none of the above resolves the issue within 30 minutes:
1. Open a VMware/Broadcom SR with host diagnostics bundle
2. Escalate to hardware vendor (Dell, HPE) if iDRAC shows hardware faults
3. Notify application owners if VMs are impacted and HA has not recovered them
