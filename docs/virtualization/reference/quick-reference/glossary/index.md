# Virtualization Glossary

```
┌───────────────┬──────────────────────────────────────────────────────────┐
│   Term        │  Definition                                              │
├───────────────┼──────────────────────────────────────────────────────────┤
│ HA            │ High Availability — auto-restarts VMs after host failure │
│ DRS           │ Distributed Resource Scheduler — balances load           │
│ vMotion       │ Live migration of running VM between hosts               │
│ Storage vMotion│ Live migration of VM storage between datastores         │
│ vSAN          │ Hyper-converged storage using host-local disks           │
│ NSX           │ Network virtualisation platform (overlay + firewall)     │
│ VCF           │ VMware Cloud Foundation — full-stack SDDC                │
│ VMDK          │ Virtual machine disk file                                │
│ RDM           │ Raw Device Mapping — direct LUN to VM                    │
│ DFW           │ Distributed Firewall — per-VM stateful firewall in NSX   │
│ TEP           │ Tunnel Endpoint — NSX overlay encapsulation point        │
│ CPU Ready     │ Time VM waits for physical CPU scheduling (%)            │
│ Ballooning    │ Memory reclamation from VMs under host memory pressure   │
│ EVC           │ Enhanced vMotion Compat — masks CPU features in cluster  │
└───────────────┴──────────────────────────────────────────────────────────┘
```

## HA
High Availability. Automatically restarts VMs after host failure.

## DRS
Distributed Resource Scheduler. Balances workloads across hosts.

## vMotion
Moves a running VM between hosts.

## Storage vMotion
Moves VM storage between datastores.

## Snapshot
Point-in-time disk state used for backup or rollback.

## Datastore Latency
Time required to complete storage operations.

## CPU Ready
Time a VM waits for CPU scheduling.

## Ballooning
Memory reclamation mechanism used during memory pressure.

## Resync
Rebuild of storage components after failure or maintenance.

## Admission Control
Ensures enough capacity exists for failover.
