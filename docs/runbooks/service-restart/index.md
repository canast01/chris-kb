# Service Restart Runbook
## Pre-Checks

```bash
# Current service status
systemctl status <service>

# Check for active connections or jobs before restarting
ss -tnp | grep <port>

# Review recent logs for errors
journalctl -u <service> -n 50 --no-pager

# Windows
Get-Service <service>
```

Confirm service owner approval and check for active users or in-flight jobs before proceeding.

## Graceful Stop and Start

```bash
# Preferred: stop then start (allows clean shutdown)
systemctl stop <service>
systemctl start <service>

# Or restart in one command
systemctl restart <service>

# Reload config without full restart (if supported)
systemctl reload <service>
```

**Windows:**
```powershell
Stop-Service <service> -Force
Start-Service <service>
# or
Restart-Service <service>
```

## Post-Restart Validation

```bash
# Confirm service is running
systemctl status <service>

# Confirm listening on expected port
ss -tnlp | grep <port>

# Check recent logs for errors
journalctl -u <service> -n 50 --no-pager --since "5 minutes ago"
```

## Test Application Response

```bash
# HTTP service check
curl -vk https://<app_host>/health

# TCP port check
nc -zv <host> <port>
```

## Windows Service Validation

```powershell
Get-Service <service>
# Should show: Running

# Check event log for service errors
Get-EventLog -LogName System -Source 'Service Control Manager' -Newest 10
```

## Checklist

- [ ] Service owner notified
- [ ] Active jobs/connections confirmed clear
- [ ] Service stopped cleanly
- [ ] Service restarted
- [ ] Service shows Running
- [ ] Port listening confirmed
- [ ] Application response confirmed
- [ ] Monitoring alert cleared

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Service won't stop | Active connections | Kill active sessions; force stop |
| Service fails to start | Logs show error | Check `journalctl -u <svc> -n 100` |
| Port not listening | Config file | Verify config is valid; check file permissions |
| Restart loop | Critical dependency missing | Check service dependencies |
