---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# APEX Storage as a Service — Diagnostics


<div class="kb-summary">
Part of the [APEX Storage as a Service](../index.md) reference.
</div>
```text
┌──────────────────────────────────── Dell Apex STaaS — Diagnostics ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Apex STaaS diagnostics: log collection, health checks, and performance analysis        │   │
│   │          Tools: management CLI, REST API, vendor support bundle, and system event log         │   │
│   │          Performance: check I/O latency, throughput, queue depth, and cache hit rate          │   │
│   │       Collect support bundle before contacting vendor support to reduce time-to-resolve       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify issue → collect logs → run diagnostics → analyse → resolve                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Owner            │   │
│   │           Hardware          │  │       NVMe/SAS arrays       │  │             Dell            │   │
│   │          Management         │  │         Apex Console        │  │           Customer          │   │
│   │          Monitoring         │  │         CloudIQ/SCG         │  │            Shared           │   │
│   │           Billing           │  │       Committed+burst       │  │         Dell billing        │   │
│   │           Network           │  │        iSCSI VLAN/FC        │  │           Customer          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Function     │      Protocol     │       Auth       │      Notes       │   │
│   │      Arrays      │  Block/File/NFS  │    iSCSI/FC/NFS   │  CHAP/Kerberos   │     On-prem      │   │
│   │   Apex Console   │  Provision/bill  │     HTTPS REST    │     SAML SSO     │   SaaS portal    │   │
│   │       SCG        │ Telemetry relay  │       HTTPS       │   Certificate    │     Local VM     │   │
│   │     CloudIQ      │ AIOps analytics  │       HTTPS       │      OAuth2      │       SaaS       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Dell array hardware on-premises · customer iSCSI VLAN / FC fabric · Apex Console SaaS    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Apex STaaS         = on-prem Dell storage consumed as a cloud service with subscription billing    │
│    Apex Console       = cloud portal; provision volumes, view usage, and raise support requests       │
│    Committed base     = minimum contracted capacity tier; billed monthly regardless of actual use     │
│    Burst capacity     = pre-installed unlocked storage above committed; billed when consumed          │
│    SCG                = Secure Connect Gateway; relays array telemetry to CloudIQ for analysis        │
│    CloudIQ            = Dell AIOps SaaS; health scores, capacity forecasts, firmware advisories       │
│    NVMe tier          = all-flash performance tier; sub-millisecond latency for database workloads    │
│    Capacity tier      = SAS/NL-SAS lower cost tier; suited to bulk storage and backup targets         │
│    iSCSI CHAP         = Challenge Handshake Auth Protocol; authenticates iSCSI initiators to array    │
│    FC port sec.       = FC fabric binding and port security; restricts which HBAs can log in          │
│    vVols              = Virtual Volumes; per-VM storage objects exposed via VASA provider to vCenter  │
│    OOB mgmt           = out-of-band management network for direct array controller access             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

```bash
# Authenticate to Dell APEX API and retrieve a bearer token
curl -s -X POST "https://console.cloudapex.dell.com/api/v1/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"client_id":"<client_id>","client_secret":"<client_secret>"}' \
  | jq -r '.access_token'

# List all subscriptions for the account
curl -s -H "Authorization: Bearer <token>" \
  "https://console.cloudapex.dell.com/api/v1/subscriptions" | jq .

# Get capacity metrics for a specific subscription
curl -s -H "Authorization: Bearer <token>" \
  "https://console.cloudapex.dell.com/api/v1/subscriptions/<subscription_id>/capacity" | jq .

# Get active alerts for all APEX resources
curl -s -H "Authorization: Bearer <token>" \
  "https://console.cloudapex.dell.com/api/v1/alerts?status=active" | jq .

# List service requests
curl -s -H "Authorization: Bearer <token>" \
  "https://console.cloudapex.dell.com/api/v1/service-requests" | jq .
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## SCG Diagnostics

If APEX systems are not reporting:

```bash
# On the SCG appliance
dsagw status
dsagw connectivity-check
dsagw list-devices
dsagw log show --last 100
```

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
