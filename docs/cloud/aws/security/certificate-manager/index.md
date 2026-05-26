# AWS Certificate Manager

```
┌────────────────────────────────────── ACM — Certificate Manager ──────────────────────────────────────┐
│                                                                                                       │
│  ACM provisions, manages, and renews TLS certificates for AWS services at no charge.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Certificate Types               │  │              Validation Methods             │   │
│   │         Public: trusted by browsers          │  │        DNS: add CNAME to hosted zone        │   │
│   │        Private: ACM Private CA issued        │  │      Email: domain owner email approval     │   │
│   │      Imported: bring own cert/key pair       │  │       DNS preferred: auto-renews cert       │   │
│   │        Wildcard: *.example.com scope         │  │        Route 53: one-click CNAME add        │   │
│   │        SAN: multi-domain single cert         │  │        Pending validation: up to 72h        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  ACM auto-renews DNS-validated certs 60 days before expiry; no manual renewal needed.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Deployment Targets              │  │             Monitoring & Alerts             │   │
│   │       ALB: HTTPS listener certificate        │  │      CloudWatch: days to expiry metric      │   │
│   │       CloudFront: us-east-1 cert only        │  │        EventBridge: cert expiry event       │   │
│   │       API Gateway: custom domain cert        │  │     Config rule: acm-certificate-expiry     │   │
│   │        AppSync / Cognito domain cert         │  │       SNS: alert 30 days before expiry      │   │
│   │     EC2 (imported only; not ACM-managed)     │  │         Security Hub: cert findings         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Certificate Manager infrastructure · ACM Private CA HSM hardware · Regional endpoints            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ACM             = AWS Certificate Manager; free TLS certs for integrated AWS services                │
│  Public cert     = Browser-trusted cert issued by Amazon root CA; free to provision                   │
│  Private CA      = ACM Private CA; issues internal certs for private services                         │
│  DNS validation  = Proves domain ownership by adding a CNAME record to DNS                            │
│  Email validation= Sends approval email to WHOIS contacts; expires if not confirmed                   │
│  SAN             = Subject Alternative Name; multi-domain cert (up to 10 SANs in ACM)                 │
│  Wildcard cert   = Single cert for *.domain.com; covers all one-level subdomains                      │
│  Auto-renewal    = ACM renews DNS-validated certs automatically 60 days before expiry                 │
│  Imported cert   = Third-party cert uploaded to ACM; manual renewal required                          │
│  CloudFront cert = ACM certs for CloudFront must be in us-east-1 regardless of region                 │
│  DaysToExpiry    = CloudWatch metric for imported certs; monitor for upcoming expiry                  │
│  Certificate pinning= Not supported with ACM managed certs due to auto-rotation                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Certificate Manager notes for day-to-day infrastructure operations.

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
