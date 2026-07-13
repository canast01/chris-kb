---
tags:
  - architecture
  - netapp
description: "SnapCenter integrations: vSphere plugin for VM-consistent snapshots, ONTAP SnapMirror chain for DR copies, SnapVault for long-term retention, and Active..."
---
# SnapCenter — Integrations

<div class="kb-summary">
SnapCenter integrations: vSphere plugin for VM-consistent snapshots, ONTAP SnapMirror chain for DR copies, SnapVault for long-term retention, and Active IQ integration.

*Applies to: SnapCenter 5.x*
</div>
![SnapCenter — Integrations](../../../../../assets/storage-netapp-snapcenter-architecture-integrations.svg)

---

## ONTAP Storage Systems

Register ONTAP clusters in SnapCenter under Settings → Storage Systems. SnapCenter communicates with ONTAP via REST API (SnapCenter 6.x) or ZAPI (SnapCenter 5.x and earlier).

```powershell
# Add ONTAP storage system via PowerShell
Add-SmStorageConnection -StorageName <cluster-mgmt-fqdn> -Protocol HTTPS -Port 443 -Credential (Get-Credential)
```

- Use a dedicated ONTAP service account with `vsadmin` role or a custom role scoped to the SVMs SnapCenter manages
- Register the cluster-management LIF, not individual node management LIFs
- SnapCenter automatically discovers SVMs, volumes, and LUNs on the registered cluster

## vCenter / VMware Integration

The **SnapCenter Plug-in for VMware vSphere** is deployed as a separate OVA and registered with vCenter:

1. Deploy the OVA from [mysupport.netapp.com](https://mysupport.netapp.com) into vCenter
2. After deployment, access the plugin UI at `https://<plugin-vm-ip>:8144`
3. Register the plugin with vCenter: Settings → vCenter registration → enter vCenter credentials
4. Add ONTAP storage systems to the plugin (separate from the SnapCenter Server connections)
5. The plugin appears as "NetApp SnapCenter" in the vCenter HTML5 client under Plugins

Use cases: VM-consistent snapshot backup, datastore backup, individual VMDK restore, and guest file restore without in-guest agents.

## Active Directory / RBAC

SnapCenter supports AD authentication for user accounts and group-based RBAC:

```powershell
# Add an AD user to SnapCenter with a specific role
Add-SmUser -UserName domain\username -RoleName "Application Backup and Clone Admin"

# Add an AD group
Add-SmUser -UserName "domain\SnapCenter-Admins" -RoleName "SnapCenter Admin"

# List all SnapCenter users and roles
Get-SmUser | Select UserName, RoleName
```

## Email Notifications

Configure SMTP in SnapCenter Settings → Global Settings → Email Notification:

- SMTP server, port (25 or 587 with TLS), sender address, and recipient lists
- Per-resource-group notification can override global settings: resource group → Edit → Notification tab
- Alert on: Never / On Error / On Error or Warning / Always — recommend "On Error or Warning" for production resource groups

```powershell
# Configure global email notification
Set-SmEmailNotification -SmtpServer mail.corp.domain.com -From snapcenter@corp.domain.com -To storage-team@corp.domain.com -NotifyWhen OnFailure
```

## REST API

SnapCenter exposes a full REST API for automation. The Swagger UI is at:

```text
https://<snapcenter-server>:8146/swagger/
```

Authenticate with a token:
```bash
# Get an auth token
curl -sk -X POST "https://<snapcenter-server>:8146/api/3.0/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"UserOperationContext":{"User":{"Name":"admin","Passphrase":"<password>","Rolename":"SnapCenter Admin"}}}' \
  | python3 -m json.tool

# List all resource groups (use token from above response)
curl -sk -X GET "https://<snapcenter-server>:8146/api/3.0/resourcegroups" \
  -H "token: <auth-token>" | python3 -m json.tool
```


```text title="Expected output"
{
  "Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTcwMjQwMTIzNCwiZXhwIjoxNzAyNDA0ODM0fQ.kX9mZ2pL5nQ8vR3wT6yJ2aB4cD7eF9gH1iK3lM5nO7p",
  "UserName": "admin",
  "Rolename": "SnapCenter Admin"
}
{
  "ResourceGroups": [
    {
      "Id": "rg-001",
      "Name": "prod-db-backup",
      "Description": "Production database daily backups",
      "HostNames": ["db-server-01.corp.local", "db-server-02.corp.local"],
      "ResourceType": "SQL Server Database"
    },
    {
      "Id": "rg-002",
      "Name": "vmware-vms",
      "Description": "VMware virtual machines",
      "HostNames": ["esx-host-03.corp.local"],
      "ResourceType": "VMware"
    },
    {
      "Id": "rg-003",
      "Name": "oracle-prod",
      "Description": "Oracle production databases",
      "HostNames": ["oracle-db-01.corp.local"],
      "ResourceType": "Oracle Database"
    }
  ],
  "TotalResourceGroups": 3
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to skip SSL verification (already present in the example, but ensure it's included if removed). |
    | `{"Error":"Invalid token or token expired"}` | Regenerate the auth token by re-running the login command and ensure the token value is copied exactly without extra whitespace. |
    | `{"Error":"User 'admin' does not have permission to access resourcegroups"}` | Verify the user account has the SnapCenter Admin role assigned in the SnapCenter UI under Settings > Users. |
## Oracle Plugin Integration

The SnapCenter Plug-in for Oracle communicates with the Oracle database via OS authentication (SYSDBA) to quiesce the database before snapshot. Requirements:
- Oracle user running the database must be discoverable by the plugin
- `oracle` OS user must have read access to `/etc/oratab`
- Plugin runs as root (Linux) to access Oracle processes and RMAN for granular restore
- RMAN catalog integration optional but recommended for tablespace and datafile-level recovery

## SQL Server Plugin Integration

The SnapCenter Plug-in for SQL Server uses VSS to quiesce SQL Server databases before snapshot:
- Supports SQL Server Availability Groups (AG) — SnapCenter discovers AG replicas and can back up from a preferred replica
- For AG, register all SQL nodes in the resource and configure preferred backup replica in the resource settings
- Post-backup log truncation controlled by policy setting (Full/Log backup chaining for point-in-time recovery)

---

## See also

- [Snapcenter — How It Works](../how-it-works/)
- [Snapcenter — Design Standards](../design-standards/)
