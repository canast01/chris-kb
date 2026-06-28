---
tags:
  - pure
---
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

```d2
direction: right

plan: "Plan" {shape: oval}
prepare: "Prepare" {shape: rectangle}
execute: "Execute" {shape: rectangle}
verify: "Verify" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prepare
prepare -> execute
execute -> verify
verify -> validate
```
