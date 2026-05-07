# AutoSupport

> Part of the [NetApp ONTAP CLI Reference](../).

AutoSupport is NetApp's telemetry and support system. It sends system health, configuration, and event data to NetApp support and can trigger proactive support cases.
## View AutoSupport Status

```bash
# AutoSupport configuration and status
autosupport show

# Per-node view
autosupport show -node <node>

# Delivery status (whether messages are reaching NetApp)
autosupport show -fields last-subject-sent, last-successful-destination
```

## Send AutoSupport Messages

```bash
# Test AutoSupport delivery (sends a test message)
autosupport invoke -node <node> -type test

# Send full AutoSupport bundle (for TAC cases)
autosupport invoke -node <node> -type all -message "Manual upload for case SR-XXXXX"

# Send specific subsystem data
autosupport invoke -node <node> -type test -subsystem storage
```

## History

```bash
# AutoSupport message history
autosupport history show

# Per-node history
autosupport history show -node <node>

# History with delivery status
autosupport history show -fields seq-num, status, triggered-time, destination
```

## Configuration

```bash
# Enable AutoSupport
autosupport modify -node <node> -state enable

# Disable AutoSupport (not recommended except for offline systems)
autosupport modify -node <node> -state disable

# Set SMTP relay
autosupport modify -node <node> -mail-hosts <smtp_server>

# Set proxy (if AutoSupport uses HTTPS via proxy)
autosupport modify -node <node> -proxy-url http://proxy.corp.local:8080

# Set notification address (where AutoSupport emails are sent)
autosupport modify -node <node> -noteto ops@corp.local
```

## AutoSupport Delivery Methods

| Method | Configuration |
|---|---|
| HTTPS | Recommended — direct to NetApp (port 443) |
| SMTP | Email relay to NetApp addresses |
| HTTP | Not recommended — insecure |

```bash
# Set protocol
autosupport modify -node <node> -transport https

# Verify HTTPS connectivity to NetApp
autosupport check show
```

## Active IQ and AutoSupport

AutoSupport data feeds into NetApp Active IQ (cloud-based analytics):

- Review at [activeiq.netapp.com](https://activeiq.netapp.com)
- Provides capacity forecasts, risk warnings, firmware recommendations
- AutoSupport must be enabled and reaching NetApp for Active IQ to populate
