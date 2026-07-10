#!/usr/bin/env python3
"""Bulk-insert *Applies to: ...* markers into content pages missing them."""
import re, os, sys

DOCS = os.path.join(os.path.dirname(__file__), '..', 'docs')
DOCS = os.path.abspath(DOCS)

_APPLIES_PAT = re.compile(r'\*Applies to:', re.IGNORECASE)
_APPLIES_SKIP = {'tags.md', 'site-map.md', 'usage-metrics.md', 'site-quality.md', 'index.md'}

# Prefix → version string (longest match wins)
VERSIONS = {
    'automation/ansible':            'Ansible 2.x',
    'automation/github-actions':     'GitHub Actions',
    'automation/powershell':         'PowerShell 5.x / 7.x',
    'automation/python':             'Python 3.x',
    'automation/terraform':          'Terraform 1.x',
    'backup/products/commvault':              'Commvault 11.x',
    'backup/products/netbackup':              'NetBackup 10.x',
    'backup/products/veeam':                  'Veeam Backup & Replication 12.x',
    'cloud/aws/evs':                 'AWS Elastic VMware Service',
    'cloud/aws/ai':                  'AWS AI / SageMaker',
    'cloud/aws':                     'AWS',
    'cloud/azure':                   'Azure',
    'cloud/gcp':                     'GCP',
    'cloud/ai':                      'Cloud AI',
    'compute/linux/mysql':           'Linux · MySQL 8.x',
    'compute/linux/nginx':           'Linux · nginx',
    'compute/linux/postgresql':      'Linux · PostgreSQL 16.x',
    'compute/linux/rhel':            'RHEL 8.x / 9.x',
    'compute/linux/ubuntu':          'Ubuntu 22.04 LTS / 24.04 LTS',
    'compute/linux':                 'Linux (RHEL / Ubuntu / Debian)',
    'compute/windows-server/active-directory': 'Windows Server 2022 · Active Directory',
    'compute/windows-server/hyper-v': 'Windows Server 2022 · Hyper-V',
    'compute/windows-server/iis':    'Windows Server 2022 · IIS',
    'compute/windows-server/sql-server': 'Windows Server 2022 · SQL Server',
    'compute/windows-server':        'Windows Server 2019 / 2022',
    'compute/vmware-tools':          'VMware Tools 12.x',
    'itsm/confluence':               'Confluence',
    'itsm/git':                      'Git',
    'itsm/jira':                     'Jira',
    'itsm/servicenow':               'ServiceNow',
    'labs':                          'Lab / Nested Environment',
    'reference/cheat-sheets':        'All products',
    'reference/decision-trees':      'All products',
    'reference/incident-response':   'All products',
    'reference/interaction-map':     'All products',
    'reference/quick-start':         'All products',
    'reference':                     'All products',
    'san/brocade':                   'Brocade FOS 9.x',
    'san/cisco':                     'Cisco MDS / NX-OS',
    'security/cyberark':             'CyberArk PAS 12.x',
    'security/venafi':               'Venafi Trust Protection Platform',
    'security':                      'All products (Security)',
    'storage/ceph':                  'Ceph 18.x (Reef)',
    'storage/dell/powermax':         'Dell PowerMax · VMAX',
    'storage/dell/powerflex':        'Dell PowerFlex 4.x',
    'storage/dell/powerpath':        'Dell PowerPath 7.x',
    'storage/dell/powerprotect':     'Dell PowerProtect Data Manager',
    'storage/dell/powerscale':       'Dell PowerScale (Isilon) 9.x',
    'storage/dell/powerstore':       'Dell PowerStore 3.x',
    'storage/dell/powervault':       'Dell PowerVault ME5',
    'storage/dell/cloudiq':          'Dell CloudIQ',
    'storage/dell/cod':              'Dell Cloud Object Detachment',
    'storage/dell':                  'Dell EMC Storage',
    'storage/netapp/snapmirror':     'NetApp ONTAP 9.x · SnapMirror',
    'storage/netapp/san':            'NetApp ONTAP 9.x · SAN',
    'storage/netapp/snapvault':      'NetApp ONTAP 9.x · SnapVault',
    'storage/netapp':                'NetApp ONTAP 9.x',
    'storage/pure/flasharray':       'Pure Storage FlashArray',
    'storage/pure/flashblade':       'Pure Storage FlashBlade',
    'storage/pure':                  'Pure Storage',
    'storage/runbooks':              'Storage (multi-vendor)',
    'virtualization/nutanix':        'Nutanix AOS 6.x · AHV',
    'virtualization/openshift':      'OpenShift 4.x',
    'virtualization/vmware/esxi':    'VMware ESXi 7.x / 8.x',
    'virtualization/vmware/vcenter': 'VMware vCenter 7.x / 8.x',
    'virtualization/vmware/vsphere': 'VMware vSphere 7.x / 8.x',
    'virtualization/vmware/vsan':    'VMware vSAN 7.x / 8.x',
    'virtualization/vmware/nsx':     'VMware NSX-T 3.x / 4.x',
    'virtualization/vmware/vxrail':  'Dell VxRail 7.x / 8.x',
    'virtualization/vmware/horizon': 'VMware Horizon 8.x',
    'virtualization/vmware/site-recovery': 'VMware SRM 9.x',
    'virtualization/vmware/aria':    'VMware Aria 8.x',
    'virtualization/vmware/tanzu':   'VMware Tanzu',
    'virtualization/vmware/hcx':     'VMware HCX 4.x',
    'virtualization/vmware/vcf':     'VMware Cloud Foundation 5.x',
    'virtualization/vmware/powercli': 'VMware PowerCLI 13.x',
    'virtualization/vmware/vcd':     'VMware Cloud Director 10.x',
    'virtualization/vmware/vrops':   'VMware vRealize Operations 8.x',
    'virtualization/vmware/vro':     'VMware vRealize Orchestrator 8.x',
    'virtualization/vmware/vra':     'VMware vRealize Automation 8.x',
    'virtualization/vmware/vcd':     'VMware Cloud Director 10.x',
    'virtualization/vmware/nsxalb':  'VMware NSX Advanced Load Balancer (Avi)',
    'virtualization/vmware':         'VMware vSphere 7.x / 8.x',
    'whats-new.md':                  'All products',
}

