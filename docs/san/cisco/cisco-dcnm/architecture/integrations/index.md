# Cisco DCNM — Integrations

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
```text
┌────────────────────────────────────── Cisco DCNM — Integrations ──────────────────────────────────────┐
│                                                                                                       │
│  DCNM integrates with Cisco ISE, SIEM, REST automation, CMDB, and NTP/SMTP.                           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Identity & Auth Integrations         │  │           Monitoring Integrations           │   │
│   │          Cisco ISE: TACACS+/RADIUS           │  │       SNMP trap to NMS (CW/Solarwinds)      │   │
│   │          LDAP: AD group-to-role map          │  │          Syslog: SIEM Splunk/QRadar         │   │
│   │         RADIUS: fallback auth method         │  │             Email: SMTP alerting            │   │
│   │        Local accounts: emergency only        │  │           REST webhook: event push          │   │
│   │            SSO: SAML 2.0 via IdP             │  │          Grafana: REST data source          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  ISE provides centralised TACACS+; SIEM integrations forward all events for correlation.              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Automation Integrations            │  │         Infrastructure Integrations         │   │
│   │           REST API: token + HTTPS            │  │        NTP: time sync for all events        │   │
│   │        Ansible: cisco.dcnm collection        │  │         DNS: switch name resolution         │   │
│   │           Terraform: DCNM provider           │  │          NFS: config backup target          │   │
│   │          ServiceNow: CMDB CI update          │  │         SCP: config archive transfer        │   │
│   │           Python requests library            │  │           vSphere: OVA VM platform          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DCNM VM · management Ethernet · Cisco ISE appliance · NFS backup share                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cisco ISE       = Identity Services Engine; TACACS+ + RADIUS for Cisco devices                       │
│  TACACS+         = Terminal Access Controller; centralised CLI + GUI auth for DCNM                    │
│  LDAP            = Lightweight Directory Access Protocol; AD group to DCNM role map                   │
│  SAML 2.0        = Security Assertion Markup Language; SSO federation for DCNM GUI                    │
│  REST API        = DCNM northbound API; JSON/HTTPS with token authentication                          │
│  cisco.dcnm      = Ansible Galaxy collection; modules for DCNM automation                             │
│  Terraform       = HashiCorp IaC; DCNM provider for zone and VLAN provisioning                        │
│  ServiceNow CMDB = CI records for MDS switches auto-synced from DCNM inventory                        │
│  SNMP trap       = DCNM forwards MDS health events to NMS (CiscoWorks/SolarWinds)                     │
│  Syslog          = DCNM forwards audit and health events to SIEM for correlation                      │
│  NFS backup      = DCNM config/DB backup to NFS; scheduled nightly                                    │
│  NTP             = Network Time Protocol; required for correlated event timestamps                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
