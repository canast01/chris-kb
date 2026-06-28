---
tags:
  - reference
---
# VMware Certificate Quick Reference


<div class="kb-summary">
VMware Certificate Quick Reference reference covering Check Expiration Quickly, Identify Certificate Type, Review Trusted Root Chain, Check STS Certificate, Validate After Replacement and 1 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>
![VMware Certificate Quick Reference](../../../../assets/virtualization-vmware-reference-quick-reference-certificate-.svg)




```d2
direction: right

center: "Quick Reference" {shape: rectangle}
check_expiration_quickly: "Check Expiration Quickly" {shape: rectangle}
identify_certificate_type: "Identify Certificate Type" {shape: rectangle}
review_trusted_root_chain: "Review Trusted Root Chain" {shape: rectangle}
check_sts_certificate: "Check STS Certificate" {shape: rectangle}
validate_after_replacement: "Validate After Replacement" {shape: rectangle}
escalate_if: "Escalate If" {shape: rectangle}

center -> check_expiration_quickly
center -> identify_certificate_type
center -> review_trusted_root_chain
center -> check_sts_certificate
center -> validate_after_replacement
center -> escalate_if
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
