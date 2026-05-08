# Veeam — Components

## Core Components

| Component | Role | Notes |
|---|---|---|
| Backup Server | Management, scheduler, config DB | Windows Server; SQL Express (≤500 VMs) or full SQL Server |
| Backup Proxy | Data mover (reads VM data via VADP or agent) | One or more per site; scale for throughput |
| Backup Repository | Target storage for backup files (.vbk/.vib) | Linux / Windows / NAS / hardened Linux |
| Scale-Out Backup Repository (SOBR) | Logical pool across multiple repos | Performance tier (fast disk) + capacity tier (object storage) |
| WAN Accelerator | Remote replication deduplication | Deployed in source/target pairs — only for VM replication jobs |
| Veeam ONE | Monitoring, alerting, reporting | Separate server; integrates with VBR via DB |

## Cloud and Agent Support

| Platform | Method |
|---|---|
| VMware vSphere | VADP, agentless |
| Microsoft Hyper-V | HV provider, agentless |
| Physical Windows | Veeam Agent for Windows (VAW) |
| Physical Linux | Veeam Agent for Linux (VAL) |
| AWS EC2 | Veeam Backup for AWS (separate appliance) |
| Azure VMs | Veeam Backup for Azure (separate appliance) |
