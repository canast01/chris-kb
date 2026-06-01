# Service Integrations


<div class="kb-summary">
Health checks and troubleshooting for common infrastructure integration points: monitoring, backup, authentication, logging, and ticketing.
</div>

## Integration Health Overview

| Integration | Health Check | Common Failure |
|---|---|---|
| Monitoring → Alertmanager | Alert rules firing; silence list empty | Webhook URL changed; auth token expired |
| Syslog → SIEM | Events appearing in SIEM within 60s | Port 514 blocked; UDP vs TCP mismatch |
| Backup agent → target storage | Agent heartbeat; backup job success | Credentials expired; storage full |
| Linux/Windows → AD (SSSD/Winbind) | `id <user>` returns AD groups | Kerberos ticket expired; DC unreachable |
| App server → database | Connection pool healthy; query success | Password rotated without app update |
| CI/CD → artifact registry | Push/pull succeeds | Token expired; registry TLS cert untrusted |
| App → secret manager | Secret retrieval latency < 200ms | IAM role missing; network policy |

## Monitoring Integration

```bash
# Prometheus: check scrape targets
curl -s http://prometheus:9090/api/v1/targets | jq '.data.activeTargets[] | {job:.labels.job, health:.health, error:.lastError}'

# Alertmanager: check alert routing
curl -s http://alertmanager:9093/api/v2/alerts | jq '.[] | {alertname:.labels.alertname, state:.status.state}'

# Grafana datasource health
curl -s -u admin:pass http://grafana:3000/api/datasources | jq '.[] | {name:.name, type:.type, url:.url}'
```
```text
┌───────────────────────────────── Integration — Service Integrations ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Patterns for integrating infrastructure components with ITSM, monitoring, backup, SIEM    │   │
│   │       Typically via: REST API (webhook/poll), SNMP traps, syslog, agent, or file export       │   │
│   │         Use dedicated service accounts; minimal scope; rotate credentials on schedule         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      ITSM (ServiceNow)      │  │          Monitoring         │  │       Security (SIEM)       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │         CMDB CI sync        │  │      SNMP trap receiver     │  │      Syslog forwarding      │   │
│   │     Incident auto-create    │  │      Agent (Zabbix/NR)      │  │      CEF / JSON events      │   │
│   │     Change feed webhook     │  │       REST API polling      │  │      API key for ingest     │   │
│   │    MID Server for on-prem   │  │     Alert routing rules     │  │    TLS syslog (port 6514)   │   │
│   │    Test: CI creation flow   │  │     Test: send test trap    │  │     Test: logger command    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    MID Server    = ServiceNow component that runs on-prem; proxies API calls to instance              │
│    SNMP trap     = Unsolicited alert from device to monitoring; receiver must be configured           │
│    CEF           = Common Event Format; Syslog header + key=value pairs; standard SIEM intake         │
│    Syslog/514    = UDP syslog; no guarantee of delivery; TLS syslog (6514) preferred                  │
│    Webhook       = HTTP callback; source POSTs event payload to receiver URL on trigger               │
│    API key scope = Limit API key to minimum permissions; rotate annually or on staff change           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```python

## Active Directory / LDAP Integration

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

## Database Connection Pooling

```bash
# PgBouncer status
psql -h /tmp -p 6432 pgbouncer -c "SHOW POOLS;"
psql -h /tmp -p 6432 pgbouncer -c "SHOW STATS;"

# ProxySQL (MySQL)
mysql -h 127.0.0.1 -P 6032 -u admin -padmin -e "SELECT hostgroup_id, hostname, status FROM mysql_servers;"
```

## Integration Restart Procedures

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

## Credential Rotation Checklist

When a shared service account password is rotated, update in this order:

1. Update secret in vault (AWS Secrets Manager / Azure Key Vault)
2. Update application config or environment variable
3. Restart the service consuming the credential
4. Validate integration health (connection pool, authentication test)
5. Confirm no errors in application logs post-restart

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| SSSD not resolving users | `sssctl domain-status`; DC reachable? | Restart SSSD; check Kerberos ticket (`klist`) |
| Syslog not arriving at SIEM | Port open? TLS cert trusted? | `nc -zv` syslog server; check rsyslog error log |
| Backup job failing | Storage full? Credentials expired? | Check vault storage; rotate creds; check agent logs |
| Prometheus target `down` | Exporter running? Port accessible? | `curl http://host:<port>/metrics`; restart exporter |
| App can't connect to DB | Pool config pointing at old IP? Password rotated? | Check connection string; verify credentials; bounce pool |
