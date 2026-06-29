---
tags:
  - aria-networks
  - operations
  - vmware
---
# vRNI Backup & Restore
![vRNI Backup & Restore](../../../../assets/virtualization-vmware-aria-operations-for-networks-operation.svg)

```bash
PLATFORM="https://aon.example.local"
TOKEN=$(curl -sk -X POST "${PLATFORM}/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"PASSWORD"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
echo "Token: $TOKEN"
```


```text title="Expected output"
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBsb2NhbCIsImlhdCI6MTcwNDExMjM0NSwiZXhwIjoxNzA0MTE1OTQ1fQ.K2xY9pQmZ_vN8aB3cD4eF5gH6iJ7kL0mN1oP2qR3sT4
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to curl to skip SSL verification (already present in the example, but ensure it's not removed).
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Verify the platform URL is correct and the authentication service is responding; check credentials and ensure the API endpoint `/api/ni/auth/token` is accessible.
    **`command not found: python3`** — Install Python 3 or replace `python3` with `python` if only Python 2 is available on the system.
```bash
# crontab entry — runs daily at 02:00
0 2 * * * /usr/local/bin/aon-backup.sh >> /var/log/aon-backup.log 2>&1
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`command not found: /usr/local/bin/aon-backup.sh`** — Verify the backup script exists at the specified path and is executable with `ls -la /usr/local/bin/aon-backup.sh && chmod +x /usr/local/bin/aon-backup.sh`.
    **`Permission denied`** — Ensure the crontab user (typically root or aria-ops service account) has execute permissions on the script and read/write access to `/var/log/aon-backup.log`.
```bash
PLATFORM="https://aon-new.example.local"
TOKEN=$(curl -sk -X POST "${PLATFORM}/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"NEWPASSWORD"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk -X POST "${PLATFORM}/api/ni/settings/restore" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  -F "file=@/path/to/aon-backup-20260101-020001.tar.gz" \
  -o /tmp/restore-response.json

cat /tmp/restore-response.json
```

```text title="Expected output"
{"status":"success","taskId":"task-restore-20260101-120045","message":"Restore operation initiated","estimatedDuration":"45 minutes","backupVersion":"8.12.1","targetVersion":"8.12.1"}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to curl to skip SSL verification (already present in the example, but ensure it's not removed).
    **`jq: command not found` or `python3: command not found`** — Install the required JSON parser with `apt-get install python3` or `yum install python3` on the Aria Operations for Networks appliance.
    **`{"status":"error","message":"Invalid or expired token","code":"AUTH_FAILED"}`** — Verify the admin credentials are correct and the authentication endpoint is reachable with `curl -sk https://aon-new.example.local/api/ni/auth/token`.
```bash
ssh ubuntu@10.10.10.51    # Collector VM

# On Collector VM:
sudo /home/ubuntu/support/pairing.sh
# Enter Platform VM FQDN when prompted
# Enter new pairing key when prompted
```

```text title="Expected output"
ubuntu@10.10.10.51's password: 
Welcome to Aria Operations for Networks Collector Pairing Tool
================================================================

Platform VM FQDN: platform.aria.local
Validating connectivity to platform.aria.local... OK
Current pairing key: a7f3e2c1-9b4d-4e8f-b2a6-d1c5e9f3a7b2
Enter new pairing key (or press Enter to keep current): 8k9m2p5q-7r3s-4t1u-6v2w-9x8y3z1a5b4c
Updating pairing configuration... OK
Restarting collector service... OK
Pairing completed successfully at 2024-01-15 14:32:47 UTC
Collector is now paired with platform.aria.local
```

!!! warning "Common errors"
    **`sudo: /home/ubuntu/support/pairing.sh: command not found`** — Verify the pairing.sh script exists at /home/ubuntu/support/ or check if the support directory path differs in your deployment.
    **`Connection refused: Unable to reach platform.aria.local on port 443`** — Ensure the Platform VM FQDN is correct and reachable from the Collector VM, and verify network connectivity and firewall rules allow port 443.
    **`Current pairing key: [key] - Error: Invalid pairing key format`** — Enter a valid UUID-format pairing key (8-4-4-4-12 hexadecimal characters separated by hyphens).
```bash
ssh ubuntu@aon-platform.example.local

# Check Cassandra status
sudo systemctl status cassandra

# If Cassandra failed to start (likely after unclean shutdown):
sudo systemctl stop cassandra
sudo find /var/lib/cassandra -name "*.tmp" -delete
sudo systemctl start cassandra
sudo systemctl status cassandra

# Check all platform services
sudo systemctl status vrni-platform nginx kafka elasticsearch postgres
```


```text title="Expected output"
ubuntu@aon-platform.example.local's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-42-generic x86_64)

● cassandra.service - Apache Cassandra
     Loaded: loaded (/etc/systemd/system/cassandra.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2min 45s ago
   Main PID: 2847 (java)
      Tasks: 47 (limit: 4915)
     Memory: 2.1G
        CPU: 18s
     CGroup: /system.slice/cassandra.service
             └─2847 /usr/lib/jvm/java-11-openjdk-amd64/bin/java -XX:+UseG1GC...

● vrni-platform.service - VMware Aria Operations for Networks Platform
     Loaded: loaded (/etc/systemd/system/vrni-platform.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:28:52 UTC; 6min 11s ago
   Main PID: 1924 (java)
      Memory: 3.4G

● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:29:01 UTC; 6min 2s ago
   Main PID: 2156 (nginx)
      Tasks: 3 (limit: 4915)
     Memory: 45.2M

● kafka.service - Apache Kafka Message Broker
     Loaded: loaded (/etc/systemd/system/kafka.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:30:15 UTC; 4min 48s ago
   Main PID: 2521 (java)
      Memory: 1.8G

● elasticsearch.service - Elasticsearch
     Loaded: loaded (/etc/systemd/system/elasticsearch.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:31:02 UTC; 3min 61s ago
   Main PID: 2704 (java)
      Memory: 2.6G

● postgres.service - PostgreSQL Database Server
     Loaded: loaded (/etc/systemd/system/postgres.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:27:33 UTC; 7min 40s ago
   Main PID: 1687 (postgres)
      Memory: 156.3M
```

!!! warning "Common errors"
    **`Job for cassandra.service failed because the control process exited with error code.`** — Run `sudo find /var/lib/cassandra -name "*.tmp" -delete && sudo systemctl start cassandra` to clear corrupted temp files from an unclean shutdown.
    **`Unit postgres.service not found.`** — Verify the correct service name with `sudo systemctl list-units --type
## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## See also

- [AON Operational Procedures](../procedures/)
- [vRNI Common Issues](../../troubleshooting/common-issues/)
- [vRNI Health Checks](../health-checks/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
