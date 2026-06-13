---
tags:
  - aria-networks
  - security
  - vmware
---
# Aria Operations for Networks — Encryption


<div class="kb-summary">
Encryption reference covering Data at Rest, Data in Transit, Certificate Management, TLS Cipher Hardening, Credential Storage.

*Applies to: Aria Networks 6.x*
</div>

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
┌─────────────────────────────────────────── vRNI Encryption ───────────────────────────────────────────┐
│                                                                                                       │
│  TLS 1.2+, LDAPS, data-at-rest encryption, and certificate management for vRNI.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            In-Transit Encryption             │  │            Certificate Management           │   │
│   │           TLS 1.2+ for all web UI            │  │           Upload cert via VAMI SSL          │   │
│   │          TLS for collector-platform          │  │           CA-signed cert preferred          │   │
│   │          LDAPS (port 636) for auth           │  │          Monitor cert expiry dates          │   │
│   │         HTTPS for all REST API calls         │  │             Rotate before expiry            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  All communications use TLS; data at rest protected by vSphere D@RE; certs monitored.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Data-at-Rest Encryption            │  │            Weak Cipher Hardening            │   │
│   │          vSphere D@RE on datastore           │  │            Disable TLS 1.0 / 1.1            │   │
│   │           vSAN encryption optional           │  │          Disable RC4 / 3DES ciphers         │   │
│   │           No native vRNI disk enc            │  │             Enforce AES-256-GCM             │   │
│   │         KMS integration via vSphere          │  │          Review cipher via openssl          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere with D@RE; KMS server for key management; CA for cert signing                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TLS 1.2+            = Minimum transport security for all vRNI communications                         │
│  LDAPS               = LDAP over TLS port 636; replaces plain LDAP port 389                           │
│  D@RE                = Data-at-Rest Encryption via vSphere encrypted datastores                       │
│  KMS                 = Key Management Server; manages encryption keys for D@RE                        │
│  CA-Signed Cert      = Certificate from internal or public CA; replaces self-signed                   │
│  Self-Signed Cert    = Default vRNI cert; replace before production use                               │
│  Cipher Suite        = Combination of key exchange, bulk encryption, and MAC algorithm                │
│  AES-256-GCM         = Preferred symmetric cipher for TLS in vRNI communications                      │
│  Cert Expiry         = Certificate validity end date; monitor to avoid outage                         │
│  VAMI SSL Settings   = Page in VAMI where cert and key are uploaded for vRNI                          │
│  vSAN Encryption     = Optional vSAN data-at-rest encryption for VM storage                           │
│  openssl s_client    = CLI tool to verify TLS version and cipher negotiated                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
