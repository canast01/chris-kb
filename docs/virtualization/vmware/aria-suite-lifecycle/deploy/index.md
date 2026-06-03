# Aria Suite Lifecycle — Deploy

<div class="kb-summary">
End-to-end deployment guide for Aria Suite Lifecycle Manager (LCM). Covers OVA deployment, VAMI first-boot configuration, Locker setup, depot synchronisation, vCenter infrastructure account registration, and first product environment creation. LCM must be deployed and validated before any Aria product can be deployed or managed.
</div>

```text
┌───────────────────────── Aria Suite Lifecycle Manager — Deployment Phases ────────────────────────────┐
│                                                                                                       │
│  Six phases from bare metal to LCM managing its first product environment.                            │
│  LCM must be stable and depot-synced before deploying any Aria product through it.                    │
│                                                                                                       │
│  ┌──────────────────────────┐  ┌──────────────────────────┐  ┌──────────────────────────────────┐     │
│  │  Phase 1: Pre-Flight     │  │  Phase 2: LCM OVA Deploy │  │     Phase 3: VAMI & Locker       │     │
│  │  DNS A + PTR for LCM     │  │  Deploy LCM OVA          │  │   Complete VAMI setup wizard     │     │
│  │  NTP sources confirmed   │  │  Set IP, FQDN, NTP, DNS  │  │   Upload CA root + intermediates │     │
│  │  vCenter svc account     │  │  Set admin password       │  │   Configure Locker passwords     │    │
│  │  Datastore ≥ 50 GB free  │  │  Power on → access UI    │  │   Assign cert to LCM itself      │     │
│  │  Product FQDNs in DNS    │  │  Accept EULA + licence   │  │   Verify UI trusted cert         │     │
│  └──────────────────────────┘  └──────────────────────────┘  └──────────────────────────────────┘     │
│                                                                                                       │
│               ▼                             ▼                                ▼                        │
│                                                                                                       │
│  ┌──────────────────────────┐  ┌──────────────────────────┐  ┌──────────────────────────────────┐     │
│  │  Phase 4: Depot + vCenter│  │  Phase 5: Environment    │  │      Phase 6: Validation         │     │
│  │  Configure depot (online │  │  Create product env      │  │   LCM UI accessible HTTPS 443    │     │
│  │  or NFS local)           │  │  Add vIDM first          │  │   Locker: certs + passwords OK   │     │
│  │  Sync product binaries   │  │  Add Aria products       │  │   Depot: PAKs downloaded         │     │
│  │  Add vCenter infra acct  │  │  LCM runs pre-checks     │  │   Environment health: green      │     │
│  │  Test inventory browse   │  │  Monitor deploy tasks    │  │   Product UIs reachable          │     │
│  └──────────────────────────┘  └──────────────────────────┘  └──────────────────────────────────┘     │
│                                                                                                       │
│  Physical Infrastructure: LCM VM on vSphere (≥50 GB datastore, static IP);                            │
│  vCenter service account; NFS or internet access for depot; product FQDN DNS entries.                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Locker          = LCM internal vault; stores passwords, TLS certificates, and licence keys           │
│  Depot           = Binary source for product PAK files; online (Broadcom) or local NFS                │
│  Environment     = Named grouping of Aria products sharing a vCenter account and cert authority       │
│  Infrastructure  = LCM term for the vCenter account used to deploy product VMs                        │
│  PAK file        = Product Activation Key; binary bundle used to deploy or upgrade an Aria product    │
│  Pre-check       = LCM automated validation run before each deploy or upgrade operation               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1 — Pre-Flight Checks

**Exit criterion:** DNS resolves forward and reverse for the LCM FQDN and all planned product FQDNs; vCenter service account prepared; datastore has capacity.

### DNS Records

Create DNS A and PTR records for LCM and every Aria product you plan to deploy through it before deploying the OVA. LCM validates FQDN resolution before deploying each product.

| Host | Example IP | Notes |
|---|---|---|
| LCM appliance | `10.10.10.40` | A + PTR required |
| Aria Operations (vROps) | `10.10.10.41` | A + PTR required |
| Aria Ops for Logs (vRLI) | `10.10.10.42` | A + PTR required |
| Aria Automation (vRA) | `10.10.10.43` | A + PTR required |

```bash
nslookup lcm.example.local
nslookup 10.10.10.40
# Both must resolve correctly before proceeding
```

### vCenter Service Account

The LCM infrastructure account requires the following vCenter privileges:

- Create and delete VMs
- Configure networking and datastores
- Power operations on VMs
- vApp deployment

Minimum: assign the **Administrator** role at the **datacenter level** (not global) to a dedicated service account such as `svc-lcm@vsphere.local`.

### Resource Requirements

| Component | vCPU | RAM | Disk | Use case |
|---|---|---|---|---|
| LCM appliance (small) | 2 | 6 GB | 50 GB | Lab only |
| LCM appliance (medium) | 4 | 16 GB | 100 GB | Production |

---

## Phase 2 — LCM OVA Deployment

**Exit criterion:** LCM UI accessible at `https://lcm.example.local`; initial setup wizard complete.

