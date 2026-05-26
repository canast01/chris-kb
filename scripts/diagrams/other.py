"""
Other (Compute, Linux, Windows, SAN, Networking) diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

@kb_diagram(
    'compute',
    'docs/compute/index.md',
    'Compute Platform Overview — Linux and Windows Server side by side',
)
def compute_platform_overview():
    """Compute Platform Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    LX_L, LX_R =  3, 50;  LX_MID = (LX_L + LX_R) // 2   # inner=46
    WS_L, WS_R = 53, 99;  WS_MID = (WS_L + WS_R) // 2   # inner=45
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Compute Platform Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Compute Infrastructure')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Physical and virtual x86-64 servers running Linux and Windows Server workloads')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Remote access: SSH port 22 (Linux) · RDP port 3389 / WinRM 5985 (Windows)')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Out-of-band: Dell iDRAC · HP iLO · IPMI — independent of the host OS')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Automation: Bash/Python (Linux) · PowerShell/DSC (Windows) · Ansible across both')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Both platforms run on the same physical hardware — differentiated by OS and tooling'))
    lines.append(txt_row())
    lines.append(R(arrow([LX_MID, WS_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LX_L, LX_R), bTop(WS_L, WS_R))))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Linux Server'),
        bMid(WS_L, WS_R, 'Windows Server'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'RHEL · Ubuntu · Debian · Rocky · Alpine'),
        bMid(WS_L, WS_R, 'Server 2019 · Server 2022 · Core mode'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Kernel: modules, parameters, namespaces'),
        bMid(WS_L, WS_R, 'Hyper-V: built-in Type 1 hypervisor'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'systemd: service management and boot'),
        bMid(WS_L, WS_R, 'Active Directory Domain Services (AD DS)'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'LVM: flexible logical volume management'),
        bMid(WS_L, WS_R, 'NTFS · ReFS: file systems with ACLs'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Package mgmt: dnf / apt / rpm / dpkg'),
        bMid(WS_L, WS_R, 'Group Policy (GPO): central config'),
    )))
    lines.append(R(merge(bBot(LX_L, LX_R), bBot(WS_L, WS_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Linux and Windows share hardware but differ in tooling, auth, and management patterns'))
    lines.append(txt_row())
    lines.append(R(arrow([LX_MID, WS_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LX_L, LX_R), bTop(WS_L, WS_R))))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Linux Operations'),
        bMid(WS_L, WS_R, 'Windows Operations'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'SSH remote access and key management'),
        bMid(WS_L, WS_R, 'RDP and WinRM remote management'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Performance: perf/sar/iostat/vmstat'),
        bMid(WS_L, WS_R, 'Performance Monitor · Get-Counter'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Security: SELinux/AppArmor · auditd'),
        bMid(WS_L, WS_R, 'Defender AV · Audit Policies · LAPS'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Logs: journalctl · rsyslog · logrotate'),
        bMid(WS_L, WS_R, 'Event Viewer: logs and diagnostics'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Automation: Bash/Python · cron jobs'),
        bMid(WS_L, WS_R, 'PowerShell automation · Task Scheduler'),
    )))
    lines.append(R(merge(bBot(LX_L, LX_R), bBot(WS_L, WS_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Day-to-day operations use platform-native tools and automation frameworks'))
    lines.append(txt_row())
    lines.append(R(arrow([LX_MID, WS_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['SSH', 'RDP', 'WinRM', 'iDRAC / BMC', 'SNMP / Syslog'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Linux remote', 'Windows remote', 'PS remoting', 'Out-of-band', 'Monitoring'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['TCP port 22', 'TCP port 3389', 'TCP 5985/86', 'IPMI / REST', 'UDP 161/162'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Key + cert auth', 'NLA + Kerberos', 'HTTP/S WS-Mgmt', 'DRAC web+CLI', 'MIB + traps'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['SCP · SFTP · rsync', 'mstsc.exe client', 'Invoke-Command', 'Lifecycle Ctrl', 'Nagios/OpenNMS'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 rack servers · NIC teaming · FC HBAs · iDRAC / iLO BMC · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('systemd      = Linux PID 1; manages service units, timers, mounts, and boot targets'))
    lines.append(txt_row('LVM          = Logical Volume Manager; PV → VG → LV abstraction for flexible disk layout'))
    lines.append(txt_row('SELinux      = Security-Enhanced Linux; mandatory access control via kernel labels'))
    lines.append(txt_row('AD DS        = Active Directory Domain Services; LDAP directory + Kerberos KDC for auth'))
    lines.append(txt_row('GPO          = Group Policy Object; settings pushed to computers and users via LDAP'))
    lines.append(txt_row('Hyper-V      = Windows built-in Type 1 hypervisor; supports checkpoints and live migration'))
    lines.append(txt_row('NTFS         = New Technology File System; ACLs, compression, encryption, and quotas'))
    lines.append(txt_row('WinRM        = Windows Remote Management; WS-Management for PowerShell PSRemoting'))
    lines.append(txt_row('iDRAC        = Dell Integrated Remote Access Controller; out-of-band BMC for server mgmt'))
    lines.append(txt_row('LAPS         = Local Admin Password Solution; rotates local admin passwords stored in AD'))
    lines.append(txt_row('auditd       = Linux audit daemon; logs syscall events for security compliance/forensics'))
    lines.append(txt_row('SNMP         = Simple Network Management Protocol; polls device metrics and receives traps'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'linux',
    'docs/compute/linux/index.md',
    'Linux Server Stack — architecture, networking, storage, ops, security, troubleshooting',
)
def linux_server_stack():
    """Linux Server Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    AR_L, AR_R =  3, 33;  AR_MID = (AR_L + AR_R) // 2
    NW_L, NW_R = 36, 66;  NW_MID = (NW_L + NW_R) // 2
    ST_L, ST_R = 69, 99;  ST_MID = (ST_L + ST_R) // 2
    OP_L, OP_R =  3, 33
    SC_L, SC_R = 36, 66
    TR_L, TR_R = 69, 99
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Linux Server Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Linux Administration')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'SSH: remote access · systemctl: service management · journalctl: log inspection')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Package management: dnf (RHEL/Rocky) · apt (Ubuntu/Debian) · rpm / dpkg')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Performance: perf/sar/iostat/vmstat/top · tracing: strace / ltrace / eBPF')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Automation: Bash scripting · Python · Ansible: idempotent configuration management')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Administration tools span all subsystems from the kernel to application processes'))
    lines.append(txt_row())
    lines.append(R(arrow([AR_MID, NW_MID, ST_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(AR_L, AR_R), bTop(NW_L, NW_R), bTop(ST_L, ST_R))))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Architecture'),
        bMid(NW_L, NW_R, 'Networking'),
        bMid(ST_L, ST_R, 'Storage'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Linux kernel: monolithic'),
        bMid(NW_L, NW_R, 'ip/ss: iproute2 toolkit'),
        bMid(ST_L, ST_R, 'LVM: PV → VG → LV chain'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Namespaces: isolation'),
        bMid(NW_L, NW_R, 'iptables/nftables: FW'),
        bMid(ST_L, ST_R, 'XFS · ext4 · Btrfs: FS'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'cgroups: resource limits'),
        bMid(NW_L, NW_R, 'NetworkManager/netplan'),
        bMid(ST_L, ST_R, 'NFS/CIFS: network mounts'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'systemd: PID 1, init'),
        bMid(NW_L, NW_R, 'NIC bonding: 802.3ad'),
        bMid(ST_L, ST_R, 'multipath: I/O failover'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'VFS: unified file layer'),
        bMid(NW_L, NW_R, 'DNS: resolv.conf+systemd'),
        bMid(ST_L, ST_R, 'RAID: md software RAID'),
    )))
    lines.append(R(merge(bBot(AR_L, AR_R), bBot(NW_L, NW_R), bBot(ST_L, ST_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Kernel subsystems provide isolation, networking, and storage to all processes'))
    lines.append(txt_row())
    lines.append(R(arrow([AR_MID, NW_MID, ST_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(OP_L, OP_R), bTop(SC_L, SC_R), bTop(TR_L, TR_R))))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'Operations'),
        bMid(SC_L, SC_R, 'Security'),
        bMid(TR_L, TR_R, 'Troubleshooting'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'cron/anacron: scheduling'),
        bMid(SC_L, SC_R, 'SELinux: MAC enforcement'),
        bMid(TR_L, TR_R, 'strace: syscall tracing'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'systemd timers: modern'),
        bMid(SC_L, SC_R, 'AppArmor: profile confinement'),
        bMid(TR_L, TR_R, 'tcpdump: packet capture'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'logrotate: log lifecycle'),
        bMid(SC_L, SC_R, 'sudo/PAM: privilege ctrl'),
        bMid(TR_L, TR_R, 'dmesg: kernel ring buffer'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'tuned: performance tuning'),
        bMid(SC_L, SC_R, 'auditd: syscall auditing'),
        bMid(TR_L, TR_R, 'lsof: open file/port map'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'ulimits: resource caps'),
        bMid(SC_L, SC_R, 'SSH: key auth + MFA'),
        bMid(TR_L, TR_R, 'perf: CPU profiling'),
    )))
    lines.append(R(merge(bBot(OP_L, OP_R), bBot(SC_L, SC_R), bBot(TR_L, TR_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Operations, security, and troubleshooting tools work at the OS and kernel level'))
    lines.append(txt_row())
    lines.append(R(arrow([AR_MID, NW_MID, ST_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['SSH', 'SFTP / SCP', 'NFS', 'SMB / CIFS', 'rsync'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Secure shell', 'File transfer', 'Unix FS mounts', 'Windows shares', 'Sync + backup'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['TCP port 22', 'SSH subsystem', 'TCP/UDP 2049', 'TCP 445', 'TCP 873'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['PubKey + TOTP', 'sftp/scp cmds', 'exports+fstab', 'smb.conf+fstab', 'rsync daemon'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['sshd_config', 'SFTP server', 'mount.nfs', 'mount.cifs', 'Incremental'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · NIC teaming · FC/iSCSI HBAs · iDRAC/iLO BMC · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('systemd  = PID 1 init system; manages service units, timers, mounts, and boot targets'))
    lines.append(txt_row('SELinux  = Security-Enhanced Linux; mandatory access control using kernel labels'))
    lines.append(txt_row('LVM      = Logical Volume Manager; abstracts physical disks into flexible logical volumes'))
    lines.append(txt_row('iproute2 = Modern Linux networking toolkit; ip, ss, tc replace ifconfig and route'))
    lines.append(txt_row('iptables = Linux kernel packet-filter firewall; replaced by nftables in newer kernels'))
    lines.append(txt_row('NFS      = Network File System; mounts remote directories over IP using exports/fstab'))
    lines.append(txt_row('cgroups  = Control Groups; kernel feature that limits CPU, memory, and I/O per process'))
    lines.append(txt_row('strace   = System call tracer; shows every kernel call a process makes in real time'))
    lines.append(txt_row('auditd   = Linux audit daemon; logs syscall events for compliance and forensic analysis'))
    lines.append(txt_row('PAM      = Pluggable Authentication Modules; controls how logins and sudo authenticate'))
    lines.append(txt_row('tuned    = Linux performance daemon; applies OS profiles for different workload types'))
    lines.append(txt_row('multipath= Device mapper feature; aggregates HBA paths to a single block device'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'windows',
    'docs/compute/windows-server/index.md',
    'Windows Server Stack — architecture, networking, AD, ops, security, troubleshooting',
)
def windows_server_stack():
    """Windows Server Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    AR_L, AR_R =  3, 33;  AR_MID = (AR_L + AR_R) // 2
    NW_L, NW_R = 36, 66;  NW_MID = (NW_L + NW_R) // 2
    AD_L, AD_R = 69, 99;  AD_MID = (AD_L + AD_R) // 2
    OP_L, OP_R =  3, 33
    SC_L, SC_R = 36, 66
    TR_L, TR_R = 69, 99
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Windows Server Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Windows Server Administration')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Server Manager · PowerShell · Windows Admin Center · Event Viewer · Task Scheduler')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Remote management: RDP (3389) · WinRM (5985/5986) · PowerShell PSRemoting')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Monitoring: Performance Monitor · Get-Counter · Resource Monitor · Defender')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Automation: PowerShell DSC · Scheduled Tasks · Group Policy · Ansible WinRM')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Administration tools span OS architecture, networking, and Active Directory'))
    lines.append(txt_row())
    lines.append(R(arrow([AR_MID, NW_MID, AD_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(AR_L, AR_R), bTop(NW_L, NW_R), bTop(AD_L, AD_R))))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Architecture'),
        bMid(NW_L, NW_R, 'Networking'),
        bMid(AD_L, AD_R, 'Active Directory'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Server 2019 / 2022'),
        bMid(NW_L, NW_R, 'DNS Server: zone mgmt'),
        bMid(AD_L, AD_R, 'AD DS: domain services'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'NTFS · ReFS filesystems'),
        bMid(NW_L, NW_R, 'DHCP Server: IP leasing'),
        bMid(AD_L, AD_R, 'Group Policy (GPO)'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Registry: config database'),
        bMid(NW_L, NW_R, 'NIC Teaming: LACP bonds'),
        bMid(AD_L, AD_R, 'Kerberos: auth tickets'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Services: Win32 daemons'),
        bMid(NW_L, NW_R, 'Windows Firewall + WDF'),
        bMid(AD_L, AD_R, 'LDAP: directory queries'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Hyper-V: Type 1 hypervisor'),
        bMid(NW_L, NW_R, 'DFS-N: namespace sharing'),
        bMid(AD_L, AD_R, 'Trusts: cross-domain auth'),
    )))
    lines.append(R(merge(bBot(AR_L, AR_R), bBot(NW_L, NW_R), bBot(AD_L, AD_R))))

    lines.append(txt_row())
    lines.append(txt_row('  OS architecture, networking, and Active Directory form the Windows platform foundation'))
    lines.append(txt_row())
    lines.append(R(arrow([AR_MID, NW_MID, AD_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(OP_L, OP_R), bTop(SC_L, SC_R), bTop(TR_L, TR_R))))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'Operations'),
        bMid(SC_L, SC_R, 'Security'),
        bMid(TR_L, TR_R, 'Troubleshooting'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'WSUS: patch management'),
        bMid(SC_L, SC_R, 'BitLocker: drive encrypt'),
        bMid(TR_L, TR_R, 'Event Viewer: logs+alerts'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'WinRM: remote execution'),
        bMid(SC_L, SC_R, 'Defender AV + EDR'),
        bMid(TR_L, TR_R, 'SFC / DISM: system repair'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'IIS: web server mgmt'),
        bMid(SC_L, SC_R, 'JEA: Just Enough Admin'),
        bMid(TR_L, TR_R, 'WinPE: recovery env.'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'Volume Shadow Copies'),
        bMid(SC_L, SC_R, 'Audit Policy: event log'),
        bMid(TR_L, TR_R, 'Process Monitor/Explorer'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'FSRM: quota+screening'),
        bMid(SC_L, SC_R, 'LAPS: local admin pwds'),
        bMid(TR_L, TR_R, 'WMI/CIM: system queries'),
    )))
    lines.append(R(merge(bBot(OP_L, OP_R), bBot(SC_L, SC_R), bBot(TR_L, TR_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Operations, security hardening, and diagnostic tools work across all Windows roles'))
    lines.append(txt_row())
    lines.append(R(arrow([AR_MID, NW_MID, AD_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['RDP', 'SMB', 'WinRM', 'Kerberos', 'LDAP / LDAPS'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Remote desktop', 'File sharing', 'PS remoting', 'Authentication', 'Directory'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['TCP 3389', 'TCP 445', 'TCP 5985/86', 'TCP 88/UDP', 'TCP 389/636'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['NLA · TLS 1.2', 'NTLM/Kerberos', 'HTTP · HTTPS', 'KDC ticket srv', 'SSL+SASL bind'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['mstsc.exe', 'net use / UNC', 'Invoke-Command', 'Ticket + PAC', 'ADSI/RSAT tools'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 rack servers · NIC teaming · iDRAC/iLO BMC · Windows licensing · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AD DS    = Active Directory Domain Services; LDAP directory + Kerberos KDC for Windows auth'))
    lines.append(txt_row('GPO      = Group Policy Object; settings pushed to computers and users via LDAP queries'))
    lines.append(txt_row('WinRM    = Windows Remote Management; WS-Management for PowerShell PSRemoting'))
    lines.append(txt_row('Kerberos = Ticket-based authentication protocol; default for all AD domain accounts'))
    lines.append(txt_row('NTFS     = New Technology File System; supports ACLs, compression, and EFS encryption'))
    lines.append(txt_row('Hyper-V  = Windows Type 1 hypervisor; VM checkpoints and live migration built in'))
    lines.append(txt_row('BitLocker= Full-volume encryption using AES; TPM-backed key storage for boot protection'))
    lines.append(txt_row('LAPS     = Local Admin Password Solution; rotates local admin passwords stored in AD'))
    lines.append(txt_row('JEA      = Just Enough Administration; limits PS remoting to specific command sets'))
    lines.append(txt_row('WSUS     = Windows Server Update Services; internal patch distribution server'))
    lines.append(txt_row('SFC      = System File Checker; scans and repairs corrupt Windows system files'))
    lines.append(txt_row('DISM     = Deployment Image Servicing; manages Windows images and component packages'))
    lines.append(txt_row('DFS-N    = Distributed File System Namespace; virtual UNC namespace across share paths'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'san',
    'docs/san/index.md',
    'SAN Fabric Overview — Cisco MDS and Brocade FC fabric side by side',
)
def san_fabric_overview():
    """SAN Fabric Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    CI_L, CI_R =  3, 50;  CI_MID = (CI_L + CI_R) // 2   # inner=46
    BR_L, BR_R = 53, 99;  BR_MID = (BR_L + BR_R) // 2   # inner=45
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'SAN Fabric Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'SAN Fabric Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Cisco: DCNM / Nexus Dashboard · CLI · NX-OS REST API · SNMP · Syslog')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Brocade: SANnav Portal · Fabric OS CLI · REST API · SNMP trap forwarding')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Both vendors: fabric-wide zoning, ISL monitoring, and performance dashboards')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'REST APIs enable programmable fabric automation and health integration')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Management platforms provide fabric-wide visibility, zoning, and lifecycle control'))
    lines.append(txt_row())
    lines.append(R(arrow([CI_MID, BR_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(CI_L, CI_R), bTop(BR_L, BR_R))))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'Cisco MDS (SAN-OS / NX-OS)'),
        bMid(BR_L, BR_R, 'Brocade (Fabric OS)'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'MDS 9000: 16/32/64G FC switches'),
        bMid(BR_L, BR_R, 'Gen 7: 64G FC switching'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'VSANs: virtual fabric isolation'),
        bMid(BR_L, BR_R, 'Zone aliases + zone configs'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'Smart Zoning + device aliases'),
        bMid(BR_L, BR_R, 'ISL trunking + Port Channels'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'IVR: inter-VSAN routing'),
        bMid(BR_L, BR_R, 'QoS: priority FC traffic'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'DCNM / Nexus Dashboard mgmt'),
        bMid(BR_L, BR_R, 'SANnav: fabric management'),
    )))
    lines.append(R(merge(bBot(CI_L, CI_R), bBot(BR_L, BR_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Both vendors deliver 16/32/64G Fibre Channel with zoning and trunked ISLs'))
    lines.append(txt_row())
    lines.append(R(arrow([CI_MID, BR_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(CI_L, CI_R), bTop(BR_L, BR_R))))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'Cisco Fabric Services'),
        bMid(BR_L, BR_R, 'Brocade Fabric Services'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'FLOGI: host login to fabric'),
        bMid(BR_L, BR_R, 'FLOGI DB: registered ports'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'FSPF: fabric shortest path'),
        bMid(BR_L, BR_R, 'D-Port: diagnostics port'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'CFS: config fabric sync'),
        bMid(BR_L, BR_R, 'MAPS: monitoring alerts'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'FCNS: fabric name service'),
        bMid(BR_L, BR_R, 'Buffer Credits: flow ctrl'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'Port modes: F · E · TE · NP'),
        bMid(BR_L, BR_R, 'E-Port: ISL · F-Port: host'),
    )))
    lines.append(R(merge(bBot(CI_L, CI_R), bBot(BR_L, BR_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Fabric protocol services register initiators and targets for SCSI data exchange'))
    lines.append(txt_row())
    lines.append(R(arrow([CI_MID, BR_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FLOGI', 'FDISC', 'Zoning', 'FSPF', 'ISL / Trunk'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['N_Port login', 'NPIV port', 'Access control', 'Link routing', 'E-port links'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['WWPN register', 'Virtual WWPN', 'pWWN / alias', 'Shortest path', 'TE/trunk port'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FC-ID assign', 'HBA multiplex', 'Hard or soft', 'ECMP spread', 'Load balance'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FCNS register', 'VF_Port serve', 'Zone database', 'Path failover', 'BB credits'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('FC switches · 16G/32G/64G SFPs · OM4 fibre · FC HBAs in hosts · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FC       = Fibre Channel; dedicated high-speed block network using optical or copper links'))
    lines.append(txt_row('WWPN     = World Wide Port Name; globally unique 64-bit identifier for each FC HBA port'))
    lines.append(txt_row('WWNN     = World Wide Node Name; 64-bit identifier for the HBA device (node) itself'))
    lines.append(txt_row('FLOGI    = Fabric Login; N-Port registers its WWPN with the fabric to get an FC-ID'))
    lines.append(txt_row('FSPF     = Fabric Shortest Path First; link-state routing protocol for FC fabric paths'))
    lines.append(txt_row('Zoning   = Fabric access control; limits which initiators can communicate with targets'))
    lines.append(txt_row('VSAN     = Virtual SAN (Cisco); logical fabric partition within a shared physical switch'))
    lines.append(txt_row('ISL      = Inter-Switch Link; E-Port or TE-Port carrying aggregated fabric traffic'))
    lines.append(txt_row('NPIV     = N-Port ID Virtualisation; one HBA presents multiple virtual WWPNs'))
    lines.append(txt_row('D-Port   = Diagnostic Port; Brocade link mode for BER and latency testing'))
    lines.append(txt_row('MAPS     = Monitoring and Alerting Policy Suite; Brocade threshold-based SAN alerts'))
    lines.append(txt_row('IVR      = Inter-VSAN Routing; Cisco controlled traffic flow between VSANs'))
    lines.append(txt_row('SANnav   = Brocade SAN management portal; replaced BSNA with modern REST-based UI'))
    lines.append(txt_row('DCNM     = Data Center Network Manager; Cisco fabric management (now Nexus Dashboard)'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'cisco-san',
    'docs/san/cisco/index.md',
    'Cisco SAN Stack — MDS 9000, DCNM, Nexus Dashboard, VSAN, Zoning, ISL',
)
def cisco_san_stack():
    """Cisco SAN Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    MD_L, MD_R =  3, 33;  MD_MID = (MD_L + MD_R) // 2
    DC_L, DC_R = 36, 66;  DC_MID = (DC_L + DC_R) // 2
    ND_L, ND_R = 69, 99;  ND_MID = (ND_L + ND_R) // 2
    VS_L, VS_R =  3, 33
    ZN_L, ZN_R = 36, 66
    IS_L, IS_R = 69, 99
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Cisco SAN Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Cisco SAN Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'DCNM / Nexus Dashboard: GUI fabric management, zoning workflows, and telemetry')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'NX-OS / SAN-OS CLI: config t · show flogi database · show zone status')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'SNMP v3 · Syslog: event collection and forwarding to monitoring platforms')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'REST API: programmable fabric config, metrics, and zoning via HTTPS/JSON')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Management tools span hardware switches, legacy DCNM, and modern Nexus Dashboard'))
    lines.append(txt_row())
    lines.append(R(arrow([MD_MID, DC_MID, ND_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(MD_L, MD_R), bTop(DC_L, DC_R), bTop(ND_L, ND_R))))
    lines.append(R(merge(
        bMid(MD_L, MD_R, 'Cisco MDS 9000'),
        bMid(DC_L, DC_R, 'DCNM'),
        bMid(ND_L, ND_R, 'Nexus Dashboard (ND)'),
    )))
    lines.append(R(merge(
        bMid(MD_L, MD_R, '9132T: 32-port 32G FC'),
        bMid(DC_L, DC_R, 'Data Center Ntwk Mgr'),
        bMid(ND_L, ND_R, 'Successor to DCNM'),
    )))
    lines.append(R(merge(
        bMid(MD_L, MD_R, '9396T: 96-port 32G FC'),
        bMid(DC_L, DC_R, 'Fabric discovery+sync'),
        bMid(ND_L, ND_R, 'Fabric Controller (NDF)'),
    )))
    lines.append(R(merge(
        bMid(MD_L, MD_R, '9700: modular director'),
        bMid(DC_L, DC_R, 'Zoning: templates+push'),
        bMid(ND_L, ND_R, 'Fabric Insights (NDI)'),
    )))
    lines.append(R(merge(
        bMid(MD_L, MD_R, 'Line cards: 16/32/64G'),
        bMid(DC_L, DC_R, 'Performance monitoring'),
        bMid(ND_L, ND_R, 'Multi-site management'),
    )))
    lines.append(R(merge(
        bMid(MD_L, MD_R, 'SAN-OS → NX-OS upgrade'),
        bMid(DC_L, DC_R, 'Health: port + fabric'),
        bMid(ND_L, ND_R, 'Flow telemetry + VXLAN'),
    )))
    lines.append(R(merge(bBot(MD_L, MD_R), bBot(DC_L, DC_R), bBot(ND_L, ND_R))))

    lines.append(txt_row())
    lines.append(txt_row('  MDS hardware, DCNM (legacy), and Nexus Dashboard (current) form the Cisco SAN stack'))
    lines.append(txt_row())
    lines.append(R(arrow([MD_MID, DC_MID, ND_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(VS_L, VS_R), bTop(ZN_L, ZN_R), bTop(IS_L, IS_R))))
    lines.append(R(merge(
        bMid(VS_L, VS_R, 'VSANs'),
        bMid(ZN_L, ZN_R, 'Zoning'),
        bMid(IS_L, IS_R, 'ISL & Trunking'),
    )))
    lines.append(R(merge(
        bMid(VS_L, VS_R, 'Virtual fabric partition'),
        bMid(ZN_L, ZN_R, 'Device aliases: names'),
        bMid(IS_L, IS_R, 'E-Port: standard ISL'),
    )))
    lines.append(R(merge(
        bMid(VS_L, VS_R, 'VSAN membership: port'),
        bMid(ZN_L, ZN_R, 'pWWN or FC ID members'),
        bMid(IS_L, IS_R, 'TE-Port: trunked ISL'),
    )))
    lines.append(R(merge(
        bMid(VS_L, VS_R, 'Domain IDs: 1–239'),
        bMid(ZN_L, ZN_R, 'Smart Zoning: auto-bind'),
        bMid(IS_L, IS_R, 'Port channels: LACP'),
    )))
    lines.append(R(merge(
        bMid(VS_L, VS_R, 'IVR: inter-VSAN route'),
        bMid(ZN_L, ZN_R, 'Enhanced zoning: atomic'),
        bMid(IS_L, IS_R, 'FSPF: load balancing'),
    )))
    lines.append(R(merge(
        bMid(VS_L, VS_R, 'VSAN DB sync via CFS'),
        bMid(ZN_L, ZN_R, 'Zone sets: named policy'),
        bMid(IS_L, IS_R, 'F-Port channels: NPV'),
    )))
    lines.append(R(merge(bBot(VS_L, VS_R), bBot(ZN_L, ZN_R), bBot(IS_L, IS_R))))

    lines.append(txt_row())
    lines.append(txt_row('  VSANs isolate traffic · Zoning controls access · ISL trunks carry aggregated load'))
    lines.append(txt_row())
    lines.append(R(arrow([MD_MID, DC_MID, ND_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FLOGI', 'FDISC', 'FC-NS', 'RSCN', 'CFS'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['N_Port login', 'NPIV port', 'Name service', 'Change notice', 'Fabric sync'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['WWPN + WWNN', 'Virtual ports', 'FCid database', 'Topology chg', 'Atomic apply'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FC-ID: 24-bit', 'HBA multiplex', 'PLOGI follows', 'Zone trigger', 'CFS lock'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FCNS register', 'VF_Port serve', 'show flogi db', 'RSCN payload', 'Full fabric'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS 9000 switches · 16G/32G/64G FC SFPs · OM4 fibre · FC HBAs · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('MDS     = Cisco Multilayer Director Switch; purpose-built FC SAN switches'))
    lines.append(txt_row('NX-OS   = Network OS used on Cisco MDS after SAN-OS; shared CLI with Nexus'))
    lines.append(txt_row('SAN-OS  = Original Cisco MDS OS; succeeded by NX-OS for unified CLI'))
    lines.append(txt_row('VSAN    = Virtual SAN; Cisco method of partitioning one fabric into isolated SANs'))
    lines.append(txt_row('IVR     = Inter-VSAN Routing; allows controlled traffic exchange between VSANs'))
    lines.append(txt_row('DCNM    = Data Center Network Manager; Cisco GUI for MDS zoning and monitoring'))
    lines.append(txt_row('ND      = Nexus Dashboard; successor to DCNM; unified multi-fabric management'))
    lines.append(txt_row('Smart Zoning= Inserts exact FC IDs into zone members; reduces unnecessary RSCN storms'))
    lines.append(txt_row('Device Alias= Fabric-wide friendly name for a WWN; simplifies zone configuration'))
    lines.append(txt_row('CFS     = Cisco Fabric Services; distributes and synchronises config across MDS peers'))
    lines.append(txt_row('RSCN    = Registered State Change Notification; alerts hosts of topology changes'))
    lines.append(txt_row('TE-Port = Trunked E-Port; carries multiple VSANs over one physical ISL link'))
    lines.append(txt_row('NPV     = N-Port Virtualiser; MDS edge mode that proxies logins to a core switch'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'brocade',
    'docs/san/brocade/index.md',
    'Brocade SAN Stack — Fabric OS, SANnav, Zoning, ISL, MAPS, D-Port',
)
def brocade_san_stack():
    """Brocade SAN Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    FO_L, FO_R =  3, 50;  FO_MID = (FO_L + FO_R) // 2   # inner=46
    SN_L, SN_R = 53, 99;  SN_MID = (SN_L + SN_R) // 2   # inner=45
    ZN_L, ZN_R =  3, 50
    IL_L, IL_R = 53, 99
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Brocade SAN Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Brocade SAN Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'SANnav Management Portal: web UI for fabric discovery, zoning, and performance')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Fabric OS CLI: switchshow · cfgshow · zoneshow · supportshow · portcfgshow')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'REST API: HTTPS-based access to FOS config and monitoring data')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'SNMP v3 · Syslog: polling and trap forwarding to SIEM and monitoring tools')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  SANnav and the FOS CLI are the two primary management surfaces for Brocade fabrics'))
    lines.append(txt_row())
    lines.append(R(arrow([FO_MID, SN_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(FO_L, FO_R), bTop(SN_L, SN_R))))
    lines.append(R(merge(
        bMid(FO_L, FO_R, 'Fabric OS (FOS)'),
        bMid(SN_L, SN_R, 'SANnav Management Portal'),
    )))
    lines.append(R(merge(
        bMid(FO_L, FO_R, 'Distributed OS across all ports'),
        bMid(SN_L, SN_R, 'Fabric discovery + inventory'),
    )))
    lines.append(R(merge(
        bMid(FO_L, FO_R, 'Zone management: cfgshow/cfgsave'),
        bMid(SN_L, SN_R, 'Health dashboard + alerts'),
    )))
    lines.append(R(merge(
        bMid(FO_L, FO_R, 'ISL trunking: trunk groups'),
        bMid(SN_L, SN_R, 'Zoning: drag-and-drop UI'),
    )))
    lines.append(R(merge(
        bMid(FO_L, FO_R, 'Port types: E / F / G / D / L'),
        bMid(SN_L, SN_R, 'Performance analytics: IOPS'),
    )))
    lines.append(R(merge(
        bMid(FO_L, FO_R, 'MAPS: threshold-based alerts'),
        bMid(SN_L, SN_R, 'Replaces older BSNA / DCFM'),
    )))
    lines.append(R(merge(bBot(FO_L, FO_R), bBot(SN_L, SN_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Fabric OS runs on the switch; SANnav is the management application layer'))
    lines.append(txt_row())
    lines.append(R(arrow([FO_MID, SN_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(ZN_L, ZN_R), bTop(IL_L, IL_R))))
    lines.append(R(merge(
        bMid(ZN_L, ZN_R, 'Zoning & Security'),
        bMid(IL_L, IL_R, 'ISL & Performance'),
    )))
    lines.append(R(merge(
        bMid(ZN_L, ZN_R, 'Zone aliases: pWWN names'),
        bMid(IL_L, IL_R, 'Trunk groups: 8 ports max'),
    )))
    lines.append(R(merge(
        bMid(ZN_L, ZN_R, 'Zone configs: named sets'),
        bMid(IL_L, IL_R, 'Buffer credits: flow ctrl'),
    )))
    lines.append(R(merge(
        bMid(ZN_L, ZN_R, 'Open / enforce / strict modes'),
        bMid(IL_L, IL_R, 'QoS: high/medium/low lanes'),
    )))
    lines.append(R(merge(
        bMid(ZN_L, ZN_R, 'DCC: device connection ctrl'),
        bMid(IL_L, IL_R, 'D-Port: link diagnostics'),
    )))
    lines.append(R(merge(
        bMid(ZN_L, ZN_R, 'SCC: switch connection ctrl'),
        bMid(IL_L, IL_R, 'Access Gateway: edge mode'),
    )))
    lines.append(R(merge(bBot(ZN_L, ZN_R), bBot(IL_L, IL_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Zoning enforces access control · ISL trunks aggregate bandwidth between switches'))
    lines.append(txt_row())
    lines.append(R(arrow([FO_MID, SN_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FLOGI DB', 'Zoning', 'ISL Trunk', 'MAPS', 'D-Port'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Login register', 'Zone alias', 'Trunk groups', 'Alert policy', 'Link test'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['WWN + FC-ID', 'cfgshow/save', 'trunkshow', 'mapsshow', 'portdiag'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['nsshow cmd', 'cfgenable', 'Port Channel', 'Threshold rules', 'BER testing'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['fabricshow', 'zonecreate', 'Load balance', 'Health scoring', 'Eye margins'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Brocade FC switches · 16G/32G/64G SFPs · OM4 fibre · FC HBAs · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FOS       = Fabric OS; Brocade switch OS distributed across all ports in the switch'))
    lines.append(txt_row('SANnav    = Brocade SAN management portal; replaced BSNA/DCFM with modern REST UI'))
    lines.append(txt_row('MAPS      = Monitoring and Alerting Policy Suite; threshold engine for SAN health'))
    lines.append(txt_row('D-Port    = Diagnostic Port; Brocade link mode for BER and optical latency testing'))
    lines.append(txt_row('Trunk Group= Bundle of ISL ports acting as one logical link for load balancing'))
    lines.append(txt_row('Buffer Credits= FC flow control; limits in-flight frames per port to prevent overflow'))
    lines.append(txt_row('Zone Alias= Named reference to a pWWN; simplifies zone member configuration'))
    lines.append(txt_row('Zone Config= Named collection of zones saved and activated as a policy on the fabric'))
    lines.append(txt_row('cfgshow   = FOS command to display zone config; cfgsave persists to flash'))
    lines.append(txt_row('DCC       = Device Connection Control; restricts ports a WWN may connect to'))
    lines.append(txt_row('SCC       = Switch Connection Control; restricts which switches may join via ISL'))
    lines.append(txt_row('Access Gateway= Brocade edge mode; connects to core switch as an N-Port proxy'))
    lines.append(txt_row('supportshow= FOS diagnostic command; captures full switch state for support cases'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-arch', 'docs/compute/linux/architecture/index.md',
            'Linux Architecture — kernel, init, VFS, namespaces, cgroups, memory')
def linux_arch():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Linux Kernel (monolithic + loadable modules)')))
    lines.append(R(bMid(L, RR, 'Process scheduler: CFS — Completely Fair Scheduler; time-slices CPU per cgroup weight')))
    lines.append(R(bMid(L, RR, 'Memory manager: virtual address spaces, page tables, TLB, OOM killer, hugepages')))
    lines.append(R(bMid(L, RR, 'VFS: Virtual File System layer — unified API over ext4, XFS, Btrfs, tmpfs, procfs')))
    lines.append(R(bMid(L, RR, 'Syscall interface: glibc wraps int 0x80 / SYSCALL into POSIX functions for userspace')))
    lines.append(R(bBot(L, RR)))

    lines.append(txt_row())
    lines.append(txt_row('  Kernel subsystems provide isolation, scheduling, and I/O to all userspace processes'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Namespaces & cgroups'), bMid(L2, R2, 'systemd & init'))))
    lines.append(R(merge(bMid(L1, R1, 'pid: process tree isolation'), bMid(L2, R2, 'PID 1: systemd is init'))))
    lines.append(R(merge(bMid(L1, R1, 'net: network stack isolation'), bMid(L2, R2, 'Units: service/timer/mount'))))
    lines.append(R(merge(bMid(L1, R1, 'mnt: mount point isolation'), bMid(L2, R2, 'Targets: multi-user/graphical'))))
    lines.append(R(merge(bMid(L1, R1, 'cgroup v2: CPU/mem/IO limits'), bMid(L2, R2, 'journald: structured logging'))))
    lines.append(R(merge(bMid(L1, R1, 'user: UID mapping isolation'), bMid(L2, R2, 'socket activation: on-demand'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 CPUs · RAM DIMMs · NVMe/SAS disks · NIC · iDRAC/iLO BMC · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CFS         = Completely Fair Scheduler; distributes CPU time using a red-black tree'))
    lines.append(txt_row('VFS         = Virtual File System; kernel abstraction layer over concrete filesystems'))
    lines.append(txt_row('cgroups     = Control Groups; enforce per-process CPU, memory, and I/O resource limits'))
    lines.append(txt_row('namespace   = Kernel isolation primitive; wraps PIDs, network, mounts, UIDs independently'))
    lines.append(txt_row('systemd     = PID 1 init; manages units (services, timers, mounts) and the boot sequence'))
    lines.append(txt_row('journald    = systemd journal daemon; stores structured binary logs with metadata fields'))
    lines.append(txt_row('OOM killer  = Out-of-Memory killer; terminates processes when the kernel exhausts RAM'))
    lines.append(txt_row('hugepages   = 2 MB / 1 GB pages; reduce TLB misses for memory-intensive workloads'))
    lines.append(txt_row('tmpfs       = RAM-backed filesystem; used for /tmp, /dev/shm, and systemd runtime dirs'))
    lines.append(txt_row('procfs      = /proc virtual filesystem; exposes kernel and process state as readable files'))
    lines.append(txt_row('syscall     = Kernel entry point; userspace requests OS services via a defined ABI'))
    lines.append(txt_row('loadable module= .ko kernel object loaded/unloaded at runtime via modprobe/rmmod'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-arch-how', 'docs/compute/linux/architecture/how-it-works/index.md',
            'Linux Architecture — How It Works: boot, syscall flow, scheduling, I/O path')
def linux_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — How It Works'))
    lines.append(txt_row())

    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Boot Sequence')))
    lines.append(R(bMid(L, RR, 'UEFI/BIOS → GRUB2 bootloader → kernel decompresses into RAM → initramfs mounts root')))
    lines.append(R(bMid(L, RR, 'kernel init: detects hardware, loads drivers, mounts real rootfs, exec /sbin/init')))
    lines.append(R(bMid(L, RR, 'systemd: reads default.target, activates units in dependency order, starts getty')))
    lines.append(R(bMid(L, RR, 'Login: PAM stack authenticates user; bash/zsh shell launched as child of sshd/getty')))
    lines.append(R(bBot(L, RR)))

    lines.append(txt_row())
    lines.append(txt_row('  Every process originates from PID 1 through fork(); exec() loads new program images'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Syscall & I/O Path'), bMid(L2, R2, 'Scheduling & Memory'))))
    lines.append(R(merge(bMid(L1, R1, 'app calls read() via glibc'), bMid(L2, R2, 'CFS picks next task by vruntime'))))
    lines.append(R(merge(bMid(L1, R1, 'SYSCALL instruction → ring 0'), bMid(L2, R2, 'context switch saves registers'))))
    lines.append(R(merge(bMid(L1, R1, 'VFS dispatches to block layer'), bMid(L2, R2, 'page fault → alloc physical page'))))
    lines.append(R(merge(bMid(L1, R1, 'I/O scheduler (mq-deadline)'), bMid(L2, R2, 'mmap: maps file into VA space'))))
    lines.append(R(merge(bMid(L1, R1, 'NVMe/SCSI driver sends cmd'), bMid(L2, R2, 'OOM: score + kill on pressure'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 CPUs (rings 0/3) · RAM · NVMe/SAS · PCIe bus · iDRAC BMC · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('GRUB2       = GRand Unified Bootloader v2; presents boot menu and loads kernel + initramfs'))
    lines.append(txt_row('initramfs   = Temporary RAM root used during boot to mount the real root filesystem'))
    lines.append(txt_row('fork        = Syscall that clones the calling process; child inherits FDs and memory'))
    lines.append(txt_row('exec        = Syscall family that replaces process image with a new program binary'))
    lines.append(txt_row('vruntime    = Virtual runtime; CFS metric tracking how much CPU time a task has used'))
    lines.append(txt_row('context switch= CPU saves registers of running task and loads state of next scheduled task'))
    lines.append(txt_row('page fault  = MMU exception when a virtual address has no mapped physical page yet'))
    lines.append(txt_row('mmap        = Memory-map syscall; maps files or anonymous memory into a process VAS'))
    lines.append(txt_row('mq-deadline = Multi-queue deadline I/O scheduler; prioritises read latency over throughput'))
    lines.append(txt_row('ring 0      = CPU privilege level for kernel code; ring 3 is unprivileged userspace'))
    lines.append(txt_row('PAM         = Pluggable Authentication Modules; configures how login and sudo authenticate'))
    lines.append(txt_row('getty       = Terminal program that presents the login prompt on a virtual console'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-arch-integrations', 'docs/compute/linux/architecture/integrations/index.md',
            'Linux Architecture — Integrations: AD/LDAP, NFS, monitoring, config mgmt')
def linux_arch_integrations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux Architecture — Integrations'))
    lines.append(txt_row())

    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Integration Points')))
    lines.append(R(bMid(L, RR, 'Identity: SSSD + realmd joins Linux hosts to Active Directory via Kerberos/LDAP')))
    lines.append(R(bMid(L, RR, 'Storage: NFS/CIFS mounts, iSCSI initiator, multipath-tools for SAN LUNs')))
    lines.append(R(bMid(L, RR, 'Monitoring: node_exporter → Prometheus → Grafana; rsyslog/journald → Elasticsearch')))
    lines.append(R(bMid(L, RR, 'Config mgmt: Ansible (agentless SSH) · Puppet (agent) · Chef · SaltStack (minion)')))
    lines.append(R(bBot(L, RR)))

    lines.append(txt_row())
    lines.append(txt_row('  Linux integrates with enterprise identity, storage, and observability stacks'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Identity & Auth'), bMid(L2, R2, 'Storage & Network'))))
    lines.append(R(merge(bMid(L1, R1, 'SSSD: caches AD queries'), bMid(L2, R2, 'NFS v4.1: Kerberos mounts'))))
    lines.append(R(merge(bMid(L1, R1, 'realmd: domain join tool'), bMid(L2, R2, 'iSCSI: open-iscsi initiator'))))
    lines.append(R(merge(bMid(L1, R1, 'Kerberos: kinit / klist'), bMid(L2, R2, 'multipath: dm-multipath I/O'))))
    lines.append(R(merge(bMid(L1, R1, 'PAM: sssd module for AD'), bMid(L2, R2, 'autofs: automount on demand'))))
    lines.append(R(merge(bMid(L1, R1, 'sudo rules: LDAP-sourced'), bMid(L2, R2, 'CIFS/SMB: mount.cifs shares'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · HBAs/NICs · SAN switches · NAS appliances · iDRAC · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SSSD        = System Security Services Daemon; caches LDAP/Kerberos identity lookups'))
    lines.append(txt_row('realmd      = Realm Discovery daemon; simplifies domain join with a single command'))
    lines.append(txt_row('Kerberos    = Ticket-based auth protocol; kinit obtains TGT from AD KDC'))
    lines.append(txt_row('NFS v4.1    = Network File System v4.1; adds pNFS parallel I/O and session trunking'))
    lines.append(txt_row('iSCSI       = IP-based SCSI protocol; carries SCSI commands over TCP/IP networks'))
    lines.append(txt_row('dm-multipath= Device Mapper multipath; aggregates multiple HBA paths to one block device'))
    lines.append(txt_row('autofs      = Kernel automounter; mounts NFS/CIFS shares on access and unmounts on idle'))
    lines.append(txt_row('node_exporter= Prometheus agent; exposes host metrics (CPU, mem, disk, net) on port 9100'))
    lines.append(txt_row('Ansible     = Agentless automation over SSH; uses YAML playbooks for idempotent config'))
    lines.append(txt_row('Puppet      = Agent-based config mgmt; enforces declared resource state on each run'))
    lines.append(txt_row('rsyslog     = Reliable syslog daemon; forwards structured log messages over UDP/TCP'))
    lines.append(txt_row('Elasticsearch= Distributed search and analytics engine for log aggregation at scale'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-arch-design', 'docs/compute/linux/architecture/design-standards/index.md',
            'Linux Architecture — Design Standards: naming, partitioning, hardening baseline')
def linux_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Design Standards'))
    lines.append(txt_row())

    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Build & Naming Standards')))
    lines.append(R(bMid(L, RR, 'Hostname convention: role-dc-seq (e.g. web-lon-001); FQDN in /etc/hosts + DNS')))
    lines.append(R(bMid(L, RR, 'Approved distros: RHEL 8/9 · Rocky 8/9 · Ubuntu 22.04 LTS · Debian 12')))
    lines.append(R(bMid(L, RR, 'Kernel: maintain vendor-supported; custom kernels require CAB approval')))
    lines.append(R(bMid(L, RR, 'Time: chronyd synced to internal NTP; timezone UTC for all server builds')))
    lines.append(R(bBot(L, RR)))

    lines.append(txt_row())
    lines.append(txt_row('  Consistent build standards reduce configuration drift and simplify troubleshooting'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Partition Layout'), bMid(L2, R2, 'Hardening Baseline'))))
    lines.append(R(merge(bMid(L1, R1, '/boot: 1 GB xfs (separate)'), bMid(L2, R2, 'SSH: PasswordAuth no; root no'))))
    lines.append(R(merge(bMid(L1, R1, '/: 20 GB xfs on LVM'), bMid(L2, R2, 'SELinux: enforcing mode'))))
    lines.append(R(merge(bMid(L1, R1, '/var: 20 GB (log growth)'), bMid(L2, R2, 'firewalld: default-deny zones'))))
    lines.append(R(merge(bMid(L1, R1, '/var/log: separate 10 GB'), bMid(L2, R2, 'auditd: CIS rule set enabled'))))
    lines.append(R(merge(bMid(L1, R1, '/home: separate 10 GB'), bMid(L2, R2, 'AIDE: file integrity baseline'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · SSD/NVMe boot · LVM volumes · iDRAC BMC · NIC · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('LVM         = Logical Volume Manager; enables flexible resizing of volumes without repartition'))
    lines.append(txt_row('SELinux     = Security-Enhanced Linux; MAC enforcement with targeted/enforcing policy'))
    lines.append(txt_row('firewalld   = Dynamic firewall daemon using zones and nftables rules under the hood'))
    lines.append(txt_row('auditd      = Linux audit daemon; records syscall events for CIS/STIG compliance'))
    lines.append(txt_row('AIDE        = Advanced Intrusion Detection Environment; detects file system changes'))
    lines.append(txt_row('chronyd     = NTP client/server daemon; preferred over ntpd on RHEL/Rocky/Ubuntu'))
    lines.append(txt_row('FQDN        = Fully Qualified Domain Name; hostname + domain (host.example.com)'))
    lines.append(txt_row('CIS         = Center for Internet Security; publishes hardening benchmarks for Linux'))
    lines.append(txt_row('STIG        = Security Technical Implementation Guide; DoD hardening specification'))
    lines.append(txt_row('CAB         = Change Advisory Board; reviews and approves infrastructure changes'))
    lines.append(txt_row('UTC         = Coordinated Universal Time; used on servers to avoid DST ambiguity'))
    lines.append(txt_row('XFS         = High-performance journaling filesystem; default on RHEL/Rocky Linux'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-ops', 'docs/compute/linux/operations/index.md',
            'Linux Operations — patching, backup, monitoring, automation, health')
def linux_ops():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Day-to-Day Linux Operations')))
    lines.append(R(bMid(L, RR, 'Patching: dnf update / apt upgrade → test → prod ring; kernel updates need reboot')))
    lines.append(R(bMid(L, RR, 'Monitoring: node_exporter metrics · journalctl · top/htop/sar · iostat · vmstat')))
    lines.append(R(bMid(L, RR, 'Automation: Ansible playbooks, Bash cron jobs, systemd timers for recurring tasks')))
    lines.append(R(bMid(L, RR, 'Access: SSH key auth; sudo with NOPASSWD for automation; MFA for privileged users')))
    lines.append(R(bBot(L, RR)))

    lines.append(txt_row())
    lines.append(txt_row('  Operations tasks span patching, monitoring, automation, and user/service management'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Service Management'), bMid(L2, R2, 'Package & Updates'))))
    lines.append(R(merge(bMid(L1, R1, 'systemctl start/stop/restart'), bMid(L2, R2, 'dnf update --security'))))
    lines.append(R(merge(bMid(L1, R1, 'systemctl enable/disable'), bMid(L2, R2, 'apt-get dist-upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'journalctl -u svc --since'), bMid(L2, R2, 'rpm -qa / dpkg -l: audit'))))
    lines.append(R(merge(bMid(L1, R1, 'systemctl daemon-reload'), bMid(L2, R2, 'dnf history / apt log'))))
    lines.append(R(merge(bMid(L1, R1, 'systemd-analyze blame: slow'), bMid(L2, R2, 'needs-restarting check'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · SSD/NVMe · NIC · iDRAC/iLO BMC · UPS · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('dnf         = Dandified YUM; package manager for RHEL/Rocky/Fedora; supports modules'))
    lines.append(txt_row('apt         = Advanced Package Tool; package manager for Debian/Ubuntu systems'))
    lines.append(txt_row('systemctl   = CLI for systemd; start/stop/enable/disable/status service units'))
    lines.append(txt_row('journalctl  = Query systemd journal; filter by unit, time, priority, or boot'))
    lines.append(txt_row('node_exporter= Prometheus exporter; exposes Linux host metrics on TCP port 9100'))
    lines.append(txt_row('sar         = System Activity Reporter; collects CPU, memory, I/O stats over time'))
    lines.append(txt_row('iostat      = I/O statistics; shows disk utilisation, throughput, and await times'))
    lines.append(txt_row('vmstat      = Virtual memory stats; reports procs, memory, swap, I/O, CPU'))
    lines.append(txt_row('needs-restarting= dnf plugin that identifies services needing restart after update'))
    lines.append(txt_row('Ansible     = Agentless SSH automation; idempotent YAML playbooks for Linux config'))
    lines.append(txt_row('cron        = Classic job scheduler; reads /etc/crontab and user crontabs'))
    lines.append(txt_row('systemd timer= Modern cron replacement; accurate scheduling with dependency support'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-ops-procedures', 'docs/compute/linux/operations/procedures/index.md',
            'Linux Operations — Procedures: standard runbooks for common admin tasks')
def linux_ops_procedures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux Operations — Procedures'))
    lines.append(txt_row())

    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Standard Operating Procedures')))
    lines.append(R(bMid(L, RR, 'User provisioning: adduser → set password → add to groups → configure sudo')))
    lines.append(R(bMid(L, RR, 'Disk expansion: pvcreate → vgextend → lvextend → xfs_growfs / resize2fs')))
    lines.append(R(bMid(L, RR, 'Service deployment: create unit file → systemctl enable → start → validate')))
    lines.append(R(bMid(L, RR, 'Kernel update: dnf update kernel → grub2-set-default → reboot → verify uname -r')))
    lines.append(R(bBot(L, RR)))

    lines.append(txt_row())
    lines.append(txt_row('  Documented procedures reduce errors and ensure consistent repeatable outcomes'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network & Firewall'), bMid(L2, R2, 'Certificate & SSH'))))
    lines.append(R(merge(bMid(L1, R1, 'ip addr add: add IP address'), bMid(L2, R2, 'ssh-keygen -t ed25519'))))
    lines.append(R(merge(bMid(L1, R1, 'nmcli: NetworkManager config'), bMid(L2, R2, 'ssh-copy-id to target host'))))
    lines.append(R(merge(bMid(L1, R1, 'firewall-cmd --permanent add'), bMid(L2, R2, 'openssl req: generate CSR'))))
    lines.append(R(merge(bMid(L1, R1, 'ss -tlnp: verify open ports'), bMid(L2, R2, 'certbot: ACME cert renewal'))))
    lines.append(R(merge(bMid(L1, R1, 'ip route: add/del routes'), bMid(L2, R2, 'known_hosts maintenance'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · LVM volumes · NIC · iDRAC/iLO BMC · NTP · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('pvcreate    = Initialise a block device as an LVM Physical Volume'))
    lines.append(txt_row('vgextend    = Add a new Physical Volume to an existing Volume Group'))
    lines.append(txt_row('lvextend    = Grow a Logical Volume; must be followed by filesystem resize'))
    lines.append(txt_row('xfs_growfs  = Online-resize an XFS filesystem to fill available LV space'))
    lines.append(txt_row('resize2fs   = Online or offline-resize an ext4 filesystem after lvextend'))
    lines.append(txt_row('grub2-set-default= Select which kernel entry GRUB2 boots by default'))
    lines.append(txt_row('nmcli       = NetworkManager CLI; manages connections, devices, and profiles'))
    lines.append(txt_row('firewall-cmd= CLI for firewalld; adds/removes services, ports, and rich rules'))
    lines.append(txt_row('ss          = Socket statistics; replaces netstat for viewing open ports/connections'))
    lines.append(txt_row('ssh-keygen  = Generates RSA/Ed25519 key pairs for SSH public-key authentication'))
    lines.append(txt_row('openssl req = Generates a Certificate Signing Request from a private key'))
    lines.append(txt_row("certbot     = ACME client for Let's Encrypt; automates TLS cert issuance and renewal"))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-ops-backup', 'docs/compute/linux/operations/backup-restore/index.md',
            'Linux Operations — Backup & Restore: rsync, tar, snapshot, Bacula/Veeam')
def linux_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Backup & Restore'))
    lines.append(txt_row())

    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Backup Strategy')))
    lines.append(R(bMid(L, RR, '3-2-1 rule: 3 copies · 2 different media · 1 offsite / cloud (S3/Glacier)')))
    lines.append(R(bMid(L, RR, 'Full weekly + incremental daily; retention: 30 days local, 1 year tape/object')))
    lines.append(R(bMid(L, RR, 'LVM snapshots: instant consistent point-in-time for live volumes before changes')))
    lines.append(R(bMid(L, RR, 'Test restores: monthly drill to verify backup integrity and RTO compliance')))
    lines.append(R(bBot(L, RR)))

    lines.append(txt_row())
    lines.append(txt_row('  Backup strategy must balance recovery time objective with storage cost'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'File-Level Tools'), bMid(L2, R2, 'Enterprise Backup'))))
    lines.append(R(merge(bMid(L1, R1, 'rsync -avz: incremental sync'), bMid(L2, R2, 'Bacula: client/director/SD'))))
    lines.append(R(merge(bMid(L1, R1, 'tar czf: archive + compress'), bMid(L2, R2, 'Veeam Agent for Linux'))))
    lines.append(R(merge(bMid(L1, R1, 'dd if=/dev/sda: disk image'), bMid(L2, R2, 'Amanda: open-source backup'))))
    lines.append(R(merge(bMid(L1, R1, 'duplicati: encrypted backup'), bMid(L2, R2, 'Commvault: enterprise CBM'))))
    lines.append(R(merge(bMid(L1, R1, 'restic: dedup + encryption'), bMid(L2, R2, 'NBU: NetBackup agent mode'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · NAS/SAN storage · tape library · S3 object store · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('3-2-1 rule  = 3 copies of data on 2 different media with 1 copy offsite'))
    lines.append(txt_row('RTO         = Recovery Time Objective; max acceptable time to restore a service'))
    lines.append(txt_row('RPO         = Recovery Point Objective; max acceptable data loss measured in time'))
    lines.append(txt_row('LVM snapshot= CoW point-in-time copy of an LV; consistent backup without stopping service'))
    lines.append(txt_row('rsync       = Remote sync tool; copies only changed blocks; supports SSH transport'))
    lines.append(txt_row('tar         = Tape ARchive; bundles files into a single stream; combined with gzip/bzip2'))
    lines.append(txt_row('dd          = Data Duplicator; copies raw blocks; used for disk imaging and cloning'))
    lines.append(txt_row('restic      = Modern backup tool; content-addressable dedup with AES-256 encryption'))
    lines.append(txt_row('Bacula      = Open-source network backup; director/storage daemon/file daemon model'))
    lines.append(txt_row('Veeam Agent = Physical Linux backup agent; image-level backup to Veeam repository'))
    lines.append(txt_row('CBM         = Changed Block Monitoring; Commvault incremental-forever backup method'))
    lines.append(txt_row('NBU         = NetBackup; Veritas enterprise backup platform with agent and catalog'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-ops-health', 'docs/compute/linux/operations/health-checks/index.md',
            'Linux Operations — Health Checks: CPU, memory, disk, network, services')
def linux_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Health Checks'))
    lines.append(txt_row())

    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Health Check Framework')))
    lines.append(R(bMid(L, RR, 'Daily: check failed services · disk usage · load average · OOM log entries')))
    lines.append(R(bMid(L, RR, 'Weekly: review auditd logs · zombie processes · swap usage · NIC error counters')))
    lines.append(R(bMid(L, RR, 'Monthly: kernel errata check · LVM free extents · certificate expiry · cron jobs')))
    lines.append(R(bMid(L, RR, 'Alerting: Prometheus rules → Alertmanager → PagerDuty / Slack / email')))
    lines.append(R(bBot(L, RR)))

    lines.append(txt_row())
    lines.append(txt_row('  Proactive health checks prevent incidents; alerts surface issues before users notice'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Resource Checks'), bMid(L2, R2, 'Service & Log Checks'))))
    lines.append(R(merge(bMid(L1, R1, 'top/htop: CPU + mem live'), bMid(L2, R2, 'systemctl --failed: list'))))
    lines.append(R(merge(bMid(L1, R1, 'df -h: filesystem usage'), bMid(L2, R2, 'journalctl -p err: errors'))))
    lines.append(R(merge(bMid(L1, R1, 'free -h: RAM + swap view'), bMid(L2, R2, 'dmesg -T: kernel messages'))))
    lines.append(R(merge(bMid(L1, R1, 'iostat -x: disk await/util'), bMid(L2, R2, 'ss -s: socket summary'))))
    lines.append(R(merge(bMid(L1, R1, 'uptime: load avg 1/5/15'), bMid(L2, R2, 'ip -s link: NIC error ctrs'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · RAM DIMMs · NVMe/SSD · NIC · iDRAC/iLO IPMI · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('load average= 1/5/15-min exponential moving avg of runnable + uninterruptible tasks'))
    lines.append(txt_row('OOM         = Out-of-Memory; kernel kills processes when physical + swap RAM exhausted'))
    lines.append(txt_row('zombie      = Process in Z state; exited but parent has not called wait(); check ppid'))
    lines.append(txt_row('df          = Disk Free; reports filesystem usage by mount point; -h for human-readable'))
    lines.append(txt_row('iostat      = I/O Stat; reports device utilisation, IOPS, await (ms), and throughput'))
    lines.append(txt_row('dmesg       = Kernel ring buffer; shows hardware errors, driver messages, and panics'))
    lines.append(txt_row('Prometheus  = Time-series metrics database; scrapes exporters on configured intervals'))
    lines.append(txt_row('Alertmanager= Prometheus companion; routes alerts to receivers (PagerDuty, email, Slack)'))
    lines.append(txt_row('ss          = Socket Statistics; replacement for netstat; faster via kernel netlink'))
    lines.append(txt_row('journalctl  = Query systemd journal; use -p err for errors, -b for current boot'))
    lines.append(txt_row('LVM extents = Free PE (Physical Extents) in a VG; available for LV growth'))
    lines.append(txt_row('NIC error counters= rx_errors/tx_errors on interface; indicate cabling or driver issues'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-ops-install', 'docs/compute/linux/operations/install-upgrade/index.md',
            'Linux Operations — Install & Upgrade: OS build, kickstart, dnf, kernel')
def linux_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Install & Upgrade'))
    lines.append(txt_row())

    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'OS Installation Methods')))
    lines.append(R(bMid(L, RR, 'Manual: boot ISO → Anaconda/text installer → partition → packages → GRUB install')))
    lines.append(R(bMid(L, RR, 'Kickstart (RHEL/Rocky): ks.cfg defines locale, packages, disk, users, post-scripts')))
    lines.append(R(bMid(L, RR, 'Preseed (Debian/Ubuntu): auto-installs from netboot DHCP + TFTP PXE boot')))
    lines.append(R(bMid(L, RR, 'Cloud-init: first-boot configuration for cloud/VM images via user-data metadata')))
    lines.append(R(bBot(L, RR)))

    lines.append(txt_row())
    lines.append(txt_row('  Automated installs ensure repeatable, drift-free builds across the fleet'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Package Upgrades'), bMid(L2, R2, 'In-Place Upgrades'))))
    lines.append(R(merge(bMid(L1, R1, 'dnf update: all packages'), bMid(L2, R2, 'RHEL 8→9: leapp upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'dnf update kernel: kernel'), bMid(L2, R2, 'Ubuntu: do-release-upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'dnf history: audit trail'), bMid(L2, R2, 'leapp preupgrade: pre-check'))))
    lines.append(R(merge(bMid(L1, R1, 'apt upgrade / dist-upgrade'), bMid(L2, R2, 'ELevate: CentOS 7→8→9'))))
    lines.append(R(merge(bMid(L1, R1, 'unattended-upgrades: auto'), bMid(L2, R2, 'Snapshot before upgrade'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · PXE/TFTP network · SSD/NVMe · iDRAC virtual media · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Kickstart   = RHEL/Rocky automated install file; defines all install parameters'))
    lines.append(txt_row('Preseed     = Debian/Ubuntu automated install; answers installer questions via DHCP'))
    lines.append(txt_row('Anaconda    = Red Hat graphical/TUI installer; interprets kickstart files'))
    lines.append(txt_row('PXE         = Preboot Execution Environment; boots host over network from TFTP server'))
    lines.append(txt_row('cloud-init  = First-boot tool for cloud VMs; applies user-data from metadata service'))
    lines.append(txt_row('leapp       = Red Hat in-place upgrade tool; RHEL 7→8 and RHEL 8→9 migration'))
    lines.append(txt_row('ELevate     = AlmaLinux project tool; migrates CentOS 7/8 to RHEL-compatible distros'))
    lines.append(txt_row('do-release-upgrade= Ubuntu official in-place major version upgrade command'))
    lines.append(txt_row('unattended-upgrades= Debian/Ubuntu daemon for automatic security patch application'))
    lines.append(txt_row('GRUB2       = Boot loader installed to MBR/EFI; presents kernel selection menu'))
    lines.append(txt_row('dnf history = Audit log of all dnf transactions; allows undo of package changes'))
    lines.append(txt_row('leapp preupgrade= Pre-flight check for RHEL upgrades; reports inhibitors before proceeding'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-ops-scripts', 'docs/compute/linux/operations/scripts/index.md',
            'Linux Operations — Scripts: Bash/Python automation patterns and examples')
def linux_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Scripts & Automation'))
    lines.append(txt_row())

    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Scripting Standards')))
    lines.append(R(bMid(L, RR, 'Bash: shebang #!/bin/bash; set -euo pipefail; trap ERR for safe error handling')))
    lines.append(R(bMid(L, RR, 'Python: use venv / pipenv; type hints; logging module; argparse for CLI args')))
    lines.append(R(bMid(L, RR, 'Idempotency: scripts must be safely re-runnable without double-applying changes')))
    lines.append(R(bMid(L, RR, 'Storage: version-controlled in Git; tested in staging before production rollout')))
    lines.append(R(bBot(L, RR)))

    lines.append(txt_row())
    lines.append(txt_row('  Well-structured scripts reduce human error and enable reliable automation at scale'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Bash Patterns'), bMid(L2, R2, 'Python Patterns'))))
    lines.append(R(merge(bMid(L1, R1, 'set -euo pipefail: strict'), bMid(L2, R2, 'subprocess.run: exec cmds'))))
    lines.append(R(merge(bMid(L1, R1, 'trap cleanup EXIT ERR'), bMid(L2, R2, 'paramiko: SSH automation'))))
    lines.append(R(merge(bMid(L1, R1, 'getopts / getopt: arg parse'), bMid(L2, R2, 'fabric: remote execution'))))
    lines.append(R(merge(bMid(L1, R1, 'logger: syslog from script'), bMid(L2, R2, 'click: CLI framework'))))
    lines.append(R(merge(bMid(L1, R1, 'lockfile: prevent parallel'), bMid(L2, R2, 'jinja2: config templating'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · Git repo server · cron/systemd timers · NIC · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('set -e      = Exit immediately if any command returns non-zero exit code'))
    lines.append(txt_row('set -u      = Treat unset variables as errors; prevents typo variable bugs'))
    lines.append(txt_row('set -o pipefail= Propagate pipeline failures; catches errors in piped commands'))
    lines.append(txt_row('trap        = Register signal/event handler; useful for cleanup on EXIT or ERR'))
    lines.append(txt_row('idempotency = Property of an operation that produces same result on repeated runs'))
    lines.append(txt_row('getopts     = Bash built-in for short option parsing (-v, -f); POSIX compliant'))
    lines.append(txt_row('logger      = Shell command that writes messages to syslog / systemd journal'))
    lines.append(txt_row('paramiko    = Python SSH library; programmatic remote command execution'))
    lines.append(txt_row('fabric      = Python SSH automation; high-level remote task execution over SSH'))
    lines.append(txt_row('click       = Python CLI framework; decorators for commands, options, arguments'))
    lines.append(txt_row('jinja2      = Python template engine; used by Ansible for config file rendering'))
    lines.append(txt_row('shebang     = First line of script (#!/bin/bash); tells kernel which interpreter to use'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines
