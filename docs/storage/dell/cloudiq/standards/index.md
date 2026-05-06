# CloudIQ Standards

## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| CloudIQ system display name | Use the same hostname/identifier as in Unisphere/SYMCLI | `lon01-powermax-001` |
| CloudIQ tag (site) | `site:<site-code>` | `site:lon01` |
| CloudIQ tag (environment) | `env:<environment>` | `env:prod` |
| CloudIQ tag (platform) | `platform:<type>` | `platform:powermax` |
| API client name | `svc-cloudiq-<purpose>` | `svc-cloudiq-monitoring` |
| Notification group name | `<team>-<severity>-alerts` | `storage-ops-critical-alerts` |
| Webhook integration name | `<target-system>-<channel>` | `servicenow-incident-creation` |

Apply at minimum three tags per system: site, environment, and platform. This enables efficient filtering in the CloudIQ dashboard across large estates.

## Build and Deployment Baseline

- Deploy the Secure Connect Gateway virtual appliance per the Dell SCG Installation Guide before onboarding systems to CloudIQ
- Register each Dell storage system to SCG from the system's management interface (Unisphere, SYMCLI) before the system will appear in CloudIQ
- Confirm SCG → CloudIQ telemetry is flowing: all systems should appear in the CloudIQ dashboard within 30 minutes of SCG registration
- Create a dedicated API client (`svc-cloudiq-monitoring`) in CloudIQ → Settings → API Access for all automation; do not use personal user accounts in scripts
- Apply tags to all systems at onboarding; do not leave systems untagged
- Configure notification rules for CRITICAL and ERROR severity alerts at minimum — direct to a monitoring email list or webhook
- Set up a webhook to the ITSM system (ServiceNow or equivalent) for CRITICAL alerts to trigger automatic incident creation
- Rotate API client secrets annually; maintain the secret in a secrets vault (not in plaintext scripts)

## Configuration Checklist

- [ ] SCG appliance deployed and reachable from management network
- [ ] All Dell storage systems registered to SCG and visible in CloudIQ dashboard
- [ ] All systems tagged with site, environment, and platform tags
- [ ] Health scores visible for all systems (no system showing "No Data" after 30 minutes)
- [ ] Notification rules configured for CRITICAL alerts → email distribution list
- [ ] Notification rules configured for CRITICAL alerts → ITSM webhook (ServiceNow or equivalent)
- [ ] API client created (`svc-cloudiq-monitoring`) with `client_id` and `client_secret` stored in secrets vault
- [ ] API token generation tested: `curl` to auth endpoint returns a valid `access_token`
- [ ] Capacity forecasting enabled and baseline trends visible (requires at least 7 days of telemetry)
- [ ] SSO configured if corporate identity provider is in use
- [ ] SCG redundancy: two SCG appliances deployed; each device registered to both
