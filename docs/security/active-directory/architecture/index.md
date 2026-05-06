# Active Directory Architecture

Active Directory is organised into a Forest → Domain → Site hierarchy, with the forest as the ultimate security boundary and domains providing administrative partitions. Key services include LDAP (ports 389/636), Kerberos (port 88), DNS (port 53), and SMB/RPC for inter-DC replication. The typical enterprise design uses a single forest with one or more regional domains, two Domain Controllers per site for high availability, and deliberate FSMO role placement across DCs to avoid single points of failure.

| Component | Role |
|---|---|
| Forest Root Domain | Schema master, Enterprise Admins, trust anchor |
| Regional Domains | Administrative boundary per region or BU |
| Sites & Site Links | Control replication topology and KDC selection |
| FSMO Roles | PDC Emulator, RID Master, Infrastructure Master, Schema Master, Domain Naming Master |
| Global Catalog | Partial attribute set replica, universal group membership cache |
