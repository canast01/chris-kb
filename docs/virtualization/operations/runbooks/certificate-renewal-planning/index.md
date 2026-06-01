# VMware Certificate Renewal Runbook


<div class="kb-summary">
VMware Certificate Renewal Runbook reference covering Identify the Expiring Certificate, Confirm Affected Products, Capture Current Certificate Details, Confirm Backup Exists, Schedule Maintenance Window and 4 more sections.
</div>

```text
┌───────────────────────────────── VMware Certificate Renewal Runbook ──────────────────────────────────┐
│                                                                                                       │
│    Plan certificate renewals early; capture pre/post evidence; test all integrations                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                   Planning                   │  │                  Execution                  │   │
│   │        ──────────────────────────────        │  │        ─────────────────────────────        │   │
│   │        Identify expiring certificate         │  │         Schedule maintenance window         │   │
│   │         Confirm type: SSL / STS / SU         │  │             Notify stakeholders             │   │
│   │          List all affected products          │  │          Run cert renewal procedure         │   │
│   │          Note integrations at risk           │  │           Post-change: login test           │   │
│   │        Capture: subject, SAN, expiry         │  │          Verify all integrations OK         │   │
│   │          Screenshot as pre-evidence          │  │         Capture post-change evidence        │   │
│   │        Confirm vCenter backup exists         │  │             Close change record             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Machine SSL = vCenter/ESXi HTTPS cert; presented to browsers and API clients                       │
│    STS cert    = Security Token Service cert; used for SAML token signing in SSO                      │
│    SU cert     = Solution User cert; used by vCenter services to authenticate to SSO                  │
│    SAN         = Subject Alternative Name; list of FQDNs the cert is valid for                        │
│    VMCA        = VMware Certificate Authority; built-in CA; issues certs to ESXi hosts                │
│    Expiry buffer = Renew at 60 days remaining; 30 days = urgent; 0 days = service outage              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Identify the Expiring Certificate

- Review certificate inventory
- Confirm the certificate type: Machine SSL, STS, solution user, or integration endpoint
- Note the affected product and expiration date

## Confirm Affected Products

- List all products that trust or use this certificate
- Confirm which integrations may be disrupted during replacement

## Capture Current Certificate Details

- Subject, SAN, issuer, expiration date
- Screenshot from VAMI or vSphere Client as pre-change evidence

## Confirm Backup Exists

- Confirm vCenter file-based backup is current
- Confirm product backup for Aria or NSX if their certificate is being replaced

## Schedule Maintenance Window

- Plan replacement outside peak hours
- Allow time for service restarts and integration validation

## Replace the Certificate

- Follow the correct replacement method for the certificate type
- For VMCA-issued certs: use vSphere Client or VAMI
- For custom CA certs: generate CSR, submit to CA, import signed cert

## Restart Required Services

```bash
service-control --restart --all
```

Only restart services after confirming the new certificate is applied.

## Validate Integrations

- vCenter browser access — no certificate warning
- SSO login for local and AD accounts
- Aria, NSX, backup, and monitoring integrations confirmed

## Document Final Expiration Date

- Update the certificate inventory with the new expiration date
- Set a review reminder 60 days before the new expiration
