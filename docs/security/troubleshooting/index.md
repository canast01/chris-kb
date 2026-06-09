# Security — Troubleshooting

<div class="kb-summary">
Security platform troubleshooting — certificate validation failures, CyberArk vault connectivity, Venafi policy errors, MFA authentication issues, and SIEM connectivity problems.
</div>

```text
┌──────────────────────────────────── Security — Troubleshooting ───────────────────────────────────────┐
│                                                                                                       │
│   Symptoms covered: cert not trusted, CyberArk lock, Venafi policy error, MFA push missing, LDAP bind │
│   Also: SIEM not receiving logs, Kerberos auth failures                                               │
│   First steps: check expiry (openssl), check bind account (Get-ADUser), check NTP sync (timedatectl)  │
│   Escalate to: PKI team (cert chain), SecOps (SIEM), AD team (Kerberos/LDAP)                          │
│                                                                                                       │
│   Common failure patterns                                                                             │
│   Cert not trusted     Check chain: openssl s_client -connect host:443; verify CA in trust store      │
│   CyberArk acct locked Check CPM log; check max allowed requests setting in PrivateArk                │
│   Venafi policy error  Check policy zone; verify CSR attributes match zone requirements               │
│   MFA push missing     Duo proxy log; verify user enrolled; check fail_mode in duoproxy.cfg           │
│   LDAP bind failing    ldapsearch test; check svc account password and OU bind permissions            │
│   SIEM no logs         Check syslog forwarding rule; verify firewall allows UDP/514 or TCP/514        │
│   Kerberos fails       NTP sync < 5 min drift; klist -e; check SPN with setspn -L                     │
│                                                                                                       │
│   Diagnostic commands                                                                                 │
│   TLS cert check: openssl s_client -connect host:443 | grep -E 'verify|subject|issuer'                │
│   Cert expiry: openssl x509 -noout -dates -in cert.crt                                                │
│   CA trust: openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt cert.crt                        │
│   Kerberos: kinit username@CORP.LOCAL; klist -e; check time with timedatectl status                   │
│                                                                                                       │
│   Key terms:                                                                                          │
│   CPM          = CyberArk Central Policy Manager; handles credential rotation; check its log first    │
│   Duo proxy    = Authentication Proxy; log at /var/log/duo/authproxy.log; check fail_mode setting     │
│   LDAP bind    = service account authentication to LDAP; fails if password expired or OU wrong        │
│   SPN          = Service Principal Name; required for Kerberos; check with setspn -L or ldapsearch    │
│   NTP drift    = Kerberos requires < 5 min time difference between client and KDC                     │
│   fail_mode    = Duo proxy setting; failopen allows login without MFA if Duo is unreachable           │
│   syslog port  = UDP/514 or TCP/514; must be open on firewall between source and SIEM collector       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-1">
<a class="kb-card" href="authentication-failures/"><strong>Authentication Failures</strong><span>AD, Kerberos, LDAP, certificate, and MFA authentication failure diagnosis and resolution.</span></a>
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
