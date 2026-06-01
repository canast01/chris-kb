# Certificates Scripts


<div class="kb-summary">
Certificate automation scripts cover expiry scanning across all servers and services, TLS endpoint checking across all registered hostnames, CRL freshness monitoring, auto-renewal triggering via Venafi or ACME, and certificate chain validation.
</div>

 Scripts are maintained in PowerShell for Windows environments and Python for cross-platform use.

| Script | Language | Purpose |
|---|---|---|
| `cert-expiry-scanner.ps1` | PowerShell | Scan all servers in inventory for certificates expiring within N days |
| `tls-endpoint-check.py` | Python | Check TLS certificate validity and chain for a list of hostnames |
| `crl-freshness-check.ps1` | PowerShell | Verify CRL nextUpdate is within acceptable window for all CAs |
| `acme-renew-trigger.sh` | Bash | Trigger Let's Encrypt ACME renewal for public-facing services |
| `cert-chain-validator.py` | Python | Validate full certificate chain from end-entity to Root CA |

**Example: TLS endpoint check (Python)**

```python
import ssl, socket, datetime

def check_cert_expiry(hostname, port=443, warn_days=30):
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
        s.connect((hostname, port))
        cert = s.getpeercert()
    expiry = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
    days_left = (expiry - datetime.datetime.utcnow()).days
    if days_left < warn_days:
        print(f"WARNING: {hostname} expires in {days_left} days ({expiry})")
    return days_left
```
