# Server Reboot Runbook


<div class="kb-summary">
| Field | Value | |---|---| | Risk | Medium | | Approval | Change ticket required; maintenance window recommended for production | | Estimated time | 15–30 minutes (excludes application validation) | | Impact | Server and hosted services unavailable during reboot |
</div>

| Field | Value |
|---|---|
| Risk | Medium |
| Approval | Change ticket required; maintenance window recommended for production |
| Estimated time | 15–30 minutes (excludes application validation) |
| Impact | Server and hosted services unavailable during reboot |

## Process Flow

```text
  Reboot request received
           │
           ▼
  Change approved + window confirmed? ─── No ──► Stop. Obtain approval.
           │ Yes
           ▼
  Active users or in-flight jobs? ──────── Yes ──► Wait or force-notify; schedule
           │ No
           ▼
  Stop dependent application services gracefully
           │
           ▼
  Initiate reboot
           │
           ▼
  Server responds to ping within 15 min? ── No ──► Check console / iDRAC / BMC
           │ Yes
           ▼
  All services running? ─────────────────── No ──► Investigate; restart manually
           │ Yes
           ▼
  Application health confirmed?
           │
           ▼
  Close change ticket + clear monitoring alert
```
┌─────────────────────────────────────── Runbook — Server Reboot ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Safe server reboot: pre-checks → drain connections → shutdown → boot → validate        │   │
│   │         Never reboot production without change ticket; notify stakeholders beforehand         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Pre-Reboot Checks               │  │              Post-Reboot Checks             │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │            No active backup jobs             │  │           Server responds to ping           │   │
│   │            No running migrations             │  │             All services started            │   │
│   │          Quiesce cluster resources           │  │          Filesystems mounted clean          │   │
│   │             Notify stakeholders              │  │             No new alerts/errors            │   │
│   │           Confirm IPMI/iLO access            │  │         Application health confirmed        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │       Step       │      Linux       │      Windows      │      VMware      │      Verify      │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │      Drain       │  Stop services   │   Stop services   │   vMotion VMs    │  Confirmed idle  │   │
│   │      Reboot      │   shutdown -r    │  Restart-Computer │    Maint mode    │    Console OK    │   │
│   │       Wait       │    Ping + SSH    │     Ping + RDP    │    Maint exit    │     Login OK     │   │
│   │     Validate     │ systemctl status │   Services check  │   VMs running    │   App healthy    │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    IPMI/iLO  = Out-of-band management; use for console if OS becomes unresponsive post-reboot         │
│    Drain     = Gracefully remove load before shutdown; prevents in-flight request errors              │
│    Maint mode= ESXi maintenance mode; vMotion VMs off host before hardware reboot                     │
│    Quiesce   = Cluster: move resources to peer node; HA group: disable before reboot                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```powershell

**Windows:**
```powershell
Stop-Service <service> -Force
Get-Service <service>    # confirm Stopped
```

## Step 3 — Reboot

**Linux:**
```bash
sudo shutdown -r +1 "Rebooting for maintenance — <reason>"
# or immediate:
sudo reboot
```

**Windows:**
```powershell
Restart-Computer -Force
# With delay:
shutdown /r /t 60 /c "Rebooting for maintenance"
```

**VMware VM via PowerCLI:**
```powershell
Restart-VMGuest -VM <vmname>
```

## Step 4 — Post-Reboot Validation

```bash
# Confirm online
ping -c 4 <server_ip>

# Boot time and uptime
uptime
who -b

# Failed services
systemctl --failed

# Critical service status
systemctl status <service1> <service2>

# Review boot errors
journalctl -b -p err
```

**Windows:**
```powershell
# Services set to Automatic but not running
Get-Service | Where-Object { $_.Status -ne 'Running' -and $_.StartType -eq 'Automatic' }

# Recent system errors since boot
Get-EventLog -LogName System -EntryType Error -Newest 20
```

## Step 5 — Application Health Confirmation

Confirm with the application owner or run the service's own health check before closing the ticket.

```bash
curl -sf https://<app-host>/health && echo OK
```

## Rollback

A reboot is inherently non-reversible. If a service fails to start post-reboot:

1. Check `journalctl -u <service> -n 100` or Windows Event Viewer
2. Restore from last known-good config backup if a config change caused the failure
3. Escalate to application owner if service cannot be recovered within SLA

## Checklist

- [ ] Change approved and maintenance window confirmed
- [ ] Active users notified and logged off
- [ ] Active jobs confirmed clear
- [ ] Application services stopped gracefully
- [ ] Reboot initiated
- [ ] Server responds to ping
- [ ] All services running
- [ ] Application health confirmed by owner
- [ ] Monitoring alert cleared
- [ ] Change ticket closed
