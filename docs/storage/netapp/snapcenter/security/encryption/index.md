# SnapCenter — Encryption

> Part of the [SnapCenter Security](../) reference.

---

## TLS and Certificate Management

- SnapCenter web server uses TLS 1.2 minimum; configure in IIS → SSL Settings
- Replace the default self-signed certificate with a CA-signed certificate for production deployments:
  1. Generate a CSR from IIS on the SnapCenter Server
  2. Submit to internal CA or public CA
  3. Import signed certificate and update the IIS HTTPS binding on port 8146
- Verify the certificate is trusted by all automation hosts and browsers used to access the GUI
