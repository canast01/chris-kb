---
tags:
  - aws
  - certifications
---
# AWS Certification Review Plan


<div class="kb-summary">
AWS Certification Review Plan reference covering Target Exam and Study Timeline, AWS Skill Builder, Key Whitepapers, Practice Exam Resources, AWS Labs and 1 more sections.
</div>
```text
┌─────────────────────────────────── Certifications Aws Review Plan ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                          Aws: Certifications Aws Review Plan platform                         │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                 Management: Certifications Aws Review Plan management console                 │   │
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
│    Physical: Certifications Aws Review Plan infrastructure · management network · monitoring          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Aws                = Certifications Aws Review Plan platform overview and core concepts            │
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


## Target Exam and Study Timeline

Recommended plan for AWS Solutions Architect Associate (SAA-C03):

| Week | Focus Domain | Activities | Target |
|---|---|---|---|
| Week 1 | Security (30%) | IAM, KMS, VPC security, WAF, Shield | Know policy evaluation order |
| Week 2 | Resilient Architectures (26%) | Multi-AZ, Auto Scaling, Route 53, SQS/SNS | Design HA patterns |
| Week 3 | High-Performing Architectures (24%) | EC2 types, RDS, DynamoDB, ElastiCache, CloudFront | Match workload to service |
| Week 4 | Cost Optimization (20%) | Reserved vs On-Demand vs Spot, S3 storage classes, Trusted Advisor | Estimate cost trade-offs |
| Week 5 | Full mock exams | Tutorialsdojo, Whizlabs practice sets | Score 75%+ |
| Week 6 | Weak area review + final practice | Review flagged questions, re-read whitepaper sections | Score 82%+ |

## AWS Skill Builder

- Free tier: Digital training courses, exam prep for Foundational and some Associate exams
- Enhanced subscription ($29/month): All exam prep courses, official practice exams, labs
- Focus paths: "Solutions Architect – Associate Learning Plan", "Cloud Practitioner Essentials"
- Official Practice Exam: 20–65 questions depending on exam; counts toward exam prep score

## Key Whitepapers

| Whitepaper | Relevant Exams | Key Topics |
|---|---|---|
| AWS Well-Architected Framework | All | 6 pillars: operational excellence, security, reliability, performance, cost, sustainability |
| AWS Security Best Practices | SAA, Security Specialty | IAM, data protection, incident response |
| Disaster Recovery Whitepaper | SAA, SA Pro | RTO/RPO, DR strategies (Backup/Restore, Pilot Light, Warm Standby, Multi-Site) |
| AWS Storage Services Overview | SAA | S3, EBS, EFS, FSx selection guidance |

## Practice Exam Resources

- **Tutorialsdojo** (tutorialsdojo.com): Highly recommended; cheat sheets + practice sets
- **Whizlabs** (whizlabs.com): Large question bank; good for breadth
- **AWS Official Practice** (via Skill Builder): Closest to real exam format
- **Udemy — Stephane Maarek**: Practice exams with detailed explanations
- **ExamTopics**: Community answers; verify all answers independently

## AWS Labs

- **AWS Free Tier**: 12-month free tier covers EC2 t2.micro, S3, RDS db.t2.micro, Lambda requests
- **AWS Workshops** (workshops.aws): Hands-on labs for specific services
- **Skill Builder Labs**: Guided, sandboxed environment — no credit card risk
- **A Cloud Guru / Linux Academy**: Virtual sandbox environments included in subscription

## Study Checklist

- [ ] Book exam date 6–8 weeks out to create study urgency
- [ ] Complete AWS Skill Builder domain-specific learning paths
- [ ] Read the Well-Architected Framework whitepaper (all 6 pillars)
- [ ] Read the DR whitepaper — know all 4 strategies with RTO/RPO characteristics
- [ ] Do at least one hands-on lab per major service category
- [ ] Complete 3 full practice exam sets; log scores by domain
- [ ] Spend final week only on weak domains and exam strategy
