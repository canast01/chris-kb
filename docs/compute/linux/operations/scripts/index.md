# Linux — Scripts

Automation scripts and reusable code.

Scripts stored in the team's Git repository. All are idempotent and safe to run on production systems. Output logged to `/var/log/ops/` and forwarded to the central logging platform.

## Script Deployment Flow

```mermaid
flowchart LR
    gitRepo["Git Repository\nscripts/linux/"]
    ansible["Ansible Playbook\ndeploy-scripts.yml"]
    copy["Copy to servers\n/usr/local/bin/"]
    cron["Cron Schedule\ncrontab · systemd timer"]
    output["Output\n/var/log/ops/ · logger"]
    siem["SIEM / Log Platform\ncentralised logging"]

    gitRepo --> ansible --> copy --> cron --> output --> siem
```
┌──────────────────────────────────── Linux — Scripts & Automation ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                      Scripting Standards                                      │   │
│   │         Bash: shebang #!/bin/bash; set -euo pipefail; trap ERR for safe error handling        │   │
│   │          Python: use venv / pipenv; type hints; logging module; argparse for CLI args         │   │
│   │        Idempotency: scripts must be safely re-runnable without double-applying changes        │   │
│   │        Storage: version-controlled in Git; tested in staging before production rollout        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Well-structured scripts reduce human error and enable reliable automation at scale                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Bash Patterns                 │  │               Python Patterns               │   │
│   │          set -euo pipefail: strict           │  │          subprocess.run: exec cmds          │   │
│   │            trap cleanup EXIT ERR             │  │           paramiko: SSH automation          │   │
│   │         getopts / getopt: arg parse          │  │           fabric: remote execution          │   │
│   │          logger: syslog from script          │  │             click: CLI framework            │   │
│   │          lockfile: prevent parallel          │  │          jinja2: config templating          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 servers · Git repo server · cron/systemd timers · NIC · Power & Cooling                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  set -e      = Exit immediately if any command returns non-zero exit code                             │
│  set -u      = Treat unset variables as errors; prevents typo variable bugs                           │
│  set -o pipefail= Propagate pipeline failures; catches errors in piped commands                       │
│  trap        = Register signal/event handler; useful for cleanup on EXIT or ERR                       │
│  idempotency = Property of an operation that produces same result on repeated runs                    │
│  getopts     = Bash built-in for short option parsing (-v, -f); POSIX compliant                       │
│  logger      = Shell command that writes messages to syslog / systemd journal                         │
│  paramiko    = Python SSH library; programmatic remote command execution                              │
│  fabric      = Python SSH automation; high-level remote task execution over SSH                       │
│  click       = Python CLI framework; decorators for commands, options, arguments                      │
│  jinja2      = Python template engine; used by Ansible for config file rendering                      │
│  shebang     = First line of script (#!/bin/bash); tells kernel which interpreter to use              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## log-archival.sh

Compresses rotated logs older than 30 days to NFS archive:

```bash
#!/bin/bash
ARCHIVE_PATH="/mnt/nfs-archive/logs/$(hostname)"
LOG_PATH="/var/log"
mkdir -p "$ARCHIVE_PATH"

find "$LOG_PATH" -name "*.log-*" -mtime +30 -type f | while read f; do
    gzip -9 "$f" && mv "${f}.gz" "$ARCHIVE_PATH/" && \
    logger "Archived $f to $ARCHIVE_PATH"
done
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
