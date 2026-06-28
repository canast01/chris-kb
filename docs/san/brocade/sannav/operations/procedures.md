---
tags:
  - operations
  - san
---
# Brocade SANnav — Operations Procedures

SANnav Management Portal is the Brocade web-based tool for SAN fabric discovery, zoning, health monitoring, firmware management, and reporting across Brocade FC switch fabrics.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

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

## Add a Fabric to SANnav

Registering a new fabric allows SANnav to discover, monitor, and manage all switches in that fabric from a single pane of glass.

1. Log in to SANnav and navigate to **Fabric Management > Add Fabric**.
2. Enter the seed switch IP address (principal switch for the target fabric).
3. Provide SNMPv3 credentials (auth and priv) and SSH credentials for the seed switch.
4. Click **Discover** to initiate fabric discovery.
5. Wait for the topology view to populate — progress is shown in **Monitor > Jobs > Fabric Discovery**.
6. Confirm all expected switches appear and ISL links are green before saving.

---

## Discover or Rediscover Switches in a Fabric

Use this when new switches are added to an existing fabric or when SANnav shows stale or missing topology data.

1. In SANnav, navigate to **SAN > Fabrics** and select the relevant fabric.
2. Click **Actions > Discover** (for a new fabric) or **Actions > Rediscover** (for an existing fabric).
3. Wait for the discovery job to complete.
4. Navigate to **SAN > Fabrics > [Fabric Name] > Switches** and verify all switches appear in the topology.
5. Investigate any switch that remains in **Unmanaged** state — common causes are credential mismatch, firewall blocking SSH/SNMP, or unreachable management IP.

---

## Generate a Fabric Health Report

Use this for routine health reviews or before planned changes to establish a baseline.

1. In SANnav, navigate to **Reports > Fabric Health**.
2. Select the target fabric and set the time range (e.g., last 7 days).
3. Click **Generate**.
4. Review the report for port errors (CRC, loss-of-sync), ISL utilisation percentages, and any offline ports.
5. Export as PDF for change record attachment or CSV for trend analysis.

---

## Configure MAPS Alert Thresholds and Email Notifications

MAPS (Monitoring and Alerting Policy Suite) drives proactive alerting on port errors, BB credit starvation, and ISL saturation.

1. In SANnav, navigate to **Monitoring > MAPS Policies**.
2. Select the active policy for the target fabric (e.g., `dflt_aggressive_policy`).
3. Adjust thresholds for port errors, BB credits, and ISL utilisation to match site standards.
4. Navigate to **Notifications** within the policy and configure the SMTP relay (host, port, sender address) and recipient list.
5. Click **Test Alert** to confirm email delivery.
6. Save and apply the updated policy to the fabric.

---

## Generate a Performance Report

Use this to identify throughput bottlenecks, IOPS hotspots, or latency outliers across the fabric.

1. In SANnav, navigate to **Reports > Performance**.
2. Select the switches or individual ports to include in the report.
3. Set the metric to report on: port throughput (MB/s), IOPS, or latency (ms).
4. Set the time range for the report.
5. Click **Generate**.
6. Review peak vs. average values — sustained peak throughput approaching port speed indicates saturation.
7. Export the report as CSV for trend tracking or PDF for stakeholder review.

---

## Export Fabric Topology Diagram

Use this to produce an up-to-date fabric topology diagram for documentation, change records, or incident review.

1. In SANnav, navigate to **Topology** and select the target fabric.
2. Click **Export**.
3. Choose the output format: **PNG** for document embedding or **SVG** for scalable diagrams.
4. Save the exported file and attach to the relevant documentation or change record.

---

## Upgrade SANnav Software

Upgrade SANnav during a scheduled maintenance window — fabric management is unavailable while the upgrade applies.

1. In SANnav, navigate to **Administration > Software Management**.
2. Click **Check for Updates** to retrieve available upgrade bundles from the Brocade update server.
3. Download the upgrade bundle (or upload a locally downloaded bundle if the SANnav VM has no internet access).
4. Schedule the upgrade for an approved maintenance window and notify stakeholders.
5. Apply the upgrade — SANnav services will restart automatically.
6. Verify all SANnav services have resumed: check **Administration > System Status**.
7. Confirm all fabrics have reconnected and topology data is current in **SAN > Fabrics**.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Sannav — Health Checks](../health-checks/)
- [Sannav — CLI Reference](../cli-reference/)
- [Sannav — Common Issues](../../troubleshooting/common-issues/)
