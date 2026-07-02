---
tags:
  - security
  - troubleshooting
search:
  boost: 1.5
---
# Security — Troubleshooting

<div class="kb-summary">
Security platform troubleshooting — certificate validation failures, CyberArk vault connectivity, Venafi policy errors, MFA authentication issues, and SIEM connectivity problems.
</div>

<div class="kb-grid kb-grid-1">
<a class="kb-card" href="authentication-failures/"><strong>Authentication Failures</strong><span>AD, Kerberos, LDAP, certificate, and MFA authentication failure diagnosis and resolution.</span></a>
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
symptom_index: "Symptom Index" {shape: rectangle}
tls_certificate_failures: "TLS / Certificate Failures" {shape: rectangle}
cyberark_vault_connectivity: "CyberArk Vault Connectivity" {shape: rectangle}
mfa_duo_troubleshooting: "MFA / Duo Troubleshooting" {shape: rectangle}
kerberos_authentication_failures: "Kerberos Authentication Failures" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> symptom_index: investigate
symptom -> tls_certificate_failures: investigate
symptom -> cyberark_vault_connectivity: investigate
symptom -> mfa_duo_troubleshooting: investigate
symptom -> kerberos_authentication_failures: investigate
symptom_index -> resolution
tls_certificate_failures -> resolution
cyberark_vault_connectivity -> resolution
mfa_duo_troubleshooting -> resolution
kerberos_authentication_failures -> resolution
```

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


```text title="Expected output"
verify ok
subject=CN = host.example.com, O = Example Corp, C = US
issuer=C = US, O = DigiCert Inc, CN = DigiCert Global G2 TLS RSA SHA256 CA
Cipher : ECDHE-RSA-AES128-GCM-SHA256
Protocol : TLSv1.3
notBefore=Jan 15 08:22:14 2023 GMT
notAfter=Jan 15 08:22:13 2025 GMT
cert.crt: OK
```

!!! warning "Common errors"
    **`verify error:num=20:unable to get local issuer certificate`** — Add the intermediate CA certificate to your trust store or use the `-CApath` flag pointing to the directory containing CA bundles.
    **`error in x509 lookup`** — Ensure the certificate file path is correct and readable; verify with `ls -la /etc/ssl/certs/cert.crt`.
    **`Verify return code: 1 (self signed certificate)`** — For self-signed certificates in testing, use `openssl verify -CAfile cert.crt cert.crt` or add the cert to your trust store.
**Expected output:** Chain check shows `verify return:1` for each cert in the chain and `Verification: OK` at the end. `openssl verify` returns `cert.crt: OK`. Absence of `OK` or presence of `verify error:num=` indicates a chain or trust store problem.

See [TLS Troubleshooting](../../networking/protocols/tls/troubleshooting/) for detailed steps.

## CyberArk Vault Connectivity

```bash
# Test vault reachability (port 1858)
nc -zv vault.corp.local 1858

# Test CPM → target account
# Review: PrivateArk → Monitoring → Last PM Action log

# Verify CPM service running
sc query CyberArk_CPM   # Windows
```


```text title="Expected output"
Connection to vault.corp.local 1858 port [tcp/*] succeeded!
(no output — command completes silently)
SERVICE_NAME: CyberArk_CPM
        TYPE               : 10  INTERACTIVE
        STATE              : 4  RUNNING
                                (STOPPABLE, PAUSABLE, ACCEPTS_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0
```

!!! warning "Common errors"
    **`nc: getaddrinfo for name=vault.corp.local port=1858: Name or service not known`** — Verify DNS resolution with `nslookup vault.corp.local` and confirm the hostname is correct in your network.
    **`SERVICE_NAME: CyberArk_CPM STATE              : 1  STOPPED`** — Start the CyberArk CPM service using `sc start CyberArk_CPM` or the Windows Services GUI.
**Expected output:** `nc` returns `Connection to vault.corp.local port 1858 [tcp] succeeded`. `sc query CyberArk_CPM` shows `STATE: 4 RUNNING`. If connection refused, check firewall rule for TCP 1858 between the CPM server and the Vault.

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


```text title="Expected output"
Wed Jan 15 14:32:47 UTC 2025
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
ntp.ubuntu.com      .POOL.          16 p    -   64    0    0.000    0.000   0.000
0.ubuntu.pool.ntp.o 216.239.35.0     2 u   28   64  377   45.231   -2.145   3.821
1.ubuntu.pool.ntp.o 129.6.15.28      2 u   26   64  377   52.104    1.832   2.456
2.ubuntu.pool.ntp.o 132.163.96.1     2 u   31   64  377   48.567   -0.923   1.204

               Local time: Wed 2025-01-15 14:32:47 UTC
           Universal time: Wed 2025-01-15 14:32:47 UTC
                 RTC time: Wed 2025-01-15 14:32:47
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
RTC in local TZ: no

Ticket cache: FILE:/tmp/krb5cc_0
Default principal: username@CORP.LOCAL

Valid starting     Expires            Service principal
01/15/25 14:32:47  01/16/25 00:32:47  krbtgt/CORP.LOCAL@CORP.LOCAL
01/15/25 14:32:47  01/16/25 00:32:47  HTTP/host.corp.local@CORP.LOCAL

servicePrincipalName: HTTP/host.corp.local
servicePrincipalName: HTTP/host.corp.local:80
objectClass: computer
cn: hostname
```

!!! warning "Common errors"
    **`kinit: Clients credentials have been revoked while getting initial credentials`** — Verify the user account is active in Active Directory and hasn't exceeded password expiration or failed login attempts.
    **`ldapsearch: Invalid credentials (49)`** — Ensure the admin account credentials are correct and the LDAP bind DN format matches your domain structure (e.g., "CN=admin,CN=Users,DC=corp,DC=local").