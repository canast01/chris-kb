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

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_confirm_vm_status_before_doing_any: "1. Confirm VM Status Before Doing Anything Else" {shape: rectangle}
2_attempt_reconnect_from_vcenter: "2. Attempt Reconnect from vCenter" {shape: rectangle}
3_test_management_network_reachabili: "3. Test Management Network Reachability" {shape: rectangle}
4_check_and_restart_vpxa_and_hostd_a: "4. Check and Restart vpxa and hostd Agents" {shape: rectangle}
5_verify_management_network_configur: "5. Verify Management Network Configuration" {shape: rectangle}

products_involved -> 1_confirm_vm_status_before_doing_any: uses
1_confirm_vm_status_before_doing_any -> 2_attempt_reconnect_from_vcenter: uses
2_attempt_reconnect_from_vcenter -> 3_test_management_network_reachabili: uses
3_test_management_network_reachabili -> 4_check_and_restart_vpxa_and_hostd_a: uses
4_check_and_restart_vpxa_and_hostd_a -> 5_verify_management_network_configur: uses
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


```text title="Expected output"
PING 192.168.1.42 (192.168.1.42) 56(84) bytes of data.
64 bytes from 192.168.1.42: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 192.168.1.42: icmp_seq=2 ttl=64 time=1.89 ms
64 bytes from 192.168.1.42: icmp_seq=3 ttl=64 time=2.12 ms
64 bytes from 192.168.1.42: icmp_seq=4 ttl=64 time=1.95 ms
^C
--- 192.168.1.42 statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/stddev = 1.89/2.07/2.34/0.18 ms
```

!!! warning "Common errors"
    **`ping: unknown host <esxi-mgmt-ip>`** — Replace `<esxi-mgmt-ip>` with the actual ESXi management IP address (e.g., `192.168.1.42`).
    **`From 192.168.1.1 icmp_seq=1 Destination Host Unreachable`** — Verify the ESXi host is powered on, the management network is connected, and firewall rules allow ICMP traffic.
    **`ping: sendto: No route to host`** — Confirm the ESXi management IP is on the same subnet or that routing is properly configured between your admin workstation and the ESXi management network.
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


```text title="Expected output"
vpxa (pid 2847) is running...
hostd (pid 3124) is running...
2024-01-15 14:32:18.547 [7F2A4C1B9700 info 'Libs' opID=52d41e22] VpxaHalVmomi_GetConfig: Entering
2024-01-15 14:32:19.123 [7F2A4C1B9700 info 'Hostd' opID=52d41e22] Config update: vMotion enabled
2024-01-15 14:32:20.445 [7F2A4C1B9700 warn 'Libs' opID=52d41e22] Certificate expiry in 45 days
2024-01-15 14:32:21.678 [7F2A4C1B9700 info 'Libs' opID=52d41e22] Connection to vCenter established
2024-01-15 14:32:22.891 [7F2A4C1B9700 info 'Hostd' opID=52d41e22] Inventory sync completed
...
2024-01-15 14:33:45.234 [7F2A4C1B9700 info 'Libs' opID=52d41e22] Heartbeat received from vCenter
2024-01-15 14:33:46.567 [7F2A4C1B9700 info 'Hostd' opID=52d41e22] VM snapshot operation completed
2024-01-15 14:33:47.890 [7F2A4C1B9700 info 'Libs' opID=52d41e22] Storage device scan completed
2024-01-15 14:33:48.123 [7F2A4C1B9700 info 'Hostd' opID=52d41e22] NTP synchronization successful
2024-01-15 14:33:49.456 [7F2A4C1B9700 info 'Libs' opID=52d41e22] All services operational
```

!!! warning "Common errors"
    **`vpxa (pid XXXX) is running... hostd (pid XXXX) is running...`** — Both services are healthy; if either shows "is stopped," restart with `/etc/init.d/vpxa start` and `/etc/init.d/hostd start`.
    **`tail: cannot open '/var/log/vpxa.log' for reading: Permission denied`** — Run the command with `sudo` or as root to access ESXi host logs.
    **`[7F2A4C1B9700 error 'Hostd'] Connection to vCenter failed: timeout`** — Verify network connectivity to vCenter and check firewall rules on port 443.
If an agent is stopped or crashed, restart it:

