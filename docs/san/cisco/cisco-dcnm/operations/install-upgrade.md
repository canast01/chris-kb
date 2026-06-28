---
tags:
  - operations
  - san
---
# Cisco DCNM — Install and Upgrade
![Cisco DCNM — Install and Upgrade](../../../../assets/san-cisco-cisco-dcnm-operations-install-upgrade.svg)


```bash
# On the primary (active) DCNM node
ssh root@dcnm-dc1-active.corp.example.com

# Run HA setup utility
/usr/local/cisco/dcm/dcnm/bin/dcnm-ha-setup.sh \
  --primary \
  --vip 10.10.5.15 \
  --peer 10.10.5.11 \
  --password <ha-password>

# On the secondary (standby) node
ssh root@dcnm-dc1-standby.corp.example.com

/usr/local/cisco/dcm/dcnm/bin/dcnm-ha-setup.sh \
  --secondary \
  --vip 10.10.5.15 \
  --peer 10.10.5.10 \
  --password <ha-password>

# Verify HA status from active node
/usr/local/cisco/dcm/dcnm/bin/dcnm-ha-status.sh
# Expected: ACTIVE/STANDBY pair, VIP reachable
```

```bash
# On each MDS switch
no snmp-server host <dcnm-ip> traps version 3 priv dcnm_poll

# Remove syslog forwarding to DCNM
no logging server <dcnm-ip>

# Remove DCNM service account
no username dcnm_mgmt
```

```d2
direction: right

hub: "Cisco DCNM\nOperations" {shape: hexagon}
verify: "Verify" {shape: rectangle}

hub -> verify
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Cisco Dcnm — Procedures](procedures/)
- [Cisco Dcnm — Health Checks](health-checks/)
- [Cisco Dcnm — Deploy](../deploy/)
