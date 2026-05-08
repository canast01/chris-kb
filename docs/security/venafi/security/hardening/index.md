# Venafi — Hardening

All certificate lifecycle events are captured in the Venafi audit log and should be forwarded to a SIEM via the Log Server. Admin and service accounts should be reviewed quarterly.

| Control | Detail |
|---|---|
| Audit log | All lifecycle events logged; forward to SIEM via Log Server |
| Certificate pinning | Policy enforcement for pinned certificate use cases |
| Admin account review | Quarterly review of Venafi admin and service accounts |
