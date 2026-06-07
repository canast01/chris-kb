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
│   │  Total pages:       2,200+  │  │  Storage:          600       │  │  ASCII diagrams:     2,050+ │  │
│   │  Sections:             16   │  │  Virtualization:   529       │  │  Formatted tables:   1,410  │  │
│   │  Avg pages/section:   138   │  │  Cloud:            225       │  │  Code examples:      1,132  │  │
│   │  New 2026-06-07:      +66   │  │                              │  │  Mermaid diagrams:     455  │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Section          │  Pages  │  Section            │  Pages  │  Section          │  Pages     │   │
│   │   Storage          │   600   │  SAN                │   121   │  Certifications   │    39      │   │
│   │   Virtualization   │   529   │  ITSM               │   112   │  AI               │    32      │   │
│   │   Cloud            │   225   │  Security           │    97   │  Monitoring Std   │    20      │   │
│   │   Compute          │   140   │  Backup             │    80   │  Networking       │     8      │   │
│   │   Automation       │   134   │  Protocols          │    65   │                   │            │   │
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

Generated: 2026-06-07

## Current totals

| Metric | Count |
|---|---:|
| Total markdown pages | ~2,200 |
| Sections | 16 |
| Pages with full-width ASCII diagrams | ~2,050 |
| Pages with formatted tables | 1,410 |
| Pages with code examples | 1,132 |
| Pages with Mermaid diagrams | 455 |

## Section growth

| Section | Pages |
|---|---:|
| Storage | 600 |
| Virtualization | 529 |
| Cloud | 225 |
| Compute | 140 |
| Automation | 134 |
| SAN | 121 |
| ITSM | 112 |
| Security | 97 |
| Backup | 80 |
| Protocols | 65 |
| Certifications | 39 |
| AI | 32 |
| Monitoring Standards | 20 |
| Networking | 8 |
| Start Here | 1 |
| Stats | 1 |

## Health checks

Run:

./validate-site.sh
./audit-site.sh
./preview-site.sh
