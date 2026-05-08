# Aria Suite Lifecycle — Common Issues

## Installation and Deployment Failures

```bash
# Check LCM installer log for root cause
tail -200 /var/log/vmware/vrlcm/lcm-install.log

# Verify DNS resolution for all product FQDNs from LCM node
for fqdn in vrops.corp.local vra.corp.local vidm.corp.local vrli.corp.local; do
  echo -n "$fqdn → "; nslookup "$fqdn" | grep "Address" | tail -1
done

# Verify reverse DNS (PTR) for each product IP
for ip in 10.0.1.10 10.0.1.11 10.0.1.20 10.0.1.30; do
  echo -n "$ip → "; nslookup "$ip" | grep "name ="
done

# Check NTP — certificate operations fail with drift > 5 seconds
chronyc tracking | grep "System time"

# Disk space — /data needs at least 50 GB free per product version
df -h /data /var/log /tmp
```

| Error Code | Meaning | Resolution |
|---|---|---|
| `VRLCM_ERR_001` | DNS resolution failure | Fix A/PTR records; verify from LCM node with `nslookup` |
| `VRLCM_ERR_012` | Insufficient disk space on `/data` | Free space or expand NFS share; minimum 50 GB free per product |
| `VRLCM_ERR_023` | OVA/PAK checksum mismatch | Re-download bundle; verify SHA256 against Broadcom portal |
| `VRLCM_ERR_031` | vCenter connectivity failure | Check credentials, firewall port 443, and vCenter certificate trust |
| `VRLCM_ERR_045` | NTP time drift too large | Fix NTP source on LCM or product appliance; restart `chronyd` |
| `VRLCM_ERR_057` | VIDM registration failed | Verify VIDM FQDN, credentials, and TLS certificate trust |

---

## Upgrade Gets Stuck or Times Out

Symptoms: upgrade request stays in `RUNNING` state for more than 2 hours; no progress on the workflow screen.

```bash
# Check if product appliance VMs are powered on and responsive
ping <product-fqdn>
ssh admin@<product-fqdn> "vracli status"

# Check LCM application log for timeout or error
grep -i "timeout\|error\|exception" /var/log/vmware/vrlcm/lcm-app.log | tail -100

# Check if the upgrade agent on the product appliance is running
ssh root@<product-fqdn> "systemctl status vra-appliance-agent"
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
curl -sk https://vidm.corp.local/SAAS/API/1.0/REST/system/health
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
TOKEN=$(curl -sk -X POST "https://lcm-prod-01.corp.local/lcm/authz/api/v2/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<password>"}' | jq -r '.token')

# List last 20 requests
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.corp.local/lcm/lcmservice/api/v2/requests?size=20" | \
  jq -r '.[] | "\(.state)\t\(.requestType)\t\(.requestId)\t\(.startTime)"'

# Get detail of a failed request
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.corp.local/lcm/lcmservice/api/v2/requests/<request-id>" | \
  jq '.tasks[] | {name: .taskName, state: .taskState, message: .message}'
```
