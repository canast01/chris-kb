# SAN Certification Review Plan


<div class="kb-summary">
SAN Certification Review Plan reference covering Target Certifications, Study Resources, 8-Week SAN Study Plan, Hands-On Lab Options, Study Checklist.
</div>
```
┌─────────────────────────────────── Certifications San Review Plan ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                          San: Certifications San Review Plan platform                         │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                 Management: Certifications San Review Plan management console                 │   │
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
│    Physical: Certifications San Review Plan infrastructure · management network · monitoring          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    San                = Certifications San Review Plan platform overview and core concepts            │
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


## Target Certifications

| Certification | Vendor | Level | Notes |
|---|---|---|---|
| Brocade Certified Fabric Professional (BCFP) | Broadcom / Brocade | Professional | FC fabric design and troubleshooting |
| Cisco Certified Network Professional — Data Center (CCNP DC) | Cisco | Professional | Includes SAN (DCSAN exam 300-625) |
| EMC Proven Professional | Dell / EMC | Various | Storage array + SAN design tracks |
| NetApp Certified SAN Specialist (NCSS) | NetApp | Specialist | ONTAP SAN protocol implementation |

## Study Resources

| Resource | Type | URL / Location |
|---|---|---|
| Broadcom FOS Administration Guide | Vendor documentation | support.broadcom.com |
| Cisco MDS 9000 NX-OS Configuration Guide | Vendor documentation | cisco.com/c/en/us/support |
| SNIA Training Courses | Standards body training | snia.org/education |
| "Fibre Channel for Beginners" (SNIA) | White paper | snia.org |
| Cisco DCSAN (300-625) Exam Topics | Official exam blueprint | cisco.com/go/certifications |
| Brocade SAN Design Guide | Architecture reference | support.broadcom.com |
| INE / CBT Nuggets SAN courses | Video training | ine.com, cbtnuggets.com |

## 8-Week SAN Study Plan

| Week | Focus | Topics |
|---|---|---|
| Week 1 | FC fundamentals | Layers FC-0 through FC-4, port types, WWN |
| Week 2 | Fabric login and addressing | FLOGI, PLOGI, PRLI, FCID structure, Name Server |
| Week 3 | Zoning | Zone types, zone sets, hard vs soft, WWPN vs port zoning |
| Week 4 | Fabric design | ISL, trunk groups, VSAN/Virtual Fabric, domain IDs |
| Week 5 | Vendor-specific: Brocade | FOS CLI, switchshow, zoneshow, portcfg, fabric merge |
| Week 6 | Vendor-specific: Cisco | NX-OS VSAN, DPVM, zone configuration, IVR |
| Week 7 | Troubleshooting scenarios | FLOGI failures, zone not active, ISL down, BB_Credit |
| Week 8 | Practice exams and review | Full practice sets, review flagged topics |

## Hands-On Lab Options

| Lab Option | Notes |
|---|---|
| GNS3 / EVE-NG with Cisco MDS images | Requires licensed Cisco NX-OS images |
| Cisco DevNet sandbox | Free MDS 9000 lab environments |
| Brocade vLAB | Contact Broadcom partner portal for access |
| Physical lab access (work environment) | Best option — use production SAN in maintenance windows |
| VMware vSphere lab with software iSCSI | Simulates SAN concepts without FC hardware |

## Study Checklist

- [ ] Read Brocade FOS Administration Guide chapters: Zoning, Fabric, Troubleshooting
- [ ] Read Cisco MDS NX-OS SAN Switching Configuration Guide: VSAN and Zoning chapters
- [ ] Complete the SNIA Fibre Channel overview white paper
- [ ] Practice at least 20 zoning scenario questions
- [ ] Do hands-on: create zones, activate zone set, add/remove members
- [ ] Practice troubleshooting: simulate a zone not active and ISL down scenario
- [ ] Review Cisco DCSAN 300-625 exam blueprint for topic weights
