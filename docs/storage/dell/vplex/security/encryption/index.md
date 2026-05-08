# Dell VPLEX — Encryption

> TLS certificate management and data encryption for Dell VPLEX.

## Data in Transit

- VPLEX management traffic between VMS and directors uses encrypted protocols
- Unisphere for VPLEX web UI uses HTTPS (TLS); replace the default self-signed certificate with a certificate signed by the corporate CA
- `vplexcli` access is via SSH to the VMS; enforce SSH key authentication and disable password-based SSH where possible

## Data at Rest

VPLEX itself does not perform data-at-rest encryption — encryption at rest is the responsibility of the backend storage arrays:

- Enable encryption on backend PowerMax, Unity, or PowerStore arrays as appropriate for compliance requirements
- Verify encryption is active on the backend array before claiming storage volumes into VPLEX
- VPLEX is transparent to backend array encryption; encrypted volumes are presented and virtualised without modification

## TLS Certificate Management

- Replace the Unisphere for VPLEX self-signed certificate with a corporate CA-signed certificate on initial deployment
- Monitor certificate expiry; renew at least 30 days before the expiry date
- Store certificate private keys in a secrets management system
