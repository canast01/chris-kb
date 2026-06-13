---
tags:
  - azure
  - certifications
---
# Azure Certification



<div class="kb-summary">
Azure Certification reference covering Overview, Core Certification Paths, Daily Study Focus, Useful Commands, Renewal Notes.
</div>
```text
┌──────────────────────────────────────── Certifications Azure ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Azure: Certifications Azure platform                             │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                      Management: Certifications Azure management console                      │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Certifications Azure infrastructure · management network · monitoring                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Certifications Azure platform overview and core concepts                      │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


<div class="kb-grid kb-grid-1">

<a class="kb-card" href="exam-tracking/">
  <strong>Exam Tracking</strong>
  <span>Exam scheduling, scores, and certification tracking.</span>
</a>

<a class="kb-card" href="practice-notes/">
  <strong>Practice Notes</strong>
  <span>Practice exam notes and study materials.</span>
</a>

<a class="kb-card" href="review-plan/">
  <strong>Review Plan</strong>
  <span>Study plan and review schedule.</span>
</a>

<a class="kb-card" href="weak-areas/"><strong>Weak Areas</strong><span>Topics needing additional study and focus.</span></a>
<a class="kb-card" href="services/"><strong>Services</strong><span>Per-service study notes — Entra ID, VMs, VNet, Blob Storage, AKS, and more.</span></a>

</div>
## Overview

Azure certifications validate skills in managing Microsoft Azure infrastructure, networking, storage, and identity services.

## Core Certification Paths

- AZ-900 Fundamentals
- AZ-104 Administrator
- AZ-305 Architect
- AZ-500 Security

## Daily Study Focus

- Review Azure resource management
- Practice virtual networking scenarios
- Study identity and access management
- Review monitoring and backup services

## Useful Commands

```bash
az login
az vm list
az network vnet list
az storage account list
```

## Renewal Notes

Azure certifications typically require renewal annually through online assessment.
