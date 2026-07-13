---
tags:
  - linux
  - security
---
# Linux — Encryption

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


```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu Nov 14 09:47:22 2024.
Dependencies resolved.
================================================================================
 Package             Arch         Version              Repository         Size
================================================================================
Installing:
 cryptsetup          x86_64       2.6.1-5.el9          rhel-9-baseos-rpms 156 kB

Transaction Summary
================================================================================
Install  1 Package

Total download size: 156 kB
Installed size: 412 kB
Downloading Packages:
cryptsetup-2.6.1-5.el9.x86_64.rpm                    156 kB/s | 156 kB     00:01
Running transaction
Preparing        :                                                        1/1
Installing       : cryptsetup-2.6.1-5.el9.x86_64                         1/1
Verifying        : cryptsetup-2.6.1-5.el9.x86_64                         1/1

Installed:
  cryptsetup-2.6.1-5.el9.x86_64

Complete!
WARNING: Device /dev/sdb already contains a 'dos' partition table. Proceed? (yes/no) yes
Enter passphrase for /dev/sdb: 
Verify passphrase: 
Initializing LUKS2 format with sha512 hash...
Key slot 0 created.
Command successful.
(no output — command completes silently)
meta-data=/dev/mapper/secure-data isize=512 agcount=4, agsize=2621440 blks
         =                       secctrs=8 attr=2, projid32bit=1
         =                       crc=1 finobt=1, sparse=0, rmapbt=0
         =                       reflink=1 finobt=1 spinodes=0
data     =                       bsize=4096 blocks=10485760, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0 fsuuid=a7f2c9e1-4b6d-4a92-8c3f-5d8e2b1a9f47 ftype=1
log      =internal               bsize=4096   blocks=5120, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, extsz=4096 blks
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Device /dev/sdb is not a block device or does not exist.` | Verify the correct device path with `lsblk` and ensure the device is attached and visible to the system. |
    | `No key available with this passphrase.` | Ensure the passphrase entered during `luksOpen` exactly matches the one set during `luksFormat`, including case and special characters. |
    | `Device /dev/mapper/secure-data is busy` | Unmount the filesystem with `umount /mnt/secure-data` and close the LUKS device with `cryptsetup l |
```bash
# Get the UUID of the LUKS device
blkid /dev/sdb
```

```text title="Expected output"
/dev/sdb: UUID="a7f3c2e1-9b4d-4f8a-b2c6-1d5e8f9a3b7c" TYPE="crypto_LUKS" PARTUUID="5e8f9a3b-7c2d"
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `blkid: command not found` | Install util-linux package with `apt-get install util-linux` or `yum install util-linux`. |
    | `blkid: error: /dev/sdb: No such file or directory` | Verify the device exists with `lsblk` and use the correct device path (e.g., `/dev/nvme0n1` for NVMe drives). |
```bash
# /etc/crypttab — maps the encrypted device to a name at boot
# Format: name  device-or-UUID  key-file  options
secure-data  UUID=a1b2c3d4-e5f6-7890-abcd-ef1234567890  none  luks

# If using a key file instead of interactive passphrase:
secure-data  UUID=a1b2c3d4-e5f6-7890-abcd-ef1234567890  /root/keyfile  luks
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cryptsetup: ERROR: Device UUID=a1b2c3d4-e5f6-7890-abcd-ef1234567890 not found.` | Verify the UUID matches the actual encrypted device using `blkid` and correct the entry in `/etc/crypttab`. |
    | `cryptsetup: ERROR: Keyfile /root/keyfile does not exist or is not readable.` | Ensure the keyfile exists and has restrictive permissions (`chmod 600 /root/keyfile`) and is readable by root. |
