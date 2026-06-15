---
tags:
  - aria-lcm
  - operations
  - vmware
---
# Aria Suite Lifecycle — Procedures


<div class="kb-summary">
Procedures reference covering Rotate a Password in Locker, Add a vCenter Server to LCM, Content Migration Between Environments, Register VIDM (Workspace ONE Access), Decommission a Product from LCM.

*Applies to: Aria LCM 8.x*
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
Via UI: **LCM → Locker → Certificates → Import Certificate** — paste PEM content for each field.

**Step 4 — Apply the certificate to the product:**

LCM → Lifecycle Operations → Environments → select product → **Replace Certificate** → choose the new Locker alias → confirm.

LCM applies the certificate to all product nodes. Monitor via **Requests**.

---

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Rotate a Password in Locker

When a service account password is changed at source (vCenter, AD, database):

1. LCM → Locker → Passwords → locate the alias for the changed credential
2. Click **Edit** → update the password value
3. Navigate to all products that use this credential and re-validate their connections
4. For vCenter-linked credentials: LCM → Settings → vCenter Server → edit → re-validate

---

## Add a vCenter Server to LCM
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

!!! warning "External integrations using the rotated credentials will break immediately"
    LCM rotates passwords within the Aria product stack, but any external system that authenticates using these credentials — ITSM connectors, monitoring agents, custom ABX actions, CI/CD pipelines — will fail the moment the rotation completes. Before rotating, enumerate all external callers and prepare to update their stored credentials immediately after rotation. Step 6 is time-critical.

1. LCM → Lifecycle Operations → Environments → select the environment
2. Click **Rotate Passwords** → select scope: **All Products** (or select individual products)
3. Confirm the operation — LCM generates new passwords and updates them across all product nodes
4. Monitor via **Requests** — each product's password rotation shown as a subtask
5. After completion: verify no service disruptions — check product health for all components in the environment
6. Update any external integrations (ITSM connectors, monitoring agents) that use the rotated credentials

---

## Decommission an Environment

!!! danger "Permanently deletes all product VMs across the entire environment"
    Step 3 triggers LCM to power off and delete every product VM (Aria Operations, Aria Automation, Aria Logs, vIDM) registered in this environment from vCenter. There is no undo. Confirm all integrations are removed, all data is archived, and all dependent services are decommissioned before proceeding.

1. Confirm all workloads have been migrated off the environment — no active VMs or services should depend on it
2. Remove all external integrations pointing to the environment (cloud accounts, monitoring adapters, ITSM plugins)
3. LCM → Lifecycle Operations → Environments → select the environment → **Delete**
4. LCM runs a pre-delete check and then removes all product registrations from its database
5. LCM powers off and deletes product VMs from the linked vCenter
6. Verify in vCenter that all product VMs are deleted and datastores freed
7. Clean up: remove DNS records, IP reservations from IPAM, and firewall rules for the decommissioned environment

---

## Upgrade the Aria Suite Lifecycle Appliance

Prerequisites: take a snapshot of the LCM VM before starting; verify the target version is supported in the Broadcom compatibility matrix at `https://interopmatrix.broadcom.com`.

1. Log in to the LCM UI as `admin@local`
2. Navigate to **Settings → Lifecycle Management**
3. Click **Check for Updates** — LCM queries the depot for available appliance updates
4. Select the target update and click **Download** — wait for the download to complete (progress shown in **Tasks**)
5. Click **Apply Update** — the appliance will restart; the UI will be unavailable for 5–15 minutes
6. Monitor upgrade progress via **Settings → Lifecycle Management → Tasks**
7. After restart, log back in and navigate to **Settings → About** — confirm the new version is displayed
8. Verify all managed environments: **Lifecycle Operations → Environments** — all product cards should return to green within 5 minutes of LCM restart

Rollback: if the update fails, revert to the pre-upgrade snapshot from vCenter and raise a Broadcom support case with the upgrade log from `/var/log/vmware/vrlcm/lcm-install.log`.

---

## Configure Custom SSL Certificates for LCM

!!! warning "All managed Aria products lose trust with LCM when the cert changes"
    LCM uses its certificate as a trust anchor for all managed product integrations. After replacing the cert, every registered Aria product (Aria Operations, Aria Automation, Aria Logs, vIDM) will report a trust failure against LCM until re-registered or reconfigured to trust the new cert. Plan a maintenance window, notify all users, and execute step 5 immediately after the cert change.

Changing the LCM appliance certificate affects all browser sessions and all managed-product trust anchors. Plan a maintenance window and notify all users.

1. Generate a CSR: **Settings → Certificate Management → Generate CSR** — provide the LCM FQDN as the Common Name; add SANs for any additional hostnames or IPs
2. Download the CSR and submit to your internal CA; obtain a signed certificate in PEM format
3. Import the signed cert: **Settings → Certificate Management → Import Certificate** — paste the signed cert, intermediate chain, and private key into the respective fields
4. Apply the certificate — LCM restarts the web service; verify the browser shows the new cert via the padlock icon
5. After cert replacement: all managed Aria products lose trust with LCM; navigate to each product's trust configuration and re-import the new LCM certificate or re-register the products via LCM
6. Test authentication flows (VIDM SSO, vCenter connectivity) after the cert change is complete

---

## Request and Install Product Certificates via LCM

LCM can push CA-signed certificates to managed Aria products, replacing self-signed certificates issued at deployment.

