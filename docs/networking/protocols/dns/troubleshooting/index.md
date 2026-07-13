---
tags:
  - networking
  - troubleshooting
search:
  boost: 1.5
description: "DNS Troubleshooting reference covering Overview, Resolution Failure Triage, dcdiag /test:dns, Cache Poisoning Checks, Replication Issues and 2 more..."
---
# DNS Troubleshooting

<div class="kb-summary">
DNS Troubleshooting reference covering Overview, Resolution Failure Triage, dcdiag /test:dns, Cache Poisoning Checks, Replication Issues and 2 more sections.
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
resolution_failure_triage: "Resolution Failure Triage" {shape: rectangle}
dcdiag_testdns: "dcdiag /test:dns" {shape: rectangle}
cache_poisoning_checks: "Cache Poisoning Checks" {shape: rectangle}
replication_issues: "Replication Issues" {shape: rectangle}
common_error_reference: "Common Error Reference" {shape: rectangle}
known_issues: "Known Issues" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> resolution_failure_triage: investigate
symptom -> dcdiag_testdns: investigate
symptom -> cache_poisoning_checks: investigate
symptom -> replication_issues: investigate
symptom -> common_error_reference: investigate
symptom -> known_issues: investigate
resolution_failure_triage -> resolution
dcdiag_testdns -> resolution
cache_poisoning_checks -> resolution
replication_issues -> resolution
common_error_reference -> resolution
known_issues -> resolution
```

## Before you begin

- **Access:** Network admin credentials; console or SSH to devices
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

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


```text title="Expected output"
Server:		10.0.0.1
Address:	10.0.0.1#53

Name:	host.example.local
Address: 10.0.2.45

Server:		10.0.0.53
Address:	10.0.0.53#53

Name:	host.example.local
Address: 10.0.2.45

host.example.local.	300	IN	A	10.0.2.45

Windows IP Configuration

Successfully flushed the DNS Resolver Cache.
```

!!! warning "Common errors"
    **`** server can't find host.example.local: NXDOMAIN`** — Verify the record exists on the authoritative server with `dig @10.0.0.53 host.example.local` and check zone file syntax.
    **`nslookup: command not found`** — Install `bind-utils` (RHEL/CentOS) or `dnsutils` (Debian/Ubuntu) package.
    **`resolvectl: command not found`** — Use `sudo systemctl restart systemd-resolved` instead, or manually clear `/etc/resolv.conf` cache on non-systemd systems.
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

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Forwarders](../forwarders/)
- [Lookups](../lookups/)
- [Records](../records/)
- [Zones](../zones/)
- [DNS — Overview](../)