### Download and Deploy OVA

Download from Broadcom Support Portal: My Downloads → Aria Suite Lifecycle.

OVA filename example: `VMware-Aria-Suite-Lifecycle-Manager-8.x.x.ova`

Deploy via vCenter: Actions → Deploy OVF Template, then set OVF properties:

| Property | Example Value |
|---|---|
| IP Address | `10.10.10.40` |
| Subnet Mask | `255.255.255.0` |
| Default Gateway | `10.10.10.1` |
| DNS Server 1 | `10.10.0.1` |
| DNS Server 2 | `10.10.0.2` |
| Hostname (FQDN) | `lcm.example.local` |
| NTP Server | `ntp.example.local` |
| Admin Password | *(set initial password)* |

Power on. First boot takes 5–10 minutes.

### Verify LCM Is Accessible

```bash
# HTTPS reachable
curl -sk https://lcm.example.local -o /dev/null -w "HTTP %{http_code}\n"
# Expected: HTTP 200 or 302 redirect to login

# SSH to LCM appliance as root (use VAMI credentials)
ssh root@lcm.example.local
systemctl status lcm-vmon
# Should show: Active (running)
```

### Accept EULA and Enter Licence

1. Browse to `https://lcm.example.local`.
2. Log in with `admin` and the password set during OVA deploy.
3. Accept EULA.
4. Enter the Aria Suite Lifecycle licence key.
5. Complete the initial setup wizard.

---

## Phase 3 — Certificate Configuration and Locker Setup

**Exit criterion:** LCM UI served with a CA-trusted certificate; Locker operational with at least one certificate imported.

### Upload CA Certificate to LCM Trust Store

LCM → Locker → Certificates → Import CA Certificate

```text
Certificate Type:  CA Certificate
Alias:             corp-root-ca
Certificate:       (paste PEM of your root CA)
```

If using a chain (root + intermediate), import both separately or as a bundle.

### Create Certificate Request for LCM Itself

LCM → Locker → Certificates → Generate CSR

```text
Common Name (CN):   lcm.example.local
Organisation:       Example Corp
Org Unit:           IT Infrastructure
Country:            GB
SANs:               lcm.example.local, 10.10.10.40
Key Size:           2048
```

Sign the generated CSR with your internal CA, then import the signed certificate back into LCM:

LCM → Locker → Certificates → Import Signed Certificate → select the alias for the CSR.

### Assign Certificate to LCM Appliance

LCM → Settings → SSL Certificates → replace the self-signed cert with the newly imported CA-signed cert. LCM services restart (~2 minutes).

```bash
# Verify cert after restart
openssl s_client -connect lcm.example.local:443 -showcerts 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
# CN must match lcm.example.local; Issuer must be your internal CA
```

### Configure Locker Passwords

LCM → Locker → Passwords → Add Password

Add passwords for all service accounts that LCM will use to deploy products:

```text
Alias:       vcenter-admin
Username:    svc-lcm@vsphere.local
Password:    ********
Description: vCenter infra account for LCM deployments
```

---

## Phase 4 — Depot Configuration and vCenter Integration

**Exit criterion:** Depot synchronised with at least one PAK binary available; vCenter infrastructure account registered and inventory browseable.

### Configure Depot

#### Online Depot (requires internet or proxy)

LCM → Settings → System Details → Depot Settings

```text
Depot Type:   VMware Online
My VMware account credentials (Broadcom login)
Proxy host/port if required
```

#### Local NFS Depot

```text
Depot Type:   NFS
NFS Server:   nas.example.local
NFS Path:     /exports/aria-binaries
Mount point auto-configured by LCM
```

### Sync Product Binaries

LCM → Lifecycle Operations → Settings → Binary Mapping → Sync

