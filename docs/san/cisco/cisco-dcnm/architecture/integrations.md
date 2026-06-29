---
tags:
  - architecture
  - san
---
# Cisco DCNM — Integrations
![Cisco DCNM — Integrations](../../../../assets/san-cisco-cisco-dcnm-architecture-integrations.svg)

```bash
# On DCNM appliance
ssh root@dcnm-mgmt.corp.example.com

# Configure syslog forwarding (rsyslog)
cat >> /etc/rsyslog.d/dcnm-forward.conf << 'EOF'
# Forward DCNM application logs to SIEM
local0.* @10.10.3.50:514
*.err @@10.10.3.50:514
EOF

systemctl restart rsyslog
logger -p local0.info -t dcnm "Test message"
# Verify arrival at SIEM
```


```text title="Expected output"
root@dcnm-mgmt:~# ssh root@dcnm-mgmt.corp.example.com
root@dcnm-mgmt:~# cat >> /etc/rsyslog.d/dcnm-forward.conf << 'EOF'
> # Forward DCNM application logs to SIEM
> local0.* @10.10.3.50:514
> *.err @@10.10.3.50:514
> EOF
root@dcnm-mgmt:~# systemctl restart rsyslog
root@dcnm-mgmt:~# logger -p local0.info -t dcnm "Test message"
root@dcnm-mgmt:~# tail -f /var/log/syslog | grep dcnm
Jan 15 14:23:47 dcnm-mgmt dcnm[4521]: Test message
```

!!! warning "Common errors"
    **`bash: /etc/rsyslog.d/dcnm-forward.conf: Permission denied`** — Ensure you are logged in as root or use `sudo` to write to the rsyslog configuration directory.
    **`Job for rsyslog.service failed because the control process exited with error code.`** — Validate the rsyslog configuration syntax with `rsyslog -N1` before restarting the service.
    **`connect(10.10.3.50:514): Connection refused`** — Verify the SIEM syslog receiver is running and listening on UDP/TCP port 514 with `netstat -tuln | grep 514` on the SIEM host.
---

## See also

- [Cisco Dcnm — How It Works](../how-it-works/)
- [Cisco Dcnm — Design Standards](../design-standards/)
