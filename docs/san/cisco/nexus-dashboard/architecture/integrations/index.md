# Cisco Nexus Dashboard — Architecture Integrations

```bash
# SSH to any ND cluster node
ssh ndadmin@nd-node1.corp.example.com

# Configure syslog forwarding via ND CLI
acs system syslog add --server 10.10.3.50 --port 514 --protocol udp

# Verify
acs system syslog show
```

```text
┌────────────────────────── Cisco Nexus Dashboard — Architecture Integrations ──────────────────────────┐
│                                                                                                       │
│  ND integrates with identity providers, SIEM, monitoring tools, and cloud platforms.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Identity Integrations             │  │           Monitoring Integrations           │   │
│   │            LDAP: user/group sync             │  │           Syslog: event forwarding          │   │
│   │               RADIUS: AAA auth               │  │            SNMP: trap generation            │   │
│   │         TACACS+: per-cmd accounting          │  │           Webhook: alert delivery           │   │
│   │            SAML 2.0: SSO with IdP            │  │           Email: SMTP notification          │   │
│   │          Cisco ISE: device posture           │  │           Splunk/SIEM: syslog TLS           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  IdP and AAA integrate at cluster level; monitoring integrations are per-app                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Cloud Integrations              │  │               Cisco Ecosystem               │   │
│   │         Intersight: infra management         │  │           APIC: ACI policy source           │   │
│   │          AWS/Azure: cloud site add           │  │          DCNM/NDFC: SAN/LAN fabric          │   │
│   │           VMware vCenter: VM aware           │  │          Tetration/Secure Workload          │   │
│   │         Terraform: infra-as-code API         │  │         ThousandEyes: WAN assurance         │   │
│   │         REST API: programmable mgmt          │  │          AppDynamics: app telemetry         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster · IdP/AAA server · SIEM · Intersight · cloud connectors · APIC cluster                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SAML 2.0       = Security Assertion Markup Language; federated SSO protocol                          │
│  Intersight     = Cisco cloud management SaaS for UCS and HCI infrastructure                          │
│  Tetration      = Cisco workload security analytics (now Secure Workload)                             │
│  ThousandEyes   = Cisco network intelligence platform for WAN path monitoring                         │
│  AppDynamics    = Cisco APM platform; correlates app and network performance                          │
│  ISE            = Identity Services Engine; network access policy and posture                         │
│  REST API       = Representational State Transfer API; ND primary programmability                     │
│  Terraform      = IaC tool; Cisco ND provider available for automation                                │
│  APIC           = Application Policy Infrastructure Controller; manages ACI fabric                    │
│  Webhook        = HTTP callback delivering alert payload to external systems                          │
│  Syslog TLS     = Encrypted syslog transport using TLS to SIEM                                        │
│  VM-aware       = ND correlates network paths with vCenter VM identifiers                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
