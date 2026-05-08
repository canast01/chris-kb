# FOD — Hardening

> Part of the [Flex on Demand](../../) reference.

---

- Keep SCG appliance software current — outdated SCG versions may break telemetry delivery and cause metering gaps
- Deploy two SCG appliances for redundancy; register each array to both
- Use dedicated API service accounts per integration for CloudIQ and APEX API access
- Rotate API credentials every 90 days; store in a secrets vault
- Review CloudIQ audit log monthly for unexpected API access patterns