```bash
# /etc/fstab — mount the mapped device
/dev/mapper/secure-data  /mnt/secure-data  xfs  defaults,_netdev  0 0
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `mount: /mnt/secure-data: special device /dev/mapper/secure-data does not exist.` | Ensure the LUKS volume is unlocked with `cryptsetup luksOpen /dev/sdXN secure-data` before mounting or at boot via crypttab. |
    | `mount: /mnt/secure-data: mount point does not exist.` | Create the mount directory with `mkdir -p /mnt/secure-data` before attempting to mount. |
```bash
# Test without rebooting
systemctl daemon-reload
systemctl start systemd-cryptsetup@secure-data
mount /mnt/secure-data
```

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Failed to start systemd-cryptsetup@secure-data.service: Unit systemd-cryptsetup@secure-data.service not found.` | Verify the encrypted device is defined in `/etc/crypttab` with the correct name `secure-data`. |
    | `mount: /mnt/secure-data: special device /dev/mapper/secure-data does not exist.` | Ensure the cryptsetup unit started successfully by checking `systemctl status systemd-cryptsetup@secure-data` before attempting to mount. |
```bash
# Backup header to a secure location
cryptsetup luksHeaderBackup /dev/sdb --header-backup-file /secure-backup/sdb-luks-header.bak

# Restore header if needed
cryptsetup luksHeaderRestore /dev/sdb --header-backup-file /secure-backup/sdb-luks-header.bak
```

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Device /dev/sdb is in use.` | Close all open file handles to the device with `lsof /dev/sdb` and unmount it with `umount /dev/sdb` before running the command. |
    | `No such file or directory` | Ensure the backup directory `/secure-backup/` exists and is writable by running `mkdir -p /secure-backup/` with appropriate permissions. |
    | `No key available with this passphrase.` | Verify you are using the correct LUKS passphrase or keyfile when restoring the header. |
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

```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu 19 Dec 2024 14:22:18 UTC.
Dependencies resolved.
================================================================================
 Package              Arch         Version              Repository       Size
================================================================================
Installing:
 tang                 x86_64       15-1.el9             appstream       48 k

Transaction Summary
================================================================================
Install  1 Package

Total download size: 48 k
Installed size: 156 k
Downloading Packages:
[100%] tang-15-1.el9.x86_64.rpm                    1.2 MB/s |  48 kB     00:00
Running transaction
Preparing        :                                                        1/1
Installing       : tang-15-1.el9.x86_64                                  1/1
Verifying        : tang-15-1.el9.x86_64                                  1/1

Installed:
  tang-15-1.el9.x86_64

Created symlink /etc/systemd/system/sockets.target.wants/tangd.socket → /usr/lib/systemd/system/tangd.socket.
.  ..  .  ..  d7c6f4e2b9a1  5f8e3c1a2b7d

{"kty":"EC","crv":"P-521","x":"MQ1vK8pL...","y":"nZ9xQ2aB...","kid":"d7c6f4e2b9a1"}
{"kty":"EC","crv":"P-521","x":"aB7cN4mK...","y":"pQ3rS5tU...","kid":"5f8e3c1a2b7d"}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `dnf: command not found` | Verify you are on a RHEL/CentOS/Fedora system; on Debian-based systems use `apt install tang` instead. |
    | `Error getting authority: Could not connect to system bus` | Run commands with `sudo` or as root to allow systemctl to access the system bus. |
    | `Failed to enable unit: Unit /etc/systemd/system/tangd.socket is masked` | Unmask the unit with `systemctl unmask tangd.socket` before enabling it. |
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

