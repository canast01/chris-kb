# Site Quality Dashboard

Generated: 2026-05-07

## Current state

| Item | Count |
|---|---:|
| Total markdown pages | 1720 |

## Pages by section

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
