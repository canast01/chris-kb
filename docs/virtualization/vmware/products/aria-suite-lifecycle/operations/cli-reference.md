---
tags:
  - aria-lcm
  - operations
  - vmware
---
# Aria Suite Lifecycle — CLI Reference

<div class="kb-summary">
CLI Reference reference covering Services, Certificates, Proxy & Network, NTP & Time, Logs.

*Applies to: Aria LCM 8.x*
</div>
![Aria Suite Lifecycle — CLI Reference](../../../../../assets/virtualization-vmware-aria-suite-lifecycle-operations-cli-re.svg)

  LCM CLI Coverage (SSH to LCM as root)

---

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Certificates

The Locker stores certificates used by Aria products. Manage them here before triggering certificate replacement operations in LCM.

```bash
# List all certificates in the Locker
vracli certificate list

# Show detail for a certificate
vracli certificate show --alias <alias>

# Import a certificate and key pair
vracli certificate import --cert <cert.pem> --key <key.pem> --alias <alias>

# Delete a certificate from the Locker
vracli certificate delete --alias <alias>

# Check certificate expiry
vracli certificate list | grep -E "alias|expiry"
```


```text title="Expected output"
vracli certificate list
Alias                          Issuer                    Expiry Date            Status
aria-default-cert             CN=VMware,O=VMware        2025-06-15 10:30:00    Valid
custom-api-cert               CN=Custom CA,O=Internal   2024-11-22 14:45:30    Expired
lb-wildcard-cert              CN=*.corp.local           2026-03-10 08:15:00    Valid
tenant-isolation-cert         CN=Tenant-CA              2025-01-08 16:20:00    Valid

vracli certificate show --alias aria-default-cert
Certificate Details for: aria-default-cert
Subject: CN=aria.corp.local,O=VMware,C=US
Issuer: CN=VMware,O=VMware,C=US
Serial Number: 4A:2B:C1:D9:E8:F5:6A:7B
Valid From: 2023-06-15 10:30:00 UTC
Valid Until: 2025-06-15 10:30:00 UTC
Fingerprint (SHA256): a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1
Status: Valid

vracli certificate import --cert /etc/ssl/certs/new-cert.pem --key /etc/ssl/private/new-key.pem --alias production-cert
(no output — command completes silently)

vracli certificate delete --alias custom-api-cert
Certificate 'custom-api-cert' deleted successfully.

vracli certificate list | grep -E "alias|expiry"
Alias                          Issuer                    Expiry Date            Status
aria-default-cert             CN=VMware,O=VMware        2025-06-15 10:30:00    Valid
lb-wildcard-cert              CN=*.corp.local           2026-03-10 08:15:00    Valid
tenant-isolation-cert         CN=Tenant-CA              2025-01-08 16:20:00    Valid
production-cert               CN=production.local       2027-09-20 12:00:00    Valid
```

!!! warning "Common errors"
    **`Error: Certificate file not found: /etc/ssl/certs/new-cert.pem`** — Verify the certificate file path exists and is readable by the vracli user.
    **`Error: Alias 'aria-default-cert' is in use and cannot be deleted`** — Use a different alias or ensure the certificate is not actively bound to any service before deletion.
    **`Error: Private key does not match certificate`** — Ensure the certificate and private key pair are from the same CSR and re-run the import command with the correct files.
---

## Proxy & Network

```bash
# Show current proxy configuration
vracli proxy show

# Set outbound proxy for bundle downloads
vracli proxy set --host <proxy_host> --port <proxy_port>

# Clear proxy
vracli proxy clear

# Show network configuration
vracli network show

# Update DNS servers
vracli network dns set --servers <dns1>,<dns2>
```


```text title="Expected output"
Proxy Configuration:
  Host: proxy.corp.local
  Port: 8080
  Username: (not configured)
  Status: Active

Network Configuration:
  Hostname: aria-lifecycle-01.corp.local
  IPv4 Address: 192.168.1.45
  Subnet Mask: 255.255.255.0
  Gateway: 192.168.1.1
  DNS Servers: 8.8.8.8, 8.8.4.4
  MTU: 1500

Proxy cleared successfully.

DNS servers updated:
  Primary: 10.0.0.10
  Secondary: 10.0.0.11
  Status: Applied
```

!!! warning "Common errors"
    **`Error: Unable to connect to proxy host proxy.corp.local:8080`** — Verify the proxy hostname/IP and port are correct, and that the appliance has network connectivity to the proxy server.
    **`Error: vracli command not found`** — Ensure you are logged into the Aria Suite Lifecycle appliance via SSH and have appropriate permissions; vracli is only available on the appliance itself.
    **`Error: DNS update failed - invalid server format`** — Use comma-separated IP addresses without spaces (e.g., `10.0.0.10,10.0.0.11`) for the `--servers` parameter.
