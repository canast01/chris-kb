---
tags:
  - dell
  - security
---
# Dell ECS — Encryption

<div class="kb-summary">
Encryption reference covering Encryption Layers, TLS Configuration, Data at Rest Encryption, Certificate Expiry Monitoring.

*Applies to: ECS 3.x*
</div>
![Dell ECS — Encryption](../../../../../assets/storage-dell-ecs-security-encryption.svg)

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Encryption Layers

![Encryption Layers](../../../../../assets/storage-dell-ecs-security-encryption-mermaid-svg.svg)

| Layer | Method | Notes |
|---|---|---|
| Data in transit | TLS 1.2+ | Enforced on S3 (443/9021), Swift (9024), Management API (4443); configure minimum TLS version in ECS Portal → Settings → Security |
| Data at rest | Software AES-256 (ECS encryption at rest) | Enable per-namespace in ECS Portal → Namespace → Edit → Encryption; key management via internal or external KMIP KMS |
| Key management | Internal ECS KMS or external KMIP server | For compliance, use an external KMIP-compatible KMS (e.g., HashiCorp Vault, Thales CipherTrust) |

Enable encryption at rest on namespaces that hold regulated data (PCI, HIPAA, GDPR). Note that enabling encryption on an existing namespace does not retroactively encrypt already-stored objects — only objects written after encryption is enabled are encrypted.

## TLS Configuration

### Certificate Management

ECS ships with self-signed certificates for both the Management API (port 4443) and the S3 endpoint (port 443/9021). Replace these with certificates signed by your corporate CA before go-live.

**Certificate locations in ECS Portal:**
- ECS Portal → Settings → Certificates → Management Certificate (for port 4443)
- ECS Portal → Settings → Certificates → Object Virtual Pool Certificate (for S3 endpoint)

**Certificate requirements:**

| Field | Requirement |
|---|---|
| Key type | RSA 2048-bit minimum; RSA 4096-bit or ECDSA P-256 recommended |
| Signature algorithm | SHA-256 or stronger |
| Subject Alternative Names | Must include all node FQDNs and the load balancer FQDN / VIP |
| Validity period | Maximum 2 years recommended (1 year preferred for compliance) |
| Key Usage | Digital Signature, Key Encipherment |
| Extended Key Usage | TLS Web Server Authentication |

**Certificate renewal procedure:**

1. Generate a CSR from ECS Portal → Settings → Certificates → Generate CSR
2. Submit the CSR to your corporate CA and obtain a signed certificate
3. Upload the signed certificate to ECS Portal → Settings → Certificates → Upload Certificate
4. ECS applies the certificate to the endpoint; no service restart required for certificate updates in ECS 3.8+
5. Verify the new certificate is served on the endpoint:
   ```bash
   openssl s_client -connect <ecs-node>:4443 -showcerts </dev/null 2>/dev/null \
     | openssl x509 -noout -dates -subject -issuer
   
   openssl s_client -connect <ecs-s3-endpoint>:9021 -showcerts </dev/null 2>/dev/null \
     | openssl x509 -noout -dates -subject -issuer
   ```
6. Confirm consuming applications can connect without SSL errors
7. Update monitoring to track the new certificate expiry date

### TLS Version and Cipher Configuration

```yaml
ECS Portal → Settings → Security → SSL/TLS Settings
  - Minimum TLS version: TLS 1.2 (disable TLS 1.0 and 1.1)
  - Cipher suites: Remove RC4, DES, 3DES, and NULL ciphers
  - Prefer: TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
```

Verify cipher configuration from a Linux host:

```bash
# Check which TLS versions and ciphers the endpoint accepts
nmap --script ssl-enum-ciphers -p 9021 <ecs-node>

# Verify TLS 1.0 is rejected
openssl s_client -connect <ecs-node>:9021 -tls1 </dev/null 2>&1 | grep -E "CONNECTED|handshake failure"

# Verify TLS 1.2 succeeds
openssl s_client -connect <ecs-node>:9021 -tls1_2 </dev/null 2>&1 | grep -E "CONNECTED|Protocol"
```