This downloads the product PAK catalogue. Download individual PAK files for products you intend to deploy:

```text
LCM → Settings → Binary Mapping → Available Binaries
→ Select: VMware Aria Operations 8.x.x PAK
→ Download to LCM
```

Verify download complete:

```bash
ssh root@lcm.example.local
ls -lh /data/lcm/binary-store/
# PAK files should be present with correct sizes
```

### Add vCenter Infrastructure Account

LCM → Lifecycle Operations → Settings → My VMware vCenter Servers → Add vCenter

```text
vCenter FQDN:   vcenter.example.local
Username:       svc-lcm@vsphere.local
Password:       (select from Locker)
```

Test the connection — LCM will validate connectivity and browse inventory. Confirm it can see datastores, clusters, and networks.

---

## Phase 5 — Environment Creation and Product Deployment

**Exit criterion:** First product environment created; at least vIDM (Workspace ONE Access) deployed and healthy before adding other Aria products.

### Create a Product Environment

LCM → Lifecycle Operations → Environments → Create Environment

```text
Environment Name:   prod-aria-suite
Datacenter:         select from vCenter inventory
vCenter:            vcenter.example.local (registered in Phase 4)
Default password:   select from Locker
```

### Deploy Workspace ONE Access (vIDM) First

Workspace ONE Access (vIDM) must be deployed first. All other Aria products register SSO through vIDM.

LCM → Environments → prod-aria-suite → Add Products → Workspace ONE Access

```text
Binary:           (select downloaded PAK)
Deployment Size:  Small (lab) / Medium (production)
VM Name:          vidm-01
FQDN:             vidm.example.local
IP:               10.10.10.44
Datastore:        (select from dropdown)
Network:          (select management port group)
```

Click **Submit** — LCM runs pre-checks and then deploys the OVA automatically. Monitor progress:

LCM → Requests → most recent request → View Details

### Add Aria Products to the Environment

After vIDM is healthy, add additional products:

```text
LCM → Environments → prod-aria-suite → Add Products
→ VMware Aria Operations
   Binary: select PAK, FQDN: vrops.example.local, IP: 10.10.10.41
→ VMware Aria Operations for Logs
   Binary: select PAK, FQDN: vrli.example.local, IP: 10.10.10.42
```

LCM deploys each product sequentially. Each product is validated by LCM post-deploy before the next begins.

```bash
# Check LCM request log for progress
ssh root@lcm.example.local
tail -f /var/log/vmware/lcm/lcm-install.log
```

---

## Phase 6 — Post-Deployment Validation

**Exit criterion:** LCM environment health dashboard shows all products green; each product UI is accessible; Locker certificates valid.

### LCM Environment Health Check

LCM → Lifecycle Operations → Environments → prod-aria-suite → Health Check

Run a health check. All products should show **Healthy**. Investigate any product showing **Warning** or **Error** before handing to operations.

### Verify Product UIs

```bash
# Aria Operations
curl -sk https://vrops.example.local -o /dev/null -w "HTTP %{http_code}\n"

# Aria Ops for Logs
curl -sk https://vrli.example.local -o /dev/null -w "HTTP %{http_code}\n"

# Workspace ONE Access (vIDM)
curl -sk https://vidm.example.local/SAAS/auth/login -o /dev/null -w "HTTP %{http_code}\n"
```

All should return HTTP 200 or 302.

### Verify Locker Certificate Expiry

LCM → Locker → Certificates — confirm all certificates have at least 30 days validity remaining.

```bash
ssh root@lcm.example.local
# Check LCM's own certificate expiry
openssl s_client -connect lcm.example.local:443 2>/dev/null \
  | openssl x509 -noout -enddate
```

### Post-Deployment Checklist

| Check | Expected Result |
|---|---|
| LCM UI accessible on HTTPS 443 | Login page loads with trusted CA cert |
| LCM appliance service healthy | `systemctl status lcm-vmon` shows running |
| Depot synced — PAKs available | Binary Mapping shows downloaded PAK files |
| vCenter infra account connected | LCM browses datacenter inventory |
| Locker certificates imported | At least LCM cert + CA root in Locker |
| Locker passwords configured | vCenter svc account in Locker |
| vIDM deployed and healthy | `https://vidm.example.local` returns HTTP 200 |
| All products show Healthy in env | LCM Health Check: all green |
| NTP synchronised | `chronyc tracking` offset < 1 s on LCM VM |
| DNS resolves all product FQDNs | Forward + reverse for each product IP |
