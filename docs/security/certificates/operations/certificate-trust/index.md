# Certificate Trust Store Management

<div class="kb-summary">
Adding CA certificates to OS and application trust stores so that TLS connections to internal services succeed. Covers Linux (RHEL, Ubuntu/Debian), Windows (machine store and GPO), Java keystores, and verification commands.
</div>

```text
┌───────────────────────────────── Certificate Trust Store Management ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Add CA certificates to trust stores so TLS connections to internal services succeed      │   │
│   │           Linux: copy .crt to /etc/pki/ca-trust/source/anchors/ then update-ca-trust          │   │
│   │          Windows: import to Trusted Root CA store; deploy via GPO for domain machines         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Linux Trust Store               │  │             Windows & Appliances            │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │           RHEL: /etc/pki/ca-trust/           │  │         MMC → Cert snap-in → import         │   │
│   │         Ubuntu: /usr/local/share/ca/         │  │         GPO: Computer Config → Certs        │   │
│   │            update-ca-trust (RHEL)            │  │         Appliance: upload via UI/API        │   │
│   │         update-ca-certificates (Deb)         │  │            Java: keytool -import            │   │
│   │        Verify: curl https://internal         │  │        Test: curl / PowerShell Invoke       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │     Platform     │  CA store path   │    Add command    │      Verify      │      Scope       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │   RHEL/CentOS    │ /etc/pki/anchors │  update-ca-trust  │  curl https://   │   System-wide    │   │
│   │  Ubuntu/Debian   │ /usr/local/share │  update-ca-certs  │  curl https://   │   System-wide    │   │
│   │     Windows      │ Trusted Root CA  │   certlm.msc/GPO  │   IE/Edge/curl   │  Machine store   │   │
│   │    Java apps     │   JRE cacerts    │  keytool -import  │ Java HTTPS call  │    JVM-scoped    │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Root CA      = Top of certificate chain; self-signed; must be in trust store for chain to verify   │
│    Intermediate = Signed by Root CA; signs end-entity certs; must be in cert bundle sent by server    │
│    update-ca-trust= RHEL command; rebuilds the consolidated trust bundle from source anchors          │
│    keytool      = Java utility; manages JVM trust store (cacerts); import with -importcert            │
│    GPO          = Group Policy Object; deploys CA cert to all domain machines automatically           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Ubuntu / Debian

```bash
cp internal-ca.crt /usr/local/share/ca-certificates/internal-ca.crt
update-ca-certificates
# Verify
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt server.crt
```

## RHEL / Rocky / AlmaLinux

```bash
cp internal-ca.crt /etc/pki/ca-trust/source/anchors/internal-ca.crt
update-ca-trust extract
# Verify
trust list | grep "internal-ca"
```

## Windows — Local Machine Store

```powershell
# Import CA cert to Trusted Root CA store on a single machine
certutil -addstore "Root" internal-ca.crt

# Verify
certutil -viewstore -enterprise Root | findstr "Corp"
```

## Windows — GPO (Domain Distribution)

1. Open **Group Policy Management** and create or edit a GPO linked to the domain.
2. Navigate to: `Computer Configuration → Windows Settings → Security Settings → Public Key Policies → Trusted Root Certification Authorities`
3. Right-click → **Import** → select the CA certificate file.
4. Apply the GPO and run `gpupdate /force` on a test machine.
5. Verify: open `certlm.msc` → Trusted Root Certification Authorities → check the CA appears.

This distributes the Root CA certificate to all domain-joined machines automatically at next Group Policy refresh.

## Java Keystore

```bash
# Import CA cert into JVM trust store
keytool -import \
  -alias internal-ca \
  -file internal-ca.crt \
  -keystore $JAVA_HOME/lib/security/cacerts \
  -storepass changeit \
  -noprompt

# Verify
keytool -list -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit | grep internal-ca
```

---

## Verification Commands

### openssl Chain Verification

```bash
# Full chain verification
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt server.crt

# Verify chain from a specific CA file
openssl verify -CAfile internal-ca.crt -untrusted intermediate.crt server.crt

# Inspect certificate details
openssl x509 -in server.crt -noout -text | grep -E "Subject:|Issuer:|Not After|Not Before|DNS:"

# Check certificate fingerprint (compare with expected)
openssl x509 -in server.crt -noout -fingerprint -sha256

# Test live TLS trust from the OS
openssl s_client -connect <hostname>:443 -CAfile /etc/ssl/certs/ca-certificates.crt </dev/null 2>&1 | grep -E "Verify return|Certificate chain"
```

### TLS Debug

```bash
# Full TLS handshake trace
openssl s_client -connect <host>:443 -showcerts </dev/null

# Check what CA signed the certificate
openssl s_client -connect <host>:443 </dev/null 2>/dev/null | openssl x509 -noout -issuer

# curl verbose TLS debug
curl -v --cacert /path/to/internal-ca.crt https://<host>/endpoint

# Python — test with custom CA
REQUESTS_CA_BUNDLE=/path/to/internal-ca.crt python3 -c "import requests; print(requests.get('https://<host>').status_code)"
```

### Bulk Expiry Check

```bash
# Check expiry of a file
openssl x509 -in server.crt -noout -enddate

# Check expiry on a live endpoint
echo | openssl s_client -connect <host>:443 2>/dev/null | openssl x509 -noout -enddate

# Bulk check for certs expiring within 30 days
for cert in /etc/ssl/certs/*.crt; do
  expiry=$(openssl x509 -in "$cert" -noout -enddate 2>/dev/null | cut -d= -f2)
  if openssl x509 -in "$cert" -noout -checkend 2592000 2>/dev/null; then :
  else echo "EXPIRING: $cert — $expiry"; fi
done
```
