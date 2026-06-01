# Usage Metrics


<div class="kb-summary">
Usage Metrics reference covering Current totals, Section growth, Health checks.
</div>
```
┌────────────────────────────────────────── KB Usage Metrics ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Knowledge base statistics: page counts, section distribution, and content type coverage  │   │
│   │                   Run ./audit-site.sh to regenerate; reflects last deploy                     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Content Totals        │  │      Top 3 Sections          │  │      Content Types          │   │
│   │       ─────────────         │  │      ─────────────           │  │      ─────────────          │   │
│   │  Total pages:       2,100+  │  │  Storage:          346       │  │  Mermaid flowcharts: 1,206  │   │
│   │  Sections:             27   │  │  Virtualization:   344       │  │  Formatted tables:   1,023  │   │
│   │  CLI reference pages:  251  │  │  Cloud:            223       │  │  CLI reference pages:  251  │   │
│   │  Pages per section:    78   │  │  Disaster Recovery: 134      │  │  ASCII diagrams:     129+   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Section          │  Pages  │  Section            │  Pages  │  Section          │  Pages     │   │
│   │   Storage          │   346   │  Monitoring         │   100   │  Tools            │    36      │   │
│   │   Virtualization   │   344   │  Security           │    74   │  Compute          │    34      │   │
│   │   Cloud            │   223   │  SAN                │    70   │  Project Mgmt     │    33      │   │
│   │   Disaster Rcvry   │   134   │  Automation         │    67   │  Certifications   │    37      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Health: ./validate-site.sh · ./audit-site.sh · ./preview-site.sh                                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Section         = Top-level KB area (Storage, Virtualization, Cloud, etc.)                        │
│    CLI reference   = Page with CLI commands, flags, and usage examples                               │
│    Mermaid         = Flowchart or sequence diagram embedded in a fenced mermaid block                │
│    ASCII diagram   = Full-width box-drawing architecture diagram (103+ chars wide)                   │
│    audit-site.sh   = Script that counts pages, checks structure, and flags quality issues            │
│    validate-site.sh= Strict MkDocs build check; run before every commit                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Generated: 2026-05-07

## Current totals

| Metric | Count |
|---|---:|
| Total markdown pages | 1720 |
| Sections | 27 |
| Pages with Mermaid flowcharts | 1206 |
| Pages with formatted tables | 1023 |
| CLI reference pages | 251 |

## Section growth

| Section | Pages |
|---|---:|
| Storage | 346 |
| Virtualization | 344 |
| Cloud | 223 |
| Disaster Recovery | 134 |
| Monitoring | 100 |
| Security | 74 |
| SAN | 70 |
| Automation | 67 |
| Protocols | 61 |
| Certifications | 37 |
| Tools | 36 |
| Compute | 34 |
| Project Management | 33 |
| AI | 32 |
| Standards | 31 |
| Networking | 15 |
| Troubleshooting | 9 |
| Database | 8 |
| Change Management | 8 |
| Integration | 8 |
| Lifecycle | 8 |
| Runbooks | 8 |
| Inventory | 8 |
| Data Protection | 8 |
| Performance | 8 |
| Architecture | 5 |
| Start Here | 1 |

## Health checks

Run:

./validate-site.sh
./audit-site.sh
./preview-site.sh
