# CloudIQ — Escalation

> Part of the [CloudIQ](../../) reference.

---

## Support Portal

Dell CloudIQ support cases are handled through the standard Dell support portal at [https://www.dell.com/support](https://www.dell.com/support). CloudIQ is a SaaS service and does not have its own separate support queue — issues are logged against the affected storage system's case, with CloudIQ identified as the impacted component.

If a CloudIQ issue affects multiple systems or is a platform-level SaaS problem (e.g., dashboard unavailable, API endpoints returning 5xx), open a case against any managed system and specify that the issue is with the CloudIQ SaaS platform itself.

## Opening a Case

When opening a support case for a CloudIQ-related issue:

- **Product**: select the affected storage system (e.g., PowerScale, Unity XT) as the primary product.
- **Affected component**: specify **CloudIQ** as the impacted component in the case description.
- **Summary**: include what is not working — system not reporting, API failing, incorrect health score, alert not routing.

Required information for the case:

| Field | How to Obtain |
|---|---|
| System serial number | Chassis label or array CLI (e.g., `isi version` for PowerScale) |
| SCG version | SCG web UI: Settings > About |
| Error message | Exact error text from the CloudIQ portal or API response |
| CloudIQ system list screenshot | Screenshot of CloudIQ Systems page showing reporting status |
| SCG connectivity test output | `curl -k https://esrs3.emc.com` result from the SCG host |

## Information to Collect

Collect the following diagnostic data before or immediately after opening the case:

```bash
# On the Secure Connect Gateway host:

# Check dsagw service status
systemctl status dsagw

# Review recent dsagw telemetry forwarding logs
journalctl -u dsagw --since "2 hours ago"

# Test connectivity to Dell SRS endpoint
curl -k https://esrs3.emc.com

# Test CloudIQ API authentication
curl -s -X POST "https://cloudiq.dell.com/auth/v1/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=<client_id>&client_secret=<client_secret>"
```

Additional items:

- SCG application logs from `/var/log/dsagw/` (compress and attach to the case).
- CloudIQ API error response body with HTTP status code and timestamp.
- Browser console errors (F12 > Console) if the issue is UI-related — export as a log file.
- CloudIQ audit log export (Admin > Audit Log) for the relevant time window if the issue involves access or configuration.

## SLA Tiers

CloudIQ support SLA follows the ProSupport Plus contract of the managed storage system. There is no separate CloudIQ SLA.

| Priority | Condition | Response Time | Coverage |
|---|---|---|---|
| P1 | CloudIQ outage causing inability to monitor production systems | 2 hours | 24x7x365 |
| P2 | Degraded CloudIQ functionality (partial data, delayed alerts) | 4 hours | 24x7x365 |
| P3 | Non-critical CloudIQ issue (UI display, API edge case) | Next business day | Business hours |
| P4 | General question or enhancement request | Next business day | Business hours |

## Escalation

For SaaS platform-level issues (CloudIQ dashboard unavailable, systemic reporting failures across all systems):

1. Open a P1 support case and specify that the issue is a **CloudIQ SaaS platform issue** affecting all managed systems.
2. Contact your **Dell account team** and request escalation to the **CloudIQ product team**. The CloudIQ engineering team can investigate SaaS-side infrastructure issues that front-line support cannot resolve.
3. Check [https://status.dell.com](https://status.dell.com) or the Dell support portal for any announced CloudIQ service incidents before escalating — platform maintenance or incidents may already be tracked.
4. For prolonged SaaS outages affecting contractual monitoring obligations, request engagement through **Dell Global Priority Services** via your account team.
