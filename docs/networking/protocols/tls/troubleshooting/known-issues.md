---
tags:
  - troubleshooting
  - tls
  - networking
  - certificates
  - known-issues
---
# TLS / SSL — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known TLS issues covering handshake failures, certificate validation errors, and version/cipher compatibility.

*Applies to: TLS 1.2 / 1.3*
</div>

```text
┌────────────────────────────────────────────── TLS / SSL ──────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Transport encryption — handshake, certificate validation, cipher negotiation         │   │
│   │                   Protocols: TLS 1.2 / 1.3 (layered under HTTPS/LDAPS/etc.)                   │   │
│   │                        Management: openssl CLI for testing/diagnostics                        │   │
│   │              ClientHello -> ServerHello+cert -> Key exchange -> Encrypted session             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Handshake          │  │        TLS handshake        │  │    Negotiates ver+cipher    │   │
│   │            Trust            │  │      Certificate chain      │  │     Must chain to a root    │   │
│   │          Validation         │  │        Hostname check       │  │     SAN must match host     │   │
│   │            Cipher           │  │         Cipher suite        │  │    Both sides must agree    │   │
│   │            Legacy           │  │         TLS 1.0/1.1         │  │     Disabled by default     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   ClientHello    │ Starts handshake │        TLS        │       N/A        │Lists ver/ciphers │   │
│   │   ServerHello    │ Sends cert+picks │        TLS        │   Server cert    │ Picks ver/cipher │   │
│   │ Chain validation │Trust verification│        TLS        │    CA-signed     │Client-side check │   │
│   │       mTLS       │   Mutual auth    │        TLS        │Client+server cert│Stronger, complex │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: N/A — TLS is a protocol layer, not a physical component                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Handshake      = negotiation establishing a session before data flows                                │
│  Cipher suite   = combination of algorithms used for a TLS session                                    │
│  SAN            = Subject Alternative Name; modern hostname match field                               │
│  CN             = Common Name; legacy field, ignored by modern browsers                               │
│  Root CA        = top-level trusted CA anchoring a chain                                              │
│  Intermediate CA= bridges a root CA to issued leaf certs                                              │
│  mTLS           = mutual TLS; both sides present certificates                                         │
│  ALPN           = Application-Layer Protocol Negotiation (HTTP/2)                                     │
│  SNI            = Server Name Indication; hostname sent before cert                                   │
│  Forward secrecy= session keys safe even if long-term key leaks                                       │
│  TLS termination= decrypting at a proxy/LB before forwarding plaintext                                │
│  OCSP stapling  = server includes revocation status in the handshake                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Diagnose with: `openssl s_client -connect <host>:443 -showcerts` — shows full certificate chain and TLS negotiation.
- TLS 1.0 and 1.1 are disabled by default on modern operating systems and browsers.
- Check both sides: server must support a cipher/version that the client supports.

## Handshake Failures

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| `SSL_ERROR_NO_CYPHER_OVERLAP` (Firefox) / `ERR_SSL_VERSION_OR_CIPHER_MISMATCH` (Chrome) | Client and server have no common TLS version or cipher suite | Enable TLS 1.2/1.3 on server; update legacy server software |
| `SSL3_GET_SERVER_CERTIFICATE:certificate verify failed` | Server certificate chain not trusted by client | Install CA certificate in client trust store; verify intermediate CA chain is complete |
| TLS handshake timeout | Server not responding on TLS port; or firewall dropping TLS traffic silently | Verify TCP connectivity: `nc -zv <host> 443`; check firewall for TLS inspection blocking |

## Certificate Errors

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| `Certificate has expired` | Server certificate past NotAfter date | Renew certificate; automate with ACME/Certbot |
| `hostname mismatch` | Certificate CN/SAN doesn't match the hostname being accessed | Reissue certificate with correct SAN for all hostnames |
| `self-signed certificate in certificate chain` | Intermediate or root CA is self-signed and not trusted | Add self-signed CA to client trust store; or use a trusted CA |

## TLS Version Compatibility

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| Legacy application fails after TLS 1.0/1.1 disabled on server | Application hardcoded TLS 1.0 | Update application to support TLS 1.2+; or use TLS termination proxy |
| Mutual TLS (mTLS) failing: `certificate required` | Client not presenting certificate | Configure client certificate in application; verify client cert issued by server-trusted CA |

## See also

- [TLS — Common Issues](common-issues.md)
- [Certificates / PKI — Known Issues](../../../security/certificates/troubleshooting/known-issues/)
- [Venafi — Known Issues](../../../security/venafi/troubleshooting/known-issues/)
