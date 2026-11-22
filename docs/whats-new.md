---
tags:
  - meta
search:
  boost: 2
description: "Recent additions and updates to the knowledge base. Major changes by date — newest first. Auto-updated from commit history."
---
# What's New

*Applies to: All products*

<div class="kb-summary">
Recent additions and updates to the knowledge base. Major changes by date — newest first.

Subscribe via <a href="../feed_rss_updated.xml">RSS</a> to get updates outside the browser.
</div>

![What's New](assets/whats-new.svg)

## November 2026

### 2026-11-21 — Site fixes

- Search works again for common terms like "VMware", "vSAN" and "storage". A duplicate page was breaking it.
- The full [VxRail — How It Works](virtualization/vmware/products/vxrail/architecture/how-it-works.md) page is visible again. The shorter overview moved to [Cluster Software Stack](virtualization/vmware/products/vxrail/architecture/cluster-software-stack.md).
- FAQ pages: fixed the "Operations" link and removed a repeated diagram.
- Search downloads less data, so it starts faster on phones.
- Shared links now show a preview image.

---

## July 2026

### 2026-07-10 — Sections reorganized by product

Backup, storage, security and VMware are now organized as `products/` plus shared cross-product pages. Certification material moved to [Certifications](certifications/index.md).

---

### 2026-07-12 — Easier to find and share

- Meta descriptions added to about 2,500 pages.
- [RSS feed](../feed_rss_updated.xml) for this page.
- Structured data on every page for search engines.
- Accessibility fixes from a Lighthouse pass: color contrast and the search dialog label.

---

### 2026-07-03 — Diagram cleanup

- 137 Mermaid subgraph diagrams replaced with cleaner layered SVGs.
- Fixed clipped or overflowing text in SVG diagrams across the site.
- Diagram readability pass: clearer colors and glossary coverage for FlashArray and NetApp ONTAP terms.

---

### 2026-07-01 — Hover definitions and new diagram types

- Hover over abbreviations anywhere on the site to see what they mean.
- Mermaid, D2, PlantUML and Vega-Lite diagrams rendered via Kroki.
- Video links on related pages, and tabbed content (UI / CLI).

---

## June 2026

### 2026-06-29 — Example command output

Commands across storage, SAN, cloud, compute, VMware, ITSM and security pages now show example output (1,373 pages), so you can see what a healthy result looks like.

---

### 2026-06-28 — Link and diagram fixes

- Fixed about 2,400 broken "See also" links.
- Diagrams no longer clip on narrow screens.
- Narrow top-down Mermaid diagrams (610) redrawn to read better.
- Vega-Lite threshold charts on 23 health-check pages.

---

### 2026-06-27 — Sequence diagrams

Product-specific PlantUML sequence diagrams added to architecture pages, showing how components talk to each other step by step.

---

### 2026-06-26 — More visuals

- 272 ASCII diagrams converted to SVG.
- Step-flow diagrams on 62 deploy pages.
- FAQ answers turned into comparison tables where it helps.

---

### 2026-06-25 — FAQ pages

FAQ pages added under each product's Operations section.

---

### 2026-06-21 — Full SVG coverage: every page now has a diagram

All 2,639 pages now have at least one SVG diagram. New scripts generate section-overview diagrams for every landing page, subsection card-nav page, and content page across all products and page types.

**New scripts:** `generate_svgs_remaining.py`, `generate_svgs_content.py`, `generate_svgs_learning.py`
**Total SVGs:** 3,385

---

### 2026-06-21 — Architecture page SVG coverage

Added SVGs to all `how-it-works.md`, `design-standards.md`, and `integrations.md` pages across all 54 products (161 SVGs).

---

### 2026-06-21 — Content coverage expansion

- **ONTAP Deploy guide** — full 7-phase deployment from physical racking to validated cluster
- **6 product procedure fills** — SnapMirror, SnapCenter, FlashBlade, PowerScale, Fabric-OS, PowerStore

---

### 2026-06-21 — SVG expansion project complete

1,385 SVGs added across procedures, health-checks, security, and troubleshooting pages for all products. Site audit: 37/37 checks clean.

---

### 2026-06-18 — KB Spectacular project complete

All 7 tracks shipped:

| Track | What |
|---|---|
| Tags | Every page tagged; tag cloud on index |
| Cheat sheets | 15 VMware CLI quick-reference pages |
| Interaction map | VMware product relationship map |
| Decision trees | 4 Mermaid troubleshooting flowcharts |
| Glossary | 155+ term full-stack glossary |
| Version matrix | 65+ feature/version compatibility table |
| Lab guides | 4 nested VMware lab walkthroughs |

---

### 2026-06-17 — Site audit expanded to 37 checks

Added Checks 29–37 covering heading hierarchy, broken links, anchor fragments, "See Also" validity, "Verify" sections on procedures pages, and health-check "Run This Routine" blocks.

Fixed 453 broken See Also links, 63 heading hierarchy violations, and 22 untagged pages.

---

### 2026-06-17 — Procedure depth: VMware products

Added missing procedures across vCenter, ESXi, NSX, VxRail, SRM, Aria stack, Horizon, Tanzu, VCF, and PowerCLI. Coverage target: every common admin task documented.

---

### 2026-06-16 — Known issues audit complete

Replaced all 71 placeholder diagrams with real product-specific known-issues diagrams across 91 pages.

---

### 2026-06-16 — Orphaned section merge

142 pages merged into correct product sections. Check 22 (orphan detection) verified clean.

---

### 2026-06-16 — New platform sections

OpenShift, EVS, and Ceph sections built (25 files each, full template structure).

---

### 2026-06-15 — Cross-references added

"## See also" added to 83 non-card-nav content pages across security, storage, networking, compute, backup, cloud, and certifications sections.

---

### 2026-06-13 — KB Usability project complete

All 8 tracks done: copy buttons, version labels, prerequisites, success criteria, diagnostic flowcharts, cross-references, morning health-check runbook, risk warnings.

---

## See also

- [Site Quality](site-quality.md)
- [Glossary](reference/glossary/index.md)
- [Version Matrix](reference/versions/index.md)
