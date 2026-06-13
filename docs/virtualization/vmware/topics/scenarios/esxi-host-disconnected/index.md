---
tags:
  - esxi
  - scenarios
  - vmware
  - vsphere-8
---
# ESXi Host Disconnected from vCenter

<div class="kb-summary">
An ESXi host shows "Disconnected" or "Not Responding" in vCenter. This scenario walks through confirming
whether VMs are still running, testing management network reachability, restarting vpxa and hostd agents,
diagnosing NTP and DNS as silent causes, and identifying the impact on NSX transport nodes.
</div>

```text
┌───────────────────────────── ESXi Host Disconnected — Investigation Flow ─────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│   │  START: vCenter shows host as "Disconnected" or "Not Responding"                                │ │
│   └──────────────────────────────────────────┬──────────────────────────────────────────────────────┘ │
│                                              │                                                        │
│                         ┌────────────────────┼─────────────────────┐                                  │
│                         ▼                    ▼                     ▼                                  │
│              ┌─────────────────┐  ┌─────────────────────┐  ┌──────────────────┐                       │
│              │ VMs still       │  │ Try vCenter         │  │ Check Recent     │                       │
│              │ running?        │  │ Reconnect action    │  │ Tasks — HA event │                       │
│              │ (check console) │  │ (right-click host)  │  │ triggered?       │                       │
│              └────────┬────────┘  └────────┬────────────┘  └──────────────────┘                       │
│                       │                    │                                                          │
│              ┌────────▼────────┐  ┌────────▼────────────┐                                             │
│              │ Yes → only mgmt │  │ Reconnects → blip   │                                             │
│              │ network lost;   │  │ No → dig deeper     │                                             │
│              │ no VM impact    │  └─────────────────────┘                                             │
│              └────────┬────────┘                                                                      │
│                       │                                                                               │
│         ┌─────────────┴──────────────────────────────────────┐                                        │
│         ▼                                                     ▼                                       │
│  ┌─────────────────────────┐                    ┌─────────────────────────┐                           │
│  │ Ping vmk0 from jumphost │                    │ Unreachable → network   │                           │
│  │ Reachable → agent issue │                    │ issue or host crashed   │                           │
│  └────────────┬────────────┘                    │ → iDRAC/iLO console     │                           │
│               │                                 └─────────────────────────┘                           │
│    ┌──────────▼──────────────────────────────────────────┐                                            │
│    │ SSH → check vpxa/hostd → check NTP → check DNS      │                                            │
│    │ Read /var/log/vpxa.log + /var/log/hostd.log          │                                           │
│    └─────────────────────────────────────────────────────┘                                            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter | Displays host state; used to attempt reconnect and review Recent Tasks |
| ESXi | Source of disconnect; management network, vpxa and hostd agents, NTP, DNS |
| NSX | If host is a transport node, disconnect also disrupts NSX control plane for hosted VMs |
| Aria Operations | Raises initial alert; shows host connectivity state and timeline |

---

## 1. Confirm VM Status Before Doing Anything Else

Before touching the host, confirm whether VMs are still running — if only the management network dropped, guests are unaffected.

Check the host's VM list in vCenter for last-known power state, then check **Recent Tasks** for HA events and **Monitor → vSphere HA → VM Restarts** for restart attempts in the last 10 minutes.

---

## 2. Attempt Reconnect from vCenter

Right-click the host → **Connection → Reconnect** to rule out a transient management blip.

If reconnect fails, note the error:

| Error Message | Likely Cause |
|---|---|
| "Unable to contact host" | Management network unreachable |
| "SSL certificate verification failed" | NTP drift or certificate mismatch |
| "VpxClient: Unable to connect to host" | vpxa agent down or crashed |

---

## 3. Test Management Network Reachability

Ping the host's vmk0 IP from a jump host on the management VLAN to determine whether the issue is network or agent.

```bash
ping <esxi-mgmt-ip>
```

- **Reachable** → host is up; issue is vpxa/hostd or SSL.
- **Unreachable** → network is down or host crashed; use iDRAC/iLO console.

---

## 4. Check and Restart vpxa and hostd Agents

Read the logs before restarting — the lines immediately before a crash identify the disconnect reason.

```bash
/etc/init.d/vpxa status
/etc/init.d/hostd status
tail -50 /var/log/vpxa.log
tail -50 /var/log/hostd.log
```

If an agent is stopped or crashed, restart it:

```bash
/etc/init.d/vpxa restart
/etc/init.d/hostd restart
```

Wait 60–90 seconds, then attempt the vCenter Reconnect action again.

---

## 5. Verify Management Network Configuration

Confirm vmk0 IP, gateway, and DNS have not drifted after a failed configuration change or DHCP interference.

```bash
esxcli network ip interface ipv4 get
esxcli network ip route ipv4 list
esxcli system hostname get
```

Look for: vmk0 shows the correct static IP, default gateway is present, FQDN matches what vCenter has registered. Any mismatch prevents reconnection even after agent restarts.

---

## 6. Verify DNS Resolution

ESXi must resolve the vCenter FQDN — a broken DNS lookup blocks vpxa even when IP connectivity is fine.

```bash
nslookup vcenter.domain.local
cat /etc/resolv.conf
esxcli network ip dns server list
```

Correct a missing DNS server:

```bash
esxcli network ip dns server add --server <dns-ip>
```

Look for: `nslookup` returns the correct vCenter IP; no "NXDOMAIN" or timeout errors.

---

## 7. Check NTP — Time Drift Causes SSL Failures

A time difference of more than 60 seconds between the host and vCenter causes TLS handshake failures that look identical to certificate errors.

```bash
esxcli system ntp get
ntpq -p
date
```

Look for: offset column in `ntpq -p` output beyond ±60,000 ms (60 seconds) from the reference server. Compare `date` output on the host with vCenter system time to confirm drift.

Fix NTP if drifted — see the
[NTP Drift Scenario](../ntp-drift-sso-certificate/index.md) for the full remediation procedure.

---

## 8. Read Logs for Root Cause

After any restarts, read logs to confirm the error is resolved and document the root cause.

```bash
tail -100 /var/log/hostd.log | grep -iE "error|ssl|certificate|timeout|refused"
tail -100 /var/log/vpxa.log  | grep -iE "error|ssl|certificate|timeout|refused"
```

Common patterns:

```text
[error] SSL Exception: error:14090086 — certificate verify failed → NTP drift or cert expiry
[error] Connection refused on port 902              → firewall blocking vCenter → host traffic
[error] vpxa failed to connect: timeout             → network path issue between host and vCenter
```

---

## 9. NSX Transport Node Impact

If the disconnected host is an NSX transport node, NSX Manager loses its control channel and new policy pushes queue until the host reconnects.

Check NSX Manager → **Fabric → Transport Nodes → select host**. If state remains "Down" after vCenter reconnect:

```bash
/etc/init.d/nsx-opsagent restart
/etc/init.d/nsx-mpa restart
```

Look for: transport node state transitions to "Up" in NSX Manager within 60–90 seconds.

---

## Key Terms

| Term | Definition |
|---|---|
| vpxa | VMware vCenter Agent — the ESXi daemon that maintains the persistent connection to vCenter; if it crashes, vCenter shows the host as Disconnected |
| hostd | Host Management Daemon — the primary ESXi management service that handles local host operations and API calls; must be running for vpxa to function |
| vmware-fdm | vSphere HA Fault Domain Manager — the HA agent on each ESXi host; monitors cluster membership and triggers VM restarts when a host disconnects |
| DCUI | Direct Console User Interface — the local console accessible via physical keyboard or iDRAC/iLO used to diagnose and recover a host without network access |
| vmk0 | Management VMkernel port — the primary network interface ESXi uses for management traffic including vCenter communication, SSH, and vSAN |
| vCenter | VMware vCenter Server — the centralised management platform that monitors host connectivity, runs HA orchestration, and provides the vSphere UI |
| Lockdown mode | ESXi security feature that restricts management access to vCenter only; if vCenter is unreachable while lockdown is enabled, SSH and DCUI access may also be blocked |
| DNS PTR record | Reverse DNS record mapping an IP address back to a hostname; ESXi uses PTR lookups to verify its own identity with vCenter during reconnection |
| NTP drift | Time difference between a host and a reference server; drift beyond 60 seconds causes TLS certificate validation failures that appear as SSL errors |
| SSH | Secure Shell — the remote shell protocol used to log into ESXi for CLI-level diagnosis of vpxa, hostd, NTP, and log files |
| Management network | The dedicated VLAN and vmk0 interface used for vCenter-to-ESXi control traffic; separate from VM traffic and vSAN traffic |
| Transport node | NSX term for an ESXi host that runs the NSX data plane (TEP interfaces, Geneve encapsulation); losing vCenter connectivity also impacts NSX control channel on that node |

---

## Common Mistakes

- **Rebooting the host before confirming VM status.** If VMs are running and management network just
  dropped, a reboot causes unnecessary guest downtime. Always confirm VM state first.
- **Restarting hostd before reading the log.** The log lines immediately before the crash or failure
  are the diagnosis. Restarting clears the context in memory and rotates the log file.
- **Ignoring NTP as a root cause.** SSL handshake failures caused by time drift look identical to
  certificate expiry errors. Always check `ntpq -p` offset before assuming a cert problem.
- **Not checking DNS after a network change.** A recent VLAN migration or IP change may leave DNS
  entries stale. ESXi resolving vCenter to an old IP causes silent connection failures.

---

## Related Scenarios

- [vCenter Down / Unreachable](../vcenter-down/index.md) — when multiple hosts disconnect simultaneously,
  vCenter itself may be the failing component rather than the individual hosts.
- [NTP Drift Causing SSO or Certificate Errors](../ntp-drift-sso-certificate/index.md) — the full NTP
  diagnosis and remediation procedure referenced in Step 7.
- [PSOD — ESXi Kernel Panic](../psod-esxi-kernel-panic/index.md) — if the host is unreachable at the
  network layer with no management network response, a PSOD may be the cause.
