---
tags:
  - san
  - troubleshooting
search:
  boost: 1.5
---
# Cisco DCNM — Troubleshooting Common Issues

*Applies to: Cisco MDS / NX-OS*
![Cisco DCNM — Troubleshooting Common Issues](../../../../assets/san-cisco-cisco-dcnm-troubleshooting-common-issues.svg)

```bash
# Step 1: Test SSH from DCNM to the switch
ssh -o ConnectTimeout=5 -o BatchMode=yes dcnm_mgmt@<switch-ip> 'show version' 2>&1
# If fails: SSH connectivity problem

# Step 2: Test SNMP
snmpget -v3 -u dcnm_poll -l authPriv -a SHA -A <auth-pass> \
  -x AES -X <priv-pass> <switch-ip> sysDescr.0
# If fails: SNMP credentials mismatch or network issue

# Step 3: Check DCNM discovery log
grep "<switch-ip>" /var/log/dcnm/discovery.log | tail -30
```


```text title="Expected output"
Cisco Nexus Operating System (NX-OS) Software
TAC support: http://www.cisco.com/tac
Copyright (c) 2002-2023, Cisco and/or its affiliates
Kernel uptime is 127 day(s), 14 hour(s), 22 minute(s), 58 second(s)
Last reset at 1234567890 (Wed Mar 15 10:22:30 2023)
Reason: Requested reload
System uptime is 126 day(s), 23 hour(s), 11 minute(s), 12 second(s)

SNMPv3 User-based Security Model (USM) User Table
Engine ID: 800007E5-03A0B8C10F4E
User Name: dcnm_poll
Authentication Protocol: HMAC-SHA
Privacy Protocol: AES

2024-01-18T14:32:15.847Z [INFO] Discovery initiated for switch 192.168.1.105
2024-01-18T14:32:18.923Z [INFO] SSH authentication successful for 192.168.1.105
2024-01-18T14:32:21.156Z [INFO] SNMP polling enabled for 192.168.1.105
2024-01-18T14:32:45.234Z [INFO] Device 192.168.1.105 added to inventory (N9K-C93180YC-EX)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Permission denied (publickey,password)` | Verify dcnm_mgmt user exists on switch and SSH key/password is correct in DCNM credentials. |
    | `Timeout: No Response from 192.168.1.x` | Confirm network connectivity to switch IP, firewall rules allow SNMP/SSH ports, and switch management interface is reachable. |
    | `No such file or directory: /var/log/dcnm/discovery.log` | Verify DCNM service is running with `systemctl status dcnm` and check correct log path for your DCNM installation. |
```bash
# Check PM service status
systemctl status dcnm-pm

# Check PM log for polling errors
tail -f /var/log/dcnm/pm.log | grep -i "error\|timeout\|failed"

# Restart PM service
systemctl restart dcnm-pm

# Verify SNMP polling is working manually
snmpwalk -v3 -u dcnm_poll -l authPriv -a SHA -A <auth-pass> \
  -x AES -X <priv-pass> <switch-ip> ifInOctets
# Expected: output with interface counter values
```

```text title="Expected output"
● dcnm-pm.service - Cisco DCNM Policy Manager
     Loaded: loaded (/usr/lib/systemd/system/dcnm-pm.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2h 45min ago
   Main PID: 8742 (java)
      Tasks: 47 (limit: 4096)
     Memory: 512.3M
        CPU: 18min 32.450s
     CGroup: /system.slice/dcnm-pm.service
             └─8742 /usr/lib/jvm/java-11-openjdk/bin/java -Xmx2g...

2024-01-15 14:45:22 dcnm-pm[8742]: ERROR [PollingThread-12] Timeout polling switch 10.48.22.105 after 30s
2024-01-15 14:46:15 dcnm-pm[8742]: ERROR [SNMPv3Handler] Authentication failed for user dcnm_poll on 10.48.22.106
2024-01-15 14:47:03 dcnm-pm[8742]: WARN [PollingThread-8] Failed to retrieve ifInOctets from 10.48.22.104

Restarting dcnm-pm.service...
Job for dcnm-pm.service is queued for restart, will take approx. 45 seconds.

SNMPv3 Session Details:
User Name:            dcnm_poll
Authentication:       SHA
Privacy:              AES
Engine ID:            0x80001f8800051a2c4f5a3b
Boots:                1247

IF-MIB::ifInOctets.1 = Counter64: 2847362951
IF-MIB::ifInOctets.2 = Counter64: 1923847502
IF-MIB::ifInOctets.3 = Counter64: 4102938475
IF-MIB::ifInOctets.4 = Counter64: 892374619
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `snmpwalk: Unknown user name dcnm_poll` | Verify the SNMPv3 user exists on the switch with `show snmp user` and matches the credentials in DCNM PM configuration. |
    | `Timeout: No Response from <switch-ip>` | Check network connectivity to the switch IP, verify SNMP port 161 is open in firewall rules, and confirm the switch is reachable with `ping <switch-ip>`. |
    | `Authentication failed for user dcnm_poll` | Ensure the authentication password and privacy password match exactly what is configured on the switch, and verify the switch supports SHA/AES algorithms with `show snmp engineID`. |
```bash
# Test LDAP from DCNM appliance
ldapsearch -H ldaps://ldap.corp.example.com \
  -D "CN=dcnm-svc,OU=Service Accounts,DC=corp,DC=example,DC=com" \
  -w <password> \
  -b "DC=corp,DC=example,DC=com" \
  "(sAMAccountName=<test-user>)"
