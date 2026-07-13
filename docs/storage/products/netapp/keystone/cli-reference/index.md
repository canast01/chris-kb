---
tags:
  - netapp
---
# NetApp Keystone — CLI Reference

```bash
# Exchange client credentials for a bearer token
TOKEN=$(curl -s -X POST "https://netapp-cloud-account.auth0.com/oauth/token" \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "client_credentials",
    "client_id": "<YOUR_CLIENT_ID>",
    "client_secret": "<YOUR_CLIENT_SECRET>",
    "audience": "https://api.activeiq.netapp.com"
  }' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "Token acquired"
```


```text title="Expected output"
Token acquired
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (6) Could not resolve host: netapp-cloud-account.auth0.com` | Verify network connectivity and DNS resolution; check if your firewall allows outbound HTTPS to auth0.com. |
    | `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` | Verify your client_id and client_secret are correct; check the curl response by removing the python3 pipe temporarily to see the actual error message from Auth0. |
    | `curl: (60) SSL certificate problem: unable to get local issuer certificate` | Update your CA certificate bundle or add `-k` flag to curl (not recommended for production); ensure your system's certificate store is current. |
```bash
# List service levels (tiers) available under a subscription
curl -s "https://api.activeiq.netapp.com/v1/keystone/subscriptions/${SUBSCRIPTION_ID}/service-levels" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

```text title="Expected output"
{
  "service_levels": [
    {
      "id": "sl-premium-001",
      "name": "Premium",
      "description": "High-performance tier with guaranteed IOPS",
      "storage_type": "SSD",
      "committed_capacity_gb": 10240,
      "burst_capacity_gb": 2048
    },
    {
      "id": "sl-standard-001",
      "name": "Standard",
      "description": "General-purpose tier with balanced performance",
      "storage_type": "SAS",
      "committed_capacity_gb": 51200,
      "burst_capacity_gb": 10240
    },
    {
      "id": "sl-economy-001",
      "name": "Economy",
      "description": "Cost-optimized tier for archival workloads",
      "storage_type": "SATA",
      "committed_capacity_gb": 102400,
      "burst_capacity_gb": 20480
    }
  ],
  "subscription_id": "sub-a7f2c9e1-4b6d-11ed-bdc3-0242ac120002",
  "total_count": 3
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (6) Could not resolve host: api.activeiq.netapp.com` | Verify network connectivity and DNS resolution; check if your firewall allows HTTPS outbound traffic to the ActiveIQ API endpoint. |
    | `{"error": "Unauthorized", "message": "Invalid or expired token"}` | Regenerate your Bearer token using the ActiveIQ authentication endpoint and ensure `$TOKEN` is set correctly. |
    | `curl: (7) Failed to connect to api.activeiq.netapp.com port 443: Connection refused` | Confirm the API endpoint URL is correct and that ActiveIQ services are operational; check your organization's proxy settings if applicable. |
```bash
# Check if any tier is in burst (consumed > committed)
curl -s "https://api.activeiq.netapp.com/v1/keystone/subscriptions/${SUBSCRIPTION_ID}/usage" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
data = json.load(sys.stdin)
alert = False
for tier in data.get('usageDetails', []):
    committed = float(tier.get('committedCapacity', 0))
    consumed  = float(tier.get('consumedCapacity',  0))
    pct = (consumed / committed * 100) if committed > 0 else 0
    status = 'BURST' if consumed > committed else ('WARN' if pct >= 90 else 'OK')
    print(f\"{status}  {tier['serviceLevel']:20s}  {pct:5.1f}%  ({consumed:.1f} / {committed:.1f} TiB)\")
    if status != 'OK':
        alert = True
sys.exit(1 if alert else 0)
"
```

```text title="Expected output"
OK       Standard                 45.2%  (22.6 / 50.0 TiB)
OK       Premium                  78.5%  (157.0 / 200.0 TiB)
WARN     Premium-Plus             91.3%  (219.1 / 240.0 TiB)
BURST    Extreme                  105.7%  (127.0 / 120.0 TiB)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (6) Could not resolve host: api.activeiq.netapp.com` | Verify network connectivity and DNS resolution; check if a proxy or firewall is blocking access to the ActiveIQ API endpoint. |
    | `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` | Confirm that `$TOKEN` is valid and not expired by regenerating it in the ActiveIQ portal, then retry the request. |
    | `KeyError: 'usageDetails'` | Verify that `$SUBSCRIPTION_ID` is correct and that the subscription has active usage data; check subscription status in ActiveIQ console. |
```bash
# All volumes: size, used, available
volume show -fields size,used,available,percent-used

# Sort by percent-used (highest first)
volume show -fields size,used,percent-used | sort -k4 -rn

# Aggregate-level capacity
storage aggregate show -fields size,used,available,percent-used

# SVM-level logical space view
vserver show -fields name -type data
volume show -vserver <svm_name> -fields size,used,logical-used,available

# QoS workload to correlate per-volume performance with Keystone tier
qos workload show -fields workload-name,volume,policy-group

# Check volume space guarantee (impacts Keystone committed capacity)
volume show -fields space-guarantee,size,used
```

```text title="Expected output"
Vserver   Volume       Size       Used       Available  Percent-Used
--------- ------------ ---------- ---------- ---------- ------------
svm-prod  vol_data_01  500GB      385GB      115GB      77%
svm-prod  vol_data_02  1TB        650GB      350GB      65%
svm-prod  vol_logs     200GB      180GB      20GB       90%
svm-dev   vol_test_01  250GB      45GB       205GB      18%
svm-dev   vol_backup   2TB        1.2TB      800GB      60%

Vserver   Volume       Size       Percent-Used
--------- ------------ ---------- -----------
svm-prod  vol_logs     200GB      90%
svm-prod  vol_data_01  500GB      77%
svm-prod  vol_data_02  1TB        65%
svm-dev   vol_backup   2TB        60%
svm-dev   vol_test_01  250GB      18%

Aggregate         Size       Used       Available  Percent-Used
----------------- ---------- ---------- ---------- -----------
aggr_ssd_01       10TB       7.8TB      2.2TB      78%
aggr_ssd_02       8TB        5.2TB      2.8TB      65%
aggr_sas_01       20TB       14.5TB     5.5TB      72%

Vserver Name
------------ 
svm-prod
svm-dev
svm-keystone

Vserver   Volume       Size       Used       Logical-Used Available
--------- ------------ ---------- ---------- ------------ ----------
svm-prod  vol_data_01  500GB      385GB      392GB        115GB
svm-prod  vol_data_02  1TB        650GB      668GB        350GB

Workload-Name              Volume       Policy-Group
-------------------------- ------------ ----------------
prod_oltp_tier1            vol_data_01  gold-tier
prod_analytics_tier2       vol_data_02  silver-tier
dev_batch_tier3            vol_test_01  bronze-tier

Volume       Space-Guarantee  Size       Used
------------ ---------------- ---------- ----------
vol_data_01  volume           500GB      385GB
vol_data_02  none             1TB        650GB
vol_logs     file             200GB      180GB
vol_backup   volume           2TB        1.2TB
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: command not found: volume show` | Ensure you are logged into the NetApp cluster management interface (SSH to cluster IP) and not a local shell. |
    | `Error: access denied for command "volume show"` | Verify your RBAC role includes the "volume" command capability; contact your cluster administrator to grant necessary permissions. |
```bash
# Volumes with thick guarantee (count against committed immediately)
volume show -space-guarantee volume -fields size,used,space-guarantee

# Volumes with thin/none guarantee (count against committed as written)
volume show -space-guarantee none -fields size,used,space-guarantee
```

```text title="Expected output"
Vserver   Volume       Size       Used       Space Guarantee
--------- ------------ ---------- ---------- -----------------
svm-prod  vol_data_01  1.0TB      487.2GB    volume
svm-prod  vol_data_02  2.0TB      1.2TB      volume
svm-prod  vol_backup   500GB      125.3GB    volume
svm-dev   vol_test_01  250GB      89.5GB     volume

Vserver   Volume       Size       Used       Space Guarantee
--------- ------------ ---------- ---------- -----------------
svm-prod  vol_thin_01  5.0TB      2.1TB      none
svm-prod  vol_thin_02  3.0TB      1.8TB      none
svm-dev   vol_thin_03  1.5TB      340GB      none
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: command not found: volume` | Ensure you are connected to the NetApp cluster via SSH or the ONTAP CLI, not a standard Linux shell. |
    | `Error: invalid field name "space-guarantee"` | Verify your ONTAP version supports the space-guarantee field; use `volume show -fields ?` to list available fields. |
```bash
BLUEXP_TOKEN="<bluexp_bearer_token>"

# List Digital Wallet assets
curl -s "https://api.bluexp.netapp.com/marketplace/api/v1/subscriptions" \
  -H "Authorization: Bearer $BLUEXP_TOKEN" | python3 -m json.tool

# Check capacity pool status
curl -s "https://api.bluexp.netapp.com/marketplace/api/v1/capacity-pools" \
  -H "Authorization: Bearer $BLUEXP_TOKEN" | python3 -m json.tool
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```

## See also

- [NetApp Keystone — Overview](../../)
