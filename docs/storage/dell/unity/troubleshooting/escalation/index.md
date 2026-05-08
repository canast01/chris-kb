# Unity — Escalation

## Support Portal

Open and manage Unity support cases at [https://www.dell.com/support](https://www.dell.com/support). Log in with your Dell account and navigate to **My Cases** to create, update, and track cases.

SupportAssist (formerly ESRS/SRS) is embedded in Unity OE and automatically opens hardware fault cases when an SP, drive, or power module fails. Verify SupportAssist is enabled and calling home in Unisphere under **Settings > Support > SupportAssist**. Test connectivity using the **Send Test Alert** button.

## Opening a Case

Required information before opening a case:

| Field | How to Obtain |
|---|---|
| SP serial numbers | Chassis label on each SP; or Unisphere > **System > Hardware** |
| Unity OE version | `uemcli /sys/sw show`; or Unisphere > **System > Software** |
| Symptom description | Clear description of what failed, when it started, and frequency |
| Pool and LUN names affected | `uemcli /stor/pool show`, `uemcli /stor/prov/luns show` |
| Client impact | Hosts and applications affected; protocols (FC, iSCSI, NFS, SMB) |
| Recent changes | Any firmware, OE, or configuration changes made in the 48 hours before the fault |

For SP hardware failures or drive faults, Dell dispatches replacement parts automatically when SupportAssist is enabled. For P1 cases (production I/O interrupted), call the Dell support line directly rather than using only the portal.

## Information to Collect

```bash
# Show system general health and software version
uemcli -d <sp_ip> -u admin -p <password> /sys/general show

# Show all components not in OK health state
uemcli -d <sp_ip> -u admin -p <password> /env/health show -filter "health.value ne OK"

# Show all active alerts
uemcli -d <sp_ip> -u admin -p <password> /sys/alert show

# Show alert history
uemcli -d <sp_ip> -u admin -p <password> /sys/alert/hist show
```

**Collect the service support bundle** from Unisphere:

1. Navigate to **System > Support > Collect Service Information**.
2. Click **Collect** and wait for the bundle to complete (typically 5–15 minutes).
3. Download the bundle file and upload it to the Dell support case using the **Secure Upload** link in the case.

Alternatively, initiate via CLI: `uemcli /sys/serviceinfo collect`.

Include a **screenshot of the Unisphere health dashboard** showing the fault state to provide immediate context to the support engineer.

## SLA Tiers

| Tier | Priority | Response Time | Coverage | Parts Replacement |
|---|---|---|---|---|
| ProSupport Plus | P1 — Production Down | 2 hours | 24x7x365 | 4-hour on-site (where available) |
| ProSupport Plus | P2 — Degraded Performance | 4 hours | 24x7x365 | Next business day |
| ProSupport Plus | P3/P4 | Next business day | Business hours | Next business day |
| ProSupport | P1 | 4 hours | 24x7x365 | Next business day |
| ProSupport | P2–P4 | Next business day | Business hours | Next business day |

Verify your Unity system's support contract level in the Dell support portal under **My Products and Services**.

## Escalation Path

If a P1 case is not progressing within the response SLA or the fault is causing a prolonged production outage:

1. Call the Dell support line and request **escalation for an open case** — provide the case number and explain the business impact.
2. Contact your **Dell account team Technical Account Manager (TAM)** — TAMs have direct escalation paths into the Unity engineering and field services teams.
3. For multi-hour production outages with no resolution in sight, request engagement with **Dell Global Priority Services (GPS)** via your account team. GPS provides senior engineering support beyond standard case handling.
4. When escalating, always state: case number, SP serial numbers, current fault status, duration of impact, number of hosts/applications affected, and what has already been tried.
