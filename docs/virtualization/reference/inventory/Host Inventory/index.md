# Host Inventory

```
┌────────────────────────────────────── vSphere — Host Inventory ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Per-ESXi-host record for lifecycle, capacity, and support — updated after each LCM cycle   │   │
│   │        Fields: hostname, cluster, hardware model, CPU (sockets/cores), RAM, ESXi build        │   │
│   │      Network: NIC count, VDS uplinks, NIC model; Storage: HBA count, HBA model, iDRAC IP      │   │
│   │      State: lockdown mode, maintenance mode, vSAN participation, host profile compliance      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Hardware identity drives upgrade eligibility · ESXi build drives HCL compliance state              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Identity          │  │           Hardware          │  │            State            │   │
│   │       Hostname (FQDN)       │  │      Model (PowerEdge)      │  │          ESXi build         │   │
│   │        Cluster member       │  │      CPU sockets/cores      │  │        Lockdown mode        │   │
│   │       vCenter managed       │  │        RAM (GB total)       │  │         Maint. mode         │   │
│   │        iDRAC IP addr        │  │       NIC count/model       │  │         vSAN member         │   │
│   │          Site/rack          │  │       HBA count/model       │  │          Profile OK         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Hardware + state fields determine maintenance eligibility and capacity contribution                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Host       │      Model       │     CPU / RAM     │    ESXi build    │      State       │   │
│   │   esx-prod-01    │      R750xa      │    2x18c/1.5TB    │      8.0 U3      │      Active      │   │
│   │   esx-prod-02    │      R750xa      │    2x18c/1.5TB    │      8.0 U3      │      Active      │   │
│   │   esx-prod-03    │      R750xa      │    2x18c/1.5TB    │      8.0 U2      │   Needs patch    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Dell PowerEdge servers · iDRAC OOB · NIC/HBA PCIe cards · vSAN NVMe disks                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ESXi build    = Specific patch level (e.g. 8.0 U3 build 24022510); matches HCL entry               │
│    Lockdown mode = ESXi blocks direct SSH/shell; all management via vCenter API only                  │
│    Host profile  = vCenter config template enforcing NTP, syslog, lockdown, NIC teaming               │
│    HBA           = Host Bus Adapter; FC card connecting ESXi host to SAN fabric                       │
│    iDRAC         = Dell out-of-band management; independent of ESXi state for hardware ops            │
│    vSAN member   = Host contributing local NVMe/SSD disks to the vSAN datastore pool                  │
│    Maint. mode   = ESXi state where VMs are evacuated prior to host maintenance work                  │
│    HCL           = Hardware Compatibility List; ESXi build + model + driver must be listed            │
│    NIC teaming   = Multiple physical NICs bonded for redundancy and throughput on VDS                 │
│    Profile OK    = Host configuration matches host profile; non-compliant hosts flagged               │
│    Site/rack     = Physical location tag used for anti-affinity and failure domain config             │
│    CPU sockets   = Physical CPU count; drives vCPU overcommit capacity for the cluster                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
| Field | Example |
|---|---|
| Hostname | esx-prod-01 |
| Model | Dell PowerEdge R750 |
| Serial | ABC1234 |
| CPU | 2 sockets |
| Memory | 1024 GB |
| ESXi Version | 8.x |
| Firmware Bundle | Current approved baseline |
| Cluster | cl-prod-compute-01 |
| iDRAC | idrac-esx-prod-01 |
