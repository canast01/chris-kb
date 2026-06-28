#!/usr/bin/env python3
"""
mass_diagram_gen.py — Generate and inject D2 / PlantUML diagrams into every
KB page that doesn't already have a Kroki fence.

Engine:
  1. Read each .md file
  2. Extract: product name (path → product map), page type (parent folder),
     up to 6 H2 headings
  3. Select diagram template based on page type
  4. Inject the block before the first ## heading
  5. Skip pages that already have a Kroki fence (idempotent)

CLI:
  --page-type   Only process pages whose parent folder matches (e.g. troubleshooting)
  --product     Only process pages whose path contains this string
  --dry-run     Show what would change, don't write
  --limit N     Process at most N files (for testing)
"""

import re
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent / "docs"

# ─── Product display-name map ─────────────────────────────────────────────────
# Longest-key-wins: sorted by length desc so more-specific paths match first.
PRODUCT_MAP = {
    # VMware — specific products first
    "vmware/vmware-cloud-foundation":      "VMware Cloud Foundation",
    "vmware/aria-operations-for-logs":     "Aria Operations for Logs",
    "vmware/aria-operations-for-networks": "Aria Operations for Networks",
    "vmware/aria-suite-lifecycle":         "Aria Suite Lifecycle",
    "vmware/aria-automation":              "Aria Automation",
    "vmware/aria-operations":              "Aria Operations",
    "vmware/vsphere-replication":          "vSphere Replication",
    "vmware/vcenter":                      "vCenter Server",
    "vmware/horizon":                      "Horizon",
    "vmware/vxrail":                       "VxRail",
    "vmware/powercli":                     "PowerCLI",
    "vmware/tanzu":                        "Tanzu",
    "vmware/vsan":                         "vSAN",
    "vmware/esxi":                         "ESXi",
    "vmware/nsx":                          "NSX-T",
    "vmware/srm":                          "Site Recovery Manager",
    # NetApp
    "netapp/superna-eyeglass":             "Superna Eyeglass",
    "netapp/snapcenter":                   "SnapCenter",
    "netapp/snapmirror":                   "SnapMirror",
    "netapp/insightiq":                    "InsightIQ",
    "netapp/keystone":                     "Keystone STaaS",
    "netapp/ontap":                        "NetApp ONTAP",
    # Pure Storage
    "pure/evergreen-one":                  "Evergreen//One",
    "pure/flasharray":                     "FlashArray",
    "pure/flashblade":                     "FlashBlade",
    "pure/evergreen":                      "Evergreen",
    "pure/pure1":                          "Pure1",
    # Dell
    "dell/apex-storage-as-a-service":      "APEX Storage",
    "dell/secure-connect-gateway":         "Secure Connect Gateway",
    "dell/powerscale":                     "PowerScale (Isilon)",
    "dell/data-domain":                    "Data Domain",
    "dell/recoverpoint":                   "RecoverPoint",
    "dell/powerstore":                     "PowerStore",
    "dell/powerpath":                      "PowerPath",
    "dell/powermax":                       "PowerMax",
    "dell/dell-aiops":                     "Dell AIOps",
    "dell/cloudiq":                        "CloudIQ",
    "dell/srdf-a":                         "SRDF/A",
    "dell/srdf-s":                         "SRDF/S",
    "dell/unity":                          "Unity XT",
    "dell/vplex":                          "VPLEX",
    "dell/ecs":                            "ECS",
    "dell/cod":                            "Cloud On Demand",
    "dell/fod":                            "Flex On Demand",
    # SAN
    "brocade/fabric-os":                   "Brocade Fabric OS",
    "brocade/sannav":                      "SANnav",
    "cisco/nexus-dashboard":               "Nexus Dashboard",
    "cisco/cisco-dcnm":                    "Cisco DCNM",
    "cisco/mds":                           "Cisco MDS",
    # Backup
    "backup/dr-operations":                "DR Operations",
    "backup/commvault":                    "Commvault",
    "backup/netbackup":                    "NetBackup",
    "backup/veeam":                        "Veeam",
    # Compute / OS
    "windows-server/active-directory":     "Active Directory",
    "windows-server/sql-server":           "SQL Server",
    "linux/postgresql":                    "PostgreSQL",
    "linux/mysql":                         "MySQL",
    "local-ai/ollama":                     "Ollama",
    "local-ai/gpu":                        "GPU Compute",
    "compute/windows-server":              "Windows Server",
    "compute/linux":                       "Linux",
    # Cloud
    "ai/aws-bedrock":                      "AWS Bedrock",
    "ai/azure-openai":                     "Azure OpenAI",
    "ai/openai":                           "OpenAI API",
    "cloud/aws/evs":                       "AWS EVS",
    "cloud/azure":                         "Azure",
    "cloud/aws":                           "AWS",
    # Automation
    "automation/github-actions":           "GitHub Actions",
    "automation/powershell":               "PowerShell",
    "automation/ansible":                  "Ansible",
    "automation/python":                   "Python",
    # Networking
    "protocols/api-connectivity":          "API Connectivity",
    "protocols/email-relay":               "Email Relay",
    "protocols/service-integrations":      "Service Integrations",
    "protocols/fibre-channel":             "Fibre Channel",
    "protocols/iscsi":                     "iSCSI",
    "protocols/ldap":                      "LDAP",
    "protocols/snmp":                      "SNMP",
    "protocols/syslog":                    "Syslog",
    "protocols/dhcp":                      "DHCP",
    "protocols/dns":                       "DNS",
    "protocols/nfs":                       "NFS",
    "protocols/ntp":                       "NTP",
    "protocols/smb":                       "SMB",
    "protocols/tls":                       "TLS",
    "networking/switching-routing":        "Switching & Routing",
    "networking/external-connectivity":    "External Connectivity",
    "networking/network-design":           "Network Design",
    # Virtualisation
    "virtualization/openshift":            "OpenShift",
    "virtualization/nutanix":             "Nutanix AHV",
    # Storage
    "storage/ceph":                        "Ceph",
    # ITSM
    "itsm/servicenow":                     "ServiceNow",
    "itsm/jira":                           "Jira",
}

