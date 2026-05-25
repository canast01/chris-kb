# Linux — Encryption

LUKS/dm-crypt full-disk encryption, NBDE (Network Bound Disk Encryption), TLS for services, and encrypted volume management.

```text
┌────────────────────────────────────────────────────────┐
│                Linux Encryption Layers                 │
├────────────────────────────────────────────────────────┤
│  Disk: LUKS2 (dm-crypt)                                │
│  /dev/sdX ──► luksFormat ──► luksOpen ──► /dev/mapper  │
│  Key slots: passphrase │ keyfile │ Clevis/NBDE token   │
│                                                        │
│  NBDE auto-unlock at boot:                             │
│  Clevis (client) ──► Tang server ──► release key       │
│  (only unlocks when on trusted network)                │
├────────────────────────────────────────────────────────┤
│  TLS (in-transit)                                      │
│  CA ──► sign CSR ──► server.crt + server.key           │
│  nginx/httpd: TLSv1.2+ │ strong ciphers │ HSTS         │
│  RHEL: update-crypto-policies --set DEFAULT/FUTURE     │
├────────────────────────────────────────────────────────┤
│  GPG (file/data)                                       │
│  gpg --encrypt --recipient  │  gpg --symmetric         │
└────────────────────────────────────────────────────────┘
```

## LUKS — Full Disk Encryption

LUKS (Linux Unified Key Setup) is the standard block device encryption layer on Linux, implemented via `dm-crypt`.

### Encrypt a New Block Device

```bash
# Install cryptsetup
dnf install -y cryptsetup   # RHEL
apt install -y cryptsetup   # Ubuntu

# IMPORTANT: This destroys all data on the device
cryptsetup luksFormat --type luks2 --cipher aes-xts-plain64 --key-size 512 --hash sha512 /dev/sdb

# Open (map) the encrypted device
cryptsetup luksOpen /dev/sdb secure-data

# Create a filesystem on the mapped device
mkfs.xfs /dev/mapper/secure-data

# Mount it
mkdir /mnt/secure-data
mount /dev/mapper/secure-data /mnt/secure-data
```

### Inspect a LUKS Device

```bash
# View header and key slot status
cryptsetup luksDump /dev/sdb

# Check if a device is LUKS
cryptsetup isLuks /dev/sdb && echo "LUKS device"

# Device info
cryptsetup status secure-data
```

### Key Slot Management

LUKS2 supports up to 32 key slots, allowing multiple passphrases or key files.

```bash
# Add a second passphrase (e.g., for a recovery key)
cryptsetup luksAddKey /dev/sdb
# or specify the new keyfile directly
cryptsetup luksAddKey /dev/sdb /path/to/keyfile

# Remove a passphrase from slot 1
cryptsetup luksKillSlot /dev/sdb 1

# Change passphrase (add new, then remove old)
cryptsetup luksChangeKey /dev/sdb
```

### Persistent Mount via /etc/crypttab and /etc/fstab

```bash
# Get the UUID of the LUKS device
blkid /dev/sdb
```

```bash
# /etc/crypttab — maps the encrypted device to a name at boot
# Format: name  device-or-UUID  key-file  options
secure-data  UUID=a1b2c3d4-e5f6-7890-abcd-ef1234567890  none  luks

# If using a key file instead of interactive passphrase:
secure-data  UUID=a1b2c3d4-e5f6-7890-abcd-ef1234567890  /root/keyfile  luks
```

```bash
# /etc/fstab — mount the mapped device
/dev/mapper/secure-data  /mnt/secure-data  xfs  defaults,_netdev  0 0
```

```bash
# Test without rebooting
systemctl daemon-reload
systemctl start systemd-cryptsetup@secure-data
mount /mnt/secure-data
```

### LUKS Header Backup

The LUKS header is critical — if corrupted, the volume is permanently unreadable.

```bash
# Backup header to a secure location
cryptsetup luksHeaderBackup /dev/sdb --header-backup-file /secure-backup/sdb-luks-header.bak

# Restore header if needed
cryptsetup luksHeaderRestore /dev/sdb --header-backup-file /secure-backup/sdb-luks-header.bak
```

## NBDE — Network Bound Disk Encryption

NBDE (Network Bound Disk Encryption) allows encrypted systems to unlock automatically at boot when on the trusted network, without manual passphrase entry. This uses Tang (server) and Clevis (client).

### Tang Server Setup

```bash
# Install Tang on the key escrow server
dnf install -y tang

# Enable and start the Tang socket
systemctl enable --now tangd.socket

# Tang keys are auto-generated in /var/db/tang/
ls /var/db/tang/

# Get the Tang server thumbprint (share with Clevis clients)
tang-show-keys /var/db/tang/
```

### Clevis Client Setup

```bash
# Install Clevis on the server with the LUKS volume
dnf install -y clevis clevis-luks clevis-dracut

# Bind the LUKS device to a Tang server
# Replace with your Tang server IP and thumbprint
clevis luks bind -d /dev/sdb tang '{"url":"http://tang.example.local","thp":"<thumbprint>"}'

# Verify binding
clevis luks list -d /dev/sdb

# Rebuild initramfs so Clevis runs at boot
dracut -f
```

### NBDE with Multiple Tang Servers (Redundancy)

```bash
# Bind to two Tang servers — unlock if either is reachable (threshold: 1 of 2)
clevis luks bind -d /dev/sdb sss '{"t":1,"pins":{"tang":[{"url":"http://tang1.example.local","thp":"<thp1>"},{"url":"http://tang2.example.local","thp":"<thp2>"}]}}'
```

