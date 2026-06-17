# Usage Metrics

<div class="kb-summary">
Knowledge base statistics: page counts, section distribution, and content type coverage.
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
│   │  Total pages:       2,599   │  │  Storage:          709       │  │  ASCII diagrams:     2,593  │  │
│   │  Sections:             11   │  │  Virtualization:   685       │  │  Pages with tables:  1,985  │  │
│   │  Avg pages/section:   236   │  │  Cloud:            295       │  │  Mermaid diagrams:     676  │  │
│   │  Updated 2026-06-17         │  │                              │  │  kb-summary divs:    2,319  │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Section          │  Pages  │  Section            │  Pages  │  Section          │  Pages     │   │
│   │   Storage          │   709   │  SAN                │   136   │  Backup           │   103      │   │
│   │   Virtualization   │   685   │  ITSM               │   153   │  Networking       │    83      │   │
│   │   Cloud            │   295   │  Security           │   113   │  Certifications   │    14      │   │
│   │   Compute          │   175   │  Automation         │   126   │                   │            │   │
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

Generated: 2026-06-17

## Current totals

| Metric | Count |
|---|---:|
| Total markdown pages | 2,599 |
| Sections | 11 |
| Pages with full-width ASCII diagrams | 2,593 |
| Pages with kb-summary | 2,319 |
| Pages with Mermaid diagrams | 676 |
| Pages with formatted tables | 1,985 |

## Section page counts

| Section | Pages |
|---|---:|
| Storage | 709 |
| Virtualization | 685 |
| Cloud | 295 |
| Compute | 175 |
| ITSM | 153 |
| SAN | 136 |
| Automation | 126 |
| Security | 113 |
| Backup | 103 |
| Networking | 83 |
| Certifications | 14 |

## Health checks

Run:

./validate-site.sh
./audit-site.sh
./preview-site.sh
