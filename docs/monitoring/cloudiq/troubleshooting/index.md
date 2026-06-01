# CloudIQ Troubleshooting

<div class="kb-summary">
CloudIQ Troubleshooting reference covering Diagnostic Approach, Common Issues, SCG Log Locations, Dell Support Escalation.
</div>

## Diagnostic Approach

Before escalating to Dell support, work through the standard diagnostic steps:
1. Check SCG connectivity and status first — the majority of CloudIQ issues originate at the SCG.
2. Confirm the array management interface is reachable from the SCG.
3. Check CloudIQ system last-seen timestamp to determine how stale the data is.
4. Review SCG logs for error messages.

## Common Issues

### System Not Appearing in CloudIQ

**Symptoms**: Array is not visible in the CloudIQ Assets view, or shows "Unknown" status.

**Likely causes and steps**:
```text
1. System not onboarded:
   - SCG admin UI > Systems — verify the system is listed and has a valid IP/credential
   - If missing: add the system (see Lifecycle > Array Onboarding)

2. SCG outbound connectivity blocked:
   - From SCG, test: curl -v https://cloudiq.dell.com
   - Firewall must allow SCG egress to cloudiq.dell.com on TCP 443
   - Check proxy configuration if required: SCG admin UI > Network Settings

3. Incorrect array credentials:
   - SCG admin UI > Systems > [System] > Edit > Test Connection
   - Ensure the service account has not expired or been locked
```
┌────────────────────────────────────── CloudIQ — Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Array Not Reporting              │  │              Alert/Score Issues             │   │
│   │            Check TCP 443 outbound            │  │             Verify telemetry age            │   │
│   │            Verify DNS resolution             │  │               Check issue list              │   │
│   │            Re-test from array CLI            │  │            Check threshold config           │   │
│   │              Re-register array               │  │           Clear false-pos dismiss           │   │
│   │               Check gateway VM               │  │            Open Dell support case           │   │
│   │            Review array firmware             │  │             Attach telemetry log            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  All troubleshooting via array CLI/UI and cloudiq.dell.com · Dell support via support portal          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Not reporting = Array shows Disconnected or telemetry age > 15 minutes in CloudIQ                    │
│  TCP 443 test = Telnet or curl from array management IP to cloudiq.dell.com:443                       │
│  DNS resolution = Array must resolve cloudiq.dell.com; check DNS server config on array               │
│  Re-register = Removing array from CloudIQ and re-adding; resets telemetry stream                     │
│  Gateway VM = Check VM is powered on, has internet access, and service is running                     │
│  Telemetry age = Minutes since last data received; shown per array in CloudIQ UI                      │
│  False positive = Alert that does not represent a real issue; dismiss with reason                     │
│  Threshold = Alert trigger value; adjust if getting too many low-value notifications                  │
│  Array firmware = Older firmware may have telemetry bugs; update to supported release                 │
│  Dell support case = Open at support.dell.com with array serial and CloudIQ org name                  │
│  Telemetry log = Array-side log of CloudIQ push attempts; provided to Dell GSS                        │
│  Proxy check = If gateway VM uses proxy, verify proxy allows cloudiq.dell.com:443                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

### Health Score Calculation Delay

**Symptoms**: System health score shows as "Unknown" or does not update after a firmware upgrade.

```text
- This is expected behaviour after a firmware upgrade
- Allow 2–4 hours for health score recalculation post-upgrade
- If still not updated after 4 hours, open a Dell support case with system ID and upgrade timestamp
```

### Alert Notifications Not Delivered

**Symptoms**: A CRITICAL alert fired in CloudIQ but no notification was received in PagerDuty, email, or Teams.

```text
1. CloudIQ portal > Settings > Notifications > [Rule] — verify the rule is enabled
2. Confirm the webhook URL or email address is current
3. Test the notification rule manually: Actions > Test Notification
4. Check CloudIQ audit log for notification delivery errors
5. For PagerDuty: verify the integration key has not been rotated on the PagerDuty side
```

### SCG Certificate Errors

**Symptoms**: SCG reports TLS/certificate errors when connecting to Dell cloud or array management interfaces.

```text
1. For SCG-to-cloud TLS errors:
   - Verify SCG system clock is synchronised (NTP): System Settings > Date/Time
   - Check that the SCG trusts Dell's root CA (should be pre-configured in OVA)

2. For SCG-to-array certificate errors:
   - Download and trust the array's self-signed certificate in the SCG trust store:
     SCG admin UI > Security > Trusted Certificates > Add
```

## SCG Log Locations

```bash
# From the SCG CLI (SSH as admin user):
# Service logs
journalctl -u srs-agent --since "1 hour ago"
journalctl -u cloudiq-connector --since "1 hour ago"

# Application logs
/var/log/dell/cloudiq/
/var/log/dell/scg/
```

## Dell Support Escalation

- Open a support case at: support.dell.com
- Include: SCG version, affected system model and serial number, and the last-seen timestamp from CloudIQ
- Request log bundle from SCG: SCG admin UI > Support > Generate Log Bundle
