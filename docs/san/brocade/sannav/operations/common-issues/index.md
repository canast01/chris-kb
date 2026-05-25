# SANnav — Operations Common Issues

```
┌─────────────────────────────────────── SANnav — Common Issues ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              Common SANnav operational issues with diagnosis and resolution paths             │   │
│   │     Discovery failures: unreachable switch, wrong credentials, SNMP not enabled on switch     │   │
│   │      Login issues: LDAP misconfiguration, session timeout, certificate expired on SANnav      │   │
│   │     Stale inventory: switch not re-polled after config change; trigger manual re-discovery    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Discovery issues → login/auth issues → inventory staleness → alert volume issues                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Discovery          │  │         Auth / Login        │  │          Inventory          │   │
│   │      Switch unreachable     │  │      LDAP config error      │  │        Stale topology       │   │
│   │       Wrong SSH creds       │  │       Session timeout       │  │        Missing ports        │   │
│   │        SNMP disabled        │  │         Cert expired        │  │        Old zone data        │   │
│   │       FW incompatible       │  │       Password locked       │  │         Counter gap         │   │
│   │        TCP 22 blocked       │  │           SSO fail          │  │         Alert storm         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Escalate to SANnav logs at /var/log/sannav/ and Brocade TAC if issue persists                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issue       │     Symptom      │     Root cause    │    Resolution    │    Prevention    │   │
│   │  Discovery fail  │  Switch offline  │    SSH blocked    │   Check TCP 22   │  Firewall rule   │   │
│   │    Stale data    │ Old zones shown  │   Poll interval   │Manual rediscover │   Shorten poll   │   │
│   │   Alert storm    │ Hundreds alerts  │   Threshold low   │ Tune thresholds  │  Baseline first  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: network path SANnav → switch management port; SNMP UDP 161 must be open                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Discovery fail = SANnav cannot reach or authenticate to a switch; shows as offline in UI           │
│    SNMP v3       = SANnav uses SNMPv3 for trap reception; must be enabled on each switch              │
│    Stale topo    = SANnav topology not updated after a switch change; trigger re-discovery            │
│    Manual rediscover = SANnav UI action to force immediate poll of a switch or fabric                 │
│    Alert storm   = Flood of threshold alerts; caused by misconfigured thresholds or port flap         │
│    Threshold tune = Adjust alert trigger values to match expected baseline traffic levels             │
│    Cert expired  = SANnav HTTPS cert; renew via admin console; causes browser login failure           │
│    LDAP config   = SANnav LDAP settings; test with known user before saving changes                   │
│    SSH creds     = Per-switch admin username/password stored in SANnav credential store               │
│    Poll interval = Frequency SANnav polls switches for counters and state; default 5 minutes          │
│    FW compat     = SANnav has minimum FabricOS version requirements per switch model                  │
│    Log location  = /var/log/sannav/ on SANnav VM; review sannav.log and discovery.log                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────── SANnav — Common Issues ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              Common SANnav operational issues with diagnosis and resolution paths             │   │
│   │     Discovery failures: unreachable switch, wrong credentials, SNMP not enabled on switch     │   │
│   │      Login issues: LDAP misconfiguration, session timeout, certificate expired on SANnav      │   │
│   │     Stale inventory: switch not re-polled after config change; trigger manual re-discovery    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Discovery issues → login/auth issues → inventory staleness → alert volume issues                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Discovery          │  │         Auth / Login        │  │          Inventory          │   │
│   │      Switch unreachable     │  │      LDAP config error      │  │        Stale topology       │   │
│   │       Wrong SSH creds       │  │       Session timeout       │  │        Missing ports        │   │
│   │        SNMP disabled        │  │         Cert expired        │  │        Old zone data        │   │
│   │       FW incompatible       │  │       Password locked       │  │         Counter gap         │   │
│   │        TCP 22 blocked       │  │           SSO fail          │  │         Alert storm         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Escalate to SANnav logs at /var/log/sannav/ and Brocade TAC if issue persists                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issue       │     Symptom      │     Root cause    │    Resolution    │    Prevention    │   │
│   │  Discovery fail  │  Switch offline  │    SSH blocked    │   Check TCP 22   │  Firewall rule   │   │
│   │    Stale data    │ Old zones shown  │   Poll interval   │Manual rediscover │   Shorten poll   │   │
│   │   Alert storm    │ Hundreds alerts  │   Threshold low   │ Tune thresholds  │  Baseline first  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: network path SANnav → switch management port; SNMP UDP 161 must be open                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Discovery fail = SANnav cannot reach or authenticate to a switch; shows as offline in UI           │
│    SNMP v3       = SANnav uses SNMPv3 for trap reception; must be enabled on each switch              │
│    Stale topo    = SANnav topology not updated after a switch change; trigger re-discovery            │
│    Manual rediscover = SANnav UI action to force immediate poll of a switch or fabric                 │
│    Alert storm   = Flood of threshold alerts; caused by misconfigured thresholds or port flap         │
│    Threshold tune = Adjust alert trigger values to match expected baseline traffic levels             │
│    Cert expired  = SANnav HTTPS cert; renew via admin console; causes browser login failure           │
│    LDAP config   = SANnav LDAP settings; test with known user before saving changes                   │
│    SSH creds     = Per-switch admin username/password stored in SANnav credential store               │
│    Poll interval = Frequency SANnav polls switches for counters and state; default 5 minutes          │
│    FW compat     = SANnav has minimum FabricOS version requirements per switch model                  │
│    Log location  = /var/log/sannav/ on SANnav VM; review sannav.log and discovery.log                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [SANnav](../../index.md) reference. For deeper diagnosis, see [Troubleshooting > Common Issues](../../troubleshooting/common-issues/index.md).

---

## Overview

This page is a quick-reference for operational issues encountered during day-to-day SANnav management tasks: switch discovery, zoning, firmware upgrades, alert handling, and backup operations.

---

## Switch Not Appearing After Discovery

**Symptom:** After adding a switch via **Discovery > Add Switch**, the switch does not appear in the fabric dashboard or shows in **Unknown** state.

**Checklist:**

1. **HTTPS reachable?** — From the SANnav appliance, test:
   ```bash
   curl -sk -o /dev/null -w "%{http_code}" https://<switch-ip>/rest/loginresult
   # Expected: 200 or 401; anything else = network/firewall issue
   ```
2. **Credentials correct?** — Navigate to **Discovery > Switches**, select the switch, and click **Test Connection**. Both HTTPS and SNMP tests must pass.
3. **Switch in correct resource group?** — Switches left in the default resource group may not be visible to role-scoped users. Assign it to the correct fabric under **Discovery > Switches > Assign to Fabric**.
4. **Discovery engine running?** — Check:
   ```bash
   grep "unreachable\|refused\|timeout" /opt/sannav/logs/discovery.log | tail -20
   ```

---

## Zone Change Does Not Take Effect

**Symptom:** A zone set was activated in SANnav but the host cannot see the new storage LUN, or the SANnav UI shows the previous zone set as still active.

**Resolution:**

1. Navigate to **Zoning > Zone Status** and confirm the zone set timestamp updated.
2. If the timestamp did not change, check for zone merge conflicts:
   - SANnav will report a conflict if two switches in the fabric have differing zone databases.
   - Navigate to **Events > Active Alerts** — a zone merge conflict generates a Critical alert.
3. Confirm the SANnav service account has the `admin` role on the principal switch:
   ```bash
   # On the principal switch (FOS CLI)
   userconfig --show sannav_svc
   # Role must be: admin
   ```
4. Force a zone re-sync from SANnav: **Zoning > [Fabric] > Actions > Re-Sync Zone Database**.
5. On the host side, trigger a storage rescan after confirming zone activation.

---

## Firmware Upgrade Reported as Complete but Switch Still on Old Version

**Symptom:** The Image Management upgrade job shows **Completed** but the switch firmware version in SANnav inventory still shows the old version.

**Cause:** The upgrade may have downloaded successfully but the switch has not activated yet (manual activation mode was set), or SANnav inventory cache has not refreshed.

**Resolution:**

1. Check activation mode: navigate to **Image Management > Upgrade Status** and look at the activation column. If **Pending Activation**, the switch is waiting for a manual activation window.
2. Activate manually: select the switch and click **Activate**.
3. If activation already completed but SANnav still shows the old version: force an inventory refresh:
   ```bash
   # REST API — trigger switch re-poll
   TOKEN=$(curl -sk -X POST https://sannav-dc1.corp.example.com/rest/login \
     -H "Content-Type: application/json" \
     -d '{"credentials":{"loginName":"admin","password":"<pass>"}}' \
     | python3 -c "import sys,json; print(json.load(sys.stdin)['authToken'])")
   curl -sk -X POST "https://sannav-dc1.corp.example.com/rest/resourcegroups/all/switches/<switchId>/rediscover" \
     -H "Authorization: Bearer $TOKEN"
   ```
4. Verify on the switch directly: `firmwareshow` — if the active partition shows the new version, the upgrade was successful and SANnav will catch up on next poll.

---

## Alert Emails Not Being Received

**Symptom:** Expected email alerts for Critical events are not arriving at the configured recipients.

**Resolution:**

1. Navigate to **Administration > Server Settings > SMTP** and click **Test Email**. If the test email does not arrive:
   - Check SMTP server, port, authentication, and From address
   - Verify SANnav can reach the SMTP relay (port 25 or 587): `telnet smtp.corp.example.com 587`
   - Check for SMTP relay firewall rules blocking the SANnav management IP

2. If the test email arrives but alert emails do not:
   - Navigate to **Administration > Alert Policies > Forwarding Rules** — confirm the rule severity and recipient are correct
   - Confirm the events that should trigger alerts match the configured severity filters

3. Check for bounce or relay rejection in the SMTP relay logs.

4. Check SANnav event engine log for mail delivery errors:
   ```bash
   grep -i "smtp\|mail\|email" /opt/sannav/logs/event-engine.log | tail -30
   ```

---

## Scheduled Backup Not Running

**Symptom:** The backup history shows no recent backup; the last successful backup is older than expected.

**Resolution:**

1. Navigate to **Administration > Backup > History** and check for failed backup jobs and error messages.
2. If the remote SCP/SFTP target is failing, test from the SANnav appliance:
   ```bash
   scp /tmp/testfile sannav-bkp@backup-server.corp.example.com:/backups/sannav/
   # If this fails: check SSH keys, credentials, and write permissions on target
   ```
3. Check disk space on the SANnav appliance — backup requires temporary local space:
   ```bash
   df -h /opt/sannav
   # If > 90% full, the backup process cannot write the temporary archive
   ```
4. Check the backup log:
   ```bash
   grep -i "backup\|error\|failed" /opt/sannav/logs/server.log | tail -50
   ```
5. Run a manual backup to confirm the issue: **Administration > Backup > Backup Now**.

---

## SAN Analytics Data Missing or Stale

**Symptom:** The SAN Analytics performance dashboard shows no data or data that is several hours old.

**Cause and Resolution:**

| Cause | Check | Fix |
|---|---|---|
| SAN Analytics license not applied on switch | `sanAnalyticsShow` on switch | Apply SAN Analytics license to the switch |
| NTP drift between switch and SANnav | `timedatectl status` on SANnav | Sync NTP on both SANnav and switch |
| InfluxDB disk full | `du -sh /opt/sannav/data/influxdb/` | Reduce retention or expand disk |
| InfluxDB not healthy | `curl -sk http://localhost:8086/health` | `sannav restart` |
| SAN Analytics feature not enabled on switch | `sanAnalyticsShow` | Enable via FOS: `sananalytics --enable` |

---

## SANnav Certificate Warning in Browser

**Symptom:** Browsers show a TLS certificate warning when accessing the SANnav UI.

**Resolution:**

1. The default SANnav deployment uses a self-signed certificate. Replace it with a corporate CA certificate — see [Security > Authentication](../../security/authentication/index.md) for the full procedure.
2. If a CA certificate is already installed but the warning persists, check the certificate chain:
   ```bash
   openssl s_client -connect sannav-dc1.corp.example.com:443 \
     -servername sannav-dc1.corp.example.com </dev/null 2>/dev/null \
     | openssl x509 -noout -subject -issuer -dates
   ```
   - Confirm the subject CN matches the hostname in the URL
   - Confirm the issuer is a CA trusted by browsers (corporate CA must be in the browser trust store)
3. If the certificate is expired: renew it using the same procedure as initial installation.