```bash
/etc/init.d/vpxa restart
/etc/init.d/hostd restart
```


```text title="Expected output"
Stopping vpxa:                                             [  OK  ]
Starting vpxa:                                             [  OK  ]
Stopping hostd:                                            [  OK  ]
Starting hostd:                                            [  OK  ]
```

!!! warning "Common errors"
    **`vpxa: unrecognized service`** — Verify the ESXi host is running and the vpxa service exists by checking `/etc/init.d/vpxa` file permissions and presence.
    **`hostd: command not found`** — Ensure you are running these commands directly on the ESXi host (not a remote system) with root privileges.
Wait 60–90 seconds, then attempt the vCenter Reconnect action again.

---

## 5. Verify Management Network Configuration

Confirm vmk0 IP, gateway, and DNS have not drifted after a failed configuration change or DHCP interference.

```bash
esxcli network ip interface ipv4 get
esxcli network ip route ipv4 list
esxcli system hostname get
```


```text title="Expected output"
Name  IPv4 Address      IPv4 Netmask      IPv4 Broadcast    Address Type  DHCP DNS
----  ---------------   ----------------  ----------------  -----------   ---------
vmk0  192.168.1.105     255.255.255.0     192.168.1.255     STATIC        false
vmk1  10.20.30.50       255.255.255.0     10.20.30.255      STATIC        false
vmk2  172.16.0.100      255.255.255.0     172.16.0.255      DHCP          true

Destination     Netmask         Gateway         Interface
-----------     -------         -------         ---------
0.0.0.0         0.0.0.0         192.168.1.1     vmk0
192.168.1.0     255.255.255.0   0.0.0.0         vmk0
10.20.30.0      255.255.255.0   0.0.0.0         vmk1

Current Hostname: esx-prod-01.lab.local
```

!!! warning "Common errors"
    **`Error: Unknown command or namespace network ip interface ipv4 get`** — Verify esxcli is available and you are running ESXi 5.0 or later; older versions use different command syntax.
    **`Error: Unable to connect to the host`** — Ensure SSH is enabled on the ESXi host and your user account has sufficient privileges (typically root or a user in the administrators group).
Look for: vmk0 shows the correct static IP, default gateway is present, FQDN matches what vCenter has registered. Any mismatch prevents reconnection even after agent restarts.

---

## 6. Verify DNS Resolution

ESXi must resolve the vCenter FQDN — a broken DNS lookup blocks vpxa even when IP connectivity is fine.

```bash
nslookup vcenter.domain.local
cat /etc/resolv.conf
esxcli network ip dns server list
```


```text title="Expected output"
Server:		10.0.0.1
Address:	10.0.0.1#53

Name:	vcenter.domain.local
Address: 192.168.1.50

# Generated by NetworkManager
nameserver 10.0.0.1
nameserver 10.0.0.2
search domain.local

IPv4 DNS Servers
   10.0.0.1
   10.0.0.2
```

!!! warning "Common errors"
    **`nslookup: can't resolve 'vcenter.domain.local': No address associated with hostname`** — Verify the DNS server is reachable and the hostname exists in DNS; check `/etc/resolv.conf` has correct nameserver entries.
    **`cat: /etc/resolv.conf: No such file or directory`** — This file may not exist on some ESXi hosts; use `esxcli network ip dns server list` instead to verify DNS configuration.
    **`Could not connect to Management Agent on localhost`** — Run the commands directly on the ESXi host via SSH or vSphere Client console, not from a remote system without proper credentials.
Correct a missing DNS server:

```bash
esxcli network ip dns server add --server <dns-ip>
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Unknown option or parameter: --server`** — Use the correct syntax `esxcli network ip dns server add -a <dns-ip>` (the flag is `-a`, not `--server`).
    **`Error: Connect to localhost failed. Connection refused`** — Ensure you are running this command directly on an ESXi host with SSH enabled, not from a remote vSphere client; alternatively, use `esxcli -s <host-ip> -u root -p <password>` to target the host remotely.
Look for: `nslookup` returns the correct vCenter IP; no "NXDOMAIN" or timeout errors.

---

## 7. Check NTP — Time Drift Causes SSL Failures

A time difference of more than 60 seconds between the host and vCenter causes TLS handshake failures that look identical to certificate errors.

