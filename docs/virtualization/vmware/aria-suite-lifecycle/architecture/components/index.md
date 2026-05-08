# Aria Suite Lifecycle — Components

## Overview

LCM manages version upgrades, patches, and end-of-support scheduling for all Aria Suite products. Understanding the product version matrix and upgrade sequencing prevents compatibility issues and missed EOS dates.

## Product Version Matrix

Current Aria Suite product versions and their minimum LCM version requirements:

| Product | Current Version | Min LCM Version | Release Date | EOS Date |
|---|---|---|---|---|
| Aria Suite Lifecycle | 8.16 | — | Nov 2024 | Nov 2026 |
| Aria Operations | 8.17 | 8.14 | Nov 2024 | Nov 2026 |
| Aria Operations for Logs | 8.16 | 8.14 | Nov 2024 | Nov 2026 |
| Aria Automation | 8.17 | 8.14 | Nov 2024 | Nov 2026 |
| Workspace ONE Access | 23.09 | 8.12 | Sep 2023 | Sep 2025 |
| NSX | 4.1.2 | 8.12 | Aug 2023 | Aug 2025 |

```bash
# Check installed product versions via LCM API
curl -sk -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/environments/<env-id>/products \
  | python3 -m json.tool

# List all environments
curl -sk -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/environments \
  | python3 -m json.tool
```

## Upgrade Sequencing

Always upgrade in the following order to avoid dependency conflicts:

1. Aria Suite Lifecycle (LCM itself — upgrade via SDDC Manager or self-upgrade)
2. Workspace ONE Access (Identity provider — must be upgraded before Aria products)
3. Aria Operations for Logs
4. Aria Operations
5. Aria Automation

```bash
# Trigger an upgrade via LCM API
curl -sk -X POST -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/environments/<env-id>/products/<product-id>/upgrade \
  -H "Content-Type: application/json" \
  -d '{
    "targetVersion": "8.17.0",
    "snapshotBeforeUpgrade": true
  }'

# Monitor upgrade request status
curl -sk -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/requests/<request-id> \
  | python3 -m json.tool
```

## Support Lifecycle Policy

VMware by Broadcom follows a defined support lifecycle for Aria Suite products:

| Phase | Description | Duration |
|---|---|---|
| General Support | Full support, patches, and updates | 12–18 months from GA |
| Technical Guidance | Security patches only, no new features | 6–12 months post General Support |
| End of Support (EOS) | No further patches or support | Final date |

```bash
# Check LCM for products approaching EOS
curl -sk -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/products/lifecycle \
  | python3 -m json.tool | grep -A3 "endOfSupport"
```

## Available Bundles and Content Library

```bash
# List available upgrade bundles
curl -sk -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/bundles \
  | python3 -m json.tool

# Trigger bundle download from depot
curl -sk -X POST -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/bundles/download \
  -H "Content-Type: application/json" \
  -d '{"bundleId": "<bundle-id>"}'

# Check download progress
curl -sk -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/bundles/<bundle-id>/status \
  | python3 -m json.tool

# List locally available bundles
ls -lh /data/vmware/vrlcm/bundles/
```

## Compatibility Checking

Before upgrading, verify compatibility between products and with underlying vSphere:

```bash
# Run pre-upgrade compatibility check
curl -sk -X POST -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/environments/<env-id>/precheck \
  -H "Content-Type: application/json" \
  -d '{"targetVersions": {"vrops": "8.17.0", "vra": "8.17.0"}}'

# Check vSphere compatibility for Aria Operations
curl -sk -u admin:<password> \
  "https://<lcm-fqdn>/lcm/api/v1/compatibility?product=vrops&version=8.17.0" \
  | python3 -m json.tool
```

Compatibility rules summary:

| Aria Product | Min vSphere | Min vCenter | Notes |
|---|---|---|---|
| Aria Operations 8.17 | 7.0 U3 | 7.0 U3 | vSphere 8.x recommended |
| Aria Automation 8.17 | 7.0 U3 | 7.0 U3 | NSX 3.2+ required for NSX integration |
| Aria Ops for Logs 8.16 | 7.0 | 7.0 | — |
