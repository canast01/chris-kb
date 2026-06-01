# NetApp Keystone Vendor Support

<div class="kb-summary">
NetApp Keystone Vendor Support reference covering Keystone Success Manager, Support Portal, Opening a Case, Information to Collect, SLA Tiers and 1 more sections.
</div>

## Keystone Success Manager

Every Keystone subscription includes a dedicated Keystone Success Manager (KSM). The KSM is the primary NetApp contact for:

- Service issues and escalations beyond standard support case handling
- Capacity planning discussions and subscription amendment requests
- Monthly consumption review and billing query resolution
- Renewal planning and term negotiation
- Onboarding of new service tiers or StorageGRID object capacity

Contact the KSM directly for issues that require commercial or service-level attention, in addition to or instead of opening a technical support case.

## Support Portal

- **Technical support portal:** [https://mysupport.netapp.com](https://mysupport.netapp.com) — for infrastructure issues, Collector problems, and ONTAP/StorageGRID issues on Keystone-managed hardware
- **Keystone-specific issues:** raise via the KSM or open a Keystone ticket in the BlueXP portal
- Ensure your NetApp SSO account is linked to your company's support entitlement before opening cases

## Opening a Case

Required information when opening a Keystone support case:

- Keystone subscription ID (from BlueXP Keystone dashboard)
- Affected service tier (Extreme, Premium, Standard, Object)
- Keystone Collector version
- Clear description of the symptom and business impact
- Whether the issue is a billing discrepancy, a performance SLA breach, a Collector issue, or a platform infrastructure issue

## Information to Collect

Before contacting support, gather:

- Screenshot of the BlueXP Keystone dashboard showing the affected subscription and tier
- Keystone Collector VM status (`systemctl status keystone-collector`)
- Keystone Collector logs (`journalctl -u keystone-collector -n 200`)
- Consumption report for the affected billing period (download from BlueXP digital wallet)
- ONTAP EMS log extract if the issue is related to storage platform performance

## SLA Tiers

| Priority | Response Time | Scope |
|---|---|---|
| P1 | 4 hours | Service unavailable, data inaccessible, SLA guarantee breached |
| P2 | 8 hours | Degraded performance or partial service impact |
| P3 | Next business day | Non-critical issue, billing query, configuration change |

Keystone SLA guarantees 99.9999% (six nines) availability for the infrastructure service. SLA breaches are remediated by NetApp SRE, including hardware replacement if required. Infrastructure response and remediation are included in the subscription — no additional charges for hardware repair or replacement.

## Escalation

- Escalate persistent infrastructure or SLA issues to the KSM for routing to the Keystone Engineering team
- For billing or commercial disputes, escalate via the KSM to the NetApp account team
- Executive escalation for unresolved critical issues is available via the NetApp account executive
- Request TAM (Technical Account Manager) engagement for complex hybrid deployments combining Keystone STaaS, Cloud Volumes ONTAP, and BlueXP data services
