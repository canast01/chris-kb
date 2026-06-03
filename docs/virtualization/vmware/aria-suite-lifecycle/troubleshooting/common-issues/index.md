# Aria Suite Lifecycle — Common Issues


<div class="kb-summary">
Common Issues reference covering Upgrade Gets Stuck or Times Out, NFS Mount Lost During Operation, Locker Certificate Import Fails, VIDM Authentication Failure After Password Change, Product Shows Red Health in LCM Dashboard and 1 more sections.
</div>

  LCM Triage Decision Tree
```text
┌──────────────────────────────────── Aria Suite LCM Common Issues ─────────────────────────────────────┐
│                                                                                                       │
│  Common LCM issues: deployment failure, certificate mismatch, and disk full.                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Deployment Failure              │  │             Certificate Mismatch            │   │
│   │            Check pre-check result            │  │           Verify SAN matches FQDN           │   │
│   │            DNS: FQDN resolvable?             │  │            Re-import correct cert           │   │
│   │           vCenter: credentials OK?           │  │           LCM: replace cert action          │   │
│   │            Disk: LCM VM not full?            │  │           Check product cert trust          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Deployment failure and cert mismatch are most frequent; disk full causes both.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Disk Full Issue                │  │              vIDM / SSO Failure             │   │
│   │          df -h: find full partition          │  │            vIDM: service running?           │   │
│   │             Delete old PAK files             │  │           Check vIDM cert validity          │   │
│   │           Clean /tmp and log dirs            │  │           Test SSO login manually           │   │
│   │          Expand disk if persistent           │  │           Re-register LCM in vIDM           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LCM VM on vSphere; vCenter for deploy; vIDM for auth; NFS for depot and backup                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Deployment Failure  = LCM deploy action failed; check pre-check and installer.log                    │
│  Pre-check Result    = LCM validation output; shows root cause before deploy fails                    │
│  Cert Mismatch       = Product cert SAN does not match FQDN; causes TLS errors                        │
│  SAN                 = Subject Alternative Name; must include product FQDN                            │
│  Replace Cert Action = LCM-orchestrated cert replacement; resolves mismatch                           │
│  Disk Full           = LCM VM /storage or / partition full; blocks all operations                     │
│  PAK Cleanup         = Delete old PAK binaries from LCM depot to free disk                            │
│  /tmp Cleanup        = Clear temp files accumulated during failed deployments                         │
│  vIDM SSO Failure    = LCM cannot redirect auth; all users locked out                                 │
│  vIDM Re-register    = Re-add LCM as vIDM app if SSO trust is broken                                  │
│  installer.log       = Deployment log; shows exact step and error for failures                        │
│  df -h               = Disk usage check; first step for any disk-related issue                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────── Aria Suite LCM Common Issues ─────────────────────────────────────┐
│                                                                                                       │
│  Common LCM issues: deployment failure, certificate mismatch, and disk full.                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Deployment Failure              │  │             Certificate Mismatch            │   │
│   │            Check pre-check result            │  │           Verify SAN matches FQDN           │   │
│   │            DNS: FQDN resolvable?             │  │            Re-import correct cert           │   │
│   │           vCenter: credentials OK?           │  │           LCM: replace cert action          │   │
│   │            Disk: LCM VM not full?            │  │           Check product cert trust          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Deployment failure and cert mismatch are most frequent; disk full causes both.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Disk Full Issue                │  │              vIDM / SSO Failure             │   │
│   │          df -h: find full partition          │  │            vIDM: service running?           │   │
│   │             Delete old PAK files             │  │           Check vIDM cert validity          │   │
│   │           Clean /tmp and log dirs            │  │           Test SSO login manually           │   │
│   │          Expand disk if persistent           │  │           Re-register LCM in vIDM           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LCM VM on vSphere; vCenter for deploy; vIDM for auth; NFS for depot and backup                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Deployment Failure  = LCM deploy action failed; check pre-check and installer.log                    │
│  Pre-check Result    = LCM validation output; shows root cause before deploy fails                    │
│  Cert Mismatch       = Product cert SAN does not match FQDN; causes TLS errors                        │
│  SAN                 = Subject Alternative Name; must include product FQDN                            │
│  Replace Cert Action = LCM-orchestrated cert replacement; resolves mismatch                           │
│  Disk Full           = LCM VM /storage or / partition full; blocks all operations                     │
│  PAK Cleanup         = Delete old PAK binaries from LCM depot to free disk                            │
│  /tmp Cleanup        = Clear temp files accumulated during failed deployments                         │
│  vIDM SSO Failure    = LCM cannot redirect auth; all users locked out                                 │
│  vIDM Re-register    = Re-add LCM as vIDM app if SSO trust is broken                                  │
│  installer.log       = Deployment log; shows exact step and error for failures                        │
│  df -h               = Disk usage check; first step for any disk-related issue                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────── Aria Suite LCM Common Issues ─────────────────────────────────────┐
│                                                                                                       │
│  Common LCM issues: deployment failure, certificate mismatch, and disk full.                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Deployment Failure              │  │             Certificate Mismatch            │   │
│   │            Check pre-check result            │  │           Verify SAN matches FQDN           │   │
│   │            DNS: FQDN resolvable?             │  │            Re-import correct cert           │   │
│   │           vCenter: credentials OK?           │  │           LCM: replace cert action          │   │
│   │            Disk: LCM VM not full?            │  │           Check product cert trust          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Deployment failure and cert mismatch are most frequent; disk full causes both.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Disk Full Issue                │  │              vIDM / SSO Failure             │   │
│   │          df -h: find full partition          │  │            vIDM: service running?           │   │
│   │             Delete old PAK files             │  │           Check vIDM cert validity          │   │
│   │           Clean /tmp and log dirs            │  │           Test SSO login manually           │   │
│   │          Expand disk if persistent           │  │           Re-register LCM in vIDM           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LCM VM on vSphere; vCenter for deploy; vIDM for auth; NFS for depot and backup                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Deployment Failure  = LCM deploy action failed; check pre-check and installer.log                    │
│  Pre-check Result    = LCM validation output; shows root cause before deploy fails                    │
│  Cert Mismatch       = Product cert SAN does not match FQDN; causes TLS errors                        │
│  SAN                 = Subject Alternative Name; must include product FQDN                            │
│  Replace Cert Action = LCM-orchestrated cert replacement; resolves mismatch                           │
│  Disk Full           = LCM VM /storage or / partition full; blocks all operations                     │
│  PAK Cleanup         = Delete old PAK binaries from LCM depot to free disk                            │
│  /tmp Cleanup        = Clear temp files accumulated during failed deployments                         │
│  vIDM SSO Failure    = LCM cannot redirect auth; all users locked out                                 │
│  vIDM Re-register    = Re-add LCM as vIDM app if SSO trust is broken                                  │
│  installer.log       = Deployment log; shows exact step and error for failures                        │
│  df -h               = Disk usage check; first step for any disk-related issue                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

If the upgrade is truly stuck (no log activity for 30+ minutes):
1. Do NOT power off product VMs — this risks split-brain state
2. Open a Broadcom SR with the LCM log bundle and the request ID
3. LCM may offer a **Retry** option for some stuck states — use only if advised by support

---

## NFS Mount Lost During Operation

If the NFS share becomes unavailable while LCM is running:

```bash
# Check mount status
mount | grep /data
df -h /data

