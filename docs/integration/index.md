# Integration

References for infrastructure service integrations and connectivity patterns.


```
┌─────────────────────── Integration — API, Certificate, Directory, Email & NTP ────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Integration references: patterns for connecting infrastructure to shared services       │   │
│   │        Covers: REST API auth, CA trust store setup, LDAP/AD directory, SMTP relay, NTP        │   │
│   │   External connectivity: outbound proxy config, firewall rules, service integration patterns  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Identity & Certs      │  │       Network Services      │  │       App Integrations      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │      LDAP/AD directory      │  │        NTP hierarchy        │  │       ServiceNow CMDB       │   │
│   │       CA trust stores       │  │      SMTP relay config      │  │      Monitoring agents      │   │
│   │      API auth patterns      │  │        DNS resolution       │  │     SIEM log forwarding     │   │
│   │       TLS cert install      │  │         Proxy config        │  │       Backup agent reg      │   │
│   │      SAML/SSO patterns      │  │        Firewall rules       │  │      Ticketing webhooks     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    LDAP         = Lightweight Directory Access Protocol; query AD for user/group membership           │
│    LDAPS        = LDAP over TLS; use port 636; never send credentials over plain LDAP                 │
│    Trust store  = OS/app certificate store; CA cert must be here for TLS validation to succeed        │
│    NTP stratum  = Distance from reference clock; stratum 0 = atomic; infra uses stratum 2-3           │
│    SMTP relay   = Mail server that forwards alerts; authenticated relay prevents open relay abuse     │
│    mTLS         = Mutual TLS; both sides present certificates; service-to-service auth                │
│    Proxy        = Outbound HTTP/HTTPS forwarder; set http_proxy env var for CLI tools                 │
│    SAML         = Federated SSO standard; IdP issues assertions; SP trusts them                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="api-connectivity/"><strong>API Connectivity</strong><span>Testing and troubleshooting REST API connectivity, authentication, and TLS certificate validation.</span></a>
<a class="kb-card" href="certificate-trust/"><strong>Certificate Trust</strong><span>Adding CA certificates to trust stores on Linux, Windows, and infrastructure appliances.</span></a>
<a class="kb-card" href="directory-integration/"><strong>Directory Integration</strong><span>LDAP/LDAPS integration with Active Directory for authentication and group membership.</span></a>
<a class="kb-card" href="email-relay/"><strong>Email Relay</strong><span>SMTP relay configuration for infrastructure alerts, monitoring notifications, and appliances.</span></a>
<a class="kb-card" href="external-connectivity/"><strong>External Connectivity</strong><span>Outbound internet access requirements, proxy configuration, and firewall rule documentation.</span></a>
<a class="kb-card" href="service-integrations/"><strong>Service Integrations</strong><span>ServiceNow, monitoring, backup, and SIEM integration patterns for infrastructure components.</span></a>
<a class="kb-card" href="time-synchronization/"><strong>Time Synchronization</strong><span>NTP hierarchy design, stratum configuration, and drift troubleshooting across all platforms.</span></a>
</div>