H1_PAT = re.compile(r'^(# .+)$', re.MULTILINE)


def version_for(rel_path):
    # Strip docs/ prefix if present
    p = rel_path.replace('\\', '/')
    # Longest prefix match
    best = None
    best_len = -1
    for prefix, ver in VERSIONS.items():
        if p == prefix or p.startswith(prefix + '/') or p.startswith(prefix.rstrip('.md')):
            if len(prefix) > best_len:
                best = ver
                best_len = len(prefix)
    return best or 'See product documentation'


def collect_missing():
    results = []
    for root, dirs, files in os.walk(DOCS):
        dirs.sort()
        for f in sorted(files):
            if not f.endswith('.md'):
                continue
            if f in _APPLIES_SKIP:
                continue
            path = os.path.join(root, f)
            c = open(path, errors='replace').read()
            if 'kb-grid' in c or 'kb-card' in c:
                continue
            if len(c.splitlines()) < 10:
                continue
            if not _APPLIES_PAT.search(c):
                results.append(path)
    return results


def insert_applies_to(path, dry_run=False):
    rel = os.path.relpath(path, DOCS)
    ver = version_for(rel)
    text = open(path, errors='replace').read()
    m = H1_PAT.search(text)
    if not m:
        print(f'  SKIP (no H1): {rel}')
        return False
    insert_pos = m.end()
    marker = f'\n\n*Applies to: {ver}*'
    # Don't double-insert
    snippet = text[insert_pos:insert_pos+60]
    if snippet.lstrip('\n').startswith('*Applies'):
        return False
    new_text = text[:insert_pos] + marker + text[insert_pos:]
    if dry_run:
        print(f'  {rel}: *Applies to: {ver}*')
        return True
    with open(path, 'w') as fh:
        fh.write(new_text)
    return True


if __name__ == '__main__':
    dry_run = '--dry-run' in sys.argv
    paths = collect_missing()
    print(f'Found {len(paths)} pages missing *Applies to:*')
    fixed = 0
    for p in paths:
        if insert_applies_to(p, dry_run=dry_run):
            fixed += 1
    print(f'{"Would fix" if dry_run else "Fixed"} {fixed}/{len(paths)} pages')
