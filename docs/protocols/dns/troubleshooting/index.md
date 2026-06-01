# DNS Troubleshooting


<div class="kb-summary">
DNS Troubleshooting reference covering Overview, Resolution Failure Triage, dcdiag /test:dns, Cache Poisoning Checks, Replication Issues and 2 more sections.
</div>

        TRIAGE: NSLOOKUP FAILS
```text
┌──────────────────────────────────────────────────────────────┐
│  1. nslookup host.example.local ── no answer ──► continue       │
│          │                                                   │
│          ▼                                                   │
│  2. Check resolver (which server answered?)                  │
│     nslookup host.example.local 10.0.0.53 ── ok ──► client conf│
│          │ still fails                                       │
│          ▼                                                   │
│  3. Record exists? dig @10.0.0.53 host.example.local            │
│          │ NXDOMAIN ──────────────────────────► add record   │
│          │ answer returned                                   │
│          ▼                                                   │
│  4. Zone delegation correct?                                 │
│     dig NS corp.local ──── wrong NS ────► fix delegation     │
│          │ ok                                                │
│          ▼                                                   │
│  5. AD replication? repadmin /showrepl ─► sync if needed     │
│          │ ok                                                │
│          ▼                                                   │
│  6. Flush client cache: ipconfig /flushdns (Windows)         │
│                         resolvectl flush-caches (Linux)      │
└──────────────────────────────────────────────────────────────┘
```

## Overview

DNS failures manifest as name resolution errors, application connectivity issues, or authentication failures. Systematic diagnosis starts with isolating whether the problem is client-side cache, server-side zone data, replication, or network connectivity to the resolver.

## Resolution Failure Triage

```bash
# Step 1: test from the client
nslookup host.example.local
# Note which server answered and what was returned

# Step 2: query the authoritative server directly
nslookup host.example.local 10.0.0.53

# Step 3: check if the record exists on the server
dig @10.0.0.53 host.example.local +nocmd +noall +answer

# Step 4: flush client cache and retry
ipconfig /flushdns        # Windows
resolvectl flush-caches   # Linux (systemd-resolved)
```

## dcdiag /test:dns

`dcdiag /test:dns` is the first tool for DNS issues on Active Directory domains.

```powershell
# Run full DNS test on local DC
dcdiag /test:dns /v

# Run against a specific DC
dcdiag /test:dns /s:dc02.example.local /v

# Test all DCs in the forest
dcdiag /test:dns /e /v

# Common failures and what they mean
# DNS_ERROR_RCODE_NAME_ERROR  -> record missing or zone not loaded
# LDAP bind failed            -> connectivity or credential issue
# Missing delegation          -> child zone not delegated from parent
```

## Cache Poisoning Checks

```powershell
# Verify DNSSEC validation is enabled (Windows DNS)
Get-DnsServerResponseRateLimiting

# Check if the server accepts non-secure updates only on intended zones
Get-DnsServerZone | Select-Object ZoneName, DynamicUpdate

# Inspect cached records (look for unexpected entries)
Get-DnsServerCache | Where-Object { $_.RecordType -eq "A" } |
  Sort-Object TimeToLive

# Clear server cache
Clear-DnsServerCache -Force
```

## Replication Issues

```powershell
# Force AD replication (DNS zones stored in AD replicate with AD)
repadmin /syncall /AdeP

# Check replication status
repadmin /showrepl

# Verify DNS partitions are replicating
repadmin /showrepl * /csv | ConvertFrom-Csv |
  Where-Object { $_."Number of Failures" -gt 0 }

# Check zone is present on all DCs
$zone = "corp.local"
(Get-ADDomainController -Filter *).HostName | ForEach-Object {
  $r = Resolve-DnsName $zone -Server $_ -ErrorAction SilentlyContinue
  [pscustomobject]@{ DC=$_; Resolved=[bool]$r }
}
```

## Common Error Reference

| Error | Likely Cause | Action |
|-------|--------------|--------|
| SERVFAIL | Server cannot reach forwarder or root | Check forwarder connectivity |
| NXDOMAIN | Record does not exist | Add record or check zone |
| REFUSED | Server not authoritative and no forwarder | Configure forwarder or check ACL |
| Timeout | Network issue or DNS service down | Check firewall UDP/TCP 53, DNS service |
| Wrong IP returned | Stale cache or stale record | Flush cache, remove old record |

## Known Issues

- If `dcdiag /test:dns` reports "Missing glue record", the NS record for a delegated child zone has no corresponding A record in the parent. Add the glue A record in the parent zone.
- DNS resolution works for some clients but not others on the same subnet: check client DNS server settings — some machines may point to a server that has a stale conditional forwarder.
- After a DC promotion, DNS replication may lag by up to 15 minutes. Use `repadmin /syncall` to force convergence before testing.
