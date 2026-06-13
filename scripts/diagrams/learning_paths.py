"""Learning path diagrams — one per product, 75 total."""
from ._core import kb_diagram, make_helpers, bTop, bMid, bBot, merge, title_border

W2 = 103
# 5-column layout — margin=3, gap=2, inner=[16,16,17,16,16]
# python3 scripts/ascii_diagram_gen.py --layout 16 16 17 16 16 --margin 3 --gap 2
A_L, A_R = 3, 20     # Architecture (inner=16)
D_L, D_R = 23, 40    # Deploy       (inner=16)
O_L, O_R = 43, 61    # Operations   (inner=17)
S_L, S_R = 64, 81    # Security     (inner=16)
T_L, T_R = 84, 101   # Troubleshoot (inner=16)


def _lp(product_name):
    """Return a learning-path diagram function for the given product name."""
    def _diagram():
        R, txt_row = make_helpers(W2)
        lines = []
        lines.append(title_border(W2, f'{product_name} — Learning Path'))
        lines.append(txt_row())
        lines.append(txt_row('  5 stages in order: Architecture → Deploy → Operations → Security → Troubleshoot'))
        lines.append(txt_row())
        lines.append(R(merge(bTop(A_L, A_R), bTop(D_L, D_R), bTop(O_L, O_R), bTop(S_L, S_R), bTop(T_L, T_R))))
        lines.append(R(merge(
            bMid(A_L, A_R, 'Architecture'),
            bMid(D_L, D_R, 'Deploy'),
            bMid(O_L, O_R, 'Operations'),
            bMid(S_L, S_R, 'Security'),
            bMid(T_L, T_R, 'Troubleshoot'),
        )))
        lines.append(R(merge(
            bMid(A_L, A_R, ''),
            bMid(D_L, D_R, ''),
            bMid(O_L, O_R, ''),
            bMid(S_L, S_R, ''),
            bMid(T_L, T_R, ''),
        )))
        lines.append(R(merge(
            bMid(A_L, A_R, 'How It Works'),
            bMid(D_L, D_R, 'Initial Setup'),
            bMid(O_L, O_R, 'Health Checks'),
            bMid(S_L, S_R, 'Access Control'),
            bMid(T_L, T_R, 'Common Issues'),
        )))
        lines.append(R(merge(
            bMid(A_L, A_R, 'Design Standards'),
            bMid(D_L, D_R, 'Install/Upgrade'),
            bMid(O_L, O_R, 'CLI Reference'),
            bMid(S_L, S_R, 'Authentication'),
            bMid(T_L, T_R, 'Diagnostics'),
        )))
        lines.append(R(merge(
            bMid(A_L, A_R, 'Integrations'),
            bMid(D_L, D_R, ''),
            bMid(O_L, O_R, 'Procedures'),
            bMid(S_L, S_R, 'Encryption'),
            bMid(T_L, T_R, 'Escalation'),
        )))
        lines.append(R(merge(
            bMid(A_L, A_R, ''),
            bMid(D_L, D_R, ''),
            bMid(O_L, O_R, 'Backup & Restore'),
            bMid(S_L, S_R, 'Hardening'),
            bMid(T_L, T_R, ''),
        )))
        lines.append(R(merge(
            bMid(A_L, A_R, ''),
            bMid(D_L, D_R, ''),
            bMid(O_L, O_R, 'Scripts'),
            bMid(S_L, S_R, ''),
            bMid(T_L, T_R, ''),
        )))
        lines.append(R(merge(bBot(A_L, A_R), bBot(D_L, D_R), bBot(O_L, O_R), bBot(S_L, S_R), bBot(T_L, T_R))))
        lines.append(txt_row())
        lines.append(txt_row('  Stage 1 (Architecture) builds understanding. Stage 3 (Operations) is daily work. Troubleshoot last.'))
        lines.append(txt_row())
        lines.append('└' + '─' * W2 + '┘')
        return lines
    return _diagram


# ── Registration table ─────────────────────────────────────────────────────────
# (key, file, product_name)

