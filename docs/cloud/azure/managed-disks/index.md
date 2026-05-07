# Managed Disks

Azure Managed Disks — block storage for Azure VMs, snapshots, and disk performance management.

## Disk Types

| Type | Use Case | Max IOPS | Max Throughput |
|---|---|---|---|
| Ultra Disk | Latency-sensitive databases | 400,000 | 10,000 MB/s |
| Premium SSD v2 | Business-critical apps, flexible perf | 80,000 | 1,200 MB/s |
| Premium SSD (P-series) | Production VMs, SQL Server | 20,000 | 900 MB/s |
| Standard SSD | Dev/test, lightly used apps | 6,000 | 750 MB/s |
| Standard HDD | Archival, infrequent access | 2,000 | 500 MB/s |

## Common Azure CLI Commands

```bash
# List managed disks
az disk list \
  --query '[*].{Name:name,RG:resourceGroup,Type:sku.name,Size:diskSizeGb,State:diskState}' -o table

# Show disk details
az disk show -g <rg> -n <disk-name>

# Create a managed disk from snapshot
az disk create -g <rg> -n <new-disk-name> \
  --source <snapshot-resource-id> \
  --sku Premium_LRS

# Create a snapshot
az snapshot create -g <rg> -n <snap-name> \
  --source <disk-resource-id>

# List snapshots
az snapshot list -g <rg> \
  --query '[*].{Name:name,Disk:creationData.sourceResourceId,Size:diskSizeGb,State:diskState}' -o table

# Resize a disk (VM must be deallocated or disk must be detached for OS disk)
az disk update -g <rg> -n <disk-name> --size-gb 512

# Change disk performance tier
az disk update -g <rg> -n <disk-name> --sku Premium_LRS --disk-iops-read-write 5000 --disk-mbps-read-write 200
```

## Attach / Detach Disks

```bash
# Attach an existing managed disk to a VM
az vm disk attach -g <rg> --vm-name <vm-name> \
  --name <disk-name> --caching ReadOnly

# Detach a disk
az vm disk detach -g <rg> --vm-name <vm-name> --name <disk-name>
```

## Expand OS Disk (Linux VM)

```bash
# 1. Deallocate VM
az vm deallocate -g <rg> -n <vm-name>

# 2. Resize OS disk
az disk update -g <rg> -n <os-disk-name> --size-gb 256

# 3. Start VM
az vm start -g <rg> -n <vm-name>

# 4. On the VM: extend the partition and filesystem
sudo growpart /dev/sda 1
sudo resize2fs /dev/sda1     # ext4
sudo xfs_growfs /             # xfs
```

## Disk Encryption

```bash
# Enable encryption using Azure Disk Encryption (ADE) with Key Vault
az vm encryption enable -g <rg> -n <vm-name> \
  --disk-encryption-keyvault <keyvault-resource-id> \
  --volume-type All

# Check encryption status
az vm encryption show -g <rg> -n <vm-name> \
  --query '{OS:osDisk.encryptionSettings,DataDisks:dataDiskEncryptionSettings}'
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Disk not visible in VM | Disk attached / initialised | Check disk is attached; on Linux run `lsblk`; initialise and mount |
| High latency | Disk type and burst credit | Switch to Premium SSD or Ultra; check if disk is throttling |
| Can't resize OS disk | VM deallocated? | Deallocate VM first; OS disk can't be resized while running |
| Snapshot quota hit | Snapshot count limit | Delete old snapshots; request quota increase |