```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu 19 Dec 2024 14:22:18 UTC.
Dependencies resolved.
================================================================================
 Package                    Arch       Version              Repository    Size
================================================================================
Installing:
 clevis                     x86_64     15-1.el9             appstream    45 kB
 clevis-luks                x86_64     15-1.el9             appstream    28 kB
 clevis-dracut              x86_64     15-1.el9             appstream    12 kB

Transaction Summary
================================================================================
Install  3 Packages

Total download size: 85 kB
Installed size: 187 kB
Downloading Packages:
[100%] Complete!
Installing : clevis-15-1.el9.x86_64                                       1/3
Installing : clevis-luks-15-1.el9.x86_64                                   2/3
Installing : clevis-dracut-15-1.el9.x86_64                                 3/3
Complete!

The following disk will be bound to a Tang server:
  /dev/sdb
Binding to Tang server at http://tang.example.local
Advertising key with thumbprint: <thumbprint>
Binding successful. LUKS slot 1 assigned.

1: tang '{"url":"http://tang.example.local","thp":"<thumbprint>"}'

Rebuilding /boot/initramfs-5.14.0-427.13.1.el9_2.x86_64.img
dracut: Executing: /usr/lib/dracut/dracut-install -D /var/tmp/dracut.aBcD1234/initramfs
dracut: *** Including module: clevis ***
dracut: *** Including module: crypt ***
dracut: *** Including module: lvm ***
dracut: *** Creating image: /boot/initramfs-5.14.0-427.13.1.el9_2.x86_64.img ***
dracut: *** Creating initramfs image complete ***
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error connecting to Tang server at http://tang.example.local: Connection refused` | Verify the Tang server is running and accessible at the specified URL and port (default 80). |
    | `clevis: error: LUKS device /dev/sdb not found` | Confirm the device path is correct and the LUKS volume exists with `cryptsetup luksDump /dev/sdb`. |
    | `dracut: FAILED to install a file: /usr/lib/clevis/clevis-luks-askpass` | Reinstall clevis-dracut with `dnf reinstall clevis-dracut` to ensure all dracut modules are properly installed. |
```bash
# Bind to two Tang servers — unlock if either is reachable (threshold: 1 of 2)
clevis luks bind -d /dev/sdb sss '{"t":1,"pins":{"tang":[{"url":"http://tang1.example.local","thp":"<thp1>"},{"url":"http://tang2.example.local","thp":"<thp2>"}]}}'
```

```text title="Expected output"
The disk /dev/sdb will now be bound with the following policy:
  Encryption: luks
  Pinning: sss
  Policy: {"t":1,"pins":{"tang":[{"url":"http://tang1.example.local","thp":"<thp1>"},{"url":"http://tang2.example.local","thp":"<thp2>"}]}}

Enter existing LUKS password: 
Binding successful. LUKS slot 1 assigned.
Tang server 1 (tang1.example.local) — key exchange successful
Tang server 2 (tang2.example.local) — key exchange successful
Threshold policy: 1 of 2 Tang servers required for unlock
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: No key material found. Is the LUKS device already bound?` | Ensure the LUKS device is initialized with `cryptsetup luksFormat` before binding, or use a different slot with `clevis luks bind -s <slot>`. |
    | `Error connecting to http://tang1.example.local: Name or service not known` | Verify Tang server hostnames are resolvable and reachable from the system; check DNS and network connectivity to both Tang endpoints. |
    | `Error: Invalid JSON policy` | Validate the JSON syntax in the policy string, ensuring all quotes are properly escaped and the threshold value `t` does not exceed the number of Tang servers defined. |
```bash
# Manually test that Clevis can unlock the device
clevis luks unlock -d /dev/sdb

# Check that Tang is reachable
curl http://tang.example.local/adv
```

```text title="Expected output"
The Clevis LUKS unlock command will prompt for the LUKS passphrase and then attempt network-based decryption:

Enter passphrase for /dev/sdb: 
Device /dev/sdb unlocked successfully
Mapping created at /dev/mapper/sdb_crypt

The Tang server advertisement check returns JSON:
{"protected":"eyJhbGciOiJFQ0RILUVTK0ExMjhLVyIsImN0eSI6IkpXVCIsImVuYyI6IkExMjhHQ00iLCJraWQiOiJBWEhfTVhSVEJfNkJqMHVGVjBXQkJTQjBQQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQjBCQj
```
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

```text title="Expected output"
Generating RSA private key, 4096 bit long modulus (2 primes)
.....................................................................++++
...........................................................................................................++++
e is 65537 (0x010001)
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are a number of fields but you are only some will be populated
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are a number of fields but you are only some will be populated
-----
        Subject: CN = server01.example.local, O = Corp, C = GB
        Issuer: CN = server01.example.local
        Not After : Dec 20 14:32:18 2025 GMT
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `openssl: No such file or directory` | Install OpenSSL with `yum install openssl` (RHEL/CentOS) or `apt install openssl` (Debian/Ubuntu). |
    | `Permission denied` | Run the commands with `sudo` or as root, since `/etc/pki/tls/` requires elevated privileges. |
    | `No such file or directory` | Create the required directories first with `mkdir -p /etc/pki/tls/{private,certs,misc}`. |
```bash
# Check certificate presented by a service
openssl s_client -connect server01.example.local:443 -servername server01.example.local </dev/null 2>/dev/null | openssl x509 -noout -text | grep -E "Subject:|Not After"