---

## NTP & Time

```bash
# Show current NTP configuration
vracli ntp show

# Set NTP servers
vracli ntp set <ntp_server1> <ntp_server2>

# Verify time sync
timedatectl status

# Force NTP sync
chronyc makestep
```


```text title="Expected output"
NTP Configuration:
  Server 1: 10.20.30.40
  Server 2: 10.20.30.41
  Status: synchronized
  Last update: 2.5s ago

               Local time: Wed 2024-01-17 14:32:18 UTC
           Universal time: Wed 2024-01-17 14:32:18 UTC
                 RTC time: Wed 2024-01-17 14:32:18
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
       RTC in local TZ: no

200 OK
Making a step adjustment of 125.432 seconds.
```

!!! warning "Common errors"
    **`vracli: command not found`** — Ensure you are logged into the vRealize Automation appliance via SSH and that vracli is in your PATH, or use the full path `/opt/vmware/vrealize/bin/vracli`.
    **`Failed to set NTP servers: Permission denied`** — Run the vracli commands with appropriate privileges (use `sudo` or ensure your user has NTP configuration permissions in vRA).
    **`Timed out waiting for NTP synchronization`** — Check network connectivity to the NTP servers with `ping 10.20.30.40` and verify firewall rules allow UDP port 123 outbound.
---

## Logs

```bash
# Follow the main LCM application log
tail -f /var/log/lcm/lcm-app.log

# Follow the LCM debug log
tail -f /var/log/lcm/lcm-debug.log

# Collect a support bundle
vracli support-bundle

# View recent system journal
journalctl --since "2 hours ago" -u lcm
```


```text title="Expected output"
==> /var/log/lcm/lcm-app.log <==
2024-01-15 14:32:18.456 [main] INFO  com.vmware.lcm.core.LifecycleManager - Initializing LCM application v8.12.1
2024-01-15 14:32:19.123 [pool-2-thread-3] DEBUG com.vmware.lcm.inventory.InventoryService - Loading vCenter inventory from 192.168.1.42
2024-01-15 14:32:21.789 [pool-2-thread-5] INFO  com.vmware.lcm.deployment.DeploymentEngine - Deployment task 'd4c8e2f1-9a3b-4c2e-b1d7-8f3a2c5e9b1a' started
2024-01-15 14:32:45.234 [pool-2-thread-5] INFO  com.vmware.lcm.deployment.DeploymentEngine - Component 'aria-automation-8.12.0' deployment completed successfully
2024-01-15 14:33:02.567 [main] INFO  com.vmware.lcm.core.HealthCheck - System health status: HEALTHY

==> /var/log/lcm/lcm-debug.log <==
2024-01-15 14:32:18.101 [DEBUG] Heap memory: 2048MB, Used: 1456MB, Free: 592MB
2024-01-15 14:32:19.445 [DEBUG] Database connection pool initialized: 20 connections
2024-01-15 14:32:21.678 [DEBUG] vCenter API call: GET /rest/vcenter/vm?filter.names={'aria-automation-node-01'}
2024-01-15 14:32:22.901 [DEBUG] Response received: 200 OK, 1 VM found
2024-01-15 14:33:15.234 [DEBUG] Deployment state persisted to database: COMPLETED

Support bundle collection started...
Collecting system logs...
Collecting configuration files...
Collecting diagnostic data...
Support bundle created: /tmp/lcm-support-bundle-20240115-143325.tar.gz (487MB)

Jan 15 14:31:42 aria-lcm-01 systemd[1]: Started Lifecycle Manager Application.
Jan 15 14:32:18 aria-lcm-01 lcm[2847]: Application startup sequence initiated
Jan 15 14:32:45 aria-lcm-01 lcm[2847]: Deployment task completed with status: SUCCESS
Jan 15 14:33:02 aria-lcm-01 lcm[2847]: Health check passed: all services operational
```

!!! warning "Common errors"
    **`tail: cannot open '/var/log/lcm/lcm-app.log' for reading: No such file or directory`** — Verify the LCM application is installed and running with `systemctl status lcm`, or check the correct log path in `/var/log/lcm/`.
    **`vracli: command not found`** — Ensure the vRealize Automation CLI is installed and in your PATH by running `which vracli` or sourcing the vRA environment setup script.
    **`journal
---

## See also

- [Aria Suite Lifecycle — Procedures](../procedures/)
- [Aria Suite Lifecycle — Scripts](../scripts/)
- [Aria Suite Lifecycle — Health Checks](../health-checks/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
