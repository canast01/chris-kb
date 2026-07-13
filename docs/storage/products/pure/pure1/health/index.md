---
tags:
  - pure
description: "Array Health reference covering FlashBlade Health, Health via Pure1 REST API, Connectivity Health — Phone Home, Health Monitoring Integration, Common..."
---
# Pure1 — Array Health

<div class="kb-summary">
Array Health reference covering FlashBlade Health, Health via Pure1 REST API, Connectivity Health — Phone Home, Health Monitoring Integration, Common Health Issues.

*Applies to: Pure1*
</div>

```d2
direction: down

connectivity_health_phone_home: "Connectivity Health — Phone Home" {shape: rectangle}
health_monitoring_integration: "Health Monitoring Integration" {shape: rectangle}
common_health_issues: "Common Health Issues" {shape: rectangle}

connectivity_health_phone_home -> health_monitoring_integration: uses
health_monitoring_integration -> common_health_issues: uses
```

## Connectivity Health — Phone Home

Pure1 requires outbound HTTPS connectivity (TCP 443) from the array to Pure Storage cloud. If Phone Home is failing:

```bash
# Test outbound connectivity from array
purentp list           # NTP also tests DNS/network

# Check Phone Home status
purearray list --csv   # includes phone_home_enabled, phone_home_last_contact

# Proxy configuration (if internet access is via proxy)
puresupport proxy list
puresupport proxy set --host <proxy-ip> --port 8080
```


```text title="Expected output"
Name                          NtpServer1                NtpServer2                NtpServer3
Enabled                       True                      True                      True
Status                        synced                    synced                    synced
Stratum                       2                         2                         2

Name,Model,Version,Phone_Home_Enabled,Phone_Home_Last_Contact
pure1-array-01,FlashArray//X,6.4.2,true,2024-01-15T09:47:32Z
pure1-array-02,FlashArray//X,6.4.2,true,2024-01-15T09:48:15Z

Name          Host              Port    Enabled
support-proxy 192.168.100.50    8080    true
```

!!! warning "Common errors"
    **`Error: NTP server unreachable`** — Verify NTP server IP is correct and firewall allows UDP port 123 outbound from the array.
    **`Error: Phone home disabled or no contact in 30+ days`** — Enable phone home with `purearray set --phone-home=true` and verify outbound HTTPS (port 443) connectivity to Pure's cloud.
    **`Error: proxy set: invalid host address`** — Ensure the proxy IP is valid and reachable; use `ping <proxy-ip>` to test connectivity first.
## Health Monitoring Integration

Pure1 can send health events to external systems:

- **SNMP:** Configure under Settings → Notification → SNMP. Use the Pure Storage MIB.
- **Syslog:** Settings → Notification → Syslog → add syslog server IP
- **Webhooks:** Settings → Notification → Webhooks (FlashArray 6.3+)
- **Email:** Settings → Notification → Email → add recipients

## Common Health Issues

| Symptom | Cause | Action |
|---|---|---|
| Drive shows Failed | Drive hardware fault | Open Pure support case — drive replacement covered by Evergreen |
| Controller Offline | Controller fault | Open Priority support case immediately |
| Phone Home last contact > 24h | Firewall blocking TCP 443 to pure1.purestorage.com | Check proxy/firewall; test with `curl https://pure1.purestorage.com` from array |
| Array not visible in Pure1 | Array not registered or API key expired | Re-register array under Pure1 → Settings → Arrays |
