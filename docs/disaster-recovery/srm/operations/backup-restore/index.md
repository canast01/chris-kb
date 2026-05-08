# SRM — Backup & Restore

## SRM Backup Considerations

VMware Site Recovery Manager (SRM) does not protect the virtual machines it manages — it orchestrates their recovery. Protecting the SRM infrastructure itself is a separate and critical requirement. An SRM deployment that cannot be restored is a single point of failure for the entire DR plan.

**Components that must be protected:**

| Component | What to Back Up | Method |
|---|---|---|
| SRM Server (vCenter Plugin) | SRM DB, configuration, recovery plans | DB backup + export |
| SRM Database | SQL Server or vPostgres DB | SQL backup / snapshot |
| Recovery Plans | Exported as XML | Manual export or scripted |
| SRM Certificates | Pairing certs between sites | Export from SRM UI |
| vCenter | SRM depends on vCenter — vCenter must also be protected | vCenter file-based backup (VAMI) |

---

## SRM Database Backup

SRM uses either an embedded vPostgres database (appliance deployments) or an external SQL Server / Oracle database.

### Embedded vPostgres (SRM Appliance)

SRM 8.x and later ship as a Linux appliance. The embedded database is backed up via the VAMI file-based backup.

**Enable file-based backup in VAMI:**

1. Log in to `https://<srm-appliance>:5480`.
2. Navigate to **Backup**.
3. Configure an SFTP or SCP backup destination.
4. Set a schedule (daily recommended).
5. Click **Backup Now** for an immediate backup.

The VAMI backup captures the SRM appliance state, database, and configuration in a single archive.

**Verify backup:**

```bash
# On the SRM appliance (SSH)
ls -lh /var/lib/applmgmt/backup/
# Should show recent .tar.gz archive files
```

### External SQL Server Database

```sql
-- Full database backup
BACKUP DATABASE [VMwareSRM] 
TO DISK = N'\\backup-server\sql-backups\VMwareSRM_Full.bak'
WITH FORMAT, INIT, COMPRESSION, STATS = 10;

-- Verify backup
RESTORE VERIFYONLY 
FROM DISK = N'\\backup-server\sql-backups\VMwareSRM_Full.bak';
```

Schedule via SQL Agent job, and ensure the `.bak` files are protected by your enterprise backup solution.

---

## Exporting Recovery Plan XML

Recovery Plans can be exported as XML for documentation and restore purposes. Export after every plan modification.

### Via SRM UI

1. Log in to **vSphere Client** → **Site Recovery** plugin.
2. Navigate to **Recovery Plans**.
3. Select a plan → **Export** → **Download XML**.
4. Save to a protected location (Git repository, network share, or backup system).

### Via PowerShell (SRM PowerCLI)

```powershell
# Connect to vCenter and SRM
Connect-VIServer -Server vcenter01.example.com -Credential (Get-Credential)
$srm = Connect-SrmServer -SrmServerAddress srm01.example.com `
                         -Credential (Get-Credential)

# Get SRM API
$api = $srm.ExtensionData

# List recovery plans
$plans = $api.Recovery.ListPlans()
$plans | Select-Object MoRef, Description

# Export each plan to XML
foreach ($plan in $plans) {
    $planInfo = $api.Recovery.GetPlan($plan)
    $planName = $planInfo.Info.Name -replace '[^\w]', '_'
    $xml      = $api.Recovery.ExportRecoveryPlan($plan)
    $xml | Out-File "C:\SRM-Backups\$planName.xml" -Encoding UTF8
    Write-Host "Exported: $planName.xml"
}
```

Store these XML files in version control. A `git diff` against the previous export immediately shows what changed in a plan.

---

## SRM Configuration Backup

In addition to the database and recovery plans, the SRM pairing configuration and certificates should be captured.

### Export SRM Configuration via UI

1. **vSphere Client** → **Site Recovery** → **Site Pair** → select the pair.
2. Navigate to **Configuration** → **Export Configuration**.
3. Save the export archive.

### Capture SRM Certificate Thumbprints

```powershell
# Record the pairing certificate thumbprints for reconstruction reference
$srmInstance = Connect-SrmServer -SrmServerAddress srm01.example.com -Credential (Get-Credential)
$cert = $srmInstance.ExtensionData.GetCertificate()
Write-Host "SRM Certificate Thumbprint: $($cert.Thumbprint)"
```

---

## Restore SRM from Backup

### Restore from VAMI File-Based Backup (Appliance)

1. Deploy a fresh SRM OVA at `https://<vc>/ui` → **Deploy OVF Template**.
2. Configure with the same hostname and IP as the failed instance.
3. Log in to VAMI (`https://<new-srm-appliance>:5480`).
4. Navigate to **Restore**.
5. Provide the SFTP path to the backup archive.
6. Click **Restore** — the appliance will restore configuration and DB, then restart SRM services.

