---
tags:
  - reference
description: "VMware Certificate Quick Reference reference covering Check Expiration Quickly, Identify Certificate Type, Review Trusted Root Chain, Check STS..."
---
# VMware Certificate Quick Reference

<div class="kb-summary">
VMware Certificate Quick Reference reference covering Check Expiration Quickly, Identify Certificate Type, Review Trusted Root Chain, Check STS Certificate, Validate After Replacement and 1 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

check_expiration_quickly: "Check Expiration Quickly" {shape: rectangle}
identify_certificate_type: "Identify Certificate Type" {shape: rectangle}
review_trusted_root_chain: "Review Trusted Root Chain" {shape: rectangle}
check_sts_certificate: "Check STS Certificate" {shape: rectangle}
validate_after_replacement: "Validate After Replacement" {shape: rectangle}
escalate_if: "Escalate If" {shape: rectangle}

check_expiration_quickly -> identify_certificate_type: uses
identify_certificate_type -> review_trusted_root_chain: uses
review_trusted_root_chain -> check_sts_certificate: uses
check_sts_certificate -> validate_after_replacement: uses
validate_after_replacement -> escalate_if: uses
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


```text title="Expected output"
Entry [0]
	Alias: CA
	Certificate DN: CN=CA,OU=VMware,O=VMware,C=US
	Issuer DN: CN=CA,OU=VMware,O=VMware,C=US
	NotBefore: Jan 1 00:00:00 2020 GMT
	NotAfter: Jan 1 00:00:00 2030 GMT
	Fingerprint: A1:B2:C3:D4:E5:F6:7A:8B:9C:0D:1E:2F:3A:4B:5C:6D

Entry [1]
	Alias: Root
	Certificate DN: CN=Root,OU=VMware,O=VMware,C=US
	Issuer DN: CN=Root,OU=VMware,O=VMware,C=US
	NotBefore: Jan 1 00:00:00 2015 GMT
	NotAfter: Jan 1 00:00:00 2035 GMT
	Fingerprint: F1:E2:D3:C4:B5:A6:97:88:79:6A:5B:4C:3D:2E:1F:0A
```

!!! warning "Common errors"
    **`Error: Could not connect to VMware Certificate Store`** — Ensure the vmafd service is running with `systemctl status vmware-vmafd` and restart if needed.
    **`Error: Permission denied`** — Run the command with root privileges using `sudo` or as the root user.
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