```

```text title="Expected output"
# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=example,DC=com> with scope subtree
# filter: (sAMAccountName=testuser)
# requesting: ALL
#

# testuser, Users, corp.example.com
dn: CN=testuser,CN=Users,DC=corp,DC=example,DC=com
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: testuser
sn: User
givenName: Test
mail: testuser@corp.example.com
memberOf: CN=dcnm-admins,CN=Groups,DC=corp,DC=example,DC=com
userAccountControl: 512
pwdLastSet: 133412567890123456

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ldap_sasl_bind(SIMPLE): Can't contact LDAP server (-1)` | Verify LDAP server hostname/IP is reachable and port 636 is open; check firewall rules from DCNM appliance to LDAP server. |
    | `ldap_bind: Invalid credentials (49)` | Confirm the service account password is correct and the DN format matches your Active Directory structure exactly. |
    | `ldap_search: No such object (32)` | Verify the base DN `DC=corp,DC=example,DC=com` exists in your directory and matches your domain structure. |
```bash
# Check resource usage
top -b -n 1 | head -20
free -h

# Check disk I/O
iostat -x 1 5

# Check database connections
psql -U postgres -c "SELECT count(*) FROM pg_stat_activity WHERE state='active';"
# If > 50 active connections: connection pool exhaustion

# Check for runaway queries
psql -U postgres -c "
SELECT pid, now() - query_start AS duration, query 
FROM pg_stat_activity 
WHERE state = 'active' 
ORDER BY duration DESC 
LIMIT 10;"

# Restart DCNM if Java memory leak suspected
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server restart
```

```text title="Expected output"
top - 14:32:18 up 18 days,  3:45,  2 users,  load average: 2.14, 1.87, 1.62
Tasks: 247 total,   3 running, 244 sleeping,   0 stopped,   0 zombie
%Cpu(s):  18.2 us,  4.3 sy,  0.0 ni, 76.8 id,  0.5 wa,  0.2 hi,  0.0 si,  0.0 st
MiB Mem :  32768.0 total,  24512.3 free,   6144.2 used,   2111.5 buff/cache
MiB Swap:   8192.0 total,   8192.0 free,      0.0 used.  25856.1 avail Mem

  PID USER      PR  NI    VIRT    RES  SHR S  %CPU %MEM     TIME+ COMMAND
 4521 root      20   0 8456320 2048m  45m S  42.1 6.4   1247:33 java
 8934 postgres  20   0  892456  512m  28m S  12.3 1.6    456:12 postgres
 1203 root      20   0  234567   89m  12m S   3.2 0.3     78:45 dcnm-server
...

              total        used        free      shared  buff/cache   available
Mem:           31Gi       6.2Gi        24Gi       512Mi       1.2Gi        25Gi
Swap:          8.0Gi          0B       8.0Gi

Linux 5.10.0-8-amd64 (dcnm-prod-01) 	01/15/2025 	_x86_64_	(16 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
          18.45    0.12    4.23    2.34    0.00   74.86

Device            r/s     w/s     rMB/s     wMB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz %util
sda              45.2   123.4      2.1       8.7     2.1      18.3   4.4   12.9   12.3    28.4   3.45  18.2
sdb              12.1    34.5      0.8       2.3     0.5       4.2   3.9   10.8    8.1    15.2   0.89   5.3

 count
------
    47
(1 row)

   pid   |   duration   |                                    query
---------+--------------+---------------------------------------------------------------
  18234  | 00:12:34.567 | SELECT * FROM fabric_inventory WHERE status='sync' LIMIT 1000
  18456  | 00:08:23.123 | UPDATE device_config SET last_sync=now() WHERE device_id=...
  18567  | 00:05:12.890 | SELECT count(*) FROM
```
```bash
# Capture to confirm traps are arriving
sudo tcpdump -i eth0 -n udp port 162 -c 20

# If not arriving: confirm trap destination on the switch
# On MDS switch:
show snmp host
# Should list DCNM IP

# If arriving but not processed: check event manager
tail -f /var/log/dcnm/events.log | grep "trap\|SNMP"

# Restart event service
systemctl restart dcnm-events
```

