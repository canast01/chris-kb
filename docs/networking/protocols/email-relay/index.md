---
tags:
  - networking
search:
  boost: 1
---
# Integration — Email Relay (SMTP)

<div class="kb-summary">
Email relay integration using SMTP — how infrastructure components route mail through a relay host for alerting, reporting, and system notifications.

*Applies to: Postfix · Exim · any SMTP-capable relay*
</div>

```d2
direction: down

common_relay_hosts: "Common Relay Hosts" {shape: rectangle}
postfix_quick_reference: "Postfix Quick Reference" {shape: rectangle}
key_configuration: "Key Configuration" {shape: rectangle}

common_relay_hosts -> postfix_quick_reference: uses
postfix_quick_reference -> key_configuration: uses
```

## Overview

An email relay receives SMTP messages from internal hosts and forwards them to an external mail server or MX record. Common uses include:

- Storage array and monitoring alert emails
- Scheduled report delivery
- System cron job output

## Common Relay Hosts

| Role | Typical Host | Port |
|---|---|---|
| Internal relay | Postfix / Exim on a Linux host | 25 / 587 |
| Cloud relay | AWS SES, SendGrid, Google SMTP | 465 / 587 |
| Appliance relay | vCenter, ONTAP, Unity mail settings | 25 |

## Postfix Quick Reference

```bash
# Reload after config change
postfix reload

# Test relay from CLI
echo "Test" | mail -s "Test relay" admin@example.com

# Check mail queue
mailq

# View delivery log
tail -f /var/log/maillog
```


```text title="Expected output"
postfix/postfix-script: refreshing the Postfix mail system
(no output — command completes silently)
                    Queue ID  Size Arrival Time   Sender
                    --------  ---- -------------- ------
                    4A2B1C3D  1024 Mon Dec 18 14:22 root@mail.example.com
                    5F7E8D9A  2048 Mon Dec 18 14:23 admin@mail.example.com
                    6G8H9I0B  512  Mon Dec 18 14:24 noreply@mail.example.com
-- 3 Kbytes in 3 Request.
Dec 18 14:25:33 mail-relay postfix/pickup[12345]: 4A2B1C3D: uid=0 from=<root>
Dec 18 14:25:34 mail-relay postfix/cleanup[12346]: 4A2B1C3D: message-id=<20231218142534.4A2B1C3D@mail.example.com>
Dec 18 14:25:35 mail-relay postfix/qmgr[9876]: 4A2B1C3D: from=<root@mail.example.com>, size=1024, nrcpt=1 (queue active)
Dec 18 14:25:36 mail-relay postfix/smtp[12347]: 4A2B1C3D: to=<admin@example.com>, relay=smtp.relay.com[203.0.113.45]:25, delay=2.1, delays=0.02/0.01/1.05/1.02, dsn=2.0.0, status=sent (250 2.0.0 OK)
```

!!! warning "Common errors"
    **`postfix: fatal: file /etc/postfix/main.cf not found`** — Verify postfix is installed with `postman -v` and reinstall if necessary, or check that `/etc/postfix/main.cf` exists.
    **`mail: command not found`** — Install the mailutils package with `apt-get install mailutils` (Debian/Ubuntu) or `yum install mailx` (RHEL/CentOS).
    **`postfix/master: fatal: bind port 25: Permission denied`** — Run postfix commands with `sudo` or ensure the postfix user has appropriate permissions to bind to port 25.
## Key Configuration

```ini
# /etc/postfix/main.cf
relayhost = [smtp.example.com]:587
smtp_use_tls = yes
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
```

## See Also

- [Networking Protocols](../index.md)
