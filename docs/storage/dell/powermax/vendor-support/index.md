# PowerMax Vendor Support
## Support Portal

Dell support for PowerMax is managed through: https://www.dell.com/support

- Log in with your My Dell account (company entitlement required).
- Register the array serial number under **My Products** to attach the support contract.
- **SupportAssist**: Enable SupportAssist on the array (Unisphere → Connectivity → SupportAssist) to allow Dell to proactively monitor the system and auto-create service requests for hardware faults.
- **CloudIQ**: Linked to the support contract; provides health scores, capacity forecasts, and anomaly alerts that can feed directly into support cases.
- **Secure Remote Services (SRS)**: Dell's secure remote access gateway; required for remote support sessions. Deploy the SRS virtual edition (SRS-VE) on the management network.

## Opening a Case

Required information for every support case:

| Field | How to Obtain |
|---|---|
| Array serial number (SID) | `symcfg list` — the 12-digit Symmetrix ID |
| PowerMaxOS version | `symcfg -sid <SID> show \| grep -i microcode` |
| Solutions Enabler version | `symcli -version` |
| Symptom description | Clear statement of observed behaviour and affected objects |
| Time of first occurrence | Exact timestamp from Unisphere alert or symevent log |
| Business impact | Number of hosts/applications affected; production or non-production |

Open a case at: https://www.dell.com/support → My Service Requests → Create Service Request

## Information to Collect

Run the following before or immediately after opening the case:

```bash
# Full array health and configuration snapshot
symcfg -sid <SID> show > /tmp/pmx_health_$(date +%Y%m%d).txt

# Director and port status
symcfg -sid <SID> list -dir all >> /tmp/pmx_health_$(date +%Y%m%d).txt

# Physical drive state
sympd list -sid <SID> >> /tmp/pmx_health_$(date +%Y%m%d).txt

# SRDF group and pair state
symdf list -sid <SID> >> /tmp/pmx_health_$(date +%Y%m%d).txt
symrdf -sid <SID> -rdfg <rdfg-number> query >> /tmp/pmx_health_$(date +%Y%m%d).txt

# Audit events from the last 24 hours
symevent -sid <SID> list -last 500 >> /tmp/pmx_health_$(date +%Y%m%d).txt

# Collect a full SE diagnostic bundle (requires SE host root or sudo)
seconfig collect -out /tmp/se_diag_$(date +%Y%m%d).zip
```

For hardware faults (drive failure, director offline), Dell SupportAssist can collect and upload a diagnostic bundle automatically if enabled. Confirm auto-collection is running in Unisphere → Connectivity → SupportAssist.

## SLA Tiers

Dell ProSupport Plus SLA response times:

| Severity | Definition | ProSupport Plus Response |
|---|---|---|
| P1 – Critical | Complete loss of production functionality; no workaround | 2 hours onsite or remote support engagement |
| P2 – High | Significant degradation; workaround exists but not sustainable | 4 hours remote support engagement |
| P3 – Medium | Partial degradation; workaround available | Next business day |
| P4 – Low | General guidance, documentation, or non-urgent request | Next business day |

ProSupport (standard, without Plus) carries P1 = 4-hour response, P2 = next business day.

## Escalation Path

1. **Front-line support engineer**: Initial case triage and remote diagnostics.
2. **Technical Account Manager (TAM)**: Assigned under ProSupport Plus. Use for proactive planning, upgrade guidance, and priority case escalation.
3. **Product Engineering (PE) escalation**: Request via the TAM or case owner when a suspected product defect is involved. PE can issue hot fixes and workarounds.
4. **Executive escalation**: For critical production outages with no resolution path after 4+ hours. Request through the TAM or account team.

Always reference the case number in all communications. For P1 issues, also call the Dell ProSupport phone line directly in parallel with the web case to ensure immediate engagement.

Dell ProSupport phone (US): 1-800-945-3355