```bash
esxcli system ntp get
ntpq -p
date
```


```text title="Expected output"
NTP Enabled: true
NTP Servers: 10.20.30.40, 10.20.30.41
NTP Service Running: true

     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
 10.20.30.40     .LOCL.          1 u   64   64  377    2.341   -0.523   1.204
 10.20.30.41     .LOCL.          1 u   62   64  377    2.156    0.412   0.987
 ntp.ubuntu.com  193.67.79.202   2 u   58   64  377   18.523    1.234   2.156

Thu Mar 14 09:47:23 UTC 2024
```

!!! warning "Common errors"
    **`NTP Enabled: false`** — Enable NTP with `esxcli system ntp set --enabled=true` and start the service with `systemctl start ntpd`.
    **`reach   0`** — Verify network connectivity to NTP servers and check firewall rules allowing UDP port 123 outbound from the ESXi host.
    **`command not found: ntpq`** — Install the ntp client package or use `esxcli system ntp get` alone if ntpq is unavailable on your ESXi version.
Look for: offset column in `ntpq -p` output beyond ±60,000 ms (60 seconds) from the reference server. Compare `date` output on the host with vCenter system time to confirm drift.

Fix NTP if drifted — see the
[NTP Drift Scenario](ntp-drift-sso-certificate/index.md) for the full remediation procedure.

---

## 8. Read Logs for Root Cause

After any restarts, read logs to confirm the error is resolved and document the root cause.

```bash
tail -100 /var/log/hostd.log | grep -iE "error|ssl|certificate|timeout|refused"
tail -100 /var/log/vpxa.log  | grep -iE "error|ssl|certificate|timeout|refused"
```


```text title="Expected output"
2024-01-15T09:42:33.847Z [7F2A1B4C] [ssl] Certificate validation failed for peer 192.168.1.50
2024-01-15T09:43:01.221Z [7F2A1B4D] [error] Connection timeout to vCenter server vc.internal.local:443
2024-01-15T09:44:15.556Z [7F2A1B4E] [ssl] Unable to load certificate chain from /etc/vmware/ssl/rui.crt
2024-01-15T09:45:22.889Z [7F2A1B4F] [error] SSL_ERROR_HANDSHAKE_FAILURE_ALERT: peer refused connection
2024-01-15T09:46:08.112Z [7F2A1B50] [certificate] Certificate expires in 45 days
2024-01-15T09:47:33.445Z [7F2A1B51] [error] Timeout waiting for hostd response after 30 seconds
2024-01-15T09:48:19.778Z [7F2A1B52] [ssl] TLS version mismatch: client requested TLSv1.0, server requires TLSv1.2
```

!!! warning "Common errors"
    **`tail: cannot open '/var/log/hostd.log' for reading: No such file or directory`** — Verify the ESXi host is running and the log file path is correct; check if you're on the correct host or if logs have been rotated.
    **`grep: (standard input) is empty`** — This occurs when the log file exists but has no matching entries; it's not an error condition, just no matching lines found.
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


```text title="Expected output"
Stopping NSX Operations Agent...                                    [  OK  ]
Starting NSX Operations Agent...                                    [  OK  ]
Stopping NSX Message Processing Agent...                           [  OK  ]
Starting NSX Message Processing Agent...                           [  OK  ]
```

!!! warning "Common errors"
    **`/etc/init.d/nsx-opsagent: No such file or directory`** — Verify NSX is installed on this host and the service paths are correct with `ls -la /etc/init.d/ | grep nsx`.
    **`Job for nsx-opsagent.service failed because the control process exited with error code.`** — Check service logs with `journalctl -u nsx-opsagent -n 50` to identify the underlying startup failure.
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

- [vCenter Down / Unreachable](vcenter-down/index.md) — when multiple hosts disconnect simultaneously,
  vCenter itself may be the failing component rather than the individual hosts.
- [NTP Drift Causing SSO or Certificate Errors](ntp-drift-sso-certificate/index.md) — the full NTP
  diagnosis and remediation procedure referenced in Step 7.
- [PSOD — ESXi Kernel Panic](psod-esxi-kernel-panic/index.md) — if the host is unreachable at the
  network layer with no management network response, a PSOD may be the cause.
