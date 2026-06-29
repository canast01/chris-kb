---
tags:
  - servicenow
---
# Environment Readiness Checklist

<div class="kb-summary">
Validates that infrastructure is prepared to receive a new workload, application deployment, or system migration. Complete before any provisioning begins.

*Applies to: ServiceNow*
</div>

## Readiness Assessment Flow

```d2
direction: right

A: "Workload Requirements\ndefined" {shape: rectangle}
B: "Capacity Check\nCPU · Memory · Storage · Network" {shape: rectangle}
C: "Network Readiness\nVLAN · Firewall · DNS · NTP" {shape: rectangle}
D: "Security Readiness\nBaseline · PAM · Certs" {shape: rectangle}
E: "Monitoring Readiness\nAgent · Alerting · Dashboards" {shape: rectangle}
F: "Backup Readiness\nJob · Policy · Retention" {shape: rectangle}
G: "G" {shape: rectangle}
H: "Ready — proceed\nwith onboarding" {shape: rectangle}
I: "Remediate blockers\nbefore proceeding" {shape: rectangle}

A -> B
B -> C
C -> D
D -> E
E -> F
G -> H
G -> I
```

## 2. Network Readiness

```bash
# Confirm VLAN exists on target switch/fabric
show vlan id <vlan_id>                 # Cisco
Get-VDPortgroup -VDSwitch vDS-Prod     # VMware distributed switch

# Confirm IP address allocated and not in use
ping -c 1 <planned-ip> && echo "IP IN USE" || echo "IP available"
nmap -sn <planned-ip>

# DNS A record created
nslookup <planned-hostname>.example.com
dig +short <planned-hostname>.example.com

# Firewall rules in place (test from source to destination)
nc -zv <destination-ip> <port>
curl -sk --connect-timeout 5 https://<destination>:<port>/

# NTP reachability
chronyc sources -v | grep "^*"        # confirm preferred source
ntpdate -q ntp.example.com
```


```text title="Expected output"
VLAN ID 2048 Status: active
  Name: PROD-APP-TIER
  Ports: Gi0/1, Gi0/2, Gi0/3, Gi0/48
  Type: enet

Name                           Num Portgroups Used Ports Configured Ports
vDS-Prod                       47  128              256

IP IN USE
Nmap scan report for 10.42.15.87
Host is up (0.0032s latency).

10.42.15.87 (prod-app-01.example.com) is up

;; ANSWER SECTION:
prod-app-01.example.com. 300 IN A 10.42.15.87

prod-app-01.example.com. 300 IN A 10.42.15.87

Connection to 10.42.15.87 port 443 [tcp/https] succeeded!
HTTP/1.1 200 OK
Server: nginx/1.24.0
Content-Length: 4521

     Remote refid      St t When Poll Reach   Delay   Offset   Jitter
^*    ntp.example.com  .POOL. 16 p    -   64    0    0.000    0.000    0.000
     ntpdate[12847]: adjust time server 10.20.5.10 offset 0.002345 sec
```

!!! warning "Common errors"
    **`VLAN <vlan_id> does not exist`** — Verify the VLAN ID is correct and exists on the target switch using `show vlan brief`.
    **`nslookup: can't resolve '<planned-hostname>.example.com': No address associated with hostname`** — Create the DNS A record in your DNS management system before proceeding with environment readiness.
    **`Connection refused`** — Confirm the firewall rule exists in your security policy and the destination service is listening on the specified port using `netstat -tlnp` on the target host.
| Network Check | Status |
|---|---|
| VLAN provisioned | ☐ |
| IP address reserved | ☐ |
| DNS A record created | ☐ |
| DNS PTR record created | ☐ |
| Firewall rules approved and active | ☐ |
| NTP server reachable | ☐ |
| Load balancer VIP configured (if needed) | ☐ |
| SSL certificate issued / ready | ☐ |

## 3. Security Readiness

```bash
# Confirm CyberArk PAM account created for server
# CyberArk: Accounts → Add Account → Managed System: <hostname>

# Check SSH hardening baseline
sshd -T | grep -E "PermitRootLogin|PasswordAuthentication|MaxAuthTries|Protocol"

# SELinux / AppArmor enforcing
getenforce                         # should return "Enforcing"
aa-status | grep "profiles in enforce"

# Check OS baseline applied
oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_cis_server_l1 \
  --results /tmp/oscap-results.xml \
  /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
```


```text title="Expected output"
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3
Protocol 2
Enforcing
   profiles in enforce mode.
       /etc/apparmor.d/usr.sbin.rsyslogd
       /etc/apparmor.d/usr.lib.snapd.snap-confine.classic
       /etc/apparmor.d/usr.sbin.cupsd
Benchmarks:
  xccdf_org.ssgproject.content_profile_cis_server_l1: 142/156 rules passed
Rule xccdf_org.ssgproject.content_rule_service_auditd_enabled: pass
Rule xccdf_org.ssgproject.content_rule_kernel_module_dccp_disabled: fail
Rule xccdf_org.ssgproject.content_rule_file_permissions_etc_shadow: pass
Results written to /tmp/oscap-results.xml
```

