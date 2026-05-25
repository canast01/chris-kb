# Cisco DCNM — Common Issues

> Part of the [Cisco DCNM](../../index.md) reference.

---

## Switch Shows as Unmanageable

**Symptom:** Switch in **SAN > Fabrics** shows state **Unmanageable** or **Unknown**.

**Diagnosis and resolution:**

```bash
# Step 1: Test SSH from DCNM to the switch
ssh -o ConnectTimeout=5 -o BatchMode=yes dcnm_mgmt@<switch-ip> 'show version' 2>&1
# If fails: SSH connectivity problem

# Step 2: Test SNMP
snmpget -v3 -u dcnm_poll -l authPriv -a SHA -A <auth-pass> \
  -x AES -X <priv-pass> <switch-ip> sysDescr.0
# If fails: SNMP credentials mismatch or network issue

# Step 3: Check DCNM discovery log
grep "<switch-ip>" /var/log/dcnm/discovery.log | tail -30
```

| Cause | Fix |
|---|---|
| SSH credentials incorrect or changed | Update switch credentials in **SAN > Fabrics > Edit Credentials** |
| SNMP v3 credentials mismatch | Update SNMP credentials in DCNM fabric settings |
| SSH service disabled on switch | `feature ssh` on the switch |
| Switch IP changed | Update switch IP in DCNM inventory |
| ACL blocking DCNM on switch | Remove or modify mgmt ACL on the switch to permit DCNM IP |

---

## Zone Activation Fails

**Symptom:** Zone set activation from DCNM returns an error or zone configuration does not propagate to all switches.

```bash
# On the principal switch of the fabric (NX-OS CLI)
show zone status vsan <vsan-id>
# Check: Mode, Default-zone, Merge Status

# Check for merge conflicts
show zone merge-failure vsan <vsan-id>

# If merge failure: identify the switch with conflicting zone DB
show zoneset active vsan <vsan-id>
# Compare against expected from DCNM
```

**Resolution for merge conflict:**
1. Identify the switch with the conflicting zone database.
2. If the DCNM zone set is the source of truth, clear the zone database on the conflicting switch and let DCNM re-push:

```bash
# On the conflicting switch — CAUTION: this clears all zones on this switch for the VSAN
no zoneset distribute full vsan <vsan-id>
zoneset activate name <zoneset-name> vsan <vsan-id>
# Then trigger re-push from DCNM: SAN > Zoning > Deploy
```

**Resolution for DCNM permission error:**
- Verify the `dcnm_mgmt` account has `network-admin` role on the switch: `show user-account | grep dcnm_mgmt`

---

## Performance Manager Not Collecting Data

**Symptom:** Graphs under **Monitor > Performance** show "No Data" or data is stale (> 10 minutes old).

```bash
# Check PM service status
systemctl status dcnm-pm

# Check PM log for polling errors
tail -f /var/log/dcnm/pm.log | grep -i "error\|timeout\|failed"

# Restart PM service
systemctl restart dcnm-pm

# Verify SNMP polling is working manually
snmpwalk -v3 -u dcnm_poll -l authPriv -a SHA -A <auth-pass> \
  -x AES -X <priv-pass> <switch-ip> ifInOctets
# Expected: output with interface counter values
```

Common PM issues:

| Cause | Fix |
|---|---|
| SNMP credentials changed | Update in DCNM fabric settings |
| Switch ACL blocking SNMP from DCNM | Add DCNM IP to switch SNMP ACL |
| PM database full | Reduce retention period; increase disk |
| PM service crashed | `systemctl restart dcnm-pm` |

---

## LDAP Authentication Failing

**Symptom:** Users cannot log in with AD credentials.

```bash
# Test LDAP from DCNM appliance
ldapsearch -H ldaps://ldap.corp.example.com \
  -D "CN=dcnm-svc,OU=Service Accounts,DC=corp,DC=example,DC=com" \
  -w <password> \
  -b "DC=corp,DC=example,DC=com" \
  "(sAMAccountName=<test-user>)"
```

| Error | Cause | Fix |
|---|---|---|
| `Connection refused` | Port 636 blocked | Open firewall from DCNM to LDAP server |
| `Invalid credentials (49)` | Wrong bind password | Update bind DN password in DCNM LDAP settings |
| `No such object (32)` | Wrong base DN or user OU | Verify base DN and user search base |
| SSL handshake failure | CA cert not trusted | Import CA into DCNM Java truststore |
| Role not assigned | AD group not mapped | Add group to DCNM role mapping |

---

## DCNM GUI Very Slow

**Symptom:** Pages take 30+ seconds to load; sometimes timeout.

```bash
# Check resource usage
top -b -n 1 | head -20
free -h

# Check disk I/O
iostat -x 1 5

# Check database connections
psql -U postgres -c "SELECT count(*) FROM pg_stat_activity WHERE state='active';"
# If > 50 active connections: connection pool exhaustion

# Check for runaway queries
psql -U postgres -c "
SELECT pid, now() - query_start AS duration, query 
FROM pg_stat_activity 
WHERE state = 'active' 
ORDER BY duration DESC 
LIMIT 10;"

# Restart DCNM if Java memory leak suspected
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server restart
```

If disk is > 80% full: clear PM historical data under **Administration > Settings > Data Retention**.

---

## SNMP Traps Not Received

**Symptom:** Events appear delayed; DCNM does not reflect near-real-time switch state changes.

```bash
# Capture to confirm traps are arriving
sudo tcpdump -i eth0 -n udp port 162 -c 20

# If not arriving: confirm trap destination on the switch
# On MDS switch:
show snmp host
# Should list DCNM IP

# If arriving but not processed: check event manager
tail -f /var/log/dcnm/events.log | grep "trap\|SNMP"

# Restart event service
systemctl restart dcnm-events
```

---

## Upgrade Fails or Leaves DCNM Non-Functional

**Symptom:** DCNM upgrade returns an error mid-way; UI does not come back after upgrade.

```bash
# Check upgrade log
tail -100 /var/log/dcnm/install.log

# Check if DCNM services started after upgrade
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server status

# Check for database migration errors (common cause of upgrade failure)
grep -i "liquibase\|migration\|flyway\|ERROR" /var/log/dcnm/install.log

# If upgrade is unrecoverable: revert to pre-upgrade VM snapshot
# Then contact Cisco TAC with the install log
```
