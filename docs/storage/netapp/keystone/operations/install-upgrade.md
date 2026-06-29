---
tags:
  - netapp
  - operations
---
# NetApp Keystone — Install & Upgrade

<div class="kb-summary">
Install & Upgrade reference covering Keystone Collector Deployment, Upgrade Keystone Collector, Add a New ONTAP Array to Keystone, Remove an Array from Keystone, Post-Upgrade Validation.

*Applies to: Keystone STaaS*
</div>
![NetApp Keystone — Install & Upgrade](../../../../assets/storage-netapp-keystone-operations-install-upgrade.svg)

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Keystone Collector Deployment

The Keystone Collector is deployed as an OVA on vSphere. It collects usage data from ONTAP arrays and reports to the Keystone portal.

### Prerequisites

| Requirement | Specification |
|---|---|
| vSphere version | 6.7 U3+ or 7.x |
| vCPU | 4 |
| Memory | 12 GB |
| Disk | 200 GB |
| Network | HTTPS (443) outbound to NetApp cloud endpoints |
| ONTAP version | 9.8+ recommended |

### OVA Deployment Steps

1. Download the Keystone Collector OVA from the NetApp Support portal
2. Deploy OVA via vSphere Client → **File → Deploy OVF Template**
3. Assign a static IP on the management network
4. Power on and accept EULA at first boot
5. Run initial setup wizard:

```bash
# SSH into Collector VM (default credentials in deployment guide)
ssh admin@<collector-ip>

# Run initial setup
keystone-config setup

# Follow prompts:
# - Enter Keystone portal credentials
# - Add ONTAP array IPs and credentials
# - Configure proxy if required
# - Run validation
keystone-config validate
```


```text title="Expected output"
admin@collector-ip's password: 
Welcome to Keystone Configuration Tool v4.2.1
================================================================

Keystone Configuration Setup
================================================================

Enter Keystone portal username: admin@company.com
Enter Keystone portal password: 
Keystone credentials validated successfully.

Add ONTAP Array Configuration
================================================================
Enter ONTAP cluster IP [1.1.1.1]: 192.168.1.50
Enter ONTAP admin username: clusteradmin
Enter ONTAP admin password: 
ONTAP cluster 'prod-cluster-01' discovered successfully.
Add another ONTAP cluster? (y/n): n

Proxy Configuration
================================================================
Configure HTTP proxy? (y/n): n

Configuration saved to /etc/keystone/config.yaml
Running validation...

Validation Results
================================================================
✓ Keystone portal connectivity: PASSED
✓ ONTAP cluster connectivity: PASSED (prod-cluster-01)
✓ Network latency: PASSED (avg 12ms)
✓ DNS resolution: PASSED
✓ NTP synchronization: PASSED

Setup completed successfully. Collector ID: KS-COLL-7f4a9c2e
```

!!! warning "Common errors"
    **`ssh: Could not resolve hostname <collector-ip>: Name or service not known`** — Replace `<collector-ip>` with the actual collector VM IP address from your deployment documentation.
    **`Authentication failed, permission denied (publickey,password).`** — Verify the default credentials match your deployment guide and that the admin user exists on the collector VM.
    **`Error: Failed to connect to ONTAP cluster at 192.168.1.50: Connection timed out`** — Confirm the ONTAP cluster IP is correct, reachable from the collector VM, and that firewall rules allow port 443 traffic.
## Upgrade Keystone Collector

```bash
# Check current version
keystone-collector version

# Check for available update
keystone-collector upgrade --check

# Apply upgrade (downloads and installs new version)
keystone-collector upgrade --apply

# Verify after upgrade
keystone-collector version
keystone-collector status
```


```text title="Expected output"
Keystone Collector Version 24.2.1 (Build 8847)
Release Date: 2024-01-15

Available upgrade: 24.3.0 (Build 8921)
Current version: 24.2.1
Upgrade size: 287 MB
Estimated time: 3-5 minutes

Downloading upgrade package... [████████████████████] 100%
Verifying package integrity... OK
Installing upgrade... [████████████████████] 100%
Upgrade completed successfully
Service restarted: keystone-collector

Keystone Collector Version 24.3.0 (Build 8921)
Release Date: 2024-02-10

Status: Running
Uptime: 2 minutes 14 seconds
Last collection: 2024-02-15 14:32:18 UTC
Collection interval: 1 hour
License status: Valid (expires 2025-06-30)
```