_SORTED_KEYS = sorted(PRODUCT_MAP, key=len, reverse=True)


def product_name(rel_path: str) -> str:
    rel = rel_path.replace("\\", "/")
    for key in _SORTED_KEYS:
        if key in rel:
            return PRODUCT_MAP[key]
    parts = [p for p in rel.split("/") if p and not p.endswith(".md")]
    return parts[-1].replace("-", " ").title() if parts else "System"


# ─── Helpers ─────────────────────────────────────────────────────────────────

def slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9 ]", "", text).strip().lower()
    s = re.sub(r"\s+", "_", s)
    return (s[:36] or "node")


def dedup_slugs(sections: list) -> list:
    """Return (heading, unique_slug) pairs."""
    seen = {}
    result = []
    for s in sections:
        base = slug(s)
        n = seen.get(base, 0)
        seen[base] = n + 1
        result.append((s, base if n == 0 else f"{base}_{n}"))
    return result


def d2lbl(text: str) -> str:
    return text.replace('"', "'")[:60]


def pu_lbl(text: str) -> str:
    return re.sub(r'[^a-zA-Z0-9 /\-.,()]', '', text)[:50].strip()


def extract_h2(lines: list, max_n: int = 6) -> list:
    SKIP = {"see also", "before you begin", "overview", "references",
            "further reading", "related", "notes", "tips", "next steps"}
    headings = []
    for line in lines:
        m = re.match(r"^## (.+)", line)
        if m:
            text = m.group(1).strip()
            if text.lower() not in SKIP:
                headings.append(text)
            if len(headings) >= max_n:
                break
    return headings


def page_type_of(path: Path) -> str:
    return path.parent.name.lower()


def already_has_diagram(lines: list) -> bool:
    """True if the page already has any diagram — SVG, Mermaid, Kroki, or ASCII box."""
    text = "".join(lines)
    kroki = {"```d2", "```plantuml", "```vega-lite", "```mermaid", "```vegalite"}
    if any(line.rstrip() in kroki for line in lines):
        return True
    if re.search(r'\.(svg|png|jpg)\)', text) or '<img ' in text:
        return True
    if re.search(r'[┌│└┐┘]', text):
        return True
    return False


def find_inject_pos(lines: list):
    """Return index of first ## heading, or first ### heading, or end of file."""
    for i, line in enumerate(lines):
        if line.startswith("## ") or line.startswith("### "):
            return i
    # Fall back to end of file (append)
    return len(lines)


def inject_block(lines: list, pos: int, content: str) -> list:
    block = []
    if pos > 0 and lines[pos - 1].strip():
        block.append("\n")
    block.append(content if content.endswith("\n") else content + "\n")
    if pos < len(lines) and lines[pos].strip():
        block.append("\n")
    return lines[:pos] + block + lines[pos:]


# ─── D2 templates ─────────────────────────────────────────────────────────────