# Test with specific TLS version
openssl s_client -connect server01.example.local:443 -tls1_3

# Check expiry date
echo | openssl s_client -connect server01.example.local:443 2>/dev/null | openssl x509 -noout -dates
```
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

```text title="Expected output"
DEFAULT
Setting crypto policy to DEFAULT
Note: System-wide crypto policies are applied on next application start.
Redirecting to /bin/systemctl restart sshd
Redirecting to /bin/systemctl restart nginx
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `update-crypto-policies: command not found` | Install the crypto-policies package with `sudo yum install crypto-policies` or `sudo apt install crypto-policies`. |
    | `Failed to restart sshd: Unit sshd.service not found.` | Verify the SSH service name with `systemctl list-unit-files | grep ssh` and use the correct unit name in the restart command. |
    | `Error: Policy 'FUTURE' is not available on this system.` | Update the crypto-policies package to the latest version with `sudo yum update crypto-policies` to access newer policy levels. |
```bash
# Configure encrypted swap in /etc/crypttab
# Using random key — cleared on reboot, no data persistence needed
# /etc/crypttab:
swap  /dev/sda2  /dev/urandom  swap,cipher=aes-xts-plain64,size=512

# /etc/fstab:
/dev/mapper/swap  none  swap  sw  0 0
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cryptsetup: error while loading shared libraries: libcryptsetup.so.12: cannot open shared object file` | Install libcryptsetup-dev or cryptsetup package with `apt-get install cryptsetup` (Debian/Ubuntu) or `dnf install cryptsetup` (RHEL/Fedora). |
    | `swapon: /dev/mapper/swap: read-only file system` | Ensure the root filesystem is mounted read-write during boot; if in read-only mode, remount with `mount -o remount,rw /`. |
    | `cryptsetup: No such file or directory: /dev/sda2` | Verify the correct block device path with `lsblk` or `fdisk -l` and update `/etc/crypttab` with the actual device name. |
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

```text title="Expected output"
gpg: checking the trustdb
gpg: marginals needed: 3  completes needed: 1  trust model: pgp
gpg: depth: 0  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 0u
gpg: next trustdb check due at 2025-08-14
pub   rsa4096/A7F3B2C1 2024-01-15
      Key fingerprint = 4A2E 9F1D B8C3 7E5A 6F2B  A9D4 C1E7 3F8B 2A5C 9D6E
uid                   John Smith <jsmith@corp.local>
sub   rsa4096/E2D9F4A8 2024-01-15

gpg: encrypted with 4096-bit RSA key, ID E2D9F4A8, created 2024-01-15
      "John Smith <jsmith@corp.local>"

Enter passphrase:
gpg: AES256 encrypted data
(no output — command completes silently)

gpg: signing as A7F3B2C1
gpg: encrypting for "John Smith <jsmith@corp.local>"
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `gpg: error reading key: No public key` | Import the recipient's public key first using `gpg --import recipient-pubkey.asc`. |
    | `gpg: decryption failed: No secret key` | Ensure your private key is available in your keyring; verify with `gpg --list-secret-keys`. |
    | `gpg: WARNING: no command supplied. Trying to guess what you meant ...` | Specify an explicit action flag like `--encrypt`, `--decrypt`, or `--symmetric` before the filename. |
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

```d2
direction: down

network_controls: "Network Controls" {shape: rectangle}
os_hardening: "OS Hardening" {shape: rectangle}
application_security: "Application Security" {shape: rectangle}
audit_monitoring: "Audit & Monitoring" {shape: rectangle}

network_controls -> os_hardening: hardens
os_hardening -> application_security: hardens
application_security -> audit_monitoring: hardens
```

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Linux — Hardening](../hardening/)
- [Linux — Authentication](../authentication/)
- [Linux — Access Control](../access-control/)