_LP = [
    # VMware core
    ('lp-vcenter',   'docs/virtualization/vmware/vcenter/learning-path/index.md',                   'vCenter Server'),
    ('lp-esxi',      'docs/virtualization/vmware/esxi/learning-path/index.md',                       'ESXi'),
    ('lp-vsan',      'docs/virtualization/vmware/vsan/learning-path/index.md',                       'vSAN'),
    ('lp-nsx',       'docs/virtualization/vmware/nsx/learning-path/index.md',                        'NSX'),
    ('lp-vcf',       'docs/virtualization/vmware/vmware-cloud-foundation/learning-path/index.md',    'VMware Cloud Foundation'),
    ('lp-vxrail-vm', 'docs/virtualization/vmware/vxrail/learning-path/index.md',                    'VxRail'),
    ('lp-vxrail',    'docs/virtualization/vxrail/learning-path/index.md',                            'VxRail'),
    # VMware Aria + apps
    ('lp-aria-ops',     'docs/virtualization/vmware/aria-operations/learning-path/index.md',             'Aria Operations'),
    ('lp-aria-logs',    'docs/virtualization/vmware/aria-operations-for-logs/learning-path/index.md',    'Aria Operations for Logs'),
    ('lp-aria-net',     'docs/virtualization/vmware/aria-operations-for-networks/learning-path/index.md','Aria Operations for Networks'),
    ('lp-aria-auto',    'docs/virtualization/vmware/aria-automation/learning-path/index.md',             'Aria Automation'),
    ('lp-aria-lcm',     'docs/virtualization/vmware/aria-suite-lifecycle/learning-path/index.md',        'Aria Suite Lifecycle'),
    ('lp-horizon',      'docs/virtualization/vmware/horizon/learning-path/index.md',                     'Horizon'),
    ('lp-srm',          'docs/virtualization/vmware/srm/learning-path/index.md',                         'Site Recovery Manager'),
    ('lp-tanzu',        'docs/virtualization/vmware/tanzu/learning-path/index.md',                       'Tanzu'),
    ('lp-vsphere-rep',  'docs/virtualization/vmware/vsphere-replication/learning-path/index.md',         'vSphere Replication'),
    ('lp-powercli',     'docs/virtualization/vmware/powercli/learning-path/index.md',                    'PowerCLI'),
    # OpenShift + Ceph
    ('lp-openshift', 'docs/virtualization/openshift/learning-path/index.md', 'OpenShift'),
    ('lp-ceph',      'docs/storage/ceph/learning-path/index.md',             'Ceph'),
    # Pure Storage
    ('lp-flasharray',    'docs/storage/pure/flasharray/learning-path/index.md',    'FlashArray'),
    ('lp-flashblade',    'docs/storage/pure/flashblade/learning-path/index.md',    'FlashBlade'),
    ('lp-evergreen',     'docs/storage/pure/evergreen/learning-path/index.md',     'Evergreen'),
    ('lp-evergreen-one', 'docs/storage/pure/evergreen-one/learning-path/index.md', 'Evergreen//One'),
    ('lp-pure1',         'docs/storage/pure/pure1/learning-path/index.md',         'Pure1'),
    # Dell Storage
    ('lp-powermax',   'docs/storage/dell/powermax/learning-path/index.md',                'PowerMax'),
    ('lp-powerstore', 'docs/storage/dell/powerstore/learning-path/index.md',              'PowerStore'),
    ('lp-unity',      'docs/storage/dell/unity/learning-path/index.md',                   'Unity XT'),
    ('lp-powerscale', 'docs/storage/dell/powerscale/learning-path/index.md',              'PowerScale'),
    ('lp-dd',         'docs/storage/dell/data-domain/learning-path/index.md',             'Data Domain'),
    ('lp-rp',         'docs/storage/dell/recoverpoint/learning-path/index.md',            'RecoverPoint'),
    ('lp-srdf-a',     'docs/storage/dell/srdf-a/learning-path/index.md',                  'SRDF/A'),
    ('lp-srdf-s',     'docs/storage/dell/srdf-s/learning-path/index.md',                  'SRDF/S'),
    ('lp-vplex',      'docs/storage/dell/vplex/learning-path/index.md',                   'VPLEX'),
    ('lp-ecs',        'docs/storage/dell/ecs/learning-path/index.md',                     'ECS'),
    ('lp-apex',       'docs/storage/dell/apex-storage-as-a-service/learning-path/index.md', 'APEX Storage'),
    ('lp-cloudiq',    'docs/storage/dell/cloudiq/learning-path/index.md',                 'CloudIQ'),
    ('lp-cod',        'docs/storage/dell/cod/learning-path/index.md',                     'Capacity on Demand'),
    ('lp-fod',        'docs/storage/dell/fod/learning-path/index.md',                     'Features on Demand'),
    ('lp-powerpath',  'docs/storage/dell/powerpath/learning-path/index.md',               'PowerPath'),
    ('lp-dell-aiops', 'docs/storage/dell/dell-aiops/learning-path/index.md',              'Dell AIOps'),
    # NetApp
    ('lp-ontap',    'docs/storage/netapp/ontap/learning-path/index.md',               'ONTAP'),
    ('lp-smirror',  'docs/storage/netapp/snapmirror/learning-path/index.md',          'SnapMirror'),
    ('lp-scenter',  'docs/storage/netapp/snapcenter/learning-path/index.md',          'SnapCenter'),
    ('lp-keystone', 'docs/storage/netapp/keystone/learning-path/index.md',            'Keystone'),
    ('lp-iiq',      'docs/storage/netapp/insightiq/learning-path/index.md',           'InsightIQ'),
    ('lp-eyeglass', 'docs/storage/netapp/superna-eyeglass/learning-path/index.md',   'Superna Eyeglass'),
    # SAN — Brocade
    ('lp-fos',    'docs/san/brocade/fabric-os/learning-path/index.md', 'Fabric OS'),
    ('lp-sannav', 'docs/san/brocade/sannav/learning-path/index.md',    'SANnav'),
    # SAN — Cisco
    ('lp-mds',    'docs/san/cisco/mds/learning-path/index.md',              'Cisco MDS'),
    ('lp-dcnm',   'docs/san/cisco/cisco-dcnm/learning-path/index.md',       'Cisco DCNM'),
    ('lp-nd',     'docs/san/cisco/nexus-dashboard/learning-path/index.md',  'Nexus Dashboard'),
    # Security
    ('lp-certs',    'docs/security/certificates/learning-path/index.md', 'Certificates'),
    ('lp-cyberark', 'docs/security/cyberark/learning-path/index.md',     'CyberArk'),
    ('lp-venafi',   'docs/security/venafi/learning-path/index.md',       'Venafi'),
    # Cloud
    ('lp-aws',     'docs/cloud/aws/learning-path/index.md',     'AWS'),
    ('lp-aws-evs', 'docs/cloud/aws/evs/learning-path/index.md', 'Amazon EVS'),
    ('lp-azure',   'docs/cloud/azure/learning-path/index.md',   'Azure'),
    # Automation
    ('lp-ansible',  'docs/automation/ansible/learning-path/index.md',       'Ansible'),
    ('lp-tf',       'docs/automation/terraform/learning-path/index.md',     'Terraform'),
    ('lp-python',   'docs/automation/python/learning-path/index.md',        'Python'),
    ('lp-ps',       'docs/automation/powershell/learning-path/index.md',    'PowerShell'),
    ('lp-gha',      'docs/automation/github-actions/learning-path/index.md','GitHub Actions'),
    # ITSM
    ('lp-confluence', 'docs/itsm/confluence/learning-path/index.md', 'Confluence'),
    ('lp-jira',       'docs/itsm/jira/learning-path/index.md',       'Jira'),
    ('lp-snow',       'docs/itsm/servicenow/learning-path/index.md', 'ServiceNow'),
    ('lp-git',        'docs/itsm/git/learning-path/index.md',        'Git'),
    # Compute
    ('lp-linux',  'docs/compute/linux/learning-path/index.md',                              'Linux'),
    ('lp-mysql',  'docs/compute/linux/mysql/learning-path/index.md',                        'MySQL'),
    ('lp-pgsql',  'docs/compute/linux/postgresql/learning-path/index.md',                   'PostgreSQL'),
    ('lp-winsrv', 'docs/compute/windows-server/learning-path/index.md',                     'Windows Server'),
    ('lp-ad',     'docs/compute/windows-server/active-directory/learning-path/index.md',    'Active Directory'),
    ('lp-mssql',  'docs/compute/windows-server/sql-server/learning-path/index.md',          'SQL Server'),
    # Backup
    ('lp-veeam',     'docs/backup/veeam/learning-path/index.md',     'Veeam'),
    ('lp-commvault', 'docs/backup/commvault/learning-path/index.md', 'Commvault'),
    ('lp-netbackup', 'docs/backup/netbackup/learning-path/index.md', 'NetBackup'),
]

for _key, _file, _name in _LP:
    kb_diagram(_key, _file, f'{_name} — 5-stage learning path')(_lp(_name))
