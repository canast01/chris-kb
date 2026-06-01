# Resource Optimization


<div class="kb-summary">
Identifying and right-sizing underutilised compute, storage, and cloud resources to reduce cost and improve efficiency.
</div>

## Identify Underutilised Resources

**Linux — CPU and memory:**
```bash
# List processes consuming > 1% CPU
ps aux --sort=-%cpu | awk 'NR>1 && $3>1 {print $1, $3"%", $4"%", $11}'

# Average CPU per server (last 30 days via sar)
sar -u -f /var/log/sa/sa$(date +%d) | awk '/Average/ {print $3}'

# Memory available
free -h | awk '/Mem/ {print "Available:", $7}'
```
┌───────────────────────────────── Performance — Resource Optimisation ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Optimisation: identify over-provisioned or idle resources and reduce waste          │   │
│   │       Right-size VMs using 30-day p95 CPU/RAM; reclaim unused storage and old snapshots       │   │
│   │    Test right-sizing in non-prod first; communicate with app owner before production change   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Identify Waste                │  │               Reclaim Actions               │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │           CPU < 10% avg: oversized           │  │              Reduce vCPU count              │   │
│   │          RAM < 20% used: oversized           │  │            Reduce vRAM allocation           │   │
│   │            Snapshots > 7 days old            │  │             Delete old snapshots            │   │
│   │          Powered-off VMs > 30 days           │  │           Decommission or archive           │   │
│   │            Unused datastores/LUNs            │  │            Reclaim after confirm            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Right-sizing = Match vCPU/vRAM to actual workload demand; reduces host overcommit ratio            │
│    vCPU ratio   = Total vCPUs assigned / physical cores; > 4:1 can cause CPU ready contention         │
│    Balloon      = VMware memory reclaim driver; active balloon means host is under memory pressure    │
│    Thin-prov    = Disk allocated lazily; reclaim by deleting data and running a reclaim task          │
│    Snapshot chain= Each snapshot added to chain; long chains slow reads; delete after use             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

## AWS — Cost Optimization

```bash
# Underutilised EC2 instances (Compute Optimizer)
aws compute-optimizer get-ec2-instance-recommendations \
  --query 'instanceRecommendations[?finding==`OVER_PROVISIONED`].{Instance:instanceArn,Current:currentInstanceType,Recommended:recommendationOptions[0].instanceType}'

# Unattached EBS volumes
aws ec2 describe-volumes \
  --filters Name=status,Values=available \
  --query 'Volumes[*].{ID:VolumeId,Size:Size,Type:VolumeType}' -o table

# Unused Elastic IPs
aws ec2 describe-addresses \
  --query 'Addresses[?AssociationId==null].{IP:PublicIp,AllocationId:AllocationId}' -o table
```

## Azure — Cost Optimization

```bash
# Unattached managed disks
az disk list \
  --query '[?diskState==`Unattached`].{Name:name,RG:resourceGroup,Size:diskSizeGb,SKU:sku.name}' -o table

# Azure Advisor cost recommendations
az advisor recommendation list \
  --category Cost \
  --query '[*].{Impact:impact,Resource:resourceMetadata.resourceId,Recommendation:shortDescription.solution}' -o table
```

## Storage Optimization

```bash
# ONTAP — volumes with > 50% free space
volume show -percent-used <50 -fields volume,size,used,percent-used

# Large files older than 90 days
find /data -type f -size +1G -mtime +90 -ls | sort -k7 -rn | head -20
```

## Optimization Actions Reference

| Finding | Action |
|---|---|
| VM CPU avg <10%, memory <30% | Downsize VM (1 or 2 tiers smaller) |
| Unattached EBS/disk | Delete after confirming not needed; snapshot first |
| Storage volume >50% free, static | Reduce allocation; reclaim to pool |
| Old cloud snapshots >90 days | Review retention; delete if beyond policy |
| Idle cloud instances (nights/weekends) | Schedule auto-stop for dev/test instances |
| Reserved instance opportunity (AWS/Azure) | Purchase 1-year RI/reservation for steady-state workloads |