```text title="Expected output"
Starting Nmap 7.80 ( https://nmap.org ) at 2024-01-15 14:32:22 UTC
Nmap scan report for ecs-node-01.prod.local (10.42.8.15)
Host is up (0.0042s latency).

PORT     STATE SERVICE
9021/tcp open  unknown

TLSv1.2:
  ciphers:
    TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (secp256r1) - A
    TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (secp256r1) - A
    TLS_RSA_WITH_AES_256_GCM_SHA384 - A
  least strength: A

CONNECTED
140735289855680:error:1409E0E5:SSL routines:SSL_CONNECT_EX:ssl/tls alert handshake failure:../ssl/statem/connections.c:571:

CONNECTED
Protocol  : TLSv1.2
Cipher    : ECDHE-RSA-AES256-GCM-SHA384
```

!!! warning "Common errors"
    **`connect: Connection refused`** — Verify the ECS node is running and port 9021 is accessible; check firewall rules and that the management service is listening with `netstat -tlnp | grep 9021`.
    **`error:1409E0E5:SSL routines:SSL_CONNECT_EX:ssl/tls alert handshake failure`** — This is expected output when TLS 1.0 is correctly rejected; it confirms the security policy is working as intended.
### HTTP Disablement

Disable HTTP (port 9021 plain HTTP) in production. Only HTTPS should be accessible for S3 clients.

```text
ECS Portal → Settings → Security → Object Access
  - Disable HTTP access: enabled
  - Force HTTPS only: enabled
```

Verify port 9021 (plain HTTP) is not responding externally. The HTTPS port remains 9021 for S3 when using the non-standard S3 port; ensure firewall rules allow only 443 or 9021 from authorised source networks.

## Data at Rest Encryption

### Enabling Encryption on a Namespace

Encryption at rest is configured per namespace. Enable it at namespace creation for new namespaces; enabling it on existing namespaces only encrypts objects written after the change.

**Via ECS Portal:**
1. Navigate to ECS Portal → Manage → Namespaces → New Namespace (or select existing → Edit)
2. Enable **Encryption** in the namespace configuration
3. Select the key management type: **Internal ECS KMS** or **External KMIP**
4. Save; new objects written to buckets in this namespace will be encrypted with AES-256

**Via Management REST API:**

```bash
# Enable encryption on a new namespace
curl -s -k -X POST \
  -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  -H "Content-Type: application/json" \
  "https://<ecs-node>:4443/object/namespaces/namespace" \
  -d '{
    "id": "compliance-data",
    "default_data_services_vpool": "<replication-group-id>",
    "is_encryption_enabled": true,
    "is_compliance_enabled": true
  }' | python3 -m json.tool
```


```text title="Expected output"
{
  "id": "compliance-data",
  "link": {
    "rel": "self",
    "href": "/object/namespaces/compliance-data"
  },
  "creation_time": 1704067200000,
  "vpool": "urn:storageos:ReplicationGroupInfo/rg-prod-001",
  "is_encryption_enabled": true,
  "is_compliance_enabled": true,
  "is_stale_allowed": false,
  "default_retention": 0,
  "namespace_admins": [],
  "quota": -1,
  "quota_warn_threshold": 80
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification (already present in example, but ensure it's not removed).
    **`{"error_code":401,"error_message":"Invalid or expired authentication token"}`** — Regenerate the authentication token with `curl -s -k -X GET -H "Authorization: Basic $(echo -n 'root:PASSWORD' | base64)" https://<ecs-node>:4443/login` and export it to `$TOKEN`.
    **`{"error_code":400,"error_message":"Invalid replication group ID"}`** — Verify the replication group ID exists by running `curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" https://<ecs-node>:4443/object/replication-groups | python3 -m json.tool` and use a valid `id` from the output.
### Key Management

**Internal ECS KMS:**
- Default key management built into the ECS cluster
- Encryption keys are stored within the ECS metadata store (Cassandra)
- Suitable for environments without a regulatory requirement for external key management
- Risk: if all ECS nodes are simultaneously compromised or destroyed, keys may be unrecoverable — acceptable for most enterprise environments

