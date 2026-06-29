---
tags:
  - nsx
  - nsx-4
  - security
  - vmware
---
# NSX — Authentication
![NSX — Authentication](../../../../assets/virtualization-vmware-nsx-security-authentication.svg)

```bash
curl -sk -u 'admin:password' \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "api_failed_auth_lockout_period": 900,
    "api_failed_auth_reset_period": 900,
    "api_max_requests": 100,
    "cli_failed_auth_lockout_period": 900,
    "cli_max_auth_failures": 5,
    "minimum_password_length": 20
  }' \
  "https://<nsx-manager>/api/v1/node/aaa/auth-policy"
```


```text title="Expected output"
{
  "api_failed_auth_lockout_period": 900,
  "api_failed_auth_reset_period": 900,
  "api_max_requests": 100,
  "cli_failed_auth_lockout_period": 900,
  "cli_max_auth_failures": 5,
  "minimum_password_length": 20,
  "resource_type": "AuthenticationPolicy",
  "_self": {
    "href": "/api/v1/node/aaa/auth-policy",
    "rel": "self"
  },
  "_links": [
    {
      "href": "https://nsx-mgr-01.lab.local/api/v1/node/aaa/auth-policy",
      "rel": "self"
    }
  ],
  "_schema": "/api/v1/schema/AuthenticationPolicy"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present in the example, but ensure it's included if removed).
    **`{"httpStatus":"UNAUTHORIZED","error_code":401,"module_name":"api-service","error_message":"Invalid credentials"}`** — Verify the NSX Manager admin credentials and ensure the user has API access permissions.
    **`{"httpStatus":"NOT_FOUND","error_code":404,"module_name":"api-service","error_message":"The requested resource could not be found"}`** — Confirm the NSX Manager hostname/IP is correct and the `/api/v1/node/aaa/auth-policy` endpoint is available on this NSX version.
```bash
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"search_query": "nsxadmin", "cursor": "0"}' \
  "https://<nsx-manager>/api/v1/aaa/ldap/search"

