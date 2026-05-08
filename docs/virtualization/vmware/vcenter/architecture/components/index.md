# vCenter Architecture — Components

## Platform Role

vCenter is the central management plane for VMware environments. It manages inventory, clusters, hosts, VMs, datastores, networks, permissions, alarms, tasks, events, and automation APIs.

## Core Services

| Service | Description |
|---|---|
| vCenter Server Appliance (VCSA) | The main management appliance; Photon OS-based |
| vpxd | Core vCenter daemon — inventory, scheduling, HA/DRS orchestration |
| vSphere Client | HTML5 web UI at `https://<vcenter>/ui` |
| Embedded PSC / SSO | Authentication, SSO domain, VMCA certificate authority, licensing |
| vPostgres (PostgreSQL) | Embedded database — vCenter inventory, events, tasks |
| Inventory Service | Object indexing and search |
| vAPI Endpoint | Modern REST API at `https://<vcenter>/api` |
| Lookup Service | Service registry for all vCenter components |
| Certificate Manager (VMCA) | Issues and renews certificates for VCSA and ESXi hosts |
| Task and Event Subsystem | Tracks all operations and changes |
| Backup Scheduler | Built-in file-based backup via VAMI |

## Main Dependencies

| Dependency | Notes |
|---|---|
| DNS | Forward and reverse resolution required for VCSA FQDN and all ESXi hosts |
| NTP | Time sync mandatory; skew > 5 minutes breaks Kerberos and SSO |
| Authentication Source | AD/LDAP identity source for user authentication |
| Management Network | VCSA must be reachable from all ESXi hosts on port 443; hosts reachable on 902 |
| Storage | VCSA runs as a VM; requires reliable datastore access |
| Certificate Trust | All services use TLS; expired certificates cascade into auth failures |
| Monitoring | Aria Operations or equivalent |
| Backup / Recovery | VAMI file-based backup or equivalent; tested restore procedure |
| Vendor Support | Broadcom support portal access for escalation |

## Ports and Protocols

| Use | Protocol | Port |
|---|---|---|
| vSphere Client / API | HTTPS | 443 |
| ESXi host management | HTTPS | 443 |
| ESXi host agent heartbeat | TCP/UDP | 902 |
| VCSA VAMI (appliance management) | HTTPS | 5480 |
| vCenter HA replication | TCP | 8443 |
| LDAP | TCP | 389 |
| LDAPS | TCP | 636 |
| Syslog | UDP/TCP | 514 |
| DNS | TCP/UDP | 53 |
| NTP | UDP | 123 |

## Key Logs

| Component | Log Path |
|---|---|
| vpxd (core vCenter service) | `/var/log/vmware/vpxd/vpxd.log` |
| vSphere Client | `/var/log/vmware/vsphere-ui/logs/vsphere_client_virgo.log` |
| SSO / identity | `/var/log/vmware/sso/vmware-sts-idmd.log` |
| SSO admin server | `/var/log/vmware/sso/ssoAdminServer.log` |
| vAPI endpoint | `/var/log/vmware/vapi/` |
| Appliance management (VAMI) | `/var/log/vmware/applmgmt/applmgmt.log` |
| Upgrade / patch | `/var/log/vmware/applmgmt/software-packages.log` |
| Certificate manager | `/var/log/vmware/vmcad/certificate-manager.log` |
| Postgres DB | `/var/log/vmware/vpostgres/postgresql-*.log` |

## Common Failure Points

- Expired certificates (machine SSL, STS signing, VMCA root)
- SSO or identity source failure (AD bind account, LDAP connectivity)
- Appliance partition full (`/storage/log`, `/storage/db`)
- vCenter service failure (vpxd, vmware-vpostgres)
- Host communication failure (vpxa agent stopped, certificate mismatch)
- Backup target failure (SFTP unreachable, credentials expired)
- DNS or NTP drift (causes cascading auth and certificate failures)
- Permission drift (unexpected access changes, lost admin access)

## Useful Commands

```bash
# Service management (VCSA SSH)
service-control --status
service-control --status --all
service-control --start vmware-vpostgres
service-control --start vpxd
service-control --stop --all
service-control --start --all

# Disk usage
df -h

# VECS certificate store
/usr/lib/vmware-vmafd/bin/vecs-cli store list
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT --text | grep -E "Alias|Not After"

# SSO domain info
/usr/lib/vmware-vmafd/bin/vmafd-cli get-domain-name --server-name localhost
```