!!! warning "Common errors"
    **`Error: Unable to connect to update server (Connection timeout)`** — Verify network connectivity and firewall rules allow outbound HTTPS to the Keystone update repository.
    **`Error: Insufficient disk space. Required: 500 MB, Available: 120 MB`** — Free up disk space on the collector host before attempting the upgrade.
    **`Error: Service restart failed. Manual restart required`** — Run `systemctl restart keystone-collector` to manually restart the service after upgrade completion.
## Add a New ONTAP Array to Keystone

```bash
# On Collector VM
keystone-config add-array \
    --host <ontap-mgmt-ip> \
    --username admin \
    --password <pass> \
    --type ontap

# Validate the new array is reachable
keystone-config validate

# Force immediate collection to confirm data flows
keystone-collector collect --force

# Verify in portal — array should appear within 15 minutes
```


```text title="Expected output"
Adding ONTAP array configuration...
Array added successfully: ontap-cluster-01 (192.168.1.50)
Configuration saved to /etc/keystone/arrays.conf

Validating array connectivity...
✓ ontap-cluster-01: Connection successful (ONTAP 9.12.1)
✓ API credentials verified
✓ Capacity data accessible
Validation complete: 1/1 arrays reachable

Starting forced collection cycle...
[2024-01-15 14:32:18] Connecting to ontap-cluster-01 (192.168.1.50)
[2024-01-15 14:32:22] Retrieving capacity metrics
[2024-01-15 14:32:25] Retrieving performance data
[2024-01-15 14:32:31] Uploading to Keystone portal (uuid: a7f2c9e1-4b8d-11ee-9c2a-0242ac120002)
Collection cycle completed successfully
Data transmitted: 2.3 MB | Next scheduled collection: 2024-01-15 15:32:18
```

!!! warning "Common errors"
    **`Error: Connection refused to 192.168.1.50:443`** — Verify the ONTAP management IP is correct and the cluster API is accessible from the Collector VM (check firewall rules and network connectivity).
    **`Error: Authentication failed for user 'admin'`** — Confirm the password is correct and the admin user has API access permissions enabled on the ONTAP cluster.
    **`Error: Failed to upload metrics — HTTP 401 Unauthorized`** — Verify the Collector VM's Keystone registration credentials are valid by running `keystone-config show-registration`.
## Remove an Array from Keystone

```bash
keystone-config remove-array --host <ontap-mgmt-ip>
keystone-config validate
```


```text title="Expected output"
Removing array configuration for host 192.168.1.42...
Array 'netapp-prod-01' successfully removed from Keystone configuration.
Disconnecting management session...

Validating Keystone configuration...
Configuration validation: PASSED
  - Management connectivity: OK
  - License status: Active
  - Subscription ID: KS-2024-789456
  - Next renewal: 2025-03-15
All checks completed successfully.
```

!!! warning "Common errors"
    **`Error: Unable to connect to host 192.168.1.42 on port 443`** — Verify the ONTAP management IP is reachable and the Keystone service is running with `ping <ontap-mgmt-ip>` and `ssh admin@<ontap-mgmt-ip>`.
    **`Error: Array 'netapp-prod-01' is still in use by active subscriptions`** — Remove or migrate all active subscriptions associated with the array before removing it using `keystone-config list-subscriptions --array netapp-prod-01`.
    **`Validation failed: Missing required license file`** — Reinstall the Keystone license bundle on the ONTAP cluster using `keystone-config install-license --host <ontap-mgmt-ip> --license-file <path>`.
## Post-Upgrade Validation

```bash
# Confirm status is healthy
keystone-collector status

# Confirm last collection succeeded
keystone-collector show-last-collection

# Check logs for errors
journalctl -u keystone-collector --since "30 min ago" | grep -i error
```


```text title="Expected output"
keystone-collector status
Status: HEALTHY
Version: 24.1.2
Last heartbeat: 2024-01-15T14:32:18Z
Collection interval: 1h
API connectivity: OK

keystone-collector show-last-collection
Collection ID: ks-coll-20240115-143200-a7f2e9c1
Timestamp: 2024-01-15T14:32:00Z
Duration: 45s
Records collected: 2847
Status: SUCCESS
Next collection: 2024-01-15T15:32:00Z

journalctl -u keystone-collector --since "30 min ago" | grep -i error
(no output — no errors in logs)
```

!!! warning "Common errors"
    **`Unit keystone-collector.service not found.`** — Verify the keystone-collector service is installed and enabled with `systemctl list-unit-files | grep keystone`.
    **`Failed to connect to Keystone API: Connection refused`** — Check that the Keystone API endpoint is reachable and the collector configuration has the correct hostname/IP with `cat /etc/keystone-collector/config.yaml`.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Keystone — Procedures](../procedures/)
- [Keystone — Health Checks](../health-checks/)
