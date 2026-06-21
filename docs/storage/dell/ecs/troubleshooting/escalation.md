---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# Dell ECS — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Opening a Case, Information to Collect, SLA Tiers, Escalation Path.

*Applies to: ECS 3.x*
</div>
![Dell ECS — Escalation](../../../../assets/storage-dell-ecs-troubleshooting-escalation.svg)




## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Support Portal

Dell EMC Support: [https://www.dell.com/support](https://www.dell.com/support)

- Log in with your MyDell account linked to your support contract
- Navigate to **Cases** to open a new case or view existing cases
- Navigate to **Contracts & Warranties** to verify ECS support entitlement

## Opening a Case

1. Confirm the ECS system is registered under your support contract in the Dell Support portal
2. Collect the information listed below before opening the case
3. Go to [https://www.dell.com/support](https://www.dell.com/support) → **Contact Support** → **Create Service Request**
4. Select product: **Dell EMC ECS** (Enterprise Content Storage)
5. Set severity:
   - **Severity 1** — production cluster down or data inaccessible
   - **Severity 2** — degraded cluster (nodes down, replication stopped) but data accessible
   - **Severity 3** — non-critical functional issue or question
   - **Severity 4** — general enquiry or low-impact issue
6. Attach the support bundle (ECS Portal → Support → Collect Logs) to the case immediately
7. Note the case number and communicate it to the on-call team

## Information to Collect

```bash
# ECS software version
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/version" | python3 -m json.tool

# Node list and health status
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/nodes" | python3 -m json.tool

# Active alerts
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/alerts" | python3 -m json.tool

# VDC capacity
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/capacity" | python3 -m json.tool

# Replication group status (geo deployments)
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/data-service/vpools" | python3 -m json.tool

# Namespace and bucket affected by the issue
ecscli namespace list
ecscli bucket get --namespace <namespace> --name <bucket>
```

Also provide:
- ECS Portal → Support → Collect Logs (per-node support bundle — mandatory for Severity 1/2 cases)
- VDC topology diagram (number of sites, nodes per VDC, replication group configuration)
- Approximate time the issue started
- Description of any recent changes (upgrades, replication group changes, network/firewall changes, new bucket or namespace creation)
- Error messages from the ECS Portal and from the S3/API client side

## SLA Tiers

| Severity | Description | Initial Response Target | Update Frequency |
|---|---|---|---|
| Severity 1 | Production cluster down / data inaccessible | 30 minutes | Every 2 hours until resolved |
| Severity 2 | Degraded cluster / significant impact | 2 hours | Every 4 hours |
| Severity 3 | Non-critical issue / minor impact | Next business day | As updated |
| Severity 4 | General question / low impact | 2 business days | As updated |

Response times are governed by your specific Dell support contract tier (Basic, ProSupport, ProSupport Plus, or Mission Critical). Verify your entitlement in the Support portal before assuming the above defaults.

## Escalation Path

1. **Case update**: Add a comment to the open case requesting escalation if progress is insufficient
2. **Account Team**: Contact your Dell account manager or technical account manager (TAM) to escalate a Sev1/Sev2 case that is not progressing
3. **Mission Critical escalation**: If you have a ProSupport Mission Critical contract, call the dedicated Mission Critical support line for immediate engineer engagement
4. **Executive escalation**: If the account team is unresponsive, request escalation through your Dell sales representative to Dell EMC Services management

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Ecs — Diagnostics](diagnostics/)
- [Ecs — Common Issues](common-issues/)