1. Add your CA certificate to the LCM Locker: **Locker → Certificates → Import** — import the CA root and intermediate chain; give it a descriptive alias (e.g., `internal-ca-2026`)
2. Navigate to **Lifecycle Operations → Environments** → select the target environment
3. On the product card, click **Request Certificate** → select the CA alias from the Locker → fill in the certificate template (SAN entries, validity period) → click **Submit**
4. LCM generates the CSR, submits it to the CA, retrieves the signed certificate, and pushes it to all product nodes
5. Monitor via **Lifecycle Operations → Requests** — each node cert push is a separate subtask
6. For products that require a service restart after cert installation (Aria Automation, Aria Operations for Networks): LCM will prompt to restart; confirm to complete the push
7. Validate by opening the product URL in a browser and inspecting the certificate — subject and SAN should match the requested values

---

## Add a Global Environment (Multi-vCenter)

A Global Environment in LCM spans multiple vCenter deployments, enabling a single LCM instance to manage Aria products across sites.

1. Navigate to **Lifecycle Operations → Environments → New Environment**
2. Set environment type to **Global**
3. Add vCenter registrations for each site: for each vCenter provide the FQDN, service account credentials, and accept the SSL thumbprint — LCM stores credentials in the Locker automatically
4. Configure cross-site networking: ensure the LCM appliance has routable connectivity to management networks in each site (firewall rules: TCP 443 and TCP 22 from LCM to each vCenter and ESXi management)
5. Deploy products to site-specific vCenters by selecting the target vCenter during the product wizard; product VMs are deployed locally at each site
6. Verify global environment health: **Lifecycle Operations → Environments → select the global environment** — each site's vCenter should show as Connected and each deployed product should show green
7. If a site vCenter shows Disconnected: re-validate credentials via **Settings → vCenter Servers → select vCenter → Test Connection**

---

## Configure LCM Backup (File-Based)

LCM supports scheduled file-based backups to SFTP or NFS. The backup captures the LCM database, Locker contents, and configuration.

1. Navigate to **Settings → Backup and Restore → File Based Backup**
2. Enable the backup toggle
3. Configure the destination:
   - **SFTP**: provide hostname, port (default 22), remote path, username, and password
   - **NFS**: provide the NFS server and export path (LCM mounts it automatically)
4. Set a schedule — daily at a low-activity time (e.g., 02:00); set retention to 7 days minimum
5. Click **Backup Now** to trigger an immediate test backup
6. After the backup completes, SSH to the backup target and verify the file exists:
   ```bash
   ls -lh /backup/lcm-backup-*
   # Expect a file timestamped within the last few minutes
   ```
7. Confirm the backup size is non-zero and the filename includes the LCM version and timestamp

---

## Run Environment Compliance Check

Compliance checks detect version drift — managed products that have diverged from the LCM-tracked baseline, typically due to manual upgrades or patches applied outside LCM.

1. Navigate to **Lifecycle Operations → Environments** → select the target environment
2. Click **Compliance → Run Compliance Check**
3. LCM compares the installed version of each product against the versions recorded in its database and against the latest available in the Locker
4. Review the compliance report:
   - **Compliant**: product version matches LCM baseline — no action required
   - **Non-Compliant**: version mismatch detected — product was upgraded outside LCM or LCM baseline is stale
   - **Unknown**: LCM cannot reach the product to determine version — investigate connectivity
5. Remediate non-compliant products: if the product is ahead of LCM's record, update the LCM inventory entry; if behind, initiate an upgrade via LCM
6. Schedule compliance checks monthly or after any change freeze ends

---

## Restore LCM from Backup

Use this procedure when the LCM appliance is unrecoverable and no snapshot is available.

1. Deploy a fresh LCM OVA from the Broadcom portal — use the same version as the backup was taken from (version mismatch will cause restore failure)
2. Assign the same IP address and FQDN as the original LCM appliance; update DNS if needed
3. Complete initial setup (set admin password, accept EULA) — do not configure any environments or vCenters at this stage
4. Log in to the restored LCM UI → navigate to **Settings → Backup and Restore → Restore**
5. Specify the backup location (SFTP or NFS) and credentials matching the backup destination
6. Select the target backup file and click **Restore** — LCM will restart multiple times during the restore process; this may take 20–40 minutes
7. After restore completes, log in and verify the environment inventory is repopulated: **Lifecycle Operations → Environments** — all environments and products should be visible
8. Run a health check against each environment: **Environments → select env → Health Check** — resolve any connectivity issues caused by IP or certificate changes during the rebuild

---

## Configure HA for LCM (Active-Passive)

LCM does not include built-in clustering. HA is achieved using vSphere HA for automatic restart and a standby clone with a documented manual failover procedure.

1. Take a snapshot of the active LCM VM (label: `lcm-ha-standby-base`)
2. Clone the LCM VM to a standby VM on a different ESXi host or cluster; keep the standby VM powered off
3. Configure vSphere HA on the cluster hosting the active LCM VM — this covers automatic restart on host failure (RTO: 3–5 minutes)
4. For faster RTO with a VIP: configure a load-balancer VIP (F5 or NSX ALB) pointing to the active LCM IP; update DNS to resolve the LCM FQDN to the VIP
5. Document the manual failover procedure:
   1. Power off the active LCM VM (or confirm it is already down)
   2. Power on the standby clone
   3. If using DNS (no VIP): update the A record for the LCM FQDN to point to the standby IP; wait for TTL to propagate
   4. If using VIP: update the VIP pool member to point to the standby IP
   5. Verify LCM UI is accessible at the FQDN
   6. Run environment health checks to confirm all managed products reconnect
6. Test failover in a maintenance window every 6 months; resync the standby clone from a fresh snapshot of the active LCM after each test

---

## See also

- [Aria Suite Lifecycle — Health Checks](health-checks/)
- [Aria Suite Lifecycle — Common Issues](../troubleshooting/common-issues/)
- [Aria Suite Lifecycle — CLI Reference](cli-reference/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
