# Confluence — Encryption

TLS configuration, data at rest encryption, attachment storage security, and database encryption.

## TLS — Encryption in Transit

All Confluence traffic should be served over HTTPS. TLS termination can occur at Confluence directly (via the embedded Tomcat), or at a reverse proxy (Nginx, Apache, load balancer).

### TLS at a Reverse Proxy (Recommended)

Running TLS termination at a reverse proxy is the preferred approach. It simplifies certificate management and keeps the Java keystore simple.

```nginx
# /etc/nginx/conf.d/confluence.conf
server {
    listen 80;
    server_name confluence.corp.local;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name confluence.corp.local;

    ssl_certificate     /etc/pki/tls/certs/confluence.crt;
    ssl_certificate_key /etc/pki/tls/private/confluence.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;

    location / {
        proxy_pass http://127.0.0.1:8090;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

```bash
# Verify TLS configuration
openssl s_client -connect confluence.corp.local:443 -tls1_3 </dev/null 2>/dev/null | \
  openssl x509 -noout -subject -dates

# Check for weak protocol support (should fail)
openssl s_client -connect confluence.corp.local:443 -tls1 </dev/null 2>&1 | grep "handshake failure"
openssl s_client -connect confluence.corp.local:443 -tls1_1 </dev/null 2>&1 | grep "handshake failure"
```

### TLS at Tomcat (Direct Confluence)

If not using a reverse proxy, configure TLS in Confluence's embedded Tomcat:

```bash
# Generate a certificate and import into a Java keystore
keytool -genkeypair -alias confluence \
  -keyalg RSA -keysize 4096 \
  -validity 365 \
  -keystore /opt/atlassian/confluence/conf/keystore.jks \
  -storepass changeit \
  -dname "CN=confluence.corp.local,O=Corp,C=GB"

# Import a CA-signed certificate
keytool -importcert -alias corp-ca \
  -file /tmp/corp-ca.cer \
  -keystore /opt/atlassian/confluence/conf/keystore.jks \
  -storepass changeit -noprompt
```

```xml
<!-- /opt/atlassian/confluence/conf/server.xml — SSL Connector -->
<Connector port="8443" maxHttpHeaderSize="8192"
           maxThreads="150" minSpareThreads="25" maxSpareThreads="75"
           enableLookups="false" disableUploadTimeout="true"
           acceptCount="100" scheme="https" secure="true"
           sslProtocol="TLSv1.2+TLSv1.3"
           clientAuth="false"
           sslEnabledProtocols="TLSv1.2,TLSv1.3"
           ciphers="TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
           keystoreFile="/opt/atlassian/confluence/conf/keystore.jks"
           keystorePass="changeit" />
```

## Database Encryption

Confluence stores all content (pages, comments, attachments metadata) in its database. Protect the database connection and data at rest.

### Encrypted Database Connection

```xml
<!-- /opt/atlassian/confluence/confluence/WEB-INF/classes/confluence-init.properties -->
<!-- Ensure JDBC URL uses SSL -->
```

```
# /var/atlassian/application-data/confluence/confluence.cfg.xml
# Ensure the JDBC URL includes SSL parameters:
jdbc:postgresql://dbserver.corp.local:5432/confluence?ssl=true&sslmode=require

# For MySQL:
jdbc:mysql://dbserver.corp.local:3306/confluence?useSSL=true&requireSSL=true
```

### Database Password Encryption

```bash
# Store the database password encrypted in confluence.cfg.xml
# Use Confluence's built-in password encoding tool
/opt/atlassian/confluence/bin/atlas-util.sh encrypt-password

# The encoded password is stored in confluence.cfg.xml as:
# <property name="hibernate.connection.password">{AES}EncryptedValue=</property>
```

### Database at Rest Encryption

Database-level encryption is handled at the database server, not by Confluence directly:

```sql
-- PostgreSQL with pgcrypto (column-level encryption example)
-- Prefer Transparent Data Encryption (TDE) at the storage layer

-- MySQL InnoDB TDE (MySQL Enterprise)
-- ALTER TABLE tablespace ENCRYPTION='Y';

