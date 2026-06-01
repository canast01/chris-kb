# PowerStore — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Opening a Support Case, Required Information for a Case, Case Priority Levels, Escalation Path and 4 more sections.
</div>

## Support Portal

Dell PowerStore support cases are logged through the Dell support portal at [https://www.dell.com/support](https://www.dell.com/support). PowerStore is covered under the ProSupport or ProSupport Plus contract associated with the system's service tag.

Access the portal with a Dell account that is associated with your company's service contracts. If you do not have a Dell account, your account team can provision access.

## Opening a Support Case

### Via PowerStore Manager (Recommended)

The fastest method for opening a case is directly from PowerStore Manager, which pre-populates the case with the system serial number, software version, and relevant logs:

1. PowerStore Manager → **Help → Contact Support → Open Service Request**
2. Describe the symptom and impact
3. Attach additional diagnostics if available (support package, log dumps)

Dell SupportAssist (if enabled and connected) may already have automatically created a case for qualifying hardware faults — check **PowerStore Manager → Help → My Cases** before opening a duplicate.

### Via Dell Support Portal

If PowerStore Manager is inaccessible:

1. Navigate to [https://www.dell.com/support](https://www.dell.com/support)
2. Sign in and go to **My Products and Services → Service Requests → Create New**
3. Select **PowerStore** as the product type
4. Enter the system service tag (serial number)

### Via Phone

| Region | Phone Number |
|---|---|
| Global (main) | +1 800 945 3355 |
| UK | +44 0800 028 2847 |
| Germany | +49 0800 000 3672 |
| Australia | +61 1800 812 393 |

For P1 (critical production-down) issues, always call after opening the portal case — phone escalation is faster than portal-only for urgent issues.

## Required Information for a Case

Always collect this data before or immediately after opening the case:

| Field | How to Obtain |
|---|---|
| System service tag / serial number | PowerStore Manager → Hardware → Appliance |
| PowerStoreOS version | `GET /api/rest/software_installed` |
| Appliance model | PowerStore Manager → Dashboard or `GET /api/rest/appliance` |
| Active alerts at time of incident | `GET /api/rest/alert?state=active` |
| Event log (last 24 hours) | `GET /api/rest/event?order=created_timestamp desc` |
| Support package | PowerStore Manager → Help → Collect Support Materials |
| Affected workloads | List volumes, hosts, and applications affected |
| Timeline | When the issue started; what changed before it occurred |
| Error message | Exact text from alerts or REST API responses |
| Impact statement | Production down / degraded / single host / DR site |

## Case Priority Levels

| Priority | Condition | Dell Response Time | Coverage |
|---|---|---|---|
| P1 — Critical | Production system down; all hosts have lost storage access | 2 hours initial response; continuous engagement | 24×7×365 |
| P2 — High | Production system degraded; significant performance impact; DR capability lost | 4 hours initial response | 24×7×365 |
| P3 — Medium | Degraded functionality; workaround available; non-production impacted | Next business day | Business hours |
| P4 — Low | General question; documentation request; minor issue with workaround | Next business day | Business hours |

ProSupport Plus subscribers receive enhanced SLAs including proactive mission-critical support and next-business-day onsite hardware replacement.

## Escalation Path

### Level 1 — Open a P1/P2 Case

For any production-impacting issue, open the case at P1 or P2 priority immediately. Include the impact statement in the case description — this determines initial routing.

### Level 2 — Request Technical Account Manager (TAM) Escalation

If you have a ProSupport Plus contract with a TAM assigned, contact your TAM directly for critical escalations:

- TAMs can escalate to engineering and expedite hardware dispatch
- TAM contact details are in your Dell account profile under **My Team**

### Level 3 — Executive Escalation

For prolonged P1 incidents (P1 open for more than 4 hours without satisfactory progress):

1. Call Dell support and request escalation to the **Duty Manager** or **Global Escalation Team**
2. Contact your **Dell account executive** and request formal executive escalation
3. Dell's escalation process triggers a bridge call with engineering involvement and executive sponsorship

## SupportAssist — Automated Case Creation

With SupportAssist enabled and connected, PowerStore automatically creates service requests for qualifying hardware faults (drive failures, power supply faults, node hardware alerts). These cases are pre-populated with diagnostic data and sent directly to Dell's proactive monitoring team.

Verify SupportAssist is connected: **PowerStore Manager → Settings → Support → SupportAssist → Status: Connected**.

If SupportAssist shows disconnected:

```bash
# Test outbound connectivity to Dell SRS
curl -k https://esrs3.emc.com   # Should return a 200 or redirect

# Check proxy configuration if behind a proxy
# PowerStore Manager → Settings → Support → SupportAssist → Proxy Settings

# Verify DNS resolution
nslookup esrs3.emc.com   # From the management network
```

## Remote Support Sessions

Dell Support engineers can initiate remote sessions through SupportAssist. These sessions are:

- Initiated by Dell from the SRS cloud — Dell engineers cannot initiate sessions without your consent
- Routed through the SRS gateway (not directly to your management IP)
- Audited — all session activity is logged

To permit a remote session:

1. The Dell support engineer will provide a session ID
2. In PowerStore Manager → **Help → Remote Support Sessions → Approve Session** — enter the session ID
3. The session is active for the duration specified; it terminates automatically at expiry

You can monitor active remote sessions and revoke them at any time from the same Remote Support Sessions view.

## Diagnostic Resources

| Resource | URL | Use |
|---|---|---|
| Dell Support Portal | [https://www.dell.com/support](https://www.dell.com/support) | Case management, downloads, knowledge base |
| Dell PowerStore Documentation | [https://www.dell.com/support/home/en-us/product-support/product/powerstore/docs](https://www.dell.com/support/home/en-us/product-support/product/powerstore/docs) | Official product documentation |
| Dell Security Advisories | [https://www.dell.com/support/security](https://www.dell.com/support/security) | CVEs and security patches for PowerStoreOS |
| Dell PowerStore Interoperability Matrix | [https://elabnavigator.dell.com](https://elabnavigator.dell.com) | Host OS, HBA, switch, and software compatibility |
| Dell Community Forums | [https://www.dell.com/community](https://www.dell.com/community) | Peer knowledge base; useful for non-critical questions |

## Escalation Checklist (P1 Incident)

Use this checklist when a P1 incident is declared:

- [ ] Support case opened at P1 priority with impact statement (production down)
- [ ] Dell support engineer on the bridge call or acknowledged via portal
- [ ] Support package attached to the case or upload in progress
- [ ] System serial number, software version, and hardware model confirmed with support
- [ ] Timeline documented: when the issue started; what changed; which hosts are affected
- [ ] SupportAssist confirmed — check if Dell has an existing automated case for this incident
- [ ] Internal incident declared; application owners and management notified
- [ ] TAM contacted if ProSupport Plus (can expedite engineering engagement)
- [ ] Change freeze enacted — no additional changes until the P1 is resolved
- [ ] If hardware fault: confirm Dell has dispatched the replacement component (check case notes)
- [ ] DR failover readiness assessed — if site is at risk, evaluate failing over to DR
