# Aria Suite Lifecycle — Procedures


<div class="kb-summary">
Procedures reference covering Rotate a Password in Locker, Add a vCenter Server to LCM, Content Migration Between Environments, Register VIDM (Workspace ONE Access), Decommission a Product from LCM.
</div>

  LCM Common Procedures
```text
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
```text
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
```text
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

---

## Add a Product to an Existing Environment

1. LCM → Lifecycle Operations → Environments → select the target environment
2. Click **Add Product** → select the product and version from the Locker (binary must already be imported)
3. Complete the product wizard: configure FQDN, IP addresses, sizing, and linked vCenter
4. Submit — LCM deploys the product VMs to the target vCenter
5. Monitor via **Requests** — each step shown with pass/fail status
6. Post-deploy: validate product health via **Environments → product card → Health Check**

---

## Scale Out an Existing Deployment (Add Node)

1. LCM → Lifecycle Operations → Environments → select the product to scale
2. Click **Scale Out** → select the node type: **Replica** (active-active) or **Worker** (processing node, product-dependent)
3. Configure IP address, FQDN, and vCenter placement for the new node
4. Submit — LCM deploys and joins the new node to the existing product cluster
5. Monitor via **Requests**
6. Post-deploy: validate cluster status — all nodes should show green in the product's own UI

---

## Upgrade a Product via LCM

1. LCM → Lifecycle Operations → Environments → product card → **Upgrade**
2. Select the target version (must be available in the Locker — import binary first if not present)
3. Click **Run Precheck** — LCM validates certificates, disk space, connectivity, and snapshot state
4. Resolve any Precheck failures before proceeding (common: expired certificates, low disk space)
5. Schedule the upgrade window — confirm outage impact with application teams
6. Click **Upgrade** — monitor each phase via **Requests**
7. Post-upgrade validation: product health check green, verify version in product UI, run smoke tests

---

## Import a Product Binary to the Locker

1. LCM → Locker → Product Binaries → **Import**
2. Choose import method:
   - **My VMware Download URL** — provide a direct download link (LCM downloads directly)
   - **Upload** — upload a locally downloaded binary from the LCM UI
3. LCM verifies the SHA-256 checksum after import — confirm the checksum matches VMware's published value
4. Binary is now listed in the Locker and available for new deployments and upgrades

---

## Rotate All Passwords for an Environment

1. LCM → Lifecycle Operations → Environments → select the environment
2. Click **Rotate Passwords** → select scope: **All Products** (or select individual products)
3. Confirm the operation — LCM generates new passwords and updates them across all product nodes
4. Monitor via **Requests** — each product's password rotation shown as a subtask
5. After completion: verify no service disruptions — check product health for all components in the environment
6. Update any external integrations (ITSM connectors, monitoring agents) that use the rotated credentials

---

## Decommission an Environment

1. Confirm all workloads have been migrated off the environment — no active VMs or services should depend on it
2. Remove all external integrations pointing to the environment (cloud accounts, monitoring adapters, ITSM plugins)
3. LCM → Lifecycle Operations → Environments → select the environment → **Delete**
4. LCM runs a pre-delete check and then removes all product registrations from its database
5. LCM powers off and deletes product VMs from the linked vCenter
6. Verify in vCenter that all product VMs are deleted and datastores freed
7. Clean up: remove DNS records, IP reservations from IPAM, and firewall rules for the decommissioned environment
