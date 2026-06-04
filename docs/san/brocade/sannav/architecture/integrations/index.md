# Brocade SANnav — Integrations

```bash
# SSH to SANnav appliance
ssh admin@sannav-mgmt.corp.example.com

# Edit rsyslog configuration
sudo vi /etc/rsyslog.d/sannav-forward.conf

# Add:
*.* @10.10.3.50:514        # UDP syslog
# or
*.* @@10.10.3.50:514       # TCP syslog (more reliable)

# Restart rsyslog
sudo systemctl restart rsyslog

# Verify forwarding
logger -t sannav-test "Test syslog message from SANnav"
# Check SIEM for the test message
```text
┌──────────────────────────────────── Brocade SANnav — Integrations ────────────────────────────────────┐
│                                                                                                       │
│  SANnav integrates with SIEM, TACACS+, SNMP NMS, REST automation, and NTP/SMTP.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Identity & Auth Integrations         │  │           Monitoring Integrations           │   │
│   │           TACACS+: admin user auth           │  │          SNMP trap to NMS (HPE/IBM)         │   │
│   │          LDAP: group-based role map          │  │        syslog to SIEM (Splunk/QRadar)       │   │
│   │         RADIUS: fallback auth option         │  │         Email: SMTP alert forwarding        │   │
│   │            SSO: SAML 2.0 support             │  │           Webhook: REST event push          │   │
│   │        Local accounts: fallback only         │  │           Grafana: API data source          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Auth integrations centralise login; monitoring integrations feed SIEM and NMS.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Automation Integrations            │  │         Infrastructure Integrations         │   │
│   │           REST API: token + HTTPS            │  │          NTP: time sync for events          │   │
│   │          Ansible: SANnav collection          │  │         DNS: switch hostname resolve        │   │
│   │          Terraform: SANnav provider          │  │           NFS: backup destination           │   │
│   │           ServiceNow: CMDB CI sync           │  │           SCP: supportsave upload           │   │
│   │           Python requests library            │  │           vSphere: OVA VM hosting           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SANnav VM on vSphere · management Ethernet · TACACS+/LDAP server · NFS backup share                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TACACS+         = Terminal Access Controller; centralised admin auth for SANnav GUI                  │
│  LDAP            = Lightweight Directory Access Protocol; AD group-to-role mapping                    │
│  SAML 2.0        = Security Assertion Markup Language; SSO federation for SANnav                      │
│  REST API        = SANnav northbound API; JSON/HTTPS; token-based authentication                      │
│  SNMP trap       = SANnav forwards MAPS/fabric events to NMS via SNMP v2c/v3                          │
│  Webhook         = HTTP POST to external system on SANnav event trigger                               │
│  Ansible collection= Broadcom-published Ansible modules for SANnav automation                         │
│  ServiceNow CMDB = CI records for fabric switches auto-synced from SANnav inventory                   │
│  NFS backup      = SANnav config/database backup to NFS share; scheduled daily                        │
│  NTP             = Network Time Protocol; critical for correlated event timestamps                    │
│  OVA             = Open Virtual Appliance; SANnav delivered as vSphere OVA template                   │
│  SCP             = Secure Copy; used for supportsave upload and firmware transfers                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
