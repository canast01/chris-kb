#!/usr/bin/env python3
"""
Generate SVGs for every remaining page that has no SVG ref.

Covers:
  - index.md pages at every section level (parent dir name → SVG type)
  - Leftover content pages (procedures, health-checks, common-issues, etc.)
  - Miscellaneous pages (guide, alerts, capacity, upgrade-planning, …)

Usage:
  python3 scripts/generate_svgs_remaining.py --dry-run
  python3 scripts/generate_svgs_remaining.py
"""
import argparse
import re
from pathlib import Path
from xml.etree import ElementTree as ET

REPO   = Path(__file__).parent.parent.resolve()
DOCS   = REPO / 'docs'
ASSETS = REPO / 'docs' / 'assets'

NAVY      = '#1a2744'
GREEN     = '#2e7d32'
GREEN_L   = '#e8f5e9'
TEXT_DARK = '#1a2744'
TEXT_MID  = '#37474f'
TEXT_LIGHT= '#78909c'
FOOTER_FG = '#7a8fbb'

SVG_W = 820
SVG_H = 200
HDR_H = 42
FTR_H = 26
FTR_Y = SVG_H - FTR_H
BOX_Y = HDR_H + 14
BOX_H = 58
PAD   = 18
ARW_W = 14


def _cfg(subtitle, footer, boxes):
    return {'subtitle': subtitle, 'footer': footer, 'boxes': boxes}


B = {
    'blue'  : ('#e3f2fd', '#1565c0'),
    'indigo': ('#e8eaf6', '#3949ab'),
    'amber' : ('#fff8e1', '#f57f17'),
    'red'   : ('#fce4ec', '#c62828'),
    'green' : (GREEN_L,   GREEN),
    'teal'  : ('#e0f2f1', '#00695c'),
    'purple': ('#f3e5f5', '#6a1b9a'),
    'orange': ('#fff3e0', '#e65100'),
}


def _box(label1, label2, color):
    fill, stroke = B[color]
    return (label1, label2, fill, stroke)


# ── SVG configs keyed by parent-dir OR filename stem ──────────────────────────

