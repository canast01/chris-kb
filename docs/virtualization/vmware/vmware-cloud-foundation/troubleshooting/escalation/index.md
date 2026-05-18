# VCF Troubleshooting — Escalation

```
VCF Escalation Workflow
┌─────────────────────────────────────────────────────┐
│  Before Opening SR — Collect:                       │
│                                                     │
│  ① SDDC Manager version (Admin → About)            │
│  ② SoS health check output                         │
│     sudo python3 /opt/vmware/sddc-support/sos       │
│       --health-summary                              │
│  ③ SDDC Manager support bundle                     │
│     vcf-support-bundle --type sddc                  │
│  ④ Component-specific bundle (NSX, vCenter)         │
│  ⑤ Timeline: last known good → first failure       │
│  ⑥ Screenshots of task failures or error messages   │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│  Broadcom Support Portal                            │
│  support.broadcom.com                               │
│                                                     │
│  S1 Production down        → 30 min response        │
│  S2 Major feature down     → 4 hour response        │
│  S3 Partial degradation    → next business day      │
│  S4 Question/enhancement   → next business day      │
│                                                     │
│  P1 escalation: duty manager via phone              │
│  TAM engagement if available                        │
└─────────────────────────────────────────────────────┘
```

VCF support is managed through the [Broadcom Support Portal](https://support.broadcom.com) under the VMware Cloud Foundation product line. When opening an SR, the SoS health check bundle and the SDDC Manager support bundle are the two most important artefacts — Broadcom support will almost always request these as the first action, so collecting them before opening the ticket saves significant time. The VCF Support Matrix (available on the Broadcom compatibility guide) must be referenced to confirm that the versions of vCenter, ESXi, NSX, and vSAN in your environment are a supported combination before filing lifecycle-related SRs.

## Information to Collect Before Opening an SR

- SDDC Manager version: Administration > About
- Affected component name and version
- SoS health check output: `python3 /opt/vmware/sddc-support/sos --health-summary`
- SDDC Manager support bundle: `vcf-support-bundle --type sddc`
- Component-specific support bundle if issue is isolated (e.g. NSX, vCenter)
- Timeline of events — last known good state, first observed failure, changes made
- Screenshot of SDDC Manager task failure or error message

## Support Tiers

| Severity | Description | Response SLA (Production) |
|---|---|---|
| S1 | Production down, no workaround | 30 minutes |
| S2 | Major feature unavailable | 4 hours |
| S3 | Partial degradation, workaround available | Next business day |
| S4 | General question or enhancement | Next business day |