```text title="Expected output"
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
22:14:33.445821 IP 10.48.12.55.40821 > 10.48.12.200.162: UDP, length 156
22:14:34.112547 IP 10.48.12.55.40821 > 10.48.12.200.162: UDP, length 148
22:14:35.667890 IP 10.48.12.55.40821 > 10.48.12.200.162: UDP, length 152
22:14:36.334521 IP 10.48.12.55.40821 > 10.48.12.200.162: UDP, length 160
22:14:37.891234 IP 10.48.12.55.40821 > 10.48.12.200.162: UDP, length 144
20 packets captured
20 packets received by filter
0 packets dropped by kernel

SNMP host IP address: 10.48.12.200
Community: public
Trap port: 162

2024-01-15T22:14:33.521Z [INFO] SNMP trap received from 10.48.12.55 (MDS9706-01)
2024-01-15T22:14:34.089Z [INFO] Processing linkDown trap for port Ethernet1/1
2024-01-15T22:14:35.667Z [DEBUG] Trap OID: 1.3.6.1.6.3.1.1.5.3
2024-01-15T22:14:36.334Z [INFO] Event queued for fabric-01

(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `tcpdump: eth0: No such device` | Verify the correct interface name with `ip link show` and replace eth0 with the actual interface (e.g., ens0, bond0). |
    | `tail: cannot open '/var/log/dcnm/events.log' for reading: No such file or directory` | Confirm DCNM is installed and running with `systemctl status dcnm-events`, or check the correct log path with `find /var/log -name '*dcnm*'`. |
    | `Failed to restart dcnm-events.service: Unit dcnm-events.service not found.` | Verify the correct service name with `systemctl list-units --type=service | grep dcnm` and use the actual service name. |
```bash
# Check upgrade log
tail -100 /var/log/dcnm/install.log

# Check if DCNM services started after upgrade
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server status

# Check for database migration errors (common cause of upgrade failure)
grep -i "liquibase\|migration\|flyway\|ERROR" /var/log/dcnm/install.log

# If upgrade is unrecoverable: revert to pre-upgrade VM snapshot
# Then contact Cisco TAC with the install log
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

A1: "A1" {shape: rectangle}
A2: "Fix network / firewall\nVerify mgmt IP and creds" {shape: rectangle}
A3: "Re-add switch\nCheck SNMP v3 auth settings" {shape: rectangle}
A4: "Fabric and Switch Issues" {shape: rectangle}
B: "B" {shape: rectangle}
B1: "grep discovery.log\nVerify SSH and SNMP v3 creds\nCheck domain ID conflicts" {shape: rectangle}
B2: "Fabric and Switch Issues" {shape: rectangle}
C: "C" {shape: rectangle}
C1: "systemctl status dcnm-pm\nCheck SNMP poll manually\nRestart PM service" {shape: rectangle}
C2: "Performance Issues" {shape: rectangle}
D: "D" {shape: rectangle}
D1: "Check Elasticsearch disk: df -h\nPrune old performance data\nRestart DCNM if Java heap full" {shape: rectangle}
D2: "Performance Issues" {shape: rectangle}
E: "E" {shape: rectangle}
E1: "journalctl DCNM errors\nCheck DB connections\nReview install.log for migration fail" {shape: rectangle}
E2: "Auth and Platform Issues" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}
A: "A" {shape: rectangle}

A1 -> A2
A1 -> A3
A3 -> A4
B -> B1
B1 -> B2
C -> C1
C1 -> C2
D -> D1
D1 -> D2
E -> E1
E1 -> E2
```

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Cisco Dcnm — Diagnostics](../diagnostics/)
- [Cisco Dcnm — Escalation](../escalation/)
- [Cisco Dcnm — Health Checks](../../operations/health-checks/)
