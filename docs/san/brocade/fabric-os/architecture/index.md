# Brocade Fabric OS Architecture

Fabric OS runs on Brocade/Broadcom SAN switches including the G620, G720, and X7 director platforms. Fabrics are deployed in a core-edge topology with ISLs connecting edge switches to core directors, providing scalable FC connectivity for hosts and storage. One switch per fabric is elected as the principal switch, which owns the fabric name server and manages domain ID assignments. Port types include E_Port (ISL), F_Port (fabric/host-facing), and N_Port (node/initiator-facing), with FCIDs assigned by the principal switch upon fabric login.

| Component | Role |
|---|---|
| Principal switch | Fabric name server, domain ID assignment |
| E_Port | Inter-switch link (ISL) |
| F_Port | Fabric port — connects to host HBAs or storage |
| N_Port | Node port — on the host or storage side |
| Domain ID | Unique switch identifier within the fabric (1–239) |
| FCID | 3-byte address assigned per device at FLOGI |
