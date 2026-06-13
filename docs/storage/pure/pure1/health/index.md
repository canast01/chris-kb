---
tags:
  - pure
---
# Pure1 — Array Health


<div class="kb-summary">
Array Health reference covering FlashBlade Health, Health via Pure1 REST API, Connectivity Health — Phone Home, Health Monitoring Integration, Common Health Issues.

*Applies to: Pure1*
</div>

```text
┌────────────────────────────────────── Pure1 — Health Monitoring ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Pure1 Health: continuous monitoring of array hardware, software, and performance       │   │
│   │      Component inputs: drives, controllers, power supplies, fans, network, Purity events      │   │
│   │           Health score: OK / Degraded / Unhealthy per array based on component state          │   │
│   │           Fleet view: all arrays ranked by health; filter by tag, model, or location          │   │
│   │            Drill-down: click array to see component-level detail and active alerts            │   │
│   │               30-day history: health trend; identify recurring degraded periods               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Health from Purity OS via phonehome · Pure cloud ML processes · UI updated every 2 min               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Health score = OK (all green) / Degraded (non-critical fault) / Unhealthy (critical)                 │
│  Fleet view = Pure1 UI showing all arrays ordered by health state                                     │
│  Drill-down = Clicking array opens component view: drives, controllers, shelves                       │
│  Unhealthy = Critical component failure; TAC case auto-opened if enabled                              │
│  Degraded = Non-critical fault (e.g., single drive pre-failure); warning state                        │
│  OK = All components healthy; no active alerts                                                        │
│  30-day history = Pure1 stores health state over time; shows trend per array                          │
│  Component = Physical part: drive, DIMM, NIC, controller, power supply, fan                           │
│  Purity event = Software-level error logged by array OS; contributes to health                        │
│  Pre-failure = Pure1 ML detecting imminent component failure before it occurs                         │
│  Phonehome = Array sending hardware sensor data to Pure cloud every 30 seconds                        │
│  Proactive swap = Pure staging replacement and dispatching before customer impact                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
