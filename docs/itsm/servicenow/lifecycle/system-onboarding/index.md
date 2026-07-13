---
tags:
  - servicenow
description: "Brings a new physical server, VM, or cloud instance into full production management — covering identity, networking, security, monitoring, backup, and..."
---
# System Onboarding Procedure

<div class="kb-summary">
Brings a new physical server, VM, or cloud instance into full production management — covering identity, networking, security, monitoring, backup, and documentation.

*Applies to: ServiceNow*
</div>

## Onboarding Stages

```d2
direction: right

F: "F" {shape: rectangle}
G: "Handover to\nApp / Ops Team" {shape: rectangle}
A: "Provisioned" {shape: rectangle}
B: "B" {shape: rectangle}
C: "C" {shape: rectangle}
D: "D" {shape: rectangle}
E: "E" {shape: rectangle}

F -> G
```

## 2. OS Hardening and Security Baseline

```bash
# Apply CIS baseline via Ansible
ansible-playbook -i inventory/ security/cis-baseline.yml --limit <hostname>

# SELinux enforcing
sed -i 's/^SELINUX=.*/SELINUX=enforcing/' /etc/selinux/config
setenforce 1

# Disable unnecessary services
systemctl disable --now bluetooth avahi-daemon cups rpcbind postfix

# SSH hardening
cat > /etc/ssh/sshd_config.d/hardening.conf <<EOF
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowGroups sshusers admins
EOF
systemctl reload sshd

# Host firewall
firewall-cmd --set-default-zone=drop
firewall-cmd --permanent --add-service=ssh
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.0.0.0/8" service name="ssh" accept'
firewall-cmd --reload
```


```text title="Expected output"
PLAY [Apply CIS baseline] ******************************************************

TASK [Gathering Facts] *********************************************************
ok: [prod-web-01.internal]

TASK [Apply CIS baseline controls] *********************************************
changed: [prod-web-01.internal]

PLAY RECAP *********************************************************************
prod-web-01.internal       : ok=2    changed=1    unreachable=0    failed=0

SELinux policy in enforcing mode already.
bluetooth.service: Unit not found.
Removed /etc/systemd/system/multi-user.target.wants/avahi-daemon.service.
Removed /etc/systemd/system/multi-user.target.wants/cups.service.
Removed /etc/systemd/system/multi-user.target.wants/rpcbind.service.
Removed /etc/systemd/system/multi-user.target.wants/postfix.service.
success
success
success
success
success
success
```

!!! warning "Common errors"
    **`ansible-playbook: command not found`** — Install Ansible with `pip install ansible` or `yum install ansible`.
    **`sed: can't read /etc/selinux/config: No such file or directory`** — Verify SELinux is installed with `yum install selinux-policy` before running sed.
    **`Error: INVALID_ZONE: drop`** — Use a valid firewalld zone name like `drop` is valid; check firewall-cmd --get-zones and ensure firewalld service is running with `systemctl start firewalld`.
### CyberArk PAM Registration

```yaml
CyberArk UI: Accounts → Safes → <Environment>-Safe → Add Account
  Account type: Linux / Windows
  Platform:     LinuxSSH / WinServerLocal
  Address:      <hostname>.example.com
  Username:     ansible / svc-admin
```

## 3. Monitoring and Logging

```bash
# Install Prometheus node_exporter
useradd -r -s /sbin/nologin node_exporter
curl -sL https://github.com/prometheus/node_exporter/releases/download/v1.8.0/node_exporter-1.8.0.linux-amd64.tar.gz \
  | tar xz -C /tmp/
install -m 755 /tmp/node_exporter-*/node_exporter /usr/local/bin/

cat > /etc/systemd/system/node_exporter.service <<EOF
[Unit]
Description=Prometheus Node Exporter
After=network.target
[Service]
User=node_exporter
ExecStart=/usr/local/bin/node_exporter
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now node_exporter
curl -s http://localhost:9100/metrics | head -3

# Log forwarding to central syslog
echo "*.* @syslog.example.com:514" >> /etc/rsyslog.conf
systemctl restart rsyslog

# Verify host visible in monitoring
curl -s "http://prometheus:9090/api/v1/query?query=up{instance='<hostname>:9100'}" \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['data']['result']; print('UP' if r and r[0]['value'][1]=='1' else 'NOT VISIBLE')"
```


