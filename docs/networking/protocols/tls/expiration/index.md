---
tags:
  - networking
description: "Expired certificates cause immediate outages — services reject connections without warning."
---
# TLS Certificate Expiration

<div class="kb-summary">
Expired certificates cause immediate outages — services reject connections without warning.
</div>

Expiration monitoring and automated renewal must be in place for every certificate in production.

## Checking Expiry

```bash
# Single file
openssl x509 -in certificate.pem -noout -enddate

# Remote endpoint — days until expiry
openssl s_client -connect <hostname>:443 -servername <hostname> </dev/null 2>/dev/null \
  | openssl x509 -noout -enddate

# Days remaining (single line)
echo | openssl s_client -connect <hostname>:443 -servername <hostname> 2>/dev/null \
  | openssl x509 -noout -dates \
  | awk -F= '/notAfter/{print $2}' \
  | xargs -I{} date -d "{}" +%s \
  | xargs -I{} bash -c 'echo $(( ({} - $(date +%s)) / 86400 )) days remaining'

# Bulk check across multiple hosts
for host in web01 web02 api01; do
  expiry=$(echo | openssl s_client -connect ${host}.example.com:443 2>/dev/null \
    | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  echo "$host: $expiry"
done
```


```text title="Expected output"
notAfter=Dec 15 23:59:59 2025 GMT
depth=0 CN = api.example.com
verify return:1
notAfter=Dec 15 23:59:59 2025 GMT

47 days remaining

web01: Dec 15 23:59:59 2025 GMT
web02: Jan 22 10:30:45 2026 GMT
api01: Nov 8 14:17:22 2025 GMT
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `unable to load certificate` | Verify the certificate file path is correct and the file contains valid PEM-formatted data. |
    | `connect: Connection refused` | Confirm the hostname and port are correct, the service is running, and the host is reachable (check firewall rules and DNS resolution). |
    | `date: invalid date` | Ensure the system date command supports the `-d` flag; on macOS use `date -j -f "%b %d %T %Y %Z" "<date_string>" +%s` instead. |
## Expiry Monitoring

### Prometheus — Blackbox Exporter

```yaml
# prometheus.yml
scrape_configs:
  - job_name: tls_expiry
    metrics_path: /probe
    params:
      module: [tcp_connect]
    static_configs:
      - targets:
          - <hostname>:443
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - target_label: __address__
        replacement: localhost:9115

# Alert rule
groups:
  - name: tls
    rules:
      - alert: CertExpiryWarning
        expr: probe_ssl_earliest_cert_expiry - time() < 30 * 86400
        labels:
          severity: warning
        annotations:
          summary: "Certificate on {{ $labels.instance }} expires in < 30 days"

      - alert: CertExpiryCritical
        expr: probe_ssl_earliest_cert_expiry - time() < 7 * 86400
        labels:
          severity: critical
        annotations:
          summary: "Certificate on {{ $labels.instance }} expires in < 7 days"
```

### Nagios / Icinga — check_ssl_cert

```bash
check_ssl_cert -H <hostname> -p 443 -w 30 -c 7
# -w 30: warning at 30 days
# -c 7:  critical at 7 days
```


```text title="Expected output"
SSL_CERT OK - x509 certificate valid for 45 days (until Jan 15 2025 14:32:01 GMT) |days_valid=45;30;7
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `SSL_CERT CRITICAL - x509 certificate valid for 3 days` | The certificate is expiring soon; renew and deploy the certificate immediately, then restart the relevant service. |
    | `SSL_CERT WARNING - x509 certificate valid for 28 days` | The certificate will expire within the warning threshold; schedule a certificate renewal and deployment within the next 28 days. |
    | `check_ssl_cert: command not found` | Install the monitoring plugin package (e.g., `apt-get install monitoring-plugins` on Debian or `yum install nagios-plugins-all` on RHEL). |
## Renewal Workflow

```d2
direction: right

A: "Alert: < 30 days" {shape: rectangle}
B: "Generate new CSR" {shape: rectangle}
C: "Submit to CA\nor Venafi auto-enrol" {shape: rectangle}
D: "Receive new cert" {shape: rectangle}
E: "Test in staging" {shape: rectangle}
F: "Deploy to production\nnginx/Apache/HAProxy reload" {shape: rectangle}
G: "Verify new expiry" {shape: rectangle}
H: "Remove old cert" {shape: rectangle}

A -> B
B -> C
C -> D
D -> E
E -> F
F -> G
G -> H
```

### Venafi Automated Renewal

