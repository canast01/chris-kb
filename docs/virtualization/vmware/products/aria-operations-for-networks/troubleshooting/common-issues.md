---
tags:
  - aria-networks
  - troubleshooting
  - vmware
search:
  boost: 1.5
description: "Troubleshooting guide for the most frequent Aria Operations for Networks problems: data source showing red, no flows in Flow Map, collector offline, LDAP..."
---
# Aria Operations for Networks — Common Issues

<div class="kb-summary">
Troubleshooting guide for the most frequent Aria Operations for Networks problems: data source showing red, no flows in Flow Map, collector offline, LDAP login failure, path analysis gaps, and high disk usage.

*Applies to: Aria Operations for Networks 6.x*
</div>
![Aria Operations for Networks — Common Issues](../../../../../assets/virtualization-vmware-aria-operations-for-networks-troublesh.svg)

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
data_source_red_collection_failed: "Data Source Red / Collection Failed" {shape: rectangle}
no_flows_in_flow_map: "No Flows in Flow Map" {shape: rectangle}
collector_offline_in_ui: "Collector Offline in UI" {shape: rectangle}
path_analysis_showing_no_path_or_inc: "Path Analysis Showing No Path or Incomplete Path" {shape: rectangle}
ldap_ad_login_failure: "LDAP / AD Login Failure" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> data_source_red_collection_failed: investigate
symptom -> no_flows_in_flow_map: investigate
symptom -> collector_offline_in_ui: investigate
symptom -> path_analysis_showing_no_path_or_inc: investigate
symptom -> ldap_ad_login_failure: investigate
diagnostic_flow -> resolution
data_source_red_collection_failed -> resolution
no_flows_in_flow_map -> resolution
collector_offline_in_ui -> resolution
path_analysis_showing_no_path_or_inc -> resolution
ldap_ad_login_failure -> resolution
```

## Diagnostic Flow

```d2
direction: right

S: "What is the symptom?" {shape: rectangle}
B1: "Data source red / collection failed" {shape: rectangle}
B2: "No flows in Flow Map" {shape: rectangle}
B3: "Path analysis shows no path" {shape: rectangle}
B4: "Physical device not discovered" {shape: rectangle}
B5: "Collector offline in UI" {shape: rectangle}
B6: "LDAP login failure" {shape: rectangle}
D1: "D1" {shape: rectangle}
R1: "Fix API Connectivity · Update Credentials · Re-\naccept Cert" {shape: rectangle}
R2: "Check Service Account Lock · Run Test Connection" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Set IPFIX Target to Collector IP · Enable on vDS" {shape: rectangle}
R4: "Check UDP 2055 Firewall · Review proxy.log" {shape: rectangle}
R5: "Verify All Source Devices Discovered · Check NSX\nData Source" {shape: rectangle}
R6: "Add Device via SNMP · Verify Credentials · Check\nCollector Reachability" {shape: rectangle}
D3: "D3" {shape: rectangle}
R7: "Power on Collector VM" {shape: rectangle}
R8: "Restart ni-collector service · Re-register in UI" {shape: rectangle}
R9: "Test LDAP Bind DN · Check LDAPS Cert · Use LDAP\nBrowser Tool" {shape: rectangle}

S -> B1
S -> B2
S -> B3
S -> B4
S -> B5
S -> B6
D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
B3 -> R5
B4 -> R6
D3 -> R7
D3 -> R8
B6 -> R9
```

---

## Before you begin

- **Access:** AON UI admin; SSH to platform VM (`ubuntu`) and collector VMs
- **Baseline:** check collector health first — if the collector is offline, all other issues follow from it
- **Log files:** `app.log` on platform VM; `proxy.log` on each collector VM

---

## Data Source Red / Collection Failed

**Symptoms:** Data source shows red status or "Collection Failed" in AON UI → Settings → Data Sources.

```bash
# From the collector VM — test API connectivity to the data source
# vCenter:
curl -sk https://vcenter.corp.local/rest/com/vmware/cis/session \
  -X POST -u 'svc-aon:PASSWORD' -o /dev/null -w "HTTP %{http_code}\n"
