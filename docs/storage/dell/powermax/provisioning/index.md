# Provisioning

End-to-end workflow for provisioning storage on Dell PowerMax: create volumes, add to a storage group, and create (or update) a masking view so the host can see the storage.

## Prerequisites

Before provisioning, confirm:
- Host HBA WWNs are logged into the fabric and registered with the array
- An appropriate Storage Resource Pool (SRP) and service level exist
- Zoning is in place (if Fibre Channel)

## Step 1 — Create or Identify the Storage Group

```bash
# Check if a suitable SG already exists
symsg list -sid <sid> | grep <hostname>

# Create a new storage group with SRP and service level
symsg create <hostname>_SG -sid <sid> -srp SRP_1 -slo Diamond
```

## Step 2 — Create Thin Devices

```bash
# Create 5 x 100 GB TDEV devices and add directly to the SG
symconfigure -sid <sid> -cmd \
    "create dev count=5, size=100GB, emulation=FBA, config=TDEV, sg=<hostname>_SG;" \
    commit -noprompt

# Verify devices were created and added
symsg show <hostname>_SG -sid <sid>
```

## Step 3 — Create the Initiator Group

```bash
# Create initiator group for the host
symaccess create -sid <sid> -name <hostname>_IG -type initiator

# Add host HBA WWNs (one per port)
symaccess -sid <sid> -name <hostname>_IG -type initiator add -wwn <wwn_port_a>
symaccess -sid <sid> -name <hostname>_IG -type initiator add -wwn <wwn_port_b>
```

## Step 4 — Create or Identify the Port Group

```bash
# List existing port groups
symaccess list -sid <sid> -type port

# Create a new port group (or reuse an existing one for the fabric)
symaccess create -sid <sid> -name <fabric>_PG -type port
symaccess -sid <sid> -name <fabric>_PG -type port add -dirport 01E:4
symaccess -sid <sid> -name <fabric>_PG -type port add -dirport 02E:4
```

## Step 5 — Create the Masking View

```bash
# Create masking view linking SG + IG + PG
symaccess create view -sid <sid> -name <hostname>_MV \
    -sg <hostname>_SG \
    -ig <hostname>_IG \
    -pg <fabric>_PG

# Verify masking view
symaccess show view <hostname>_MV -sid <sid>
```

## Step 6 — Host-Side Validation

```bash
# On Linux — rescan for new devices
rescan-scsi-bus.sh
echo "- - -" > /sys/class/scsi_host/host*/scan
multipath -ll

# On Windows — rescan via PowerShell
Update-HostStorageCache
Get-Disk | Where-Object OperationalStatus -eq "Offline"
```

## Adding More Devices to an Existing Host

```bash
# Create additional devices in existing SG
symconfigure -sid <sid> -cmd \
    "create dev count=2, size=500GB, emulation=FBA, config=TDEV, sg=<hostname>_SG;" \
    commit -noprompt

# No masking view change needed — new devices in existing SG are automatically visible
```

## Capacity Checks Before Provisioning

```bash
# SRP free capacity
symcfg -sid <sid> list -srp

# Thin pool subscription
symcfg -sid <sid> show -pool -thin -demand
# Warning: do not exceed 85% subscribed on the SRP
```
