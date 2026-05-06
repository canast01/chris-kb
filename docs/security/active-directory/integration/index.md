# Active Directory Integration

Active Directory serves as the central identity provider for the enterprise, with integrations spanning hybrid cloud, Linux systems, network infrastructure, security tools, and SIEM platforms. Azure AD Connect synchronises on-premises AD objects to Entra ID for hybrid identity, supporting password hash sync, pass-through authentication, or federation. Linux systems authenticate via SSSD with the `ad` provider, joining the domain with `realm join` and applying access control via `ad_access_filter`.

| Integration | Method | Notes |
|---|---|---|
| Azure AD Connect (Entra ID) | LDAP sync + writeback | Password hash sync or PTA; staged rollout supported |
| Linux (SSSD/PAM) | SSSD `ad` provider | `realm join` for domain join; `/etc/sssd/sssd.conf` for config |
| Cisco switches / MDS | TACACS+ / RADIUS to AD via NPS | NPS Network Policy maps AD groups to privilege levels |
| VMware vCenter | AD SSO integration | vCenter joined to AD domain; AD groups mapped to vCenter roles |
| CyberArk | LDAP bind to AD | CyberArk authenticates users via AD LDAP; safe access mapped to AD groups |
| Venafi | LDAP / AD group membership | Venafi TPP uses AD groups for RBAC role assignment |
| Splunk (SIEM) | Windows Event Log forwarding | Universal Forwarder on DCs ships Security log to Splunk; AD audit events 4624/4625/4740 |