```text title="Expected output"
# node_exporter user created
# Download and extraction complete
# Binary installed to /usr/local/bin/node_exporter
# Service file created
# Systemd daemon reloaded
Created symlink /etc/systemd/system/multi-user.target.wants/node_exporter.service → /etc/systemd/system/node_exporter.service.
node_exporter.service enabled and started successfully.
# HELP node_cpu_seconds_total Seconds the cpus spent in each mode.
# TYPE node_cpu_seconds_total counter
node_cpu_seconds_total{cpu="0",mode="user"} 1247.89
# Syslog forwarding rule appended to rsyslog.conf
# Rsyslog service restarted
Redirecting to /bin/systemctl restart rsyslog.service
UP
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to localhost port 9100: Connection refused`** — Wait 2–3 seconds after `systemctl enable --now node_exporter` for the service to start, then retry the curl command.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Verify Prometheus is running and accessible at `http://prometheus:9090`, and replace `<hostname>` with the actual node hostname (e.g., `web-server-01`).
    **`useradd: user 'node_exporter' already exists`** — Remove the existing user with `userdel node_exporter` before re-running the installation, or skip the useradd step if upgrading.
## 4. Backup Configuration

```powershell
# Veeam — add to backup job
$job = Get-VBRJob -Name "Production Linux VMs"
$vm = Find-VBRViEntity -Name "<hostname>"
Add-VBRViJobObject -Job $job -Entities $vm

# Run first backup and verify
Start-VBRJob -Job $job
Get-VBRSession | Where-Object JobName -eq "Production Linux VMs" | Select-Object -Last 1
```

## 5. Ansible Inventory Registration

```bash
# Add to inventory
cat >> inventory/production/hosts.yml <<EOF
    <hostname>.example.com:
      ansible_host: <ip>
EOF

# Host-specific vars
mkdir -p inventory/production/host_vars/<hostname>.example.com/
cat > inventory/production/host_vars/<hostname>.example.com/main.yml <<EOF
environment: production
role: <app_role>
owner: <team>
EOF

# Verify connectivity
ansible <hostname>.example.com -i inventory/production/ -m ansible.builtin.ping
```


```text title="Expected output"
web-app-prod-01.example.com:
      ansible_host: 10.42.18.156
(no output — command completes silently)
(no output — command completes silently)
web-app-prod-01.example.com | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```

!!! warning "Common errors"
    **`[WARNING]: Unable to parse <hostname>.example.com as an inventory source`** — Replace `<hostname>` and `<ip>` placeholders with actual values before running the commands.
    **`fatal: [web-app-prod-01.example.com]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}`** — Ensure the Ansible control node has SSH key-based authentication configured for the target host and the key is added to ssh-agent.
    **`[ERROR]: inventory/production/hosts.yml is not a valid YAML file`** — Verify YAML indentation is consistent (use spaces, not tabs) and that the hostname entry aligns with existing inventory structure.
## 6. CMDB Entry

| Field | Value |
|---|---|
| Hostname | |
| FQDN | |
| IP Address | |
| Environment | Production / Staging / Dev |
| OS / Version | |
| CPU / Memory / Disk | |
| Hypervisor / Physical host | |
| Owner / Team | |
| Application | |
| Backup job | |
| Patch schedule | |
| DR tier | |
| CyberArk safe | |
| Date onboarded | |

## Onboarding Checklist

| Step | Status |
|---|---|
| Hostname and IP configured | ☐ |
| DNS A + PTR records created | ☐ |
| NTP synchronized | ☐ |
| Domain joined | ☐ |
| OS security baseline applied | ☐ |
| SSH hardened (key-only) | ☐ |
| Host firewall configured | ☐ |
| CyberArk account created | ☐ |
| Monitoring agent installed | ☐ |
| Host visible in monitoring | ☐ |
| Log forwarding configured | ☐ |
| Backup job includes host | ☐ |
| First backup successful | ☐ |
| Ansible inventory updated | ☐ |
| CMDB entry created | ☐ |
| Handover to app team complete | ☐ |
