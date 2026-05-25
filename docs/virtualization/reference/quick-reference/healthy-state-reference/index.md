# Healthy State Reference

```text
┌───────────────────────────────────────────────────────────────────────┐
│                  Green Indicators by Component                        │
├─────────────────┬─────────────────────────────────────────────────────┤
│  Component      │  Healthy State Indicators                           │
├─────────────────┼─────────────────────────────────────────────────────┤
│ vCenter         │ Login OK │ All services running │ No cert warnings  │
│ ESXi Hosts      │ All Connected │ None in unexpected maintenance      │
│ Clusters        │ HA=On │ DRS=Automated │ No HA errors on any host    │
│ vSAN            │ Skyline Health all green │ 0 degraded objects        │
│                 │ No active resync (outside maint) │ Disk groups Up   │
│ NSX             │ MP=STABLE │ Edge nodes Up │ BGP=Established          │
│ Datastores      │ All mounted │ APD=0 │ PDL=0 │ < 75% used            │
│ VMs             │ No consolidation warnings │ Tools running+current   │
│                 │ CPU Ready < 5% │ Balloon = 0 │ No swap              │
│ Backups         │ Last job: success │ No missed jobs in 24h           │
│ Monitoring      │ Aria Ops collection=OK │ No critical alerts active  │
└─────────────────┴─────────────────────────────────────────────────────┘
```

## Cluster

All hosts connected  
No alarms  
Capacity healthy  

## Storage

Latency < 10 ms  
No failed paths  
No resync backlog  

## Network

No packet loss  
All uplinks up  

## VMs

No consolidation warnings  
No swap  
CPU ready low  

## Management

vCenter reachable  
Services running  
Backups successful
