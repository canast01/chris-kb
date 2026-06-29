---
tags:
  - servicenow
---
# Inventory — Environment Mapping

```markdown

```d2
direction: down

application_payments_api: "Application: Payments API" {shape: rectangle}

```

## Application: Payments API

**Tier:** Production
**Hosts:** pay-api-01, pay-api-02, pay-api-03 (load balanced via alb-pay-prod)
**Owner:** Payments Team — payments-team@example.com

### Inbound Dependencies (who calls this service)
| Caller | Protocol | Port | Auth |
|---|---|---|---|
| Web frontend | HTTPS | 443 | JWT |
| Mobile app | HTTPS | 443 | JWT |
| Batch job (billing-cron) | HTTPS | 443 | mTLS |

### Outbound Dependencies (what this service calls)
| Target | Protocol | Port | Auth | Failure Impact |
|---|---|---|---|---|
| payments-db-primary | PostgreSQL | 5432 | DB user | Full outage |
| payments-db-replica | PostgreSQL | 5432 | DB user | Read-only degraded |
| fraud-detection-api | HTTPS | 443 | API key | Transactions blocked |
| vault | HTTPS | 8200 | AppRole | Auth fails; downtime |
| smtp-relay | SMTP | 25 | None | Email receipts fail only |

### Data Flows
- Payment transaction → payments-db → fraud-detection-api → response
- Audit log → kafka-payments-topic → SIEM

### Infrastructure
- Load Balancer: alb-pay-prod (AWS ALB)
- DNS: api.payments.example.com → alb-pay-prod CNAME
- TLS cert: *.payments.example.com — expires 2027-03-01
- Secrets: vault path `secret/payments/db_password`, `secret/payments/fraud_api_key`
```

```bash
# netstat — find connections on a host
ss -tnp    # established TCP connections and owning process
ss -tlnp   # listening ports

# Find which process owns a port
lsof -i :<port>

# Trace network path to a service
traceroute <target-host>
mtr --report <target-host>

# DNS record discovery
dig <hostname> ANY
dig -t SRV _service._proto.<domain>
```


```text title="Expected output"
$ ss -tnp
State      Recv-Q Send-Q Local Address:Port       Peer Address:Port Process
ESTAB      0      0      192.168.1.42:52847      10.240.15.8:443   users:(("chrome",pid=3847,fd=24))
ESTAB      0      0      192.168.1.42:52891      172.16.0.5:3306   users:(("mysql",pid=2156,fd=12))
ESTAB      0      0      192.168.1.42:22         203.0.113.99:54321 users:(("sshd",pid=1024,fd=3))

$ ss -tlnp
State      Recv-Q Send-Q Local Address:Port       Peer Address:Port Process
LISTEN     0      128    127.0.0.1:5432          0.0.0.0:*         users:(("postgres",pid=891,fd=5))
LISTEN     0      128    0.0.0.0:80              0.0.0.0:*         users:(("nginx",pid=1205,fd=6))
LISTEN     0      128    0.0.0.0:443             0.0.0.0:*         users:(("nginx",pid=1205,fd=7))

$ lsof -i :8080
COMMAND   PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
java      2847    appuser 45u  IPv4  0x12a4f5c0      0t0  TCP localhost:8080 (LISTEN)

$ traceroute api-prod.internal.corp
traceroute to api-prod.internal.corp (10.50.12.33), 30 hops max, 60 byte packets
 1  gateway.local (192.168.1.1)  2.341 ms  2.156 ms  2.089 ms
 2  core-router-01.dc1 (10.0.0.1)  5.623 ms  5.401 ms  5.512 ms
 3  10.240.15.1  8.934 ms  9.012 ms  8.876 ms
 4  api-prod.internal.corp (10.50.12.33)  12.445 ms  12.389 ms  12.567 ms

$ dig api-prod.internal.corp ANY
; <<>> DiG 9.16.1-Ubuntu <<>> api-prod.internal.corp ANY
;; ANSWER SECTION:
api-prod.internal.corp. 300 IN A 10.50.12.33
api-prod.internal.corp. 300 IN AAAA 2001:db8::1
api-prod.internal.corp. 300 IN MX 10 mail.internal.corp.

$ dig -t SRV _ldap._tcp.internal.corp
; <<>> DiG 9.16.1-Ubuntu <<>> -t SRV _ldap._tcp.internal.corp
;; ANSWER SECTION:
_ldap._tcp.internal.corp. 3600 IN SRV 10 60 389 ldap-01.internal.corp.
_ldap._tcp.internal.corp. 3600 IN SRV 10
```