# Expected: returns the matching user object from AD
```

```text title="Expected output"
{
  "result_count": 1,
  "results": [
    {
      "resource_type": "LdapUser",
      "display_name": "nsxadmin",
      "username": "nsxadmin",
      "email": "nsxadmin@corp.local",
      "full_name": "NSX Administrator",
      "distinguished_name": "CN=nsxadmin,OU=Service Accounts,DC=corp,DC=local",
      "object_sid": "S-1-5-21-3623811015-3361044348-30300820-1234"
    }
  ],
  "cursor": "0"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification, or use `--cacert /path/to/ca.pem` with a valid CA bundle.
    **`{"error_code": 401, "error_message": "Invalid credentials"}`** — Verify the NSX Manager admin credentials in the `-u` parameter match the actual configured user and password.
    **`{"error_code": 400, "error_message": "LDAP search not configured"}`** — Configure LDAP integration on the NSX Manager via the UI (System > Users and Roles > LDAP) before attempting LDAP searches.
```bash
# Assign Enterprise Admin role to an AD group
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "roles": [{
      "role": "enterprise_admin"
    }],
    "name": "CN=NSX-Admins,OU=Groups,DC=corp,DC=local",
    "type": "remote_group",
    "identity_source_type": "LDAP",
    "identity_source_id": "<ldap-source-id>"
  }' \
  "https://<nsx-manager>/api/v1/aaa/role-bindings"
```

```text title="Expected output"
{
  "resource_type": "RoleBinding",
  "id": "7f8c9d2e-4a1b-5c3d-8e9f-2a4b6c8d0e1f",
  "display_name": "CN=NSX-Admins,OU=Groups,DC=corp,DC=local",
  "name": "CN=NSX-Admins,OU=Groups,DC=corp,DC=local",
  "type": "remote_group",
  "identity_source_type": "LDAP",
  "identity_source_id": "ldap-source-001",
  "roles": [
    {
      "role": "enterprise_admin",
      "display_name": "Enterprise Admin"
    }
  ],
  "_self": {
    "href": "/api/v1/aaa/role-bindings/7f8c9d2e-4a1b-5c3d-8e9f-2a4b6c8d0e1f",
    "rel": "self"
  }
}
```

!!! warning "Common errors"
    **`{"httpStatus":401,"error_code":10000,"module_name":"common","error_message":"Authentication failed"}`** — Verify NSX Manager credentials and ensure the admin account has API access enabled.
    **`{"httpStatus":400,"error_code":10001,"error_message":"Invalid identity_source_id"}`** — Confirm the LDAP source ID exists by running `curl -sk -u 'admin:password' https://<nsx-manager>/api/v1/aaa/identity-sources` and use the correct ID.
    **`{"httpStatus":404,"error_code":10002,"error_message":"Role 'enterprise_admin' not found"}`** — Use a valid role name such as `enterprise_admin`, `security_admin`, or `auditor` instead.
```bash
curl -sk -u 'admin:Password123!' \
  "https://nsx-manager.example.local/api/v1/cluster/status"
```

```text title="Expected output"
{
  "cluster_status": "STABLE",
  "node_id": "550e8400-e29b-41d4-a716-446655440000",
  "control_cluster_status": {
    "status": "STABLE",
    "node_count": 3,
    "online_nodes": 3
  },
  "mgmt_cluster_status": {
    "status": "STABLE",
    "node_count": 3,
    "online_nodes": 3
  },
  "detailed_cluster_status": [
    {
      "node_id": "550e8400-e29b-41d4-a716-446655440001",
      "status": "UP",
      "role": "CONTROLLER",
      "ip": "192.168.1.10"
    },
    {
      "node_id": "550e8400-e29b-41d4-a716-446655440002",
      "status": "UP",
      "role": "CONTROLLER",
      "ip": "192.168.1.11"
    },
    {
      "node_id": "550e8400-e29b-41d4-a716-446655440003",
      "status": "UP",
      "role": "CONTROLLER",
      "ip": "192.168.1.12"
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag (already present) or import the NSX Manager's CA certificate into your system trust store.
    **`curl: (7) Failed to connect to nsx-manager.example.local port 443: Connection refused`** — Verify NSX Manager is running and accessible at the hostname/IP, and check firewall rules allow HTTPS access to port 443.
    **`{"error_code":401,"error_message":"Unauthorized"}`** — Confirm the admin credentials are correct and the user account has API access permissions in NSX Manager.
```bash
# Create session (returns Set-Cookie header)
curl -sk -u 'admin:Password123!' \
  -X POST \
  -c /tmp/nsx-session.txt \
  "https://nsx-manager.example.local/api/v1/aaa/session"

# Use session cookie for subsequent requests
curl -sk \
  -b /tmp/nsx-session.txt \
  "https://nsx-manager.example.local/api/v1/cluster/status"

# Invalidate session when done
curl -sk -u 'admin:Password123!' \
  -X DELETE \
  -b /tmp/nsx-session.txt \
  "https://nsx-manager.example.local/api/v1/aaa/session"
```

```text title="Expected output"
{
  "session_timeout": 1800,
  "user": "admin",
  "roles": ["enterprise_admin"],
  "session_id": "a7f3c2e1-9b4d-47e8-b2f6-8c1d5a9e3f2b"
}
{
  "cluster_status": "STABLE",
  "node_count": 3,
  "nodes": [
    {
      "uuid": "550e8400-e29b-41d4-a716-446655440001",
      "hostname": "nsx-node-01.example.local",
      "status": "UP",
      "role": "MASTER"
    },
    {
      "uuid": "550e8400-e29b-41d4-a716-446655440002",
      "hostname": "nsx-node-02.example.local",
      "status": "UP",
      "role": "FOLLOWER"
    },
    {
      "uuid": "550e8400-e29b-41d4-a716-446655440003",
      "hostname": "nsx-node-03.example.local",
      "status": "UP",
      "role": "FOLLOWER"
    }
  ]
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification (already present; verify NSX manager certificate is accessible or use `--cacert` with proper CA bundle).
    **`{"httpStatus":"UNAUTHORIZED","error_code":401,"module_error_details":"The credentials supplied to the API were invalid","error_message":"The credentials supplied to the API were invalid"}`** — Verify admin username and password are correct and the user has API access permissions in NSX.
```bash
# Generate client key and CSR
openssl req -newkey rsa:2048 -nodes \
  -keyout nsx-automation.key \
  -out nsx-automation.csr \
  -subj "/CN=nsx-automation/O=corp"

# Submit CSR to internal CA and get certificate (nsx-automation.crt)

# Register the certificate with NSX Manager
curl -sk -u 'admin:Password123!' \
  -X POST \
  -H "Content-Type: application/json" \
  -d "{
    \"pem_encoded\": \"$(cat nsx-automation.crt | awk '{printf \"%s\\\\n\", $0}')\"
  }" \
  "https://nsx-manager.example.local/api/v1/trust-management/certificates?action=import"

# Bind the certificate to a principal identity (service account)
curl -sk -u 'admin:Password123!' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "name": "automation-account",
    "node_id": "automation-host-01",
    "role": "network_engineer",
    "certificate_id": "<cert-id-from-above>",
    "is_protected": true
  }' \
  "https://nsx-manager.example.local/api/v1/aaa/principal-identities"

# Use certificate for API calls (no password needed)
curl -sk \
  --cert nsx-automation.crt \
  --key nsx-automation.key \
  "https://nsx-manager.example.local/api/v1/cluster/status"
```

```text title="Expected output"
Generating RSA private key, 2048 bit long modulus (2 primes)
.......................................................................+++++
.......................+++++
e is 65537 (0x010001)

{
  "resource_type": "Certificate",
  "id": "8f4c2a91-7e3d-4b6f-9c1a-5d8e2f7b4a9c",
  "pem_encoded": "-----BEGIN CERTIFICATE-----\nMIIDXTCCAkWgAwIBAgIJAKp7...",
  "used_by_system": false,
  "used_by_services": []
}

{
  "resource_type": "PrincipalIdentity",
  "id": "automation-account",
  "node_id": "automation-host-01",
  "role": "network_engineer",
  "certificate_id": "8f4c2a91-7e3d-4b6f-9c1a-5d8e2f7b4a9c",
  "is_protected": true,
  "creation_time": 1704067200000
}

{
  "resource_type": "ClusterStatus",
  "cluster_status": "STABLE",
  "node_count": 3,
  "online_node_count": 3,
  "offline_node_count": 0,
  "degraded_node_count": 0
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification, or import the NSX Manager's CA certificate into your system trust store.
    **`{"error_code":400,"error_message":"Invalid PEM format in pem_encoded field"}`** — Ensure the certificate file contains valid PEM-formatted text and the awk command properly escapes newlines; test with `cat nsx-automation.crt | head -2`.
    **`{"error_code":403,"error_message":"User admin does not have permission to perform this operation"}`** — Verify the admin account has the NSX Administrator role and that certificate management permissions are not restricted by role-based access control policies.
```bash
# Enable audit log export (NSX Manager CLI)
nsxcli
set service syslog exporter siem-01 level info protocol TLS server 10.0.0.100 port 6514
```

```text title="Expected output"
NSX CLI (build 22.1.2.0.0)
Copyright (c) 2023 VMware, Inc. All rights reserved.

nsx> set service syslog exporter siem-01 level info protocol TLS server 10.0.0.100 port 6514
Syslog exporter 'siem-01' configured successfully.
nsx> exit
```

!!! warning "Common errors"
    **`Error: Syslog exporter 'siem-01' already exists`** — Use a different exporter name or delete the existing one with `delete service syslog exporter siem-01` first.
    **`Error: Unable to resolve hostname or IP address 10.0.0.100`** — Verify network connectivity from NSX Manager to the SIEM server and confirm the IP address is reachable.
    **`Error: TLS certificate validation failed for server 10.0.0.100:6514`** — Import the SIEM server's CA certificate into NSX Manager's trust store using `set service syslog exporter siem-01 ca-cert <cert-path>`.
```bash
# View recent auth events on NSX Manager node
tail -100 /var/log/vmware/nsx-manager/audit.log | grep -i "login\|auth\|role"
```


```text title="Expected output"
2024-01-15T14:32:18.456Z [INFO] User 'admin' authenticated successfully from 192.168.1.45 via LDAP
2024-01-15T14:28:52.123Z [INFO] User 'nsx-operator' role assignment updated: added role 'Enterprise Admin'
2024-01-15T14:15:33.789Z [WARN] Authentication attempt failed for user 'readonly-user' from 10.50.22.18 - invalid credentials
2024-01-15T14:12:07.445Z [INFO] User 'automation-svc' authenticated successfully from 10.20.15.33 via certificate
2024-01-15T13:58:41.912Z [INFO] Role 'Security Admin' assigned to user 'sec-team-lead' by 'admin'
2024-01-15T13:45:19.654Z [WARN] Authentication timeout for session 'sess-8f4a2c9e' after 30 minutes of inactivity
2024-01-15T13:32:05.321Z [INFO] User 'admin' logged out from 192.168.1.45
2024-01-15T13:18:44.876Z [INFO] User 'network-admin' authenticated successfully from 172.16.8.92 via LDAP
```

!!! warning "Common errors"
    **`tail: cannot open '/var/log/vmware/nsx-manager/audit.log' for reading: No such file or directory`** — Verify the NSX Manager service is running with `systemctl status nsx-manager` and check the correct log path with `find /var/log -name "*audit*"`.
    **`grep: (standard input): Permission denied`** — Run the command with `sudo` or ensure your user account has read permissions on the audit log file.
## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## See also

- [NSX — Access Control](../access-control/)
- [NSX — Hardening](../hardening/)
