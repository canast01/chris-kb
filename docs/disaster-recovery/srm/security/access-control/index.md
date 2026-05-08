# SRM Security — Access Control

## vCenter RBAC for DR Operators

Define a dedicated `DR-Operator` role in vCenter with only the privileges required for SRM operations:

```
Privileges to include:
  Site Recovery Manager:
    - Site Recovery.Manage
    - Site Recovery.Test
    - Site Recovery.Recovery
  Datastore:
    - Datastore.AllocateSpace
  Network:
    - Network.Assign (for network customisation)
  Virtual Machine:
    - Virtual Machine.Provisioning.* (for recovery)
```

Assign the role at the SRM inventory root — do not grant broad vCenter Admin privileges to DR operators.
