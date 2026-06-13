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

  LCM CLI Coverage (SSH to LCM as root)
```text
┌──────────────────────────────────── Aria Suite LCM CLI Reference ─────────────────────────────────────┐
│                                                                                                       │
│  VAMI management, REST API endpoints, vlcm log files, and SSH commands for LCM.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Key REST API Endpoints            │  │               VAMI Operations               │   │
│   │         GET /lcm/api/v1/environments         │  │              https://<lcm>:5480             │   │
│   │           GET /lcm/api/v1/products           │  │             Backup + restore UI             │   │
│   │         POST /lcm/api/v1/request/...         │  │            Network + NTP settings           │   │
│   │            GET /lcm/api/v1/health            │  │           Depot configuration page          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  REST API for automation; VAMI for appliance config; SSH for log and service access.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 SSH Commands                 │  │                Log Locations                │   │
│   │             service vlcm status              │  │                /var/log/vlcm/               │   │
│   │             service vlcm restart             │  │            vlcm.log: main LCM log           │   │
│   │          lcm-support.sh: bundle gen          │  │        installer.log: product deploy        │   │
│   │          ntpq -p: time sync verify           │  │         logscraper: all product logs        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LCM VM on vSphere; SSH via jump host; VAMI on port 5480; log files on LCM disk                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VAMI                = Virtual Appliance Management Interface; port 5480                              │
│  GET /environments   = REST endpoint listing all LCM environments and status                          │
│  GET /products       = REST endpoint listing products and their versions                              │
│  POST /request       = REST endpoint to trigger install, upgrade, or cert action                      │
│  GET /health         = REST endpoint returning LCM and product health summary                         │
│  vlcm service        = Main LCM application service; restart to recover hung UI                       │
│  vlcm.log            = Primary LCM log; first stop for any LCM issue                                  │
│  installer.log       = Records product deployment steps and errors                                    │
│  logscraper          = LCM tool collecting logs from all managed products                             │
│  lcm-support.sh      = Script generating LCM support bundle for GSS                                   │
│  ntpq -p             = NTP peer verification; LCM must be in sync                                     │
│  Depot Config Page   = VAMI page to add/edit online or local content depot                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
