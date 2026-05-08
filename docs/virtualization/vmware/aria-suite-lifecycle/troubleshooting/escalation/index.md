# Aria Suite Lifecycle — Escalation

VMware/Broadcom support for LCM is accessed via the [Broadcom Support Portal](https://support.broadcom.com). When opening a Support Request (SR), the product to select is "VMware Aria Suite Lifecycle" under the VMware Cloud Foundation portfolio. Log bundles for LCM SRs should be collected with `vracli support-bundle generate`, which packages LCM application logs, service logs, deployment history, and system diagnostics into a single archive under `/data/support-bundles/`.

**Information to collect before opening an SR:**
- LCM version: Settings > System Details > Version
- Affected product name and version
- LCM log bundle: `vracli support-bundle generate`
- Browser HAR file if issue is UI-related
- Description of last successful operation and first observed failure
- Screenshot of LCM dashboard Environment Health at time of issue

**Support tiers:**
| Severity | Description | Response SLA (Production) |
|---|---|---|
| S1 | Production down, no workaround | 30 minutes |
| S2 | Major feature unavailable | 4 hours |
| S3 | Partial degradation, workaround exists | Next business day |
| S4 | General question or enhancement request | Next business day |
