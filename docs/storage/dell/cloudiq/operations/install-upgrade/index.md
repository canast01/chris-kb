# CloudIQ — Install & Upgrade

```
┌──────────────────────────────── Dell CloudIQ — Install and Onboarding ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    CloudIQ onboarding: deploy SCG, register to CloudIQ tenant, add arrays, configure alerts   │   │
│   │   Prerequisites: Dell support account with CloudIQ entitlement, array management credentials  │   │
│   │    SCG deployed as VMware OVA (or physical appliance) on management network per datacenter    │   │
│   │   After registration CloudIQ pulls telemetry within 15 minutes; health scores appear in 1 h   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Prerequisites → SCG deploy → portal setup → array registration → alert config → validation         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Prerequisites        │  │        SCG Deployment       │  │         Portal Setup        │   │
│   │      Dell support acct      │  │         Download OVA        │  │          Create org         │   │
│   │       CloudIQ license       │  │       Deploy on VMware      │  │         Invite users        │   │
│   │       Array mgmt creds      │  │      Configure network      │  │       Configure alerts      │   │
│   │      Outbound 443 open      │  │      Register to cloud      │  │          Add arrays         │   │
│   │        DNS resolution       │  │       Verify telemetry      │  │        Verify scores        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Upgrade SCG via CloudIQ portal: Settings > SCG > Update; zero-downtime rolling update              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Phase       │       Step       │        Tool       │      Owner       │ Success Criteria │   │
│   │     Planning     │   Size SCG VM    │     Spec sheet    │    Infra team    │    VM created    │   │
│   │    Deployment    │    Deploy OVA    │      vSphere      │   Storage eng.   │    SCG online    │   │
│   │   Registration   │    Add arrays    │       SCG UI      │   Storage eng.   │Telemetry flowing │   │
│   │    Validation    │   Check scores   │   CloudIQ portal  │   Storage lead   │   Score >= 80    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SCG OVA on vSphere management cluster · mgmt VLAN · NTP synced · 443 outbound            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    OVA            = Open Virtualization Archive; SCG VM image downloaded from Dell support portal     │
│    Entitlement    = CloudIQ license tied to support contract; required before portal access           │
│    Tenant / org   = CloudIQ logical container for all sites and arrays under one customer account     │
│    Array registration = Providing array management IP and credentials to SCG so it can collect data   │
│    Telemetry      = Performance counters, capacity stats, events collected from arrays via SCG        │
│    Health score   = Appears within ~1 hour of first telemetry; reflects array-wide health 0-100       │
│    Proxy config   = Configure on SCG if direct outbound 443 is blocked; HTTP/HTTPS proxy supported    │
│    Upgrade path   = CloudIQ initiates SCG update remotely; no manual download required                │
│    Management IP  = Dedicated array management interface IP; used by SCG not data-path IPs            │
│    Alert policy   = Set after arrays appear; defines thresholds for email or webhook notifications    │
│    NTP sync       = Required on SCG VM; clock skew over 5 minutes causes telemetry rejection          │
│    Rolling update = SCG update completes without interrupting telemetry collection pipeline           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [CloudIQ](../../index.md) reference.

---

## Platform Updates

CloudIQ is a SaaS platform hosted and operated by Dell — there is no on-premises upgrade process. All connected systems automatically use the current CloudIQ version. Dell releases major feature updates quarterly, with minor feature additions and bug fixes deployed continuously. Release notes are published at [https://www.dell.com/support](https://www.dell.com/support) under the CloudIQ product page.

Because CloudIQ is always current, lifecycle management focuses on the components you control: API credentials, the Secure Connect Gateway appliance, and your active ProSupport entitlements.

## API Token Management

CloudIQ REST API access uses OAuth2 client credentials (client ID and client secret). Client secrets have a configurable maximum validity and must be rotated before expiry to avoid automation outages.

| Token Type | Max Validity | Recommended Rotation Schedule |
|---|---|---|
| Client Secret (API credential) | Up to 2 years (configurable at creation) | Every 90 days |
| Access Token (bearer) | 1 hour | Fetched per session by automation; not stored |

Rotation process:

1. Create a new client credential pair in CloudIQ under **Settings > API Access**.
2. Update all automation scripts and vaults with the new client ID and secret.
3. Validate that scripts authenticate successfully using the new credential.
4. Delete the old client credential from CloudIQ.

Store client secrets in a secrets manager (CyberArk, HashiCorp Vault, or AWS Secrets Manager) — never in plaintext configuration files.

## Secure Connect Gateway Compatibility

The Secure Connect Gateway (SCG) is the on-premises component that forwards encrypted telemetry to CloudIQ. SCG must be kept on a current supported version; older SCG versions may lose compatibility with CloudIQ telemetry ingestion endpoints as the SaaS platform evolves.

| SCG Version | CloudIQ Compatibility | Notes |
|---|---|---|
| 5.x (current) | Full compatibility | Recommended for all new deployments |
| 4.x | Supported with limited features | Upgrade to 5.x before next feature release cycle |
| 3.x and below | End of support | Must upgrade; telemetry forwarding may fail |

Check SCG version and update status in the SCG web UI under **Settings > About**. Download SCG updates from the Dell support portal.

## Supported Systems

CloudIQ telemetry coverage spans the following Dell platforms. Systems added to CloudIQ must have an active ProSupport contract and must be connected via SCG.

| Dell Platform | CloudIQ Support Added | Notes |
|---|---|---|
| PowerMax | CloudIQ v1.0 (2019) | Full capacity, performance, and health visibility |
| PowerStore | CloudIQ v1.0 (2019) | Full support including CloudIQ-native alerts |
| PowerScale (Isilon) | CloudIQ v1.1 (2020) | Requires OneFS 8.1.2 or later |
| Unity XT | CloudIQ v1.1 (2020) | Requires Unity OE 5.0 or later |
| VPLEX | CloudIQ v1.2 (2021) | Health and alert visibility; limited performance metrics |
| Data Domain (PowerProtect DD) | CloudIQ v1.2 (2021) | Capacity and protection visibility |
| PowerEdge Servers | CloudIQ v1.3 (2022) | Server health and firmware tracking |

## Renewal and Subscription

CloudIQ entitlement is included with an active **ProSupport** or **ProSupport Plus** contract on each managed system. There is no separate CloudIQ subscription fee. When a system's ProSupport contract expires or lapses, that system will stop reporting telemetry to CloudIQ within 30 days of contract expiry.

To maintain CloudIQ coverage:

- Audit contract renewal dates annually in the Dell support portal under **My Products and Services**.
- Renew ProSupport contracts before expiry — lapsed coverage may result in gaps in capacity trend data.
- When decommissioning a system, remove it from CloudIQ (**Settings > Systems**) to avoid stale alerts.
