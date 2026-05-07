# Aria Operations Troubleshooting

## Adapter Collection Failures

Adapter collection failures appear as red or yellow status on the **Environment > Object Browser** page. Check the adapter instance health first.

```bash
# SSH into the Aria Operations node
ssh admin@<vrops-node>

# Check adapter status via vROPS CLI
chkadapter --list
chkadapter --instance <adapter-instance-name>
chkadapter --test <adapter-instance-name>

# Restart a specific adapter
service vmware-vcops-watchdog restart
```

Log locations for adapter collection issues:

| Log File | Path | Purpose |
|---|---|---|
| Collector log | `/data/vcops/log/collector.log` | Adapter collection events |
| Adapter log | `/data/vcops/log/adapters/<adapter-name>/` | Per-adapter debug output |
| Casa log | `/data/vcops/log/casa.log` | Authentication and session events |
| Analytics log | `/data/vcops/log/analytics.log` | Metric processing pipeline |

```bash
# Tail the collector log in real time
tail -f /data/vcops/log/collector.log

# Search for errors in the last 500 lines
tail -500 /data/vcops/log/collector.log | grep -i "error\|exception\|failed"

# Check adapter-specific log
ls /data/vcops/log/adapters/
tail -200 /data/vcops/log/adapters/VMwareAdapter/adapter.log
```

## Login Issues

Login failures are usually certificate mismatches, LDAP/AD configuration, or expired local passwords.

```bash
# Check CASA service (authentication service)
service vmware-vcops-casa status
service vmware-vcops-casa restart

# Check Tomcat SSL certificate
/usr/lib/vmware-vcops/tools/bin/vcops-ssl.sh --check

# View current certificate details
openssl s_client -connect <vrops-fqdn>:443 </dev/null 2>/dev/null | openssl x509 -noout -dates

# Reset admin password via CLI
/usr/lib/vmware-vcops/tools/bin/vrops-admin-passwd.sh --reset
```

Common login error causes:

| Symptom | Likely Cause | Action |
|---|---|---|
| "Invalid credentials" on known-good password | Locked account or LDAP bind failure | Check CASA log; verify LDAP bind account |
| Certificate warning on login page | Self-signed or expired cert | Replace cert via Admin UI or `vcops-ssl.sh` |
| SSO redirect loop | vCenter SSO trust not configured | Re-register SSO in Admin > Global Settings |
| "Service unavailable" on login | CASA or web service down | `service vmware-vcops-casa restart` |

## Slow Dashboards

Dashboard performance problems are usually caused by too many widgets, unoptimised super metric queries, or undersized nodes.

```bash
# Check system resource usage
top -bn1 | head -20
free -h
df -h

# Check vROPS analytics heap usage
/usr/lib/vmware-vcops/tools/bin/vcops-support.sh --heap

# Identify slow super metrics
grep "slow\|timeout" /data/vcops/log/analytics.log | tail -100

# Check cluster node status
/usr/lib/vmware-vcops/tools/bin/cluster-nodes.sh --status
```

Dashboard tuning recommendations:

| Area | Default | Recommended |
|---|---|---|
| Widgets per dashboard | No limit | <= 12 per tab |
| Super metric lookback | 6 hours | <= 2 hours for live dashboards |
| Auto-refresh interval | 5 min | 10-15 min for large dashboards |
| Objects per widget | No limit | <= 500 |

## Missing Metrics

Metrics disappear when collection gaps exceed the retention window, adapter credentials expire, or the object falls out of scope.

```bash
# Check object collection state
chkadapter --object "<object-name>" --adapter <adapter-instance>

# Force a collection cycle
chkadapter --collect <adapter-instance>

# Verify object exists and is not orphaned
grep "<object-name>" /data/vcops/log/collector.log | tail -50

# Check data retention settings
/usr/lib/vmware-vcops/tools/bin/vrops-retention.sh --show
```

## Certificate Errors

```bash
# List certificates managed by vROPS
/usr/lib/vmware-vcops/tools/bin/vcops-ssl.sh --list

# Check certificate expiry for all endpoints
/usr/lib/vmware-vcops/tools/bin/vcops-ssl.sh --check-expiry

# Import a new certificate from PEM files
/usr/lib/vmware-vcops/tools/bin/vcops-ssl.sh --import \
  --cert /tmp/vrops.crt \
  --key /tmp/vrops.key \
  --ca /tmp/ca-chain.crt

# Restart web service after cert replacement
service vmware-vcops-web restart
service vmware-vcops-casa restart
```

Certificate error reference:

| Error Message | Root Cause | Resolution |
|---|---|---|
| `PKIX path building failed` | CA not trusted by JVM truststore | Import CA cert into Java truststore |
| `Certificate expired` | Cert past NotAfter date | Replace certificate immediately |
| `Hostname mismatch` | FQDN not in SAN/CN | Re-issue cert with correct FQDN |
| `Handshake failure` | TLS version mismatch | Check and align TLS settings on both ends |

## Support Bundle Collection

```bash
# Generate a support bundle (outputs to /tmp by default)
/usr/lib/vmware-vcops/tools/bin/vcops-support.sh --generate

# Collect with specific time range
/usr/lib/vmware-vcops/tools/bin/vcops-support.sh --generate \
  --start "2026-05-01 00:00" \
  --end "2026-05-07 23:59"

# Check bundle location
ls -lh /storage/log/vcops-support-*.zip
```
