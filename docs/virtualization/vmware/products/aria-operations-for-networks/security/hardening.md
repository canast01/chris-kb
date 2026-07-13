---
tags:
  - aria-networks
  - security
  - vmware
---
# vRNI Security Hardening

*Applies to: VMware Aria 8.x*
![vRNI Security Hardening](../../../../../assets/virtualization-vmware-aria-operations-for-networks-security-.svg)

```bash
ssh ubuntu@vrni.example.local

sudo vim /etc/ssh/sshd_config
# Apply:
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers ubuntu

sudo systemctl restart sshd
```


```text title="Expected output"
ubuntu@vrni.example.local's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-42-generic x86_64)

 System load: 0.45             Processes:           127
 Usage of /: 18.2% of 19.29GB   Users logged in:     1
 Last login: Mon Jan 16 14:22:33 2025 from 192.168.1.50

ubuntu@vrni:~$ sudo vim /etc/ssh/sshd_config
(no output — command opens editor)
ubuntu@vrni:~$ sudo systemctl restart sshd
(no output — command completes silently)
ubuntu@vrni:~$
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `sshd: no hostkeys available -- exiting.` | Run `sudo ssh-keygen -A` to generate missing host keys before restarting sshd. |
    | `Permission denied (publickey).` | Ensure your public key is added to `~/.ssh/authorized_keys` on the target system before disabling password authentication. |
    | `sudo: vim: command not found` | Install vim with `sudo apt-get install vim` or use `sudo nano /etc/ssh/sshd_config` instead. |
```bash
# On Platform VM, if no external firewall:
sudo iptables -A INPUT -p tcp --dport 443 -s 10.10.10.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j DROP
sudo iptables-save > /etc/iptables/rules.v4
```

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `iptables v1.8.7 (nf_tables): Could not fetch rule set generation id: Permission denied` | Run commands with `sudo` or as root user. |
    | `iptables-save: command not found` | Install iptables-persistent package with `sudo apt-get install iptables-persistent` on Debian/Ubuntu systems. |
```bash
sudo vim /etc/nginx/nginx.conf
# Set:
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers on;

sudo nginx -t && sudo systemctl reload nginx
```
```yaml
Settings → Notifications → Syslog
  Protocol: TCP
  Host: siem.example.local
  Port: 514
  Format: RFC 5424
Enable: Audit events, Alert notifications
```
```bash
# Check current expiry
echo | openssl s_client -connect vrni.example.local:443 2>/dev/null \
  | openssl x509 -noout -enddate

# Renew 30 days before expiry via Settings → SSL Certificate → Upload
```


```text title="Expected output"
notAfter=Jan 15 12:34:56 2025 GMT
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `unable to load certificate` | Ensure the certificate file path is correct and the file contains valid PEM-encoded certificate data. |
    | `SSL: CERTIFICATE_VERIFY_FAILED` | This is expected for self-signed certificates; the command still extracts the expiry date successfully despite the verification warning. |
## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## See also

- [Aria Operations for Networks — Access Control](../access-control/)
- [Aria Operations for Networks — Authentication](../authentication/)
- [vRNI Health Checks](../../operations/health-checks/)
