# AWS KMS

```
┌──────────────────────────────────── KMS — Key Management Service ─────────────────────────────────────┐
│                                                                                                       │
│  KMS manages encryption keys used by AWS services; CMKs provide full customer control.                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Key Types                   │  │                Key Operations               │   │
│   │      Symmetric: AES-256 for encryption       │  │         Encrypt: up to 4KB directly         │   │
│   │       Asymmetric: RSA/ECC sign/verify        │  │        GenerateDataKey: envelope enc        │   │
│   │         HMAC: message authentication         │  │       Sign/Verify: digital signatures       │   │
│   │        AWS-managed: per service; free        │  │      CreateGrant: temporary delegation      │   │
│   │        Customer-managed: full control        │  │     Decrypt: returns plaintext data key     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key policies are the primary access control; IAM policies alone are insufficient for CMKs.           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Key Policy                  │  │               KMS Integration               │   │
│   │       Root account: full admin access        │  │        S3: SSE-KMS per bucket/object        │   │
│   │        Key admins: manage but not use        │  │         EBS: CMK at volume creation         │   │
│   │        Key users: encrypt/decrypt ops        │  │        RDS: CMK at database creation        │   │
│   │     kms:ViaService: service restriction      │  │        Secrets Manager: auto-rotation       │   │
│   │     Cross-account: explicit allow needed     │  │        CloudTrail: all KMS API calls        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS KMS HSM hardware (FIPS 140-2 Level 3) · Regional KMS endpoints · CloudHSM option                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CMK             = Customer-Managed Key; KMS key managed by customer with full control                │
│  Key policy      = Resource-based JSON policy attached to a KMS key; required for access              │
│  Envelope encryption= Plaintext encrypted with data key; data key encrypted with CMK                  │
│  GenerateDataKey = KMS returns plaintext + encrypted data key for envelope encryption                 │
│  Key rotation    = Annual automatic rotation of key material; previous material retained              │
│  Key alias       = Friendly name (alias/my-key) for a CMK; updatable without re-keying                │
│  Grant           = Programmatic temporary delegation of key use to a principal                        │
│  kms:ViaService  = Condition restricting key use to calls made by a specific AWS service              │
│  Key deletion    = 7–30 day waiting period before permanent deletion; irreversible                    │
│  Multi-region key= Replica key in another region; same key material, different ARN                    │
│  CloudHSM        = Dedicated hardware HSM; FIPS 140-2 Level 3; customer-managed cluster               │
│  Asymmetric key  = Public key downloadable; private key never leaves KMS HSM                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS KMS notes for day-to-day infrastructure operations.

## Where It Fits

Use this page for build work, support checks, troubleshooting, standards, and operational review.

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| Confirm service health. |  |  |
| Review alerts. |  |  |
| Check recent changes. |  |  |
| Confirm capacity and performance are within normal range. |  |  |

## Health Commands

~~~bash
# Add environment-specific commands here
~~~

## Common Issues

- Misconfiguration after change work.
- Missing access or permissions.
- Alert noise without clear ownership.
- Drift from documented standards.

## Operational Tasks

| Task | Command |
|---|---|
| Review current configuration. |  |
| Validate dependencies. |  |
| Record changes. |  |
| Confirm monitoring coverage. |  |

## Upgrade Notes

- Check release notes before upgrades.
- Validate backup or rollback options.
- Confirm maintenance window and communication plan.
- Test after the change.

## Best Practices

| Recommendation | Detail |
|---|---|
| Keep naming consistent. | Keep naming consistent. |
| Document ownership. | Document ownership. |
| Use least privilege access. | Use least privilege access. |
| Validate changes after implementation. | Validate changes after implementation. |
