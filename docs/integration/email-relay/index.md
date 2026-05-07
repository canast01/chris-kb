# Email Relay

## Overview

Email relay services deliver system alerts, notifications, and automated messages.

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Verify SMTP service running |  |  |
| Check mail queue status |  |  |
| Confirm relay permissions |  |  |
| Review failed message logs |  |  |

## Health Commands

```bash
systemctl status postfix
mailq
tail -n 50 /var/log/mail.log
```

## Troubleshooting Workflow

1. Confirm SMTP connectivity
2. Check authentication settings
3. Review firewall rules
4. Validate DNS configuration
