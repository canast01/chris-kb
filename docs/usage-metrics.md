# Usage Metrics

<div class="kb-summary">
Knowledge base statistics: page counts, section distribution, and content type coverage.
</div>

```text
┌────────────────────────────────────────── KB Usage Metrics ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Knowledge base statistics: page counts, section distribution, and content type coverage  │   │
│   │              Run python3 scripts/site_audit.py to regenerate; reflects last audit             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Content Totals        │  │      Top 3 Sections          │  │      Content Types          │  │
│   │       ─────────────         │  │      ─────────────           │  │      ─────────────          │  │
│   │  Total pages:       2,638   │  │  Storage:          709       │  │  ASCII diagrams:     2,623  │  │
│   │  Sections:             13   │  │  Virtualization:   685       │  │  SVG diagrams:         123  │  │
│   │  Avg pages/section:   236   │  │  Cloud:            295       │  │  Mermaid diagrams:     680  │  │
│   │  Updated 2026-06-18         │  │                              │  │  kb-summary divs:    2,358  │  │
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
│    Audit: python3 scripts/site_audit.py (37 checks) · Score: 36/37 clean                              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Section         = Top-level KB area (Storage, Virtualization, Cloud, etc.)                         │
│    CLI reference   = Page with CLI commands, flags, and usage examples                                │
│    Mermaid         = Flowchart or sequence diagram embedded in a fenced mermaid block                 │
│    ASCII diagram   = Full-width box-drawing architecture diagram (105 chars wide)                     │
│    SVG diagram     = Vector diagram in docs/assets/; injected via markdown image reference            │
│    site_audit.py   = 37-check automated audit; covers structure, content, links, and quality          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Generated: 2026-06-18

## Current totals

| Metric | Count |
|---|---:|
| Total markdown pages | 2,638 |
| Sections | 11 |
| Pages with full-width ASCII diagrams | 2,623 |
| Pages with SVG diagrams | 123 |
| Pages with Mermaid diagrams | 680 |
| Pages with kb-summary | 2,358 |
| Pages with tags | 2,611 |
| Audit score | 36 / 37 |

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

```bash
python3 scripts/site_audit.py          # full 37-check audit
python3 scripts/site_audit.py --full   # include all issue details
mkdocs build --strict                  # strict build check
mkdocs serve                           # local preview
```
