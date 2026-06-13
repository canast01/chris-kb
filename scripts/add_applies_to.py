#!/usr/bin/env python3
"""
Add 'Applies to:' version line into kb-summary for product pages that are missing it.
"""
import os, re

DOCS = "docs"

PRODUCT_VERSIONS = {
    "vcenter":  "*Applies to: vSphere 7.x · 8.x*",
    "esxi":     "*Applies to: vSphere 7.x · 8.x*",
    "vsan":     "*Applies to: vSAN 7.x · 8.x*",
    "nsx":      "*Applies to: NSX-T 3.x · NSX 4.x*",
    "vmware-cloud-foundation": "*Applies to: VCF 4.x · 5.x*",
    "horizon":  "*Applies to: Horizon 8.x*",
    "srm":      "*Applies to: SRM 8.x*",
    "vsphere-replication": "*Applies to: vSphere Replication 8.x*",
    "aria-operations": "*Applies to: Aria Operations 8.x*",
    "aria-operations-for-logs": "*Applies to: Aria Operations for Logs 8.x*",
    "aria-suite-lifecycle": "*Applies to: Aria Suite Lifecycle 8.x*",
    "powercli":  "*Applies to: PowerCLI 13.x*",
    "vxrail":   "*Applies to: VxRail 7.x · 8.x*",
    "openshift": "*Applies to: OpenShift 4.x*",
    "nutanix":  "*Applies to: AOS 6.x · AHV*",
    "evs":      "*Applies to: Amazon EVS*",
    "ceph":     "*Applies to: Red Hat Ceph Storage · Upstream Ceph*",
}

SUMMARY_RE = re.compile(r'(<div class="kb-summary">)(.*?)(</div>)', re.DOTALL)

def get_product(path):
    parts = os.path.normpath(path).split(os.sep)
    for p in parts:
        if p in PRODUCT_VERSIONS:
            return p
    return None

fixed = 0
for root, dirs, files in os.walk(DOCS):
    dirs[:] = sorted(d for d in dirs if not d.startswith('.'))
    for f in sorted(files):
        if not f.endswith('.md'):
            continue
        path = os.path.join(root, f)
        product = get_product(path)
        if not product:
            continue
        text = open(path, encoding='utf-8').read()
        if 'Applies to' in text:
            continue
        if '<div class="kb-summary">' not in text:
            continue
        applies = PRODUCT_VERSIONS[product]

        def _patch(m, a=applies):
            body = m.group(2).rstrip()
            return f'{m.group(1)}{body}\n\n{a}\n{m.group(3)}'

        new_text = SUMMARY_RE.sub(_patch, text, count=1)
        if new_text != text:
            open(path, 'w', encoding='utf-8').write(new_text)
            print(f"  FIXED  {os.path.relpath(path, DOCS)}")
            fixed += 1

print(f"\nTotal: {fixed} pages updated")