def d2_troubleshooting(product: str, sections: list) -> str:
    nodes = sections or ["Service Unavailable", "Performance Degraded", "Data Inconsistency"]
    pairs = dedup_slugs(nodes)
    out = ["```d2", "direction: down", ""]
    out.append('symptom: Identify Symptom {shape: diamond}')
    for txt, sid in pairs:
        out.append(f'{sid}: "{d2lbl(txt)}" {{shape: rectangle}}')
    out.append('resolution: Resolve or Escalate {shape: oval}')
    out.append("")
    for _, sid in pairs:
        out.append(f"symptom -> {sid}: investigate")
    for _, sid in pairs:
        out.append(f"{sid} -> resolution")
    out.append("```\n")
    return "\n".join(out)


def d2_operations(product: str, sections: list) -> str:
    nodes = sections or ["Routine Checks", "Configuration", "Monitoring", "Maintenance"]
    pairs = dedup_slugs(nodes)
    out = ["```d2", "direction: right", ""]
    for txt, sid in pairs:
        out.append(f'{sid}: "{d2lbl(txt)}" {{shape: rectangle}}')
    out.append("")
    for i in range(len(pairs) - 1):
        out.append(f"{pairs[i][1]} -> {pairs[i+1][1]}")
    out.append("```\n")
    return "\n".join(out)


def d2_security_boundary(product: str, sections: list) -> str:
    nodes = sections or ["Perimeter Controls", "Identity & Access", "Audit & Logging"]
    pairs = dedup_slugs(nodes)
    out = ["```d2", "direction: down", ""]
    out.append('external: External / Untrusted {shape: rectangle}')
    for txt, sid in pairs:
        out.append(f'{sid}: "{d2lbl(txt)}" {{shape: rectangle}}')
    out.append(f'core: "{d2lbl(product)} Core" {{shape: hexagon}}')
    out.append("")
    out.append(f"external -> {pairs[0][1]}: traffic in")
    for i in range(len(pairs) - 1):
        out.append(f"{pairs[i][1]} -> {pairs[i+1][1]}")
    out.append(f"{pairs[-1][1]} -> core: secured path")
    out.append("```\n")
    return "\n".join(out)


def d2_pipeline(product: str, sections: list, start: str = "Plan", end: str = "Validate") -> str:
    stages = sections or ["Prepare", "Execute", "Verify"]
    pairs = dedup_slugs(stages)
    start_slug = slug(start)
    end_slug = slug(end)
    out = ["```d2", "direction: right", ""]
    out.append(f'{start_slug}: "{start}" {{shape: oval}}')
    for txt, sid in pairs:
        out.append(f'{sid}: "{d2lbl(txt)}" {{shape: rectangle}}')
    out.append(f'{end_slug}: "{end}" {{shape: oval}}')
    out.append("")
    prev = start_slug
    for _, sid in pairs:
        out.append(f"{prev} -> {sid}")
        prev = sid
    out.append(f"{prev} -> {end_slug}")
    out.append("```\n")
    return "\n".join(out)


def d2_components(product: str, sections: list) -> str:
    """Dependency chain — replaces the old hub-and-spoke pattern."""
    nodes = sections or ["Component A", "Component B", "Component C"]
    pairs = dedup_slugs(nodes)
    out = ["```d2", "direction: down", ""]
    for txt, sid in pairs:
        out.append(f'{sid}: "{d2lbl(txt)}" {{shape: rectangle}}')
    out.append("")
    for i in range(len(pairs) - 1):
        out.append(f"{pairs[i][1]} -> {pairs[i+1][1]}: uses")
    out.append("```\n")
    return "\n".join(out)


def d2_learning_path(product: str, sections: list) -> str:
    stages = sections or ["Fundamentals", "Core Concepts", "Advanced Topics", "Certification"]
    pairs = dedup_slugs(stages)
    out = ["```d2", "direction: right", ""]
    for txt, sid in pairs:
        out.append(f'{sid}: "{d2lbl(txt)}" {{shape: rectangle}}')
    out.append("")
    for i in range(len(pairs) - 1):
        out.append(f"{pairs[i][1]} -> {pairs[i+1][1]}: next")
    out.append("```\n")
    return "\n".join(out)


def d2_rbac(product: str, sections: list) -> str:
    roles = sections or ["Administrator", "Operator", "Auditor", "Read-Only"]
    pairs = dedup_slugs(roles)
    out = ["```d2", "direction: down", ""]
    out.append(f'auth: "{d2lbl(product)}\\nAuthentication" {{shape: rectangle}}')
    for txt, sid in pairs:
        out.append(f'{sid}: "{d2lbl(txt)}" {{shape: rectangle}}')
    out.append('resources: Protected Resources {shape: cylinder}')
    out.append("")
    for _, sid in pairs:
        out.append(f"auth -> {sid}: grants")
        out.append(f"{sid} -> resources: access")
    out.append("```\n")
    return "\n".join(out)


