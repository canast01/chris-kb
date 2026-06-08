# Azure Certification Review Plan


<div class="kb-summary">
Azure Certification Review Plan reference covering Recommended Study Path, 8-Week AZ-104 Study Schedule, Microsoft Learn Resources, Sandbox and Lab Options, Practice Assessment Resources and 1 more sections.
</div>
```text
┌────────────────────────────────── Certifications Azure Review Plan ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        Azure: Certifications Azure Review Plan platform                       │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                Management: Certifications Azure Review Plan management console                │   │
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
│    Physical: Certifications Azure Review Plan infrastructure · management network · monitoring        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Certifications Azure Review Plan platform overview and core concepts          │
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


## Recommended Study Path

| Stage | Exam | Prerequisites | Suggested Duration |
|---|---|---|---|
| 1 | AZ-900 Fundamentals | None | 2–4 weeks |
| 2 | AZ-104 Administrator | AZ-900 or equivalent experience | 6–8 weeks |
| 3 | AZ-305 Architect Expert | AZ-104 required | 8–10 weeks |

## 8-Week AZ-104 Study Schedule

| Week | Domain | Focus Topics |
|---|---|---|
| Week 1 | Identity and Governance | AAD/Entra, RBAC, Policy, Management Groups |
| Week 2 | Identity and Governance | Subscriptions, Cost Management, Locks, Blueprints |
| Week 3 | Storage | Storage accounts, Blob, File Sync, AzCopy, SAS |
| Week 4 | Compute | VMs, VMSS, Azure App Service, Container Instances, AKS |
| Week 5 | Networking | VNets, NSG, ASG, UDR, VPN Gateway, ExpressRoute |
| Week 6 | Networking + Monitor | Peering, DNS, Network Watcher, Azure Monitor, Log Analytics |
| Week 7 | Full practice exams | Tutorialsdojo, Whizlabs, Microsoft Learn assessments |
| Week 8 | Weak area review | Targeted review of lowest-scoring domains |

## Microsoft Learn Resources

- **Microsoft Learn paths** (learn.microsoft.com): Free, official; search by exam code (e.g., "AZ-104")
- **Learning paths include**: Sandbox exercises with free Azure resources (no subscription needed)
- **Microsoft Applied Skills**: Scenario-based credentials for hands-on labs
- **Microsoft Official Curriculum (MOC)**: Available through authorized training partners
- **Exam Study Guide**: Download PDF from the exam page on learn.microsoft.com — always current

## Sandbox and Lab Options

| Platform | Cost | Notes |
|---|---|---|
| Microsoft Learn Sandbox | Free | Limited resource types; no subscription required |
| Azure Free Account | Free 12 months | $200 credit + free tier services; requires credit card |
| Visual Studio Dev Essentials | Free | Monthly Azure credits ($25–$150 depending on tier) |
| A Cloud Guru / Pluralsight | Subscription | Guided Azure sandboxes |
| Tutorialsdojo Labs | Subscription | Scenario-based Azure labs |

## Practice Assessment Resources

- **Microsoft Learn Practice Assessments**: Free, official; 50 questions per exam (learn.microsoft.com/certifications/practice-assessments-for-microsoft-certifications)
- **Tutorialsdojo Azure exams**: Best third-party option; detailed explanations
- **Whizlabs Azure**: Good breadth; less detailed explanations
- **MeasureUp**: Official Microsoft partner practice tests; same format as real exam
- **Udemy — Alan Rodrigues / Neil Davis**: Popular instructor-based courses with practice exams

## Study Checklist

- [ ] Download the official exam study guide PDF from Microsoft Learn
- [ ] Complete the Microsoft Learn path for target exam code
- [ ] Do all sandbox exercises in Microsoft Learn modules
- [ ] Complete 3 practice assessment sets; log domain-level scores
- [ ] Identify the two lowest-scoring domains and do targeted review
- [ ] Schedule renewal reminder in calendar for 6 months after pass date
- [ ] Review Microsoft Azure pricing calculator for cost-optimization questions
