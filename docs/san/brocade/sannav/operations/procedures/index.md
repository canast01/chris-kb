# Brocade SANnav — Operations Procedures

SANnav Management Portal is the Brocade web-based tool for SAN fabric discovery, zoning, health monitoring, firmware management, and reporting across Brocade FC switch fabrics.

---

## Add a Fabric to SANnav Management

Registering a fabric in SANnav allows centralised management, monitoring, and zoning across all switches in that fabric.

1. Log in to SANnav at `https://<sannav-ip>:443` using an account with the **Administrator** role.
2. Navigate to **SAN > Fabrics** and click **+ Add Fabric**.
3. Enter the IP address of the principal (domain 1) switch of the fabric in the **Seed Switch IP** field.
4. Select the authentication protocol — use **SNMPv3** and enter the SNMPv3 credentials (auth and priv passwords) configured on the switch.
5. Enter the switch SSH credentials (username and password or SSH key) for out-of-band management.
6. Click **Discover** — SANnav contacts the seed switch, maps all connected switches in the fabric, and populates the topology view.
7. Confirm all expected switches appear under **SAN > Fabrics > [Fabric Name] > Switches** and that port states are correct.
8. Assign a meaningful fabric name (e.g., `DC1-Fabric-A`) and save.

---

## Discover Switches in a Fabric

When new switches are added to an existing fabric, SANnav must re-discover to update the topology and inventory.

1. In SANnav, navigate to **SAN > Fabrics** and select the relevant fabric.
2. Click **Actions > Rediscover Fabric** to trigger an immediate topology refresh.
3. Wait for the discovery job to complete — progress is visible in **Monitor > Jobs > Fabric Discovery**.
4. Navigate to **SAN > Fabrics > [Fabric Name] > Switches** and confirm the new switch appears with status **Online**.
5. Verify all ISL links from the new switch are shown as green/active in the topology diagram.
6. Set the MAPS policy on the new switch: select the switch, go to **Configure > MAPS Policy**, and apply the site-standard policy (e.g., `dflt_aggressive_policy`).
7. Confirm SNMP v3 credentials are applied: **Inventory > Switch > SNMP Configuration**.

```bash
# On the switch — verify SNMPv3 is configured before SANnav discovery
ssh admin@<switch-ip>
snmpconfig --show snmpv3
```

---

## Create and Run a Fabric Health Report

Fabric health reports provide a point-in-time assessment of switch, port, and zoning status across the fabric.

1. In SANnav, navigate to **Monitor > Reports** and click **+ New Report**.
2. Select **Fabric Health** as the report type.
3. Choose the target fabric from the drop-down and set the scope (all switches or selected switches).
4. Set the output format to **PDF** or **HTML** as required.
5. Click **Run Now** to generate immediately, or configure a schedule under **Schedule** tab for recurring reports.
6. Once complete, the report appears in **Monitor > Reports > Report History** — click **Download** to save.
7. Review the report sections: **Switch Health**, **Port Status** (CRC errors, sync loss), **Zone Consistency**, and **MAPS Alert Summary**.
8. Escalate any switches showing amber or red health status to the SAN team for investigation.

---

## Configure Alert Thresholds and Notifications

MAPS (Monitoring and Alerting Policy Suite) enforces threshold-based alerting on Brocade switches. SANnav centralises policy management.

1. Navigate to **Configure > MAPS > Policies** in SANnav and select the fabric.
2. Select the active MAPS policy applied to each switch (or create a new one by clicking **+ Add Policy**).
3. Review and edit threshold rules for key counters:
   - **CRC errors per port**: set alert threshold to `> 0` per 5-minute window.
   - **Signal loss (ITW)**: threshold `> 5` per 5-minute window.
   - **Port utilisation**: warning at 70%, critical at 85%.
4. Under **Actions**, configure the notification action for each alert level — select **Email** and enter the operations distribution list.
5. Optionally configure **SNMP Trap** to forward alerts to your monitoring platform (Zabbix, SolarWinds, etc.) by entering the trap receiver IP and community string.
6. Click **Apply** to push the policy to all switches in the fabric; SANnav executes `mapsPolicy --enable <policy_name>` on each switch.
7. Validate by checking **Monitor > MAPS > Alerts** — confirm test alerts appear within 5 minutes of a triggered condition.

---

## Generate a Performance Report

Performance reports capture port-level throughput, IOPS, and utilisation trends for capacity planning and troubleshooting.

1. In SANnav, go to **Monitor > Performance > Reports** and click **+ New Performance Report**.
2. Select the fabric and choose the scope: **All Ports**, **ISL Ports Only**, or a custom port group.
3. Set the time range — use **Last 7 Days** for trend analysis or **Custom** for a specific incident window.
4. Choose metrics to include: **Throughput (MB/s)**, **Frame Count**, **Error Count**, **BB Credit Zero**.
5. Click **Generate** — the report renders as a graph and table view in the browser.
6. Export to CSV for spreadsheet analysis: click **Export > CSV** from the report toolbar.
7. Identify ports exceeding 70% sustained utilisation — flag these for ISL expansion or load rebalancing.
8. Save the report to the shared team drive and reference it in the monthly capacity review.

---

## Export Fabric Topology Diagram

Topology diagrams are required for documentation, change management submissions, and incident post-mortems.

