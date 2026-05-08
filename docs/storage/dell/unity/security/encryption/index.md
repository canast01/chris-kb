# Unity — Encryption

## Encryption Layers

| Layer | Method | Notes |
|---|---|---|
| Data at Rest (D@RE) | AES-256 self-encrypting drives | Enabled at pool creation on capable hardware; cannot be enabled on an existing unencrypted pool without data migration |
| External Key Management | KMIP protocol to an external KMS (Thales, Vormetric, SafeNet) | Configure KMIP in Unisphere under Settings > Encryption; recommended for compliance environments |
| Data in Transit (management) | TLS 1.2+ for Unisphere GUI, REST API, and uemcli | Disable TLS 1.0/1.1; verify with `uemcli /sys/security show` |
| Data in Transit (iSCSI) | CHAP authentication for iSCSI initiator authentication | Configure CHAP per host in Unisphere > Hosts; mutual CHAP is recommended |
| Data in Transit (NFS) | Kerberos (krb5, krb5i, krb5p) for NFS v4 with AD-joined NAS servers | Configure Kerberos security mode on NFS exports requiring in-transit protection |
