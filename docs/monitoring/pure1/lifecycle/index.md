# Pure1 — Lifecycle Management

```bash
# From Purity CLI — verify Pure1 connectivity
purearray list --connection
# Look for "connected" status for pure1.purestorage.com

# If connectivity shows "disconnected":
purearray set --proxy https://<proxy>:<port>   # if behind a proxy
# Or check firewall rules for outbound HTTPS to pure1.purestorage.com
```
```text
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
```text
API base URLs:
- v1: https://api.pure1.purestorage.com/api/1.latest/
- v2: https://api.pure1.purestorage.com/api/2.x/  (tag management, subscriptions)
```
```text
1. Identify all scripts and integrations using deprecated endpoints
2. Update to replacement endpoints per Pure1 migration guide
3. Test in non-prod before rolling out to production scripts
4. Complete migration before the published deprecation date
```
```text
Rotation procedure:
1. Pure1 portal > Account > API Registration > [Service Account] > Rotate Key
2. Download the new private key (only shown once)
3. Update the key in the team secrets manager
4. Redeploy/restart all automation scripts using the old key
5. Verify API calls succeed with the new key
6. Log the rotation date and next due date in the credential register
```