SECTION_TYPES = {
    # Section landing pages (parent dir = section name)
    'operations': _cfg('Operations Overview', 'Operations',
        [_box('Health', 'Checks', 'blue'), _box('Procedures', '', 'indigo'),
         _box('CLI', 'Reference', 'amber'), _box('Scripts', '', 'red'),
         _box('✓ Lifecycle', '', 'green')]),

    'troubleshooting': _cfg('Troubleshooting Overview', 'Troubleshooting',
        [_box('Symptoms', '& Triage', 'blue'), _box('Diagnostics', '', 'indigo'),
         _box('Known', 'Issues', 'amber'), _box('Escalation', '', 'red'),
         _box('✓ Resolved', '', 'green')]),

    'security': _cfg('Security Overview', 'Security',
        [_box('Access', 'Control', 'blue'), _box('Authentication', '', 'indigo'),
         _box('Encryption', '', 'amber'), _box('Hardening', '', 'red'),
         _box('✓ Secured', '', 'green')]),

    'deploy': _cfg('Deployment Overview', 'Deploy',
        [_box('Planning', '& Pre-Check', 'blue'), _box('Install', '& Stage', 'indigo'),
         _box('Configure', '', 'amber'), _box('Validate', '', 'red'),
         _box('✓ Production', '', 'green')]),

    'architecture': _cfg('Architecture Overview', 'Architecture',
        [_box('How It', 'Works', 'blue'), _box('Design', 'Standards', 'indigo'),
         _box('Integrations', '', 'amber'), _box('Reference', 'Diagrams', 'red'),
         _box('✓ Documented', '', 'green')]),

    'procedures': _cfg('Procedures Overview', 'Procedures',
        [_box('Identify', 'Task', 'blue'), _box('Prerequisites', '', 'indigo'),
         _box('Execute', 'Steps', 'amber'), _box('Verify', 'Result', 'red'),
         _box('✓ Complete', '', 'green')]),

    'health-checks': _cfg('Health Checks Overview', 'Health Checks',
        [_box('Run', 'Routine', 'blue'), _box('Review', 'Output', 'indigo'),
         _box('Assess', '✓ / ✗', 'amber'), _box('Remediate', 'if Fail', 'red'),
         _box('✓ Healthy', '', 'green')]),

    'cli-reference': _cfg('CLI Reference Overview', 'CLI Reference',
        [_box('Command', 'Groups', 'blue'), _box('Syntax &', 'Options', 'indigo'),
         _box('Examples', '', 'amber'), _box('Output', 'Format', 'red'),
         _box('✓ Reference', 'Ready', 'green')]),

    'scripts': _cfg('Scripts Overview', 'Scripts',
        [_box('Trigger /', 'Schedule', 'blue'), _box('Validate', 'Inputs', 'indigo'),
         _box('Execute', 'Logic', 'amber'), _box('Log', 'Results', 'red'),
         _box('✓ Automated', '', 'green')]),

    'backup-restore': _cfg('Backup & Restore Overview', 'Backup & Restore',
        [_box('Schedule /', 'Trigger', 'blue'), _box('Snapshot /', 'Agent', 'indigo'),
         _box('Transfer', 'to Target', 'amber'), _box('Verify', 'Integrity', 'red'),
         _box('✓ RPO/RTO', 'Met', 'green')]),

    'install-upgrade': _cfg('Install & Upgrade Overview', 'Install & Upgrade',
        [_box('Pre-Check', '& Staging', 'blue'), _box('Download /', 'Stage Image', 'indigo'),
         _box('Apply &', 'Reboot', 'amber'), _box('Validate', 'Services', 'red'),
         _box('✓ Version', 'Confirmed', 'green')]),

    'learning-path': _cfg('Learning Path', 'Learning Path',
        [_box('Foundation', 'Concepts', 'blue'), _box('Core', 'Operations', 'indigo'),
         _box('Advanced', 'Topics', 'amber'), _box('Hands-on', 'Labs', 'red'),
         _box('✓ Certified', 'Ready', 'green')]),

    'ports': _cfg('Network Port Topology', 'Ports Reference',
        [_box('Management', 'Ports', 'blue'), _box('Cluster / HA', 'Ports', 'indigo'),
         _box('Data /\nProtocol', '', 'amber'), _box('Replication', 'Ports', 'red'),
         _box('✓ All Ports', 'Secured', 'green')]),

    'how-it-works': _cfg('Architecture — How It Works', 'How It Works',
        [_box('Components', '& Layers', 'blue'), _box('Internal', 'Interactions', 'indigo'),
         _box('Data /\nControl Flow', '', 'amber'), _box('Integration', 'Points', 'red'),
         _box('✓ Architecture', 'Understood', 'green')]),

    'design-standards': _cfg('Design Standards', 'Design Standards',
        [_box('Requirements', '& Constraints', 'blue'), _box('Design', 'Principles', 'indigo'),
         _box('Standards', '& Patterns', 'amber'), _box('Review /', 'Validation', 'red'),
         _box('✓ Compliant', 'Design', 'green')]),

    'integrations': _cfg('Integration Topology', 'Integrations',
        [_box('Source', 'System', 'blue'), _box('API /', 'Protocol', 'indigo'),
         _box('Connector /', 'Adapter', 'amber'), _box('Target', 'System', 'red'),
         _box('✓ Integrated', '& Verified', 'green')]),

    'lifecycle': _cfg('Lifecycle Management', 'Lifecycle',
        [_box('Plan', '& Assess', 'blue'), _box('Upgrade /', 'Patch', 'indigo'),
         _box('Validate', '& Test', 'amber'), _box('Monitor', '', 'red'),
         _box('✓ Current', 'Version', 'green')]),

    'integration': _cfg('Integration Overview', 'Integration',
        [_box('Source', 'System', 'blue'), _box('API /', 'Protocol', 'indigo'),
         _box('Middleware', '', 'amber'), _box('Target', 'System', 'red'),
         _box('✓ Connected', '', 'green')]),

    'vendor-support': _cfg('Vendor Support Process', 'Vendor Support',
        [_box('Gather', 'Diagnostics', 'blue'), _box('Open', 'Case', 'indigo'),
         _box('Engage', 'TAM / SE', 'amber'), _box('Track', '& Update', 'red'),
         _box('✓ Resolved', '', 'green')]),

    'practice-notes': _cfg('Practice Notes', 'Practice Notes',
        [_box('Context', '& Scope', 'blue'), _box('Lessons', 'Learned', 'indigo'),
         _box('Recommendations', '', 'amber'), _box('References', '', 'red'),
         _box('✓ Documented', '', 'green')]),

    'review-plan': _cfg('Review Plan', 'Review Plan',
        [_box('Scope', '& Criteria', 'blue'), _box('Data', 'Collection', 'indigo'),
         _box('Analysis', '', 'amber'), _box('Findings /', 'Actions', 'red'),
         _box('✓ Reviewed', '', 'green')]),
}

