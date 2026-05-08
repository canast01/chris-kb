# Linux — Escalation

Vendor escalation procedures and support contacts.

## Red Hat (RHEL)

### Opening a Support Case

Support portal: [access.redhat.com](https://access.redhat.com)

1. Log in with the team's Red Hat account
2. Support → Open a Support Case
3. Select: Product = Red Hat Enterprise Linux, Version = deployed RHEL version
4. Describe the issue with: hostname, RHEL version, kernel version, and sosreport

### Collecting the sosreport

Always collect a sosreport before opening an SR:

```bash
# Generate sosreport
sosreport

# Output: /var/tmp/sosreport-<hostname>-<timestamp>.tar.xz
# Attach to the Red Hat support case via the portal
```

If the system is non-interactive (no TTY), use:
```bash
sosreport --batch --all-logs
```

### Checking Subscription Status

```bash
subscription-manager status
subscription-manager list --installed   # Verify products are registered
subscription-manager list --consumed    # Verify entitlements consumed
```

If entitlement shows `Invalid`: run `subscription-manager refresh` and check the RH portal.

### RHEL Lifecycle Dates

| Version | Full Support EOL | Maintenance Support EOL | Extended Life (RHEL ELS) |
|---|---|---|---|
| RHEL 9 | May 2027 | May 2032 | Optional |
| RHEL 8 | May 2024 | May 2029 | Optional |
| RHEL 7 | August 2019 | June 2024 | Available until June 2028 |

Track lifecycle in CMDB — alert 90 days before Full Support EOL to initiate leapp upgrade.

## Canonical (Ubuntu)

### Opening a Support Case

Support portal: [ubuntu.com/advantage](https://ubuntu.com/advantage) (Ubuntu Pro)

```bash
# Check Ubuntu Pro status
pro status
pro attach <token>   # If not yet attached
```

### Collecting Diagnostics

```bash
# Ubuntu Pro apport-collect for kernel/package issues
ubuntu-bug linux   # Interactive — opens Launchpad by default
# For non-interactive collection:
apport-collect --output /tmp/ubuntu-diag.tgz
```

### Ubuntu LTS Support Timeline

| Version | Standard Support | Ubuntu Pro (LTS) | Notes |
|---|---|---|---|
| Ubuntu 24.04 LTS | April 2029 | April 2034 | Current LTS |
| Ubuntu 22.04 LTS | April 2027 | April 2032 | Active |
| Ubuntu 20.04 LTS | April 2025 | April 2030 | ESM only |

## Escalation

| Situation | Action |
|---|---|
| Kernel panic / hang | Collect crash dump (`/var/crash/`) + sosreport; open Sev 1 SR |
| Data corruption | Do not run fsck without vendor guidance; open SR first |
| Security vulnerability (CVE) | Check Red Hat Security Advisories; apply errata; open SR if patch unavailable |
| Subscription/licensing | Contact Red Hat account team or use portal chat |

## Crash Dump Configuration

```bash
# RHEL — verify kdump is configured
systemctl status kdump
cat /etc/kdump.conf | grep path   # Default: /var/crash

# Test kdump is enabled
cat /proc/cmdline | grep crashkernel   # Should include crashkernel=auto or explicit value
```

Crash dumps must be available before opening a kernel-related SR.
