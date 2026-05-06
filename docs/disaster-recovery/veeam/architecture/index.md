# Veeam Architecture

Veeam Backup & Replication (VBR) is built around four core components: the Veeam Backup Server (management, job orchestration, and configuration database), Backup Proxies (data movers that read VM data via VADP or agent), Backup Repositories (target storage for backup files), and the optional Scale-Out Backup Repository (SOBR) which presents a logical pool across multiple repositories with automatic offload to an object-storage capacity tier. WAN Accelerators are deployed in pairs (source and target) to deduplicate replication traffic across slow links. Veeam supports VMware vSphere, Microsoft Hyper-V, physical Windows and Linux agents, NAS shares via File Share backup jobs, and cloud workloads on AWS, Azure, and GCP.

| Component | Role | Notes |
|---|---|---|
| Backup Server | Management, scheduler, config DB | Windows Server; SQL Express or full SQL |
| Backup Proxy | Data mover (VADP / agent) | One or more; scale for throughput |
| Backup Repository | Backup file storage | Linux / Windows / NAS / object store |
| SOBR | Logical storage pool | Performance + capacity tier |
| WAN Accelerator | Remote replication dedup | Deployed in source/target pairs |
| Veeam ONE | Monitoring and reporting | Separate server; integrates with VBR |
