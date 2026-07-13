---
tags:
  - networking
---
# Integration — Service Integrations

```bash
# Prometheus: check scrape targets
curl -s http://prometheus:9090/api/v1/targets | jq '.data.activeTargets[] | {job:.labels.job, health:.health, error:.lastError}'

# Alertmanager: check alert routing
curl -s http://alertmanager:9093/api/v2/alerts | jq '.[] | {alertname:.labels.alertname, state:.status.state}'

# Grafana datasource health
curl -s -u admin:pass http://grafana:3000/api/datasources | jq '.[] | {name:.name, type:.type, url:.url}'
```


```text title="Expected output"
{
  "job": "prometheus",
  "health": "up",
  "error": null
}
{
  "job": "node-exporter",
  "health": "up",
  "error": null
}
{
  "job": "blackbox-exporter",
  "health": "down",
  "error": "connection refused"
}
{
  "alertname": "HighCPUUsage",
  "state": "firing"
}
{
  "alertname": "DiskSpaceLow",
  "state": "resolved"
}
{
  "name": "Prometheus",
  "type": "prometheus",
  "url": "http://prometheus:9090"
}
{
  "name": "Loki",
  "type": "loki",
  "url": "http://loki:3100"
}
{
  "name": "TestData",
  "type": "testdata",
  "url": ""
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to prometheus port 9090: Connection refused` | Verify Prometheus is running with `docker ps | grep prometheus` or check service status with `systemctl status prometheus`. |
    | `jq: parse error: Invalid JSON text at line 1` | Ensure the endpoint is responding with valid JSON by testing with `curl -s http://prometheus:9090/api/v1/targets | head -c 200` first. |
    | `curl: (401) Unauthorized` | Update the Grafana credentials in the curl command to match your actual admin password, or generate an API token with `-H "Authorization: Bearer <token>"`. |
```bash
# SSSD on Linux
systemctl status sssd
sssctl domain-status <domain>
id <ad-user>               # should return AD UID + groups

# Winbind
wbinfo -t                  # test trust to domain
wbinfo -u | head -5        # list domain users
net ads info               # show DC and site info

# LDAP reachability
ldapsearch -x -H ldap://<dc-hostname> -b "dc=corp,dc=example,dc=com" "(sAMAccountName=testuser)" cn mail
```

```text title="Expected output"
● sssd.service - System Security Services Daemon
     Loaded: loaded (/usr/lib/systemd/system/sssd.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:23:47 UTC; 2 days ago
   Main PID: 2847 (sssd)
      Tasks: 12 (limit: 4915)
     Memory: 45.2M
        CPU: 2min 34s
     CGroup: /system.slice/sssd.service

Domain name: corp.example.com
Status: Online
Online status last updated: 2024-01-15 11:42:18

uid=1105(testuser) gid=513(domain users) groups=513(domain users),512(domain admins),1050(engineering-team)

Trust is up and running.

BUILTIN\Administrators
BUILTIN\Users
corp\testuser
corp\admin-service
corp\jenkins-bot
...

Forest            : corp.example.com
Domain            : corp.example.com
Dc                : dc01.corp.example.com [2001:db8::42]
Site              : US-EAST-1
Kdc               : dc01.corp.example.com

# LDAP search output
dn: CN=testuser,CN=Users,DC=corp,DC=example,DC=com
cn: testuser
mail: testuser@corp.example.com
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Could not get domain status for <domain>: No such domain` | Verify the domain name matches SSSD configuration in `/etc/sssd/sssd.conf` and restart sssd with `systemctl restart sssd`. |
    | `wbinfo: error looking up domain users` | Ensure Winbind is running with `systemctl start winbind` and the domain trust is established via `net ads join -U administrator`. |
    | `ldapsearch: error code 49 - 80090308: LdapErr: DSID-0C090400, comment: AcceptSecurityContext error, data 52e, v3839` | Verify AD user credentials are correct and the account is not locked; use a service account with appropriate permissions for LDAP queries. |
```bash
# PgBouncer status
psql -h /tmp -p 6432 pgbouncer -c "SHOW POOLS;"
psql -h /tmp -p 6432 pgbouncer -c "SHOW STATS;"

# ProxySQL (MySQL)
mysql -h 127.0.0.1 -P 6032 -u admin -padmin -e "SELECT hostgroup_id, hostname, status FROM mysql_servers;"
```

```text title="Expected output"
database      |   user    | cl_active | cl_waiting | sv_active | sv_idle | sv_used | sv_tested | sv_login | maxwait | pool_mode
------------------+-----------+-----------+------------+-----------+---------+---------+-----------+---------+---------+-----------
 postgres         | postgres  |         2 |          0 |         5 |       3 |       8 |         0 |       0 |       0 | transaction
 myapp_db         | appuser   |         1 |          0 |         2 |       1 |       3 |         0 |       0 |       0 | session
 template1        | postgres  |         0 |          0 |         0 |       0 |       0 |         0 |       0 |       0 | transaction

 database      | total_xact_count | total_query_count | total_recv | total_sent | total_wait_time
------------------+-----------------+-------------------+------------+------------+-----------------
 postgres         |            1247 |             3891 |   524288 B |   786432 B |            1250
 myapp_db         |             892 |             2156 |   262144 B |   393216 B |             890

hostgroup_id | hostname          | status
-----------+-----------------+--------
           0 | db-primary.local  | ONLINE
           1 | db-replica-01.local | ONLINE
           1 | db-replica-02.local | ONLINE
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: could not translate host name "/tmp" to address: Name or service not known` | Verify PgBouncer is listening on the Unix socket path `/tmp` or use `-h 127.0.0.1` with the correct TCP port. |
    | `ERROR 1045 (28000): Access denied for user 'admin'@'127.0.0.1' (using password: YES)` | Confirm ProxySQL admin credentials in `/etc/proxysql.cnf` or reset them with `proxysql --initial`. |
    | `psql: error: connection refused` | Ensure PgBouncer is running with `systemctl status pgbouncer` and listening on port 6432. |
```bash
# SSSD (re-read AD group membership)
sssctl cache-remove -y && systemctl restart sssd

# rsyslog
systemctl restart rsyslog && systemctl status rsyslog

# PgBouncer
systemctl restart pgbouncer && psql -h /tmp -p 6432 pgbouncer -c "SHOW POOLS;"

# Veeam agent
systemctl restart veeam
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```