def d2_security_layers(product: str, sections: list) -> str:
    layers = sections or ["Network Controls", "OS Hardening", "Application Security", "Audit & Monitoring"]
    pairs = dedup_slugs(layers)
    out = ["```d2", "direction: down", ""]
    for txt, sid in pairs:
        out.append(f'{sid}: "{d2lbl(txt)}" {{shape: rectangle}}')
    out.append("")
    for i in range(len(pairs) - 1):
        out.append(f"{pairs[i][1]} -> {pairs[i+1][1]}: hardens")
    out.append("```\n")
    return "\n".join(out)


def d2_diagnostic_tree(product: str, sections: list) -> str:
    nodes = sections or ["Check Logs", "Verify Connectivity", "Inspect Configuration"]
    pairs = dedup_slugs(nodes)
    out = ["```d2", "direction: down", ""]
    out.append('start: Begin Diagnostic {shape: diamond}')
    for txt, sid in pairs:
        out.append(f'{sid}: "{d2lbl(txt)}" {{shape: rectangle}}')
    out.append('outcome: Resolution Path {shape: oval}')
    out.append("")
    for _, sid in pairs:
        out.append(f"start -> {sid}: check")
        out.append(f"{sid} -> outcome")
    out.append("```\n")
    return "\n".join(out)


# ─── PlantUML templates ───────────────────────────────────────────────────────

def pu_auth_flow(product: str, sections: list) -> str:
    out = [
        "```plantuml",
        "@startuml",
        "skinparam sequenceArrowThickness 1.5",
        "skinparam roundcorner 5",
        "",
        'actor "User / Service" as USR',
        f'participant "{pu_lbl(product)}" as SVC',
        'participant "Identity Provider\\n(LDAP / OIDC / AD)" as IDP',
        'participant "Token / Session Store" as TOKEN',
        "",
        "USR -> SVC: Authentication request",
        "SVC -> IDP: Validate credentials",
        "IDP --> SVC: Identity confirmed",
        "SVC -> TOKEN: Issue session token",
        "TOKEN --> SVC: Token granted",
        "SVC --> USR: Access allowed",
    ]
    if sections:
        out += ["", "note over SVC"]
        for s in sections[:3]:
            out.append(f"  {pu_lbl(s)}")
        out.append("end note")
    out += ["", "@enduml", "```\n"]
    return "\n".join(out)


def pu_sequence(product: str, sections: list, actor_a: str = "Admin", actor_b: str = "") -> str:
    b = actor_b or f"{pu_lbl(product)} System"
    steps = sections or ["Initiate", "Process", "Confirm", "Complete"]
    out = [
        "```plantuml",
        "@startuml",
        "skinparam sequenceArrowThickness 1.5",
        "skinparam roundcorner 5",
        "",
        f'actor "{actor_a}" as A',
        f'participant "{b}" as B',
        'participant "Dependent System" as C',
        "",
    ]
    for s in steps:
        out.append(f'A -> B: {pu_lbl(s)}')
        out.append(f'B --> A: OK')
    out += ["", "@enduml", "```\n"]
    return "\n".join(out)


def pu_backup_restore(product: str, sections: list) -> str:
    steps = sections or ["Initiate Backup", "Transfer Data", "Write to Vault", "Verify Backup"]
    out = [
        "```plantuml",
        "@startuml",
        "skinparam sequenceArrowThickness 1.5",
        "skinparam roundcorner 5",
        "",
        f'participant "Source\\n({pu_lbl(product)})" as SRC',
        'participant "Backup Engine" as ENG',
        'participant "Target / Vault" as TGT',
        "",
    ]
    for s in steps:
        out.append(f'SRC -> ENG: {pu_lbl(s)}')
        out.append(f'ENG -> TGT: Write')
        out.append(f'TGT --> ENG: Confirmed')
        out.append(f'ENG --> SRC: Done')
    out += ["", "@enduml", "```\n"]
    return "\n".join(out)