# ── Filename-stem configs (for non-index pages without SVGs) ──────────────────

FILENAME_TYPES = {
    'common-issues': _cfg('Common Issues Overview', 'Common Issues',
        [_box('Identify', 'Symptom', 'blue'), _box('Root Cause', 'Analysis', 'indigo'),
         _box('Apply', 'Fix', 'amber'), _box('Validate', 'Resolution', 'red'),
         _box('✓ Issue', 'Resolved', 'green')]),

    'diagnostics': _cfg('Diagnostics Flow', 'Diagnostics',
        [_box('Collect', 'Symptoms', 'blue'), _box('Run', 'Commands', 'indigo'),
         _box('Analyse', 'Output', 'amber'), _box('Identify', 'Root Cause', 'red'),
         _box('✓ Diagnosis', 'Complete', 'green')]),

    'escalation': _cfg('Escalation Path', 'Escalation',
        [_box('Triage &', 'Assess', 'blue'), _box('Internal', 'L2/L3', 'indigo'),
         _box('Vendor', 'Case', 'amber'), _box('TAM /', 'Exec Bridge', 'red'),
         _box('✓ Escalated', 'Tracked', 'green')]),

    'known-issues': _cfg('Known Issues Reference', 'Known Issues',
        [_box('Symptom', 'Pattern', 'blue'), _box('Root', 'Cause', 'indigo'),
         _box('Workaround', '', 'amber'), _box('Fix / KB', 'Article', 'red'),
         _box('✓ Resolved', 'or Tracked', 'green')]),

    'guide': _cfg('Guide Overview', 'Guide',
        [_box('Scope &', 'Audience', 'blue'), _box('Prerequisites', '', 'indigo'),
         _box('Step-by-', 'Step', 'amber'), _box('Verify', '& Test', 'red'),
         _box('✓ Complete', '', 'green')]),

    'alerts': _cfg('Alerts Reference', 'Alerts',
        [_box('Alert', 'Trigger', 'blue'), _box('Severity', 'Assessment', 'indigo'),
         _box('Investigate', '', 'amber'), _box('Remediate', '', 'red'),
         _box('✓ Cleared', '', 'green')]),

    'capacity': _cfg('Capacity Planning', 'Capacity',
        [_box('Baseline', 'Metrics', 'blue'), _box('Forecast', 'Growth', 'indigo'),
         _box('Threshold', 'Analysis', 'amber'), _box('Expansion', 'Plan', 'red'),
         _box('✓ Capacity', 'Secured', 'green')]),

    'reports': _cfg('Reports Overview', 'Reports',
        [_box('Data', 'Collection', 'blue'), _box('Aggregate', '& Filter', 'indigo'),
         _box('Generate', 'Report', 'amber'), _box('Review &', 'Distribute', 'red'),
         _box('✓ Reported', '', 'green')]),

    'maintenance-window': _cfg('Maintenance Window', 'Maintenance',
        [_box('Schedule', '& Notify', 'blue'), _box('Pre-Change', 'Checks', 'indigo'),
         _box('Apply', 'Change', 'amber'), _box('Validate', '& Monitor', 'red'),
         _box('✓ Window', 'Closed', 'green')]),

    'post-change-validation': _cfg('Post-Change Validation', 'Post-Change',
        [_box('Verify', 'Services Up', 'blue'), _box('Test', 'Connectivity', 'indigo'),
         _box('Check', 'Logs', 'amber'), _box('Smoke', 'Test', 'red'),
         _box('✓ Validated', '', 'green')]),

    'post-upgrade-validation': _cfg('Post-Upgrade Validation', 'Post-Upgrade',
        [_box('Verify', 'Version', 'blue'), _box('Service', 'Health', 'indigo'),
         _box('Functional', 'Test', 'amber'), _box('Performance', 'Baseline', 'red'),
         _box('✓ Upgrade', 'Validated', 'green')]),

    'upgrade-planning': _cfg('Upgrade Planning', 'Upgrade Planning',
        [_box('Assess', 'Current', 'blue'), _box('Target', 'Version', 'indigo'),
         _box('Impact', 'Analysis', 'amber'), _box('Schedule &', 'Communicate', 'red'),
         _box('✓ Plan', 'Approved', 'green')]),

    'rollback-planning': _cfg('Rollback Planning', 'Rollback Planning',
        [_box('Define', 'Trigger', 'blue'), _box('Backup /', 'Snapshot', 'indigo'),
         _box('Rollback', 'Procedure', 'amber'), _box('Validate', 'State', 'red'),
         _box('✓ Plan', 'Tested', 'green')]),

    'disk-space-cleanup': _cfg('Disk Space Cleanup', 'Disk Cleanup',
        [_box('Identify', 'Large Files', 'blue'), _box('Assess', 'Safe to Remove', 'indigo'),
         _box('Cleanup /', 'Archive', 'amber'), _box('Verify', 'Space', 'red'),
         _box('✓ Cleaned', '', 'green')]),

    'server-reboot': _cfg('Server Reboot Procedure', 'Server Reboot',
        [_box('Notify', '& Schedule', 'blue'), _box('Drain /', 'Quiesce', 'indigo'),
         _box('Reboot', 'Node', 'amber'), _box('Verify', 'Services', 'red'),
         _box('✓ Online', '', 'green')]),

    'service-restart': _cfg('Service Restart Procedure', 'Service Restart',
        [_box('Identify', 'Service', 'blue'), _box('Graceful', 'Stop', 'indigo'),
         _box('Clear', 'State', 'amber'), _box('Start &', 'Verify', 'red'),
         _box('✓ Running', '', 'green')]),

    # VMware quick-reference pages
    'aria-automation': _cfg('Aria Automation Quick Ref', 'Aria Automation',
        [_box('Request', 'Intake', 'blue'), _box('Blueprint', 'Deploy', 'indigo'),
         _box('Approval', 'Flow', 'amber'), _box('Resource', 'Lifecycle', 'red'),
         _box('✓ Delivered', '', 'green')]),

    'aria-logs': _cfg('Aria Logs Quick Ref', 'Aria Logs',
        [_box('Log', 'Ingest', 'blue'), _box('Parse &', 'Index', 'indigo'),
         _box('Alert', 'Rules', 'amber'), _box('Dashboards', '', 'red'),
         _box('✓ Monitored', '', 'green')]),

    'aria-networks': _cfg('Aria Networks Quick Ref', 'Aria Networks',
        [_box('Discover', 'Topology', 'blue'), _box('Flow', 'Analysis', 'indigo'),
         _box('Micro-seg', 'Check', 'amber'), _box('Change', 'Mgmt', 'red'),
         _box('✓ Secured', '', 'green')]),

    'aria-operations': _cfg('Aria Operations Quick Ref', 'Aria Operations',
        [_box('Collect', 'Metrics', 'blue'), _box('Alert &', 'Analyse', 'indigo'),
         _box('Workload', 'Balance', 'amber'), _box('Capacity', 'Plan', 'red'),
         _box('✓ Optimised', '', 'green')]),

    'aria-suite-lifecycle': _cfg('Aria Suite Lifecycle Quick Ref', 'Aria LCM',
        [_box('Environment', 'Inventory', 'blue'), _box('Product', 'Deploy', 'indigo'),
         _box('Certificate', 'Mgmt', 'amber'), _box('Upgrade', 'Orchestration', 'red'),
         _box('✓ Lifecycle', 'Managed', 'green')]),

    'esxi': _cfg('ESXi Quick Reference', 'ESXi',
        [_box('Host', 'Boot', 'blue'), _box('DCUI /', 'SSH', 'indigo'),
         _box('Networking', 'Config', 'amber'), _box('VM', 'Operations', 'red'),
         _box('✓ Host', 'Ready', 'green')]),

    'horizon': _cfg('Horizon Quick Reference', 'Horizon',
        [_box('Connection', 'Server', 'blue'), _box('Desktop', 'Pool', 'indigo'),
         _box('User', 'Entitlement', 'amber'), _box('Session', 'Mgmt', 'red'),
         _box('✓ VDI', 'Delivered', 'green')]),

    'nsx': _cfg('NSX Quick Reference', 'NSX',
        [_box('Transport', 'Zones', 'blue'), _box('Segments &', 'Gateways', 'indigo'),
         _box('Distributed', 'Firewall', 'amber'), _box('Load', 'Balancer', 'red'),
         _box('✓ Network', 'Deployed', 'green')]),

    'powercli': _cfg('PowerCLI Quick Reference', 'PowerCLI',
        [_box('Connect-', 'VIServer', 'blue'), _box('Get VM /', 'Host', 'indigo'),
         _box('Execute', 'Cmdlet', 'amber'), _box('Parse', 'Output', 'red'),
         _box('✓ Automated', '', 'green')]),

    'srm': _cfg('SRM Quick Reference', 'SRM',
        [_box('Protection', 'Groups', 'blue'), _box('Recovery', 'Plans', 'indigo'),
         _box('Test', 'Failover', 'amber'), _box('Failover /', 'Failback', 'red'),
         _box('✓ DR', 'Validated', 'green')]),

    'tanzu': _cfg('Tanzu Quick Reference', 'Tanzu',
        [_box('Namespace', 'Setup', 'blue'), _box('Cluster', 'Deploy', 'indigo'),
         _box('Workload', 'Deploy', 'amber'), _box('Ingress /', 'LB', 'red'),
         _box('✓ App', 'Running', 'green')]),

    'vcenter': _cfg('vCenter Quick Reference', 'vCenter',
        [_box('Cluster', 'Config', 'blue'), _box('VM', 'Deploy', 'indigo'),
         _box('DRS / HA', 'Config', 'amber'), _box('Alarms &', 'Monitor', 'red'),
         _box('✓ Managed', '', 'green')]),

    'vcf': _cfg('VMware Cloud Foundation Quick Ref', 'VCF',
        [_box('SDDC', 'Manager', 'blue'), _box('Workload', 'Domains', 'indigo'),
         _box('NSX / vSAN', 'Config', 'amber'), _box('Lifecycle', 'Mgmt', 'red'),
         _box('✓ Platform', 'Ready', 'green')]),

    'vsan': _cfg('vSAN Quick Reference', 'vSAN',
        [_box('Disk', 'Groups', 'blue'), _box('Storage', 'Policies', 'indigo'),
         _box('Health &', 'Monitor', 'amber'), _box('Capacity', 'Mgmt', 'red'),
         _box('✓ Storage', 'Operational', 'green')]),
}

