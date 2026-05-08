# CloudIQ — Diagnostics

> Part of the [CloudIQ](../../) reference.

---

Run the following on the **Secure Connect Gateway** host to diagnose connectivity and service health:

```bash
# Verify SCG can reach Dell's SRS telemetry endpoint
curl -k https://esrs3.emc.com

# Check dsagw service status (the core SCG telemetry forwarding service)
systemctl status dsagw

# Restart dsagw if it is stopped or failed
systemctl restart dsagw

# View dsagw logs live for telemetry send errors
journalctl -u dsagw -f

# Test CloudIQ API authentication (replace with your client_id and client_secret)
curl -s -X POST "https://cloudiq.dell.com/auth/v1/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=<client_id>&client_secret=<client_secret>"

# Confirm DNS resolution for CloudIQ and SRS endpoints from the SCG host
nslookup cloudiq.dell.com
nslookup esrs3.emc.com
```

For systems connected via a **proxy**, verify proxy settings in the SCG web UI under **Settings > Proxy** and confirm the proxy allows HTTPS to `cloudiq.dell.com` and `esrs3.emc.com` on port 443.

## Log Locations

| Log | Location | Use |
|---|---|---|
| SCG telemetry forwarding logs | `/var/log/dsagw/` on the SCG host | Diagnose why a system is not reporting; look for connection refused or TLS errors |
| SCG application logs | `/var/log/esrs/` | Broader SCG service errors |
| CloudIQ audit log | CloudIQ portal: **Admin > Audit Log** | Track user actions, API calls, and configuration changes |
| Browser console | Browser DevTools (F12) > Console | Diagnose UI rendering errors or failed API calls in the CloudIQ dashboard |

## Before Calling Support

Collect the following before opening a Dell support case for a CloudIQ issue:

- **SCG version**: visible in SCG web UI under **Settings > About**
- **CloudIQ system list screenshot**: screenshot of the Systems page showing which systems are and are not reporting
- **API error response**: full JSON error body and HTTP status code from any failing API call, with timestamp
- **SCG connectivity test output**: output of `curl -k https://esrs3.emc.com` and `systemctl status dsagw`
- **dsagw logs**: relevant lines from `/var/log/dsagw/` around the time the issue started
- **Browser console errors**: for dashboard UI issues, export the browser console log with timestamps