### Test NBDE Unlock

```bash
# Manually test that Clevis can unlock the device
clevis luks unlock -d /dev/sdb

# Check that Tang is reachable
curl http://tang.example.local/adv
```

## TLS for System Services

### Generating a Certificate with OpenSSL

```bash
# Generate a private key (RSA 4096 or ECDSA P-256)
openssl genrsa -out /etc/pki/tls/private/server.key 4096
chmod 600 /etc/pki/tls/private/server.key

# Generate a CSR
openssl req -new -key /etc/pki/tls/private/server.key \
  -out /etc/pki/tls/misc/server.csr \
  -subj "/CN=server01.example.local/O=Corp/C=GB"

# Self-signed certificate (for testing only)
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout /etc/pki/tls/private/server.key \
  -out /etc/pki/tls/certs/server.crt \
  -days 365 \
  -subj "/CN=server01.example.local"

# Verify a certificate
openssl x509 -in /etc/pki/tls/certs/server.crt -text -noout | grep -E "Subject:|Issuer:|Not After"
```

### Verify TLS on a Running Service

```bash
# Check certificate presented by a service
openssl s_client -connect server01.example.local:443 -servername server01.example.local </dev/null 2>/dev/null | openssl x509 -noout -text | grep -E "Subject:|Not After"

# Test with specific TLS version
openssl s_client -connect server01.example.local:443 -tls1_3

# Check expiry date
echo | openssl s_client -connect server01.example.local:443 2>/dev/null | openssl x509 -noout -dates
```

### Nginx TLS Hardening

```nginx
# /etc/nginx/conf.d/ssl.conf
server {
    listen 443 ssl;
    server_name server01.example.local;

    ssl_certificate     /etc/pki/tls/certs/server.crt;
    ssl_certificate_key /etc/pki/tls/private/server.key;

    # TLS 1.2 minimum; 1.3 preferred
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305';
    ssl_prefer_server_ciphers on;

    # HSTS — once enabled, browsers enforce HTTPS
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;

    # Session resumption
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8;
}
```

### System-Wide Crypto Policy (RHEL)

```bash
# View current policy
update-crypto-policies --show

# Set to DEFAULT (TLS 1.2+, SHA-1 deprecated)
update-crypto-policies --set DEFAULT

# Stricter: FUTURE policy (TLS 1.3 only, 3072-bit RSA minimum)
update-crypto-policies --set FUTURE

# Apply without reboot
update-crypto-policies --set DEFAULT && systemctl restart sshd nginx
```

## Encrypted Swap

```bash
# Configure encrypted swap in /etc/crypttab
# Using random key — cleared on reboot, no data persistence needed
# /etc/crypttab:
swap  /dev/sda2  /dev/urandom  swap,cipher=aes-xts-plain64,size=512

# /etc/fstab:
/dev/mapper/swap  none  swap  sw  0 0
```

## GnuPG — File and Data Encryption

```bash
# Encrypt a file for a recipient (using their public key)
gpg --encrypt --recipient jsmith@corp.local --armor /path/to/sensitive.tar.gz

# Decrypt
gpg --decrypt sensitive.tar.gz.asc > sensitive.tar.gz

# Symmetric encryption (passphrase only)
gpg --symmetric --cipher-algo AES256 sensitive.tar.gz

# Sign and encrypt
gpg --sign --encrypt --recipient jsmith@corp.local document.pdf
```

## Key Management Best Practices

| Practice | Implementation |
|---|---|
| Store LUKS header backups offline | USB drive in physical safe, separated from server |
| Rotate Tang server keys periodically | `tang-show-keys` + re-bind Clevis clients |
| Restrict TLS private key permissions | `chmod 600`, owned by service user or root |
| Certificate expiry monitoring | `openssl x509 -noout -dates` + alerting |
| Use hardware tokens for master keys | YubiKey / TPM as LUKS token slot |
| No weak ciphers | `update-crypto-policies --set DEFAULT` minimum |

## Audit — Encryption Posture

```bash
# Find unencrypted block devices (no LUKS signature)
lsblk -o NAME,FSTYPE,MOUNTPOINT | grep -v crypto_LUKS

# Check all LUKS devices on the system
blkid | grep LUKS

# Confirm TLS is used on sensitive ports
ss -tlnp | grep -E ':443|:8443|:636|:9200'

# Check SSH server for weak algorithms
sshd -T | grep -E "ciphers|macs|kexalgorithms"

# Check system crypto policy
update-crypto-policies --show

# Find private key files readable by non-root
find /etc /home /opt -name "*.key" -o -name "*.pem" 2>/dev/null | xargs ls -la 2>/dev/null | grep -v "^-r.------"
```

## Quick Reference

| Topic | Key Command / Path |
|---|---|
| Encrypt a device | `cryptsetup luksFormat /dev/sdX` |
| Open LUKS device | `cryptsetup luksOpen /dev/sdX name` |
| Persistent mapping | `/etc/crypttab` |
| LUKS header backup | `cryptsetup luksHeaderBackup` |
| NBDE Tang server | `systemctl enable --now tangd.socket` |
| NBDE Clevis bind | `clevis luks bind -d /dev/sdX tang '...'` |
| System crypto policy | `update-crypto-policies --set DEFAULT` |
| Certificate info | `openssl x509 -in cert.crt -text -noout` |
| Test TLS endpoint | `openssl s_client -connect host:443` |
