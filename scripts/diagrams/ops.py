"""
Operational runbooks, change management, lifecycle, and cross-platform troubleshooting.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import kb_diagram, make_helpers, bTop, bMid, bBot, sections, arrow, connector, merge, title_border, row

# ── Runbooks ──────────────────────────────────────────────────────────────────

@kb_diagram(
    'runbooks',
    'docs/runbooks/index.md',
    'Runbooks landing — operational procedures for infrastructure tasks',
)
def runbooks_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []

    lines.append(title_border(W2, 'Runbooks — Operational Procedures'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Runbooks: step-by-step operational procedures for common infrastructure tasks')))
    lines.append(R(bMid(IV_L, IV_R, 'Each runbook: pre-checks → steps → validation → rollback path → close-out')))
    lines.append(R(bMid(IV_L, IV_R, 'Run all runbooks under a change ticket; document start/end time and outcome')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Request arrives → identify runbook → raise change ticket → execute → validate → close'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Access / Identity'), bMid(B2_L, B2_R, 'Infrastructure'), bMid(B3_L, B3_R, 'Storage / VMs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Account unlock'), bMid(B2_L, B2_R, 'Server reboot'), bMid(B3_L, B3_R, 'Volume expansion'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Certificate renewal'), bMid(B2_L, B2_R, 'Service restart'), bMid(B3_L, B3_R, 'VM snapshot'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Password reset'), bMid(B2_L, B2_R, 'Disk cleanup'), bMid(B3_L, B3_R, 'Snapshot delete'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Group membership'), bMid(B2_L, B2_R, 'Log rotation'), bMid(B3_L, B3_R, 'LUN expansion'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SSO token reset'), bMid(B2_L, B2_R, 'NTP fix'), bMid(B3_L, B3_R, 'Datastore extend'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Runbook     = Documented procedure with explicit steps; reduces error rate in ops tasks'))
    lines.append(txt_row('  Pre-checks  = Verify system state is safe to proceed before any change'))
    lines.append(txt_row('  Validation  = Post-execution verification that the task succeeded as expected'))
    lines.append(txt_row('  Rollback    = Steps to undo the change if validation fails; always plan before executing'))
    lines.append(txt_row('  Change ticket= Every runbook execution linked to a change request for auditability'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'rb-account-unlock',
    'docs/runbooks/account-unlock/index.md',
    'Account unlock runbook — AD lockout, password reset, lockout source investigation',
)
def rb_account_unlock():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Runbook — Account Unlock'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Unlock AD account; identify lockout source; prevent re-lock before fix')))
    lines.append(R(bMid(IV_L, IV_R, 'Pre-check: confirm account is locked; find lockout source DC and application')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identify Lockout Source'), bMid(B2_L, B2_R, 'Unlock Steps'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check Security Event Log (4740)'), bMid(B2_L, B2_R, 'ADUC: right-click → Unlock'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Use LockoutStatus.exe tool'), bMid(B2_L, B2_R, 'PowerShell: Unlock-ADAccount'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Find PDC emulator for events'), bMid(B2_L, B2_R, 'Reset password if unknown'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Caller workstation in event'), bMid(B2_L, B2_R, 'Clear cached creds on device'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service account = check services'), bMid(B2_L, B2_R, 'Update service/app creds'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, '# PowerShell — unlock and check')))
    lines.append(R(bMid(IV_L, IV_R, 'Get-ADUser <user> -Properties LockedOut,BadLogonCount | Select Name,LockedOut')))
    lines.append(R(bMid(IV_L, IV_R, 'Unlock-ADAccount -Identity <user>')))
    lines.append(R(bMid(IV_L, IV_R, 'Search-ADAccount -LockedOut | Select Name,LockedOut,PasswordExpired')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Step', 'Action', 'Command/tool', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Confirm lock', 'Check state', 'Get-ADUser', 'LockedOut=True', 'Before unlock'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Find source', 'Event 4740', 'LockoutStatus', 'Caller found', 'PDC emulator'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Unlock', 'Unlock acct', 'Unlock-ADAccount', 'LockedOut=False', 'Sync all DCs'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Fix cause', 'Clear creds', 'Device/service', 'No re-lock', 'Test login'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Event 4740     = Windows Security Event: account was locked out; caller and workstation noted'))
    lines.append(txt_row('  PDC emulator   = FSMO role; receives lockout events fastest; check Security log here first'))
    lines.append(txt_row('  LockoutStatus  = Microsoft tool; shows bad password count and lockout status per DC'))
    lines.append(txt_row('  Cached creds   = Windows stores last-used credentials; stale cached cred causes re-lock'))
    lines.append(txt_row('  Service account= Non-interactive account; lockout = service failing; update credential source'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'rb-cert-renewal',
    'docs/runbooks/certificate-renewal/index.md',
    'Certificate renewal runbook — SSL/TLS expiry, CSR, CA sign, deploy, verify',
)
def rb_cert_renewal():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    lines = []

    lines.append(title_border(W2, 'Runbook — Certificate Renewal'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Renew SSL/TLS certificates before expiry; update all consumers; verify chain')))
    lines.append(R(bMid(IV_L, IV_R, 'Timeline: start 30+ days before expiry; verify deployment before old cert expires')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Step 1 — Identify expiring certificates (< 30 days)')))
    lines.append(R(bMid(IV_L, IV_R, '  openssl s_client -connect <host>:443 | openssl x509 -noout -dates')))
    lines.append(R(bMid(IV_L, IV_R, '  Venafi / cert inventory report for < 30-day expiry')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 2 — Generate CSR (or use ACME/Venafi auto)')))
    lines.append(R(bMid(IV_L, IV_R, '  openssl req -new -key server.key -out server.csr -subj "/CN=<fqdn>"')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 3 — Submit to CA; download signed certificate + chain')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 4 — Install new certificate on service (nginx/IIS/appliance GUI)')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 5 — Verify: openssl verify -CAfile chain.pem cert.pem')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 6 — Test all consumers (browser, API clients, backup agents)')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 7 — Update Venafi/CMDB with new expiry; close change ticket')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, '# Check cert expiry on all hosts from inventory')))
    lines.append(R(bMid(IV_L, IV_R, 'for HOST in "${HOSTS[@]}"; do')))
    lines.append(R(bMid(IV_L, IV_R, '  EXPIRY=$(echo | openssl s_client -connect $HOST:443 2>/dev/null \\')))
    lines.append(R(bMid(IV_L, IV_R, '    | openssl x509 -noout -enddate 2>/dev/null)')))
    lines.append(R(bMid(IV_L, IV_R, '  echo "$HOST: $EXPIRY"; done')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  CSR          = Certificate Signing Request; includes public key and subject; sent to CA'))
    lines.append(txt_row('  Chain        = CA certificate chain (intermediate + root) required for full trust validation'))
    lines.append(txt_row('  ACME         = Automated cert issuance protocol (Let\'s Encrypt, Venafi, etc.); 90-day auto-renew'))
    lines.append(txt_row('  SAN          = Subject Alternative Name; include all FQDNs/IPs the cert covers'))
    lines.append(txt_row('  Venafi       = Enterprise cert lifecycle management; tracks expiry and automates renewal'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'rb-disk-cleanup',
    'docs/runbooks/disk-space-cleanup/index.md',
    'Disk space cleanup runbook — identify large files, logs, snapshots, temp cleanup',
)
def rb_disk_cleanup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []

    lines.append(title_border(W2, 'Runbook — Disk Space Cleanup'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Free disk space: identify large files, clear logs/temp, delete old snapshots')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert threshold: > 80% full; critical > 90%; action required before writes fail')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Linux'), bMid(B2_L, B2_R, 'Windows'), bMid(B3_L, B3_R, 'VMware'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'df -h / lsblk'), bMid(B2_L, B2_R, 'WinDirStat / DU'), bMid(B3_L, B3_R, 'Datastore report'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'du -sh /* | sort -rh'), bMid(B2_L, B2_R, 'C:\\Windows\\Temp'), bMid(B3_L, B3_R, 'Delete snapshots'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'journalctl --vacuum'), bMid(B2_L, B2_R, 'Disk Cleanup util'), bMid(B3_L, B3_R, 'Remove ISOs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'find /tmp -mtime +7'), bMid(B2_L, B2_R, 'C:\\Logs rotate'), bMid(B3_L, B3_R, 'Thin provision'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'logrotate -f'), bMid(B2_L, B2_R, 'WER dumps delete'), bMid(B3_L, B3_R, 'Storage vMotion'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, '# Linux: find top 10 largest directories')))
    lines.append(R(bMid(IV_L, IV_R, 'du -ah / --max-depth=3 2>/dev/null | sort -rh | head -10')))
    lines.append(R(bMid(IV_L, IV_R, '# Clear journal logs older than 7 days')))
    lines.append(R(bMid(IV_L, IV_R, 'journalctl --vacuum-time=7d')))
    lines.append(R(bMid(IV_L, IV_R, '# Find core dumps')))
    lines.append(R(bMid(IV_L, IV_R, 'find /var/core /tmp -name "core.*" -mtime +1 -ls')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  journalctl vacuum= Deletes old systemd journal logs; use --vacuum-time or --vacuum-size'))
    lines.append(txt_row('  WER dumps        = Windows Error Reporting crash dumps in C:\\ProgramData\\Microsoft\\Windows\\WER'))
    lines.append(txt_row('  Snapshot cleanup = Old VM snapshots accumulate delta VMDKs; delete via vCenter snapshot manager'))
    lines.append(txt_row('  Thin provision   = Reclaim unused blocks on thin-provisioned VMDK via Storage vMotion'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'rb-server-reboot',
    'docs/runbooks/server-reboot/index.md',
    'Server reboot runbook — pre-checks, graceful shutdown, post-reboot validation',
)
def rb_server_reboot():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Runbook — Server Reboot'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Safe server reboot: pre-checks → drain connections → shutdown → boot → validate')))
    lines.append(R(bMid(IV_L, IV_R, 'Never reboot production without change ticket; notify stakeholders beforehand')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pre-Reboot Checks'), bMid(B2_L, B2_R, 'Post-Reboot Checks'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No active backup jobs'), bMid(B2_L, B2_R, 'Server responds to ping'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No running migrations'), bMid(B2_L, B2_R, 'All services started'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Quiesce cluster resources'), bMid(B2_L, B2_R, 'Filesystems mounted clean'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Notify stakeholders'), bMid(B2_L, B2_R, 'No new alerts/errors'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confirm IPMI/iLO access'), bMid(B2_L, B2_R, 'Application health confirmed'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Step', 'Linux', 'Windows', 'VMware', 'Verify'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Drain', 'Stop services', 'Stop services', 'vMotion VMs', 'Confirmed idle'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Reboot', 'shutdown -r', 'Restart-Computer', 'Maint mode', 'Console OK'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Wait', 'Ping + SSH', 'Ping + RDP', 'Maint exit', 'Login OK'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Validate', 'systemctl status', 'Services check', 'VMs running', 'App healthy'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  IPMI/iLO  = Out-of-band management; use for console if OS becomes unresponsive post-reboot'))
    lines.append(txt_row('  Drain     = Gracefully remove load before shutdown; prevents in-flight request errors'))
    lines.append(txt_row('  Maint mode= ESXi maintenance mode; vMotion VMs off host before hardware reboot'))
    lines.append(txt_row('  Quiesce   = Cluster: move resources to peer node; HA group: disable before reboot'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'rb-service-restart',
    'docs/runbooks/service-restart/index.md',
    'Service restart runbook — dependency order, graceful restart, post-restart validation',
)
def rb_service_restart():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []

    lines.append(title_border(W2, 'Runbook — Service Restart'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Restart services in dependency order; verify each layer before proceeding')))
    lines.append(R(bMid(IV_L, IV_R, 'Always stop dependants first; start dependencies first on the way back up')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Linux (systemctl)'), bMid(B2_L, B2_R, 'Windows (PowerShell)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'systemctl status <svc>'), bMid(B2_L, B2_R, 'Get-Service <svc>'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'systemctl stop <svc>'), bMid(B2_L, B2_R, 'Stop-Service <svc>'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'systemctl start <svc>'), bMid(B2_L, B2_R, 'Start-Service <svc>'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'systemctl restart <svc>'), bMid(B2_L, B2_R, 'Restart-Service <svc>'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'journalctl -u <svc> -f'), bMid(B2_L, B2_R, 'Get-EventLog -LogName App'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Order for dependent stack restart:')))
    lines.append(R(bMid(IV_L, IV_R, '  STOP:  app-tier → middleware → database → storage-mount')))
    lines.append(R(bMid(IV_L, IV_R, '  START: storage-mount → database → middleware → app-tier')))
    lines.append(R(bMid(IV_L, IV_R, 'Verify each layer healthy before starting the next layer up')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Dependency order= Services depend on each other; wrong stop/start order causes cascading fails'))
    lines.append(txt_row('  Graceful stop   = SIGTERM before SIGKILL; lets service flush buffers and close connections'))
    lines.append(txt_row('  journalctl -f   = Follow live service log; monitor for errors during restart'))
    lines.append(txt_row('  Health check    = HTTP endpoint or service-level test confirming service is accepting traffic'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'rb-vol-expand',
    'docs/runbooks/storage-volume-expansion/index.md',
    'Storage volume expansion runbook — LUN expand, filesystem grow, no downtime',
)
def rb_vol_expand():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Runbook — Storage Volume Expansion'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Expand storage: grow array LUN → OS rescans → extend filesystem — all online')))
    lines.append(R(bMid(IV_L, IV_R, 'Pre-check: snapshot before expansion; confirm free pool capacity on array')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, '1. Array'), bMid(B2_L, B2_R, '2. OS rescan'), bMid(B3_L, B3_R, '3. FS extend'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Expand LUN/vol'), bMid(B2_L, B2_R, 'Linux: rescan-scsi'), bMid(B3_L, B3_R, 'Linux: resize2fs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify pool free'), bMid(B2_L, B2_R, 'Windows: DiskMgmt'), bMid(B3_L, B3_R, 'Windows: Extend'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confirm new size'), bMid(B2_L, B2_R, 'lsblk / diskpart'), bMid(B3_L, B3_R, 'pvresize + lvextend'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Array CLI/GUI'), bMid(B2_L, B2_R, 'ESXi: rescan HBAs'), bMid(B3_L, B3_R, 'df -h verify'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snapshot first'), bMid(B2_L, B2_R, 'Multipath update'), bMid(B3_L, B3_R, 'xfs_growfs for XFS'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['FS type', 'Grow command', 'Partition needed', 'Online?', 'Verify'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['ext4', 'resize2fs /dev/X', 'growpart first', 'Yes', 'df -h'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['XFS', 'xfs_growfs /mnt', 'growpart first', 'Yes', 'df -h'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['LVM', 'lvextend + resize', 'PV extend first', 'Yes', 'lvdisplay'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['NTFS', 'Extend Volume', 'DiskMgmt', 'Yes', 'Explorer'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  rescan-scsi-bus= Script to trigger OS rescan after LUN resize; alternative: echo 1 > /sys/...'))
    lines.append(txt_row('  growpart       = Extends a partition within a disk; required before online FS extend'))
    lines.append(txt_row('  pvresize       = LVM: expands physical volume to use new LUN capacity'))
    lines.append(txt_row('  lvextend -r    = LVM: extends logical volume and resizes filesystem in one step'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'rb-vm-snapshot',
    'docs/runbooks/vm-snapshot/index.md',
    'VM snapshot runbook — create, manage, delete, snapshot best practices',
)
def rb_vm_snapshot():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Runbook — VM Snapshot'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VM snapshots capture state for short-term rollback; NOT a backup solution')))
    lines.append(R(bMid(IV_L, IV_R, 'Delete snapshots within 24–72 hours; older snapshots degrade VM performance')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Create Snapshot'), bMid(B2_L, B2_R, 'Delete Snapshot'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confirm VM not in snapshot'), bMid(B2_L, B2_R, 'Verify change succeeded'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Quiesce filesystem (VMware tools)'), bMid(B2_L, B2_R, 'Delete via Snapshot Mgr'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Name: CHG-XXXXX-pre-change'), bMid(B2_L, B2_R, '"Delete All" commits deltas'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Note creation time'), bMid(B2_L, B2_R, 'Monitor datastore space'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Max 1 snapshot in change'), bMid(B2_L, B2_R, 'Confirm space reclaimed'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Action', 'vSphere GUI', 'PowerCLI', 'Limit', 'Risk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Create', 'Actions > Snapshot', 'New-Snapshot', '1 per change', 'Delta growth'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['List', 'Snapshot Mgr', 'Get-Snapshot', '—', '—'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Delete', 'Delete in Mgr', 'Remove-Snapshot', 'Delete all', 'Consolidation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Revert', 'Revert to snap', 'Set-VM -Snapshot', 'Loss of data', 'Irreversible'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Delta VMDK   = Snapshot child disk capturing writes after snapshot; grows until deleted'))
    lines.append(txt_row('  Quiesce      = VMware Tools flushes guest FS buffers; ensures consistent snapshot state'))
    lines.append(txt_row('  Consolidation= vCenter merges delta disks back into base on snapshot delete'))
    lines.append(txt_row('  Snapshot stun= Momentary IO pause during snapshot create/delete; worse with large VMs'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Change Management ─────────────────────────────────────────────────────────

@kb_diagram(
    'change-management',
    'docs/change-management/index.md',
    'Change management landing — ITIL change process, CAB, types, workflow',
)
def change_management_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Change Management'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Change management: structured process to control IT changes and minimise risk')))
    lines.append(R(bMid(IV_L, IV_R, 'Types: Standard (pre-approved), Normal (CAB review), Emergency (expedited)')))
    lines.append(R(bMid(IV_L, IV_R, 'ITIL framework: RFC → assessment → approval → implementation → review → close')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  RFC raised → assessed → CAB reviewed → approved → scheduled → executed → closed'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Standard Change'), bMid(B2_L, B2_R, 'Normal Change'), bMid(B3_L, B3_R, 'Emergency Change'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pre-approved'), bMid(B2_L, B2_R, 'CAB review'), bMid(B3_L, B3_R, 'ECAB or on-call'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Low risk'), bMid(B2_L, B2_R, 'Risk assessment'), bMid(B3_L, B3_R, 'P1 fix only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Documented template'), bMid(B2_L, B2_R, 'Backout plan req'), bMid(B3_L, B3_R, 'Retrospective req'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No CAB needed'), bMid(B2_L, B2_R, 'Scheduled window'), bMid(B3_L, B3_R, 'Immediate exec'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'e.g. patching'), bMid(B2_L, B2_R, 'e.g. upgrade'), bMid(B3_L, B3_R, 'e.g. P1 fix'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Phase', 'Activity', 'Owner', 'Artefact', 'Gate'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Raise', 'RFC creation', 'Requestor', 'RFC form', 'Completeness'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Assess', 'Risk + impact', 'Change mgr', 'Risk matrix', 'Assessment'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Approve', 'CAB vote', 'CAB', 'Approval rec', 'Approved status'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Close', 'PIR/review', 'Change mgr', 'Closure note', 'Success/fail'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  RFC    = Request for Change; formal document describing the change and its rationale'))
    lines.append(txt_row('  CAB    = Change Advisory Board; reviews normal changes; approves or rejects'))
    lines.append(txt_row('  ECAB   = Emergency CAB; subset of CAB for expedited emergency change approval'))
    lines.append(txt_row('  PIR    = Post-Implementation Review; assesses whether change met objectives'))
    lines.append(txt_row('  Backout= Rollback plan; must be documented before every normal/emergency change'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cm-approval',
    'docs/change-management/change-approval/index.md',
    'Change approval — CAB submission, risk matrix, approval workflow, sign-off',
)
def cm_approval():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Change Approval'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Change approval: RFC submitted to CAB with risk matrix, impact, and backout plan')))
    lines.append(R(bMid(IV_L, IV_R, 'CAB reviews risk, impact, and readiness; approves, defers, or rejects RFC')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RFC Submission Requirements'), bMid(B2_L, B2_R, 'CAB Review Criteria'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Change description + scope'), bMid(B2_L, B2_R, 'Risk: Low/Med/High/Critical'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Business justification'), bMid(B2_L, B2_R, 'Impact: services affected'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Risk and impact assessment'), bMid(B2_L, B2_R, 'Backout plan complete?'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Implementation steps'), bMid(B2_L, B2_R, 'Testing completed?'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backout plan'), bMid(B2_L, B2_R, 'Maintenance window OK?'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Test evidence'), bMid(B2_L, B2_R, 'Stakeholders notified?'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Risk level', 'Approval path', 'Notice period', 'Window', 'PIR required'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Low', 'Change mgr', '3 business days', 'Business hours', 'Optional'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Medium', 'CAB', '5 business days', 'Maintenance', 'Required'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['High', 'CAB + sponsor', '7 business days', 'Maintenance', 'Required'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Emergency', 'ECAB', '< 4 hours', 'ASAP', 'Required'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Risk matrix  = Likelihood × impact grid; determines required approval path'))
    lines.append(txt_row('  Business sponsor= Senior stakeholder sign-off required for high-risk changes'))
    lines.append(txt_row('  Deferred     = CAB sends RFC back with questions; requestor must resubmit after addressing'))
    lines.append(txt_row('  Notice period= Minimum lead time between RFC submission and earliest implementation date'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cm-communication',
    'docs/change-management/change-communication/index.md',
    'Change communication — stakeholder notify, downtime notice, post-change update',
)
def cm_communication():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []

    lines.append(title_border(W2, 'Change Communication'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Communication plan: notify stakeholders before, during, and after each change')))
    lines.append(R(bMid(IV_L, IV_R, 'Downtime notice: send at T-7d, T-1d, T-1h; post-change update on completion')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pre-Change'), bMid(B2_L, B2_R, 'During Change'), bMid(B3_L, B3_R, 'Post-Change'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'T-7d: initial notice'), bMid(B2_L, B2_R, 'T+0: change started'), bMid(B3_L, B3_R, 'Change completed'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'T-1d: reminder'), bMid(B2_L, B2_R, 'Status updates'), bMid(B3_L, B3_R, 'Service restored'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'T-1h: final reminder'), bMid(B2_L, B2_R, 'Delay comms'), bMid(B3_L, B3_R, 'Outcome summary'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Affected services'), bMid(B2_L, B2_R, 'Rollback comms'), bMid(B3_L, B3_R, 'Action items'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Contact for queries'), bMid(B2_L, B2_R, 'Bridge/chat link'), bMid(B3_L, B3_R, 'PIR scheduled'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Pre-change email template:')))
    lines.append(R(bMid(IV_L, IV_R, '  Subject: [Planned Maintenance] <service> — <date> <time> <timezone>')))
    lines.append(R(bMid(IV_L, IV_R, '  Body: What, When, Duration, Affected services, Contact, Rollback trigger')))
    lines.append(R(bMid(IV_L, IV_R, 'Post-change email:')))
    lines.append(R(bMid(IV_L, IV_R, '  Subject: [Completed] <service> maintenance — result: SUCCESS/FAILED')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Stakeholder map = Who needs to know: business owners, service users, on-call teams'))
    lines.append(txt_row('  Downtime notice = Mandatory for any user-impacting change; minimum T-24h notice'))
    lines.append(txt_row('  Bridge call     = Shared conference line during change; key contacts join for live comms'))
    lines.append(txt_row('  Rollback comms  = Notify immediately if rollback triggered; give new ETA for service restore'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cm-request',
    'docs/change-management/change-request/index.md',
    'Change request form — RFC fields, categorisation, submission checklist',
)
def cm_request():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Change Request (RFC)'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'RFC: formal document capturing all change details for CAB review and audit trail')))
    lines.append(R(bMid(IV_L, IV_R, 'Incomplete RFCs returned by CAB; complete all mandatory fields before submission')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Mandatory Fields'), bMid(B2_L, B2_R, 'Optional / Supporting'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Title (short, descriptive)'), bMid(B2_L, B2_R, 'Architecture diagram'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Change type: S/N/E'), bMid(B2_L, B2_R, 'Test evidence'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Description and scope'), bMid(B2_L, B2_R, 'Vendor runbook ref'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Business justification'), bMid(B2_L, B2_R, 'Config backup confirmation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Risk / impact assessment'), bMid(B2_L, B2_R, 'Approval from app owner'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Implementation steps'), bMid(B2_L, B2_R, 'Change dependency list'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backout plan + trigger'), bMid(B2_L, B2_R, 'Monitoring plan'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Maintenance window'), bMid(B2_L, B2_R, 'Communication plan'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Field', 'Type', 'Example', 'Mandatory', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Change type', 'Dropdown', 'Normal', 'Yes', 'S/N/E'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Risk', 'Dropdown', 'Medium', 'Yes', 'L/M/H/C'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Window', 'Datetime', 'Sat 02:00 UTC', 'Yes', 'Duration too'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Backout plan', 'Text', 'Step-by-step', 'Yes', 'With trigger'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  S/N/E     = Standard / Normal / Emergency change type'))
    lines.append(txt_row('  Backout trigger= Defined condition that automatically initiates rollback (e.g., service fails test)'))
    lines.append(txt_row('  Scope     = Exact systems, services, or components affected; used to notify correct teams'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cm-validation',
    'docs/change-management/change-validation/index.md',
    'Change validation — pre-change checks, success criteria, rollback triggers',
)
def cm_validation():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Change Validation'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Validation: pre-change baseline + post-change verification against success criteria')))
    lines.append(R(bMid(IV_L, IV_R, 'Document before/after state; define clear pass/fail criteria before execution')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pre-Change'), bMid(B2_L, B2_R, 'During Change'), bMid(B3_L, B3_R, 'Post-Change'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Screenshot baseline'), bMid(B2_L, B2_R, 'Step checkpoints'), bMid(B3_L, B3_R, 'Success criteria'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Config backup'), bMid(B2_L, B2_R, 'Rollback triggers'), bMid(B3_L, B3_R, 'Service healthy'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service state'), bMid(B2_L, B2_R, 'Time tracking'), bMid(B3_L, B3_R, 'Monitoring clean'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity baseline'), bMid(B2_L, B2_R, 'Comms updates'), bMid(B3_L, B3_R, 'Test results'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Performance metrics'), bMid(B2_L, B2_R, 'Decision gate'), bMid(B3_L, B3_R, 'Close ticket'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Check type', 'What', 'Method', 'Pass criteria', 'If fails'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Service', 'App response', 'Health endpoint', '200 OK < 1s', 'Rollback'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Monitoring', 'No new alerts', 'Alert console', 'All clear', 'Investigate'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Performance', 'Latency normal', 'Dashboard', 'Within baseline', 'Rollback'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Replication', 'In sync', 'Rep console', 'Lag < threshold', 'Investigate'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Success criteria= Defined measurable outcomes that prove the change worked as intended'))
    lines.append(txt_row('  Rollback trigger= Specific condition (timeout, error, threshold breach) that activates backout'))
    lines.append(txt_row('  Decision gate   = Checkpoint mid-change where team decides: continue, pause, or rollback'))
    lines.append(txt_row('  Baseline        = Pre-change metric snapshot; used as comparison target for post-change check'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cm-deployment',
    'docs/change-management/deployment-procedure/index.md',
    'Deployment procedure — execution steps, checkpoints, sequencing, sign-off',
)
def cm_deployment():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Deployment Procedure'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Deployment: execute change per approved RFC; document each step and outcome')))
    lines.append(R(bMid(IV_L, IV_R, 'No deviation from approved steps without ECAB approval; call out any variance')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Deployment Steps'), bMid(B2_L, B2_R, 'Documentation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '1. Go/No-Go decision call'), bMid(B2_L, B2_R, 'Log start time'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '2. Confirm attendees on bridge'), bMid(B2_L, B2_R, 'Capture each step output'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '3. Execute RFC steps in order'), bMid(B2_L, B2_R, 'Note any deviations'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '4. Checkpoint after each tier'), bMid(B2_L, B2_R, 'Screenshot key states'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '5. Run validation checks'), bMid(B2_L, B2_R, 'Log end time + outcome'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '6. Go/No-Go for next phase'), bMid(B2_L, B2_R, 'Notify stakeholders'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Checkpoint', 'Trigger', 'Decision', 'If pass', 'If fail'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Go/No-Go', 'Before exec', 'Team vote', 'Proceed', 'Defer change'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Mid-change', 'After each tier', 'Lead decides', 'Next step', 'Rollback'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Validation', 'After last step', 'Test results', 'Close change', 'Rollback'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Time overrun', 'Beyond window', 'Lead decides', 'Brief extend', 'Rollback'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Go/No-Go   = Explicit decision call before proceeding; requires confirmation from lead'))
    lines.append(txt_row('  Deviation   = Any step that differs from approved RFC; document and get verbal ECAB approval'))
    lines.append(txt_row('  Time overrun= Execution exceeds approved window; decision: extend (if safe) or rollback'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cm-emergency',
    'docs/change-management/emergency-change/index.md',
    'Emergency change — ECAB authorisation, expedited approval, retrospective',
)
def cm_emergency():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Emergency Change'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Emergency change: expedited process for P1/P2 incidents requiring immediate action')))
    lines.append(R(bMid(IV_L, IV_R, 'ECAB approval: verbal/email from ECAB quorum; document before or immediately after')))
    lines.append(R(bMid(IV_L, IV_R, 'Retrospective RFC required within 24 hours; post-change review within 5 days')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Emergency Change Criteria'), bMid(B2_L, B2_R, 'ECAB Process'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Active P1/P2 incident'), bMid(B2_L, B2_R, 'Call ECAB members (min 2)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service unavailable'), bMid(B2_L, B2_R, 'Explain risk + action'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Imminent security threat'), bMid(B2_L, B2_R, 'Verbal or email approval'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Regulatory deadline'), bMid(B2_L, B2_R, 'Execute immediately'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No time for normal CAB'), bMid(B2_L, B2_R, 'Document retrospectively'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Timeline', 'Action', 'Owner', 'Artefact', 'Deadline'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['T=0', 'Incident declared', 'Incident mgr', 'P1 ticket', 'Immediate'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['T+30 min', 'ECAB approval', 'Change mgr', 'Approval log', '30 min'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['T+24 hr', 'RFC raised', 'Change mgr', 'Retro RFC', '24 hours'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['T+5 days', 'PIR', 'Change mgr', 'PIR report', '5 business days'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  ECAB         = Emergency CAB; subset of CAB members available 24/7 for emergency approval'))
    lines.append(txt_row('  Retrospective= RFC created after emergency change to formalise the record'))
    lines.append(txt_row('  PIR          = Post-Implementation Review; required after emergency changes within 5 days'))
    lines.append(txt_row('  Quorum       = Minimum 2 ECAB members must approve; single approver insufficient'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cm-release',
    'docs/change-management/release-management/index.md',
    'Release management — packaging, scheduling, dependency mapping, go/no-go',
)
def cm_release():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Release Management'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Release management: package, schedule, and coordinate multi-change deployments')))
    lines.append(R(bMid(IV_L, IV_R, 'Release calendar: scheduled windows, freeze periods, and dependency sequencing')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Planning'), bMid(B2_L, B2_R, 'Execution'), bMid(B3_L, B3_R, 'Close-out'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Release packaging'), bMid(B2_L, B2_R, 'Sequenced deploy'), bMid(B3_L, B3_R, 'Release review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dependency map'), bMid(B2_L, B2_R, 'Gate checks'), bMid(B3_L, B3_R, 'Lessons learned'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Go/No-Go criteria'), bMid(B2_L, B2_R, 'Rollback trigger'), bMid(B3_L, B3_R, 'Metrics review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Freeze periods'), bMid(B2_L, B2_R, 'Communication'), bMid(B3_L, B3_R, 'Backlog update'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Stakeholder comms'), bMid(B2_L, B2_R, 'Live dashboard'), bMid(B3_L, B3_R, 'RFC closure'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Phase', 'Timeline', 'Gate', 'Owner', 'Artefact'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Planning', 'T-14d', 'Release plan', 'Release mgr', 'Release doc'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Freeze', 'T-7d', 'No new items', 'Change mgr', 'Freeze notice'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Go/No-Go', 'T-1h', 'All checks pass', 'Release mgr', 'Decision log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Review', 'T+2d', 'Success verify', 'Release mgr', 'Review report'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Release package= Group of related changes deployed together in a coordinated window'))
    lines.append(txt_row('  Freeze period  = No new changes added to release after freeze date; scope locked'))
    lines.append(txt_row('  Dependency map = Which changes must complete before others can start; sequence critical'))
    lines.append(txt_row('  Go/No-Go call  = Release decision meeting T-1h; all dependencies and pre-checks confirmed'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Lifecycle ─────────────────────────────────────────────────────────────────

@kb_diagram(
    'lifecycle',
    'docs/lifecycle/index.md',
    'Lifecycle landing — onboarding, upgrade, migration, decommission procedures',
)
def lifecycle_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []

    lines.append(title_border(W2, 'Lifecycle Management'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'System lifecycle: plan → onboard → operate → upgrade → migrate → decommission')))
    lines.append(R(bMid(IV_L, IV_R, 'Each phase documented; no phase skipped without CAB approval and risk assessment')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Procure → build → onboard → BAU → upgrade readiness → migration → decommission'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Onboard'), bMid(B2_L, B2_R, 'Operate / Upgrade'), bMid(B3_L, B3_R, 'Retire'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'System readiness'), bMid(B2_L, B2_R, 'Upgrade readiness'), bMid(B3_L, B3_R, 'Decommission plan'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CMDB entry'), bMid(B2_L, B2_R, 'Upgrade execution'), bMid(B3_L, B3_R, 'Data migration'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Monitoring setup'), bMid(B2_L, B2_R, 'Post-upgrade check'), bMid(B3_L, B3_R, 'Backup retention'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Runbook creation'), bMid(B2_L, B2_R, 'Rollback path'), bMid(B3_L, B3_R, 'Asset disposal'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Handover to ops'), bMid(B2_L, B2_R, 'Migration plan'), bMid(B3_L, B3_R, 'CMDB retire'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Onboarding    = Process of introducing a new system into BAU operations with documentation'))
    lines.append(txt_row('  Decommission  = Formal retirement of a system; data migration, backup, and asset recovery'))
    lines.append(txt_row('  CMDB          = Configuration Management Database; track system attributes through lifecycle'))
    lines.append(txt_row('  Upgrade window= Scheduled maintenance period for OS/firmware/software upgrades'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'lc-onboarding',
    'docs/lifecycle/system-onboarding/index.md',
    'System onboarding — new system intake, CMDB, monitoring, runbooks, handover',
)
def lc_onboarding():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'System Onboarding'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Onboarding: register new system in CMDB, configure monitoring, create runbooks')))
    lines.append(R(bMid(IV_L, IV_R, 'Gate: system not in BAU until all checklist items complete and signed off')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Technical Checklist'), bMid(B2_L, B2_R, 'Operational Checklist'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CMDB entry created'), bMid(B2_L, B2_R, 'Runbook created'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Monitoring configured'), bMid(B2_L, B2_R, 'On-call schedule updated'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup configured'), bMid(B2_L, B2_R, 'Support contract linked'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Patching schedule set'), bMid(B2_L, B2_R, 'Admin credentials in vault'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Network/DNS configured'), bMid(B2_L, B2_R, 'Team training completed'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Item', 'Owner', 'Tool', 'Pass criteria', 'Sign-off'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['CMDB', 'Infra team', 'CMDB tool', 'All fields', 'Infra lead'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Monitoring', 'Ops team', 'Zabbix/etc', 'Alerts active', 'Ops lead'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Backup', 'Backup team', 'Backup app', 'Job verified', 'Backup lead'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Runbook', 'Infra team', 'KB', 'Published', 'Peer review'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  BAU gate      = System accepted into Business As Usual operations only after all items complete'))
    lines.append(txt_row('  Onboarding doc= System record: owner, contacts, dependencies, SLA, backup, change history'))
    lines.append(txt_row('  Vault entry   = Admin credentials stored in CyberArk/vault; no shared spreadsheet creds'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'lc-upgrade-readiness',
    'docs/lifecycle/upgrade-readiness/index.md',
    'Upgrade readiness — pre-upgrade checklist, compatibility, backout, test plan',
)
def lc_upgrade_readiness():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Upgrade Readiness'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Upgrade readiness: verify compatibility, backup, backout plan, and test in lab first')))
    lines.append(R(bMid(IV_L, IV_R, 'Never upgrade production without lab validation; always have a tested rollback path')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pre-Upgrade Checks'), bMid(B2_L, B2_R, 'Readiness Gate'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Vendor release notes read'), bMid(B2_L, B2_R, 'Lab test passed'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Compatibility matrix verified'), bMid(B2_L, B2_R, 'Config backup confirmed'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Known issues reviewed'), bMid(B2_L, B2_R, 'Backout plan documented'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dependencies checked'), bMid(B2_L, B2_R, 'RFC approved'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Lab upgrade completed'), bMid(B2_L, B2_R, 'Stakeholders notified'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Check', 'Source', 'Pass criteria', 'Fail action', 'Owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Compat matrix', 'Vendor docs', 'All deps OK', 'Defer upgrade', 'Infra lead'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Lab test', 'Lab env', 'No regressions', 'Fix first', 'Infra lead'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Config backup', 'Backup system', 'Verified restore', 'Backup first', 'Backup team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Backout plan', 'RFC doc', 'Steps tested', 'Document first', 'Infra lead'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Compatibility matrix= Vendor document; shows which versions of deps are supported together'))
    lines.append(txt_row('  Lab upgrade    = Full upgrade rehearsal in non-production; validates procedure and time estimate'))
    lines.append(txt_row('  Known issues   = Vendor-published list of bugs in release; check for impact on your environment'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'lc-post-upgrade',
    'docs/lifecycle/post-upgrade-validation/index.md',
    'Post-upgrade validation — service health, performance, monitoring, sign-off',
)
def lc_post_upgrade():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Post-Upgrade Validation'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Post-upgrade: verify service health, performance baseline, monitoring alerts clear')))
    lines.append(R(bMid(IV_L, IV_R, 'Monitor for 24–72 hours post-change; keep rollback path available until stable')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Immediate (0–30 min)'), bMid(B2_L, B2_R, 'Soak Period (24–72 hr)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Version confirmed'), bMid(B2_L, B2_R, 'No error rate increase'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Services all running'), bMid(B2_L, B2_R, 'Latency at baseline'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No new alerts'), bMid(B2_L, B2_R, 'Backup job completes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Basic function test'), bMid(B2_L, B2_R, 'Replication in sync'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Log review for errors'), bMid(B2_L, B2_R, 'Monitoring stable'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Check', 'Method', 'Pass', 'Fail action', 'Window'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Version', 'CLI/GUI', 'Expected ver', 'Rollback', 'Immediate'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Services', 'systemctl/SC', 'All running', 'Rollback', 'Immediate'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Monitoring', 'Alert console', 'No new alerts', 'Investigate', 'Ongoing 72 hr'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Perf baseline', 'Dashboard', 'Within 5%', 'Investigate', 'Ongoing 72 hr'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Soak period    = Extended monitoring after change; typically 24–72 hours for major upgrades'))
    lines.append(txt_row('  Version confirm= Verify upgrade completed to expected target version; not partial'))
    lines.append(txt_row('  Error rate     = Application error rate; an increase post-upgrade indicates regression'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'lc-rollback',
    'docs/lifecycle/rollback-procedure/index.md',
    'Rollback procedure — trigger criteria, steps, validation, incident escalation',
)
def lc_rollback():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Rollback Procedure'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Rollback: revert change to pre-change state when success criteria not met')))
    lines.append(R(bMid(IV_L, IV_R, 'Trigger rollback at defined criteria; do not wait — sooner is safer')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Rollback Triggers'), bMid(B2_L, B2_R, 'Rollback Execution'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service unavailable'), bMid(B2_L, B2_R, 'Declare rollback on bridge'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Error rate > threshold'), bMid(B2_L, B2_R, 'Execute backout steps'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Validation test fails'), bMid(B2_L, B2_R, 'Restore from config backup'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Maintenance window end'), bMid(B2_L, B2_R, 'Verify service restored'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Team consensus'), bMid(B2_L, B2_R, 'Notify stakeholders'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Time overrun + P1'), bMid(B2_L, B2_R, 'Raise P1 if unresolved'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Trigger', 'Decision', 'Action', 'Timeline', 'Escalate if'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Service down', 'Auto trigger', 'Execute backout', 'Immediate', 'Backout fails'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Test fails', 'Lead decides', 'Execute backout', '< 15 min', 'P1 if down'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Window end', 'Team decides', 'Execute backout', 'At window end', 'P1 if down'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Partial fail', 'Lead decides', 'Assess risk', 'Context dep', 'If no backout'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Auto trigger  = Pre-defined condition that initiates rollback without manual decision'))
    lines.append(txt_row('  Config backup = Saved configuration state from before change; used to restore previous state'))
    lines.append(txt_row('  Backout steps = Documented reversal steps from RFC; must be tested before change execution'))
    lines.append(txt_row('  Partial fail  = Some components succeeded, others failed; assess risk vs completing rollback'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'lc-migration',
    'docs/lifecycle/migration-procedure/index.md',
    'Migration procedure — plan, data migration, cutover, validation, rollback',
)
def lc_migration():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Migration Procedure'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Migration: move workload/data from source to destination with cutover window')))
    lines.append(R(bMid(IV_L, IV_R, 'Phases: plan → pre-migrate (bulk) → cutover (delta) → validate → decommission source')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Plan → pre-migrate bulk data → cutover window → delta sync → validate → retire source'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pre-Migration'), bMid(B2_L, B2_R, 'Cutover'), bMid(B3_L, B3_R, 'Post-Migration'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Inventory source'), bMid(B2_L, B2_R, 'Quiesce source'), bMid(B3_L, B3_R, 'Validate dest'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Bulk data copy'), bMid(B2_L, B2_R, 'Final delta sync'), bMid(B3_L, B3_R, 'Test workload'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Test destination'), bMid(B2_L, B2_R, 'DNS/IP cutover'), bMid(B3_L, B3_R, 'Monitor 24–72 hr'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Size validation'), bMid(B2_L, B2_R, 'Update CMDB'), bMid(B3_L, B3_R, 'Decommission src'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Application mapping'), bMid(B2_L, B2_R, 'Notify stakeholders'), bMid(B3_L, B3_R, 'Confirm backup'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Phase', 'Duration', 'RPO during', 'Rollback', 'Key check'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Bulk copy', 'Days/hours', 'Source stays up', 'Cancel copy', 'Data integrity'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Cutover', 'Minutes/hours', 'Outage window', 'Re-point DNS', 'Service up'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Validation', '24–72 hr', 'Dest only', 'Re-point back', 'No data loss'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Decommission', 'After stable', '—', 'Restore backup', 'CMDB updated'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Bulk copy      = Initial large data transfer before cutover; source remains live'))
    lines.append(txt_row('  Delta sync     = Final sync of changes made during bulk copy; minimises cutover downtime'))
    lines.append(txt_row('  DNS cutover    = Update DNS to point clients to new destination; fast client redirect'))
    lines.append(txt_row('  Quiesce source = Stop writes to source for delta sync; creates RPO = zero at cutover'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'lc-env-readiness',
    'docs/lifecycle/environment-readiness/index.md',
    'Environment readiness — pre-deployment environment checks, capacity, dependencies',
)
def lc_env_readiness():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Environment Readiness'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Environment readiness: verify capacity, connectivity, dependencies, and credentials')))
    lines.append(R(bMid(IV_L, IV_R, 'Complete readiness checklist before any deployment or major change starts')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Infrastructure Readiness'), bMid(B2_L, B2_R, 'Dependency Readiness'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Storage: capacity available'), bMid(B2_L, B2_R, 'DNS resolves correctly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Compute: CPU/RAM headroom'), bMid(B2_L, B2_R, 'Network paths verified'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No active alarms on target'), bMid(B2_L, B2_R, 'Auth/credentials ready'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup current before deploy'), bMid(B2_L, B2_R, 'Downstream deps notified'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Monitoring configured'), bMid(B2_L, B2_R, 'Firewall rules in place'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Check', 'Method', 'Pass', 'Fail action', 'Owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Storage cap', 'Array GUI', '> 20% free', 'Expand first', 'Infra'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Compute cap', 'vCenter/Hyp-V', '> 20% free', 'Resize first', 'Infra'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Network conn', 'Ping + trace', 'All paths OK', 'Fix network', 'Network team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Auth', 'Test login', 'Success', 'Fix creds', 'Infra'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Headroom      = Free compute/storage capacity above the deployment requirement; 20% minimum'))
    lines.append(txt_row('  Downstream deps= Services or systems that depend on the environment being deployed to'))
    lines.append(txt_row('  Pre-deploy backup= Snapshot/config backup taken immediately before any change starts'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'lc-decommission',
    'docs/lifecycle/system-decommission/index.md',
    'System decommission — data migration, backup, asset recovery, CMDB retire',
)
def lc_decommission():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'System Decommission'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Decommission: retire system safely — migrate data, preserve backups, recover assets')))
    lines.append(R(bMid(IV_L, IV_R, 'No system retired without sign-off from business owner and storage/data team')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pre-Decommission'), bMid(B2_L, B2_R, 'Execution'), bMid(B3_L, B3_R, 'Close-out'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Business owner sign-off'), bMid(B2_L, B2_R, 'Migrate data'), bMid(B3_L, B3_R, 'CMDB retired status'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confirm no consumers'), bMid(B2_L, B2_R, 'Final backup'), bMid(B3_L, B3_R, 'Asset returned'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identify data retention'), bMid(B2_L, B2_R, 'DNS/IP removed'), bMid(B3_L, B3_R, 'License recovered'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Data classification review'), bMid(B2_L, B2_R, 'Monitoring removed'), bMid(B3_L, B3_R, 'Creds deleted'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup retention check'), bMid(B2_L, B2_R, 'Power off'), bMid(B3_L, B3_R, 'Secure erase data'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Step', 'Owner', 'Gate', 'Artefact', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Biz sign-off', 'Biz owner', 'Email approval', 'Approval email', 'Mandatory'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Data migrate', 'Infra team', 'Transfer verified', 'Migration log', 'Integrity check'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Secure erase', 'Infra team', 'Erasure cert', 'Certificate', 'Regulatory req'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['CMDB retire', 'Infra team', 'Status updated', 'CMDB record', 'End of process'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Secure erase   = DoD 7-pass or crypto erase of data before disposal; required by policy'))
    lines.append(txt_row('  Erasure cert   = Certificate from erase tool documenting that secure wipe completed'))
    lines.append(txt_row('  Consumer check = Confirm no active services, users, or applications depend on the system'))
    lines.append(txt_row('  Asset recovery = Return hardware to vendor, send to spare pool, or dispose per WEEE'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Cross-Platform Troubleshooting ────────────────────────────────────────────

@kb_diagram(
    'troubleshooting',
    'docs/troubleshooting/index.md',
    'Troubleshooting landing — cross-platform issue triage index',
)
def troubleshooting_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []

    lines.append(title_border(W2, 'Cross-Platform Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Common infrastructure issues across platforms: methodology + platform-specific paths')))
    lines.append(R(bMid(IV_L, IV_R, 'Universal triage: define symptom → collect data → isolate → test fix → confirm')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Alert fires → triage symptom → narrow scope → isolate component → fix → verify → close'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Compute / OS'), bMid(B2_L, B2_R, 'Storage / Network'), bMid(B3_L, B3_R, 'Services / Auth'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'High CPU'), bMid(B2_L, B2_R, 'Storage latency'), bMid(B3_L, B3_R, 'Auth failures'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VM performance'), bMid(B2_L, B2_R, 'Replication fail'), bMid(B3_L, B3_R, 'DNS resolution'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Memory pressure'), bMid(B2_L, B2_R, 'Network connectivity'), bMid(B3_L, B3_R, 'Backup failures'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Disk full'), bMid(B2_L, B2_R, 'Path failures'), bMid(B3_L, B3_R, 'Service down'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Kernel panic'), bMid(B2_L, B2_R, 'Packet loss'), bMid(B3_L, B3_R, 'SSO failures'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Triage    = Rapid initial assessment to determine urgency, scope, and next diagnostic step'))
    lines.append(txt_row('  Isolate   = Narrow the problem to a specific component, host, or path'))
    lines.append(txt_row('  RCA       = Root Cause Analysis; document underlying cause after resolution'))
    lines.append(txt_row('  P1/P2/P3  = Priority levels; P1 = service down, P2 = degraded, P3 = no user impact'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'ts-auth-failures',
    'docs/troubleshooting/authentication-failures/index.md',
    'Auth failures — AD/LDAP lockout, Kerberos, SSO/SAML, certificate trust',
)
def ts_auth_failures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Authentication Failures'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Auth failures: account lockout, expired password, Kerberos clock skew, SSO config')))
    lines.append(R(bMid(IV_L, IV_R, 'First check: Is the user account locked? Is the service account credential expired?')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'AD / LDAP'), bMid(B2_L, B2_R, 'Kerberos'), bMid(B3_L, B3_R, 'SSO / SAML'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Account locked'), bMid(B2_L, B2_R, 'Clock skew > 5 min'), bMid(B3_L, B3_R, 'Metadata mismatch'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Password expired'), bMid(B2_L, B2_R, 'SPN missing'), bMid(B3_L, B3_R, 'Certificate expired'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP port blocked'), bMid(B2_L, B2_R, 'Delegation issue'), bMid(B3_L, B3_R, 'ACS URL mismatch'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DC unreachable'), bMid(B2_L, B2_R, 'Realm mismatch'), bMid(B3_L, B3_R, 'Claim mapping'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Group policy block'), bMid(B2_L, B2_R, 'KDC unreachable'), bMid(B3_L, B3_R, 'IdP unreachable'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Symptom', 'First check', 'Command', 'Fix', 'Verify'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Locked out', 'AD LockedOut', 'Get-ADUser', 'Unlock-ADAccount', 'Login OK'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Kerberos fail', 'NTP clock', 'w32tm /query', 'Sync NTP', 'klist purge+test'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SSO fail', 'IdP logs', 'Browser trace', 'Fix metadata', 'SAML trace'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['LDAP blocked', 'Port 389/636', 'Test-NetConn', 'Open FW', 'ldapsearch OK'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Clock skew     = Kerberos requires all participants within 5 min; verify NTP on all hosts'))
    lines.append(txt_row('  SPN            = Service Principal Name; must exist and be unique for Kerberos auth to work'))
    lines.append(txt_row('  SAML trace     = Browser extension (SAML Tracer) captures assertion for SP/IdP debugging'))
    lines.append(txt_row('  ACS URL        = Assertion Consumer Service URL; SP endpoint; must match IdP configuration'))
    lines.append(txt_row('  klist purge    = Clears cached Kerberos tickets; forces re-auth after fixing KDC issue'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'ts-backup-failures',
    'docs/troubleshooting/backup-failures/index.md',
    'Backup failures — Veeam/NBU/Commvault job errors, proxy, repo, snapshot issues',
)
def ts_backup_failures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Backup Failures'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Backup failures: job errors, proxy overload, repo full, snapshot stun, network')))
    lines.append(R(bMid(IV_L, IV_R, 'First check: job log → error code → check proxy/repo/network → resolve')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Veeam'), bMid(B2_L, B2_R, 'NetBackup'), bMid(B3_L, B3_R, 'Commvault'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Proxy agent error'), bMid(B2_L, B2_R, 'Media server err'), bMid(B3_L, B3_R, 'MA agent error'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Repository full'), bMid(B2_L, B2_R, 'STU full'), bMid(B3_L, B3_R, 'Disk library full'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snapshot removal'), bMid(B2_L, B2_R, 'Snapshot timeout'), bMid(B3_L, B3_R, 'VSS failure'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VMware tools err'), bMid(B2_L, B2_R, 'Client network'), bMid(B3_L, B3_R, 'Subclient miss'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Transport mode'), bMid(B2_L, B2_R, 'Expired certs'), bMid(B3_L, B3_R, 'Job schedule'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Problem', 'First check', 'Fix', 'Verify', 'Escalate if'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Job failed', 'Job log error', 'Per error code', 'Job retry OK', 'Persistent fail'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Repo full', 'Repo capacity', 'Expire/expand', 'Space freed', 'No space avail'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Snapshot fail', 'VMware tools', 'Update tools', 'Snapshot OK', 'Datastore full'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Proxy err', 'Proxy CPU/RAM', 'Reduce tasks', 'Job completes', 'Agent reinstall'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Transport mode= Veeam: HotAdd, NBD, Direct SAN; wrong mode causes snapshot or perf issues'))
    lines.append(txt_row('  VSS           = Windows Volume Shadow Copy Service; required for consistent Windows backups'))
    lines.append(txt_row('  STU           = NetBackup Storage Unit; target for backup data; check capacity and path'))
    lines.append(txt_row('  Snapshot stun = ESXi: brief VM pause during snapshot create/commit; worse on large disks'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'ts-dns',
    'docs/troubleshooting/dns-resolution/index.md',
    'DNS resolution — forward/reverse failure, forwarder issues, cache flush, split-brain',
)
def ts_dns():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'DNS Resolution Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'DNS failures: forward lookup fail, reverse fail, forwarder down, stale cache')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnose with: nslookup, dig, Resolve-DnsName, ipconfig /displaydns')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Diagnostic Commands'), bMid(B2_L, B2_R, 'Common Fixes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'nslookup <host> <dns_ip>'), bMid(B2_L, B2_R, 'Flush DNS cache on client'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'dig @<dns_ip> <host>'), bMid(B2_L, B2_R, 'Check/restart DNS service'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'dig +trace <host>'), bMid(B2_L, B2_R, 'Add missing A/PTR record'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ipconfig /flushdns'), bMid(B2_L, B2_R, 'Fix forwarder config'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Resolve-DnsName (PS)'), bMid(B2_L, B2_R, 'Replicate zone to all DCs'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Problem', 'Diagnosis', 'Root cause', 'Fix', 'Verify'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Fwd lookup fail', 'nslookup fails', 'No A record', 'Add A record', 'nslookup passes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Reverse fail', 'nslookup reverse', 'No PTR record', 'Add PTR record', 'PTR resolves'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Stale cache', 'Wrong IP returned', 'Cached record', 'Flush client DNS', 'Correct IP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Forwarder fail', 'External fail', 'Forwarder down', 'Fix forwarder', 'External resolves'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Forwarder   = DNS server passing unresolved queries to upstream server (e.g., ISP or 8.8.8.8)'))
    lines.append(txt_row('  Split-brain = Internal and external DNS serving different records for same name'))
    lines.append(txt_row('  TTL         = Time To Live; cached record duration; lower TTL speeds propagation'))
    lines.append(txt_row('  PTR record  = Reverse DNS record; IP → hostname; required for many services and logs'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'ts-high-cpu',
    'docs/troubleshooting/high-cpu/index.md',
    'High CPU — identify top processes on Linux, Windows, ESXi; vCPU contention',
)
def ts_high_cpu():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'High CPU Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'High CPU: identify top consumers, check for CPU ready, investigate runaway processes')))
    lines.append(R(bMid(IV_L, IV_R, 'ESXi: CPU ready > 5% indicates overcommit; vCPU wait for physical CPU time')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Linux'), bMid(B2_L, B2_R, 'Windows'), bMid(B3_L, B3_R, 'ESXi / VMware'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'top / htop'), bMid(B2_L, B2_R, 'Task Manager'), bMid(B3_L, B3_R, 'esxtop: CPU'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ps aux --sort=-%cpu'), bMid(B2_L, B2_R, 'Get-Process sort'), bMid(B3_L, B3_R, 'CPU ready %'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'perf top'), bMid(B2_L, B2_R, 'Perfmon: % CPU'), bMid(B3_L, B3_R, 'Co-stop %'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'sar -u 1 10'), bMid(B2_L, B2_R, 'WPA profiler'), bMid(B3_L, B3_R, 'VM CPU limit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'strace / ftrace'), bMid(B2_L, B2_R, 'Process dump'), bMid(B3_L, B3_R, 'NUMA topology'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Symptom', 'Tool', 'Indicator', 'Fix', 'Verify'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Runaway proc', 'top / Task Mgr', 'High PID CPU%', 'Kill/restrain', 'CPU normalises'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['CPU ready', 'esxtop %RDY', '> 5%', 'Reduce vCPU', 'Ready drops'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Steal time', 'top %st', '> 0 in cloud', 'Upgrade VM type', 'Steal = 0'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['IRQ load', 'cat /proc/intr', 'One CPU pinned', 'irqbalance', 'IRQ spread'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  CPU ready  = ESXi: time vCPU waits for physical CPU; > 5% impacts VM performance'))
    lines.append(txt_row('  Co-stop    = ESXi SMP VMs wait for all vCPUs to be scheduled simultaneously'))
    lines.append(txt_row('  Steal time = In VMs: hypervisor withholding CPU from guest; indicates host overcommit'))
    lines.append(txt_row('  irqbalance = Linux daemon; distributes hardware interrupts across CPUs for load balance'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'ts-network-conn',
    'docs/troubleshooting/network-connectivity/index.md',
    'Network connectivity — ping, trace, MTU, VLAN, firewall, path isolation',
)
def ts_network_conn():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Network Connectivity Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Network troubleshooting: isolate at which layer connectivity fails')))
    lines.append(R(bMid(IV_L, IV_R, 'Methodology: ping gateway → trace route → check firewall → MTU → VLAN')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Diagnostic Steps'), bMid(B2_L, B2_R, 'Common Causes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '1. ping 127.0.0.1 (loopback)'), bMid(B2_L, B2_R, 'Firewall rule blocking port'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '2. ping default gateway'), bMid(B2_L, B2_R, 'Wrong VLAN tagging'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '3. traceroute to destination'), bMid(B2_L, B2_R, 'MTU mismatch (jumbo frames)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '4. Test on specific port'), bMid(B2_L, B2_R, 'NIC or vmnic down'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '5. Check firewall logs'), bMid(B2_L, B2_R, 'Route missing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '6. Verify VLAN config'), bMid(B2_L, B2_R, 'ARP table stale'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Layer', 'Check', 'Command', 'Fix', 'Platform'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['L2 / VLAN', 'VLAN tagging', 'show int trunk', 'Fix VLAN', 'Switch / vSwitch'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['L3 / Route', 'Route table', 'ip route / route', 'Add route', 'All OSes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Firewall', 'Port block', 'Test-NetConn', 'Open FW rule', 'All OSes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['MTU', 'Jumbo frames', 'ping -s 8972 -M do', 'Match MTU', 'Linux'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  MTU mismatch  = Jumbo frame configured on one side but not other; packets silently dropped'))
    lines.append(txt_row('  ARP stale     = ARP cache holds wrong MAC; clear with arp -d or wait for TTL expiry'))
    lines.append(txt_row('  Test-NetConn  = PowerShell: tests TCP connectivity to specific host and port'))
    lines.append(txt_row('  traceroute    = Shows each hop to destination; identifies where path breaks'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'ts-rep-failures',
    'docs/troubleshooting/replication-failures/index.md',
    'Replication failures — SRDF, SnapMirror, vSphere Replication link/lag/state errors',
)
def ts_rep_failures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Replication Failure Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Replication failures: WAN link loss, auth error, lag exceeds RPO, pair state error')))
    lines.append(R(bMid(IV_L, IV_R, 'First check: WAN connectivity → replication link state → pair state → lag')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SRDF (PowerMax)'), bMid(B2_L, B2_R, 'SnapMirror (ONTAP)'), bMid(B3_L, B3_R, 'vSphere Rep'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'symrdf query'), bMid(B2_L, B2_R, 'snapmirror show'), bMid(B3_L, B3_R, 'VR appliance UI'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RDF link state'), bMid(B2_L, B2_R, 'SM state field'), bMid(B3_L, B3_R, 'VR status'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'R1/R2 state'), bMid(B2_L, B2_R, 'Lag time'), bMid(B3_L, B3_R, 'RPO status'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'symrdf failover'), bMid(B2_L, B2_R, 'snapmirror resync'), bMid(B3_L, B3_R, 'Re-register VM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RDF group'), bMid(B2_L, B2_R, 'Peering cluster'), bMid(B3_L, B3_R, 'VRS configuration'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Symptom', 'First check', 'Fix', 'Verify', 'Escalate if'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Link down', 'WAN ping/test', 'Fix WAN', 'Rep resumes', 'Persistent down'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['High lag', 'WAN bandwidth', 'Throttle or fix', 'Lag decreases', 'RPO breach'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Pair error', 'Auth/cert', 'Re-authenticate', 'State normal', 'Data diverge'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Suspended', 'Manual suspend', 'Resume rep', 'In-sync', 'If not resuming'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  RDF link    = Fibre Channel or IP link between PowerMax pairs; GigE or dedicated FC'))
    lines.append(txt_row('  Peering     = ONTAP cluster peer relationship; required for SnapMirror cross-cluster'))
    lines.append(txt_row('  VRS         = vSphere Replication Server; collects replication data on target site'))
    lines.append(txt_row('  RPO breach  = Lag exceeds configured RPO target; escalate immediately as DR goal at risk'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'ts-storage-latency',
    'docs/troubleshooting/storage-latency/index.md',
    'Storage latency — queue depth, path health, array performance, I/O contention',
)
def ts_storage_latency():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Storage Latency Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'High storage latency: check queue depth, path health, array load, and KAVG')))
    lines.append(R(bMid(IV_L, IV_R, 'ESXi: KAVG > 5ms = host queue issue; DAVG = array latency; GAVG = total')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Host Layer'), bMid(B2_L, B2_R, 'Path / HBA'), bMid(B3_L, B3_R, 'Array Layer'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'KAVG > 5ms'), bMid(B2_L, B2_R, 'Dead paths'), bMid(B3_L, B3_R, 'DAVG > 10ms'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Queue depth limit'), bMid(B2_L, B2_R, 'Degraded paths'), bMid(B3_L, B3_R, 'Hot pool/tier'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ABPG (abort)'), bMid(B2_L, B2_R, 'HBA errors'), bMid(B3_L, B3_R, 'Array queue full'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'IO scheduler'), bMid(B2_L, B2_R, 'MPIO imbalance'), bMid(B3_L, B3_R, 'Cache hit ratio'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VMware balloon'), bMid(B2_L, B2_R, 'FC fabric errors'), bMid(B3_L, B3_R, 'Drive rebuild'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Metric', 'Tool', 'Threshold', 'Cause', 'Fix'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['KAVG', 'esxtop/vscsistats', '< 5ms', 'Host queue', 'Reduce queue depth'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['DAVG', 'esxtop/vscsistats', '< 10ms', 'Array perf', 'Array QoS/tiering'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['GAVG', 'esxtop', 'KAVG+DAVG', 'Combined', 'Isolate layer'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Path health', 'esxcli nmp', 'All active', 'Dead path', 'Rescan HBAs'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  KAVG = Kernel Average latency; time I/O spends in ESXi storage stack (queue)'))
    lines.append(txt_row('  DAVG = Device Average latency; time I/O spends on storage array (wire + array)'))
    lines.append(txt_row('  GAVG = Guest Average; total latency seen by VM; KAVG + DAVG approximately'))
    lines.append(txt_row('  ABPG = Abort Per Second; commands timing out; indicates severe latency or path issue'))
    lines.append(txt_row('  MPIO = Multipath I/O; balanced across paths; single active path = higher DAVG'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'ts-vm-perf',
    'docs/troubleshooting/vm-performance/index.md',
    'VM performance — CPU ready, memory balloon, disk latency, network drops',
)
def ts_vm_perf():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VM Performance Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Slow VM: check CPU ready, memory balloon/swap, disk DAVG, and network drops')))
    lines.append(R(bMid(IV_L, IV_R, 'Use esxtop to triage all four resource domains simultaneously')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CPU'), bMid(B2_L, B2_R, 'Memory'), bMid(B3_L, B3_R, 'Disk / Net'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CPU ready > 5%'), bMid(B2_L, B2_R, 'Balloon > 0'), bMid(B3_L, B3_R, 'DAVG > 10ms'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Co-stop high'), bMid(B2_L, B2_R, 'Swap > 0'), bMid(B3_L, B3_R, 'Net drops'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Overcommit'), bMid(B2_L, B2_R, 'Mem compression'), bMid(B3_L, B3_R, 'IOPS saturate'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CPU limit set'), bMid(B2_L, B2_R, 'Reservation miss'), bMid(B3_L, B3_R, 'Rx/Tx drops'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NUMA mismatch'), bMid(B2_L, B2_R, 'Guest leak'), bMid(B3_L, B3_R, 'Snapshot present'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Symptom', 'esxtop key', 'Threshold', 'Root cause', 'Fix'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['CPU slow', 'c → %RDY', '> 5%', 'Overcommit', 'Reduce vCPU or DRS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Mem slow', 'm → MCTL', '> 0 MB', 'Overcommit', 'Add RAM/reserv.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Disk slow', 'd → DAVG', '> 10ms', 'Array latency', '→ storage-latency'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Net drops', 'n → Drp/s', '> 0', 'NIC saturate', 'Increase vNIC/QoS'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  CPU ready  = vCPU waiting for physical CPU; reduce vCPU count or migrate VM to less loaded host'))
    lines.append(txt_row('  Balloon    = VMware reclaiming guest RAM via balloon driver; guest must free its own memory'))
    lines.append(txt_row('  Swap       = VMware swapping guest RAM to host swap file; causes severe performance impact'))
    lines.append(txt_row('  NUMA miss  = vCPU accesses RAM from remote NUMA node; size VMs within physical NUMA boundary'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines
