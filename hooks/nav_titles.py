"""
MkDocs hook: fix nav titles and restructure top-level tabs.

Top-level nav becomes: Home | Platforms | Site Map
All other sections are nested under Platforms.

Title fixes are applied word-by-word so product names and acronyms
render correctly regardless of how MkDocs derives them from folder names.
"""

from mkdocs.structure.nav import Section

# Word-level substitutions — matched case-insensitively against each individual word.
# MkDocs derives section titles from folder names via:
#   folder_name.replace('-', ' ').replace('_', ' ').capitalize()
# That produces e.g. "Vmware cloud foundation", "Dhcp", "Smb".
# This map fixes every word that needs special casing.
WORD_FIXES = {
    # ── Infrastructure acronyms ──────────────────────────────────────────────
    "acl":          "ACL",
    "acls":         "ACLs",
    "ai":           "AI",
    "aiops":        "AIOps",
    "ami":          "AMI",
    "amis":         "AMIs",
    "api":          "API",
    "bgp":          "BGP",
    "bios":         "BIOS",
    "cli":          "CLI",
    "cmdb":         "CMDB",
    "cod":          "COD",
    "cpu":          "CPU",
    "csv":          "CSV",
    "dcnm":         "DCNM",
    "dhcp":         "DHCP",
    "dns":          "DNS",
    "dr":           "DR",
    "drs":          "DRS",
    "ebs":          "EBS",
    "ec2":          "EC2",
    "ecs":          "ECS",
    "efs":          "EFS",
    "eks":          "EKS",
    "fod":          "FOD",
    "fsx":          "FSx",
    "gpu":          "GPU",
    "gui":          "GUI",
    "ha":           "HA",
    "hci":          "HCI",
    "http":         "HTTP",
    "https":        "HTTPS",
    "iam":          "IAM",
    "id":           "ID",
    "idrac":        "iDRAC",
    "ip":           "IP",
    "ire":          "IRE",
    "iscsi":        "iSCSI",
    "json":         "JSON",
    "kms":          "KMS",
    "lcm":          "LCM",
    "ldap":         "LDAP",
    "mds":          "MDS",
    "mfa":          "MFA",
    "nat":          "NAT",
    "nfs":          "NFS",
    "nic":          "NIC",
    "nsx":          "NSX",
    "ntfs":         "NTFS",
    "ntp":          "NTP",
    "os":           "OS",
    "pki":          "PKI",
    "rbac":         "RBAC",
    "rca":          "RCA",
    "rds":          "RDS",
    "rpo":          "RPO",
    "rto":          "RTO",
    "s3":           "S3",
    "saml":         "SAML",
    "san":          "SAN",
    "sdk":          "SDK",
    "smb":          "SMB",
    "smtp":         "SMTP",
    "snmp":         "SNMP",
    "snmpv3":       "SNMPv3",
    "sql":          "SQL",
    "srdf":         "SRDF",
    "srm":          "SRM",
    "ssh":          "SSH",
    "ssl":          "SSL",
    "ssm":          "SSM",
    "sso":          "SSO",
    "tls":          "TLS",
    "ui":           "UI",
    "url":          "URL",
    "vcf":          "VCF",
    "vdi":          "VDI",
    "vlan":         "VLAN",
    "vm":           "VM",
    "vpc":          "VPC",
    "vpn":          "VPN",
    "waf":          "WAF",
    "wwn":          "WWN",
    "wwns":         "WWNs",
    "yaml":         "YAML",
    # ── AWS services ─────────────────────────────────────────────────────────
    "aws":          "AWS",
    "cloudformation": "CloudFormation",
    "cloudtrail":   "CloudTrail",
    "cloudwatch":   "CloudWatch",
    "guardduty":    "GuardDuty",
    "rasr":         "RASR",
    # ── Azure services ───────────────────────────────────────────────────────
    "azure":        "Azure",
    "aks":          "AKS",
    "entra":        "Entra",
    "expressroute": "ExpressRoute",
    # ── VMware products ──────────────────────────────────────────────────────
    "esxi":         "ESXi",
    "vcenter":      "vCenter",
    "vmware":       "VMware",
    "vsan":         "vSAN",
    "vsphere":      "vSphere",
    "vxrail":       "VxRail",
    # ── Dell / EMC products ──────────────────────────────────────────────────
    "dell":         "Dell",
    "idrac":        "iDRAC",
    "powermax":     "PowerMax",
    "powerpath":    "PowerPath",
    "powerscale":   "PowerScale",
    "powerstore":   "PowerStore",
    "recoverpoint": "RecoverPoint",
    "vplex":        "VPlex",
    # ── NetApp products ──────────────────────────────────────────────────────
    "netapp":       "NetApp",
    "netbackup":    "NetBackup",
    "ontap":        "ONTAP",
    "snapcenter":   "SnapCenter",
    "snapmirror":   "SnapMirror",
    # ── Pure Storage products ────────────────────────────────────────────────
    "cloudiq":      "CloudIQ",
    "flasharray":   "FlashArray",
    "flashblade":   "FlashBlade",
    "insightiq":    "InsightIQ",
    "pure":         "Pure",
    "pure1":        "Pure1",
    # ── Cisco / Brocade ──────────────────────────────────────────────────────
    "brocade":      "Brocade",
    "cisco":        "Cisco",
    "sannav":       "SANnav",
    # ── Other vendors & tools ────────────────────────────────────────────────
    "ansible":      "Ansible",
    "aria":         "Aria",
    "commvault":    "Commvault",
    "confluence":   "Confluence",
    "cyberark":     "CyberArk",
    "git":          "Git",
    "github":       "GitHub",
    "horizon":      "Horizon",
    "jira":         "Jira",
    "keystone":     "Keystone",
    "linux":        "Linux",
    "nexus":        "Nexus",
    "ollama":       "Ollama",
    "openai":       "OpenAI",
    "powershell":   "PowerShell",
    "python":       "Python",
    "servicenow":   "ServiceNow",
    "superna":      "Superna",
    "tanzu":        "Tanzu",
    "terraform":    "Terraform",
    "veeam":        "Veeam",
    "venafi":       "Venafi",
    "windows":      "Windows",
}

# Prepositions / conjunctions that stay lowercase unless they open the title.
# Based on Chicago Manual of Style title-case rules.
_LOWERCASE_WORDS = {
    "a", "an", "and", "as", "at", "but", "by", "for", "if",
    "in", "nor", "of", "off", "on", "or", "so", "the", "to",
    "up", "via", "vs", "with", "yet",
}


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
            # Prepositions stay lowercase unless they open the title
            out.append(lower)
        else:
            # If the word came from a folder name it will be all-lowercase
            # (after MkDocs capitalize()). Force first letter up.
            # If it already has mixed case (came from a page H1), leave it.
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

    # ── Step 2: explicit labels for Home and Site Map ────────────────────────
    for item in nav.items:
        if hasattr(item, "file") and item.file:
            src = item.file.src_path
            if src == "index.md":
                item.title = "Home"
            elif src == "site-map.md":
                item.title = "Site Map"

    # ── Step 3: restructure → Home | Platforms | Site Map ───────────────────
    home = next(
        (i for i in nav.items
         if hasattr(i, "file") and i.file and i.file.src_path == "index.md"),
        None,
    )
    sitemap = next(
        (i for i in nav.items
         if hasattr(i, "file") and i.file and i.file.src_path == "site-map.md"),
        None,
    )

    middle = [i for i in nav.items if i is not home and i is not sitemap]

    if middle:
        # Order sections logically — core platforms first, then supporting areas.
        # Derived from the folder names MkDocs uses as section keys.
        SECTION_ORDER = [
            "virtualization",
            "cloud",
            "storage",
            "san",
            "compute",
            "networking",
            "monitoring",
            "security",
            "tools",
            "automation",
            "disaster-recovery",
            "data-protection",
            "troubleshooting",
            "runbooks",
            "change-management",
            "architecture",
            "performance",
            "certifications",
            "project-management",
            "protocols",
            "database",
            "integration",
            "inventory",
            "lifecycle",
            "ai",
            "start-here",
        ]

        def _section_key(item):
            # Use the item's url path or title to determine sort key.
            # Sections have a url derived from their folder; pages have file.src_path.
            url = getattr(item, "url", None) or ""
            # Strip leading slash and trailing slash, take first segment
            slug = url.strip("/").split("/")[0] if url else ""
            if not slug:
                # Fallback: derive from title
                slug = item.title.lower().replace(" ", "-") if item.title else ""
            try:
                return SECTION_ORDER.index(slug)
            except ValueError:
                return len(SECTION_ORDER)  # unknown sections go last

        middle_sorted = sorted(middle, key=_section_key)

        platforms = Section(title="Platforms", children=middle_sorted)
        for child in middle_sorted:
            child.parent = platforms

        new_items = []
        if home:
            new_items.append(home)
        new_items.append(platforms)
        if sitemap:
            new_items.append(sitemap)
        nav.items = new_items

    return nav
