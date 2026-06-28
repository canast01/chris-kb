---
tags:
  - aria-networks
  - security
  - vmware
---
# vRNI Security Hardening
![vRNI Security Hardening](../../../../assets/virtualization-vmware-aria-operations-for-networks-security-.svg)

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

```bash
# On Platform VM, if no external firewall:
sudo iptables -A INPUT -p tcp --dport 443 -s 10.10.10.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j DROP
sudo iptables-save > /etc/iptables/rules.v4
```
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
