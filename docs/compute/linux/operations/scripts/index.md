---
tags:
  - linux
  - operations
description: "Automation scripts and reusable code. Scripts stored in the team's Git repository. All are idempotent and safe to run on production systems. Output logged..."
---
# Linux — Scripts

<div class="kb-summary">
Automation scripts and reusable code. Scripts stored in the team's Git repository. All are idempotent and safe to run on production systems. Output logged to `/var/log/ops/` and forwarded to the central logging platform.

*Applies to: RHEL / Ubuntu LTS*
</div>

Automation scripts and reusable code.

Scripts stored in the team's Git repository. All are idempotent and safe to run on production systems. Output logged to `/var/log/ops/` and forwarded to the central logging platform.

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Script Deployment Flow

```d2
direction: right

gitRepo: "Git Repository\nscripts/linux/" {shape: rectangle}
ansible: "Ansible Playbook\ndeploy-scripts.yml" {shape: rectangle}
copy: "Copy to servers\n/usr/local/bin/" {shape: rectangle}
cron: "Cron Schedule\ncrontab · systemd timer" {shape: rectangle}
output: "Output\n/var/log/ops/ · logger" {shape: rectangle}
siem: "SIEM / Log Platform\ncentralised logging" {shape: rectangle}

gitRepo -> ansible
ansible -> copy
copy -> cron
cron -> output
output -> siem
```

## patch-status-report.sh

Reports pending updates and last patch date:

```bash
#!/bin/bash
echo "=== Patch Status: $(hostname) at $(date) ==="

# RHEL/CentOS
if command -v dnf &>/dev/null; then
    echo "Available updates:"
    dnf check-update --quiet 2>/dev/null | grep -v "^$" | wc -l | xargs echo "  Packages:"
    rpm -qa --last | head -5 | xargs echo "  Last installed:"
fi

# Ubuntu/Debian
if command -v apt-get &>/dev/null; then
    apt-get -q --just-print upgrade 2>/dev/null | grep "^Inst" | wc -l | xargs echo "  Packages pending:"
fi
```


```text title="Expected output"
=== Patch Status: web-prod-01.internal at Thu Mar 14 09:42:17 UTC 2024 ===
Available updates:
  Packages: 23
  Last installed: kernel-5.10.0-28.el8.x86_64 Thu Mar 14 08:15:22 2024
bash-4.4.20-4.el8.x86_64 Thu Mar 14 08:15:18 2024
openssl-1.1.1k-12.el8.x86_64 Thu Mar 14 08:15:10 2024
glibc-2.28-225.el8.x86_64 Thu Mar 14 08:14:55 2024
systemd-239-82.el8.x86_64 Thu Mar 14 08:14:42 2024
```

!!! warning "Common errors"
    **`dnf check-update: command not found`** — Verify dnf is installed with `dnf --version` or check if the system uses yum instead on older RHEL versions.
    **`E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)`** — Run the script with sudo or ensure the user has read permissions on apt cache directories.
## user-audit.sh

Lists local users, sudo group members, and last login dates:

```bash
#!/bin/bash
echo "=== User Audit: $(hostname) at $(date) ==="
echo "--- Local users with shell access ---"
awk -F: '$7 !~ /nologin|false/ {print $1, $7}' /etc/passwd

echo "--- Sudo group members ---"
getent group sudo wheel 2>/dev/null

echo "--- Last 10 logins ---"
last -n 10 | head -10

echo "--- Currently logged in ---"
who
```


```text title="Expected output"
=== User Audit: prod-web-01 at Thu Jan 16 14:32:45 UTC 2025 ===
--- Local users with shell access ---
root /bin/bash
ubuntu /bin/bash
appuser /bin/bash
jenkins /bin/bash
--- Sudo group members ---
sudo:x:27:ubuntu,jenkins
wheel:x:10:appuser,sysadmin
--- Last 10 logins ---
ubuntu   pts/0        203.0.113.42     Thu Jan 16 14:15   still logged in
jenkins  pts/1        10.0.2.15        Thu Jan 16 13:48   still logged in
root     pts/2        10.0.2.1         Thu Jan 16 12:30 - 12:45  (00:15)
ubuntu   pts/3        203.0.113.42     Thu Jan 16 11:20 - 12:10  (00:50)
appuser  pts/4        10.0.1.88        Wed Jan 15 22:15 - 23:45  (01:30)
--- Currently logged in ---
ubuntu   pts/0        2025-01-16 14:15 (203.0.113.42)
jenkins  pts/1        2025-01-16 13:48 (10.0.2.15)
```

!!! warning "Common errors"
    **`awk: can't open file /etc/passwd`** — Verify the file exists and the script has read permissions on /etc/passwd.
    **`last: command not found`** — Install the `util-linux` package (apt install util-linux on Debian/Ubuntu or yum install util-linux on RHEL).
    **`getent: command not found`** — Ensure glibc-common or libc-bin is installed; this is a core system utility that should be present on all Linux distributions.
## disk-alert.sh

Sends alert if any filesystem exceeds threshold — designed for cron:

```bash
#!/bin/bash
THRESHOLD=80
ALERT_EMAIL="ops@corp.local"

df -H | awk -v t=$THRESHOLD 'NR>1 && int($5) > t {
    print "DISK ALERT on " ENVIRON["HOSTNAME"] ": " $6 " is " $5
}' | while read -r line; do
    echo "$line" | mail -s "[DISK ALERT] $(hostname)" "$ALERT_EMAIL"
    logger "$line"
done
```


```text title="Expected output"
DISK ALERT on prod-web-01: /var/log is 87%
DISK ALERT on prod-web-01: /home is 92%
```

!!! warning "Common errors"
    **`mail: command not found`** — Install mailutils with `apt-get install mailutils` or `yum install mailx` depending on your distribution.
    **`logger: command not found`** — Install bsd-mailx or util-linux with `apt-get install bsdmainutils` to enable syslog logging.
    **`ENVIRON["HOSTNAME"] is not set`** — Replace `ENVIRON["HOSTNAME"]` with `$(hostname)` or ensure the HOSTNAME environment variable is exported in your shell profile.
## Deployment

Scripts are deployed and scheduled via Ansible:

```yaml
# tasks/deploy-scripts.yml
- name: Copy operational scripts
  copy:
    src: "{{ item }}"
    dest: /usr/local/bin/
    mode: "0750"
    owner: root
    group: root
  loop:
    - system-health-check.sh
    - disk-alert.sh

- name: Schedule disk alert via cron
  cron:
    name: disk-alert
    minute: "0"
    hour: "*/4"
    job: /usr/local/bin/disk-alert.sh
    user: root
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Linux — Procedures](../procedures/)
- [Linux — CLI Reference](../cli-reference/)
- [Linux — Health Checks](../health-checks/)
