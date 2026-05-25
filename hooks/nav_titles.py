ACRONYM_TITLES = {
    "Ai": "AI",
    "Aws": "AWS",
    "Dns": "DNS",
    "Esxi": "ESXi",
    "Iam": "IAM",
    "Iscsi": "iSCSI",
    "Ldap": "LDAP",
    "Mfa": "MFA",
    "Mds": "MDS",
    "Nfs": "NFS",
    "Nsx": "NSX",
    "Ntp": "NTP",
    "Rbac": "RBAC",
    "San": "SAN",
    "Snmp": "SNMP",
    "Snmpv3": "SNMPv3",
    "Srm": "SRM",
    "Tls": "TLS",
    "Vsan": "vSAN",
    "Vxrail": "VxRail",
}


def _fix(item):
    if hasattr(item, "title") and item.title in ACRONYM_TITLES:
        item.title = ACRONYM_TITLES[item.title]
    for child in getattr(item, "children", None) or []:
        _fix(child)


def on_nav(nav, **kwargs):
    for item in nav:
        _fix(item)
    return nav
