---
tags:
  - security
description: "Security Incident Handling reference covering Severity Classification, Phase 1 — Identify and Triage, Phase 2 — Contain, Phase 3 — Investigate, Phase 4 —..."
---
# Security Incident Handling

<div class="kb-summary">
Security Incident Handling reference covering Severity Classification, Phase 1 — Identify and Triage, Phase 2 — Contain, Phase 3 — Investigate, Phase 4 — Eradicate and Recover and 3 more sections.
</div>

<div class="kb-grid">
  <a class="kb-card" href="operations/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">Operations</div>
    <div class="kb-card-desc">Incident lifecycle, containment, eradication, recovery procedures</div>
  </a>
</div>

## Severity Classification

| Severity | Definition | Example | Response Time |
|---|---|---|---|
| P1 — Critical | Active breach, ransomware, data exfiltration in progress | Ransomware spreading, admin credential stolen | Immediate (call on-call now) |
| P2 — High | Confirmed compromise with limited scope, or high-confidence threat | Single workstation infected, phishing link clicked | 1 hour |
| P3 — Medium | Suspicious activity, potential threat, no confirmed impact | Anomalous login from foreign IP, port scan | Business day |
| P4 — Low | Informational security event, policy violation | Password policy violation, USB insertion | Within 1 week |

## Phase 1 — Identify and Triage

```bash
# Check for active suspicious processes (Linux)
ps aux | grep -E "nc|ncat|nmap|metasploit|mimikatz|powersploit"

# Recent logins from unusual IPs
last -n 50
grep "Failed password\|Accepted password" /var/log/auth.log | tail -50

# Windows — check for active remote sessions
query session /server:<hostname>
Get-EventLog -LogName Security -InstanceId 4624,4625 -Newest 50
```


```text title="Expected output"
root@prod-web-01:~# ps aux | grep -E "nc|ncat|nmap|metasploit|mimikatz|powersploit"
root      2847  0.1  0.3  45628  12544 ?        Ss   14:22   0:00 sshd: root@pts/0
root      3156  0.0  0.1   6432   4128 pts/0    S+   14:23   0:00 grep -E nc|ncat|nmap|metasploit|mimikatz|powersploit

root@prod-web-01:~# last -n 50
root     pts/0        203.0.113.45     Wed Dec 13 14:22   still logged in
admin    pts/1        198.51.100.87    Wed Dec 13 12:15 - 13:45  (1:30)
root     pts/0        192.0.2.156      Tue Dec 12 23:47 - 01:22  (1:35)
svc_app  pts/2        10.0.45.78       Tue Dec 12 18:30 - 18:45  (0:15)
root     tty1         -                Tue Dec 12 16:12 - down   (2:18)

root@prod-web-01:~# grep "Failed password\|Accepted password" /var/log/auth.log | tail -50
Dec 13 14:22:15 prod-web-01 sshd[3142]: Accepted password for root from 203.0.113.45 port 54821 ssh2
Dec 13 14:15:03 prod-web-01 sshd[3089]: Failed password for invalid user testuser from 198.51.100.201 port 48392 ssh2
Dec 13 14:14:58 prod-web-01 sshd[3087]: Failed password for invalid user admin from 198.51.100.201 port 48388 ssh2
Dec 13 13:45:22 prod-web-01 sshd[2956]: Accepted password for admin from 198.51.100.87 port 52104 ssh2
Dec 13 12:30:11 prod-web-01 sshd[2801]: Failed password for root from 192.0.2.99 port 41256 ssh2

C:\Windows\System32> query session /server:dc-prod-01
 SESSIONNAME       USERNAME                 ID  STATE   TYPE        DEVICE
 services                                    0  Disc
 console                                     1  Conn
 rdp-tcp#0         DOMAIN\jsmith             2  Active  rdpwd
 rdp-tcp#1         DOMAIN\mchen              3  Active  rdpwd
 rdp-tcp#2         DOMAIN\svc_backup        4  Disc

C:\Windows\System32> Get-EventLog -LogName Security -InstanceId 4624,4625 -Newest 50
   Index Time          EntryType   Source                 InstanceID Message
   ----- ----          ---------   ------                 ---------- -------
    8847 Dec 13 14:25  SuccessAu... Security                    4624
```
## Phase 2 — Contain

**Network isolation (do not power off — preserve forensic state):**

```powershell
# Windows — disable NIC (keeps system running but disconnected)
Get-NetAdapter | Disable-NetAdapter -Confirm:$false

# Or block at firewall / network switch level
# Contact network team to port-isolate the switch port
```

