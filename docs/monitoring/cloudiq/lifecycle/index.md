# CloudIQ Lifecycle

<div class="kb-summary">
CloudIQ Lifecycle reference covering Platform Update Model, Secure Connect Gateway (SCG) Lifecycle, Array Decommission, API Token Lifecycle, Release Notes Review.
</div>

## Platform Update Model

CloudIQ is a SaaS platform managed entirely by Dell. There is no customer-managed version to upgrade. Feature releases, AI model updates, and API changes are deployed by Dell and communicated via the CloudIQ release notes published in the CloudIQ portal under **Settings > Release Notes**.

Customer lifecycle responsibilities are limited to:
1. Keeping the Secure Connect Gateway (SCG) current
2. Onboarding newly deployed Dell systems
3. Managing CloudIQ API token lifecycle
4. Monitoring CloudIQ release notes for breaking API changes

## Secure Connect Gateway (SCG) Lifecycle

The SCG has its own version lifecycle and must be kept current for compatibility with new Dell platforms and CloudIQ features.

### SCG Version Check

```text
1. Log into SCG admin UI: https://<SCG-IP>:9443
2. Navigate to: System Settings > About
3. Note the current SCG version
4. Compare against the latest available version in the Dell Support Portal
```
```
┌─────────────────────────────────── CloudIQ — Lifecycle Management ────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Onboarding                  │  │             Ongoing Maintenance             │   │
│   │             Create Dell account              │  │            Monitor telemetry age            │   │
│   │               Register arrays                │  │             Re-register if stale            │   │
│   │               Configure alerts               │  │            Update array firmware            │   │
│   │              Add users + roles               │  │            Rotate service account           │   │
│   │            Test webhook delivery             │  │             Annual access review            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  CloudIQ is SaaS — no on-prem component to patch · array firmware controls telemetry client           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Telemetry age = Time since last successful push from array; stale > 15 min triggers alert            │
│  Re-registration = Removing and re-adding array to CloudIQ; resets telemetry stream                   │
│  Service account rotation = Changing Dell account password used for CloudIQ API access                │
│  Access review = Auditing CloudIQ user list; removing departed staff and role changes                 │
│  Array firmware = On-array software; update process depends on array model (PSTCLI, ESRS)             │
│  ESRS = EMC Secure Remote Services; gateway used by some older Dell arrays for telemetry              │
│  CloudIQ SaaS = Hosted by Dell; no customer upgrade responsibility for the platform itself            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## API Token Lifecycle

CloudIQ REST API tokens use OAuth2 client credentials. Tokens should be rotated annually.

```text
Rotation procedure:
1. CloudIQ portal > Settings > API Clients > [Client] > Rotate Secret
2. Update the new client_secret in the team secrets manager
3. Redeploy or restart any automation scripts that use the old secret
4. Verify API scripts return HTTP 200 after rotation
```

## Release Notes Review

Review CloudIQ release notes when notified by Dell (typically monthly). Check for:
- New platform support (confirm newly deployed systems are supported)
- API endpoint changes or deprecations
- Feature changes that affect existing alert rules or notification configurations

**Location**: CloudIQ portal > Settings > Release Notes
