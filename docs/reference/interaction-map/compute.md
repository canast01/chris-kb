---
tags:
  - esxi
  - vcenter
  - compute
  - architecture
description: "How ESXi, vCenter, and PowerCLI interact — vSphere API protocols, hostd, govmomi, and integration with NSX, vSAN, VCF, and Tanzu."
---
# Compute Domain — Interaction Map

*Applies to: All products*

<div class="kb-summary">
How ESXi, vCenter, and PowerCLI interact — vSphere API protocols, hostd, govmomi, and integration with NSX, vSAN, VCF, and Tanzu.
</div>

![Compute Domain Interaction Map](../../assets/interaction-map-compute.svg)

## Integration summary

| From | To | Protocol / API | Notes |
|---|---|---|---|
| ESXi | vCenter | vSphere API (hostd on :443) | ESXi host agent reports state to vpxd |
| vCenter | ESXi | vSphere API (vpxd → hostd) | vCenter pushes config, DRS decisions |
| vCenter | vSAN | SPBM / kernel module | Policies assigned at vCenter; enforced in ESXi |
| vCenter | NSX | NSX Manager REST | NSX plugin registers with vCenter; DFW sync |
| PowerCLI | vCenter | govmomi / SDK over :443 | `Connect-VIServer`; SSO session token |
| VCF | vCenter | SDDC Manager REST API | VCF deploys, patches, and manages vCenter lifecycle |
| Tanzu | vCenter | WCP / vSphere API | Supervisor cluster registers with vCenter; `kubectl vsphere login` |

## Key API endpoints

```bash
# vCenter REST API (new, preferred)
GET https://vcenter/api/vcenter/vm
GET https://vcenter/api/vcenter/host

# vCenter SOAP API (legacy, used by older tools)
https://vcenter/sdk

# ESXi host agent (direct host access)
https://esxi-host/sdk                         # hostd API
```


```text title="Expected output"
# vCenter REST API (new, preferred)
GET https://vcenter/api/vcenter/vm
GET https://vcenter/api/vcenter/host

# vCenter SOAP API (legacy, used by older tools)
https://vcenter/sdk

# ESXi host agent (direct host access)
https://esxi-host/sdk                         # hostd API
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to vcenter port 443: Connection refused`** — Verify vCenter is running and accessible on the network; check firewall rules and DNS resolution with `nslookup vcenter`.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl or import the vCenter SSL certificate into your trusted store with `curl -cacert /path/to/cert.pem`.
    **`HTTP/1.1 401 Unauthorized`** — Authenticate with valid vCenter credentials using `-u username:password` or by obtaining a session token via the `/api/session` endpoint first.
## See also

- [ESXi Cheat Sheet](../../cheat-sheets/esxi/)
- [vCenter Cheat Sheet](../../cheat-sheets/vcenter/)
- [PowerCLI Cheat Sheet](../../cheat-sheets/powercli/)
- [Back to Interaction Map](index.md)
