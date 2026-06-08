# Security — Troubleshooting

<div class="kb-summary">
Security platform troubleshooting — certificate validation failures, CyberArk vault connectivity, Venafi policy errors, MFA authentication issues, and SIEM connectivity problems.
</div>

## Symptom Index

| Symptom | Component | First steps |
|---|---|---|
| Certificate not trusted | PKI / TLS | Check chain, expiry, CA trust store |
| CyberArk account locked | CyberArk | Check CPM log; check max allowed requests |
| Venafi policy violation error | Venafi | Check policy zone; verify CSR attributes |
| MFA push not arriving | MFA / Duo | Check Duo proxy; verify user enrolled |
| LDAP bind failing | Identity | `ldapsearch` test; check svc account password |
| SIEM not receiving logs | SIEM | Check syslog forwarding; firewall UDP/514 or TCP/514 |
| Kerberos auth fails | AD / DNS | Check NTP sync; `klist -e`; check SPN |

## TLS / Certificate Failures

```bash
# Check certificate chain
openssl s_client -connect host:443 -servername host.example.com 2>&1 | \
  grep -E 'verify|subject|issuer|Cipher|Protocol'

# Check expiry
openssl x509 -noout -dates -in /etc/ssl/certs/cert.crt

# Check if CA in trust store
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt cert.crt
```

See [TLS Troubleshooting](../../protocols/tls/troubleshooting/) for detailed steps.

## CyberArk Vault Connectivity

```bash
# Test vault reachability (port 1858)
nc -zv vault.corp.local 1858

# Test CPM → target account
# Review: PrivateArk → Monitoring → Last PM Action log

# Verify CPM service running
sc query CyberArk_CPM   # Windows
```

## MFA / Duo Troubleshooting

```text
Symptom: User not receiving push
Check:
1. Mobile app connectivity (iOS/Android not blocked by corporate MDM)
2. Duo Authentication Proxy: tail /var/log/duo/authproxy.log
3. User enrolled: Duo Admin Panel → Users → search user
4. Failopen vs failclosed: check duoproxy.cfg fail_mode
```

## Kerberos Authentication Failures

```bash
# Check time sync (< 5 min drift required)
date; ntpq -pn
timedatectl status

# List current Kerberos tickets
klist -e

# Test kinit
kinit username@CORP.LOCAL
klist

# Check SPN
setspn -L hostname   # Windows
ldapsearch -H ldap://dc -D "CORP\admin" -W -b "DC=corp,DC=local" "(servicePrincipalName=HTTP/host.corp.local)"
```
