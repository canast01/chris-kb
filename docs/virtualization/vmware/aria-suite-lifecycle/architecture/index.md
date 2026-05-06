# Aria Suite Lifecycle Architecture

Aria Suite Lifecycle (LCM) is deployed as a single Linux appliance provisioned via the vRealize Easy Installer, which orchestrates the initial deployment of LCM, Workspace ONE Access (VIDM), and other Aria products in a defined sequence. The appliance hosts the Lifecycle Manager service, the Locker (for certificates and passwords), and an embedded PostgreSQL database; NFS is used for binary and snapshot storage, while NTP is mandatory for certificate validity and cluster coordination. Load balancers (NSX-T or hardware) are placed in front of clustered Aria product deployments but not in front of LCM itself, which runs as a standalone appliance in the management network.

| Component | Role |
|---|---|
| LCM Appliance | Central orchestration, UI, API, Locker |
| Workspace ONE Access (VIDM) | Identity provider for all Aria products |
| vRealize Easy Installer | Bootstrap ISO for initial deployment |
| NFS Share | Binary repository and snapshot storage |
| NTP Server | Time synchronisation (mandatory) |
| DNS | Forward/reverse resolution required for all nodes |
