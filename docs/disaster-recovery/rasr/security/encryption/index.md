```bash
# Unity — check Data at Rest Encryption status
uemcli /sys/security/encryption show

# Expected output should show:
# Encryption status: Enabled
# Encryption mode: SED (Self-Encrypting Drives) or software

# PowerStore — check encryption
pstcli --action show --object cluster | grep -i encrypt

# View individual drive encryption status
uemcli /stor/drive show -detail | grep -i encrypt
```

```text
┌────────────────────────────────────────── RASR — Encryption ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                RASR — Encryption Configuration                                │   │
│   │     AES-256 at rest on vault; TLS 1.3 for all management; vault lock enforces immutability    │   │
│   │              In-transit: TLS 1.2+ for all management; data channel also encrypted             │   │
│   │              At-rest: AES-256 on repository or vault storage; key managed by KMS              │   │
│   │               Key lifecycle: generate → use → rotate (annual) → retire → destroy              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  In-Transit                  │  │                   At-Rest                   │   │
│   │              TLS 1.2+ (minimum)              │  │              AES-256 encryption             │   │
│   │          443 (PPDM REST API) HTTPS           │  │              KMS key management             │   │
│   │             Mutual TLS internal              │  │               WORM / immutable              │   │
│   │             Cert rotation annual             │  │             Key rotation annual             │   │
│   │             No plain-text admin              │  │               Audit key access              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts     │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest       │
│  Vault         = isolated, air-gapped storage appliance receiving periodic replication copies         │
│  Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies      │
│  CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures        │
│  PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery      │
│  Air Gap       = physical or logical network isolation preventing attacker lateral movement to        │
│  Delta Set     = incremental changed blocks replicated from production to vault each cycle            │
│  Clean Room    = isolated recovery environment: separate vCenter, network, and workstations           │
│  Recovery Point= specific vault snapshot timestamp from which clean recovery is performed             │
│  Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac       │
│  Journal       = write-order-consistent journal on vault enabling point-in-time recovery              │
│  Scan Report   = CyberSense output: clean/suspect classification per file and block                   │
│  Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept                    │
│  RTO           = Recovery Time Objective; time from failover decision to restored service             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Backup the LUKS header (required to recover if header is damaged)
cryptsetup luksHeaderBackup /dev/sdX2 \
  --header-backup-file /secure-storage/rasr-usb-header.bak
# Store this backup in a separate secure location from the USB
```
```powershell
# Enable BitLocker on the recovery USB drive
Enable-BitLocker -MountPoint "E:" `
  -EncryptionMethod XtsAes256 `
  -RecoveryPasswordProtector

# Store the recovery key in AD
$keyId = (Get-BitLockerVolume "E:").KeyProtector |
  Where-Object { $_.KeyProtectorType -eq "RecoveryPassword" } |
  Select-Object -ExpandProperty KeyProtectorId

Backup-BitLockerKeyProtector -MountPoint "E:" -KeyProtectorId $keyId

# Display the recovery key for offline backup
(Get-BitLockerVolume "E:").KeyProtector |
  Where-Object { $_.KeyProtectorType -eq "RecoveryPassword" } |
  Select-Object RecoveryPassword
```
```bash
# Unity — configure replication connection with encryption
uemcli /remote/sys create \
  -name "DR-Site-Array" \
  -mgmtAddr dr-array.example.local \
  -connection synchronized \
  -port 443

# Verify replication connection is using TLS
uemcli /remote/sys show -detail | grep -i "connection\|encrypt\|tls"

# View replication sessions and status
uemcli /prot/rep/session show -detail
```
```bash
# Linux — configure IPsec tunnel between sites for iSCSI replication
# Using strongSwan
cat >> /etc/ipsec.conf << 'EOF'
conn prod-to-dr-replication
    left=10.10.10.1          # Production site replication interface
    leftsubnet=10.10.10.0/24
    right=10.20.10.1         # DR site replication interface
    rightsubnet=10.20.10.0/24
    ike=aes256-sha256-ecp256!
    esp=aes256-sha256!
    keyingtries=%forever
    auto=start
EOF

systemctl restart strongswan

# Verify tunnel is established
ipsec status
ipsec statusall | grep "prod-to-dr-replication"
```
```bash
# iDRAC — set minimum TLS version
racadm set iDRAC.WebServer.TLSProtocol TLS1_2
# Or TLS1_2_AND_ABOVE on newer iDRAC firmware

# Disable weak cipher suites via racadm
racadm set iDRAC.WebServer.SslEncryptionBitLength 256

# Verify certificate used by iDRAC
openssl s_client -connect <idrac-ip>:443 </dev/null 2>/dev/null | \
  openssl x509 -noout -subject -dates

# Replace self-signed iDRAC certificate with a corporate CA-signed certificate
racadm sslkeyupload -t 1 -f /tmp/idrac-private.key
racadm sslcertupload -t 1 -f /tmp/idrac-cert.pem
racadm racreset   # Restart iDRAC to apply
```
```bash
# Unity — verify TLS configuration
# Unisphere web UI enforces TLS; verify via:
openssl s_client -connect unisphere.example.local:443 -tls1_2 </dev/null 2>&1 | grep "Protocol:"
openssl s_client -connect unisphere.example.local:443 -tls1 </dev/null 2>&1 | grep "Protocol:\|handshake failure"
# TLS 1.0 connection should fail
```
```bash
# Verify LUKS volumes are still encrypted after restore
cryptsetup luksDump /dev/sda3   # OS data partition
cryptsetup luksDump /dev/sdb    # Data disk

# Confirm dm-crypt mappings are active
lsblk -o NAME,TYPE,FSTYPE,MOUNTPOINT | grep crypt

# If NBDE/Clevis was used, verify Tang binding is still present
clevis luks list -d /dev/sda3

# If Tang server was also recovered or moved, rebind
clevis luks bind -d /dev/sda3 tang '{"url":"http://tang.example.local","thp":"<thumbprint>"}'
```
```powershell
# Verify BitLocker protection status after RASR recovery
Get-BitLockerVolume | Select-Object MountPoint, VolumeStatus, ProtectionStatus, EncryptionMethod

# If ProtectionStatus = Off — resume protection
Resume-BitLocker -MountPoint "C:"

# If recovery key was used to unlock during recovery, rotate the key
$keyId = (Get-BitLockerVolume "C:").KeyProtector |
  Where-Object {$_.KeyProtectorType -eq "RecoveryPassword"} |
  Select-Object -ExpandProperty KeyProtectorId

Remove-BitLockerKeyProtector -MountPoint "C:" -KeyProtectorId $keyId
Add-BitLockerKeyProtector -MountPoint "C:" -RecoveryPasswordProtector
Backup-BitLockerKeyProtector -MountPoint "C:" -KeyProtectorId (
    (Get-BitLockerVolume "C:").KeyProtector |
    Where-Object {$_.KeyProtectorType -eq "RecoveryPassword"} |
    Select-Object -ExpandProperty KeyProtectorId)
```
```bash
# Array encryption enabled
uemcli /sys/security/encryption show | grep "Encryption status"

# External KMS configured and reachable
uemcli /sys/security/keymanage/kmip show | grep "Status"

# Recovery USB is encrypted
cryptsetup isLuks /dev/sdX2 && echo "LUKS encrypted" || echo "NOT encrypted"
# Or for Windows: check BitLocker status via Manage-bde -status E:

# Management plane TLS 1.0/1.1 disabled
openssl s_client -connect unisphere.example.local:443 -tls1 2>&1 | grep "handshake failure"

# Replication traffic encrypted (check IPsec tunnel status)
ipsec status | grep "prod-to-dr-replication"

# Post-recovery: BitLocker / LUKS still active
Get-BitLockerVolume | Where-Object {$_.ProtectionStatus -eq "Off"}
lsblk | grep crypt
```
