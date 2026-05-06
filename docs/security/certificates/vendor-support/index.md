# Certificates Vendor Support

Microsoft ADCS issues are raised through the Microsoft Support portal (support.microsoft.com) — collect CA event logs, the `certutil -ping` output, and CRL freshness data before opening a case. DigiCert and Entrust commercial CA issues are handled via their respective customer portals; provide the order number, certificate serial number, and full error message. Let's Encrypt issues are handled via the community forum at community.letsencrypt.org (no paid support tier).

Venafi support covers lifecycle automation failures — see the Venafi vendor-support section for SR creation details. For all cases, pre-collect `certutil` diagnostic output and CA event log exports to reduce time-to-resolution.

| Vendor | Support Channel | Key Data to Collect |
|---|---|---|
| Microsoft ADCS | support.microsoft.com | CA event logs, `certutil -ping`, CRL freshness |
| DigiCert | digicert.com/support | Order number, serial number, error message |
| Entrust | entrust.com/support | Certificate ID, error message, issuance date |
| Let's Encrypt | community.letsencrypt.org | ACME challenge logs, domain validation errors |
| Venafi | support.venafi.com | See Venafi vendor-support page |
