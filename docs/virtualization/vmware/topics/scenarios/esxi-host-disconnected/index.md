# ESXi Host Disconnected from vCenter

<div class="kb-summary">
An ESXi host shows "Disconnected" or "Not Responding" in vCenter. This scenario walks through confirming
whether VMs are still running, testing management network reachability, restarting vpxa and hostd agents,
diagnosing NTP and DNS as silent causes, and identifying the impact on NSX transport nodes.
</div>

```text
┌──────────────────────────── ESXi Host Disconnected — Investigation Flow ────────────────────────────────┐
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
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

Before touching the host, determine whether VMs are still running. If the host lost only its management
network, all VMs on it continue operating normally — guests have no idea vCenter lost contact.

In vCenter, check the host's VM list for last-known power state. Check **Recent Tasks** for any HA events
(HA-triggered restarts indicate the host truly became unavailable, not just disconnected from management).

Check the cluster **Monitor → vSphere HA → VM Restarts** tab for restart attempts in the last 10 minutes.

---

## 2. Attempt Reconnect from vCenter

Right-click the host in vCenter → **Connection → Reconnect**. If it succeeds within 30 seconds, the
disconnect was a temporary management network blip and no further action is needed — monitor for
recurrence.

If reconnect fails with an error, note the error message. Common errors:

| Error Message | Likely Cause |
|---|---|
| "Unable to contact host" | Management network unreachable |
| "SSL certificate verification failed" | NTP drift or certificate mismatch |
| "VpxClient: Unable to connect to host" | vpxa agent down or crashed |

---

## 3. Test Management Network Reachability

From a jump host on the management VLAN, ping the host's vmk0 IP address:

```bash
ping <esxi-mgmt-ip>
```

- **Reachable** → host is up; the issue is an agent (vpxa or hostd) or SSL/certificate problem.
- **Unreachable** → management network is down, or the host has crashed. Use iDRAC/iLO remote console
  to check whether the host is responsive.

---

## 4. Check and Restart vpxa and hostd Agents

If the host is reachable via SSH, log in and check the two agents vCenter depends on:

```bash
/etc/init.d/vpxa status
/etc/init.d/hostd status
```

Read the logs before restarting — the last error lines explain the disconnect reason. Restarting without
reading destroys that context.

```bash
tail -50 /var/log/vpxa.log
tail -50 /var/log/hostd.log
```

If an agent is stopped or crashed:

```bash
/etc/init.d/vpxa restart
/etc/init.d/hostd restart
```

After restarting, wait 60–90 seconds then attempt the vCenter Reconnect action again.

---

## 5. Verify Management Network Configuration

Confirm vmk0 IP, gateway, and DNS have not drifted (this can happen after a failed configuration change
or after PXE/DHCP interference):

```bash
esxcli network ip interface ipv4 get
esxcli network ip route ipv4 list
esxcli system hostname get
```

Expected output: vmk0 shows the correct static IP, default gateway is present, FQDN matches what vCenter
has registered for this host. Any mismatch here will prevent vCenter from reconnecting even after agent
restarts.

---

## 6. Verify DNS Resolution

ESXi must be able to resolve the vCenter FQDN. If DNS is broken, vpxa cannot reach vCenter even when the
IP network is working:

```bash
nslookup vcenter.domain.local
```

If DNS resolution fails, check `/etc/resolv.conf` for correct nameserver entries:

```bash
cat /etc/resolv.conf
esxcli network ip dns server list
```

Correct a missing DNS server:

```bash
esxcli network ip dns server add --server <dns-ip>
```

---

## 7. Check NTP — Time Drift Causes SSL Failures

A time difference of more than 60 seconds between the ESXi host and vCenter causes SSL certificate
handshake failures. The connection attempt appears to succeed at the network layer but fails at TLS
negotiation — logs show certificate errors, not network errors.

```bash
esxcli system ntp get
ntpq -p
date
```

The `ntpq -p` output shows offset in milliseconds. An offset of more than 60,000 ms (60 seconds) from
the reference server is the threshold for vCenter disconnection. Compare `date` output on the host with
the vCenter system time to confirm drift.

Fix NTP if drifted — see the
[NTP Drift Scenario](../ntp-drift-sso-certificate/index.md) for the full remediation procedure.

---

## 8. Read Logs for Root Cause

After any restarts, read the logs to confirm the error is resolved and to document the root cause:

```bash
tail -100 /var/log/hostd.log | grep -iE "error|ssl|certificate|timeout|refused"
tail -100 /var/log/vpxa.log  | grep -iE "error|ssl|certificate|timeout|refused"
```

The log lines before the first restart attempt are the most valuable. Common patterns:

```text
[error] SSL Exception: error:14090086 — certificate verify failed → NTP drift or cert expiry
[error] Connection refused on port 902              → firewall blocking vCenter → host traffic
[error] vpxa failed to connect: timeout             → network path issue between host and vCenter
```

---

## 9. NSX Transport Node Impact

If the disconnected host is registered as an NSX transport node, NSX Manager loses its control channel
to that host. Overlay segments hosted on that node lose configuration updates (new flows still work via
cached TEP table entries, but new segment or policy pushes will queue until the host reconnects).

Check NSX Manager → **Fabric → Transport Nodes → select host**. State should show "Up" once the host
reconnects to vCenter. If it remains "Down" after vCenter reconnect, restart the NSX agent on the host:

```bash
/etc/init.d/nsx-opsagent restart
/etc/init.d/nsx-mpa restart
```

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
