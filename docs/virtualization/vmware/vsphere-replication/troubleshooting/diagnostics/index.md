---
tags:
  - troubleshooting
  - vmware
  - vsphere-replication
---
# vSphere Replication — Diagnostics


<div class="kb-summary">
Diagnostics reference covering VRA Log Locations, Collect VRA Support Bundle, Check VRA Service Status, Test Connectivity from Source ESXi to Target VRA, Check ESXi hbrsvc (Replication Source Service) and 4 more sections.

*Applies to: vSphere Replication 8.x*
</div>

  VR Diagnostic Data Sources
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  VRA Appliance (both sites)    ESXi Source Host                                                       │
│  ┌───────────────────────┐     ┌─────────────────────────┐                                            │
│  │ VAMI → Support Bundle │     │ /var/log/hbr.log        │                                            │
│  │ /opt/vmware/logs/hms/ │     │ /var/log/hostd.log      │                                            │
│  │ /opt/vmware/logs/vrms/│     │ /etc/init.d/hbrsvc stat │                                            │
│  │ journalctl -u hms     │     │ nc -vz <VRA> 31031      │                                            │
│  │ journalctl -u vrms    │     └─────────────────────────┘                                            │
│  └───────────────────────┘                                                                            │
│                                                                                                       │
│  Connectivity Tests              vCenter                                                              │
│  ┌───────────────────────┐     ┌─────────────────────────┐                                            │
│  │ ESXi → VRA:31031      │     │ Monitor → Recent Tasks  │                                            │
│  │ VRA → VRA:44046       │     │ filter "HBR" / "VR"     │                                            │
│  │ openssl s_client :443 │     │ Export System Logs      │                                            │
│  │ REST /api/rest/vr/    │     └─────────────────────────┘                                            │
│  │   health (no auth)    │                                                                            │
│  └───────────────────────┘                                                                            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## VRA Log Locations

```bash
ssh admin@vra-london.example.local

# Main VRA application logs:
/opt/vmware/logs/hms/          # Home Management Server logs
/opt/vmware/logs/vrms/         # VRA management service

# System logs:
/var/log/messages              # OS syslog
journalctl -u hms -f           # Follow HMS log
journalctl -u vrms -f          # Follow VRMS log
journalctl -u nginx -f         # Follow nginx (API gateway) log
```

---

## Collect VRA Support Bundle

```text
VRA VAMI (https://vra-london.example.local:5480)
  → Support → Generate Support Bundle → Download

The bundle includes: all VRA logs, configuration, service state
```

Manual collection if VAMI is unreachable:
```bash
ssh admin@vra-london.example.local
/opt/vmware/support/support-bundle.sh
# Bundle location: /tmp/vr-support-<timestamp>.tar.gz
scp admin@vra-london.example.local:/tmp/vr-support-*.tar.gz /local/path/
```

---

## Check VRA Service Status

```bash
ssh admin@vra-london.example.local

# Core services:
systemctl status hms        # Should be: active (running)
systemctl status vrms       # Should be: active (running)
systemctl status nginx      # Should be: active (running)

# If stopped:
systemctl start hms
systemctl start vrms
```

---

## Test Connectivity from Source ESXi to Target VRA

```bash
# SSH to source ESXi host
ssh root@<source-esxi-ip>

# Test replication data port (31031):
nc -vz <target-vra-ip> 31031
# Success: "Connection to <ip> 31031 port [tcp] succeeded!"
# Failure: "Connection refused" or timeout → firewall issue

# Test VRA management port (44046):
nc -vz <target-vra-ip> 44046

# VMkernel ping:
vmkping -I vmk0 <target-vra-ip>

# Or using vmkping on specific VMkernel adapter:
vmkping -I vmk1 <target-vra-ip>
```

---

## Check ESXi hbrsvc (Replication Source Service)

```bash
# SSH to source ESXi host
ssh root@<source-esxi-host>

# Check replication service:
/etc/init.d/hbrsvc status

# View hbr log:
tail -100 /var/log/hostd.log | grep -i hbr
tail -100 /var/log/hbr.log

# List active replication tasks on this host:
esxcli vm process list | grep -i replication
```

---

## Verify VRA Certificate

```bash
# Check VRA management interface cert:
echo | openssl s_client -connect vra-london.example.local:443 -servername vra-london.example.local 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer

# Check VRA inter-site port cert:
echo | openssl s_client -connect vra-amsterdam.example.local:44046 2>/dev/null \
  | openssl x509 -noout -dates -subject
```

---

## Review Replication Task Status in vCenter

```text
vCenter → Monitor → Recent Tasks
  Filter by: "vSphere Replication" or "HBR" in task description
  Stuck tasks: right-click → Cancel Task (only if truly stuck >30 min)
```

---

## REST API Health Check

```bash
# Quick health check (no auth required):
curl -sk https://vra-london.example.local/api/rest/vr/health

# Detailed status with auth:
TOKEN=$(curl -sk -X POST \
  https://vra-london.example.local/api/rest/vr/authentication/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<pass>"}' | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['token'])")

curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-london.example.local/api/rest/vr/replications" | \
  python3 -m json.tool
```

---

## Capture Network Traffic on Replication Port

```bash
# On source ESXi host — capture replication traffic (TCP 31031):
pktcap-uw --vmk vmk0 --dstport 31031 -o /tmp/hbr-capture.pcap --count 1000

# Transfer and analyze in Wireshark:
scp root@<esxi-host>:/tmp/hbr-capture.pcap /local/path/
```