### Restore from SQL Backup (External DB)

```sql
-- Restore on SQL Server
RESTORE DATABASE [VMwareSRM]
FROM DISK = N'\\backup-server\sql-backups\VMwareSRM_Full.bak'
WITH REPLACE, RECOVERY;
```

1. Ensure the restored SQL instance is accessible from the new SRM server.
2. Install a fresh SRM appliance/server.
3. During setup wizard, point to the existing (restored) SQL database.
4. SRM will import the configuration from the restored DB.

### Recover Recovery Plans from XML Export

If the DB is unrecoverable but XML exports exist:

1. Install and configure SRM fresh.
2. Re-pair the sites (see below).
3. In **Recovery Plans** → **Import Recovery Plan** → select each XML file.
4. Review imported plans — protection groups and inventory mappings must be re-validated.

---

## Re-pairing Sites After Recovery

After SRM is reinstalled or restored, the site pair may need to be re-established.

```mermaid
flowchart TD
    A([SRM Restored on Primary Site]) --> B[Log in to vSphere Client\nSite Recovery plugin]
    B --> C{Site pair still intact?}
    C --> |Yes| D[Verify pair status\nand test connectivity]
    C --> |No| E[Remove existing pairing\nif stale]
    E --> F[Pair Sites]
    F --> G[Enter DR site SRM address\nand credentials]
    G --> H[Accept certificates\nfrom both sites]
    H --> I[Pair completes —\nvalidate connectivity]
    D --> J[Re-validate protection groups]
    I --> J
    J --> K{Protection groups healthy?}
    K --> |Yes| L[Re-validate recovery plans]
    K --> |No| M[Re-configure VMs\ninto protection groups]
    M --> L
    L --> N{Plans pass validation?}
    N --> |Yes| O([SRM Operational])
    N --> |No| P[Fix plan errors\nre-run validation]
    P --> L
```

### Re-pairing Steps

1. **vSphere Client** → **Site Recovery** → **Open Site Recovery**.
2. Click **New Site Pair**.
3. Enter the DR site vCenter FQDN and credentials.
4. Enter the DR site SRM FQDN and credentials.
5. Accept the self-signed certificates from both sites.
6. Click **Connect** — the pairing completes and inventory mappings are loaded.
7. Navigate to **Recovery Plans** → run **Validate** on each plan.

---

## SRM Backup & Restore Workflow

```mermaid
flowchart LR
    subgraph Protect["Protect SRM"]
        A["VAMI Scheduled Backup\n(nightly)"] --> B["Backup Archive on SFTP\n(off-appliance)"]
        C["Recovery Plan XML Export\n(after each change)"] --> D["XML Files in Version Control\nor Network Share"]
        E["SRM DB Backup\n(external SQL)"] --> F["SQL .bak on\nBackup-Protected Share"]
    end

    subgraph Recover["Recover SRM"]
        G["Deploy fresh SRM OVA"] --> H["VAMI Restore\nfrom SFTP archive"]
        H --> I["Re-pair Sites\n(if needed)"]
        I --> J["Import Recovery Plans\nfrom XML if DB lost"]
        J --> K["Validate Protection Groups\nand Recovery Plans"]
    end

    B --> H
    D --> J
    F --> H

    style Protect fill:#1a4a2a,color:#fff
    style Recover fill:#1a3a5c,color:#fff
```

---

## Post-Recovery Validation Checklist

| # | Check | Method |
|---|---|---|
| 1 | SRM services running on both sites | VAMI → Summary → Service Status |
| 2 | Site pair connected | Site Recovery → Site Pairs → Status: Connected |
| 3 | vCenter inventory mapping intact | Site Recovery → Configure → Inventory Mappings |
| 4 | Network mappings correct | Site Recovery → Configure → Network Mappings |
| 5 | Protection groups show VMs protected | Site Recovery → Protection Groups → Status |
| 6 | Recovery plans validate without errors | Recovery Plans → Validate All → 0 errors |
| 7 | SRM DB accessible and populated | Check plan count matches pre-restore |
| 8 | Recovery plan XML matches latest export | Compare imported plan with version control |
| 9 | VAMI backup scheduled and tested | VAMI → Backup → Schedule active |
| 10 | Recovery documented | Incident/DR test record updated |