```bash
# Trigger renewal via Venafi CLI
vcert renew --pickup-id <cert-id>

# Or via REST API
curl -s -X POST "https://venafi.example.com/vedsdk/certificates/renew" \
  -H "X-Venafi-API-Key: <key>" \
  -H "Content-Type: application/json" \
  -d '{"CertificateDN":"\\VED\\Policy\\Servers\\web.example.com"}'
```


```text title="Expected output"
Successfully renewed certificate
Certificate ID: 7a3f8c2e-91b4-4d2a-b8f1-2c5e9d6a1b3f
Status: ISSUED
Renewal Date: 2024-01-15T10:32:47Z
Expiration Date: 2025-01-15T10:32:47Z
Subject: CN=web.example.com,O=Example Corp,C=US

{"Success":true,"CertificateId":"7a3f8c2e-91b4-4d2a-b8f1-2c5e9d6a1b3f","RenewalId":"renewal-5892-x4k9","Status":"ISSUED","ValidFrom":"2024-01-15T10:32:47Z","ValidTo":"2025-01-15T10:32:47Z"}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Certificate not found or access denied` | Verify the cert-id or CertificateDN is correct and your API key has renewal permissions on that certificate object. |
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl or configure your CA bundle to trust the Venafi server's certificate. |
    | `Error: Certificate renewal not allowed - already renewed within 30 days` | Check the last renewal date; Venafi policies may restrict renewal frequency to prevent abuse. |
### Let's Encrypt — certbot

```bash
# Renew all certificates
certbot renew

# Test renewal without committing
certbot renew --dry-run

# Cron job (run twice daily as recommended)
0 0,12 * * * certbot renew --quiet
```


```text title="Expected output"
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Starting new HTTPS connection (1): acme-v02.api.letsencrypt.org

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Processing /etc/letsencrypt/renewal/example.com.conf
Cert not yet due for renewal

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Processing /etc/letsencrypt/renewal/api.example.com.conf
Cert not yet due for renewal

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

The following certs are not due for renewal yet:
  /etc/letsencrypt/live/example.com/fullchain.pem expires on 2025-04-15 (59 days)
  /etc/letsencrypt/live/api.example.com/fullchain.pem expires on 2025-05-22 (96 days)
No renewals were attempted.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error while running renew step for /etc/letsencrypt/renewal/example.com.conf` | Check `/var/log/letsencrypt/letsencrypt.log` for detailed error and verify the renewal hook (e.g., web server restart) is configured correctly. |
    | `PermissionError: [Errno 13] Permission denied: '/etc/letsencrypt/renewal'` | Run certbot with `sudo` or ensure the user has read/write access to `/etc/letsencrypt/`. |
## Emergency Expired Certificate Response

```bash
# 1. Confirm the certificate is expired
openssl s_client -connect <hostname>:443 2>&1 | grep -E "notAfter|verify error"

# 2. Immediate mitigation options:
#    a) Extend using existing CA (if internal)
#    b) Deploy spare/wildcard certificate
#    c) Update DNS to failover endpoint

# 3. Issue replacement certificate (Venafi/ACME/manual CA)

# 4. Deploy without downtime (nginx zero-downtime reload)
nginx -t && nginx -s reload    # tests config before reloading

# 5. Verify new certificate
openssl s_client -connect <hostname>:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -dates
```


```text title="Expected output"
verify error:num=10:certificate has expired
notAfter=Jan 15 12:34:56 2024 GMT
notBefore=Jan 15 12:34:56 2023 GMT

nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

notBefore=Jan 16 08:22:14 2024 GMT
notAfter=Jan 15 08:22:14 2025 GMT
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `verify error:num=20:unable to get local issuer certificate` | Add the intermediate CA certificate to your trust store or bundle it with the server certificate in nginx.conf. |
    | `nginx: [error] open() "/var/run/nginx.pid" failed (2: No such file or directory)` | Start nginx with `nginx` before attempting reload, or use `systemctl start nginx` if managed by systemd. |
    | `error:0906D06C:PEM routines:PEM_read_bio:no start line` | Verify the certificate file path is correct and the file contains valid PEM-formatted data (begins with `-----BEGIN CERTIFICATE-----`). |
## Expiry Thresholds Reference

| Days remaining | Action |
|---|---|
| 90 | Begin renewal planning |
| 30 | Warning alert — initiate renewal |
| 14 | Escalate — renewal must be in progress |
| 7 | Critical — immediate action required |
| 0 | Expired — service impact |
