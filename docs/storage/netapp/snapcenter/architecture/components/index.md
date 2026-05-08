# SnapCenter — Components

> Part of the [SnapCenter Architecture](../) reference.

---

## Components

| Component | Description |
|---|---|
| SnapCenter Server | Windows Server hosting the SnapCenter web application, scheduler, and REST API; accessible at `https://<server>:8146` |
| Repository Database | MySQL database installed on the SnapCenter Server host (or a separate MySQL server); stores all job history, policies, resource groups, and RBAC configuration |
| SnapCenter Agent | Lightweight Windows or Linux service (port 8145) installed on each protected host; communicates with the SnapCenter Server and runs pre/post quiesce scripts |
| SnapCenter Plug-in for Windows | Agent extension for Windows filesystem and VSS-based application backup; supports SQL Server, Exchange, and Windows filesystems |
| SnapCenter Plug-in for UNIX | Agent extension for Linux/AIX; supports Oracle, SAP HANA, and UNIX filesystems |
| SnapCenter Plug-in for VMware vSphere | Separate OVA appliance registered with vCenter; provides VM-level and datastore-level backup without an agent inside VMs |
| ONTAP Storage Systems | Registered as storage connections in SnapCenter; SnapCenter creates and manages ONTAP snapshots, SnapMirror updates, and SnapVault transfers via ONTAP APIs |
| SMTP / Email Relay | Optional; SnapCenter sends job success/failure notifications via SMTP |

## Sizing Guidelines

- **SnapCenter Server**: Minimum 4 vCPU, 8 GB RAM for up to 50 hosts; scale to 8 vCPU / 16 GB for 50–200 hosts; dedicated Windows Server (2019 or 2022)
- **Repository database**: MySQL data directory sizing — allow ~500 MB per 1,000 backup jobs retained; 20 GB minimum partition
- **Concurrent jobs**: Default maximum concurrent jobs is 5; increase to 10–20 in SnapCenter global settings for large environments, limited by ONTAP API throughput
- **Plugin hosts per server**: A single SnapCenter Server supports up to several hundred registered hosts; beyond 300–400 active hosts, evaluate a secondary SnapCenter instance for scale-out
- **SnapCenter Plug-in for VMware**: Deploy one OVA per vCenter; supports thousands of VMs; requires access to vCenter API and ONTAP APIs for all datastores

---

## Plugins

SnapCenter uses host-based plugins to quiesce applications before snapshot creation, enabling application-consistent backups.

| Plugin | Use Case |
|---|---|
| SnapCenter Plug-in for Windows | Windows file systems, SQL Server |
| SnapCenter Plug-in for SQL Server | SQL Server databases (VSS-based) |
| SnapCenter Plug-in for Oracle | Oracle DB on Linux/Windows |
| SnapCenter Plug-in for SAP HANA | SAP HANA databases |
| SnapCenter Plug-in for VMware vSphere | VMware VMs and datastores |
| SnapCenter Plug-in for UNIX | Linux file systems |

### Checking Plugin Status

In the SnapCenter UI:
1. Navigate to **Hosts** → verify all hosts show `Running`
2. A host with `Stopped` or `Not reachable` requires investigation

### Installing a Plugin

1. Navigate to **Hosts → Add**
2. Enter host FQDN, credentials, and select plug-in packages
3. SnapCenter pushes the installer to the host automatically
4. Verify status shows `Running` after installation

### Restarting a Plugin

If a plugin shows `Stopped`:

```bash
# Windows (PowerShell — on the target host)
Restart-Service -Name "SnapCenter Plug-in for Windows"

# Linux (on the target host)
/opt/NetApp/snapcenter/scc/bin/scc restart
```

### Plugin Communication

- SnapCenter Server communicates with plugins over **port 8145** (default)
- Ensure firewall rules allow TCP 8145 from SnapCenter Server to each managed host
- Plugin hosts require outbound connectivity back to SnapCenter Server
