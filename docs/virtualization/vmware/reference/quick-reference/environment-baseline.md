---
tags:
  - reference
---
# Environment Baseline

<div class="kb-summary">
Environment Baseline reference covering Core Platform, Networking, Storage, Backup, Monitoring.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

core_platform: "Core Platform" {shape: rectangle}
networking: "Networking" {shape: rectangle}
storage: "Storage" {shape: rectangle}
backup: "Backup" {shape: rectangle}
monitoring: "Monitoring" {shape: rectangle}

core_platform -> networking: uses
networking -> storage: uses
storage -> backup: uses
backup -> monitoring: uses
```

## Core Platform

vCenter version  
ESXi version  
Cluster count  
Host count  
Datastore count  

## Networking

Management VLAN  
vMotion VLAN  
Storage VLAN  
NSX overlay network  

## Storage

Datastore type  
Capacity  
Redundancy  

## Backup

Backup system  
Backup frequency  
Restore test date  

## Monitoring

Monitoring system  
Alert destination  
Retention period