!!! warning "Common errors"
    **`command not found: oscap`** — Install openscap-scanner package with `sudo yum install openscap-scanner` or `sudo apt install libopenscap8`.
    **`No such file or directory: /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml`** — Install scap-security-guide package with `sudo yum install scap-security-guide` to populate SCAP content files.
    **`aa-status: command not found`** — Install apparmor-utils with `sudo apt install apparmor-utils` on Debian/Ubuntu systems, or use `getenforce` alone on SELinux-only systems.
| Security Check | Status |
|---|---|
| PAM / CyberArk account created | ☐ |
| SSH key-based auth only | ☐ |
| OS security baseline applied | ☐ |
| Host-based firewall configured | ☐ |
| Antivirus / EDR agent installed | ☐ |
| Vulnerability scan clean | ☐ |
| TLS certificate valid and trusted | ☐ |

## 4. Monitoring Readiness

```bash
# Install and verify Prometheus node_exporter
systemctl is-active node_exporter
curl -s http://localhost:9100/metrics | grep "node_uname_info"

# Confirm host visible in Prometheus/Grafana
curl -s "http://prometheus:9090/api/v1/query?query=up{instance='<host>:9100'}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['result'])"

# Windows — confirm monitoring agent
Get-Service "Prometheus Windows Exporter" | Select-Object Status
# or for Zabbix / SCOM
Get-Service "Zabbix Agent" | Select-Object Status
```


```text title="Expected output"
active
node_uname_info{domainname="corp.local",machine="x86_64",nodename="app-srv-prod-01",release="5.10.0-28-generic",sysname="Linux",version="#1 SMP Debian 5.10.209-2 (2024-01-31)"} 1.0
[{'metric': {'__name__': 'up', 'instance': 'app-srv-prod-01:9100', 'job': 'node'}, 'value': [1707312845.123, '1']}]
Status
------
Running
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to localhost port 9100: Connection refused`** — Verify node_exporter is installed and running with `systemctl start node_exporter && systemctl enable node_exporter`.
    **`'data' KeyError`** — Confirm the Prometheus instance is accessible and the target host has been scraped at least once by checking `http://prometheus:9090/targets` in the UI.
    **`Get-Service : Cannot find any service with service name 'Prometheus Windows Exporter'`** — Install the Windows exporter MSI or verify the exact service name with `Get-Service | findstr -i prometheus`.
| Monitoring Check | Status |
|---|---|
| Monitoring agent installed and running | ☐ |
| Host visible in monitoring platform | ☐ |
| Alerting rules configured | ☐ |
| Dashboard available | ☐ |
| Log forwarding configured (syslog/Splunk) | ☐ |
| On-call escalation configured | ☐ |

## 5. Backup Readiness

```bash
# Veeam — confirm backup job exists and targets new VM
Get-VBRJob | Where-Object {$_.GetObjectsInJob().Name -like "*HOSTNAME*"}

# Commvault — confirm client registered
qlist client -name HOSTNAME

# Run first backup and verify
Start-VBRJob -Job "Production VMs"
Get-VBRSession | Where-Object JobName -like "*Production VMs*" | Select-Object -Last 1
```


```text title="Expected output"
Name                           Type            TargetRepository
----                           ----            ----------------
HOSTNAME-Daily-Backup          Backup          RepoA-LUN02
HOSTNAME-Weekly-Full           Backup          RepoB-LUN03

Client Name                    OS              Status
-----------                    --              ------
HOSTNAME                       Windows 2019    Active

Backup job started successfully.
JobId                 : 00000000-1111-2222-3333-444444444444
JobName               : Production VMs
State                 : Working
Progress              : 45%
StartTime             : 2024-01-15 14:32:18
```

!!! warning "Common errors"
    **`Get-VBRJob : The term 'Get-VBRJob' is not recognized`** — Import the Veeam PowerShell snapin with `Add-PSSnapin VeeamPSSnapin` before running the command.
    **`qlist: command not found`** — Ensure the Commvault client is installed and the `qlogin` command has been executed to authenticate the session.
    **`Get-VBRSession : No matching jobs found for filter`** — Verify the job name matches exactly (case-sensitive) and wait 10-15 seconds after `Start-VBRJob` for the session to appear in the list.
| Backup Check | Status |
|---|---|
| Backup job includes new system | ☐ |
| Backup policy meets RPO requirement | ☐ |
| Retention period configured | ☐ |
| First backup completed successfully | ☐ |
| Restore test performed | ☐ |

## 6. Documentation and CMDB

```bash
# Items to complete before handover
# → CMDB entry created with: hostname, IP, owner, location, specs, environment
# → Run book / system overview doc drafted
# → Support contact assigned
# → Patch schedule assigned
```

| Documentation | Status |
|---|---|
| CMDB entry created | ☐ |
| System owner assigned | ☐ |
| Patch schedule set | ☐ |
| Runbook / system doc available | ☐ |
| DR/recovery procedure documented | ☐ |

## Readiness Sign-Off

| Domain | Status | Signed Off By |
|---|---|---|
| Capacity | ☐ Ready / ☐ Blocked | |
| Network | ☐ Ready / ☐ Blocked | |
| Security | ☐ Ready / ☐ Blocked | |
| Monitoring | ☐ Ready / ☐ Blocked | |
| Backup | ☐ Ready / ☐ Blocked | |
| Documentation | ☐ Ready / ☐ Blocked | |
| **Overall** | ☐ **Ready** / ☐ **Not Ready** | |
