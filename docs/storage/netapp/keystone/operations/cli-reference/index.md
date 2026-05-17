# NetApp Keystone — CLI Reference

## Keystone Collector CLI

The Keystone Collector is managed via SSH and a dedicated CLI on the collector VM.

```bash
# Show Collector status and version
keystone-collector status
keystone-collector version

# Validate configuration
keystone-config validate

# Force data collection (triggers immediate usage push to Keystone portal)
keystone-collector collect --force

# Show last collection result
keystone-collector show-last-collection

# List managed arrays
keystone-collector list-arrays

# Update Collector software
keystone-collector upgrade --check     # dry-run
keystone-collector upgrade --apply
```

## ONTAP CLI — Keystone Volumes

Keystone storage runs on ONTAP SVMs. Use ONTAP CLI to inspect and manage underlying volumes.

```bash
# List Keystone SVM volumes
volume show -vserver <keystone-svm>

# Volume capacity detail
volume show -vserver <keystone-svm> -fields size,used,available,percent-used

# List snapshot schedules
snapshot policy show

# Show protection group status (for SnapMirror-backed tiers)
snapmirror show -vserver <keystone-svm>

# Check aggregate capacity supporting Keystone volumes
aggr show -fields size,used-percent

# Show qtree details (Keystone NFS shares map to qtrees)
qtree show -vserver <keystone-svm>
```

## NetApp ONTAP REST API (Keystone Collector Bootstrap)

```bash
# Test API connectivity from Collector VM to ONTAP
curl -s -u admin:<password> \
    "https://<ontap-mgmt-ip>/api/cluster" | jq '.name, .version.full'

# List SVMs via REST
curl -s -u admin:<password> \
    "https://<ontap-mgmt-ip>/api/svm/svms" | jq '.records[].name'

# Volume list via REST
curl -s -u admin:<password> \
    "https://<ontap-mgmt-ip>/api/storage/volumes?svm.name=<keystone-svm>" | \
    jq '.records[] | "\(.name) \(.space.used) / \(.space.size)"'
```

## Keystone Portal API

NetApp exposes Keystone subscription data via API for reporting and integration.

```python
import requests

PORTAL = "https://keystone.netapp.com/api/v1"
TOKEN  = "<keystone-api-token>"
HDR    = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Get subscription details
resp = requests.get(f"{PORTAL}/subscriptions", headers=HDR)
for sub in resp.json().get("subscriptions", []):
    print(f"{sub['subscriptionNumber']}  committed={sub['committedCapacity']} consumed={sub['consumedCapacity']}")
```

## Quick Reference

| Task | Command |
|---|---|
| Check Collector status | `keystone-collector status` |
| Force usage collection | `keystone-collector collect --force` |
| List managed arrays | `keystone-collector list-arrays` |
| Validate config | `keystone-config validate` |
| ONTAP volume list | `volume show -vserver <svm>` |
| ONTAP SnapMirror status | `snapmirror show` |
| Test ONTAP API | `curl -u admin:pass https://<ip>/api/cluster` |
