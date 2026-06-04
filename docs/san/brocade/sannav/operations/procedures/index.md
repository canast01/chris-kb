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