**External KMIP KMS:**
- Required for PCI DSS, HIPAA, and other regulated environments that mandate external key custody
- ECS communicates with the KMIP server to retrieve encryption keys at object read/write time
- Supported KMIP-compatible servers:
  - HashiCorp Vault (with KMIP Secrets Engine)
  - Thales CipherTrust Manager
  - Entrust KeyControl
  - Dell PowerProtect Data Manager
  - Unbound CORE (formerly Unbound Tech)

**External KMIP configuration:**

```yaml
ECS Portal → Settings → Key Management
  - KMIP server hostname/IP: <kmip-server-fqdn>
  - KMIP port: 5696 (standard KMIP port)
  - Client certificate: <ECS-KMIP-client-cert.pem>
  - Client key: <ECS-KMIP-client-key.pem>
  - CA certificate: <KMIP-server-CA.pem> (for server validation)
  - Test connection before saving
```

**Key management operational considerations:**

| Consideration | Detail |
|---|---|
| KMIP availability | The KMIP server must be reachable for ECS to read encrypted objects; KMIP unavailability blocks reads on encrypted namespaces |
| Key backup | Back up KMIP server data and encryption key material independently; key loss makes encrypted objects unrecoverable |
| Network path | Dedicate a low-latency, reliable network path between ECS nodes and the KMIP server; KMIP latency adds to every object I/O on encrypted namespaces |
| Certificate rotation | KMIP client certificates (ECS-to-KMIP TLS) must be rotated before expiry; certificate expiry causes KMIP communication failure |

## Certificate Expiry Monitoring

Track all ECS certificate expiry dates in your monitoring system. Certificates should be renewed at least 30 days before expiry.

| Certificate | Location | Typical Validity | Renewal Lead Time |
|---|---|---|---|
| Management API TLS cert | ECS Portal → Settings → Certificates | 1–2 years | 30 days |
| S3 endpoint TLS cert | ECS Portal → Settings → Certificates | 1–2 years | 30 days |
| KMIP client cert (if used) | KMIP KMS and ECS key management config | 1–3 years | 60 days |
| LDAP/LDAPS CA cert (if used) | ECS namespace LDAP config | 1–10 years | 60 days |

```bash
# Check certificate expiry on the Management API endpoint
openssl s_client -connect <ecs-node>:4443 -servername <ecs-node> </dev/null 2>/dev/null \
  | openssl x509 -noout -enddate

# Check certificate expiry on the S3 endpoint
openssl s_client -connect <ecs-node>:9021 -servername <ecs-node> </dev/null 2>/dev/null \
  | openssl x509 -noout -enddate

# Alert if certificate expires within 30 days (for use in monitoring scripts)
EXPIRY=$(openssl s_client -connect <ecs-node>:4443 </dev/null 2>/dev/null \
  | openssl x509 -noout -enddate | cut -d= -f2)
EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s)
NOW_EPOCH=$(date +%s)
DAYS_LEFT=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))
echo "Certificate expires in $DAYS_LEFT days"
[[ $DAYS_LEFT -lt 30 ]] && echo "WARNING: Certificate renewal required"
```


```text title="Expected output"
notBefore=Jan 15 10:23:45 2023 GMT
notAfter=Jan 15 10:23:45 2025 GMT
notBefore=Jan 15 10:23:45 2023 GMT
notAfter=Jan 15 10:23:45 2025 GMT
Certificate expires in 287 days
```

!!! warning "Common errors"
    **`unable to connect to <ecs-node>:4443`** — Verify the ECS node hostname/IP is correct and the Management API port 4443 is accessible from your client (check firewall rules and node status).
    **`date: invalid date '<date-string>'`** — Ensure your system's `date` command supports the `-d` flag (use `date -j` on macOS, or install GNU coreutils on BSD systems).
    **`error in x509 parsing`** — Confirm the certificate chain is valid by running `openssl s_client -connect <ecs-node>:4443 -showcerts` to inspect the full certificate output.
---

## See also

- [Ecs — Hardening](../hardening/)
- [Ecs — Authentication](../authentication/)
- [Ecs — Access Control](../access-control/)
