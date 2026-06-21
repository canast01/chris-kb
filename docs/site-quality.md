# Site Quality Dashboard

<div class="kb-summary">
Quality gates and content standards for the chrisanastasiadis.com knowledge base.
</div>

```text
┌────────────────────────────────────── KB Site Quality Dashboard ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Quality gates and content standards for the chrisanastasiadis.com knowledge base        │   │
│   │              37-check automated audit · pre-commit hooks · GitHub Actions CI                  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │     Structure Rules         │  │      Content Rules           │  │       CI / Tooling          │  │
│   │     ─────────────           │  │      ─────────────           │  │       ─────────────         │  │
│   │  Every page in nav          │  │  ≥ 3 ## sections on CLI pg  │  │  site_audit.py (37 checks)  │   │
│   │  index.md → card grid only  │  │  ≥ 1 code block on CLI pg   │  │  pre-commit hooks (5 rules) │   │
│   │  No raw kb-grid in content  │  │  Mermaid via fenced block    │  │  GitHub Actions CI pipeline │  │
│   │  Products under vendor nav  │  │  Tags on every content page  │  │  MkDocs strict build check  │  │
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
│    Physical: GitHub Pages / Cloudflare CDN · MkDocs Material build · Actions CI pipeline              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    kb-summary      = Required <div> block on every page; summarises content for search/nav            │
│    kb-card         = Anchor-style card (<a class="kb-card">) used in landing page grids               │
│    kb-grid         = Card grid container; appears on index.md pages only, never content pages         │
│    CLI reference   = Page with commands, flags, and examples; must have ≥ 3 sections + code block     │
│    Mermaid         = Diagram syntax rendered by mkdocs-material; must use fenced ```mermaid block     │
│    site_audit.py   = 37-check automated audit; run before committing or after bulk changes            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Generated: 2026-06-21

## Current state

| Item | Count |
|---|---:|
| Total markdown pages | 2,639 |
| Sections | 11 |
| Pages with kb-summary | 2,359 |
| Pages with full-width ASCII diagram | 1,682 |
| Pages with SVG diagrams | 1,131 |
| Pages with Mermaid diagrams | 680 |
| Pages with tags | 2,612 |
| Audit score | 36 / 37 |
| MkDocs strict build warnings | 0 |

## Pages by section

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

## Quality rules

- Every page should be reachable from the left nav.
- Landing pages (`index.md`) must have a card grid linking to sub-pages using `<a class="kb-card">` anchor style only — no `<div class="kb-card">`.
- Keep the left nav light — section landing pages are the entry point.
- Product pages stay under their vendor/platform landing page.
- No raw HTML card blocks (`kb-grid`, `kb-card`) in content pages — card grids belong on index pages only.
- All CLI reference pages must have at least 3 `##` sections and at least one fenced code block.
- Mermaid flowcharts are added via fenced ` ```mermaid ` blocks — do not use raw HTML `<div class="mermaid">`.
- Every content page must have at least one product tag and one domain tag.
- Run `python3 scripts/site_audit.py` before bulk changes and after.

## Useful commands

```bash
python3 scripts/site_audit.py          # full 37-check audit
python3 scripts/site_audit.py --full   # include all issue details
mkdocs build --strict                  # strict build check
mkdocs serve                           # local preview
```