-- PostgreSQL — use filesystem-level encryption (LUKS on the data partition)
-- or pgcrypto for sensitive column encryption
```

## Attachment Storage Encryption

Confluence stores file attachments on the filesystem (by default under `<confluence-home>/attachments/`).

### Filesystem-Level Encryption (Linux)

```bash
# The attachment directory should be on an encrypted volume (LUKS)
# Verify the attachment directory location
grep "attachments" /var/atlassian/application-data/confluence/confluence.cfg.xml

# Check if the directory is on an encrypted mount
df /var/atlassian/application-data/confluence/attachments/
mount | grep "$(df /var/atlassian/application-data/confluence/attachments/ | tail -1 | awk '{print $1}')"

# If not on encrypted storage, move attachments to an encrypted mount:
# 1. Stop Confluence
systemctl stop confluence

# 2. Move attachments to encrypted mount
rsync -avz /var/atlassian/application-data/confluence/attachments/ /secure/confluence-attachments/

# 3. Update attachment path in confluence.cfg.xml
# <property name="attachments.dir">/secure/confluence-attachments</property>

# 4. Start Confluence
systemctl start confluence
```

### Windows — BitLocker for Attachment Storage

```powershell
# If Confluence is running on Windows, ensure the attachment volume is BitLocker-encrypted
Get-BitLockerVolume -MountPoint "D:" | Select-Object VolumeStatus, ProtectionStatus

# Verify attachment directory location
Get-Content "C:\ProgramData\Atlassian\Application Data\Confluence\confluence.cfg.xml" |
  Select-String "attachments.dir"
```

## Backup Encryption

Confluence backups contain all content and must be encrypted.

```bash
# Encrypt a Confluence backup archive with GPG
gpg --symmetric --cipher-algo AES256 /backups/confluence-backup-2026-05-07.zip

# Or use openssl for encryption
openssl enc -aes-256-cbc -salt -in /backups/confluence-backup.zip \
  -out /backups/confluence-backup.zip.enc \
  -pass file:/secure/backup-passphrase.txt

# Verify the encrypted backup can be decrypted
openssl enc -d -aes-256-cbc \
  -in /backups/confluence-backup.zip.enc \
  -out /tmp/test-decrypt.zip \
  -pass file:/secure/backup-passphrase.txt
ls -la /tmp/test-decrypt.zip
```

## Cookie and Session Security

```
Confluence security properties (General Configuration > Security Configuration):
- Secure flag on cookies: Enabled (cookies sent only over HTTPS)
- HttpOnly flag: Enabled (JavaScript cannot read session cookies)
- Content Security Policy: Configure via reverse proxy headers
```

```nginx
# Nginx — security headers for Confluence
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

## Encryption Audit

```bash
# Verify HTTPS enforced (HTTP redirects to HTTPS)
curl -I http://confluence.corp.local/ 2>/dev/null | grep "Location:"
# Should redirect to https://

# Verify TLS version
nmap --script ssl-enum-ciphers -p 443 confluence.corp.local | grep -E "TLS|SSLv"

# Verify certificate is valid and not self-signed
openssl s_client -connect confluence.corp.local:443 </dev/null 2>/dev/null | \
  openssl x509 -noout -issuer -subject -dates

# Verify database connection uses SSL
grep -i "ssl\|encrypt" /var/atlassian/application-data/confluence/confluence.cfg.xml

# Verify attachment directory is on encrypted storage
lsblk -o NAME,TYPE,MOUNTPOINT | grep crypt
mount | grep "/secure\|/encrypted"

# Check backup files are encrypted (should not be plain zip)
file /backups/confluence-backup-*.zip* | grep -v "Zip archive"
```

## Quick Reference

| Topic | Location / Command |
|---|---|
| TLS certificate (Nginx) | `/etc/nginx/conf.d/confluence.conf` |
| TLS certificate (Tomcat) | `/opt/atlassian/confluence/conf/server.xml` |
| Java truststore | `/opt/atlassian/confluence/jre/lib/security/cacerts` |
| Database JDBC URL | `/var/atlassian/.../confluence.cfg.xml` |
| Attachment directory | `<confluence-home>/attachments/` (configurable in cfg.xml) |
| Cookie security | General Configuration > Security Configuration |
| Verify TLS ciphers | `nmap --script ssl-enum-ciphers -p 443 <host>` |
| Backup encryption | `gpg --symmetric` or `openssl enc -aes-256-cbc` |
