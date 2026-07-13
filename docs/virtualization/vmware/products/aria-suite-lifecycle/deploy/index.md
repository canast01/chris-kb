---
tags:
  - aria-lcm
  - deployment
  - vmware
search:
  boost: 1.5
description: "End-to-end deployment guide for Aria Suite Lifecycle Manager (LCM). Covers OVA deployment, VAMI first-boot configuration, Locker setup, depot..."
---
# Aria Suite Lifecycle — Deploy

<div class="kb-summary">
End-to-end deployment guide for Aria Suite Lifecycle Manager (LCM). Covers OVA deployment, VAMI first-boot configuration, Locker setup, depot synchronisation, vCenter infrastructure account registration, and first product environment creation. LCM must be deployed and validated before any Aria product can be deployed or managed.

*Applies to: Aria LCM 8.x*
</div>

---

```d2
direction: right

plan: "Plan" {shape: oval}
phase_1_preflight_checks: "Phase 1 — Pre-Flight Checks" {shape: rectangle}
phase_2_lcm_ova_deployment: "Phase 2 — LCM OVA Deployment" {shape: rectangle}
phase_3_certificate_configuration_an: "Phase 3 — Certificate Configuration and Locker Setup" {shape: rectangle}
phase_4_depot_configuration_and_vcen: "Phase 4 — Depot Configuration and vCenter Integration" {shape: rectangle}
phase_5_environment_creation_and_pro: "Phase 5 — Environment Creation and Product Deployment" {shape: rectangle}
phase_6_postdeployment_validation: "Phase 6 — Post-Deployment Validation" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> phase_1_preflight_checks
phase_1_preflight_checks -> phase_2_lcm_ova_deployment
phase_2_lcm_ova_deployment -> phase_3_certificate_configuration_an
phase_3_certificate_configuration_an -> phase_4_depot_configuration_and_vcen
phase_4_depot_configuration_and_vcen -> phase_5_environment_creation_and_pro
phase_5_environment_creation_and_pro -> phase_6_postdeployment_validation
phase_6_postdeployment_validation -> validate
```

## Before you begin

- **Access:** vCenter Administrator role and SSH access to VCSA/ESXi hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

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


```text title="Expected output"
Server:		10.10.10.1
Address:	10.10.10.1#53

Name:	lcm.example.local
Address: 10.10.10.40
Address: 10.10.10.41

Server:		10.10.10.1
Address:	10.10.10.1#53

40.10.10.10.in-addr.arpa	name = lcm.example.local.
40.10.10.10.in-addr.arpa	name = lcm-secondary.example.local.
```

!!! warning "Common errors"
    **`** server can't find lcm.example.local: NXDOMAIN`** — Verify the DNS A record exists in your DNS server and check that your resolver is configured to query the correct nameserver.
    **`** server can't find 10.10.10.40.in-addr.arpa: NXDOMAIN`** — Ensure reverse DNS (PTR record) is configured for 10.10.10.40 on your DNS server.
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


