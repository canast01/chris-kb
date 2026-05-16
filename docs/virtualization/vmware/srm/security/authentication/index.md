# SRM — Authentication

---

## SRM Authentication via vCenter SSO

SRM authenticates all users through vCenter Single Sign-On. There are no SRM-local user accounts.

```powershell
# Authenticate to SRM through vCenter
Connect-VIServer -Server vcenter-protected.corp.local -User "administrator@vsphere.local" -Password "<password>"
$srm = Connect-SrmServer -SrmServerAddress srm-protected.corp.local
# SRM session is derived from the vCenter session — no separate SRM login
```

---

## Site Pairing Authentication (Certificate-Based)

SRM sites authenticate to each other using the SRM Server's SSL certificates. When pairing sites:

```
Site Recovery → New Site Pair
  Remote vCenter FQDN → enter
  Remote SRM Server FQDN → enter
  → vCenter presents remote SRM certificate thumbprint for acceptance
  Accept thumbprint → pairing established
```

The certificate thumbprint is permanently stored — if either site's certificate is replaced, the pairing must be re-established or the new thumbprint accepted.

### Re-establishing Pairing After Cert Rotation

```
Site Recovery → Site Pair → [pair] → Edit
  Update thumbprints if cert changed
  OR: delete and re-create site pair
```

---

## SRA Authentication to Storage Array

SRAs authenticate to storage arrays using credentials stored in SRM:

```
Site Recovery → Storage → Array Pairs → [pair] → Adapter Configuration
  FlashArray: management IP + API token (preferred over username/password)
  Other arrays: management IP + username/password
```

Credentials are encrypted at rest using SRM's internal encryption. Rotate on a schedule:
1. Create new credential on the array
2. Update in SRM adapter configuration
3. Delete old credential on array

---

## REST API Authentication

SRM REST API uses vCenter session tokens:

```bash
# Step 1: Get vCenter session token
TOKEN=$(curl -sk -X POST \
  "https://vcenter-protected.corp.local/rest/com/vmware/cis/session" \
  -u "administrator@vsphere.local:<password>" | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['value'])")

# Step 2: Use token for SRM API calls
curl -sk -H "vmware-api-session-id: $TOKEN" \
  "https://vcenter-protected.corp.local/api/vcenter/dr/recovery/plans"
```

---

## vSphere Replication Authentication

VRA appliances authenticate to each other and to vCenter using certificates. The VRA registers with vCenter using vCenter SSO credentials provided during initial configuration.

If vCenter certificate is replaced, re-register VRA:
```
VRA VAMI (https://vra-protected.corp.local:5480)
  Configuration → vCenter Server → Reconfigure
  Re-enter vCenter credentials
```

---

## Break-Glass Access to SRM

If vCenter SSO is unavailable, SRM cannot authenticate users. SRM is not operational without vCenter.

Recovery procedure: restore vCenter first, then SRM reconnects automatically. This is why vCenter must be included in DR plans — it is a dependency of SRM itself.
