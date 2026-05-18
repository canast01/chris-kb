# VMware Platform Upgrade Procedure

This procedure covers a full VMware platform upgrade including vCenter, ESXi, vSAN, NSX, and VCF-related components.

```
┌──────────────────────────────────────────────────────────────────────────┐
│            VMware Platform Upgrade Order                                 │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ 1. Backup: vCenter (VAMI) + NSX + Aria snapshots + CR VM snaps    │   │
│  └───────────────────────────────┬────────────────────────────────────┘  │
│                                  ▼                                       │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ 2. vCenter upgrade (must be ≥ ESXi version at all times)          │   │
│  └───────────────────────────────┬────────────────────────────────────┘  │
│                                  ▼                                       │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ 3. NSX upgrade (Coordinator → Managers → Edges → Hosts)           │   │
│  └───────────────────────────────┬────────────────────────────────────┘  │
│                                  ▼                                       │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ 4. ESXi host upgrades (one host at a time, via LCM)               │   │
│  └───────────────────────────────┬────────────────────────────────────┘  │
│                                  ▼                                       │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ 5. vSAN disk format upgrade (after all hosts upgraded + health OK) │  │
│  └───────────────────────────────┬────────────────────────────────────┘  │
│                                  ▼                                       │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ 6. Final validation + CR closure + version inventory update        │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│  VxRail: use VxRail LCM for all steps — do NOT upgrade ESXi manually     │
└──────────────────────────────────────────────────────────────────────────┘
```
## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| VMware Engineer | Owns upgrade execution and validation |
| Storage Engineer | Validates datastore, vSAN, or external array health |
| Network Engineer | Validates VLANs, MTU, routing, NSX, and uplinks |
| Backup Engineer | Confirms backups and restore points |
| Application Owner | Validates application functionality after upgrade |
| Change Owner | Owns communication, approval, and ticket updates |
| Vendor Support | Assists with failures, stuck upgrades, or rollback decisions |

---

## Phase 1: Planning

### Capture Current Versions

Document before starting:

- vCenter version and build
- ESXi version and build per cluster
- vSAN version and disk format version
- NSX version
- VCF version if used
- VxRail version if applicable
- Aria Operations version
- Backup platform version
- Storage array code version
- Server firmware and driver versions

### Confirm Target Versions

- Target vCenter version
- Target ESXi version
- Target vSAN version
- Target NSX version
- Target VCF bill of materials if applicable
- Target firmware and driver baseline
- Target backup plugin version if needed

### Review Upgrade Path

Confirm:

- Direct upgrade is supported
- No intermediate version is required
- Component compatibility is confirmed
- Known issues are reviewed
- Deprecated features and removed drivers noted
- Plugin compatibility confirmed
- API or integration changes understood

### Upgrade Order

Common order:

1. Backup and monitoring compatibility review
2. vCenter backup
3. NSX backup if used
4. VCF or SDDC Manager pre-checks if used
5. vCenter upgrade
6. NSX upgrade if used
7. ESXi host upgrades (one host at a time)
8. vSAN disk format upgrade if required
9. Aria and monitoring validation
10. Backup validation
11. Application validation

> For VCF environments, use SDDC Manager lifecycle order instead of manually upgrading components.

---

## Phase 2: Pre-Upgrade Checks

### Change Approval

Confirm before starting:

- Approved change ticket with maintenance window
- Business impact documented
- Application owner awareness confirmed
- Communication plan ready
- Rollback plan documented
- Vendor support contacts available

### Access Validation

Confirm access to:

- vCenter and vSphere Client
- VCSA Appliance Management Interface
- SSO administrator account
- VCSA root account if needed
- Hardware management interface (iDRAC/iLO)
- Backup console
- NSX Manager if used
- SDDC Manager if VCF is used
- VxRail Manager if VxRail is used

### Backup Validation

Confirm:

- vCenter file-based backup completed and encryption password is available
- NSX backup completed if NSX is used
- Aria backup or snapshot plan confirmed
- Critical VM backups completed
- Backup repository has capacity

### Environment Health Checks

Validate:

- vCenter services healthy, no critical alarms
- All ESXi hosts Connected, none unexpectedly in maintenance mode
- HA and DRS healthy
- Datastores accessible with adequate free space
- No unexpected snapshot growth
- vSAN Skyline Health green, no active resyncs if avoidable
- NSX Manager cluster healthy if used
- Backup jobs not running against target VMs
- Monitoring active

