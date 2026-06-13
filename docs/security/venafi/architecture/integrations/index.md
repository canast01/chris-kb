---
tags:
  - architecture
  - security
---
# Venafi — Integrations


<div class="kb-summary">
Venafi TPP integrates with Microsoft ADCS as the primary internal CA backend, with DigiCert and Entrust for external and public certificate issuance.
</div>
```text
┌───────────────────────────── Security Venafi Architecture — Integrations ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Venafi integrations: VMware vSphere, Kubernetes CSI, backup software, and monitoring     │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │ API: Security Venafi Architecture management console REST API enables automation and third-pa │   │
│   │             Plug-ins available for vCenter, OpenShift, Splunk, and SIEM platforms             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Venafi → REST API / plug-ins → VMware / K8s / backup / monitoring                                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Security Venafi Architecture infrastructure · management network · monitoring            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Venafi             = Security Venafi Architecture platform overview and core concepts              │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


 HashiCorp Vault PKI secrets engine can be fronted by Venafi policy to enforce organisational standards on dynamically issued certificates. Kubernetes cert-manager uses the Venafi issuer plugin to request certificates from TPP or VaaS for workloads running in-cluster.

ServiceNow integration enables certificate request workflows via ITSM tickets, routing requests through approval before Venafi issues. SIEM integration is achieved via the Venafi Log Server forwarding audit events. A Terraform provider is available for certificate provisioning as part of infrastructure-as-code pipelines.

| Integration | Method | Purpose |
|---|---|---|
| Microsoft ADCS | CA driver in TPP | Internal certificate issuance |
| DigiCert / Entrust | CA driver in TPP | External / public certificate issuance |
| HashiCorp Vault PKI | Venafi policy enforcement layer | Standards enforcement on dynamic PKI |
| Kubernetes cert-manager | Venafi issuer plugin | In-cluster certificate provisioning |
| ServiceNow | REST API / workflow connector | Certificate request approval workflow |
| SIEM | Venafi Log Server syslog forwarding | Audit event centralisation |
| Terraform | Venafi Terraform provider | Certificate provisioning in IaC pipelines |
