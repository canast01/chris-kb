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


@kb_diagram('linux', 'docs/compute/linux/index.md', 'Linux Platform Overview')
def linux_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2, L3, R3 = 3, 33, 36, 66, 69, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Platform Overview'))
    lines.append(txt_row())
    lines.append(txt_row('Linux is the primary OS for compute workloads: servers, containers, and automation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Architecture'), bMid(L2, R2, 'Operations'), bMid(L3, R3, 'Security'))))
    lines.append(R(merge(bMid(L1, R1, 'Kernel + userspace'), bMid(L2, R2, 'Day-2 procedures'), bMid(L3, R3, 'Access control'))))
    lines.append(R(merge(bMid(L1, R1, 'Distro selection'), bMid(L2, R2, 'Backup & restore'), bMid(L3, R3, 'Authentication'))))
    lines.append(R(merge(bMid(L1, R1, 'Integration model'), bMid(L2, R2, 'Health checks'), bMid(L3, R3, 'Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'Design standards'), bMid(L2, R2, 'Install/upgrade'), bMid(L3, R3, 'Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'How it works'), bMid(L2, R2, 'Scripts & CLI'), bMid(L3, R3, 'Audit & compliance'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 / ARM64 servers · NIC · SAN/NAS storage · network switches · power & cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('kernel      = Core of the OS; manages CPU, memory, devices, and system calls'))
    lines.append(txt_row('userspace   = Everything outside the kernel: daemons, shells, applications'))
    lines.append(txt_row('distro      = Linux distribution: kernel + package manager + default tooling'))
    lines.append(txt_row('RHEL        = Red Hat Enterprise Linux; subscription-based, enterprise-grade OS'))
    lines.append(txt_row('Ubuntu      = Debian-based distro popular for cloud and development workloads'))
    lines.append(txt_row('systemd     = Init system and service manager; PID 1 on modern Linux distros'))
    lines.append(txt_row('cgroups     = Kernel feature to limit and isolate CPU/memory per process group'))
    lines.append(txt_row('namespace   = Kernel isolation for PID, network, mount, UTS, IPC, user scopes'))
    lines.append(txt_row('SELinux     = Mandatory access control framework built into the Linux kernel'))
    lines.append(txt_row('PAM         = Pluggable Authentication Modules; flexible auth stack for Linux'))
    lines.append(txt_row('LVM         = Logical Volume Manager; flexible disk/volume abstraction layer'))
    lines.append(txt_row('LUKS        = Linux Unified Key Setup; standard for block-device encryption'))
    lines.append(txt_row('rpm / dpkg  = Package managers for RHEL/Debian families respectively'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-ops-cli', 'docs/compute/linux/operations/cli-reference/index.md', 'Linux Operations — CLI Reference')
def linux_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('Command-line reference for day-to-day Linux administration tasks.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'System & Process'), bMid(L2, R2, 'File & Disk'))))
    lines.append(R(merge(bMid(L1, R1, 'ps aux: all processes'), bMid(L2, R2, 'ls -lah: list w/ sizes'))))
    lines.append(R(merge(bMid(L1, R1, 'top / htop: live view'), bMid(L2, R2, 'df -h: disk usage'))))
    lines.append(R(merge(bMid(L1, R1, 'kill / killall: signals'), bMid(L2, R2, 'du -sh *: dir sizes'))))
    lines.append(R(merge(bMid(L1, R1, 'systemctl status svc'), bMid(L2, R2, 'find / grep / awk'))))
    lines.append(R(merge(bMid(L1, R1, 'journalctl -u svc -f'), bMid(L2, R2, 'rsync / scp: transfer'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network'), bMid(L2, R2, 'User & Permissions'))))
    lines.append(R(merge(bMid(L1, R1, 'ip addr / ip route'), bMid(L2, R2, 'useradd / usermod'))))
    lines.append(R(merge(bMid(L1, R1, 'ss -tlnp: open ports'), bMid(L2, R2, 'passwd / chage'))))
    lines.append(R(merge(bMid(L1, R1, 'ping / traceroute'), bMid(L2, R2, 'chmod / chown'))))
    lines.append(R(merge(bMid(L1, R1, 'nmap / netstat'), bMid(L2, R2, 'sudo / visudo'))))
    lines.append(R(merge(bMid(L1, R1, 'tcpdump / curl'), bMid(L2, R2, 'id / groups / who'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · terminal emulator · SSH client · NIC · storage mounts'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('stdin/stdout= Standard input (fd 0) and output (fd 1); pipes connect them'))
    lines.append(txt_row('stderr      = Standard error (fd 2); separate from stdout for clean pipelines'))
    lines.append(txt_row('pipe |      = Passes stdout of left command as stdin of right command'))
    lines.append(txt_row('redirect >  = Sends stdout to a file; >> appends; 2>&1 merges stderr'))
    lines.append(txt_row('signal      = IPC mechanism: SIGTERM (15) graceful, SIGKILL (9) immediate'))
    lines.append(txt_row('PID         = Process ID; unique integer assigned by kernel to each process'))
    lines.append(txt_row('UID / GID   = User/Group ID; integers that control file permission checks'))
    lines.append(txt_row('sudo        = Run command as another user (default root) via policy in sudoers'))
    lines.append(txt_row('sticky bit  = Restricts file deletion in shared dir to owner only (e.g. /tmp)'))
    lines.append(txt_row('inode       = Metadata structure on disk: permissions, owner, size, timestamps'))
    lines.append(txt_row('hard link   = Directory entry pointing to same inode; same data, diff name'))
    lines.append(txt_row('symlink     = Symbolic link; pointer to another path, can cross filesystems'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-ops-common-issues', 'docs/compute/linux/operations/common-issues/index.md', 'Linux Operations — Common Issues')
def linux_ops_common_issues():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Common Operational Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Recurring Linux issues and their triage steps for quick resolution.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Performance Issues'), bMid(L2, R2, 'Storage Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'High CPU: top/htop'), bMid(L2, R2, 'Disk full: df -h / du'))))
    lines.append(R(merge(bMid(L1, R1, 'OOM: journalctl grep'), bMid(L2, R2, 'Inode exhaust: df -i'))))
    lines.append(R(merge(bMid(L1, R1, 'High LA: check iowait'), bMid(L2, R2, 'Mount fail: dmesg'))))
    lines.append(R(merge(bMid(L1, R1, 'Memory leak: pmap'), bMid(L2, R2, 'FS errors: fsck'))))
    lines.append(R(merge(bMid(L1, R1, 'Swap thrash: vmstat'), bMid(L2, R2, 'LVM resize: lvextend'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network Issues'), bMid(L2, R2, 'Service Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'No route: ip route'), bMid(L2, R2, 'Service fail: status'))))
    lines.append(R(merge(bMid(L1, R1, 'DNS fail: dig / nslookup'), bMid(L2, R2, 'Port conflict: ss -tlnp'))))
    lines.append(R(merge(bMid(L1, R1, 'MTU mismatch: ping -M'), bMid(L2, R2, 'Dep missing: rpm -q'))))
    lines.append(R(merge(bMid(L1, R1, 'FW block: iptables -L'), bMid(L2, R2, 'Config error: syslog'))))
    lines.append(R(merge(bMid(L1, R1, 'SSH timeout: tcp dumps'), bMid(L2, R2, 'SELinux deny: audit2why'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · NIC · storage arrays · network switches · out-of-band IPMI'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('OOM killer  = Kernel mechanism that kills processes when RAM is exhausted'))
    lines.append(txt_row('load avg    = 1/5/15 min averages of runnable + uninterruptible processes'))
    lines.append(txt_row('iowait      = CPU time spent waiting for I/O; high value indicates disk bottleneck'))
    lines.append(txt_row('inode       = Fixed-count metadata structures; can exhaust independently of disk space'))
    lines.append(txt_row('fsck        = Filesystem consistency check and repair tool; run on unmounted FS'))
    lines.append(txt_row('vmstat      = Reports virtual memory stats: swap, io, cpu, processes'))
    lines.append(txt_row('pmap        = Displays memory map of a process; useful for leak investigation'))
    lines.append(txt_row('audit2why   = Explains SELinux denials in human-readable form from audit.log'))
    lines.append(txt_row('MTU         = Maximum Transmission Unit; packet size limit on a network interface'))
    lines.append(txt_row('dmesg       = Kernel ring buffer log; first place to check hardware/driver errors'))
    lines.append(txt_row('lvextend    = LVM command to grow a logical volume; paired with resize2fs/xfs_growfs'))
    lines.append(txt_row('ss          = Socket statistics; replaces netstat; shows ports, states, processes'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-sec', 'docs/compute/linux/security/index.md', 'Linux Security Overview')
def linux_sec():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2, L3, R3 = 3, 33, 36, 66, 69, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Security Overview'))
    lines.append(txt_row())
    lines.append(txt_row('Linux security spans access control, authentication, encryption, and system hardening.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Access Control'), bMid(L2, R2, 'Authentication'), bMid(L3, R3, 'Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'DAC: chmod/chown'), bMid(L2, R2, 'PAM stack'), bMid(L3, R3, 'CIS Benchmarks'))))
    lines.append(R(merge(bMid(L1, R1, 'MAC: SELinux'), bMid(L2, R2, 'SSH key auth'), bMid(L3, R3, 'sysctl hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'RBAC via sudo'), bMid(L2, R2, 'MFA / OTP'), bMid(L3, R3, 'Minimal packages'))))
    lines.append(R(merge(bMid(L1, R1, 'File capabilities'), bMid(L2, R2, 'LDAP / Kerberos'), bMid(L3, R3, 'Kernel params'))))
    lines.append(R(merge(bMid(L1, R1, 'ACLs (setfacl)'), bMid(L2, R2, 'Audit logging'), bMid(L3, R3, 'auditd / AIDE'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · TPM chip · hardware HSM · NIC · locked server room'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('DAC         = Discretionary Access Control; owner sets permissions on resources'))
    lines.append(txt_row('MAC         = Mandatory Access Control; policy enforced by OS, overrides DAC'))
    lines.append(txt_row('SELinux     = Security-Enhanced Linux; label-based MAC built into the kernel'))
    lines.append(txt_row('PAM         = Pluggable Authentication Modules; auth pipeline for Linux services'))
    lines.append(txt_row('capability  = Fine-grained privilege subdivision; alternative to full root access'))
    lines.append(txt_row('ACL         = Access Control List; per-user/group permissions beyond rwx triplet'))
    lines.append(txt_row('sudo        = Delegated privilege escalation controlled by /etc/sudoers policy'))
    lines.append(txt_row('TPM         = Trusted Platform Module; hardware root of trust for key storage'))
    lines.append(txt_row('auditd      = Linux audit daemon; records system calls and security events'))
    lines.append(txt_row('AIDE        = Advanced Intrusion Detection Environment; file integrity monitor'))
    lines.append(txt_row('CIS         = Center for Internet Security; publishes OS hardening benchmarks'))
    lines.append(txt_row('sysctl      = Runtime kernel parameter tuning; /etc/sysctl.conf persists settings'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-sec-access', 'docs/compute/linux/security/access-control/index.md', 'Linux Security — Access Control')
def linux_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Access Control'))
    lines.append(txt_row())
    lines.append(txt_row('Access control on Linux: DAC permissions, SELinux MAC, ACLs, and sudo delegation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'DAC — File Permissions'), bMid(L2, R2, 'MAC — SELinux'))))
    lines.append(R(merge(bMid(L1, R1, 'rwx per owner/group/other'), bMid(L2, R2, 'Labels: user:role:type:lvl'))))
    lines.append(R(merge(bMid(L1, R1, 'chmod: numeric/symbolic'), bMid(L2, R2, 'enforcing / permissive'))))
    lines.append(R(merge(bMid(L1, R1, 'chown: owner, chgrp: grp'), bMid(L2, R2, 'restorecon: fix labels'))))
    lines.append(R(merge(bMid(L1, R1, 'umask: default new perms'), bMid(L2, R2, 'semanage: policy mgmt'))))
    lines.append(R(merge(bMid(L1, R1, 'SUID/SGID/sticky bits'), bMid(L2, R2, 'audit2allow: custom rules'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'ACLs — Extended Perms'), bMid(L2, R2, 'sudo — Privilege Delegation'))))
    lines.append(R(merge(bMid(L1, R1, 'setfacl -m u:user:rwx'), bMid(L2, R2, '/etc/sudoers + visudo'))))
    lines.append(R(merge(bMid(L1, R1, 'getfacl: view ACL'), bMid(L2, R2, 'User/Group aliases'))))
    lines.append(R(merge(bMid(L1, R1, 'mask: effective limit'), bMid(L2, R2, 'NOPASSWD: passwordless'))))
    lines.append(R(merge(bMid(L1, R1, 'default ACL on dirs'), bMid(L2, R2, 'Cmnd_Alias: cmd groups'))))
    lines.append(R(merge(bMid(L1, R1, 'inheritance rules'), bMid(L2, R2, 'sudo -l: list allowed'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · filesystem with ACL support (ext4/xfs) · LDAP/AD for group info'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('DAC         = Discretionary AC; owner discretion controls who accesses a file'))
    lines.append(txt_row('MAC         = Mandatory AC; kernel-enforced policy independent of owner wishes'))
    lines.append(txt_row('umask       = Default permission mask applied when creating new files/directories'))
    lines.append(txt_row('SUID        = Set-UID: run executable as its owner (e.g. passwd runs as root)'))
    lines.append(txt_row('SGID        = Set-GID: run as group, or inherit group on new files in directory'))
    lines.append(txt_row('sticky bit  = Only owner can delete their files in shared dir (e.g. /tmp)'))
    lines.append(txt_row('ACL mask    = Maximum effective permission for named users/groups in ACL'))
    lines.append(txt_row('setfacl     = Set file ACL entries beyond standard rwx triplet'))
    lines.append(txt_row('SELinux ctx = Security context: user:role:type:sensitivity label on every object'))
    lines.append(txt_row('restorecon  = Restore default SELinux file context from policy database'))
    lines.append(txt_row('audit2allow = Generate SELinux allow rule from audit denial log entries'))
    lines.append(txt_row('visudo      = Safe editor for sudoers; validates syntax before saving'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-sec-auth', 'docs/compute/linux/security/authentication/index.md', 'Linux Security — Authentication')
def linux_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('Linux authentication: PAM stack, SSH keys, MFA, LDAP/Kerberos, and audit logging.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'PAM Stack'), bMid(L2, R2, 'SSH Authentication'))))
    lines.append(R(merge(bMid(L1, R1, '/etc/pam.d/* config'), bMid(L2, R2, 'Public key auth preferred'))))
    lines.append(R(merge(bMid(L1, R1, 'auth / account modules'), bMid(L2, R2, '~/.ssh/authorized_keys'))))
    lines.append(R(merge(bMid(L1, R1, 'session / password'), bMid(L2, R2, 'ed25519 / RSA-4096'))))
    lines.append(R(merge(bMid(L1, R1, 'pam_faillock: lockout'), bMid(L2, R2, 'sshd_config hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'pam_unix / pam_ldap'), bMid(L2, R2, 'Certificate authority SSH'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Directory Services'), bMid(L2, R2, 'MFA & Audit'))))
    lines.append(R(merge(bMid(L1, R1, 'SSSD: AD/LDAP bridge'), bMid(L2, R2, 'pam_google_auth / TOTP'))))
    lines.append(R(merge(bMid(L1, R1, 'Kerberos: ticket auth'), bMid(L2, R2, 'pam_duo: Duo MFA'))))
    lines.append(R(merge(bMid(L1, R1, 'realmd: AD join tool'), bMid(L2, R2, 'auditd: login events'))))
    lines.append(R(merge(bMid(L1, R1, 'krb5.conf: realm cfg'), bMid(L2, R2, 'last / lastlog / who'))))
    lines.append(R(merge(bMid(L1, R1, 'klist: view tickets'), bMid(L2, R2, '/var/log/auth.log'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · AD/LDAP servers · NTP (Kerberos req) · NIC · HSM for CA keys'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('PAM         = Pluggable Authentication Modules; modular auth framework for Linux'))
    lines.append(txt_row('SSSD        = System Security Services Daemon; caches AD/LDAP credentials locally'))
    lines.append(txt_row('Kerberos    = Network auth protocol using encrypted tickets; AD uses it natively'))
    lines.append(txt_row('TGT         = Ticket Granting Ticket; initial Kerberos ticket from KDC (AS)'))
    lines.append(txt_row('realm       = Kerberos/AD domain identifier (e.g. CORP.EXAMPLE.COM)'))
    lines.append(txt_row('realmd      = Discovers and joins AD/Kerberos realms; configures SSSD + krb5'))
    lines.append(txt_row('pam_faillock= Locks account after N failed auth attempts; thwarts brute force'))
    lines.append(txt_row('TOTP        = Time-based One-Time Password (RFC 6238); 30-second rotating code'))
    lines.append(txt_row('authorized_keys= File listing public keys allowed to log in via SSH'))
    lines.append(txt_row('ed25519     = Modern elliptic-curve SSH key type; faster and more secure than RSA'))
    lines.append(txt_row('Certificate = SSH CA-signed cert; enables expiring, revocable SSH credentials'))
    lines.append(txt_row('auditd      = Linux audit daemon; records logins, sudo, file access as events'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-sec-enc', 'docs/compute/linux/security/encryption/index.md', 'Linux Security — Encryption')
def linux_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('Encryption at rest (LUKS) and in transit (TLS/SSH) for Linux systems.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Disk Encryption — LUKS'), bMid(L2, R2, 'Transport — TLS / SSH'))))
    lines.append(R(merge(bMid(L1, R1, 'cryptsetup luksFormat'), bMid(L2, R2, 'OpenSSL: cert mgmt'))))
    lines.append(R(merge(bMid(L1, R1, 'dm-crypt: kernel layer'), bMid(L2, R2, 'TLS 1.2/1.3 only'))))
    lines.append(R(merge(bMid(L1, R1, '/etc/crypttab: auto open'), bMid(L2, R2, 'SSH: ed25519 preferred'))))
    lines.append(R(merge(bMid(L1, R1, 'TPM2: key seal/unseal'), bMid(L2, R2, 'stunnel: TLS wrapper'))))
    lines.append(R(merge(bMid(L1, R1, 'Clevis + Tang: network'), bMid(L2, R2, 'WireGuard: modern VPN'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'File / Secret Encryption'), bMid(L2, R2, 'Key Management'))))
    lines.append(R(merge(bMid(L1, R1, 'GPG: file encryption'), bMid(L2, R2, 'PKCS#11: HSM interface'))))
    lines.append(R(merge(bMid(L1, R1, 'age: modern enc tool'), bMid(L2, R2, 'TPM2-tools: seal keys'))))
    lines.append(R(merge(bMid(L1, R1, 'ansible-vault encrypt'), bMid(L2, R2, 'HashiCorp Vault agent'))))
    lines.append(R(merge(bMid(L1, R1, '/dev/urandom: entropy'), bMid(L2, R2, 'Clevis: auto-unseal'))))
    lines.append(R(merge(bMid(L1, R1, 'shred: secure delete'), bMid(L2, R2, 'Tang: network key srv'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · TPM 2.0 chip · hardware HSM · encrypted SSDs · NIC'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('LUKS        = Linux Unified Key Setup; block device encryption standard'))
    lines.append(txt_row('dm-crypt    = Kernel device-mapper target providing transparent encryption'))
    lines.append(txt_row('cryptsetup  = CLI for managing LUKS containers and dm-crypt mappings'))
    lines.append(txt_row('TPM         = Trusted Platform Module; stores keys in hardware, survives reboot'))
    lines.append(txt_row('Clevis      = Automated LUKS unlock framework supporting TPM and Tang backends'))
    lines.append(txt_row('Tang        = Network-bound disk encryption server; key released only on LAN'))
    lines.append(txt_row('GPG         = GNU Privacy Guard; OpenPGP for file/email encryption and signing'))
    lines.append(txt_row('age         = Modern file encryption tool; simpler than GPG, X25519/SSH keys'))
    lines.append(txt_row('TLS         = Transport Layer Security; cryptographic protocol for secure channels'))
    lines.append(txt_row('WireGuard   = Modern VPN protocol; kernel module, fast, simple configuration'))
    lines.append(txt_row('HSM         = Hardware Security Module; tamper-resistant key storage device'))
    lines.append(txt_row('PKCS#11     = Standard API for interacting with HSMs and smart cards'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-sec-hard', 'docs/compute/linux/security/hardening/index.md', 'Linux Security — Hardening')
def linux_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — System Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('CIS benchmark-aligned Linux hardening: kernel, network, packages, and auditing.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Kernel Hardening'), bMid(L2, R2, 'Network Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'sysctl: disable IPv6 fwd'), bMid(L2, R2, 'firewalld / nftables'))))
    lines.append(R(merge(bMid(L1, R1, 'kernel.dmesg_restrict=1'), bMid(L2, R2, 'deny all inbound default'))))
    lines.append(R(merge(bMid(L1, R1, 'fs.suid_dumpable=0'), bMid(L2, R2, 'TCP SYN cookies on'))))
    lines.append(R(merge(bMid(L1, R1, 'kernel.yama.ptrace=1'), bMid(L2, R2, 'RP filter enabled'))))
    lines.append(R(merge(bMid(L1, R1, 'randomize_va_space=2'), bMid(L2, R2, 'No ICMP redirect accept'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Package & Service'), bMid(L2, R2, 'Audit & Monitoring'))))
    lines.append(R(merge(bMid(L1, R1, 'Remove unused packages'), bMid(L2, R2, 'auditd: syscall rules'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable unused services'), bMid(L2, R2, 'AIDE: integrity checks'))))
    lines.append(R(merge(bMid(L1, R1, 'Auto-patch: dnf-automatic'), bMid(L2, R2, 'logwatch / journald'))))
    lines.append(R(merge(bMid(L1, R1, 'RPM GPG verify always'), bMid(L2, R2, 'oscap: CIS scan'))))
    lines.append(R(merge(bMid(L1, R1, 'noexec on /tmp /var/tmp'), bMid(L2, R2, 'fail2ban: brute force'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · hardware firewall · TPM 2.0 · NIC with port security · physical locks'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CIS Benchmark= Consensus security configuration standard for OS and apps'))
    lines.append(txt_row('ASLR        = Address Space Layout Randomization; randomize_va_space=2'))
    lines.append(txt_row('sysctl      = Kernel runtime parameters in /proc/sys; persisted via sysctl.conf'))
    lines.append(txt_row('AIDE        = Advanced Intrusion Detection Environment; compares file hashes'))
    lines.append(txt_row('auditd      = Records security-relevant syscalls; stores in /var/log/audit/'))
    lines.append(txt_row('oscap       = OpenSCAP tool; applies and reports on SCAP/CIS benchmarks'))
    lines.append(txt_row('noexec      = Mount option preventing execution of binaries from that filesystem'))
    lines.append(txt_row('nftables    = Modern Linux firewall framework replacing iptables'))
    lines.append(txt_row('fail2ban    = Bans IPs after repeated failed auth attempts via iptables/nftables'))
    lines.append(txt_row('ptrace      = Kernel syscall for process tracing; restrict to prevent privilege esc'))
    lines.append(txt_row('RP filter   = Reverse path filter; drops packets with spoofed source addresses'))
    lines.append(txt_row('SYN cookie  = Defense against SYN flood DoS by encoding state in SYN-ACK'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-trouble', 'docs/compute/linux/troubleshooting/index.md', 'Linux Troubleshooting Overview')
def linux_trouble():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2, L3, R3 = 3, 33, 36, 66, 69, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Troubleshooting Overview'))
    lines.append(txt_row())
    lines.append(txt_row('Structured approach to Linux problem diagnosis: common issues, diagnostics, escalation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Common Issues'), bMid(L2, R2, 'Diagnostics'), bMid(L3, R3, 'Escalation'))))
    lines.append(R(merge(bMid(L1, R1, 'Perf degradation'), bMid(L2, R2, 'dmesg / journalctl'), bMid(L3, R3, 'Vendor support'))))
    lines.append(R(merge(bMid(L1, R1, 'Network failures'), bMid(L2, R2, 'strace / ltrace'), bMid(L3, R3, 'Escalation path'))))
    lines.append(R(merge(bMid(L1, R1, 'Disk / FS errors'), bMid(L2, R2, 'perf / bpftrace'), bMid(L3, R3, 'Runbook links'))))
    lines.append(R(merge(bMid(L1, R1, 'Service crashes'), bMid(L2, R2, 'gdb / coredump'), bMid(L3, R3, 'P1 contacts'))))
    lines.append(R(merge(bMid(L1, R1, 'Auth failures'), bMid(L2, R2, 'tcpdump / ss'), bMid(L3, R3, 'RCA template'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · IPMI/iDRAC (OOB access) · console cable · NIC · storage'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('strace      = Traces system calls made by a process; essential for debugging'))
    lines.append(txt_row('ltrace      = Traces library calls; complements strace for userspace debugging'))
    lines.append(txt_row('perf        = Linux performance analysis tool; CPU sampling and tracing'))
    lines.append(txt_row('bpftrace    = eBPF-based tracing tool; powerful kernel and app observability'))
    lines.append(txt_row('gdb         = GNU debugger; inspects running processes and core dumps'))
    lines.append(txt_row('coredump    = Memory snapshot of crashed process; analysed with gdb'))
    lines.append(txt_row('dmesg       = Kernel ring buffer; first check for hardware/driver errors'))
    lines.append(txt_row('journalctl  = Query systemd journal; -u for unit, -b for boot, -f follow'))
    lines.append(txt_row('IPMI        = Out-of-band management; console access even when OS is down'))
    lines.append(txt_row('RCA         = Root Cause Analysis; post-incident document explaining failure'))
    lines.append(txt_row('tcpdump     = Packet capture tool; diagnose network-level communication issues'))
    lines.append(txt_row('OOB         = Out-of-Band; management network separate from production traffic'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-trouble-common', 'docs/compute/linux/troubleshooting/common-issues/index.md', 'Linux Troubleshooting — Common Issues')
def linux_trouble_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Troubleshooting Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Quick-reference for the most frequently encountered Linux operational problems.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Boot & Startup Issues'), bMid(L2, R2, 'Performance Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'grub rescue: grub.cfg'), bMid(L2, R2, 'CPU spike: top -o %CPU'))))
    lines.append(R(merge(bMid(L1, R1, 'initramfs: dracut --force'), bMid(L2, R2, 'RAM low: free -h'))))
    lines.append(R(merge(bMid(L1, R1, 'fstab error: nofail opt'), bMid(L2, R2, 'Disk wait: iostat -x'))))
    lines.append(R(merge(bMid(L1, R1, 'SELinux relabel needed'), bMid(L2, R2, 'Network slow: iperf3'))))
    lines.append(R(merge(bMid(L1, R1, 'Kernel panic: dmesg'), bMid(L2, R2, 'Zombie procs: pstree'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Auth & Access Issues'), bMid(L2, R2, 'Disk & FS Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'SSH deny: auth.log'), bMid(L2, R2, 'ENOSPC: df -h / df -i'))))
    lines.append(R(merge(bMid(L1, R1, 'sudo fail: sudoers -l'), bMid(L2, R2, 'FS ro: remount rw'))))
    lines.append(R(merge(bMid(L1, R1, 'SSSD down: sssd status'), bMid(L2, R2, 'fsck -y: auto repair'))))
    lines.append(R(merge(bMid(L1, R1, 'Lock: faillock --reset'), bMid(L2, R2, 'LVM snap for backup'))))
    lines.append(R(merge(bMid(L1, R1, 'PAM deny: /var/log/auth'), bMid(L2, R2, 'xfs_repair: XFS fix'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · BIOS/UEFI · RAID controller · NIC · IPMI for OOB console'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('initramfs   = Temporary root FS loaded by kernel at boot before real root'))
    lines.append(txt_row('dracut      = Tool to build initramfs images on RHEL/Fedora systems'))
    lines.append(txt_row('GRUB        = GRand Unified Bootloader; chainloads kernel at system start'))
    lines.append(txt_row('nofail      = fstab option; system boots even if that mount point is unavailable'))
    lines.append(txt_row('kernel panic= Unrecoverable kernel error; system halts/reboots automatically'))
    lines.append(txt_row('ENOSPC      = Error No Space; filesystem has no free blocks or inodes'))
    lines.append(txt_row('zombie proc = Process that has exited but parent has not yet waited on it'))
    lines.append(txt_row('iostat      = Reports CPU and I/O stats; -x for extended disk utilisation'))
    lines.append(txt_row('iperf3      = Network throughput test tool; client/server model'))
    lines.append(txt_row('faillock    = PAM tool to show and reset account lockout records'))
    lines.append(txt_row('xfs_repair  = Offline XFS filesystem repair utility'))
    lines.append(txt_row('fsck        = Filesystem check and repair; must be run on unmounted filesystem'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-trouble-diag', 'docs/compute/linux/troubleshooting/diagnostics/index.md', 'Linux Troubleshooting — Diagnostics')
def linux_trouble_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('Diagnostic tools and techniques for deep Linux system investigation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Log Analysis'), bMid(L2, R2, 'Process Tracing'))))
    lines.append(R(merge(bMid(L1, R1, 'journalctl -b -p err'), bMid(L2, R2, 'strace -p PID: syscalls'))))
    lines.append(R(merge(bMid(L1, R1, 'dmesg -T: timestamped'), bMid(L2, R2, 'ltrace: lib calls'))))
    lines.append(R(merge(bMid(L1, R1, '/var/log/messages syslog'), bMid(L2, R2, 'gdb attach PID'))))
    lines.append(R(merge(bMid(L1, R1, 'ausearch: audit events'), bMid(L2, R2, 'lsof -p PID: open files'))))
    lines.append(R(merge(bMid(L1, R1, 'grep -r /var/log/'), bMid(L2, R2, '/proc/PID/: process info'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Performance Profiling'), bMid(L2, R2, 'Network Diagnostics'))))
    lines.append(R(merge(bMid(L1, R1, 'perf stat ./cmd'), bMid(L2, R2, 'tcpdump -i eth0 port 80'))))
    lines.append(R(merge(bMid(L1, R1, 'perf top: live flamegraph'), bMid(L2, R2, 'ss -anp: all sockets'))))
    lines.append(R(merge(bMid(L1, R1, 'bpftrace: eBPF scripts'), bMid(L2, R2, 'nmap -sV: service scan'))))
    lines.append(R(merge(bMid(L1, R1, 'vmstat 1: mem/io/cpu'), bMid(L2, R2, 'mtr: traceroute+ping'))))
    lines.append(R(merge(bMid(L1, R1, 'sar -u 1 10: CPU hist'), bMid(L2, R2, 'wireshark: packet GUI'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · NIC · SAN storage · out-of-band IPMI · monitoring endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('strace      = System call tracer; shows every kernel interaction of a process'))
    lines.append(txt_row('ltrace      = Library call tracer; intercepts dynamic library function calls'))
    lines.append(txt_row('perf        = Linux profiler; samples CPU, traces events, generates flamegraphs'))
    lines.append(txt_row('bpftrace    = High-level eBPF tracing; scripts kernel and application events'))
    lines.append(txt_row('eBPF        = Extended Berkeley Packet Filter; in-kernel sandboxed programs'))
    lines.append(txt_row('lsof        = List open files; shows files, sockets, pipes held by processes'))
    lines.append(txt_row('ausearch    = Searches auditd log for specific events by user, key, syscall'))
    lines.append(txt_row('sar         = System Activity Reporter; collects and reports performance data'))
    lines.append(txt_row('vmstat      = Virtual memory statistics; shows proc, swap, io, cpu per interval'))
    lines.append(txt_row('mtr         = Combines traceroute and ping; shows per-hop latency and loss'))
    lines.append(txt_row('tcpdump     = CLI packet capture; filter by port, host, protocol'))
    lines.append(txt_row('/proc/PID   = Virtual filesystem exposing process state: maps, fd, stat, cmdline'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('linux-trouble-esc', 'docs/compute/linux/troubleshooting/escalation/index.md', 'Linux Troubleshooting — Escalation')
def linux_trouble_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Linux — Escalation Procedures'))
    lines.append(txt_row())
    lines.append(txt_row('Escalation paths, contacts, and runbooks when Linux issues exceed local resolution.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Escalation Triggers'), bMid(L2, R2, 'Escalation Path'))))
    lines.append(R(merge(bMid(L1, R1, 'Production outage >15m'), bMid(L2, R2, 'L1: ops on-call'))))
    lines.append(R(merge(bMid(L1, R1, 'Data loss risk detected'), bMid(L2, R2, 'L2: senior Linux admin'))))
    lines.append(R(merge(bMid(L1, R1, 'Kernel panic recurring'), bMid(L2, R2, 'L3: vendor support'))))
    lines.append(R(merge(bMid(L1, R1, 'Security breach suspected'), bMid(L2, R2, 'CISO + legal notify'))))
    lines.append(R(merge(bMid(L1, R1, 'Hardware fault confirmed'), bMid(L2, R2, 'DC ops + hardware vendor'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Information to Gather'), bMid(L2, R2, 'Post-Escalation'))))
    lines.append(R(merge(bMid(L1, R1, 'hostname / kernel ver'), bMid(L2, R2, 'Create RCA document'))))
    lines.append(R(merge(bMid(L1, R1, 'dmesg + journalctl dump'), bMid(L2, R2, 'Update runbook'))))
    lines.append(R(merge(bMid(L1, R1, 'sar / vmstat output'), bMid(L2, R2, 'File bug with vendor'))))
    lines.append(R(merge(bMid(L1, R1, 'Recent change log'), bMid(L2, R2, 'Apply preventive fix'))))
    lines.append(R(merge(bMid(L1, R1, 'Network topology map'), bMid(L2, R2, 'Schedule post-mortem'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · IPMI/iDRAC OOB · phone bridge · monitoring dashboards'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('escalation  = Formal handover of an issue to a higher-tier resolver or vendor'))
    lines.append(txt_row('RCA         = Root Cause Analysis; document explaining what failed and why'))
    lines.append(txt_row('post-mortem = Blameless review meeting after incident; produces action items'))
    lines.append(txt_row('runbook     = Step-by-step procedure document for known operational tasks'))
    lines.append(txt_row('P1/P2       = Priority classification; P1 = critical production impact'))
    lines.append(txt_row('on-call     = Rotation of engineers responsible for responding outside hours'))
    lines.append(txt_row('CISO        = Chief Information Security Officer; leads security escalations'))
    lines.append(txt_row('OOB         = Out-of-Band management; IPMI/iDRAC for access when OS is down'))
    lines.append(txt_row('change log  = Record of recent system changes; critical for incident correlation'))
    lines.append(txt_row('SLA         = Service Level Agreement; defines uptime and response targets'))
    lines.append(txt_row('MTTR        = Mean Time To Repair; average time to restore service after failure'))
    lines.append(txt_row('war room    = Bridge call with all stakeholders during major incident'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-arch', 'docs/compute/windows-server/architecture/index.md', 'Windows Server Architecture')
def _windows_arch():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Architecture'))
    lines.append(txt_row())
    lines.append(txt_row('Windows Server architecture: kernel, services, Active Directory, and Hyper-V integration.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'OS Architecture'), bMid(L2, R2, 'Active Directory'))))
    lines.append(R(merge(bMid(L1, R1, 'NT kernel: HAL + kernel mode'), bMid(L2, R2, 'Forest → Domain → OU tree'))))
    lines.append(R(merge(bMid(L1, R1, 'Win32 subsystem: user mode'), bMid(L2, R2, 'DC: LDAP + Kerberos + DNS'))))
    lines.append(R(merge(bMid(L1, R1, 'Services: SCM-managed'), bMid(L2, R2, 'SYSVOL: GPO + script replication'))))
    lines.append(R(merge(bMid(L1, R1, 'Registry: config store'), bMid(L2, R2, 'Trust: cross-domain auth'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('  OS layer provides platform; AD provides identity; Hyper-V provides virtualisation'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Hyper-V Architecture'), bMid(L2, R2, 'Networking'))))
    lines.append(R(merge(bMid(L1, R1, 'Parent partition: management'), bMid(L2, R2, 'Virtual switch: external/int/priv'))))
    lines.append(R(merge(bMid(L1, R1, 'Child partition: VM guest'), bMid(L2, R2, 'NIC teaming: LBFO / SET'))))
    lines.append(R(merge(bMid(L1, R1, 'VMBus: hypercall channel'), bMid(L2, R2, 'SMB Direct: RDMA file access'))))
    lines.append(R(merge(bMid(L1, R1, 'Synthetic NIC / SCSI'), bMid(L2, R2, 'Windows Firewall + GPO rules'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical server · CPU virtualization extensions · NIC · storage SAN/NAS'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('HAL          = Hardware Abstraction Layer; isolates kernel from hardware'))
    lines.append(txt_row('SCM          = Service Control Manager; manages Windows service lifecycle'))
    lines.append(txt_row('Registry     = hierarchical configuration database; HKLM and HKCU hives'))
    lines.append(txt_row('SYSVOL       = shared folder replicated to all DCs; holds GPOs and scripts'))
    lines.append(txt_row('Trust        = cross-domain auth relationship; one-way or two-way'))
    lines.append(txt_row('VMBus        = high-speed communication channel between parent and child partitions'))
    lines.append(txt_row('Synthetic NIC= Hyper-V virtual NIC using VMBus; requires integration services'))
    lines.append(txt_row('NIC teaming  = LBFO or Switch Embedded Teaming (SET); redundancy + bandwidth'))
    lines.append(txt_row('SMB Direct   = SMB over RDMA; high-throughput low-latency file access'))
    lines.append(txt_row('Parent partition= Hyper-V management OS; has direct hardware access'))
    lines.append(txt_row('Child partition= VM guest; hardware access via VMBus and VSP/VSC model'))
    lines.append(txt_row('RDMA         = Remote Direct Memory Access; bypasses OS for low-latency IO'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-arch-how', 'docs/compute/windows-server/architecture/how-it-works/index.md', 'Windows Server How It Works')
def _windows_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('Windows Server boot process, service management, and AD authentication flow.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Boot Sequence'), bMid(L2, R2, 'Kerberos Auth Flow'))))
    lines.append(R(merge(bMid(L1, R1, 'UEFI/BIOS → bootmgr'), bMid(L2, R2, 'User → AS request → TGT'))))
    lines.append(R(merge(bMid(L1, R1, 'winload.exe → kernel load'), bMid(L2, R2, 'TGT → TGS request → ticket'))))
    lines.append(R(merge(bMid(L1, R1, 'Kernel init → HAL → drivers'), bMid(L2, R2, 'Service ticket → resource'))))
    lines.append(R(merge(bMid(L1, R1, 'Session 0: services start'), bMid(L2, R2, 'PAC: user groups in ticket'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('  Boot completes before user logon; Kerberos tickets cached for session'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Group Policy Processing'), bMid(L2, R2, 'File System Operations'))))
    lines.append(R(merge(bMid(L1, R1, 'Machine GPO at startup'), bMid(L2, R2, 'NTFS: journalled metadata'))))
    lines.append(R(merge(bMid(L1, R1, 'User GPO at logon'), bMid(L2, R2, 'Shadow Copy: VSS snapshots'))))
    lines.append(R(merge(bMid(L1, R1, 'gpupdate /force: reapply'), bMid(L2, R2, 'DFS: distributed namespace'))))
    lines.append(R(merge(bMid(L1, R1, 'Loopback: machine applies user'), bMid(L2, R2, 'BranchCache: WAN optimise'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical server · Domain Controllers · NTP source · storage'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('bootmgr      = Windows Boot Manager; reads BCD store to select OS'))
    lines.append(txt_row('winload.exe  = OS loader; loads kernel, HAL, and boot drivers'))
    lines.append(txt_row('Session 0    = isolated service session; no interactive user access'))
    lines.append(txt_row('TGT          = Ticket Granting Ticket; obtained from KDC at logon'))
    lines.append(txt_row('TGS          = Ticket Granting Service; issues service-specific tickets'))
    lines.append(txt_row('PAC          = Privilege Attribute Certificate; encodes group memberships'))
    lines.append(txt_row('GPO          = Group Policy Object; settings applied at OU/domain level'))
    lines.append(txt_row('Loopback     = GPO mode applying machine-linked user policy at logon'))
    lines.append(txt_row('VSS          = Volume Shadow Copy Service; creates consistent snapshots'))
    lines.append(txt_row('DFS          = Distributed File System; namespace + replication for shares'))
    lines.append(txt_row('BranchCache  = caches remote content at branch office; reduces WAN traffic'))
    lines.append(txt_row('gpupdate     = triggers immediate GP refresh; /force reapplies all settings'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-arch-int', 'docs/compute/windows-server/architecture/integrations/index.md', 'Windows Server Integrations')
def _windows_arch_int():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Integrations'))
    lines.append(txt_row())
    lines.append(txt_row('Windows Server integrations: Azure AD, VMware, monitoring tools, and enterprise apps.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Identity Integrations'), bMid(L2, R2, 'Virtualisation'))))
    lines.append(R(merge(bMid(L1, R1, 'Azure AD Connect: hybrid sync'), bMid(L2, R2, 'Hyper-V: built-in hypervisor'))))
    lines.append(R(merge(bMid(L1, R1, 'AD FS: SAML/OAuth federation'), bMid(L2, R2, 'VMware Tools: guest agent'))))
    lines.append(R(merge(bMid(L1, R1, 'LDAPS: secure LDAP queries'), bMid(L2, R2, 'System Center VMM: mgmt'))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate Services (AD CS)'), bMid(L2, R2, 'Azure Arc: cloud-managed'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('  AD integrates with cloud via Connect/ADFS; Arc extends cloud management on-prem'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Monitoring'), bMid(L2, R2, 'Storage and Backup'))))
    lines.append(R(merge(bMid(L1, R1, 'Windows Events: WinRM forward'), bMid(L2, R2, 'Windows Server Backup'))))
    lines.append(R(merge(bMid(L1, R1, 'Azure Monitor Agent (AMA)'), bMid(L2, R2, 'DFS Replication: shares'))))
    lines.append(R(merge(bMid(L1, R1, 'SCOM: enterprise monitoring'), bMid(L2, R2, 'SAN: iSCSI / FC initiator'))))
    lines.append(R(merge(bMid(L1, R1, 'Splunk UF: log forwarding'), bMid(L2, R2, 'Storage Spaces: software RAID'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical or virtual server · NIC · SAN/NAS · Azure connectivity'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Azure AD Connect= synchronises on-prem AD users/groups to Azure AD (Entra)'))
    lines.append(txt_row('AD FS         = Active Directory Federation Services; SAML/OAuth IdP'))
    lines.append(txt_row('AD CS         = Certificate Services; internal PKI for cert issuance'))
    lines.append(txt_row('Azure Arc     = extends Azure management plane to on-prem Windows servers'))
    lines.append(txt_row('AMA           = Azure Monitor Agent; replaces Log Analytics agent'))
    lines.append(txt_row('SCOM          = System Center Operations Manager; enterprise monitoring'))
    lines.append(txt_row('WinRM         = Windows Remote Management; used for PS remoting + event forward'))
    lines.append(txt_row('LDAPS         = LDAP over TLS; requires DC certificate; port 636'))
    lines.append(txt_row('Storage Spaces= Windows software-defined storage; RAID-like redundancy'))
    lines.append(txt_row('VMM           = Virtual Machine Manager; Hyper-V cluster management'))
    lines.append(txt_row('DFS-R         = DFS Replication; multi-master file replication between servers'))
    lines.append(txt_row('iSCSI initiator= Windows built-in iSCSI client for SAN block access'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-arch-design', 'docs/compute/windows-server/architecture/design-standards/index.md', 'Windows Server Design Standards')
def _windows_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Design Standards'))
    lines.append(txt_row())
    lines.append(txt_row('Design standards: naming conventions, OU structure, GPO hierarchy, and server hardening baseline.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Naming Conventions'), bMid(L2, R2, 'AD OU Structure'))))
    lines.append(R(merge(bMid(L1, R1, 'Server: SITE-ROLE-NNN'), bMid(L2, R2, 'Domain → Servers → Role OUs'))))
    lines.append(R(merge(bMid(L1, R1, 'Domain: corp.example.com'), bMid(L2, R2, 'Tier: T0 DC / T1 server / T2 WS'))))
    lines.append(R(merge(bMid(L1, R1, 'GPO: ROLE-SETTING-POL format'), bMid(L2, R2, 'Admin Groups: per tier + role'))))
    lines.append(R(merge(bMid(L1, R1, 'Service accounts: svc-appname'), bMid(L2, R2, 'LAPS: local admin pwd mgmt'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('  Tiered admin model prevents lateral movement; LAPS eliminates shared local passwords'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'GPO Design'), bMid(L2, R2, 'Server Baseline'))))
    lines.append(R(merge(bMid(L1, R1, 'Default Domain Policy: password'), bMid(L2, R2, 'Server Core preferred over GUI'))))
    lines.append(R(merge(bMid(L1, R1, 'Workstation / Server baselines'), bMid(L2, R2, 'SMB signing: required on all'))))
    lines.append(R(merge(bMid(L1, R1, 'Role-specific: IIS / SQL / DC'), bMid(L2, R2, 'Audit: logon, object, privilege'))))
    lines.append(R(merge(bMid(L1, R1, 'Link order: lower = higher prio'), bMid(L2, R2, 'Windows Defender: AV + EDR'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical or virtual server · Domain Controllers · AD replication · PKI'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Tiered admin = Tier 0 (DCs), Tier 1 (servers), Tier 2 (workstations); no cross-tier'))
    lines.append(txt_row('LAPS         = Local Administrator Password Solution; unique pwd per machine'))
    lines.append(txt_row('OU           = Organisational Unit; container for GPO linking and delegation'))
    lines.append(txt_row('GPO link order= lowest link order number = highest priority in OU'))
    lines.append(txt_row('SMB signing  = cryptographic signing of SMB packets; prevents relay attacks'))
    lines.append(txt_row('Server Core  = no GUI; managed via PowerShell/WAC; reduced attack surface'))
    lines.append(txt_row('svc- prefix  = service account naming prefix; helps identify in audit logs'))
    lines.append(txt_row('Default Domain Policy= must only contain password and account lockout settings'))
    lines.append(txt_row('EDR          = Endpoint Detection and Response; Microsoft Defender for Endpoint'))
    lines.append(txt_row('Privilege audit= logs use of user rights assignments; required for compliance'))
    lines.append(txt_row('Object audit  = logs file/folder access; apply selectively to avoid log flood'))
    lines.append(txt_row('Logon audit   = logs interactive, network, and Kerberos logons'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-ops', 'docs/compute/windows-server/operations/index.md', 'Windows Server Operations')
def _windows_ops():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2, L3, R3 = 3, 33, 36, 66, 69, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Operations'))
    lines.append(txt_row())
    lines.append(txt_row('Windows Server day-to-day operations: patching, AD management, monitoring, and backups.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Patch Management'), bMid(L2, R2, 'AD Operations'), bMid(L3, R3, 'Monitoring'))))
    lines.append(R(merge(bMid(L1, R1, 'WSUS / Intune / MECM'), bMid(L2, R2, 'User / group lifecycle'), bMid(L3, R3, 'Event Viewer alerts'))))
    lines.append(R(merge(bMid(L1, R1, 'Patch Tuesday cadence'), bMid(L2, R2, 'GPO create + test + link'), bMid(L3, R3, 'Performance Monitor'))))
    lines.append(R(merge(bMid(L1, R1, 'WSFC: rolling update'), bMid(L2, R2, 'OU delegation: least priv'), bMid(L3, R3, 'Task Scheduler jobs'))))
    lines.append(R(merge(bMid(L1, R1, 'Test in non-prod first'), bMid(L2, R2, 'AD recycle bin: restore'), bMid(L3, R3, 'SNMP / WMI / WinRM'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical or virtual server · Domain Controllers · WSUS server · backup storage'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('WSUS         = Windows Server Update Services; on-prem patch distribution'))
    lines.append(txt_row('MECM         = Microsoft Endpoint Configuration Manager; enterprise patching'))
    lines.append(txt_row('Patch Tuesday= second Tuesday of month; Microsoft releases cumulative updates'))
    lines.append(txt_row('WSFC         = Windows Server Failover Cluster; rolling update with CAU'))
    lines.append(txt_row('CAU          = Cluster Aware Updating; non-disruptive patch application'))
    lines.append(txt_row('AD Recycle Bin= restore deleted objects within tombstone lifetime (default 180d)'))
    lines.append(txt_row('OU delegation= grant specific permissions on OU without Domain Admin'))
    lines.append(txt_row('WMI          = Windows Management Instrumentation; query system state'))
    lines.append(txt_row('Task Scheduler= built-in job scheduler; XML-based task definitions'))
    lines.append(txt_row('Event Viewer = Windows event log GUI; filter by ID/source/level'))
    lines.append(txt_row('Performance Monitor= real-time/historical counter data; PerfMon.exe'))
    lines.append(txt_row('SNMP         = network monitoring protocol; available via Windows feature'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-ops-procedures', 'docs/compute/windows-server/operations/procedures/index.md', 'Windows Server Ops Procedures')
def _windows_ops_procedures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Operations Procedures'))
    lines.append(txt_row())
    lines.append(txt_row('Standard procedures: user provisioning, server decommission, patch process, and AD cleanup.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'User Provisioning'), bMid(L2, R2, 'Server Decommission'))))
    lines.append(R(merge(bMid(L1, R1, 'Create AD user + set attributes'), bMid(L2, R2, 'Remove from all AD groups'))))
    lines.append(R(merge(bMid(L1, R1, 'Add to role-based AD groups'), bMid(L2, R2, 'Disable computer account'))))
    lines.append(R(merge(bMid(L1, R1, 'Set mailbox: Exchange/365'), bMid(L2, R2, 'Migrate data + shares'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA: enrol TOTP / smart card'), bMid(L2, R2, 'Delete after 30-day hold'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('  Provisioning via AD group membership drives access; decom must clear AD object'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Patch Procedure'), bMid(L2, R2, 'AD Cleanup'))))
    lines.append(R(merge(bMid(L1, R1, 'Download from WSUS / catalog'), bMid(L2, R2, 'Inactive computers: 90-day'))))
    lines.append(R(merge(bMid(L1, R1, 'Test on non-prod server first'), bMid(L2, R2, 'Stale users: disable then delete'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedule window + notify users'), bMid(L2, R2, 'Empty groups: quarterly review'))))
    lines.append(R(merge(bMid(L1, R1, 'Apply + verify + reboot check'), bMid(L2, R2, 'SPNs: check for orphans'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Domain Controllers · WSUS server · Exchange/365 · backup system'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Role-based groups= AD security groups named by role; drive resource access'))
    lines.append(txt_row('Smart card     = hardware MFA token; requires certificate enrollment'))
    lines.append(txt_row('Computer account= AD object for server; disable before decommission'))
    lines.append(txt_row('30-day hold    = quarantine period before deleting decommissioned object'))
    lines.append(txt_row('WSUS           = Windows Server Update Services; centralised patch repo'))
    lines.append(txt_row('Patch window   = agreed maintenance window; communicated to stakeholders'))
    lines.append(txt_row('Inactive computers= lastLogonTimestamp > 90 days; candidate for disable'))
    lines.append(txt_row('SPN            = Service Principal Name; Kerberos service identifier; orphans cause auth fail'))
    lines.append(txt_row('Stale user     = account not used in > 90 days; disable before delete'))
    lines.append(txt_row('Empty group    = AD group with no members; clean up to reduce audit noise'))
    lines.append(txt_row('mailbox        = Exchange/365 mailbox; license must be unassigned on decom'))
    lines.append(txt_row('TOTP MFA       = time-based one-time password; enforced via Azure AD CA'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-ops-backup', 'docs/compute/windows-server/operations/backup-restore/index.md', 'Windows Server Backup')
def _windows_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Backup and Restore'))
    lines.append(txt_row())
    lines.append(txt_row('Windows Server backup strategies: VSS-based backups, AD backup, and Hyper-V checkpoints.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Windows Server Backup (WSB)'), bMid(L2, R2, 'Active Directory Backup'))))
    lines.append(R(merge(bMid(L1, R1, 'wbadmin: CLI backup tool'), bMid(L2, R2, 'ntdsutil: AD snapshot + backup'))))
    lines.append(R(merge(bMid(L1, R1, 'VSS: consistent snapshots'), bMid(L2, R2, 'System State includes AD DB'))))
    lines.append(R(merge(bMid(L1, R1, 'Bare metal recovery (BMR)'), bMid(L2, R2, 'Authoritative restore: NTDS'))))
    lines.append(R(merge(bMid(L1, R1, 'Scheduled: daily + monthly'), bMid(L2, R2, 'AD Recycle Bin: 180-day'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('  System State backup captures AD; BMR for full server recovery'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Hyper-V Backup'), bMid(L2, R2, 'Third-Party / Enterprise'))))
    lines.append(R(merge(bMid(L1, R1, 'VM checkpoint: snapshot'), bMid(L2, R2, 'Veeam: agent + VM backup'))))
    lines.append(R(merge(bMid(L1, R1, 'Export VM: offline full copy'), bMid(L2, R2, 'DPM: System Center backup'))))
    lines.append(R(merge(bMid(L1, R1, 'Application-consistent VSS'), bMid(L2, R2, 'Azure Backup: cloud retention'))))
    lines.append(R(merge(bMid(L1, R1, 'Replica: standby VM copy'), bMid(L2, R2, 'Test restore: quarterly SLA'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical or virtual server · backup storage (NAS/tape/Azure) · Hyper-V host'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('wbadmin      = command-line tool for Windows Server Backup operations'))
    lines.append(txt_row('VSS          = Volume Shadow Copy Service; quiesces app for consistent backup'))
    lines.append(txt_row('BMR          = Bare Metal Recovery; restore entire OS without pre-existing install'))
    lines.append(txt_row('System State = AD DB + SYSVOL + registry + boot files; AD backup minimum'))
    lines.append(txt_row('ntdsutil     = AD utility; used for authoritative restore and metadata cleanup'))
    lines.append(txt_row('Authoritative restore= restore marks AD objects with higher USN to replicate'))
    lines.append(txt_row('AD Recycle Bin= soft-delete; restore via Get-ADObject + Restore-ADObject'))
    lines.append(txt_row('VM checkpoint= point-in-time snapshot of VM state; not a backup replacement'))
    lines.append(txt_row('VM Replica   = Hyper-V async replication to another host; DR option'))
    lines.append(txt_row('DPM          = Data Protection Manager; System Center backup product'))
    lines.append(txt_row('Azure Backup = cloud backup service; supports on-prem via MARS agent'))
    lines.append(txt_row('Test restore = periodic recovery drill; validates backup integrity'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-ops-health', 'docs/compute/windows-server/operations/health-checks/index.md', 'Windows Server Health Checks')
def _windows_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('Regular health checks: disk, AD replication, services, and event log review.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'System Health'), bMid(L2, R2, 'AD Health'))))
    lines.append(R(merge(bMid(L1, R1, 'Disk: > 20 % free required'), bMid(L2, R2, 'repadmin /replsummary'))))
    lines.append(R(merge(bMid(L1, R1, 'CPU: < 80 % sustained'), bMid(L2, R2, 'dcdiag /test:all'))))
    lines.append(R(merge(bMid(L1, R1, 'Memory: paging < 100 MB/s'), bMid(L2, R2, 'netlogon: running on all DCs'))))
    lines.append(R(merge(bMid(L1, R1, 'Event log: filter 1xxx errors'), bMid(L2, R2, 'SYSVOL: replicated + accessible'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('  System + AD checks should run daily; cluster and security checks weekly'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster Health (WSFC)'), bMid(L2, R2, 'Security Posture'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-ClusterNode: all up'), bMid(L2, R2, 'Missing patches: age < 30 d'))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster log: no errors'), bMid(L2, R2, 'Defender: signatures current'))))
    lines.append(R(merge(bMid(L1, R1, 'Quorum: witness reachable'), bMid(L2, R2, 'Local admins: minimum count'))))
    lines.append(R(merge(bMid(L1, R1, 'CSV: available + healthy'), bMid(L2, R2, 'Audit log: no gaps'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical or virtual server · Domain Controllers · cluster shared storage · SIEM'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('repadmin      = AD replication admin tool; /replsummary shows lag and errors'))
    lines.append(txt_row('dcdiag        = DC diagnostic tool; runs test battery against all DCs'))
    lines.append(txt_row('netlogon      = Windows service; required for domain auth and GPO application'))
    lines.append(txt_row('SYSVOL        = shared folder on all DCs; must be replicated and accessible'))
    lines.append(txt_row('Get-ClusterNode= PowerShell command; shows all cluster nodes and their state'))
    lines.append(txt_row('Quorum        = cluster voting mechanism; requires majority to stay online'))
    lines.append(txt_row('Witness       = quorum tie-breaker; disk witness or cloud witness'))
    lines.append(txt_row('CSV           = Cluster Shared Volume; shared storage for Hyper-V VMs'))
    lines.append(txt_row('Paging        = excessive page file activity indicates RAM shortage'))
    lines.append(txt_row('Event 1xxx    = common error range in Windows event logs; filter by level'))
    lines.append(txt_row('Audit log gap = gap in security event log sequence; may indicate tampering'))
    lines.append(txt_row('LAPS          = auto-rotated local admin password; check rotation age'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-ops-install', 'docs/compute/windows-server/operations/install-upgrade/index.md', 'Windows Server Install and Upgrade')
def _windows_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Install and Upgrade'))
    lines.append(txt_row())
    lines.append(txt_row('Windows Server installation and in-place upgrade procedures including AD DS promotion.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Fresh Install'), bMid(L2, R2, 'In-Place Upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'Boot from ISO / WDS / PXE'), bMid(L2, R2, 'Support: 2016 → 2019 → 2022'))))
    lines.append(R(merge(bMid(L1, R1, 'Partition: C: + separate data'), bMid(L2, R2, 'Compatibility check: setup.exe'))))
    lines.append(R(merge(bMid(L1, R1, 'Unattend.xml: silent install'), bMid(L2, R2, 'Backup before upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'Sysprep: image generalisation'), bMid(L2, R2, 'Driver compatibility verify'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('  Fresh install preferred for major upgrades; in-place for patch-level change'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'DC Promotion (AD DS)'), bMid(L2, R2, 'Post-Install Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Install-WindowsFeature AD-DS'), bMid(L2, R2, 'Apply CIS/STIG baseline GPO'))))
    lines.append(R(merge(bMid(L1, R1, 'Install-ADDSForest / replica'), bMid(L2, R2, 'Enable Windows Defender'))))
    lines.append(R(merge(bMid(L1, R1, 'Raise domain/forest FFL level'), bMid(L2, R2, 'Join to AD domain'))))
    lines.append(R(merge(bMid(L1, R1, 'Verify replication + DNS'), bMid(L2, R2, 'Activate: AVMA / KMS'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical or virtual server · ISO/WDS · KMS server · existing Domain Controllers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('WDS          = Windows Deployment Services; PXE-based OS deployment'))
    lines.append(txt_row('Unattend.xml = answer file; automates install choices for unattended setup'))
    lines.append(txt_row('Sysprep      = strips machine-specific info from image; required for cloning'))
    lines.append(txt_row('FFL          = Forest Functional Level; enables features across all domains'))
    lines.append(txt_row('DFL          = Domain Functional Level; enables domain-wide AD features'))
    lines.append(txt_row('Replica DC   = additional DC in existing domain; joined via dcpromo/PS'))
    lines.append(txt_row('STIG         = Security Technical Implementation Guide; DoD hardening standard'))
    lines.append(txt_row('KMS          = Key Management Service; volume activation server'))
    lines.append(txt_row('AVMA         = Automatic VM Activation; VMs activate via licensed Hyper-V host'))
    lines.append(txt_row('In-place upgrade= runs setup.exe on existing OS; preserves apps + settings'))
    lines.append(txt_row('Compatibility check= setup /compat scanonly; identifies blockers before upgrade'))
    lines.append(txt_row('Generalise   = sysprep step to remove SIDs; must do before capturing image'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-ops-scripts', 'docs/compute/windows-server/operations/scripts/index.md', 'Windows Server Scripts')
def _windows_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Operations Scripts'))
    lines.append(txt_row())
    lines.append(txt_row('PowerShell scripts for Windows Server operations: AD, disk, patching, and health checks.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'AD Management Scripts'), bMid(L2, R2, 'System Scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'New-ADUser + Set-ADUser'), bMid(L2, R2, 'Get-EventLog: filtered export'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-ADGroupMember -Recursive'), bMid(L2, R2, 'Get-Disk + Get-Partition'))))
    lines.append(R(merge(bMid(L1, R1, 'Search-ADAccount -Inactive'), bMid(L2, R2, 'Get-WindowsUpdateLog'))))
    lines.append(R(merge(bMid(L1, R1, 'repadmin /replsummary parse'), bMid(L2, R2, 'Restart-Service, Get-Service'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('  Scripts in version control; test in non-prod; log all changes'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Scheduled Task Scripts'), bMid(L2, R2, 'Hyper-V Scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'Register-ScheduledTask'), bMid(L2, R2, 'Get-VM + Start/Stop-VM'))))
    lines.append(R(merge(bMid(L1, R1, 'Log to event log: Write-EventLog'), bMid(L2, R2, 'Checkpoint-VM: snapshot'))))
    lines.append(R(merge(bMid(L1, R1, 'Error handling: try/catch'), bMid(L2, R2, 'Get-VMReplication: status'))))
    lines.append(R(merge(bMid(L1, R1, 'Send-MailMessage: alerts'), bMid(L2, R2, 'Move-VM: live migration'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Domain Controllers · WSUS · Hyper-V hosts · task scheduler on managed servers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('New-ADUser   = creates AD user; must set -AccountPassword -Enabled $true'))
    lines.append(txt_row('Search-ADAccount= finds inactive/locked/expired accounts in AD'))
    lines.append(txt_row('Get-EventLog = queries Windows Event Log; use -EntryType Error to filter'))
    lines.append(txt_row('Write-EventLog= writes entry to event log; use registered event source'))
    lines.append(txt_row('Register-ScheduledTask= creates Windows scheduled task via PowerShell'))
    lines.append(txt_row('Checkpoint-VM= creates Hyper-V checkpoint (snapshot); state + disk'))
    lines.append(txt_row('Get-VMReplication= shows Hyper-V Replica status and lag'))
    lines.append(txt_row('Move-VM      = live migration of running VM to another host'))
    lines.append(txt_row('try/catch    = error handling in PowerShell; $_ contains error details'))
    lines.append(txt_row('Send-MailMessage= sends email from script; SMTP relay required'))
    lines.append(txt_row('Get-WindowsUpdateLog= converts ETW trace to readable Windows Update log'))
    lines.append(txt_row('repadmin     = AD replication tool; output parsed by PS for reporting'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-ops-cli', 'docs/compute/windows-server/operations/cli-reference/index.md', 'Windows Server CLI Reference')
def _windows_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('Essential Windows Server CLI: PowerShell, cmd.exe, and server management commands.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'PowerShell Essentials'), bMid(L2, R2, 'Network Commands'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-Command / Get-Help'), bMid(L2, R2, 'ipconfig /all, /flushdns'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-Member: object properties'), bMid(L2, R2, 'ping / tracert / nslookup'))))
    lines.append(R(merge(bMid(L1, R1, 'Select-Object / Where-Object'), bMid(L2, R2, 'netstat -ano / netsh'))))
    lines.append(R(merge(bMid(L1, R1, 'Format-Table / Export-CSV'), bMid(L2, R2, 'Test-NetConnection port'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('  PowerShell is primary CLI; cmd.exe for legacy/batch; PS remoting via WinRM'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Disk and Services'), bMid(L2, R2, 'AD Commands'))))
    lines.append(R(merge(bMid(L1, R1, 'diskpart / diskmgmt.msc'), bMid(L2, R2, 'gpresult /r /h report.html'))))
    lines.append(R(merge(bMid(L1, R1, 'sc query / sc start/stop'), bMid(L2, R2, 'gpupdate /force'))))
    lines.append(R(merge(bMid(L1, R1, 'sfc /scannow: file check'), bMid(L2, R2, 'nltest /sc_query:domain'))))
    lines.append(R(merge(bMid(L1, R1, 'chkdsk /f /r: disk repair'), bMid(L2, R2, 'repadmin /replsummary'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical or virtual server · terminal (local/RDP/WinRM) · Domain Controllers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Get-Help -Online= opens online docs for cmdlet; -Examples shows usage'))
    lines.append(txt_row('Where-Object = filters pipeline objects by condition; alias: where or ?'))
    lines.append(txt_row('Test-NetConnection= tests TCP port reachability; -ComputerName -Port'))
    lines.append(txt_row('netstat -ano = shows all connections with PID; -a all, -n numeric, -o pid'))
    lines.append(txt_row('netsh        = network configuration tool; interface, firewall, wlan contexts'))
    lines.append(txt_row('diskpart     = interactive disk partitioning; use select disk/volume'))
    lines.append(txt_row('sc query     = query service status; sc config changes service config'))
    lines.append(txt_row('sfc /scannow = System File Checker; verifies and repairs protected system files'))
    lines.append(txt_row('chkdsk /f /r = fix file system errors and recover data from bad sectors'))
    lines.append(txt_row('gpresult /h  = generates HTML GP report; shows applied policies'))
    lines.append(txt_row('nltest       = network logon test; /sc_query verifies secure channel to DC'))
    lines.append(txt_row('repadmin     = AD replication diagnostics; /replsummary shows health'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-ops-common-issues', 'docs/compute/windows-server/operations/common-issues/index.md', 'Windows Server Common Issues')
def _windows_ops_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Common Operational Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Common issues: high CPU/RAM, RDP failures, AD replication errors, disk full, service failures.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Performance Issues'), bMid(L2, R2, 'Connectivity Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'High CPU: Task Manager → Details'), bMid(L2, R2, 'RDP port 3389 blocked/disabled'))))
    lines.append(R(merge(bMid(L1, R1, 'RAM: pooled memory leak check'), bMid(L2, R2, 'Firewall rules blocking traffic'))))
    lines.append(R(merge(bMid(L1, R1, 'Disk: windirstat + cleanmgr'), bMid(L2, R2, 'DNS resolution failure for host'))))
    lines.append(R(merge(bMid(L1, R1, 'Paging file exhausted: resize'), bMid(L2, R2, 'NIC driver or teaming errors'))))
    lines.append(R(merge(bMid(L1, R1, 'Hung service: sc stop + start'), bMid(L2, R2, 'Route table: route print check'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Performance and connectivity are top two issue classes; check Event Viewer first.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'AD / Domain Issues'), bMid(L2, R2, 'Update & Patch Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'Replication: repadmin /replsum'), bMid(L2, R2, 'Windows Update stuck pending'))))
    lines.append(R(merge(bMid(L1, R1, 'Secure channel broken: nltest'), bMid(L2, R2, 'WSUS approval not pushed down'))))
    lines.append(R(merge(bMid(L1, R1, 'Kerberos clock skew > 5 min'), bMid(L2, R2, 'WinRM errors blocking WUA'))))
    lines.append(R(merge(bMid(L1, R1, 'SRV DNS records missing: check'), bMid(L2, R2, 'CBS log: dism /online /cleanup'))))
    lines.append(R(merge(bMid(L1, R1, 'GPO not applying: gpresult /h'), bMid(L2, R2, 'Pending reboot blocks updates'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical or virtual server · CPU cores · RAM DIMMs · NIC ports · SAS/SATA/NVMe storage'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Event Viewer   = Windows MMC snap-in; System/Application logs show errors and warnings'))
    lines.append(txt_row('repadmin       = AD replication diagnostics CLI; /replsummary shows partner health'))
    lines.append(txt_row('nltest         = network logon test; /sc_query verifies secure channel to domain DC'))
    lines.append(txt_row('Kerberos       = authentication protocol; tickets require clock sync within 5 minutes'))
    lines.append(txt_row('GPO            = Group Policy Object; applied via gpupdate /force; troubleshoot gpresult'))
    lines.append(txt_row('WSUS           = Windows Server Update Services; distributes patches to managed clients'))
    lines.append(txt_row('CBS log        = Component-Based Servicing log; tracks Windows component install state'))
    lines.append(txt_row('windirstat     = third-party disk usage visualiser; identifies large file consumers'))
    lines.append(txt_row('cleanmgr       = Disk Cleanup utility; removes temp files, WinSxS backup components'))
    lines.append(txt_row('Paging file    = virtual memory extension on disk; exhaustion causes crashes'))
    lines.append(txt_row('NIC teaming    = link aggregation / failover for network adapters via LBFO or SET'))
    lines.append(txt_row('WUA            = Windows Update Agent service; communicates with WSUS or Windows Update'))
    lines.append(txt_row('dism           = Deployment Image Servicing and Management; repairs OS component store'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-sec', 'docs/compute/windows-server/security/index.md', 'Windows Server Security Overview')
def _windows_sec_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2, L3, R3 = 3, 33, 36, 66, 69, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Security Overview'))
    lines.append(txt_row())
    lines.append(txt_row('Security pillars: identity/access control, auth hardening, encryption, and OS hardening.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Access Control'), bMid(L2, R2, 'Authentication'), bMid(L3, R3, 'Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'AD RBAC + local groups'), bMid(L2, R2, 'MFA via Azure AD / Duo'), bMid(L3, R3, 'BitLocker drive encrypt'))))
    lines.append(R(merge(bMid(L1, R1, 'NTFS + Share permissions'), bMid(L2, R2, 'Kerberos + NTLM config'), bMid(L3, R3, 'TLS 1.2/1.3 enforce'))))
    lines.append(R(merge(bMid(L1, R1, 'Protected Users group'), bMid(L2, R2, 'LAPS managed passwords'), bMid(L3, R3, 'EFS for file-level enc'))))
    lines.append(R(merge(bMid(L1, R1, 'PAW for admin access'), bMid(L2, R2, 'Smart card / cert login'), bMid(L3, R3, 'IPsec transport/tunnel'))))
    lines.append(R(merge(bMid(L1, R1, 'JEA constrained PS'), bMid(L2, R2, 'NPS RADIUS for network'), bMid(L3, R3, 'WinRM HTTPS only'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('Identity and access form the foundation; encryption protects data at rest and in transit.'))
    lines.append(txt_row())
    lines.append(R(arrow([18, 51, 84])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Hardening'), bMid(L2, R2, 'Monitoring & Audit'), bMid(L3, R3, 'Compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'CIS Benchmark baseline'), bMid(L2, R2, 'Security event audit log'), bMid(L3, R3, 'GPO STIG policies'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable SMBv1/NTLM'), bMid(L2, R2, 'Advanced Audit Policy'), bMid(L3, R3, 'SCAP scanning tools'))))
    lines.append(R(merge(bMid(L1, R1, 'AppLocker / WDAC rules'), bMid(L2, R2, 'Event forwarding (WEF)'), bMid(L3, R3, 'Defender ATP policies'))))
    lines.append(R(merge(bMid(L1, R1, 'Credential Guard enable'), bMid(L2, R2, 'SIEM integration logs'), bMid(L3, R3, 'PCI/SOX/HIPAA audits'))))
    lines.append(R(merge(bMid(L1, R1, 'Windows Defender enable'), bMid(L2, R2, 'Logon/logoff tracking'), bMid(L3, R3, 'Vuln scan quarterly'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical or virtual server · TPM 2.0 chip · UEFI Secure Boot · HSM for key storage'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RBAC           = Role-Based Access Control; permissions via AD group membership'))
    lines.append(txt_row('NTFS           = New Technology File System; supports ACLs, EFS, and auditing'))
    lines.append(txt_row('LAPS           = Local Admin Password Solution; randomises local admin passwords in AD'))
    lines.append(txt_row('PAW            = Privileged Access Workstation; hardened device for admin tasks only'))
    lines.append(txt_row('JEA            = Just Enough Administration; PowerShell role-based remoting sessions'))
    lines.append(txt_row('BitLocker      = Windows full-disk encryption using TPM + PIN or USB key'))
    lines.append(txt_row('Credential Guard= Virtualisation-based security isolates LSASS credential store'))
    lines.append(txt_row('CIS Benchmark  = Center for Internet Security hardening baseline for Windows Server'))
    lines.append(txt_row('STIG           = Security Technical Implementation Guide; DoD hardening standard'))
    lines.append(txt_row('WEF            = Windows Event Forwarding; centralises events from multiple servers'))
    lines.append(txt_row('AppLocker      = policy-based app whitelisting; controls which executables run'))
    lines.append(txt_row('WDAC           = Windows Defender Application Control; kernel-level code integrity'))
    lines.append(txt_row('Defender ATP   = Microsoft Defender for Endpoint; EDR and threat detection'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-sec-access', 'docs/compute/windows-server/security/access-control/index.md', 'Windows Server Access Control')
def _windows_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Access Control'))
    lines.append(txt_row())
    lines.append(txt_row('Access control enforced through AD groups, NTFS ACLs, share permissions, and privileged access.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'AD Group-Based RBAC'), bMid(L2, R2, 'NTFS & Share Permissions'))))
    lines.append(R(merge(bMid(L1, R1, 'Domain groups → resource ACL'), bMid(L2, R2, 'NTFS ACE: Allow/Deny per SID'))))
    lines.append(R(merge(bMid(L1, R1, 'Domain Local groups for access'), bMid(L2, R2, 'Share perms: max allowed users'))))
    lines.append(R(merge(bMid(L1, R1, 'Global groups for user sets'), bMid(L2, R2, 'Effective = NTFS AND Share'))))
    lines.append(R(merge(bMid(L1, R1, 'Universal groups cross-domain'), bMid(L2, R2, 'Inheritance: propagate down'))))
    lines.append(R(merge(bMid(L1, R1, 'Least privilege by default'), bMid(L2, R2, 'icacls command for scripting'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('AD groups define who; NTFS ACLs define what access they get to which objects.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Privileged Access Control'), bMid(L2, R2, 'Protected Users & Tiering'))))
    lines.append(R(merge(bMid(L1, R1, 'PAW for Tier-0 admins only'), bMid(L2, R2, 'Protected Users: no NTLM/DES'))))
    lines.append(R(merge(bMid(L1, R1, 'Admin accounts separate from user'), bMid(L2, R2, 'Tier-0: DCs + PKI + AD'))))
    lines.append(R(merge(bMid(L1, R1, 'Time-bound access via PIM'), bMid(L2, R2, 'Tier-1: servers and services'))))
    lines.append(R(merge(bMid(L1, R1, 'JEA: constrained PS sessions'), bMid(L2, R2, 'Tier-2: workstations only'))))
    lines.append(R(merge(bMid(L1, R1, 'Local admin via LAPS only'), bMid(L2, R2, 'No cross-tier admin allowed'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical or virtual server · domain controller · AD database on DC storage'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SID            = Security Identifier; unique identifier for every AD object and account'))
    lines.append(txt_row('ACL            = Access Control List; ordered list of ACEs on a securable object'))
    lines.append(txt_row('ACE            = Access Control Entry; Allow or Deny rule for a specific SID'))
    lines.append(txt_row('NTFS ACL       = file/folder permissions enforced by NTFS file system kernel driver'))
    lines.append(txt_row('Share permission= network share access level; read/change/full — combined with NTFS'))
    lines.append(txt_row('Domain Local   = AD group scope; members from any domain; access in own domain'))
    lines.append(txt_row('Global group   = AD group scope; members from same domain; used across domains'))
    lines.append(txt_row('Universal group = AD group; members from any domain; replicated to global catalog'))
    lines.append(txt_row('PIM            = Privileged Identity Management; just-in-time admin role elevation'))
    lines.append(txt_row('PAW            = Privileged Access Workstation; hardened device for admin-only work'))
    lines.append(txt_row('Tiering        = AD admin tier model: Tier-0/1/2 separates admin account scope'))
    lines.append(txt_row('icacls         = Windows CLI tool to display and modify NTFS file/folder ACLs'))
    lines.append(txt_row('Protected Users= AD security group; blocks NTLM, unconstrained delegation, DES'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-sec-auth', 'docs/compute/windows-server/security/authentication/index.md', 'Windows Server Authentication')
def _windows_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('Authentication stack: Kerberos primary, NTLM fallback, certificate-based, MFA enforcement.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Kerberos Authentication'), bMid(L2, R2, 'NTLM Authentication'))))
    lines.append(R(merge(bMid(L1, R1, 'Default AD protocol (port 88)'), bMid(L2, R2, 'Fallback: no DC reachable'))))
    lines.append(R(merge(bMid(L1, R1, 'AS-REQ → AS-REP (TGT)'), bMid(L2, R2, 'Challenge-response 3-way'))))
    lines.append(R(merge(bMid(L1, R1, 'TGS-REQ → TGS-REP (service)'), bMid(L2, R2, 'Disable NTLMv1; allow v2 only'))))
    lines.append(R(merge(bMid(L1, R1, 'Mutual authentication built-in'), bMid(L2, R2, 'Block NTLM via GPO Network'))))
    lines.append(R(merge(bMid(L1, R1, 'SPNs register services in AD'), bMid(L2, R2, 'Monitor event 4776 for use'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Kerberos preferred; NTLM restricted by GPO; both generate audit events 4624/4625.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate & Smart Card'), bMid(L2, R2, 'MFA & Conditional Access'))))
    lines.append(R(merge(bMid(L1, R1, 'PKI: Enterprise CA issues certs'), bMid(L2, R2, 'Azure AD MFA per-user policy'))))
    lines.append(R(merge(bMid(L1, R1, 'Smart card logon: PIN + cert'), bMid(L2, R2, 'Duo MFA proxy on DC/RDS'))))
    lines.append(R(merge(bMid(L1, R1, 'PKINIT: Kerberos via cert'), bMid(L2, R2, 'Conditional access: compliant'))))
    lines.append(R(merge(bMid(L1, R1, 'SCEP/ACME enrollment for devices'), bMid(L2, R2, 'NPS for RADIUS 802.1x auth'))))
    lines.append(R(merge(bMid(L1, R1, 'Autoenroll via GPO certtempl'), bMid(L2, R2, 'Event 4625 lockout alerts'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Domain controller servers · HSM for CA key storage · smart card readers · NPS servers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Kerberos       = network auth protocol; ticket-based; default in AD domains since Win2000'))
    lines.append(txt_row('TGT            = Ticket-Granting Ticket; issued by KDC AS; used to request service tickets'))
    lines.append(txt_row('TGS            = Ticket-Granting Service; issues service tickets from presented TGT'))
    lines.append(txt_row('SPN            = Service Principal Name; identifies service instance for Kerberos'))
    lines.append(txt_row('NTLM           = NT LAN Manager; older challenge-response; kept for compatibility'))
    lines.append(txt_row('NTLMv2         = improved NTLM; uses HMAC-MD5; still weaker than Kerberos'))
    lines.append(txt_row('PKI            = Public Key Infrastructure; CA hierarchy issuing X.509 certificates'))
    lines.append(txt_row('PKINIT         = Kerberos extension; uses X.509 certs for initial TGT request'))
    lines.append(txt_row('NPS            = Network Policy Server; RADIUS server for 802.1x and VPN auth'))
    lines.append(txt_row('Event 4624     = successful logon audit event; includes logon type and auth package'))
    lines.append(txt_row('Event 4625     = failed logon audit event; source for lockout and brute-force alerts'))
    lines.append(txt_row('Event 4776     = NTLM authentication attempt; monitor to detect NTLM usage'))
    lines.append(txt_row('Conditional Access= Azure AD policy evaluating signals before granting resource access'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-sec-enc', 'docs/compute/windows-server/security/encryption/index.md', 'Windows Server Encryption')
def _windows_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('Encryption at rest via BitLocker/EFS; in transit via TLS 1.2/1.3, WinRM HTTPS, IPsec.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Encryption at Rest'), bMid(L2, R2, 'Encryption in Transit'))))
    lines.append(R(merge(bMid(L1, R1, 'BitLocker: full-volume AES-256'), bMid(L2, R2, 'TLS 1.2/1.3 on all services'))))
    lines.append(R(merge(bMid(L1, R1, 'TPM 2.0 seals BitLocker key'), bMid(L2, R2, 'WinRM: HTTPS only; cert bound'))))
    lines.append(R(merge(bMid(L1, R1, 'Network unlock for DC boot'), bMid(L2, R2, 'IPsec: transport mode AES'))))
    lines.append(R(merge(bMid(L1, R1, 'EFS: per-file cert-based enc'), bMid(L2, R2, 'SMB 3.x encryption enforce'))))
    lines.append(R(merge(bMid(L1, R1, 'Recovery key in AD BitLocker'), bMid(L2, R2, 'Disable SSL 3.0/TLS 1.0/1.1'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('BitLocker protects against physical theft; TLS/SMB encryption protects data in motion.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Key Management'), bMid(L2, R2, 'Protocol Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'AD MBAM for BitLocker keys'), bMid(L2, R2, 'Disable RC4, 3DES, MD5'))))
    lines.append(R(merge(bMid(L1, R1, 'PKI CA issues TLS certs'), bMid(L2, R2, 'Cipher suite: AES-GCM first'))))
    lines.append(R(merge(bMid(L1, R1, 'KMS / Azure Key Vault for apps'), bMid(L2, R2, 'SCHANNEL reg hardening GPO'))))
    lines.append(R(merge(bMid(L1, R1, 'Auto-enroll cert renewal'), bMid(L2, R2, 'IIS: TLS binding on port 443'))))
    lines.append(R(merge(bMid(L1, R1, 'HSM for CA root key protect'), bMid(L2, R2, 'RDP: TLS + NLA required'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('TPM 2.0 chip on server · HSM for CA keys · UEFI Secure Boot · SAS/NVMe storage'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('BitLocker      = Windows full-volume encryption; AES-256-XTS; TPM-protected key'))
    lines.append(txt_row('TPM            = Trusted Platform Module; hardware security chip; seals BitLocker key'))
    lines.append(txt_row('EFS            = Encrypting File System; per-file NTFS encryption using user cert'))
    lines.append(txt_row('MBAM           = Microsoft BitLocker Administration and Monitoring; key escrow to AD'))
    lines.append(txt_row('TLS 1.3        = Transport Layer Security 1.3; forward secrecy; removes legacy ciphers'))
    lines.append(txt_row('IPsec          = IP Security; encrypts/authenticates IP packets; transport or tunnel mode'))
    lines.append(txt_row('SMB encryption = SMB 3.0+ per-share or per-server AES-GCM encryption'))
    lines.append(txt_row('SCHANNEL       = Windows SSL/TLS implementation; configured via registry or GPO'))
    lines.append(txt_row('NLA            = Network Level Authentication; pre-auth for RDP; requires Kerberos/NTLM'))
    lines.append(txt_row('Cipher suite   = algorithm bundle: key exchange + auth + encryption + MAC'))
    lines.append(txt_row('AES-GCM        = Advanced Encryption Standard Galois/Counter Mode; authenticated enc'))
    lines.append(txt_row('PKI            = Public Key Infrastructure; CA hierarchy issuing X.509 certificates'))
    lines.append(txt_row('HSM            = Hardware Security Module; tamper-proof key storage for CA root keys'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-sec-hard', 'docs/compute/windows-server/security/hardening/index.md', 'Windows Server Hardening')
def _windows_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('OS hardening: CIS Benchmark baseline, GPO policies, attack surface reduction, Defender.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'OS & Service Hardening'), bMid(L2, R2, 'Attack Surface Reduction'))))
    lines.append(R(merge(bMid(L1, R1, 'CIS Benchmark L1/L2 GPOs'), bMid(L2, R2, 'Disable unused roles/features'))))
    lines.append(R(merge(bMid(L1, R1, 'STIG SCAP scan and remediate'), bMid(L2, R2, 'Close unused TCP/UDP ports'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable SMBv1, TelnetFTP,WDigest'), bMid(L2, R2, 'ASR rules: Office macro block'))))
    lines.append(R(merge(bMid(L1, R1, 'Enable Secure Boot + UEFI lock'), bMid(L2, R2, 'AppLocker/WDAC whitelist'))))
    lines.append(R(merge(bMid(L1, R1, 'Patch: patch Tuesday + OOB'), bMid(L2, R2, 'RDP: restrict to jump server'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('GPO baseline locks config; ASR rules reduce malware execution paths.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Defender & EDR'), bMid(L2, R2, 'Account Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Defender: real-time + cloud'), bMid(L2, R2, 'Rename built-in Admin acct'))))
    lines.append(R(merge(bMid(L1, R1, 'Defender ATP: EDR telemetry'), bMid(L2, R2, 'Disable Guest account'))))
    lines.append(R(merge(bMid(L1, R1, 'Tamper protection: on'), bMid(L2, R2, 'Fine-grained password policy'))))
    lines.append(R(merge(bMid(L1, R1, 'Credential Guard: LSASS in VBS'), bMid(L2, R2, 'Account lockout: 5 attempts'))))
    lines.append(R(merge(bMid(L1, R1, 'Device Guard: HVCI kernel'), bMid(L2, R2, 'LAPS for all local admins'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical server · TPM 2.0 · UEFI Secure Boot · dedicated management NIC (iDRAC/iLO)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CIS Benchmark  = Center for Internet Security; numbered controls for OS hardening'))
    lines.append(txt_row('STIG           = Security Technical Implementation Guide; DoD hardening standard'))
    lines.append(txt_row('SCAP           = Security Content Automation Protocol; machine-readable STIG scanning'))
    lines.append(txt_row('WDigest        = legacy auth provider; caches cleartext passwords in LSASS memory'))
    lines.append(txt_row('ASR            = Attack Surface Reduction rules; Defender policies blocking exploit paths'))
    lines.append(txt_row('AppLocker      = Windows policy engine; whitelist which executables/scripts can run'))
    lines.append(txt_row('WDAC           = Windows Defender Application Control; kernel code integrity policy'))
    lines.append(txt_row('Credential Guard= VBS-isolated LSASS; prevents pass-the-hash/ticket attacks'))
    lines.append(txt_row('Device Guard   = HVCI: Hypervisor-Protected Code Integrity; kernel driver validation'))
    lines.append(txt_row('HVCI           = Hypervisor Protected Code Integrity; kernel runs in VBS environment'))
    lines.append(txt_row('VBS            = Virtualisation-Based Security; Hyper-V isolates security features'))
    lines.append(txt_row('LAPS           = Local Admin Password Solution; rotates local admin passwords in AD'))
    lines.append(txt_row('Defender ATP   = Microsoft Defender for Endpoint; EDR platform with SIEM integration'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-trouble', 'docs/compute/windows-server/troubleshooting/index.md', 'Windows Server Troubleshooting Overview')
def _windows_trouble_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2, L3, R3 = 3, 33, 36, 66, 69, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Troubleshooting Overview'))
    lines.append(txt_row())
    lines.append(txt_row('Structured troubleshooting: common issues first, diagnostics second, escalation when needed.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Common Issues'), bMid(L2, R2, 'Diagnostics'), bMid(L3, R3, 'Escalation'))))
    lines.append(R(merge(bMid(L1, R1, 'Service failures + restarts'), bMid(L2, R2, 'Event Viewer: Sys+App logs'), bMid(L3, R3, 'Vendor TAC engage'))))
    lines.append(R(merge(bMid(L1, R1, 'Performance degradation'), bMid(L2, R2, 'Perfmon: counters + logs'), bMid(L3, R3, 'MS Premier support'))))
    lines.append(R(merge(bMid(L1, R1, 'AD replication errors'), bMid(L2, R2, 'WinRM test connectivity'), bMid(L3, R3, 'Dump analysis (.dmp)'))))
    lines.append(R(merge(bMid(L1, R1, 'Network connectivity loss'), bMid(L2, R2, 'netsh trace capture pkt'), bMid(L3, R3, 'Kernel debugger attach'))))
    lines.append(R(merge(bMid(L1, R1, 'Boot/BSOD failures'), bMid(L2, R2, 'WER reports analysis'), bMid(L3, R3, 'SysInternals tools'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('Start with Event Viewer and Perfmon; escalate with dump files and SysInternals traces.'))
    lines.append(txt_row())
    lines.append(R(arrow([18, 51, 84])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Log Sources'), bMid(L2, R2, 'CLI Tools'), bMid(L3, R3, 'Escalation Packs'))))
    lines.append(R(merge(bMid(L1, R1, 'System / Application log'), bMid(L2, R2, 'Get-EventLog/wevtutil'), bMid(L3, R3, 'memory.dmp (full/mini)'))))
    lines.append(R(merge(bMid(L1, R1, 'Security audit log'), bMid(L2, R2, 'netstat / tcpview'), bMid(L3, R3, 'procmon boot log'))))
    lines.append(R(merge(bMid(L1, R1, 'DNS debug log'), bMid(L2, R2, 'repadmin / dcdiag'), bMid(L3, R3, 'netsh trace ETL'))))
    lines.append(R(merge(bMid(L1, R1, 'DHCP audit log'), bMid(L2, R2, 'ipconfig / nslookup'), bMid(L3, R3, 'PsInfo + autoruns'))))
    lines.append(R(merge(bMid(L1, R1, 'Hyper-V event log'), bMid(L2, R2, 'diskmgmt + diskpart'), bMid(L3, R3, 'sfc /scannow + dism'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical or virtual server · iDRAC/iLO OOB console · crash dump storage · network tap'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Event Viewer   = MMC snap-in; shows System, Application, Security, custom logs'))
    lines.append(txt_row('Perfmon        = Performance Monitor; tracks CPU/RAM/disk/network counters over time'))
    lines.append(txt_row('WER            = Windows Error Reporting; collects crash and hang data for analysis'))
    lines.append(txt_row('netsh trace    = packet and event tracing; outputs .etl file for Network Monitor'))
    lines.append(txt_row('WinRM          = Windows Remote Management; Test-WSMan verifies connectivity'))
    lines.append(txt_row('repadmin       = AD replication diagnostics; /replsummary + /showrepl'))
    lines.append(txt_row('dcdiag         = Domain Controller diagnostic tool; tests DNS, replication, services'))
    lines.append(txt_row('SysInternals   = Microsoft tools: procmon, procexp, autoruns, pstools, tcpview'))
    lines.append(txt_row('memory.dmp     = full kernel crash dump; written to %SystemRoot% on BSOD'))
    lines.append(txt_row('BSOD           = Blue Screen of Death; kernel panic; error code in minidump'))
    lines.append(txt_row('sfc            = System File Checker; verifies and repairs protected OS files'))
    lines.append(txt_row('dism           = Deployment Image Servicing; repairs Windows component store'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-trouble-common', 'docs/compute/windows-server/troubleshooting/common-issues/index.md', 'Windows Server Common Troubleshooting')
def _windows_trouble_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Troubleshooting Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Step-by-step resolution for services, boot failures, high CPU/RAM, and network connectivity.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Service & Boot Failures'), bMid(L2, R2, 'Performance Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'sc query → sc start <svc>'), bMid(L2, R2, 'Task Manager → Details tab'))))
    lines.append(R(merge(bMid(L1, R1, 'Event 7034/7000: crash/start fail'), bMid(L2, R2, 'CPU: top process + call stack'))))
    lines.append(R(merge(bMid(L1, R1, 'Dependency check: sc qc <svc>'), bMid(L2, R2, 'RAM: pool monitor; poolmon'))))
    lines.append(R(merge(bMid(L1, R1, 'BSOD: check minidump + !analyze'), bMid(L2, R2, 'Disk: diskperf; latency > 20ms'))))
    lines.append(R(merge(bMid(L1, R1, 'Boot: bcdedit; recovery console'), bMid(L2, R2, 'Handle/thread leak: procexp'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Service and boot failures resolved via sc tools and event logs; perf via Perfmon/procexp.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network & DNS Issues'), bMid(L2, R2, 'AD & Authentication Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'ipconfig /flushdns + /renew'), bMid(L2, R2, 'klist purge; re-request TGT'))))
    lines.append(R(merge(bMid(L1, R1, 'nslookup to test DNS records'), bMid(L2, R2, 'nltest /sc_verify:domain'))))
    lines.append(R(merge(bMid(L1, R1, 'netsh int ip reset + Winsock'), bMid(L2, R2, 'repadmin /syncall /Ade'))))
    lines.append(R(merge(bMid(L1, R1, 'Test-NetConnection port check'), bMid(L2, R2, 'w32tm /resync for clock skew'))))
    lines.append(R(merge(bMid(L1, R1, 'netstat -ano: port conflicts'), bMid(L2, R2, 'gpupdate /force; gpresult /h'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical or virtual server · NIC ports · iDRAC/iLO OOB · domain controller network path'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('sc             = Service Control CLI; query, start, stop, configure Windows services'))
    lines.append(txt_row('Event 7034     = service terminated unexpectedly; maps to specific service crash'))
    lines.append(txt_row('bcdedit        = Boot Configuration Data editor; modify boot entries and flags'))
    lines.append(txt_row('!analyze       = WinDbg command; auto-analyses crash dump for root cause'))
    lines.append(txt_row('poolmon        = kernel pool monitor; detects pool tag memory leaks'))
    lines.append(txt_row('diskperf       = enables disk performance counters; required for Perfmon disk stats'))
    lines.append(txt_row('klist          = Kerberos ticket list; purge clears cached tickets for re-auth'))
    lines.append(txt_row('nltest         = network logon test; /sc_verify checks secure channel to DC'))
    lines.append(txt_row('w32tm          = Windows Time service tool; /resync forces NTP re-synchronisation'))
    lines.append(txt_row('repadmin       = AD replication admin; /syncall forces replication from all partners'))
    lines.append(txt_row('gpupdate       = Group Policy update; /force reapplies all policies immediately'))
    lines.append(txt_row('Test-NetConnection= PS cmdlet testing TCP port connectivity and route tracing'))
    lines.append(txt_row('procexp        = SysInternals Process Explorer; shows handles, threads, DLLs per process'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-trouble-diag', 'docs/compute/windows-server/troubleshooting/diagnostics/index.md', 'Windows Server Diagnostics')
def _windows_trouble_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('Diagnostics: event log analysis, performance data collection, network traces, memory dumps.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Event Log Analysis'), bMid(L2, R2, 'Performance Data Collection'))))
    lines.append(R(merge(bMid(L1, R1, 'wevtutil qe System /count:50'), bMid(L2, R2, 'Perfmon: data collector sets'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-WinEvent filter hash table'), bMid(L2, R2, 'typeperf: counter to CSV'))))
    lines.append(R(merge(bMid(L1, R1, 'Subscriptions: WEF centralise'), bMid(L2, R2, 'PAL: Perf Analysis of Logs'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom views: by error level'), bMid(L2, R2, 'Resource Monitor: real-time'))))
    lines.append(R(merge(bMid(L1, R1, 'Export: evtx for offline'), bMid(L2, R2, 'Process Monitor: file+reg+net'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Event logs show what happened; Perfmon and procmon show how the system behaved.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network Diagnostics'), bMid(L2, R2, 'Memory & Crash Diagnostics'))))
    lines.append(R(merge(bMid(L1, R1, 'netsh trace start capture'), bMid(L2, R2, 'Task Manager: commit charge'))))
    lines.append(R(merge(bMid(L1, R1, 'Wireshark: .etl to .pcap'), bMid(L2, R2, 'Poolmon: tag leak detection'))))
    lines.append(R(merge(bMid(L1, R1, 'netstat -anob: PID per port'), bMid(L2, R2, 'WinDbg: !analyze -v crash'))))
    lines.append(R(merge(bMid(L1, R1, 'tracert + pathping latency'), bMid(L2, R2, 'procdump -ma <PID> dump'))))
    lines.append(R(merge(bMid(L1, R1, 'PortQry: remote port scan'), bMid(L2, R2, 'MDSN for WER online search'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical or virtual server · NIC for packet capture · dump storage disk · OOB console'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('wevtutil       = Windows Event Utility; CLI query, export, and clear event logs'))
    lines.append(txt_row('Get-WinEvent   = PowerShell cmdlet; powerful filter-hash queries across event logs'))
    lines.append(txt_row('WEF            = Windows Event Forwarding; aggregates events to a central collector'))
    lines.append(txt_row('Perfmon        = Performance Monitor; records counters to BLG/CSV/SQL data sets'))
    lines.append(txt_row('typeperf       = CLI perfmon; writes counter data to CSV for offline analysis'))
    lines.append(txt_row('PAL            = Performance Analysis of Logs; analyses BLG files against thresholds'))
    lines.append(txt_row('Resource Monitor= real-time view of CPU/RAM/disk/network per process'))
    lines.append(txt_row('procmon        = SysInternals Process Monitor; captures file, registry, network events'))
    lines.append(txt_row('netsh trace    = built-in packet capture; outputs ETL for Message Analyser / Wireshark'))
    lines.append(txt_row('poolmon        = kernel pool monitor; detects memory tag leaks in driver pool'))
    lines.append(txt_row('WinDbg         = Windows Debugger; analyses crash dumps; !analyze -v auto-diagnoses'))
    lines.append(txt_row('procdump       = SysInternals; captures process memory dump for hang/crash analysis'))
    lines.append(txt_row('PortQry        = Microsoft port connectivity scanner; tests TCP/UDP port accessibility'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('windows-trouble-esc', 'docs/compute/windows-server/troubleshooting/escalation/index.md', 'Windows Server Escalation')
def _windows_trouble_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Windows Server — Troubleshooting Escalation'))
    lines.append(txt_row())
    lines.append(txt_row('Escalation path: internal L2/L3 → Microsoft Premier/TAC → CSS with diagnostic bundle.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Internal Escalation Path'), bMid(L2, R2, 'Microsoft Support Escalation'))))
    lines.append(R(merge(bMid(L1, R1, 'L1 → L2: event logs + timeline'), bMid(L2, R2, 'Open MS Support case online'))))
    lines.append(R(merge(bMid(L1, R1, 'L2 → L3: attach dump + procmon'), bMid(L2, R2, 'Premier: SfMC / DSE assign'))))
    lines.append(R(merge(bMid(L1, R1, 'L3 → Vendor: full diag bundle'), bMid(L2, R2, 'CSS: case + severity rating'))))
    lines.append(R(merge(bMid(L1, R1, 'Incident commander for Sev-1'), bMid(L2, R2, 'Share: SDP (Support Diag Pkg)'))))
    lines.append(R(merge(bMid(L1, R1, 'Bridge call + screen share'), bMid(L2, R2, 'Remote: MSRA or DART tool'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Internal triage first; escalate to Microsoft with a complete diagnostic data package.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Diagnostic Bundle Contents'), bMid(L2, R2, 'Escalation Criteria'))))
    lines.append(R(merge(bMid(L1, R1, 'Event logs: evtx all channels'), bMid(L2, R2, 'Sev-A: production down now'))))
    lines.append(R(merge(bMid(L1, R1, 'memory.dmp (full kernel dump)'), bMid(L2, R2, 'Sev-B: degraded production'))))
    lines.append(R(merge(bMid(L1, R1, 'Perfmon BLG: 72h before issue'), bMid(L2, R2, 'Sev-C: non-critical impact'))))
    lines.append(R(merge(bMid(L1, R1, 'netsh trace ETL during issue'), bMid(L2, R2, 'Sev-D: general question'))))
    lines.append(R(merge(bMid(L1, R1, 'msinfo32 /nfo sysinfo file'), bMid(L2, R2, 'CSAT after case closed'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical or virtual server · OOB console · network path to Microsoft CSS upload endpoint'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SDP            = Support Diagnostic Package; Microsoft data collection script bundle'))
    lines.append(txt_row('CSS            = Customer Support Services; Microsoft front-line support organisation'))
    lines.append(txt_row('Premier        = Microsoft Premier Support; dedicated TAM and faster SLA'))
    lines.append(txt_row('DSE            = Delivery Service Engineer; Microsoft Premier on-site or remote engineer'))
    lines.append(txt_row('SfMC           = Support for Microsoft Cloud; specialist cloud support tier'))
    lines.append(txt_row('Severity A/B/C/D= Microsoft case severity; A = production down, D = informational'))
    lines.append(txt_row('MSRA           = Microsoft Remote Assistance; remote session for support engineer'))
    lines.append(txt_row('DART           = Diagnostics and Recovery Toolset; bootable WinPE recovery kit'))
    lines.append(txt_row('msinfo32       = System Information utility; exports full hardware/software snapshot'))
    lines.append(txt_row('memory.dmp     = full kernel crash dump; written on BSOD to SystemRoot'))
    lines.append(txt_row('procmon        = SysInternals Process Monitor; captures all I/O for escalation bundle'))
    lines.append(txt_row('BLG            = binary performance log; Perfmon native format for counter data'))
    lines.append(txt_row('CSAT           = Customer Satisfaction survey; sent after Microsoft case closure'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines
