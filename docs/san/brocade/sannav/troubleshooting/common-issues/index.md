# SANnav — Common Issues

> Part of the [SANnav](../../) reference.

---

## Switch Shows as Unreachable

**Symptom:** A switch in the SANnav inventory shows **Unreachable** or **Unknown** connectivity state.

**Causes and resolution:**

| Cause | Check | Fix |
|---|---|---|
| Switch management IP unreachable | `ping <switch-ip>` from SANnav appliance | Fix routing / firewall between SANnav and switch mgmt VRF |
| HTTPS credentials changed on switch | Test connection in SANnav **Discovery > Switches** | Update credentials in SANnav |
| HTTPS service disabled on switch | `firmwareshow` / check switch web access | Enable: `httpscfg --set -protocol https` on switch |
| SANnav discovery engine hung | Check `/opt/sannav/logs/discovery.log` for stuck threads | `sannav restart` |
| IP address changed on switch | Switch responds on new IP, old IP unreachable | Edit switch IP in **Discovery > Switches** |
| Certificate mismatch | HTTPS connect fails with TLS error in discovery log | Accept or re-trust the switch certificate in SANnav |

---

## SNMP Traps Not Being Received

**Symptom:** Events appear delayed or absent; SANnav does not react to link events in real time.

**Resolution:**

```bash
# Step 1: Confirm SANnav IP is the trap destination on the switch (FOS CLI)
snmpconfig --show trapdest
# Should list SANnav management IP on port 162

# Step 2: Confirm UDP 162 is not blocked between switch and SANnav
# From a host with tcpdump on the SANnav management network:
sudo tcpdump -i eth0 -n udp port 162

# Trigger a test trap from the switch
snmptraps --send 1  # sends a test trap

# Step 3: Confirm SANnav event engine is processing traps
tail -f /opt/sannav/logs/event-engine.log | grep "trap\|SNMP"

# Step 4: If traps arrive but are discarded, check community/credential mismatch
# Ensure SNMPv3 credentials on switch match what SANnav has configured
```

---

## Zone Activation Fails

**Symptom:** Zone set activation from SANnav UI returns an error or the zone set does not propagate to all switches in the fabric.

**Resolution:**

1. Navigate to **Zoning > Zone Status** and check if any switch in the fabric shows a zone merge conflict.
2. SSH to the principal switch of the affected fabric:

```bash
# Check zone merge status
cfgshow          # displays defined and active zone sets
zoneshow         # zone membership

# Check for merge conflict
fabricshow       # confirm all switches are in the same fabric and principal

# If merge conflict exists, check conflicting zone databases
# Isolate the switch with the conflicting DB and clear/re-sync:
cfgclear         # CAUTION: clears the zone database on the switch — confirm before running
cfgsave
# Then push the correct zone set from SANnav
```

3. Confirm the SANnav service account (`sannav_svc`) has the **admin** role on the switch — zoning operations require admin privileges.

---

## SANnav GUI Slow or Unresponsive

**Symptom:** The SANnav web UI takes > 30 seconds to load pages; sessions time out frequently.

**Resolution:**

```bash
ssh admin@sannav-dc1.corp.example.com

# Check CPU and memory
top -b -n 1 | head -20
free -h

# Check disk I/O
iostat -x 1 5

# Check disk space — PostgreSQL growth is the most common cause
df -h /opt/sannav
du -sh /opt/sannav/data/postgres/
du -sh /opt/sannav/data/influxdb/

# Check for slow queries in PostgreSQL
sudo -u postgres psql -c "SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"

# Restart services if memory leak is suspected
sannav restart
```

If disk is > 85% full: purge old performance data. Navigate to **Administration > System > Data Retention** and reduce the retention period for historical data.

---

## LDAP Authentication Fails

**Symptom:** Users cannot log in with AD credentials; login page shows "Invalid credentials" or "LDAP error."

**Resolution:**

```bash
# Test LDAP connectivity from SANnav appliance
openssl s_client -connect ldap.corp.example.com:636 -brief
# Expected: CONNECTED with no certificate errors

# Test bind with the service account
ldapsearch -H ldaps://ldap.corp.example.com \
  -D "CN=sannav-svc,OU=Service Accounts,DC=corp,DC=example,DC=com" \
  -w <bind-password> \
  -b "DC=corp,DC=example,DC=com" \
  "(sAMAccountName=testuser)" sAMAccountName mail
# Expected: returns the test user's attributes
```

Common LDAP issues:

| Error | Cause | Fix |
|---|---|---|
| `LDAP: error code 49` | Wrong bind password | Update bind DN password in SANnav LDAP settings |
| `LDAP: error code 32` | User not found in search base | Verify user OU matches search base configuration |
| SSL handshake failure | CA cert not trusted | Import CA certificate into SANnav JRE truststore |
| Connection timeout | Firewall blocking port 636 | Open port 636 from SANnav to LDAP server |

---

## Firmware Upgrade Stuck or Failed

**Symptom:** A firmware upgrade initiated from SANnav shows **In Progress** for more than 30 minutes, or shows **Failed**.

**Resolution:**

1. Navigate to **Image Management > Upgrade Status** and note the error message.
2. SSH to the switch and check FOS firmware download status:

```bash
# On the switch (FOS CLI)
firmwareshow
# Shows current and backup partition firmware

# If the switch is in firmware download state, check progress:
firmwaredownload --status

# If upgrade is stuck, check system logs on the switch
errdump
```

3. If the switch rebooted and SANnav shows it as failed, the switch may be on the new firmware and healthy:

```bash
# Verify switch firmware from SANnav after reconnect
# Inventory > Switches > [Switch] > Details
# If firmware matches target, mark the upgrade as complete in SANnav
```

4. Common failure causes:

| Cause | Fix |
|---|---|
| Insufficient disk space on switch | Clean up `/var` on switch: `firmwareshow -s` to check |
| Network interruption during download | Retry the upgrade; SANnav will resume from the checkpoint |
| Incompatible firmware for hardware | Verify hardware generation support matrix |
| Switch in ISL-only mode | Upgrade from FOS CLI directly: `firmwaredownload` |

---

## Backup Failing to Remote Target

**Symptom:** Scheduled or manual backups fail with a remote transfer error.

**Resolution:**

```bash
# Test SCP connectivity from SANnav to backup server
ssh admin@sannav-dc1.corp.example.com
scp /tmp/testfile.txt sannav-bkp@backup-server.corp.example.com:/backups/sannav/
# If this fails, investigate:
# - SSH key or password authentication to backup server
# - Firewall between SANnav and backup server (TCP 22)
# - Write permissions on the remote backup directory

# Check SANnav backup logs
grep -i "backup\|transfer\|ERROR" /opt/sannav/logs/server.log | tail -50
```

If remote transfer is configured via NFS, verify NFS mount is active:
```bash
df -h | grep backup
# If not mounted: sudo mount -a
```
