# FlashArray — Components

## Core Components

| Component | Description |
|---|---|
| Controllers (CT0, CT1) | Two active-active controllers sharing ownership of all volumes; each runs a full Purity//FA instance |
| NVMe drives / SAS SSDs | Flash media carrying user data and Purity metadata; drives are direct-attached inside the chassis |
| Purity//FA OS | The operating system managing data services: deduplication, compression, thin provisioning, snapshots, and replication |
| Fabric modules (//X) | NVMe-oF fabric connectivity cards in the //X series providing NVMe/FC, NVMe/RoCE, and NVMe/TCP host ports |
| Host interface cards | FC (16/32 Gb), iSCSI (10/25 GbE), or NVMe/TCP (25/100 GbE) adapters in the I/O module bays |
| Replication / management ports | Dedicated 10 GbE ports for inter-array replication, management access, and Pure1 phone-home |
| Pure1 cloud management | SaaS monitoring, AI analytics, capacity planning, and upgrade scheduling; no on-premises management VM required |
| SafeMode snapshots | Immutable, admin-delete-locked snapshot capability for ransomware protection |