```bash
# Linux — drop all traffic except management (use with caution)
iptables -I INPUT -s <mgmt-ip> -j ACCEPT
iptables -I OUTPUT -d <mgmt-ip> -j ACCEPT
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `iptables: No chain/target/match by that name` | Ensure iptables is installed and the kernel module is loaded with `modprobe ip_tables`. |
    | `iptables: Permission denied` | Run the commands with `sudo` or as root; iptables requires elevated privileges. |
    | `Bad argument '<mgmt-ip>'` | Replace `<mgmt-ip>` with an actual IP address (e.g., `192.168.1.100`) before executing the script. |
**CyberArk — rotate or suspend compromised accounts immediately:**
1. CyberArk PVWA → Accounts → locate account → Change password (immediate rotation)
2. For suspected account compromise: suspend account in AD and rotate all credentials

## Phase 3 — Investigate

**Windows event IDs to review:**

| Event ID | Meaning |
|---|---|
| 4624 | Successful logon |
| 4625 | Failed logon |
| 4648 | Logon with explicit credentials |
| 4720 | User account created |
| 4728 | Member added to security-enabled global group |
| 4740 | User account locked out |
| 7045 | New service installed |

```powershell
# Pull security events from last 4 hours
Get-WinEvent -FilterHashtable @{LogName='Security'; StartTime=(Get-Date).AddHours(-4)} |
  Where-Object {$_.Id -in @(4624,4625,4648,4720,4728,7045)} |
  Select-Object TimeCreated, Id, Message | Format-List
```

**Linux — audit log:**
```bash
# Recent sudo usage
grep sudo /var/log/auth.log | tail -50

# File access audit (if auditd running)
ausearch -k <audit-key> -ts recent

# Network connections at time of incident
ss -tnp
netstat -anp | grep ESTABLISHED
```


```text title="Expected output"
Oct 15 10:23:45 prod-web-01 sudo: alice : TTY=pts/0 ; PWD=/home/alice ; USER=root ; COMMAND=/bin/bash
Oct 15 10:24:12 prod-web-01 sudo: bob : TTY=pts/1 ; PWD=/var/www ; USER=root ; COMMAND=/usr/bin/systemctl restart nginx
Oct 15 10:25:33 prod-web-01 sudo: alice : TTY=pts/0 ; PWD=/home/alice ; USER=root ; COMMAND=/usr/bin/cat /etc/shadow
Oct 15 10:26:01 prod-web-01 sudo: charlie : TTY=pts/2 ; PWD=/opt/app ; USER=root ; COMMAND=/usr/bin/rm -rf /tmp/cache
Oct 15 10:27:44 prod-web-01 sudo: alice : TTY=pts/0 ; PWD=/home/alice ; USER=root ; COMMAND=/usr/bin/curl http://external-host.com/script.sh
...
No matches found
tcp    LISTEN      0      128      0.0.0.0:22                 0.0.0.0:*                   users:(("sshd",pid=412,fd=3))
tcp    LISTEN      0      128      0.0.0.0:80                 0.0.0.0:*                   users:(("nginx",pid=2847,fd=6))
tcp    ESTAB       0      0      10.42.1.15:54321            203.0.113.42:443             users:(("curl",pid=8934,fd=3))
tcp    ESTAB       0      0      10.42.1.15:22               10.20.0.88:51234             users:(("sshd",pid=5621,fd=3))
tcp    ESTAB       0      0      10.42.1.15:3306             10.42.1.20:45678             users:(("mysqld",pid=1203,fd=14))
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ausearch: command not found` | Install auditd with `apt-get install auditd` or `yum install audit` and ensure the audit daemon is running. |
    | `grep: /var/log/auth.log: No such file or directory` | Check the correct log path for your system; on some distributions use `/var/log/secure` instead of `/var/log/auth.log`. |
    | `netstat: command not found` | Use `ss` instead (already shown in the block) or install net-tools with `apt-get install net-tools`. |
## Phase 4 — Eradicate and Recover

- Remove malicious files, scheduled tasks, persistence mechanisms
- Re-image if full compromise suspected (do not trust a compromised OS)
- Restore from known-good backup (verify backup pre-dates compromise)
- Apply patches that were exploited
- Reset all passwords for affected accounts and service accounts

## Phase 5 — Post-Incident

```markdown
Incident Report (template):
- Date/time detected:
- Date/time contained:
- Systems affected:
- Data at risk / confirmed exfiltrated:
- Root cause:
- Attack vector:
- Timeline:
- Actions taken:
- Lessons learned:
- Remediation items (with owners and due dates):
```

## Escalation Contacts

| Role | Contact | When to Escalate |
|---|---|---|
| Security Lead | _fill in_ | Any P1/P2 |
| CISO | _fill in_ | P1 — confirmed breach |
| Legal / Compliance | _fill in_ | Any data exfiltration risk |
| PR / Comms | _fill in_ | External disclosure required |
| Vendor TAC | _fill in_ | Platform-specific technical response |

## Key Notification Requirements

- **GDPR**: 72 hours from awareness of personal data breach to supervisory authority
- **PCI-DSS**: Notify card brands within 24 hours of suspected cardholder data compromise
- **Internal SLA**: Management notified within 1 hour of P1 identification
