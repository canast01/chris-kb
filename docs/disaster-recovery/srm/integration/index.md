# SRM Integration

SRM supports both array-based replication (via vendor SRAs) and vSphere Replication as built-in protection mechanisms, allowing mixed protection strategies within a single SRM deployment. NSX network mapping enables micro-segmentation policies to follow VMs across sites during failover, preserving security group membership. Aria Operations includes an SRM monitoring pack that surfaces protection group health, RPO compliance, and recovery plan readiness metrics.

- **Dell EMC SRA**: Supports PowerMax SRDF/A and SRDF/S; install SRA v5.x+ on both SRM servers and register via SRM UI → Array Managers.
- **Pure Storage SRA**: Supports ActiveCluster (synchronous) and async SnapMirror-equivalent; registered and managed the same way.
- **NetApp SnapMirror SRA**: Supports ONTAP SnapMirror for array-based protection groups.
- **vSphere Replication**: Built-in; no SRA needed; per-VM RPO configurable from 5 minutes; managed via embedded vSphere Replication appliance.
- **NSX integration**: Define network mappings between NSX segments on protected and recovery sites; micro-segmentation policies are preserved on failover.
- **Aria Operations SRM pack**: Dashboards for RPO compliance, protection group state, and recovery plan history.
