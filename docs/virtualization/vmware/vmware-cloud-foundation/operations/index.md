# VMware Cloud Foundation Operations

Daily operational checks for VCF begin in the SDDC Manager dashboard, which surfaces domain health, certificate status, and component alerts across the management and workload domains. NSX overlay health — including BGP adjacency state, edge cluster status, and tunnel endpoint reachability — should be verified via NSX Manager each morning, as VCF does not surface all NSX fabric events in SDDC Manager. vSAN cluster health can be reviewed via the vCenter Skyline Health plugin or the `RVC` utility, and any failed disk or resync events must be investigated before initiating any lifecycle operations.

**Daily check runbook:**
- SDDC Manager > Dashboard: all workload domains show "Healthy"
- SDDC Manager > Security > Certificates: no certificates expiring within 60 days
- NSX Manager > System > Fabric > Nodes: all hosts "Up"; transport nodes healthy
- NSX Manager > Networking > Tier-0 Gateways: BGP neighbours established
- vCenter > vSAN Cluster > Skyline Health: no critical alerts
- SDDC Manager > Lifecycle Management > Bundle Management: review available updates
- Check SDDC Manager disk: `df -h` on the appliance — `/` and `/data` below 80%
