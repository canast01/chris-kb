# Aria Operations for Logs — Search Examples

```mermaid
flowchart LR
    for_Logs["for Logs"]
    for_Logs --> S0["Host Disconnect Events"]
    for_Logs --> S1["vCenter Authentication Failures"]
    for_Logs --> S2["Certificate Errors"]
    for_Logs --> S3["vMotion Failures"]
    for_Logs --> S4["HA Events"]
    for_Logs --> S5["DRS Events"]
    for_Logs --> S6["Datastore Errors"]
    for_Logs --> S7["vSAN Errors"]
```

## Host Disconnect Events

```
lost connectivity to the server
not responding
connection refused
```

## vCenter Authentication Failures

```
Failed to authenticate
Login failed
password incorrect
SessionManager
```

## Certificate Errors

```
certificate
SSL
handshake failed
x509
STS
```

## vMotion Failures

```
vmotion
migration failed
VMotionFailed
```

## HA Events

```
HA failover
ha.vm.restart
failover started
admission control
```

## DRS Events

```
DRS
migration recommended
load balance
```

## Datastore Errors

```
datastore
SCSI error
APD
PDL
NFS
VMFS
```

## vSAN Errors

```
vsan
disk group
resync
object health
storage compliance
```

## NSX Errors

```
nsx
transport node
edge
TEP
segment
```

## Time-Based Search Tips

- Always set a time range — start with the last 1 hour for active incidents
- Expand to 24 hours or 7 days when investigating intermittent issues
- Use the timeline view to identify event spikes
- Cross-reference vCenter event timestamps with host log timestamps
