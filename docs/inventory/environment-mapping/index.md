# Environment Mapping

Document relationships between systems, applications, and services so that change impact, failure blast radius, and dependency chains are understood.

## Environment Tiers

| Tier | Purpose | Change Risk | SLA |
|---|---|---|---|
| Production | Live user-facing workload | Highest | Full SLA applies |
| Staging / Pre-prod | Final validation before production | High | Best effort |
| UAT | User acceptance testing | Medium | Business hours |
| Development | Active development | Low | No SLA |
| DR | Standby for production failover | High (when activated) | RTO/RPO as per DR plan |

## Dependency Map Template

For each application, document:

```markdown
## Application: Payments API

**Tier:** Production
**Hosts:** pay-api-01, pay-api-02, pay-api-03 (load balanced via alb-pay-prod)
**Owner:** Payments Team — payments-team@example.com

### Inbound Dependencies (who calls this service)
| Caller | Protocol | Port | Auth |
|---|---|---|---|
| Web frontend | HTTPS | 443 | JWT |
| Mobile app | HTTPS | 443 | JWT |
| Batch job (billing-cron) | HTTPS | 443 | mTLS |

### Outbound Dependencies (what this service calls)
| Target | Protocol | Port | Auth | Failure Impact |
|---|---|---|---|---|
| payments-db-primary | PostgreSQL | 5432 | DB user | Full outage |
| payments-db-replica | PostgreSQL | 5432 | DB user | Read-only degraded |
| fraud-detection-api | HTTPS | 443 | API key | Transactions blocked |
| vault | HTTPS | 8200 | AppRole | Auth fails; downtime |
| smtp-relay | SMTP | 25 | None | Email receipts fail only |

### Data Flows
- Payment transaction → payments-db → fraud-detection-api → response
- Audit log → kafka-payments-topic → SIEM

### Infrastructure
- Load Balancer: alb-pay-prod (AWS ALB)
- DNS: api.payments.example.com → alb-pay-prod CNAME
- TLS cert: *.payments.example.com — expires 2027-03-01
- Secrets: vault path `secret/payments/db_password`, `secret/payments/fraud_api_key`
```
┌─────────────────────────────────── Inventory — Environment Mapping ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Environment map: production, staging, dev, DR — document dependencies and data flows     │   │
│   │      Identify: shared services (AD, DNS, NTP) vs environment-specific (app, DB, storage)      │   │
│   │       DR site must mirror prod sizing; test failover path; document RTO/RPO per service       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Production         │  │        Non-Production       │  │        DR / Recovery        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Live workloads       │  │     Staging mirrors prod    │  │      Replication target     │   │
│   │        Change managed       │  │        Dev = isolated       │  │       Tested annually       │   │
│   │        Monitored 24/7       │  │     No prod data in dev     │  │       RTO/RPO defined       │   │
│   │         SLA enforced        │  │      Refresh from prod      │  │      Activation runbook     │   │
│   │      Access controlled      │  │     Config parity check     │  │        Config in sync       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Config parity = Staging config matches prod (versions, settings) for realistic testing             │
│    Data masking  = Replace prod PII with synthetic data before copying to non-prod environments       │
│    Shared service= Component used across environments (AD, DNS, NTP); single point of attention       │
│    Blast radius  = Scope of impact if an environment fails; keep prod isolated from dev               │
│    DR activation = Switch workloads to DR site; requires tested runbook and communications plan       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

### Azure

```bash
# List all resources by environment tag
az resource list --tag Environment=Production \
  --query '[*].{Name:name,Type:type,RG:resourceGroup,Location:location}' -o table

# Show VM and its disk / network dependencies
az vm show -g <rg> -n <vm-name> --show-details \
  --query '{Name:name,IP:publicIps,PrivateIP:privateIps,OS:storageProfile.osDisk.name}' -o json
```

## Change Impact Assessment

Before any change, use the dependency map to answer:

1. Which services call the component being changed?
2. What does the component depend on that might be affected?
3. If this change fails, what is the blast radius?
4. Which monitoring alerts should be watched during the window?
5. Who are the downstream service owners to notify?

## Mapping Maintenance

- Update dependency maps when: new service deployed, existing service retired, integration added or removed
- Review environment maps quarterly or after major incidents
- Keep maps in version-controlled docs alongside infrastructure code

## Discovery Tools

```bash
# netstat — find connections on a host
ss -tnp    # established TCP connections and owning process
ss -tlnp   # listening ports

# Find which process owns a port
lsof -i :<port>

# Trace network path to a service
traceroute <target-host>
mtr --report <target-host>

# DNS record discovery
dig <hostname> ANY
dig -t SRV _service._proto.<domain>
```
