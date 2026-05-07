# DNS


<div class="kb-grid kb-grid-1">

  <div class="kb-card">
    <h3><a href="lookups/">Lookups</a></h3>
    <p>Lookups notes, checks, commands, and references.</p>
  </div>

  <div class="kb-card">
    <h3><a href="troubleshooting/">Troubleshooting</a></h3>
    <p>Common issues, diagnostic steps, and resolution guides.</p>
  </div>

</div>
## Overview

DNS resolves names to IP addresses and is a critical dependency for authentication, applications, storage, cloud services, monitoring, and automation.

## Daily Checks

- Verify forward and reverse lookup
- Confirm DNS server availability
- Review stale or duplicate records
- Check zone replication
- Validate conditional forwarders

## Health Commands

```bash
nslookup example.com
dig example.com
dig -x 10.0.0.10
ipconfig /displaydns
```

## Upgrade Workflow

1. Export or back up DNS zones
2. Confirm replication health
3. Apply OS or DNS service updates
4. Validate name resolution
5. Confirm dependent applications are healthy
