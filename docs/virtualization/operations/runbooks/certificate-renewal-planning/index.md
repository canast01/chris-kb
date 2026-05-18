# VMware Certificate Renewal Runbook

```
┌─────────────────────────────────────────────────────────────────┐
│               CERTIFICATE RENEWAL PLANNING FLOW                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │   Inventory Expiry      │
              │  Scan all certs: VCSA,  │
              │  NSX, Aria, ESXi hosts  │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   Plan Sequence         │
              │  Identify dependencies  │
              │  CA root ► intermediary │
              │  ► leaf certs           │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   Schedule Window       │
              │  Outside peak hours     │
              │  Confirm backup current │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   Renew Certificate     │
              │  VMCA / custom CA path  │
              │  Restart required svcs  │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   Validate & Close      │
              │  Browser ✓ SSO ✓        │
              │  Integrations ✓         │
              │  Update inventory       │
              └─────────────────────────┘
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
