# Usage Metrics


<div class="kb-summary">
Usage Metrics reference covering Current totals, Section growth, Health checks.
</div>
```text
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
│   │       Content Totals        │  │      Top 3 Sections          │  │      Content Types          │  │
│   │       ─────────────         │  │      ─────────────           │  │      ─────────────          │  │
│   │  Total pages:       2,100+  │  │  Storage:          346       │  │  Mermaid flowcharts: 1,206  │  │
│   │  Sections:             27   │  │  Virtualization:   344       │  │  Formatted tables:   1,023  │  │
│   │  CLI reference pages:  251  │  │  Cloud:            223       │  │  CLI reference pages:  251  │  │
│   │  Pages per section:    78   │  │  Disaster Recovery: 134      │  │  ASCII diagrams:     129+   │  │
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
│    Health: ./validate-site.sh · ./audit-site.sh · ./preview-site.sh                                   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Section         = Top-level KB area (Storage, Virtualization, Cloud, etc.)                         │
│    CLI reference   = Page with CLI commands, flags, and usage examples                                │
│    Mermaid         = Flowchart or sequence diagram embedded in a fenced mermaid block                 │
│    ASCII diagram   = Full-width box-drawing architecture diagram (103+ chars wide)                    │
│    audit-site.sh   = Script that counts pages, checks structure, and flags quality issues             │
│    validate-site.sh= Strict MkDocs build check; run before every commit                               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Generated: 2026-06-01

## Current totals

| Metric | Count |
|---|---:|
| Total markdown pages | 2,122 |
| Sections | 27 |
| Pages with full-width ASCII diagrams | 1,984 |
| Pages with formatted tables | 1,410 |
| Pages with code examples | 1,132 |
| Pages with Mermaid diagrams | 455 |

## Section growth

| Section | Pages |
|---|---:|
| Virtualization | 448 |
| Storage | 434 |
| Cloud | 223 |
| Disaster Recovery | 199 |
| Monitoring | 118 |
| SAN | 113 |
| Automation | 107 |
| Security | 96 |
| Tools | 85 |
| Protocols | 61 |
| Compute | 45 |
| Certifications | 38 |
| Project Management | 33 |
| AI | 32 |
| Troubleshooting | 9 |
| Change Management | 8 |
| Data Protection | 8 |
| Database | 8 |
| Integration | 8 |
| Inventory | 8 |
| Lifecycle | 8 |
| Performance | 8 |
| Runbooks | 8 |
| Architecture | 5 |
| Networking | 5 |
| Start Here | 1 |
| Stats | 1 |

## Health checks

Run:

./validate-site.sh
./audit-site.sh
./preview-site.sh
