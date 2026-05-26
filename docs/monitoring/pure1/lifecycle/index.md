# Pure1 Lifecycle
## Platform Update Model

Pure1 is a SaaS platform managed entirely by Pure Storage. There is no customer-managed version to upgrade. Feature releases, analytics model updates, and UI changes are deployed by Pure Storage and communicated via Pure1 release notes.

Customer lifecycle responsibilities:
1. Onboarding new arrays when deployed
2. Monitoring Purity version compatibility with Pure1 features
3. Managing Pure1 API token lifecycle
4. Monitoring connection status for all arrays
5. Reviewing Pure1 release notes for API changes

## Array Onboarding

New FlashArray and FlashBlade systems connect to Pure1 automatically once Purity is initialised and outbound HTTPS connectivity is available. No manual registration is required — arrays authenticate to Pure1 using their factory-installed certificates and serial numbers.

### Onboarding Verification

```bash
# From Purity CLI — verify Pure1 connectivity
purearray list --connection
# Look for "connected" status for pure1.purestorage.com

# If connectivity shows "disconnected":
purearray set --proxy https://<proxy>:<port>   # if behind a proxy
# Or check firewall rules for outbound HTTPS to pure1.purestorage.com
```
┌──────────────────────────────────── Pure1 — Lifecycle Management ─────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Onboarding                  │  │                   Ongoing                   │   │
│   │              Activate Pure1 org              │  │              Monitor phonehome              │   │
│   │              Add arrays via SN               │  │             Keep Purity current             │   │
│   │               Enable phonehome               │  │             Renew Evergreen sub             │   │
│   │               Configure alerts               │  │              Rotate API tokens              │   │
│   │               Set up webhooks                │  │             Annual access review            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Pure1 is SaaS — no on-prem component to maintain · Purity upgrades handled by ops team               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Pure1 org = Customer organisation in Pure1; all arrays grouped under one org                         │
│  Activate = Creating Pure1 org via Pure portal using Evergreen contract                               │
│  Add arrays via SN = Arrays register to Pure1 using serial number + phonehome                         │
│  Enable phonehome = purearray setattr --phonehome enabled on FlashArray                               │
│  Purity current = Keep array OS on supported release; Pure1 tracks versions                           │
│  Evergreen subscription = Annual renewal; includes Pure1, support, and hardware refresh               │
│  Rotate API tokens = Pure1 API tokens have no expiry; rotate annually per policy                      │
│  Access review = Yearly audit of Pure1 org users; remove departed staff                               │
│  Monitor phonehome = Daily check that all arrays show Connected in Pure1                              │
│  SaaS = Pure1 platform updated by Pure Storage; no customer upgrade action                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Array Decommission

```text
1. Open a Pure Storage support case to initiate array decommission from Pure1
   (arrays cannot be removed from Pure1 by the customer directly)
2. Ensure all alert notification rules referencing the array are updated
3. Update automation scripts to exclude the decommissioned array serial number
```

## Purity Version Compatibility

Some Pure1 features require minimum Purity OS versions. Track Purity versions across the fleet and plan upgrades to maintain feature access.

| Feature | Minimum Purity Version |
|---|---|
| Pure1 Meta workload analytics | FlashArray Purity 5.2+ |
| Pure1 Meta capacity forecasting | FlashArray Purity 5.3+ |
| Pure1 REST API v2 | FlashArray Purity 6.0+ |
| Pure1 anomaly detection | FlashArray Purity 6.1+ |

Review the [Pure Storage Compatibility Matrix](https://support.purestorage.com) for the current version requirements.

## Pure1 REST API Lifecycle

The Pure1 REST API is versioned. The `v1.latest` alias tracks the current stable version. Older API versions are deprecated on a published schedule.

```text
API base URLs:
- v1: https://api.pure1.purestorage.com/api/1.latest/
- v2: https://api.pure1.purestorage.com/api/2.x/  (tag management, subscriptions)
```

Monitor Pure1 release notes for API deprecation notices. When a deprecation is announced:

```text
1. Identify all scripts and integrations using deprecated endpoints
2. Update to replacement endpoints per Pure1 migration guide
3. Test in non-prod before rolling out to production scripts
4. Complete migration before the published deprecation date
```

## API Token Lifecycle

Pure1 API tokens are long-lived keys associated with service accounts. Rotate annually.

```text
Rotation procedure:
1. Pure1 portal > Account > API Registration > [Service Account] > Rotate Key
2. Download the new private key (only shown once)
3. Update the key in the team secrets manager
4. Redeploy/restart all automation scripts using the old key
5. Verify API calls succeed with the new key
6. Log the rotation date and next due date in the credential register
```

## Metrics Retention Management

Pure1 retains 90 days of rolling performance and capacity metrics in the API. For longer-term capacity planning data:

- Run the `pure1_capacity_report.py` script weekly and archive results to a team shared drive or S3 bucket
- Monthly capacity trend reports should be retained for 2 years for capacity planning and chargeback purposes
