# APEX Storage as a Service — Hardening

> Part of the [APEX Storage as a Service](../../) reference.

---

- Keep SCG appliances at the current recommended version — outdated SCG versions may break telemetry and SupportAssist connectivity
- Deploy two SCG appliances for redundancy; register each APEX system to both
- Rotate APEX API credentials every 90 days; store in a secrets vault
- Enable MFA for all Dell account users with APEX Console access
- Review APEX Console audit log monthly for unexpected access or configuration changes
