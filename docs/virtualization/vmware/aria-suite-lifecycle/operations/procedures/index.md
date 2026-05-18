# Aria Suite Lifecycle — Procedures

```
  LCM Common Procedures
┌─────────────────────────────────────────────────────────────────┐
│  Deploy Product           Replace Certificate                   │
│  ┌──────────────────┐     ┌──────────────────────────────────┐  │
│  │ Add Product →    │     │ Generate CSR (Locker or external)│  │
│  │  select version  │     │ Submit to CA → import signed     │  │
│  │  set size / IPs  │     │  cert into Locker (alias)        │  │
│  │  pre-checks pass │     │ Environments → Replace Cert      │  │
│  │  Deploy → monitor│     │  select alias → monitor          │  │
│  └──────────────────┘     └──────────────────────────────────┘  │
│                                                                 │
│  Rotate Password          Content Migration (Dev → Prod)        │
│  ┌──────────────────┐     ┌──────────────────────────────────┐  │
│  │ Locker → Passwords│    │ Content Lifecycle Mgr            │  │
│  │  Edit alias →    │     │  Extract from source env         │  │
│  │  update value    │     │  Deploy to target env            │  │
│  │ Re-validate prods│     │  map env-specific variables      │  │
│  │  using credential│     └──────────────────────────────────┘  │
│  └──────────────────┘                                           │
└─────────────────────────────────────────────────────────────────┘
```

## Deploy a New Aria Product

1. LCM → Lifecycle Operations → Environments → select or create environment
2. Click **Add Product**
3. Select product, version, and deployment size (Medium/Large)
4. Provide vCenter target: cluster, datastore, network, IP addresses, FQDNs, and admin password (stored in LCM Locker)
5. LCM runs pre-checks (DNS, NTP, vCenter connectivity) — all must pass before deployment begins
6. Click **Deploy** — monitor progress via **Lifecycle Operations → Requests**
7. Post-deployment: validate product UI is accessible and health shows green in LCM environment view

---

## Trigger a Product Upgrade

1. LCM → Lifecycle Operations → Environments → click the environment containing the product
2. Locate the product card and click **Upgrade**
3. LCM presents compatible target versions — select the target version
4. Review pre-checks: fix any failures before proceeding (disk space, DNS, NTP, snapshot presence)
5. Click **Start Upgrade** — LCM takes snapshots automatically, performs the upgrade, and validates post-state
6. Monitor: **Lifecycle Operations → Requests** — the upgrade request shows stages and percentage complete

If the upgrade fails mid-way, LCM provides a **Rollback** option that reverts all product VMs from the snapshots taken at step 5.

---

## Import and Replace a Product Certificate via Locker

Use this procedure when renewing a CA-signed certificate for any LCM-managed product.

**Step 1 — Generate a CSR:**

```bash
# On the LCM appliance (SSH)
# LCM can generate the CSR or you can supply your own
# Via UI: LCM → Locker → Certificates → Generate CSR
# Fill in: CN (product FQDN), SANs (all product node FQDNs + VIP), key size 4096
```

**Step 2 — Submit CSR to CA and retrieve the signed certificate chain.**

**Step 3 — Import the signed certificate into Locker:**

```bash
# Via API
TOKEN=$(curl -sk -X POST "https://lcm-prod-01.corp.local/lcm/authz/api/v2/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<password>"}' | jq -r '.token')

# Import certificate (PEM-encoded leaf + intermediates + root, and private key)
curl -sk -X POST -H "x-xenon-auth-token: $TOKEN" \
  -H "Content-Type: application/json" \
  "https://lcm-prod-01.corp.local/lcm/locker/api/v2/certificates/import" \
  -d '{
    "alias": "vrops-prod-cert-2026",
    "certificateChain": "<PEM chain as single escaped string>",
    "privateKey": "<PEM private key as single escaped string>"
  }'
```

Via UI: **LCM → Locker → Certificates → Import Certificate** — paste PEM content for each field.

**Step 4 — Apply the certificate to the product:**

LCM → Lifecycle Operations → Environments → select product → **Replace Certificate** → choose the new Locker alias → confirm.

LCM applies the certificate to all product nodes. Monitor via **Requests**.

---

## Rotate a Password in Locker

When a service account password is changed at source (vCenter, AD, database):

1. LCM → Locker → Passwords → locate the alias for the changed credential
2. Click **Edit** → update the password value
3. Navigate to all products that use this credential and re-validate their connections
4. For vCenter-linked credentials: LCM → Settings → vCenter Server → edit → re-validate

---

## Add a vCenter Server to LCM

```
LCM → Settings → vCenter Server → Add vCenter Server
```

Provide:
- vCenter FQDN (must be resolvable from LCM appliance)
- Username: `svc-lcm@vsphere.local` (dedicated service account — not administrator@vsphere.local)
- Password (stored in Locker automatically)
- Accept the vCenter SSL thumbprint

Required vCenter permissions for the LCM service account:

| Permission | Scope |
|---|---|
| Virtual Machine — Create New | Datacenter |
| Virtual Machine — Power | All VMs |
| Datastore — Allocate Space | Target datastores |
| Network — Assign Network | Target port groups |
| Host — CIM Interaction | All hosts |
| Global — Cancel Task | Global |

---

## Content Migration Between Environments

When promoting content (dashboards, blueprints, templates) from a lower environment (Dev) to production via LCM Content Lifecycle Manager:

1. LCM → **Content Lifecycle Manager** → select source environment
2. Select content type: Aria Operations dashboards / Aria Automation blueprints
3. Click **Extract** — creates a content snapshot
4. Navigate to the target environment → **Deploy Content**
5. Select the extracted content snapshot and map any environment-specific variables (cloud account names, network profiles)
6. Click **Deploy** — monitor via Requests

---

## Register VIDM (Workspace ONE Access)

If VIDM was deployed separately (not via Easy Installer) or needs to be re-registered:

```
LCM → Settings → Identity Manager → Configure
```

Provide:
- VIDM FQDN
- Admin username and password
- LCM then registers itself as a client in VIDM and configures SSO

All subsequently deployed Aria products automatically use the registered VIDM as their SSO source.

---

## Decommission a Product from LCM

1. Ensure the product has no active integrations (e.g., Aria Automation cloud accounts pointing to Aria Operations)
2. LCM → Lifecycle Operations → Environments → product card → **Delete**
3. LCM runs a pre-delete check and then powers off and deletes the product VMs from vCenter
4. Remove the product's DNS records and IP address reservations from IPAM
5. Archive the product's Locker credentials (do not delete until confirmed decommissioned)