1. In SANnav, navigate to **SAN > Fabrics > [Fabric Name]** and open the **Topology** tab.
2. Wait for the topology to render fully — all switches and ISL links should be visible.
3. Use the **Layout** controls to arrange switches logically (e.g., core switches in the centre, edge switches around the perimeter).
4. Click **Actions > Export Topology** and select the output format: **PNG** (for documents) or **SVG** (for vector editing).
5. Set the export resolution — use **High** (300 dpi) for printed change submissions.
6. Save the exported file with a standardised name: `<fabric-name>_topology_<YYYYMMDD>.png`.
7. Attach the topology diagram to the relevant change ticket or network documentation page in Confluence/SharePoint.

---

## Upgrade SANnav Software

SANnav upgrades are performed in-place on the SANnav VM. Follow the vendor-supported upgrade path; do not skip major versions.

1. Download the SANnav upgrade package (`.bin` installer) from the Broadcom Support Portal and verify the SHA-256 checksum.
2. Take a snapshot of the SANnav VM in vCenter before starting — label it `sannav-pre-upgrade-<version>-<YYYYMMDD>`.
3. Log in to SANnav and navigate to **Administration > System > Software Update**.
4. Click **Upload Update Package** and select the downloaded `.bin` file.
5. Review the upgrade compatibility matrix displayed — confirm the current version to target version upgrade path is supported.
6. Click **Install** — the system will display a warning that SANnav will be unavailable during the upgrade (typically 15–30 minutes).
7. Monitor the upgrade via the SANnav console (if accessible) or wait for the web UI to return; log back in and confirm the version under **Administration > System > About**.
8. Verify fabric discovery is functioning: navigate to **SAN > Fabrics** and confirm all fabrics show **Connected** status.

---

## Backup SANnav Configuration and Database

Regular backups of the SANnav configuration and database protect against appliance failure and support rollback after an upgrade.

1. In SANnav, navigate to **Administration > System > Backup & Restore**.
2. Click **Backup Now** to trigger an immediate backup; set the backup destination to an NFS export (e.g., `nas01:/sannav-backups/`) configured under **Settings > Backup Location**.
3. Confirm the backup job completes and note the backup file name — format: `sannav_backup_<timestamp>.tar.gz`.
4. Copy the backup file to a secondary location (tape, object storage, or off-site NAS) for offsite retention.
5. Schedule recurring automated backups under the **Schedule** tab — configure daily at 02:00 local time with 30-day retention.
6. After any major configuration change (new fabric, zone update, firmware upload), trigger a manual backup immediately.
7. To verify backup integrity, restore to a test SANnav instance: **Administration > System > Backup & Restore > Restore** and point to the backup file.

---

```bash
# SSH to the affected switch
ssh admin@switch-ip

# List available MAPS policies
mapsPolicy --show

# Activate a MAPS policy
mapsPolicy --enable dflt_aggressive_policy

# Verify active policy
mapsPolicy --show
```text
┌─────────────────────────────── Brocade SANnav — Operations Procedures ────────────────────────────────┐
│                                                                                                       │
│  Day-to-day SANnav procedures: zone changes, switch adds, firmware, health monitoring.                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Zone Change Procedure             │  │             Switch Add / Remove             │   │
│   │         1. Create alias for HBA WWN          │  │          1. Add switch IP in SANnav         │   │
│   │         2. Add alias to target zone          │  │          2. Set SNMP v3 credentials         │   │
│   │         3. Add zone to active config         │  │          3. Discover: verify ports          │   │
│   │          4. Review diff before push          │  │           4. Configure MAPS policy          │   │
│   │            5. cfgsave + cfgenable            │  │           5. Verify firmware level          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Zone changes require change ticket; always review diff before activating config.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Firmware Management              │  │          Health Monitoring Routine          │   │
│   │         1. Upload FOS to SANnav repo         │  │           Daily: MAPS alert review          │   │
│   │        2. Validate against switch ver        │  │          Weekly: port error report          │   │
│   │          3. Schedule upgrade window          │  │          Monthly: utilisation trend         │   │
│   │         4. HA upgrade: standby first         │  │            Quarterly: zone audit            │   │
│   │        5. Verify version post-upgrade        │  │            Annual: SANnav upgrade           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SANnav VM · management network · Brocade FC switch chassis · SFP transceivers                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Alias           = named WWN or alias group; used as zone member instead of raw WWN                   │
│  Zone diff       = SANnav shows before/after view of zone changes before activating                   │
│  cfgsave/cfgenable= save and activate zone config; SANnav executes these on switches                  │
│  MAPS            = Monitoring and Alerting Policy Suite; daily alert review priority                  │
│  HA upgrade      = firmware activated on standby CP first; switchover then active                     │
│  FOS repo        = SANnav local repository for staging Fabric OS firmware images                      │
│  Port error report= weekly SANnav report on CRC/loss-of-sync per port                                 │
│  Zone audit      = quarterly review of all zones for unused aliases and orphaned WWNs                 │
│  Change ticket   = ITSM-required approval before any zone or fabric configuration change              │
│  WWN             = World Wide Name; 64-bit identifier for HBAs and switch ports                       │
│  Utilisation trend= monthly SANnav capacity report; identifies approaching saturation                 │
│  SNMP v3         = SNMPv3 credentials required for SANnav to discover and poll switches               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
