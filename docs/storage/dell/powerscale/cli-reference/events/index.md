# Events & Alerts

> Part of the Dell PowerScale (Isilon) CLI Reference.

## View Events

```bash
# All active events
isi event events list

# Critical events only
isi event events list --severity critical

# Warning and above
isi event events list --severity warning

# Events since a specific date
isi event events list --start-time 2026-05-01

# Verbose output with full description
isi event events list -v

# Filter by event type
isi event events list | grep -i "disk\|node\|network\|quota"
```

## Resolve and Acknowledge Events

```bash
# Resolve an event (marks it as handled)
isi event events resolve <event_id>

# Resolve all events of a specific type
isi event events list | grep <event_type> | awk '{print $1}' | xargs -I{} isi event events resolve {}
```

## Alert Channels

```bash
# List configured alert channels (email, SNMP, etc.)
isi event channels list

# View details of a specific channel
isi event channels view <channel_name>

# Create an email alert channel
isi event channels create email-ops \
    --type smtp \
    --address ops-team@corp.local \
    --send-test yes

# Modify a channel
isi event channels modify <channel_name> --address new@corp.local
```

## Alert Rules

```bash
# List alert rules (which events trigger which channels)
isi event alerts list

# View a specific alert rule
isi event alerts view <alert_name>

# Create an alert rule — send critical events to email channel
isi event alerts create critical-to-email \
    --event-category all \
    --severity critical \
    --channels email-ops
```

## SNMP Configuration

```bash
# View SNMP settings
isi snmp settings view

# Modify SNMP community and target
isi snmp settings modify \
    --snmp-v3-access-enable yes \
    --system-contact "infra-team@corp.local" \
    --system-location "DC1-Row3-Rack5"
```

## Event Log in syslog

```bash
# Events are also forwarded to syslog if configured
isi audit settings global view | grep syslog

# Modify syslog forwarding
isi audit settings global modify --syslog-forwarding-enabled yes
```
