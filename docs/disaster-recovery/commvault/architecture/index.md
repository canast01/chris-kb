# CommVault Architecture

CommVault's Intelligent Data Services platform is built on three core components: the CommServe (management server and SQL Server database), MediaAgents (data movement engines that read from clients and write to storage), and Clients (systems running backup agents). The CommServe hosts the configuration database and orchestrates all jobs, making it the most critical component — its SQL database must be backed up daily. Deduplication is performed at the MediaAgent layer using a Deduplication Database (DDB) stored on an attached disk; DDB placement on SSD is strongly recommended for write performance. Hyperscale X appliances integrate CommServe, MediaAgent, and storage into a scale-out node cluster.

| Component | Role | Notes |
|---|---|---|
| CommServe | Management, scheduling, SQL DB | HA pair (passive standby) for critical environments |
| MediaAgent | Data movement, deduplication | Multiple; one DDB per storage pool |
| Client | Backup agent | Windows, Linux, VSA agent for VMware |
| Command Center | Web UI for administration | Replaces legacy Java GUI in recent FRs |
| Storage Policy | Job-to-storage mapping | Primary copy + secondary (offsite) copy |
