# Syslog and Centralized Logging

## Overview

Centralized logging collects system and application logs for troubleshooting, auditing, and security monitoring.

## Daily Checks

- Verify log ingestion
- Check disk utilization on log servers
- Confirm time synchronization
- Review critical error logs

## Health Commands

```bash
systemctl status rsyslog
df -h
tail -n 50 /var/log/messages
logger test-message
```

## Troubleshooting Workflow

1. Confirm log service running
2. Verify network connectivity to log collector
3. Check log file permissions
4. Validate time synchronization
5. Review error logs
