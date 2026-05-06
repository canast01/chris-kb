# Certificates Security

Root CA and Issuing CA private keys must be protected by HSMs — software-only key storage is not acceptable for CA keys. The Root CA must remain offline and air-gapped, powered on only for the specific purpose of issuing or renewing subordinate CA certificates. Certificate pinning implementations must be carefully managed to avoid service disruptions during certificate renewal.

All publicly trusted certificates must be submitted to Certificate Transparency (CT) logs as required by CA/Browser Forum rules. OCSP stapling should be enforced on all TLS endpoints to avoid privacy leakage via OCSP queries and to improve client connection performance. CRL Distribution Points must remain highly available — their unavailability can cause soft-fail clients to proceed with revoked certificates.

| Control | Detail |
|---|---|
| CA key protection | HSM required for Root and Issuing CA private keys |
| Root CA offline policy | Powered on only for subordinate CA issuance events |
| CT log submission | Mandatory for all publicly trusted certificates |
| OCSP stapling | Enforce on all public TLS endpoints |
| CRL availability | CRL Distribution Points must be HA — monitor freshness |
| Certificate pinning | Document all pinned certificates; coordinate renewal carefully |
| Audit logging | All CA issuance and revocation events forwarded to SIEM |
