# VMware Certificate Quick Reference

```
┌───────────────────┬───────────────────────────┬────────────────────────────────┐
│   Component       │  Expiry Check             │  Renewal Steps                 │
├───────────────────┼───────────────────────────┼────────────────────────────────┤
│ vCenter SSL       │ VAMI :5480 → Certs        │ vSphere Client → Cert Mgmt     │
│ vCenter STS       │ vecs-cli entry list       │ STS renewal via KB procedure   │
│ NSX Manager       │ NSX UI → System → Certs   │ Generate CSR → import signed   │
│ Aria endpoints    │ Aria Admin → Settings     │ Custom CA → import via UI      │
├───────────────────┴───────────────────────────┴────────────────────────────────┤
│  openssl: openssl s_client -connect <host>:443 2>/dev/null | openssl x509      │
│           -noout -dates                                                         │
│  Alert threshold: < 60 days to expiry  │  Review: monthly                      │
└─────────────────────────────────────────────────────────────────────────────────┘
```
## Check Expiration Quickly

In vCenter Appliance Management (VAMI) at `https://<vcenter>:5480`:
- Navigate to **Certificate Management**
- Review all certificate expiration dates

## Identify Certificate Type

| Symptom | Likely Certificate |
|---|---|
| Browser warning on vCenter | Machine SSL certificate |
| Login fails for all users | STS certificate |
| Product integration broken | Trusted root or endpoint cert |
| NSX UI unreachable | NSX Manager certificate |
| Aria product unreachable | Aria endpoint certificate |

## Review Trusted Root Chain

- Confirm the issuing CA root certificate is trusted by vCenter
- If a custom CA is used, confirm both root and intermediate are imported

## Check STS Certificate

```bash
# SSH to vCenter
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store TRUSTED_ROOTS
```

## Validate After Replacement

- Browser access to vCenter — no certificate warning
- SSO login working for local and AD accounts
- All hosts Connected
- Integrations working (Aria, NSX, backup)
- Document new expiration date

## Escalate If

- vCenter services fail after certificate replacement
- STS cannot be recovered in place
- Certificate replacement causes SSO token failures
