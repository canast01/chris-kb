# Protocols — Troubleshooting

<div class="kb-summary">
Protocol troubleshooting — FC fabric errors, TLS handshake failures, LDAP connectivity, DNS resolution failures, NTP drift, and HTTP/HTTPS diagnosis.
</div>

<div class="kb-grid kb-grid-1">
<a class="kb-card" href="dns-resolution/"><strong>DNS Resolution Failures</strong><span>DNS resolution failure diagnosis — resolver, zone, and client-side troubleshooting steps.</span></a>
</div>

## Protocol Symptom Index

| Symptom | Protocol | First command |
|---|---|---|
| Name resolution fails | DNS | `dig @<server> A hostname` |
| Kerberos auth fails | DNS / Kerberos | `dcdiag /test:dns`, check NTP sync |
| TLS handshake fails | TLS | `openssl s_client -connect host:443` |
| Certificate not trusted | TLS/PKI | `openssl verify -CAfile ca.crt cert.crt` |
| LDAP bind fails | LDAP | `ldapsearch -H ldap://dc -x -b "dc=corp,dc=local"` |
| FC port not online | Fibre Channel | `fcinfo hba-port`, `show interface fc` |
| iSCSI target unreachable | iSCSI | `iscsiadm -m discovery`, check port 3260 |
| NTP time drift | NTP | `timedatectl status`, `ntpq -pn` |

## DNS Troubleshooting

```bash
dig @<authoritative-server> A hostname      # query specific server
dig +trace hostname                          # trace from root
nslookup hostname <server>                   # Windows/Linux
dig -x <IP>                                  # reverse lookup
```

Common problems: wrong resolver, stale TTL, split-horizon misconfiguration. See [DNS Troubleshooting](../dns/troubleshooting/).

## TLS Troubleshooting

```bash
openssl s_client -connect host:443 -servername host.example.com
# Look for: Verify return code: 0 (ok)
```

See [TLS Troubleshooting](../tls/troubleshooting/).

## LDAP Troubleshooting

```bash
# Anonymous bind test
ldapsearch -H ldap://dc01.corp.local -x -b "dc=corp,dc=local" "(objectClass=*)" | head -20

# Authenticated bind
ldapsearch -H ldap://dc01.corp.local -D "CORP\svc_app" -W \
  -b "OU=Users,DC=corp,DC=local" "(sAMAccountName=testuser)"
```

Common errors: `LDAP_INVALID_CREDENTIALS` (wrong bind DN), `LDAP_UNWILLING_TO_PERFORM` (anonymous bind disabled), port 389/636 blocked.

## NTP Troubleshooting

```bash
timedatectl status                  # Linux: show time source and sync status
ntpq -pn                            # show NTP peer status (reach > 0 = receiving)
chronyc tracking                    # if using chrony: offset and stratum
w32tm /query /status                # Windows: time service status
```

Alert threshold: offset > 5 minutes breaks Kerberos authentication.

## Fibre Channel Troubleshooting

```bash
fcinfo hba-port                     # Linux: show HBA ports and WWPNs
cat /sys/class/fc_host/host*/port_state   # port online/offline
systool -c fc_host -v               # detailed HBA info
```

See [Fibre Channel](../fibre-channel/) for zoning and fabric troubleshooting.
