---
tags:
  - san
  - security
---
# Cisco Nexus Dashboard — Security Access Control
![Cisco Nexus Dashboard — Security Access Control](../../../../assets/san-cisco-nexus-dashboard-security-access-control.svg)


```bash
# Via REST API
TOKEN=$(curl -sk -X POST https://nd-dc1.corp.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"userName":"admin","userPasswd":"<pass>","domain":"local"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk -X POST https://nd-dc1.corp.example.com/nexus/api/v1/users \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "svc-monitor",
    "password": "<strong-password>",
    "firstName": "Service",
    "lastName": "Monitor",
    "email": "san-team@corp.example.com",
    "roles": [{"name": "Viewer", "sites": [{"name": "DC1-SAN"}, {"name": "DC2-SAN"}]}]
  }' | python3 -m json.tool
```


```d2
direction: down

external: External / Untrusted {shape: rectangle}
perimeter_controls: "Perimeter Controls" {shape: rectangle}
identity_access: "Identity & Access" {shape: rectangle}
audit_logging: "Audit & Logging" {shape: rectangle}
core: "Nexus Dashboard Core" {shape: hexagon}

external -> perimeter_controls: traffic in
perimeter_controls -> identity_access
identity_access -> audit_logging
audit_logging -> core: secured path
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Nexus Dashboard — Authentication](authentication/)
- [Nexus Dashboard — Hardening](hardening/)
- [Nexus Dashboard — Encryption](encryption/)
