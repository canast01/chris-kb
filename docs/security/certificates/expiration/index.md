# Certificate Expiration Monitoring

Expired certificates cause immediate service outages. Monitoring expiry and alerting well in advance (90/30/7 day thresholds) is essential.

## Checking Expiry with openssl

```bash
# Check expiry date of a remote server cert
echo | openssl s_client -connect example.com:443 2>/dev/null \
    | openssl x509 -noout -dates

# Check expiry of a local cert file
openssl x509 -in server.crt -noout -enddate

# Check if cert expires within N days (exit code 1 if expired)
openssl x509 -in server.crt -noout -checkend $((30 * 86400))
# Exit 0 = valid for 30+ days; Exit 1 = expires within 30 days

# Get expiry as epoch for scripting
openssl x509 -in server.crt -noout -enddate \
    | cut -d= -f2 | date -f - +%s
```

## Alert Thresholds

| Threshold | Action |
|---|---|
| 90 days | Ticket creation, assigned to cert owner |
| 30 days | Escalation to team lead, renewal started |
| 14 days | Daily alerts, management notification |
| 7 days | P1 incident, emergency renewal |
| Expired | Outage declared, break-glass procedure |

## Bulk Expiry Check Script (Bash)

```bash
#!/bin/bash
# Check expiry for a list of hosts
HOSTS=("example.com:443" "api.example.com:443" "intranet.corp.example.com:8443")
WARN_DAYS=30

for HOST in "${HOSTS[@]}"; do
    EXPIRY=$(echo | openssl s_client -connect "$HOST" 2>/dev/null \
        | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
    if [ -z "$EXPIRY" ]; then
        echo "UNREACHABLE: $HOST"
        continue
    fi
    EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s 2>/dev/null || date -j -f "%b %d %T %Y %Z" "$EXPIRY" +%s)
    NOW_EPOCH=$(date +%s)
    DAYS_LEFT=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))
    if [ "$DAYS_LEFT" -le "$WARN_DAYS" ]; then
        echo "WARNING: $HOST expires in $DAYS_LEFT days ($EXPIRY)"
    else
        echo "OK: $HOST expires in $DAYS_LEFT days"
    fi
done
```

## Windows Certificate Expiry Checks

```powershell
# Check all certs in local machine store expiring within 90 days
Get-ChildItem Cert:\LocalMachine\My |
    Where-Object {$_.NotAfter -lt (Get-Date).AddDays(90)} |
    Select-Object Subject, Thumbprint, NotAfter | Sort-Object NotAfter

# Check a remote host cert
$tcp = New-Object System.Net.Sockets.TcpClient("example.com", 443)
$ssl = New-Object System.Net.Security.SslStream($tcp.GetStream())
$ssl.AuthenticateAsClient("example.com")
$cert = $ssl.RemoteCertificate
[System.Security.Cryptography.X509Certificates.X509Certificate2]::new($cert) |
    Select-Object Subject, NotAfter
$ssl.Close(); $tcp.Close()
```

## Monitoring Integration

```bash
# Nagios/Icinga check_ssl_cert style check
openssl s_client -connect example.com:443 </dev/null 2>/dev/null \
    | openssl x509 -noout -checkend $((14 * 86400))
echo "Exit: $?"

# Export expiry dates for Prometheus node exporter (textfile collector)
EXPIRY=$(echo | openssl s_client -connect example.com:443 2>/dev/null \
    | openssl x509 -noout -enddate | cut -d= -f2)
EPOCH=$(date -d "$EXPIRY" +%s)
echo "ssl_cert_expiry_seconds{host=\"example.com\"} $EPOCH" \
    > /var/lib/node_exporter/textfile_collector/ssl.prom
```
