#!/usr/bin/env python3
"""
Add '*Applies to: ...*' version labels to kb-summary blocks across the KB.

Rules:
- Only pages that have a <div class="kb-summary"> block
- Only pages that don't already contain 'Applies to:'
- Version string determined by path prefix (most specific wins)
- None = no version label appropriate (skip silently)

Usage:
    python3 scripts/add_version_labels.py --dry-run
    python3 scripts/add_version_labels.py
    python3 scripts/add_version_labels.py --verbose
"""

import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
DRY  = '--dry-run' in sys.argv
VERBOSE = '--verbose' in sys.argv

# Ordered rules: most specific path prefix first.
# Value = None means skip (no version label appropriate for this section).
RULES = [
    # VMware products
    ("virtualization/vmware/vcenter",                      "vSphere 7.x / 8.x"),
    ("virtualization/vmware/esxi",                         "vSphere 7.x / 8.x"),
    ("virtualization/vmware/vsan",                         "vSAN 7.x / 8.x"),
    ("virtualization/vmware/nsx",                          "NSX-T 3.x / NSX 4.x"),
    ("virtualization/vmware/vcf",                          "VCF 4.x / 5.x"),
    ("virtualization/vmware/vxrail",                       "VxRail 7.x / 8.x"),
    ("virtualization/vmware/aria-automation",              "Aria Automation 8.x"),
    ("virtualization/vmware/aria-operations-for-networks", "Aria Operations for Networks 6.x"),
    ("virtualization/vmware/aria-operations-for-logs",     "Aria Operations for Logs 8.x"),
    ("virtualization/vmware/aria-operations",              "Aria Operations 8.x"),
    ("virtualization/vmware/powercli",                     "PowerCLI 13.x"),
    ("virtualization/vmware/horizon",                      "Horizon 8.x"),
    ("virtualization/vmware/hcx",                          "HCX 4.x"),
    ("virtualization/vmware/tanzu",                        "Tanzu 2.x"),
    ("virtualization/vmware/srm",                          "SRM 8.x"),
    ("virtualization/vmware/certifications",               None),
    ("virtualization/vmware/internals",                    "vSphere 7.x / 8.x"),
    ("virtualization/vmware/operations",                   "vSphere 7.x / 8.x"),
    ("virtualization/vmware/reference",                    "vSphere 7.x / 8.x"),
    ("virtualization/vmware/topics",                       "vSphere 7.x / 8.x"),
    # Nutanix
    ("virtualization/nutanix",                             "AOS 6.x · AHV"),
    # OpenShift
    ("virtualization/openshift",                           "OpenShift 4.x"),
    # Storage — Dell
    ("storage/dell/powerstore",                            "PowerStore 3.x"),
    ("storage/dell/powermax",                              "PowerMax 2500 / 8500"),
    ("storage/dell/unity",                                 "Unity XT"),
    ("storage/dell/recoverpoint",                          "RecoverPoint 5.x"),
    ("storage/dell/srdf-s",                                "SRDF/S"),
    ("storage/dell/srdf-a",                                "SRDF/A"),
    ("storage/dell/vplex",                                 "VPLEX"),
    ("storage/dell/powerscale",                            "PowerScale (Isilon) 9.x"),
    ("storage/dell/ecs",                                   "ECS 3.x"),
    ("storage/dell/data-domain",                           "Data Domain DD OS 7.x"),
    ("storage/dell/cloudiq",                               "CloudIQ"),
    ("storage/dell/cod",                                   "Cloud for Desktop (COD)"),
    ("storage/dell/apex-storage-as-a-service",             "APEX Storage-as-a-Service"),
    ("storage/dell/dell-aiops",                            "Dell AIOps"),
    ("storage/dell/fod",                                   "Dell FOD"),
    ("storage/dell/powerpath",                             "PowerPath"),
    ("storage/dell/secure-connect-gateway",                "Secure Connect Gateway"),
    # Storage — NetApp
    ("storage/netapp/ontap",                               "ONTAP 9.x"),
    ("storage/netapp/snapmirror",                          "SnapMirror"),
    ("storage/netapp/snapcenter",                          "SnapCenter 5.x"),
    ("storage/netapp/keystone",                            "Keystone STaaS"),
    ("storage/netapp/superna-eyeglass",                    "Superna Eyeglass"),
    ("storage/netapp/insightiq",                           "InsightIQ"),
    # Storage — Pure
    ("storage/pure/flasharray",                            "FlashArray Purity 6.x"),
    ("storage/pure/flashblade",                            "FlashBlade Purity//FB 4.x"),
    ("storage/pure/pure1",                                 "Pure1"),
    ("storage/pure/evergreen-one",                         "Evergreen//One"),
    ("storage/pure/evergreen",                             "Evergreen"),
    # Storage — Ceph
    ("storage/ceph",                                       "Ceph 18.x (Reef)"),
    # Storage — generic (no version label)
    ("storage/runbooks",                                   None),
    ("storage/storage-design",                             None),
    ("storage/troubleshooting",                            None),
    ("storage/netapp/operations",                          "ONTAP 9.x"),
    ("storage/pure/operations",                            "FlashArray Purity 6.x"),
    # SAN
    ("san/brocade",                                        "Brocade FOS 9.x"),
    ("san/cisco",                                          "Cisco MDS · Nexus"),
    # Backup
    ("backup/veeam",                                       "Veeam Backup & Replication 12.x"),
    ("backup/netbackup",                                   "NetBackup 10.x"),
    ("backup/commvault",                                   "Commvault 11.x"),
    ("backup/dr-operations",                               None),
    # Compute
    ("compute/linux/mysql",                                "MySQL 8.x · MariaDB 10.x"),
    ("compute/linux/postgresql",                           "PostgreSQL 15.x / 16.x"),
    ("compute/linux",                                      "RHEL 8.x / 9.x · Ubuntu 22.04 / 24.04"),
    ("compute/windows-server/active-directory",            "Active Directory (Windows Server 2019 / 2022)"),
    ("compute/windows-server/sql-server",                  "SQL Server 2019 / 2022"),
    ("compute/windows-server",                             "Windows Server 2019 / 2022"),
    ("compute/local-ai/ollama",                            "Ollama"),
    ("compute/local-ai/gpu",                               None),
    ("compute/local-ai",                                   "Local AI"),
    # Cloud
    ("cloud/aws/evs",                                      "Amazon EVS"),
    ("cloud/aws/certifications",                           None),
    ("cloud/aws",                                          "AWS"),
    ("cloud/azure/certifications",                         None),
    ("cloud/azure",                                        "Azure"),
    ("cloud/ai/aws-bedrock",                               "AWS Bedrock"),
    ("cloud/ai/azure-openai",                              "Azure OpenAI"),
    ("cloud/ai/openai",                                    "OpenAI API"),
    ("cloud/ai/certifications",                            None),
    # Networking — protocol specs, not versioned products
    ("networking",                                         None),
    # Security
    ("security/certificates",                              None),
    ("security/cyberark",                                  "CyberArk PAM"),
    ("security/venafi",                                    "Venafi TLS Protect"),
    ("security",                                           None),
    # Automation
    ("automation/ansible",                                 "Ansible 2.x"),
    ("automation/terraform",                               "Terraform 1.x"),
    ("automation/python",                                  "Python 3.x"),
    ("automation/powershell",                              "PowerShell 7.x"),
    ("automation/github-actions",                          "GitHub Actions"),
    # ITSM
    ("itsm/jira",                                          "Jira Cloud / Data Center"),
    ("itsm/confluence",                                    "Confluence Cloud / Data Center"),
    ("itsm/servicenow",                                    "ServiceNow"),
    ("itsm/git",                                           "Git 2.x"),
    # Certifications — study notes, no product version
    ("certifications",                                     None),
]