# Expected: HTTP 200

# NSX-T:
curl -sk https://nsxmgr.corp.local/api/v1/cluster \
  -u 'svc-aon:PASSWORD' -o /dev/null -w "HTTP %{http_code}\n"
# Expected: HTTP 200
```


```text title="Expected output"
HTTP 200
HTTP 200
```

!!! warning "Common errors"
    **`HTTP 401`** — Verify the service account credentials are correct and the password hasn't expired in vCenter or NSX-T.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip SSL verification, or import the data source's CA certificate into the collector VM's trust store.
    **`curl: (7) Failed to connect to vcenter.corp.local port 443: Connection timed out`** — Confirm network connectivity and firewall rules allow the collector VM to reach the data source on port 443.
**Common causes and fixes:**

| Cause | Indicator | Fix |
|---|---|---|
| Wrong credentials | "Authentication failed" in data source details | Update credentials in Settings → Data Sources |
| Service account locked | AD lockout event in DC event log | Unlock account; check for auth storm from AON |
| TLS cert mismatch | "Certificate error" message | Re-accept thumbprint in data source settings, or upload correct CA to AON |
| API endpoint unreachable | `curl` times out | Check firewall; verify AON collector can reach data source on TCP 443 |
| Service account permissions | "Access denied" on specific API calls | Re-verify service account roles (vCenter read-only, NSX Auditor minimum) |

**Re-test after fixing:**
```bash
# Use AON UI built-in test:
# Settings → Data Sources → select source → Test Connection
# Or trigger re-sync via REST:
curl -sk -X POST "${AON_URL}/api/ni/datasources/${DS_ID}/sync" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}"
```


```text title="Expected output"
{
  "id": "ds-12847-prod-vcenter",
  "name": "vCenter-Cluster-01",
  "type": "vCenter",
  "lastSyncTime": "2024-01-15T14:32:18Z",
  "syncStatus": "COMPLETED",
  "recordsProcessed": 2847,
  "duration": "45s"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification, or import the AON certificate into your system trust store.
    **`{"error": "Unauthorized", "code": 401}`** — Verify the `AON_TOKEN` is valid and not expired by checking Settings → Administration → API Tokens in the AON UI.
    **`curl: (7) Failed to connect to aon-prod.example.com port 443: Connection refused`** — Confirm `AON_URL` is correct and the AON appliance is running and network-accessible from your client.
---

## No Flows in Flow Map

**Symptoms:** Flow Map is empty or shows only partial data; specific VMs show no flows.

**Triage order:**
1. Confirm collector is online (see Collector Offline below)
2. Check IPFIX is configured to send to the collector IP

```bash
# On collector VM — verify UDP 2055 packets are arriving from switches/vDS
sudo tcpdump -i eth0 -n udp port 2055 -c 50
# If 0 packets: IPFIX is not reaching this collector

# Check proxy.log for flow receipt
sudo tail -100 /var/log/proxy.log | grep -E "received|forward|error"
```


```text title="Expected output"
tcpdump: verbose output suppressed, use -v or -vv for full packet decode
listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
22:14:33.445821 IP 10.45.12.88.54321 > 192.168.1.50.2055: UDP, length 1472
22:14:33.512047 IP 10.45.12.89.54322 > 192.168.1.50.2055: UDP, length 1472
22:14:34.103456 IP 10.45.13.201.54323 > 192.168.1.50.2055: UDP, length 1456
22:14:34.667892 IP 10.45.12.88.54324 > 192.168.1.50.2055: UDP, length 1472
22:14:35.234561 IP 10.45.13.202.54325 > 192.168.1.50.2055: UDP, length 1464
22:14:35.891234 IP 10.45.12.89.54326 > 192.168.1.50.2055: UDP, length 1472
50 packets captured
50 packets received by filter
0 packets dropped by kernel

2024-01-15 22:14:33 [INFO] Flow record received from 10.45.12.88 (vDS-prod-01): 2847 flows
2024-01-15 22:14:34 [INFO] Flow record received from 10.45.13.201 (sw-core-01): 1923 flows
2024-01-15 22:14:34 [INFO] Forward to analytics engine: batch_id=ae7f2c91-4d22-11ee-b56e-0242ac110002
2024-01-15 22:14:35 [INFO] Flow record received from 10.45.12.89 (vDS-prod-02): 3156 flows
2024-01-15 22:14:35 [INFO] Forward to analytics engine: batch_id=ae7f2d12-4d22-11ee-b56e-0242ac110002
```

!!! warning "Common errors"
    **`tcpdump: Permission denied`** — Run the command with `sudo` or add your user to the `tcpdump` group with `sudo usermod -aG tcpdump $USER`.
    **`grep: /var/log/proxy.log: No such file or directory`** — Verify the collector service is running with `sudo systemctl status aria-collector` and check the actual log path in `/var/log/aria/` or `/opt/aria/logs/`.
**IPFIX not configured on vDS:**
```text
vSphere Client → Distributed Switch → Configure → NetFlow
  Collector IP: <AON collector IP>
  Collector Port: 2055
  Active flow export timeout: 60s
  Idle flow export timeout: 15s
  Apply to all port groups
```

**Firewall blocking UDP 2055:**
- Physical switches must send IPFIX to the collector IP on UDP 2055
- Network firewall between switches and collector must allow UDP 2055 (not just TCP 443)

---

## Collector Offline in UI

**Symptoms:** AON UI → Settings → Infrastructure and Support → Collectors shows collector as "Offline" or "Disconnected".

```bash
# SSH to the offline collector VM
ssh ubuntu@aon-collector.corp.local

# Check if collector service is running
sudo systemctl status ni-collector

# Restart collector service
sudo systemctl restart ni-collector
sudo systemctl status ni-collector   # verify running

# Check collector can reach platform VM
nc -zv aon-platform.corp.local 443
# If unreachable: firewall or DNS issue — fix connectivity first

# View collector logs for errors
sudo journalctl -u ni-collector -n 100 --no-pager | grep -i "error\|fail\|warn"
```


```text title="Expected output"
ubuntu@aon-collector:~$ sudo systemctl status ni-collector
● ni-collector.service - Aria Operations for Networks Collector
     Loaded: loaded (/etc/systemd/system/ni-collector.service; enabled; vendor preset: enabled)
     Active: inactive (dead) since Thu 2024-01-18 14:32:15 UTC; 2min 43s ago
ubuntu@aon-collector:~$ sudo systemctl restart ni-collector
ubuntu@aon-collector:~$ sudo systemctl status ni-collector
● ni-collector.service - Aria Operations for Networks Collector
     Loaded: loaded (/etc/systemd/system/ni-collector.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2024-01-18 14:34:52 UTC; 1s ago
     Process: 8742 ExecStart=/opt/ni/collector/bin/collector.sh start (code=exited, status=0/SUCCESS)
ubuntu@aon-collector:~$ nc -zv aon-platform.corp.local 443
Connection to aon-platform.corp.local 443 port [tcp/https] succeeded!
ubuntu@aon-collector:~$ sudo journalctl -u ni-collector -n 100 --no-pager | grep -i "error\|fail\|warn"
Jan 18 14:34:53 aon-collector ni-collector[8751]: WARN: Retrying connection to platform at 10.42.8.15:443 (attempt 2/5)
Jan 18 14:35:01 aon-collector ni-collector[8762]: ERROR: Failed to load SSL certificate from /etc/ni/certs/collector.pem
```

!!! warning "Common errors"
    **`sudo: command not found`** — Verify the user has sudo privileges or log in as root; check `/etc/sudoers` includes the ubuntu user.
    **`Connection refused`** — Ensure the ni-collector service is actually running with `systemctl status ni-collector` and check firewall rules allow outbound 443 to the platform VM.
    **`ERROR: Failed to load SSL certificate from /etc/ni/certs/collector.pem`** — Regenerate or restore the collector certificate bundle using the platform's certificate management tool or re-register the collector.
**If service restart doesn't fix it — re-register in UI:**
```text
AON UI → Settings → Infrastructure and Support → Collectors
  Select offline collector → Re-register
  Copy the pairing key shown
```

```bash
# On the collector VM, run the re-pairing script
sudo /home/ubuntu/support/pairing.sh
# Enter platform FQDN and paste the pairing key
```


```text title="Expected output"
Aria Operations for Networks - Collector Re-pairing Script
===========================================================

Checking collector status... OK
Current platform: platform.example.com
Collector UUID: 550e8400-e29b-41d4-a716-446655440000

Enter platform FQDN [platform.example.com]: 
Enter pairing key: 
Validating pairing key... OK
Connecting to platform at platform.example.com:443... Connected
Registering collector... OK
Collector re-paired successfully
Restarting services... Done

Pairing complete. Collector is now active.
```

!!! warning "Common errors"
    **`sudo: /home/ubuntu/support/pairing.sh: command not found`** — Verify the script exists at that path and run `ls -la /home/ubuntu/support/pairing.sh` to confirm permissions and location.
    **`Validating pairing key... FAILED - Invalid or expired key`** — Obtain a fresh pairing key from the Aria Operations platform UI under Administration > Collectors and re-run the script.
    **`Connecting to platform at platform.example.com:443... Connection refused`** — Verify network connectivity to the platform FQDN with `ping platform.example.com` and confirm the platform is running and accessible on port 443.
**Collector disk full (stops forwarding flows at >85% disk usage):**
```bash
df -h /   # check root partition
sudo journalctl --vacuum-size=1G   # free journal space
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   42G  5.2G  85% /
Vacuumed journals from /var/log/journal/abc123def456 to 1.0G.
```

!!! warning "Common errors"
    **`df: '/': Permission denied`** — Run the command without `sudo` as `df` doesn't require elevated privileges, or check that the mount point exists and is accessible.
    **`sudo: journalctl: command not found`** — Install systemd-journal or verify the system uses systemd; on some minimal distributions, journalctl may not be available.
---

## Path Analysis Showing No Path or Incomplete Path

**Symptoms:** Path Analysis tool returns "No path found" or missing hops between two VMs.

**Common causes:**
- One or more network devices in the path are not discovered as data sources
- NSX-T data source not added (missing logical overlay hops)
- Physical switches not added via SNMP

```bash
# Check which data sources are configured
curl -sk -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  "${AON_URL}/api/ni/datasources" \
  | python3 -c "
import sys, json
for d in json.load(sys.stdin).get('results', []):
    print(f\"{d.get('datasource_type','?'):<25} {d.get('nickname','?'):<30} {d.get('enabled','')}\")"
```


```text title="Expected output"
vCenter                      prod-vcenter-01                  True
vCenter                      dr-vcenter-02                    True
NSX-T                        nsx-t-cluster-primary            True
vRealize Operations         vrops-instance-01                False
Kubernetes                   k8s-prod-cluster                 True
Intersight                   intersight-connector             True
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification, or import the AON server's certificate into your system trust store.
    **`jq: command not found`** — Install `python3-json` or use the provided Python one-liner instead of piping to `jq`.
    **`Authorization header missing or invalid`** — Verify `${AON_TOKEN}` is set with a valid API token by running `echo $AON_TOKEN` and regenerate it in the AON UI if expired.
**Fix:** In AON UI → Settings → Data Sources → Add Source:
- Ensure all NSX-T Managers are added
- Add physical switch SNMP credentials for switches in the path
- Add the underlay IP fabric (if spine/leaf architecture)

---

## LDAP / AD Login Failure

**Symptoms:** Users cannot log in to AON UI with AD credentials; local `admin@local` works.

```bash
# Test LDAP bind from the platform VM
ldapsearch -x -H ldap://dc.corp.local:389 \
  -D "svc-aon@corp.local" -w "PASSWORD" \
  -b "DC=corp,DC=local" "(sAMAccountName=testuser)" cn

# For LDAPS (port 636):
ldapsearch -x -H ldaps://dc.corp.local:636 \
  -D "svc-aon@corp.local" -w "PASSWORD" \
  -b "DC=corp,DC=local" "(sAMAccountName=testuser)" cn
```


```text title="Expected output"
# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=local> with scope subtree
# filter: (sAMAccountName=testuser)
# requesting: cn
#

# testuser, Users, corp.local
dn: CN=testuser,CN=Users,DC=corp,DC=local
cn: Test User

# search result
search: 2
result: 0 Success
matchedDN:
text:

# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=local> with scope subtree
# filter: (sAMAccountName=testuser)
# requesting: cn
#

# testuser, Users, corp.local
dn: CN=testuser,CN=Users,DC=corp,DC=local
cn: Test User

# search result
search: 2
result: 0 Success
matchedDN:
text:
```

!!! warning "Common errors"
    **`ldap_bind: Invalid credentials (49)`** — Verify the service account password is correct and the account is not locked in Active Directory.
    **`Can't contact LDAP server (-1)`** — Confirm the DC hostname resolves and port 389/636 is reachable from the platform VM (use `nc -zv dc.corp.local 389`).
    **`ldap_bind: Inappropriate authentication (48)`** — Remove the `-x` flag if using SASL authentication, or ensure the bind DN format matches your AD schema (try `svc-aon@corp.local` or `corp\svc-aon`).
**Common causes:**

| Cause | Fix |
|---|---|
| Wrong bind DN format | Try `svc-aon@corp.local` (UPN) vs `CN=svc-aon,OU=Service,DC=corp,DC=local` (DN) |
| LDAPS cert not trusted | Upload AD CA cert to AON: Settings → Authentication → Upload Certificate |
| Service account locked | Unlock in AD; check for auth storms from AON retrying failed binds |
| Wrong base DN | Verify `DC=corp,DC=local` matches your actual domain structure |

**Re-test:**
```text
AON UI → Settings → Authentication → Test Connection
  Enter a valid AD username and password to verify
```

---

## High Disk Usage / Data Retention

```bash
# Check disk usage (alert at 80%, collection stops at ~90%)
df -h /var/lib/cassandra    # flow data
df -h /var/lib/elasticsearch   # search index
df -h /var/log

# Free journal space
sudo journalctl --vacuum-size=1G
sudo journalctl --vacuum-time=7d
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda3       500G  412G   88G  83% /var/lib/cassandra
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda4       300G  261G   39G  87% /var/lib/elasticsearch
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       100G   78G   22G  78% /var/log
Vacuumed journals space from 2.3G to 1.0G.
Vacuumed journals space from 1.0G to 892M.
```

!!! warning "Common errors"
    **`df: /var/lib/cassandra: No such file or directory`** — Verify the Aria Operations for Networks collector node is running and the Cassandra service has initialized its data directory.
    **`sudo: journalctl: command not found`** — Remove `sudo` prefix as journalctl requires root privileges via `sudo journalctl` without redundant elevation, or run the command directly as root.
    **`Permission denied`** — Run the entire script with `sudo bash` or prefix each command with `sudo` to ensure proper permissions for system directories.
**Adjust retention in UI:**
```text
AON UI → Settings → Infrastructure and Support → Platform Settings
  Data Retention: reduce from default (6 months) to 30 days for lab; 90 days for production
```

---

---

## Verify

- Data source shows green status in Settings → Data Sources — no red indicators
- Flow Map displays flows for at least the test VMs / workloads
- Collector shows Online in Settings → Infrastructure and Support → Collectors
- AD users can log in if LDAP was the issue; test with a known-good AD account

---

## See also

- [AON Diagnostics](../diagnostics/)
- [AON Escalation](../escalation/)
- [AON Health Checks](../../operations/health-checks/)
