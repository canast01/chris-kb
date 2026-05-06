# Venafi Vendor Support

Venafi support cases are raised via the Venafi Support Portal at support.venafi.com. When opening an SR, include the TPP version, CA type and version, approximate managed certificate count, and the full error message with timestamp. Collect TPP logs from the VdcLogFile directory and policy server application logs before engaging support to reduce round-trips.

Venafi offers Premier Support tiers with defined SLA response times. Critical production outages (Severity 1) should be raised by phone in addition to the portal ticket to ensure fastest response.

| Item | Detail |
|---|---|
| Support portal | https://support.venafi.com |
| Log location (TPP) | `%ProgramData%\Venafi\log\VdcLogFile*.log` |
| Policy server logs | Windows Event Log → Application (source: Venafi) |
| Required info for SR | TPP version, CA type, certificate count, error + timestamp |
| Premier Support tiers | Standard, Premier, Premier Plus — check entitlement in portal |
| Sev 1 escalation | Raise via portal and call support hotline simultaneously |
