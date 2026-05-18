# Resource Optimization

Identifying and right-sizing underutilised compute, storage, and cloud resources to reduce cost and improve efficiency.

```
┌─────────────────────────────────┐   ┌──────────────┐   ┌─────────────┐   ┌──────────────┐
│     Utilisation Metrics         │   │ Rightsizing  │   │   Reclaim   │   │ Cost Saving  │
│                                 │   │              │   │             │   │              │
│ CPU avg / Mem avg / Disk free   │──►│ Downsize VM  │──►│ Delete      │──►│ RI purchase  │
│ Unattached EBS/disks            │   │ Reduce alloc │   │ orphans     │   │ Schedule     │
│ Idle cloud instances            │   │ Archive data │   │ Reclaim vol │   │ auto-stop    │
└─────────────────────────────────┘   └──────────────┘   └─────────────┘   └──────────────┘
         │                                   │
         │   ┌───────────────────────────────┘
         ▼   ▼
┌──────────────────┐
│  Finding Sources │
│ AWS Compute Opt  │
│ Azure Advisor    │
│ ONTAP vol report │
│ VMware vROps     │
└──────────────────┘
```

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

**VMware — VM rightsizing:**
```powershell
# VMs with low memory usage
Get-VM | Get-Stat -Stat mem.usage.average -MaxSamples 48 |
  Group-Object Entity |
  Select-Object Name, @{N='AvgMem%';E={($_.Group.Value | Measure-Object -Average).Average}} |
  Where-Object 'AvgMem%' -lt 20
```

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