# Attempt remount
mount -a
# or explicitly:
mount -t nfs <nfs-server>:/lcm-repo /data

# Verify write access
touch /data/.write-test && echo "OK" && rm /data/.write-test

# Check for NFS errors in syslog
grep -i "nfs\|mount" /var/log/messages | tail -30
```

After restoring the NFS mount, any in-progress upgrade will need to be resumed or retried via LCM. If the upgrade failed due to missing binaries, re-map the product binaries in **Lifecycle Operations → Settings → Binary Mapping** before retrying.

---

## Locker Certificate Import Fails

```bash
# Verify certificate chain validity before importing
openssl verify -CAfile chain.pem leaf.pem
# Expected: leaf.pem: OK

# Check that the private key matches the certificate
openssl x509 -noout -modulus -in leaf.pem | md5sum
openssl rsa -noout -modulus -in private.key | md5sum
# Both MD5 hashes must match

# Verify SANs in the certificate
openssl x509 -noout -text -in leaf.pem | grep -A5 "Subject Alternative Name"

# Confirm no passphrase on the private key (LCM requires unencrypted key)
openssl rsa -in private.key -check 2>&1 | head -1
# Must output: RSA key ok (not: Enter pass phrase)
```

---

## VIDM Authentication Failure After Password Change

If the VIDM admin password is changed externally, LCM loses its registration credentials.

```bash
# Verify VIDM health from LCM appliance
curl -sk https://vidm.example.local/SAAS/API/1.0/REST/system/health
# If health is UP but login fails, re-register VIDM:
```

Re-register VIDM: **LCM → Settings → Identity Manager → Edit → update credentials → Save**.

After re-registration, verify that all AD-backed users can still log into LCM via the VIDM login button.

---

## Product Shows Red Health in LCM Dashboard

1. Click the red product card — LCM shows the specific component or service that is unhealthy
2. SSH to the product appliance and check service status:

```bash
ssh admin@<product-fqdn>
vracli status
systemctl status <failing-service>
journalctl -u <failing-service> --since "1 hour ago" | tail -100
```

3. Common causes: disk full on the product appliance, internal service crash, or expired certificate
4. If the product health does not self-recover after the root cause is resolved: **LCM → Environments → product card → Run Health Check** to force a re-evaluation

---

## Checking Request History

All LCM operations are tracked as requests with full audit logs:

```bash
TOKEN=$(curl -sk -X POST "https://lcm-prod-01.example.local/lcm/authz/api/v2/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<password>"}' | jq -r '.token')

# List last 20 requests
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/lcmservice/api/v2/requests?size=20" | \
  jq -r '.[] | "\(.state)\t\(.requestType)\t\(.requestId)\t\(.startTime)"'

# Get detail of a failed request
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/lcmservice/api/v2/requests/<request-id>" | \
  jq '.tasks[] | {name: .taskName, state: .taskState, message: .message}'
```
