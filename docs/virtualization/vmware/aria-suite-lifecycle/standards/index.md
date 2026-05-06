# Aria Suite Lifecycle Standards

All LCM-managed appliances must follow a consistent naming scheme: `<product>-<env>-<node#>.<domain>` (e.g. `lcm-prod-01.corp.local`). The pre-deployment checklist must confirm DNS forward/reverse resolution, NTP reachability, NFS mount availability, and proxy exclusions for all management-network CIDRs before running the Easy Installer. Certificates imported into the Locker must be SHA-256 signed with a minimum 2048-bit RSA key and include the full SAN list; wildcard certificates are supported but discouraged for individual product nodes.

**Pre-deployment checklist:**
- DNS A and PTR records for all appliance FQDNs
- NTP reachable and time delta < 5 seconds
- NFS export accessible with read/write from the LCM appliance IP
- Proxy configured with bypass for `*.corp.local` and vCenter/NSX FQDNs
- Password complexity: minimum 15 characters, upper + lower + digit + special
- CA certificate chain (root + intermediates) uploaded to LCM Locker before deployment