SUMMARY_RE = re.compile(r'(<div class="kb-summary">)(.*?)(</div>)', re.DOTALL)
APPLIES_RE = re.compile(r'Applies to:')


def get_version(rel_path: str) -> str | None:
    # Normalise to forward slashes
    rel = rel_path.replace(os.sep, '/')
    for prefix, label in RULES:
        if rel.startswith(prefix):
            return label
    return None  # no rule match → skip


def apply_label(fpath: str, label: str) -> bool:
    content = open(fpath, encoding='utf-8').read()
    if 'Applies to:' in content:
        return False
    m = SUMMARY_RE.search(content)
    if not m:
        return False
    body = m.group(2)
    if APPLIES_RE.search(body):
        return False
    new_body = body.rstrip() + f'\n\n*Applies to: {label}*\n'
    new_content = content[:m.start()] + m.group(1) + new_body + m.group(3) + content[m.end():]
    if not DRY:
        open(fpath, 'w', encoding='utf-8').write(new_content)
    return True


modified = 0
skipped_no_rule = []

for root, dirs, files in os.walk(DOCS):
    dirs[:] = sorted([d for d in dirs if not d.startswith('.')])
    for fname in sorted(files):
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(root, fname)
        rel = os.path.relpath(fpath, DOCS)

        content = open(fpath, encoding='utf-8').read()
        if '<div class="kb-summary">' not in content:
            continue
        if 'Applies to:' in content:
            continue

        label = get_version(rel)
        if label is None:
            skipped_no_rule.append(rel)
            continue

        changed = apply_label(fpath, label)
        if changed:
            modified += 1
            if VERBOSE or DRY:
                print(f'  [{label}] {rel}')

mode = 'DRY RUN — ' if DRY else ''
print(f'\n{mode}{modified} pages updated')
if skipped_no_rule and VERBOSE:
    print(f'\nSkipped (no version label for section): {len(skipped_no_rule)}')
    for r in skipped_no_rule:
        print(f'  - {r}')
elif skipped_no_rule:
    print(f'Skipped (no version label for section): {len(skipped_no_rule)}')