def pu_escalation(product: str, sections: list) -> str:
    steps = sections or ["Identify Severity", "Collect Diagnostics", "Open Support Case", "Track Resolution"]
    out = [
        "```plantuml",
        "@startuml",
        "skinparam sequenceArrowThickness 1.5",
        "skinparam roundcorner 5",
        "",
        'actor "On-Call Engineer" as ENG',
        f'participant "{pu_lbl(product)}\\nSystem" as SYS',
        'participant "Vendor Support" as SUP',
        "",
    ]
    for s in steps[:3]:
        out.append(f'ENG -> SYS: {pu_lbl(s)}')
        out.append(f'SYS --> ENG: Output')
    out.append('ENG -> SUP: Escalate with diagnostic bundle')
    out.append('SUP --> ENG: Case / resolution path')
    out += ["", "@enduml", "```\n"]
    return "\n".join(out)


# ─── Template dispatch ────────────────────────────────────────────────────────

def build_diagram(ptype: str, product: str, sections: list) -> str:
    if ptype in ("troubleshooting", "common-issues", "diagnostics"):
        return d2_troubleshooting(product, sections)
    if ptype in ("operations", "procedures", "monitoring"):
        return d2_operations(product, sections)
    if ptype in ("hardening", "encryption", "standards", "design-standards"):
        return d2_security_layers(product, sections)
    if ptype == "authentication":
        return pu_auth_flow(product, sections)
    if ptype == "access-control":
        return d2_rbac(product, sections)
    if ptype == "security":
        return d2_security_boundary(product, sections)
    if ptype in ("deploy", "install-upgrade", "upgrade-readiness", "lifecycle", "install"):
        return d2_pipeline(product, sections, start="Plan", end="Validate")
    if ptype in ("health-checks", "review-plan"):
        return d2_pipeline(product, sections, start="Begin Checks", end="Generate Report")
    if ptype == "backup-restore":
        return pu_backup_restore(product, sections)
    if ptype in ("escalation", "vendor-support"):
        return pu_escalation(product, sections)
    if ptype in ("runbooks", "incident-response"):
        return pu_sequence(product, sections, actor_a="Responder")
    if ptype == "learning-path":
        return d2_learning_path(product, sections)
    if ptype in ("integrations", "scenarios", "integration"):
        return d2_components(product, sections)
    if ptype in ("cli-reference", "cheat-sheets", "quick-reference", "inventory", "scripts"):
        return d2_components(product, sections)
    if ptype in ("how-it-works", "architecture"):
        return d2_components(product, sections)
    # default
    return d2_components(product, sections)


# ─── Per-file processor ───────────────────────────────────────────────────────

def process_file(path: Path, dry_run: bool) -> str:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    if already_has_diagram(lines):
        return "SKIP"

    # Skip nav/card pages — they don't need diagrams
    if "kb-card" in text or "kb-grid" in text:
        return "SKIP"

    pos = find_inject_pos(lines)

    rel = str(path.relative_to(ROOT))
    prod = product_name(rel)
    ptype = page_type_of(path)
    sections = extract_h2(lines)

    diagram = build_diagram(ptype, prod, sections)

    if not dry_run:
        new_lines = inject_block(lines, pos, diagram)
        path.write_text("".join(new_lines), encoding="utf-8")

    return "DRY" if dry_run else "OK"


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--page-type", help="Only process pages whose parent folder matches")
    ap.add_argument("--product",   help="Only process pages whose path contains this string")
    ap.add_argument("--dry-run",   action="store_true")
    ap.add_argument("--limit",     type=int, default=0, help="Max files to process")
    args = ap.parse_args()

    paths = sorted(ROOT.rglob("*.md"))

    if args.page_type:
        paths = [p for p in paths if p.parent.name.lower() == args.page_type.lower()]
    if args.product:
        paths = [p for p in paths if args.product.lower() in str(p).lower()]

    counts = {"OK": 0, "DRY": 0, "SKIP": 0, "NO_H2": 0, "ERR": 0}
    processed = 0

    for path in paths:
        if args.limit and processed >= args.limit:
            break
        try:
            result = process_file(path, args.dry_run)
        except Exception as exc:
            print(f"[ERR    ] {path.relative_to(ROOT)}  — {exc}")
            counts["ERR"] += 1
            processed += 1
            continue

        counts[result] += 1
        processed += 1

        if result not in ("SKIP", "NO_H2"):
            verb = "DRY RUN" if result == "DRY" else "UPDATED"
            print(f"[{verb:7}] {path.relative_to(ROOT)}")

    print()
    print("=" * 68)
    n = counts["DRY"] if args.dry_run else counts["OK"]
    action = "Would update" if args.dry_run else "Updated"
    print(f"{action}: {n}  |  Has Kroki: {counts['SKIP']}  |  "
          f"No H2: {counts['NO_H2']}  |  Errors: {counts['ERR']}")
    print("=" * 68)


if __name__ == "__main__":
    main()