### DNS, NTP, and Certificate Checks

- DNS forward and reverse lookup working for vCenter, ESXi, NSX
- NTP synced across vCenter, ESXi, NSX, and identity sources
- vCenter machine, STS, and solution user certificates valid
- NSX and Aria certificates valid
- No certificate expiring during the maintenance window

---

## Phase 3: vCenter Upgrade

### Before Starting

- Run a fresh file-based backup and confirm it completes
- Pause large VM migrations, storage migrations, bulk provisioning, and backup snapshot jobs
- Run upgrade pre-checks: disk space, database health, service health, SSO health, plugin compatibility

### Upgrade Steps

1. Mount or launch vCenter installer
2. Start upgrade workflow
3. Deploy new appliance if required
4. Connect to source vCenter
5. Run pre-checks and resolve any failures
6. Confirm network settings and appliance size
7. Start data migration
8. Monitor upgrade progress
9. Log into new vCenter after completion
10. Confirm old appliance state — do not delete until new vCenter is validated

### Post-Upgrade Validation

- vCenter login works
- All services running: `service-control --status`
- Inventory, hosts, clusters, datastores, and distributed switches visible
- Permissions and tags intact
- Plugins working
- Backup and monitoring tools reconnected
- No unexpected alarms

### Rollback Notes

Consider rollback if:

- Upgrade fails before migration completes
- vCenter services fail after upgrade
- Inventory is missing or SSO is broken
- Hosts cannot reconnect
- Critical integrations fail

---

## Phase 4: NSX Upgrade

*Only perform if NSX is part of the environment.*

### Pre-Checks

- NSX Manager cluster healthy, all nodes online
- Edge nodes and transport nodes healthy
- TEP connectivity confirmed
- Backup completed
- vCenter registration healthy
- No critical NSX alarms

### Upgrade Order

1. NSX Upgrade Coordinator pre-check
2. Edge nodes
3. Host transport nodes
4. NSX Manager nodes
5. Post-upgrade validation

### Post-Upgrade Validation

- NSX Manager UI login
- Edge node and transport node health
- Segment connectivity and TEP connectivity
- Gateway, distributed firewall rules, and routing functioning

---

## Phase 5: ESXi Host Upgrade

### Pre-Checks (Per Host)

- Host Connected with no hardware errors
- Cluster has enough capacity for evacuation
- DRS can evacuate workloads
- No VM is pinned to this host
- vSAN resync not active if avoidable
- Correct image or baseline confirmed
- Firmware and driver compatibility confirmed

### Maintenance Mode — vSAN Evacuation Options

| Option | Use Case |
|---|---|
| Ensure Accessibility | Common for planned maintenance when redundancy exists |
| Full Data Migration | Safer but slower; requires enough free capacity |
| No Data Migration | Higher risk; use only when approved and understood |

### Remediation Steps

1. Attach baseline or image in Lifecycle Manager
2. Stage patches if supported
3. Remediate host
4. Allow reboot and wait for host reconnect
5. Confirm ESXi version and build
6. Exit maintenance mode
7. Validate host health

### Continue Cluster Upgrade

- Upgrade one host at a time
- Watch DRS behavior, vSAN resyncs, and datastore latency
- Pause if errors repeat on multiple hosts

---

## Phase 6: vSAN Upgrade

*Only perform if vSAN is used.*

### Pre-Checks

- Skyline Health green, no failed disks, no inaccessible objects
- No unexpected resyncs, capacity within safe limits
- All hosts on the correct ESXi version
- Disk groups healthy

### Disk Format Upgrade

Only upgrade disk format after confirming it is required and all hosts are upgraded.

1. Confirm Skyline Health is green
2. Confirm no active resync
3. Start disk format upgrade
4. Monitor resync activity and object compliance
5. Validate vSAN health after completion

---

## Phase 7: Final Validation

- vCenter access and services
- All ESXi hosts Connected, HA and DRS healthy
- Datastores accessible, VMs running
- vMotion and storage vMotion working
- vSAN healthy
- NSX healthy if used
- Backup jobs running
- Monitoring dashboards active
- Aria integrations working
- Application owner validation complete
- Active alarms reviewed

## Phase 8: Documentation

Update:

- Change ticket with results and screenshots
- Version inventory
- Upgrade notes and lessons learned
- Support case numbers if used
- Rollback notes
- Next recommended action
