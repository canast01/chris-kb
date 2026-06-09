"""
PowerCLI diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

# ── PowerCLI Root ────────────────────────────────────────────────────────────

@kb_diagram(
    'powercli',
    'docs/virtualization/vmware/powercli/index.md',
    'PowerCLI Overview — modules, connection model, API binding, use cases',
)
def powercli_root():
    """PowerCLI Platform Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    B3_L, B3_R = 3, 50
    B4_L, B4_R = 53, 99

    lines = []
    lines.append(title_border(W2, 'VMware PowerCLI Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware PowerCLI — PowerShell module suite for vSphere automation')))
    lines.append(R(bMid(IV_L, IV_R, 'Built on top of the vSphere SOAP/REST APIs — same calls as vCenter UI')))
    lines.append(R(bMid(IV_L, IV_R, 'Platform: PowerShell 7+ (cross-platform) or Windows PowerShell 5.1')))
    lines.append(R(bMid(IV_L, IV_R, 'Install: Install-Module VMware.PowerCLI from PSGallery; 40+ sub-modules')))
    lines.append(R(bMid(IV_L, IV_R, 'Session: Connect-VIServer -> $global:DefaultVIServer -> all cmdlets use it')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())

    lines.append(R(bTop(B1_L, B1_R)))
    lines.append(R(bMid(B1_L, B1_R, 'Core Modules')))
    lines.append(R(bMid(B1_L, B1_R, 'VimAutomation.Core  VM + host + cluster')))
    lines.append(R(bMid(B1_L, B1_R, 'VimAutomation.Vds   vDS + portgroups')))
    lines.append(R(bMid(B1_L, B1_R, 'VimAutomation.Storage  VMDK + datastores')))
    lines.append(R(bMid(B1_L, B1_R, 'VimAutomation.Nsxt  NSX-T policy objects')))
    lines.append(R(bBot(B1_L, B1_R)))

    lines.append(R(bTop(B2_L, B2_R)))
    lines.append(R(bMid(B2_L, B2_R, 'Add-on Modules')))
    lines.append(R(bMid(B2_L, B2_R, 'VimAutomation.Srm   SRM recovery plans')))
    lines.append(R(bMid(B2_L, B2_R, 'VimAutomation.Hcx   HCX migration')))
    lines.append(R(bMid(B2_L, B2_R, 'VimAutomation.Horizon  Horizon VDI')))
    lines.append(R(bMid(B2_L, B2_R, 'VimAutomation.vROps  Aria Operations')))
    lines.append(R(bBot(B2_L, B2_R)))
    lines.append(txt_row())

    lines.append(R(bTop(B3_L, B3_R)))
    lines.append(R(bMid(B3_L, B3_R, 'Connection Model')))
    lines.append(R(bMid(B3_L, B3_R, 'Connect-VIServer -Server <FQDN>')))
    lines.append(R(bMid(B3_L, B3_R, '  -> SSO token from vCenter')))
    lines.append(R(bMid(B3_L, B3_R, '  -> $global:DefaultVIServer set')))
    lines.append(R(bMid(B3_L, B3_R, '  -> All cmdlets use this implicitly')))
    lines.append(R(bBot(B3_L, B3_R)))

    lines.append(R(bTop(B4_L, B4_R)))
    lines.append(R(bMid(B4_L, B4_R, 'API Binding')))
    lines.append(R(bMid(B4_L, B4_R, 'High-level: Get-VM -> VI objects')))
    lines.append(R(bMid(B4_L, B4_R, 'Low-level: Get-View -> raw vSphere API')))
    lines.append(R(bMid(B4_L, B4_R, 'View objects: faster, no wrappers')))
    lines.append(R(bMid(B4_L, B4_R, 'ExtensionData: .NET SDK access')))
    lines.append(R(bBot(B4_L, B4_R)))
    lines.append(txt_row())

    lines.append(txt_row('Physical Infrastructure: Windows/Linux jump host with PowerShell 7+ installed'))
    lines.append(txt_row('Network: HTTPS/443 to vCenter FQDN  ·  DNS resolution required'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VI Object    = high-level wrapper (Get-VM, Get-VMHost) with helper properties'))
    lines.append(txt_row('View Object  = raw vSphere API object; faster but no helper properties'))
    lines.append(txt_row('SOAP API     = vSphere legacy API (port 443 /sdk); used by most cmdlets'))
    lines.append(txt_row('REST API     = vSphere modern API; used by newer NSX/vSAN cmdlets'))
    lines.append(txt_row('SSO Token    = session credential; valid 8 h by default; auto-renewed'))
    lines.append(txt_row('PSGallery    = PowerShell module repository; source for Install-Module'))
    lines.append(txt_row('DefaultVIServer = implicit connection target for all cmdlets in session'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')

    return lines


# ── PowerCLI Operations ──────────────────────────────────────────────────────

@kb_diagram(
    'powercli-operations',
    'docs/virtualization/vmware/powercli/operations/cli-reference/index.md',
    'PowerCLI operations — cmdlet categories and vSphere object hierarchy',
)
def powercli_operations():
    """PowerCLI Operations Reference — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 32
    B2_L, B2_R = 35, 65
    B3_L, B3_R = 68, 99

    lines = []
    lines.append(title_border(W2, 'PowerCLI — vSphere Object Hierarchy and Cmdlet Categories'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vSphere Inventory Hierarchy (top to bottom)')))
    lines.append(R(bMid(IV_L, IV_R, 'vCenter -> Datacenter -> Cluster -> ESXi Host -> VM / Resource Pool')))
    lines.append(R(bMid(IV_L, IV_R, 'vCenter -> Datacenter -> Datastore / Network -> VM')))
    lines.append(R(bMid(IV_L, IV_R, 'Use -Location to scope: Get-VM -Location (Get-Cluster "Prod")')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())

    lines.append(R(bTop(B1_L, B1_R)))
    lines.append(R(bMid(B1_L, B1_R, 'Compute Cmdlets')))
    lines.append(R(bMid(B1_L, B1_R, 'Get-VM / Set-VM')))
    lines.append(R(bMid(B1_L, B1_R, 'New-VM / Remove-VM')))
    lines.append(R(bMid(B1_L, B1_R, 'Start/Stop/Restart-VM')))
    lines.append(R(bMid(B1_L, B1_R, 'Move-VM (vMotion)')))
    lines.append(R(bMid(B1_L, B1_R, 'Get-VMHost / Set-VMHost')))
    lines.append(R(bMid(B1_L, B1_R, 'Get-Cluster / Set-Cluster')))
    lines.append(R(bBot(B1_L, B1_R)))

    lines.append(R(bTop(B2_L, B2_R)))
    lines.append(R(bMid(B2_L, B2_R, 'Storage Cmdlets')))
    lines.append(R(bMid(B2_L, B2_R, 'Get-Datastore')))
    lines.append(R(bMid(B2_L, B2_R, 'Get-HardDisk / Set-HardDisk')))
    lines.append(R(bMid(B2_L, B2_R, 'Get-Snapshot / New-Snapshot')))
    lines.append(R(bMid(B2_L, B2_R, 'Remove-Snapshot')))
    lines.append(R(bMid(B2_L, B2_R, 'Get-VsanDisk')))
    lines.append(R(bMid(B2_L, B2_R, 'Get-VsanClusterHealthSummary')))
    lines.append(R(bBot(B2_L, B2_R)))

    lines.append(R(bTop(B3_L, B3_R)))
    lines.append(R(bMid(B3_L, B3_R, 'Management Cmdlets')))
    lines.append(R(bMid(B3_L, B3_R, 'Get-VIPermission')))
    lines.append(R(bMid(B3_L, B3_R, 'New-VIPermission')))
    lines.append(R(bMid(B3_L, B3_R, 'Get-VIRole / New-VIRole')))
    lines.append(R(bMid(B3_L, B3_R, 'Get-Tag / New-Tag')))
    lines.append(R(bMid(B3_L, B3_R, 'Get-VIEvent')))
    lines.append(R(bMid(B3_L, B3_R, 'Get-View (raw API)')))
    lines.append(R(bBot(B3_L, B3_R)))
    lines.append(txt_row())

    lines.append(txt_row('Physical Infrastructure: management workstation or automation server running PowerShell 7+'))
    lines.append(txt_row('Network path: jump host -> HTTPS/443 -> vCenter FQDN -> vSphere API endpoint'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Pipeline      = PowerShell pipe; Get-VM | Get-Snapshot chains cmdlets'))
    lines.append(txt_row('Where-Object  = filter items in a pipeline by property value'))
    lines.append(txt_row('Select-Object = choose which properties to display or export'))
    lines.append(txt_row('ForEach-Object = iterate over each item in the pipeline'))
    lines.append(txt_row('Export-Csv    = write pipeline output to CSV file'))
    lines.append(txt_row('Format-Table  = render properties as columns in the console'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')

    return lines
