# Cisco MDS Security

MDS management is hardened by disabling unused services including Telnet, HTTP, and TFTP, leaving SSH and HTTPS as the only access methods. AAA is configured with RADIUS or TACACS+ pointing to Active Directory, with local `admin` account retained as break-glass only. Role-based access uses NX-OS built-in roles: `network-admin` for full access, `network-operator` for read-only, and `san-admin` for SAN-specific operations. VSAN isolation provides security zone separation, ensuring hosts in different VSANs cannot communicate without explicit routing policy. IP ACLs on the management interface restrict access to the management network subnet only.

| Control | Implementation |
|---|---|
| Management protocols | SSH, HTTPS only (Telnet/HTTP/TFTP disabled) |
| AAA | TACACS+/RADIUS to Active Directory |
| RBAC | network-admin, network-operator, san-admin |
| VSAN isolation | Separate name servers and zone DBs per VSAN |
| Management ACL | IP ACL restricting mgmt interface to mgmt subnet |
| Audit logging | NX-OS accounting log for all config commands |
