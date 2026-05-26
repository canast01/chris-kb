"""
MkDocs hook: fix nav titles and restructure top-level tabs.

Top-level nav becomes: Home | Platforms | Site Map
All other sections are nested under Platforms.

Title fixes are applied word-by-word so product names and acronyms
render correctly regardless of how MkDocs derives them from folder names.
"""

from mkdocs.structure.nav import Section

# Word-level substitutions (matched case-insensitively against each word)
WORD_FIXES = {
    # Acronyms
    "ai":        "AI",
    "api":       "API",
    "aws":       "AWS",
    "cli":       "CLI",
    "cpu":       "CPU",
    "csv":       "CSV",
    "dcnm":      "DCNM",
    "dns":       "DNS",
    "dr":        "DR",
    "gui":       "GUI",
    "ha":        "HA",
    "hci":       "HCI",
    "http":      "HTTP",
    "https":     "HTTPS",
    "iam":       "IAM",
    "ip":        "IP",
    "iscsi":     "iSCSI",
    "json":      "JSON",
    "lcm":       "LCM",
    "ldap":      "LDAP",
    "mds":       "MDS",
    "mfa":       "MFA",
    "nfs":       "NFS",
    "nsx":       "NSX",
    "ntp":       "NTP",
    "os":        "OS",
    "rbac":      "RBAC",
    "rca":       "RCA",
    "rpo":       "RPO",
    "rto":       "RTO",
    "san":       "SAN",
    "sdk":       "SDK",
    "smtp":      "SMTP",
    "snmp":      "SNMP",
    "snmpv3":    "SNMPv3",
    "sql":       "SQL",
    "srm":       "SRM",
    "ssh":       "SSH",
    "ssl":       "SSL",
    "sso":       "SSO",
    "syslog":    "Syslog",
    "tls":       "TLS",
    "ui":        "UI",
    "url":       "URL",
    "vcf":       "VCF",
    "vdi":       "VDI",
    "vlan":      "VLAN",
    "vm":        "VM",
    "yaml":      "YAML",
    # Product / brand names
    "aria":      "Aria",
    "aws":       "AWS",
    "azure":     "Azure",
    "brocade":   "Brocade",
    "cisco":     "Cisco",
    "cloudiq":   "CloudIQ",
    "confluence": "Confluence",
    "dell":      "Dell",
    "esxi":      "ESXi",
    "github":    "GitHub",
    "git":       "Git",
    "horizon":   "Horizon",
    "insightiq": "InsightIQ",
    "jira":      "Jira",
    "linux":     "Linux",
    "netapp":    "NetApp",
    "nexus":     "Nexus",
    "pure":      "Pure",
    "pure1":     "Pure1",
    "sannav":    "SANnav",
    "servicenow": "ServiceNow",
    "tanzu":     "Tanzu",
    "vcenter":   "vCenter",
    "vmware":    "VMware",
    "vsan":      "vSAN",
    "vsphere":   "vSphere",
    "vxrail":    "VxRail",
    "windows":   "Windows",
}

# Prepositions / conjunctions that stay lowercase unless they open the title
_LOWERCASE_WORDS = {"a", "an", "and", "at", "by", "for", "in", "of", "on", "or",
                    "the", "to", "vs", "with"}


def _fix_title(title: str) -> str:
    if not title:
        return title
    words = title.split()
    out = []
    for i, word in enumerate(words):
        lower = word.lower()
        if lower in WORD_FIXES:
            out.append(WORD_FIXES[lower])
        elif i > 0 and lower in _LOWERCASE_WORDS:
            out.append(lower)
        else:
            # Preserve existing capitalisation; only force first letter up when
            # the word is all-lowercase (i.e. came straight from a folder name).
            if word == word.lower():
                out.append(word.capitalize())
            else:
                out.append(word)
    return " ".join(out)


def _fix(item) -> None:
    if hasattr(item, "title") and item.title:
        item.title = _fix_title(item.title)
    for child in getattr(item, "children", None) or []:
        _fix(child)


def on_nav(nav, **kwargs):
    # ── Step 1: fix titles everywhere ────────────────────────────────────────
    for item in nav.items:
        _fix(item)

    # ── Step 2: set explicit titles for Home and Site Map ────────────────────
    for item in nav.items:
        if hasattr(item, "file") and item.file:
            src = item.file.src_path
            if src == "index.md":
                item.title = "Home"
            elif src == "site-map.md":
                item.title = "Site Map"

    # ── Step 3: restructure → Home | Platforms | Site Map ───────────────────
    home    = next((i for i in nav.items
                    if hasattr(i, "file") and i.file
                    and i.file.src_path == "index.md"), None)
    sitemap = next((i for i in nav.items
                    if hasattr(i, "file") and i.file
                    and i.file.src_path == "site-map.md"), None)

    middle = [i for i in nav.items if i is not home and i is not sitemap]

    if middle:
        platforms = Section(title="Platforms", children=middle)
        for child in middle:
            child.parent = platforms

        new_items = []
        if home:
            new_items.append(home)
        new_items.append(platforms)
        if sitemap:
            new_items.append(sitemap)
        nav.items = new_items

    return nav
