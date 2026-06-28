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
