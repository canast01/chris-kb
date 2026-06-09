# Site Quality Dashboard

<div class="kb-summary">
Quality gates and content standards for the chrisanastasiadis.com knowledge base.
</div>

```text
┌────────────────────────────────────── KB Site Quality Dashboard ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Quality gates and content standards for the chrisanastasiadis.com knowledge base        │   │
│   │                Every page reachable from nav · no raw HTML · fenced code only                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │     Structure Rules         │  │      Content Rules           │  │       CI / Tooling          │  │
│   │     ─────────────           │  │      ─────────────           │  │       ─────────────         │  │
│   │  Every page in nav          │  │  ≥ 3 ## sections on CLI pg  │  │  validate-site.sh before    │   │
│   │  index.md → card grid only  │  │  ≥ 1 code block on CLI pg   │  │  commit (strict build)      │   │
│   │  No raw kb-grid in content  │  │  Mermaid via fenced block    │  │  audit-site.sh for counts   │  │
│   │  Products under vendor nav  │  │  No raw HTML mermaid divs    │  │  preview-site.sh to check   │  │
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
│    Physical: GitHub Pages / Cloudflare CDN · MkDocs Material build · Actions CI pipeline              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    kb-summary      = Required <div> block on every page; summarises content for search/nav            │
│    kb-card         = Anchor-style card (<a class="kb-card">) used in landing page grids               │
│    kb-grid         = Card grid container; appears on index.md pages only, never content pages         │
│    CLI reference   = Page with commands, flags, and examples; must have ≥ 3 sections + code block     │
│    Mermaid         = Diagram syntax rendered by mkdocs-material; must use fenced ```mermaid block     │
│    validate-site.sh= Runs mkdocs build --strict; fails on any warning; run before every commit        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Generated: 2026-06-07

## Current state

| Item | Count |
|---|---:|
| Total markdown pages | ~2,200 |
| Sections | 16 |
| Pages with kb-summary | ~2,200 |
| Pages with full-width ASCII diagram | ~2,050 |
| MkDocs strict build warnings | 0 |

## Pages by section

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

## Quality rules

- Every page should be reachable from the left nav.
- Landing pages (`index.md`) must have a card grid linking to sub-pages using `<a class="kb-card">` anchor style only — no `<div class="kb-card">`.
- Keep the left nav light — section landing pages are the entry point.
- Product pages stay under their vendor/platform landing page.
- No raw HTML card blocks (`kb-grid`, `kb-card`) in content pages — card grids belong on index pages only.
- All CLI reference pages must have at least 3 `##` sections and at least one fenced code block.
- Mermaid flowcharts are added via fenced ` ```mermaid ` blocks — do not use raw HTML `<div class="mermaid">`.
- Run backup before bulk changes.
- Run strict validation before committing.

## Useful commands

./validate-site.sh
./audit-site.sh
./preview-site.sh