```text title="Expected output"
HTTP 302
root@lcm.example.local's password: 
● lcm-vmon.service - VMware Lifecycle Manager vMon Service
     Loaded: loaded (/etc/systemd/system/lcm-vmon.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:23:45 UTC; 2h 14min ago
       Docs: man:systemd.unit(5)
    Process: 2847 ExecStart=/opt/vmware/lcm/bin/vmon-service.sh start (code=exited, status=0/SUCCESS)
   Main PID: 2891 (java)
      Tasks: 47 (limit: 4915)
     Memory: 1.2G
        CPU: 18min 34.231s
     CGroup: /system.slice/lcm-vmon.service
             └─2891 /usr/lib/jvm/java-11-openjdk-11.0.18.0.10-1.el7_9.x86_64/bin/java -Xmx2g...
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to curl to skip certificate verification, or import the LCM certificate into your system CA bundle.
    **`ssh: connect to host lcm.example.local port 22 (Connection refused)`** — Verify the LCM appliance is powered on and SSH is enabled; check network connectivity with `ping lcm.example.local`.
    **`Unit lcm-vmon.service could not be found.`** — SSH into the appliance and verify the LCM service name with `systemctl list-units --all | grep lcm`, then use the correct service name.
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


```text title="Expected output"
subject=CN = lcm.example.local, O = Example Corp, C = US
issuer=CN = Example Corp Internal CA, O = Example Corp, C = US
notBefore=Jan 15 10:22:33 2024 GMT
notAfter=Jan 15 10:22:33 2025 GMT
```

!!! warning "Common errors"
    **`unable to get local issuer certificate`** — The internal CA certificate is not in the system trust store; add it to `/etc/pki/ca-trust/source/anchors/` and run `update-ca-trust`.
    **`Verify return code: 21 (unable to verify the first certificate)`** — The certificate chain is incomplete; ensure the intermediate CA certificate is installed on the LCM appliance in the certificate chain file.
    **`subject=CN = lcm.example.local` does not match expected hostname** — Update the certificate with the correct FQDN or add a Subject Alternative Name (SAN) entry for the actual hostname and redeploy.
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


```text title="Expected output"
root@lcm.example.local's password: 
total 18G
drwxr-xr-x  4 root root 4.0K Nov 15 10:23 .
drwxr-xr-x  3 root root 4.0K Nov 10 08:45 ..
-rw-r--r--  1 root root 4.2G Nov 15 09:12 vRealize-Automation-8.10.0-20231101.pak
-rw-r--r--  1 root root 3.8G Nov 15 09:18 vRealize-Operations-8.13.0-20231105.pak
-rw-r--r--  1 root root 2.1G Nov 15 09:25 vRealize-Log-Insight-8.14.0-20231108.pak
-rw-r--r--  1 root root 2.9G Nov 15 09:31 vRealize-Business-7.6.0-20231112.pak
-rw-r--r--  1 root root 4.7G Nov 15 09:42 vSAN-8.0.1-20231115.pak
drwxr-xr-x  2 root root 4.0K Nov 15 10:15 checksums
```

!!! warning "Common errors"
    **`Permission denied (publickey,password).`** — Verify SSH credentials and that root login is enabled in /etc/ssh/sshd_config on the LCM appliance.
    **`ls: cannot access '/data/lcm/binary-store/': No such file or directory`** — Confirm the LCM appliance is fully deployed and the binary-store directory exists; check mount points with `df -h`.
    **`Connection refused`** — Ensure the LCM appliance is powered on and SSH service is running; verify network connectivity with `ping lcm.example.local`.
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


```text title="Expected output"
Connected to lcm.example.local.
Last login: Wed Mar 15 14:32:18 2024 from 10.45.120.88
[root@lcm-prod-01 ~]# tail -f /var/log/vmware/lcm/lcm-install.log
2024-03-15T14:35:22.441Z [INFO] LCM Request ID: req-8f4c2a9b-7e1d-4f92-b8c3-2d5e9a1c3f7b
2024-03-15T14:35:23.156Z [INFO] Starting deployment of Aria Suite components
2024-03-15T14:35:45.892Z [INFO] Validating infrastructure prerequisites
2024-03-15T14:36:12.334Z [INFO] Configuring vCenter integration: vcenter.example.local
2024-03-15T14:36:58.721Z [INFO] Deploying Aria Automation appliance (aria-auto-01.example.local)
2024-03-15T14:37:15.443Z [INFO] Appliance network configuration: 10.45.120.45/24, GW: 10.45.120.1
2024-03-15T14:38:02.667Z [INFO] Deploying Aria Operations appliance (aria-ops-01.example.local)
2024-03-15T14:39:44.891Z [WARN] High memory utilization detected on ESXi host esx-04.example.local (87%)
2024-03-15T14:40:21.556Z [INFO] Configuring Aria Operations analytics cluster
2024-03-15T14:41:33.778Z [INFO] Deployment 45% complete - estimated 18 minutes remaining
```

!!! warning "Common errors"
    **`Permission denied (publickey,password).`** — Verify SSH key is loaded with `ssh-add` or use password authentication; confirm root account is enabled on LCM appliance.
    **`tail: cannot open '/var/log/vmware/lcm/lcm-install.log' for reading: No such file or directory`** — Confirm LCM deployment has started and the log directory exists; check actual log path with `find /var/log -name "*lcm*" -type f`.
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


```text title="Expected output"
HTTP 200
HTTP 200
HTTP 200
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to vrops.example.local port 443: Connection refused`** — Verify the Aria Operations appliance is powered on and network connectivity exists using `ping vrops.example.local`.
    **`curl: (60) SSL certificate problem: self signed certificate`** — The `-k` flag should suppress this, but if it appears, ensure you're using curl version 7.10 or later with `curl --version`.
    **`HTTP 000`** — The appliance is reachable but the service hasn't fully initialized; wait 2-3 minutes after deployment and retry the health check.
All should return HTTP 200 or 302.

### Verify Locker Certificate Expiry

LCM → Locker → Certificates — confirm all certificates have at least 30 days validity remaining.

```bash
ssh root@lcm.example.local
# Check LCM's own certificate expiry
openssl s_client -connect lcm.example.local:443 2>/dev/null \
  | openssl x509 -noout -enddate
```


```text title="Expected output"
depth=0 CN = lcm.example.local
verify error:num=18:self signed certificate
verify return:1
depth=0 CN = lcm.example.local
verify return:1
notAfter=Dec 15 09:23:47 2025 GMT
```

!!! warning "Common errors"
    **`connect: Connection refused`** — Verify LCM is running and listening on port 443 with `netstat -tlnp | grep 443` or check firewall rules blocking the connection.
    **`unable to load certificate`** — The SSL handshake failed or the certificate chain is incomplete; try adding `-showcerts` to `openssl s_client` to diagnose the full chain.
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

---

## See also

- [Aria Suite Lifecycle — How It Works](../architecture/how-it-works/)
- [Aria Suite Lifecycle — Health Checks](../operations/health-checks/)
- [Aria Suite Lifecycle — Common Issues](../troubleshooting/common-issues/)

## Verify

- **vSphere Client:** confirm the component is visible and shows a healthy status
- **Alarms:** Home → Alarms — no new critical alarms after deployment
- **Logs:** review vmware.log / recent events for any errors in the first 5 minutes
