---
tags:
  - operations
  - san
---
# Cisco DCNM — Backup and Restore
![Cisco DCNM — Backup and Restore](../../../../assets/san-cisco-cisco-dcnm-operations-backup-restore.svg)

```bash
ssh root@dcnm-dc1.corp.example.com

# Full database dump (all DCNM databases)
pg_dumpall -U postgres -f /var/backup/dcnm/dcnm-db-$(date +%Y%m%d-%H%M).sql

# Compress the dump
gzip /var/backup/dcnm/dcnm-db-$(date +%Y%m%d-%H%M).sql

# Transfer to remote backup server
scp /var/backup/dcnm/dcnm-db-$(date +%Y%m%d-%H%M).sql.gz \
    bkp@backup-server.corp.example.com:/backups/dcnm/db/

# List backups
ls -lh /var/backup/dcnm/
```


```text title="Expected output"
root@dcnm-dc1:~# pg_dumpall -U postgres -f /var/backup/dcnm/dcnm-db-20240115-1430.sql
root@dcnm-dc1:~# gzip /var/backup/dcnm/dcnm-db-20240115-1430.sql
root@dcnm-dc1:~# scp /var/backup/dcnm/dcnm-db-20240115-1430.sql.gz \
>     bkp@backup-server.corp.example.com:/backups/dcnm/db/
dcnm-db-20240115-1430.sql.gz                100%  2847MB   45.2MB/s   01:03
root@dcnm-dc1:~# ls -lh /var/backup/dcnm/
total 5.6G
-rw-r--r-- 1 postgres postgres 2.8G Jan 15 14:30 dcnm-db-20240115-1430.sql.gz
-rw-r--r-- 1 postgres postgres 3.2G Jan 14 09:15 dcnm-db-20240114-0915.sql.gz
-rw-r--r-- 1 postgres postgres 2.9G Jan 13 22:45 dcnm-db-20240113-2245.sql.gz
```

!!! warning "Common errors"
    **`pg_dumpall: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory`** — Verify PostgreSQL is running with `systemctl status postgresql` and start it if needed.
    **`scp: /var/backup/dcnm/dcnm-db-20240115-1430.sql.gz: No such file or directory`** — Ensure the gzip command completed successfully and the backup directory exists with `mkdir -p /var/backup/dcnm/`.
    **`Permission denied (publickey,password).`** — Verify SSH key is configured for the `bkp` user on backup-server or add password authentication to the scp command.
```bash
# Key configuration directories
tar -czf /var/backup/dcnm/dcnm-config-$(date +%Y%m%d).tar.gz \
  /usr/local/cisco/dcm/dcnm/conf/ \
  /etc/ssl/dcnm/ \
  /var/dcnm/

scp /var/backup/dcnm/dcnm-config-$(date +%Y%m%d).tar.gz \
    bkp@backup-server.corp.example.com:/backups/dcnm/config/
```

```text title="Expected output"
tar: removing leading `/' from member names
/usr/local/cisco/dcm/dcnm/conf/
/etc/ssl/dcnm/
/var/dcnm/
dcnm-config-20240115.tar.gz

bkp@backup-server.corp.example.com's password: 
dcnm-config-20240115.tar.gz                    100%  245MB   18.2MB/s   00:13
```

!!! warning "Common errors"
    **`tar: /usr/local/cisco/dcm/dcnm/conf/: Cannot open: No such file or directory`** — Verify the DCNM installation path matches your environment with `ls -d /usr/local/cisco/dcm/dcnm/conf/` before running the backup.
    **`scp: /backups/dcnm/config/: No such file or directory`** — Create the destination directory on the backup server with `ssh bkp@backup-server.corp.example.com mkdir -p /backups/dcnm/config/` first.
    **`Permission denied (publickey,password).`** — Ensure SSH key-based authentication is configured for the `bkp` user or provide the correct password when prompted.
```bash
# Get auth cookie
curl -sk -c dcnm-cookie.txt -X POST \
  https://dcnm-dc1.corp.example.com/rest/logon \
  -H "Content-Type: application/json" \
  -d '{"expirationTime": 3600}' \
  -u "svc-automation:<password>"

# Export zone configuration for a fabric
curl -sk -b dcnm-cookie.txt \
  "https://dcnm-dc1.corp.example.com/rest/san/zoning?fabricName=DC1-FABRIC-A" \
  -o DC1-FABRIC-A-zones-$(date +%Y%m%d).json

curl -sk -b dcnm-cookie.txt -X POST \
  https://dcnm-dc1.corp.example.com/rest/logout
```

```text title="Expected output"
{"StatusCode":200,"StatusMessage":"Authentication successful","Reason":"User svc-automation authenticated"}
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2847  100  2847    0     0   8234      0 --:--:-- --:--:-- --:--:-- --:--:-- 100%
{"StatusCode":200,"StatusMessage":"Logout successful","Reason":"Session terminated"}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present; if error persists, verify DCNM hostname resolves correctly).
    **`{"StatusCode":401,"StatusMessage":"Authentication failed"}`** — Verify the svc-automation service account credentials and that the account has SAN zoning API permissions in DCNM.
    **`curl: (7) Failed to connect to dcnm-dc1.corp.example.com port 443: Connection refused`** — Confirm DCNM appliance is running and accessible on the network; check firewall rules and DNS resolution of the hostname.
```bash
ssh root@dcnm-dc1.corp.example.com

# Stop DCNM services first
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server stop

# Drop and recreate databases
psql -U postgres -c "DROP DATABASE IF EXISTS sane;"
psql -U postgres -c "CREATE DATABASE sane;"
psql -U postgres -c "DROP DATABASE IF EXISTS pmdb;"
psql -U postgres -c "CREATE DATABASE pmdb;"

# Restore from full dump
gunzip -c /var/backup/dcnm/dcnm-db-20260506-0200.sql.gz | psql -U postgres

# Start DCNM services
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server start

# Monitor startup
tail -f /var/log/dcnm/server.log
```


```text title="Expected output"
root@dcnm-dc1.corp.example.com's password: 
Stopping DCNM services...
DCNM Server stopped successfully.
DROP DATABASE
CREATE DATABASE
DROP DATABASE
CREATE DATABASE
SET
SET
CREATE SCHEMA
CREATE TABLE
CREATE TABLE
CREATE INDEX
CREATE INDEX
...
ALTER TABLE
(1247 rows affected)
Starting DCNM services...
DCNM Server started successfully. PID: 8742
2026-05-06 02:15:33 [INFO] DCNM Server initialization started
2026-05-06 02:15:45 [INFO] Loading fabric inventory from database
2026-05-06 02:15:52 [INFO] Initializing policy engine
2026-05-06 02:16:08 [INFO] DCNM Server ready to accept connections on port 8443
2026-05-06 02:16:12 [INFO] All services online
```

!!! warning "Common errors"
    **`psql: error: connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL: Ident authentication failed for user "postgres"`** — Run psql commands as the postgres system user or configure pg_hba.conf to allow password authentication.
    **`gunzip: /var/backup/dcnm/dcnm-db-20260506-0200.sql.gz: No such file or directory`** — Verify the backup file path and date match an existing dump in /var/backup/dcnm/ using `ls -lh /var/backup/dcnm/`.
    **`ERROR: database "sane" is being accessed by other users`** — Ensure all DCNM services and client connections are fully stopped before dropping databases, or use `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='sane';` first.
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

- [Cisco Dcnm — Procedures](../procedures/)
- [Cisco Dcnm — Health Checks](../health-checks/)
- [Cisco Dcnm — Common Issues](../../troubleshooting/common-issues/)
