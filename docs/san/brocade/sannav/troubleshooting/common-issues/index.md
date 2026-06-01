# SANnav — Common Issues


<div class="kb-summary">
> Part of the [SANnav](../../index.md) reference.
</div>

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
┌─────────────────────────── Brocade SANnav — Troubleshooting Common Issues ────────────────────────────┐
│                                                                                                       │
│  Common SANnav issues: switch unreachable, zone push fail, auth error, stale data, UI slow.           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Switch Connectivity Issues          │  │            Zone Management Issues           │   │
│   │        Switch unreachable: ping test         │  │           Zone push fail: FOS auth          │   │
│   │         SNMP poll fail: check creds          │  │         Conflict: out-of-band change        │   │
│   │         Wrong mgmt IP: re-add switch         │  │           Stale zone: re-discover           │   │
│   │         Discovery timeout: increase          │  │        Zone diff: confirm before push       │   │
│   │           FOS version unsupported            │  │        Config lock: cfgdisable first        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Switch connectivity must be verified first; zone failures often trace to FOS auth.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Auth & Login Issues              │  │           Performance & UI Issues           │   │
│   │        TACACS+ timeout: check server         │  │         UI slow: browser cache clear        │   │
│   │         LDAP bind fail: verify creds         │  │         Elasticsearch overload: disk        │   │
│   │           Token expired: re-login            │  │         DB size: run prune old data         │   │
│   │         Local fallback: TACACS+ down         │  │           Sannav service: restart           │   │
│   │        Audit log: check failed logins        │  │          Log: journalctl -u sannav          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SANnav VM · management network · TACACS+ server · Brocade FC switches                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SNMP poll       = SANnav polls switches every 5 minutes; fail = switch shows red                     │
│  FOS auth        = SANnav stores per-switch FOS login credentials for zone push                       │
│  Out-of-band change= zone change made directly on switch bypassing SANnav                             │
│  Config lock     = FOS zone config locked if another session is editing                               │
│  Re-discover     = SANnav re-polls switch to refresh stale topology and zone data                     │
│  TACACS+ timeout = SANnav login fails if TACACS+ server unreachable; uses local                       │
│  LDAP bind       = service account bind to AD; check password expiry                                  │
│  JWT token       = expires after configured period; re-login to get new token                         │
│  Elasticsearch   = performance data store; disk full causes SANnav UI slowness                        │
│  Prune old data  = sannav-admin command to remove old perf data and free disk                         │
│  journalctl      = Linux systemd log; check for SANnav service errors and restarts                    │
│  Config diff     = SANnav compares its zone db to switch; shows out-of-band changes                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
