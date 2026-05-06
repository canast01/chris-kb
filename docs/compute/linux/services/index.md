# Linux Services

Managing systemd services on RHEL and Ubuntu.

## Service Status and Control

```bash
# Check service status
systemctl status <service>

# Start / stop / restart
systemctl start <service>
systemctl stop <service>
systemctl restart <service>

# Reload configuration without full restart (if supported)
systemctl reload <service>

# Enable at boot / disable at boot
systemctl enable <service>
systemctl disable <service>

# Enable and start in one command
systemctl enable --now <service>
```

## Listing Services

```bash
# All active services
systemctl list-units --type=service --state=active

# Failed services
systemctl --failed

# All services (active + inactive)
systemctl list-units --type=service --all

# Services that are enabled but not running
systemctl list-units --type=service --state=inactive | grep enabled
```

## Service Logs

```bash
# Follow logs in real time
journalctl -u <service> -f

# Last 100 lines
journalctl -u <service> -n 100

# Since last boot
journalctl -u <service> -b

# Errors only
journalctl -u <service> -p err

# From a specific time
journalctl -u <service> --since "2026-05-01 10:00:00"
```

## Service Dependencies

```bash
# What does a service depend on?
systemctl list-dependencies <service>

# What depends on this service?
systemctl list-dependencies --reverse <service>

# Show service unit file
systemctl cat <service>

# Show all properties
systemctl show <service>
```

## Creating a Custom Service

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/myapp --config /etc/myapp/config.yaml
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=myapp

[Install]
WantedBy=multi-user.target
```

```bash
# Load and start the new unit
systemctl daemon-reload
systemctl enable --now myapp
```

## Common Infrastructure Services

| Service | Unit Name | Description |
|---|---|---|
| SSH | `sshd` | Remote access |
| NTP (chrony) | `chronyd` | Time synchronisation |
| DNS cache | `systemd-resolved` | Local DNS resolution |
| Firewall | `firewalld` / `ufw` | Host-based firewall |
| Audit daemon | `auditd` | Syscall and file auditing |
| Log daemon | `rsyslog` | Remote syslog forwarding |
| Cron | `crond` / `cron` | Scheduled jobs |
| LVM monitoring | `lvm2-monitor` | Thin pool and VG monitoring |
| Multipath | `multipathd` | SAN multipath I/O |
| Network manager | `NetworkManager` | Interface and connection management |

## Restart Policies

```bash
# View current restart policy
systemctl show <service> | grep -E "Restart=|RestartSec="

# Override restart policy without editing the unit file
systemctl edit <service>
# Add under [Service]:
# Restart=always
# RestartSec=10
systemctl daemon-reload
systemctl restart <service>
```

## Service Resource Limits

```bash
# Check current limits on a running service
systemctl show <service> | grep -E "LimitNOFILE|LimitNPROC|MemoryMax|CPUQuota"

# Set memory limit via drop-in
mkdir -p /etc/systemd/system/<service>.service.d/
cat > /etc/systemd/system/<service>.service.d/limits.conf <<EOF
[Service]
MemoryMax=2G
LimitNOFILE=65536
EOF
systemctl daemon-reload
systemctl restart <service>
```

## Masking and Unwanted Services

```bash
# Mask a service (prevents any start, even manual)
systemctl mask <service>

# Unmask
systemctl unmask <service>

# Services to disable on production servers (no UI needed)
systemctl disable --now bluetooth cups avahi-daemon
```

## Troubleshooting a Failed Service

```bash
# 1. Check status for the error message
systemctl status <service> -l

# 2. Check journal for the unit
journalctl -u <service> -n 50 --no-pager

# 3. Check dependencies
systemctl list-dependencies <service> | grep failed

# 4. Validate unit file syntax
systemd-analyze verify /etc/systemd/system/<service>.service

# 5. Test ExecStart command manually as the service user
sudo -u <service-user> /path/to/binary --args
```
