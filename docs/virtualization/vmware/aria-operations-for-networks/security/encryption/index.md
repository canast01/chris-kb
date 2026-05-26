# Aria Operations for Networks — Encryption

---

## Data at Rest

| Component | Encryption | Method |
|---|---|---|
| Platform VM disks | Optional | vSphere VM Encryption or encrypted datastore |
| Collector VM disks | Optional | vSphere VM Encryption or encrypted datastore |
| Stored credentials (vCenter/NSX) | Yes | AES-256, Platform VM keystore |
| Flow database | Datastore-level | Encrypt underlying datastore (vSAN encrypted storage policy) |

Apply vSphere VM Encryption to Platform and Collector VMs via an encrypted storage policy if the datastore does not use hardware encryption.

---

## Data in Transit

| Traffic Path | Encryption | Notes |
|---|---|---|
| Browser → Platform UI | TLS 1.2+ HTTPS | TCP 443 |
| REST API client → Platform | TLS 1.2+ HTTPS | TCP 443 |
| Collector → Platform | TLS 1.2+ HTTPS | TCP 443 |
| Platform/Collector → vCenter | TLS 1.2+ HTTPS | TCP 443 |
| Platform/Collector → NSX Manager | TLS 1.2+ HTTPS | TCP 443 |
| Switches → Collector (NetFlow/IPFIX) | None | UDP — unencrypted by protocol design |

NetFlow/IPFIX is inherently unencrypted. Mitigate by placing Collector VMs on a dedicated management or replication VLAN with no routing from untrusted segments.

---

## Certificate Management

vRNI ships with a self-signed certificate. Replace with a CA-signed certificate for production.

### Replace via UI

```text
Settings → SSL Certificate → Upload Certificate
  Upload: PEM certificate chain (server cert + intermediate CAs)
  Upload: Private key (PEM, no passphrase)
  Save → UI restarts — reconnect after ~60 seconds
```

### Replace via REST API

```bash
CERT_B64=$(base64 -i server.crt | tr -d '\n')
KEY_B64=$(base64 -i server.key | tr -d '\n')

curl -sk -X PUT \
  "https://vrni.example.local/api/ni/system/ssl/certificate" \
  -H "Authorization: NetworkInsight $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"certificate\": \"$CERT_B64\", \"private_key\": \"$KEY_B64\"}"
```

### Verify Certificate Expiry

```bash
echo | openssl s_client -connect vrni.example.local:443 -servername vrni.example.local 2>/dev/null \
  | openssl x509 -noout -dates
# notBefore= and notAfter= lines show validity window
```

---

## TLS Cipher Hardening

Restrict to strong ciphers by editing the Nginx config on the Platform VM:

```bash
ssh ubuntu@vrni.example.local
sudo vim /etc/nginx/nginx.conf

# Find and update ssl_* directives:
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers on;

sudo nginx -t && sudo systemctl reload nginx
```

Verify:
```bash
nmap --script ssl-enum-ciphers -p 443 vrni.example.local
# Confirm: no TLS 1.0/1.1, no RC4/DES/3DES
```

---

## Credential Storage

vRNI encrypts all data source credentials (vCenter, NSX, physical device passwords) in its internal database. The encryption key is tied to the Platform VM instance. Do not copy the Platform VM VMDK to another host — credentials will not decrypt without the original key material.

Update stored credentials when source system passwords change:
```text
Settings → Data Sources → [source] → Edit → update password → Save
```
