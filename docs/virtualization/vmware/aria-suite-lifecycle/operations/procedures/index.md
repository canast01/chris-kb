# Aria Suite Lifecycle — Procedures


<div class="kb-summary">
Procedures reference covering Rotate a Password in Locker, Add a vCenter Server to LCM, Content Migration Between Environments, Register VIDM (Workspace ONE Access), Decommission a Product from LCM.
</div>

  LCM Common Procedures
```
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
```
┌────────────────────────────────────── Aria Suite LCM Procedures ──────────────────────────────────────┐
│                                                                                                       │
│  Certificate rotation, password rotation, and add product procedures for LCM.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Certificate Rotation             │  │              Password Rotation              │   │
│   │          1. Import new cert to LCM           │  │          1. Update account password         │   │
│   │        2. Assign cert to environment         │  │          2. LCM: Locker > Password          │   │
│   │         3. LCM: replace cert action          │  │         3. Update stored credential         │   │
│   │           4. Validate all products           │  │            4. Test product health           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Cert rotation via LCM covers all nodes; password rotation via LCM Locker.                            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Add Product to Environment          │  │                Remove Product               │   │
│   │         1. Depot: ensure PAK synced          │  │            1. LCM: Delete product           │   │
│   │         2. Environment > Add Product         │  │           2. LCM removes from env           │   │
│   │          3. Complete product wizard          │  │            3. Delete VM manually            │   │
│   │         4. Validate health post-add          │  │           4. Clean DNS + firewall           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LCM VM; managed product VMs on vSphere; CA for cert signing; AD for accounts                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cert Rotation       = LCM replaces TLS cert across all nodes of a product                            │
│  LCM Locker          = Secure password store in LCM; holds all product creds                          │
│  Password Rotation   = Update credential in LCM Locker after account pw change                        │
│  Cert Import         = Upload CA-signed cert and key to LCM trust store                               │
│  Cert Assignment     = Link imported cert to an environment or specific product                       │
│  Replace Cert Action = LCM-orchestrated cert push to all product VMs                                  │
│  Add Product         = Deploy new Aria product into existing LCM environment                          │
│  Product Wizard      = LCM UI wizard collecting hostname, IP, size for new product                    │
│  Remove Product      = LCM unregisters product; VM must be deleted separately                         │
│  PAK Sync            = Required before adding product; ensures binary is available                    │
│  Health Validation   = Post-procedure check that all products remain green                            │
│  Credential Test     = LCM verifies stored account password still authenticates                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

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

```text
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

```text
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
