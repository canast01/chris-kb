# NetBackup Architecture

NetBackup uses a three-tier architecture: the Master Server handles policy management, scheduling, catalog maintenance, and job orchestration; Media Servers perform the actual data movement between clients and storage units; and Clients run the backup agents that stream data to media servers. Storage units include BasicDisk, AdvancedDisk, Cloud (S3-compatible), tape libraries via NDMP or SAN, and Dell Data Domain via OpenStorage Technology (OST) for deduplication. NetBackup Appliances (5250, 5350) combine master server, media server, and storage into a single integrated platform.

| Component | Role | Typical Scale |
|---|---|---|
| Master Server | Policy, catalog, scheduling | 1 per domain (HA pair optional) |
| Media Server | Data movement, dedup | Multiple, load-balanced |
| Client | Backup agent | Per protected host |
| Storage Unit | Target storage | BasicDisk, AdvDisk, OST, Cloud, Tape |
| OpsCenter | Reporting and monitoring | Centralised, multi-domain |