# Generic fallback
DEFAULT_CFG = _cfg('Section Overview', 'Overview',
    [_box('Context', '& Scope', 'blue'), _box('Key', 'Concepts', 'indigo'),
     _box('Procedures', '& Tasks', 'amber'), _box('Reference', 'Material', 'red'),
     _box('✓ Ready', '', 'green')])

_ASCII_RE   = re.compile(r'```text\n┌[^`]*?┘[ \t]*\n```', re.DOTALL)
_H1_RE      = re.compile(r'^# .+$', re.MULTILINE)
_SUMMARY_RE = re.compile(r'<div class="kb-summary">.*?</div>', re.DOTALL)


def xe(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _rel_assets(page: Path) -> str:
    depth = len(page.parts) - len(DOCS.parts) - 1
    return '../' * depth + 'assets/'


def _product_label(page: Path) -> str:
    parts = page.parts
    docs_idx = next(i for i, p in enumerate(parts) if p == 'docs')
    # Exclude generic section dir names from the label
    skip = {'operations', 'security', 'troubleshooting', 'architecture',
            'procedures', 'health-checks', 'cli-reference', 'scripts',
            'backup-restore', 'install-upgrade', 'learning-path', 'ports',
            'how-it-works', 'design-standards', 'integrations', 'deploy',
            'lifecycle', 'integration', 'vendor-support', 'practice-notes',
            'review-plan'}
    segs = [s for s in parts[docs_idx + 1: -1] if s not in skip]
    return ' / '.join(s.replace('-', ' ').title() for s in segs[:3])


def _get_cfg(page: Path):
    parent = page.parent.name
    stem   = page.stem

    if stem == 'index':
        return SECTION_TYPES.get(parent, DEFAULT_CFG)
    else:
        return FILENAME_TYPES.get(stem, DEFAULT_CFG)


def make_svg(cfg: dict, product_label: str, page_title: str) -> str:
    boxes = cfg['boxes']
    n = len(boxes)
    total_arrow = (n - 1) * ARW_W
    box_w = (SVG_W - 2 * PAD - total_arrow) // n

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" '
        f"font-family=\"'Segoe UI',Arial,sans-serif\">",
        f'  <rect width="{SVG_W}" height="{SVG_H}" fill="#f4f6f9"/>',
        f'  <rect x="0" y="0" width="{SVG_W}" height="{HDR_H}" fill="{NAVY}"/>',
        f'  <text x="410" y="25" text-anchor="middle" fill="white" '
        f'font-size="13" font-weight="700">{xe(page_title[:80])}</text>',
        f'  <text x="410" y="37" text-anchor="middle" fill="{FOOTER_FG}" '
        f'font-size="9">{xe(product_label)} — {xe(cfg["subtitle"])}</text>',
    ]

    x = PAD
    for i, (l1, l2, fill, stroke) in enumerate(boxes):
        l1_clean = l1.replace('\n', ' ').strip()
        cx = x + box_w // 2
        lines.append(
            f'  <rect x="{x}" y="{BOX_Y}" width="{box_w}" height="{BOX_H}" '
            f'fill="{fill}" rx="4" stroke="{stroke}" stroke-width="1.5"/>'
        )
        ty = BOX_Y + (BOX_H // 2 - (5 if l2 else 0))
        lines.append(
            f'  <text x="{cx}" y="{ty}" text-anchor="middle" '
            f'fill="{TEXT_DARK}" font-size="10" font-weight="700">{xe(l1_clean)}</text>'
        )
        if l2:
            lines.append(
                f'  <text x="{cx}" y="{ty + 14}" text-anchor="middle" '
                f'fill="{TEXT_MID}" font-size="9">{xe(l2)}</text>'
            )
        if i < n - 1:
            ax = x + box_w
            ay = BOX_Y + BOX_H // 2
            lines += [
                f'  <line x1="{ax}" y1="{ay}" x2="{ax + ARW_W - 3}" y2="{ay}" '
                f'stroke="{TEXT_LIGHT}" stroke-width="1.5"/>',
                f'  <polygon points="{ax + ARW_W - 3},{ay - 4} '
                f'{ax + ARW_W + 1},{ay} {ax + ARW_W - 3},{ay + 4}" fill="{TEXT_LIGHT}"/>',
            ]
        x += box_w + ARW_W

    lines += [
        f'  <rect x="0" y="{FTR_Y}" width="{SVG_W}" height="{FTR_H}" fill="{NAVY}"/>',
        f'  <text x="410" y="{FTR_Y + 16}" text-anchor="middle" '
        f'fill="{FOOTER_FG}" font-size="9">'
        f'{xe(product_label)} · {xe(cfg["footer"])}</text>',
        '</svg>',
    ]

    svg = '\n'.join(lines)
    ET.fromstring(svg)
    return svg


def _slug_from_path(page: Path) -> str:
    parts = page.parts
    docs_idx = next(i for i, p in enumerate(parts) if p == 'docs')
    slug = '-'.join(parts[docs_idx + 1:]).replace('/', '-').replace('.md', '')
    return re.sub(r'[^a-z0-9-]', '-', slug.lower()).strip('-')[:60]


def _page_title(text: str, page: Path) -> str:
    m = _H1_RE.search(text)
    if m:
        return m.group(0).lstrip('# ').strip()
    return page.parent.name.replace('-', ' ').title() if page.stem == 'index' \
        else page.stem.replace('-', ' ').title()


def process_page(page: Path, dry_run: bool = False) -> int:
    if 'admin' in page.parts:
        return 0
    text = page.read_text(encoding='utf-8')
    if '![' in text:
        return 0  # already has SVG

    cfg = _get_cfg(page)
    product_label = _product_label(page)
    title = _page_title(text, page)
    rel_assets = _rel_assets(page)
    svg_fname = _slug_from_path(page) + '.svg'
    svg_path  = ASSETS / svg_fname

    if not dry_run:
        svg = make_svg(cfg, product_label, title)
        svg_path.write_text(svg, encoding='utf-8')

        new_text = _ASCII_RE.sub('', text)
        img_ref = f'\n![{title}]({rel_assets}{svg_fname})\n'
        if svg_fname in new_text:
            return 1  # already injected

        if _SUMMARY_RE.search(new_text):
            new_text = _SUMMARY_RE.sub(lambda m: m.group(0) + img_ref, new_text, count=1)
        elif _H1_RE.search(new_text):
            new_text = _H1_RE.sub(lambda m: m.group(0) + img_ref, new_text, count=1)
        else:
            new_text = img_ref + new_text

        page.write_text(new_text, encoding='utf-8')

    return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--path', help='Limit to pages under this docs/ subpath')
    args = parser.parse_args()

    pages = sorted(DOCS.rglob('*.md'))
    if args.path:
        pages = [p for p in pages if args.path in str(p)]

    total = 0
    for page in pages:
        total += process_page(page, dry_run=args.dry_run)

    print(f'Total SVGs {"(dry run)" if args.dry_run else "generated"}: {total}')


if __name__ == '__main__':
    main()
