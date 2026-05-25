# Environment Baseline

```text
┌─────────────────────────────────────────────────────────────────────────┐
│               Environment Baseline — Normal Thresholds                  │
├──────────────────┬──────────────────────────────────────────────────────┤
│  Platform        │  vCenter ver ___  │  ESXi ver ___  │  Clusters ___   │
├──────────────────┼──────────────────────────────────────────────────────┤
│  CPU             │  Avg host util < 70%  │  CPU Ready < 5%              │
│  Memory          │  Balloon = 0          │  Swap = 0  │  < 80% consumed │
│  Storage (VMFS)  │  DAVG < 5ms           │  GAVG < 20ms                 │
│  Storage (vSAN)  │  DAVG < 2ms           │  GAVG < 10ms                 │
│  Network         │  0 packet drops       │  All uplinks active          │
│  vSAN            │  Resync = 0 (normal)  │  All objects Healthy         │
├──────────────────┼──────────────────────────────────────────────────────┤
│  Backup          │  Tool: ___  │  Freq: ___  │  Last restore: ___       │
│  Monitoring      │  System: ___  │  Alerts to: ___  │  Retention: ___   │
└──────────────────┴──────────────────────────────────────────────────────┘
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
