# Aria Automation — Procedures


<div class="kb-summary">
Procedures reference covering Rotate Service Account Passwords, Stale Deployment Cleanup, Cloud Account Connectivity Failure, Adding a New Cloud Zone to a Project, Adding an Approval Policy and 1 more sections.
</div>

## Rotate Service Account Passwords

When rotating vCenter or NSX service account passwords:

1. Update the password in the target system (vCenter local account or AD)
2. In Aria Automation: **Infrastructure → Connections → Cloud Accounts**
3. Edit each affected cloud account and update the credentials
4. Click **Validate** to confirm connectivity is restored
5. Check **Design → Cloud Templates** — ensure any templates referencing the credential are not broken

---

## Stale Deployment Cleanup

Review **Deployments → All Deployments** and address deployments that are orphaned or past their lease:

```bash
# List expired deployments via API
TOKEN=<your-token>
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/deployment/api/deployments?status=CREATE_FAILED&size=50" | \
  jq '.content[] | {id: .id, name: .name, owner: .ownedBy, status: .status}'

# Delete a specific deployment (Day-2 action — fires the destroy workflow)
DEPLOYMENT_ID="<id>"
curl -sk -X DELETE -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/deployment/api/deployments/$DEPLOYMENT_ID"
```
```text
┌────────────────────────────── Aria Automation — Operational Procedures ───────────────────────────────┐
│                                                                                                       │
│  Common vRA operational tasks: cert rotation, password rotation, account changes, cleanup.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Certificate Rotation             │  │              Password Rotation              │   │
│   │      Generate new cert (SAN: vRA FQDN)       │  │      vRA admin password: VAMI → change      │   │
│   │        Import via LCM cert management        │  │     Postgres password: vracli + restart     │   │
│   │       LCM redeploys certs to products        │  │      Cloud account creds: update in UI      │   │
│   │        Validate SSO and catalog after        │  │      Service account: rotate + test ABX     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Account and resource management procedures keep vRA clean and correctly scoped.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Cloud Account Management           │  │               Resource Cleanup              │   │
│   │       Add: wizard + test connectivity        │  │      Orphaned deployments: force delete     │   │
│   │        Update creds: edit + reconnect        │  │    Stale catalog items: unpublish+delete    │   │
│   │      Remove: detach from projects first      │  │      Expired leases: auto or manual del     │   │
│   │      Data collection: trigger manually       │  │     ABX logs: retained 30d, purge older     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA appliances · LCM appliance · Postgres · vIDM · vCenter · CA for cert issuance                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cert rotation     = Replacing expiring TLS cert on vRA via LCM certificate management UI             │
│  LCM cert push     = LCM distributes updated cert to all products in the Environment                  │
│  VAMI password     = Root/admin password for vRA appliance changed via VAMI web UI at :5480           │
│  Postgres creds    = DB credentials stored in vracli config; update and restart service               │
│  Cloud account creds= AWS access key / vCenter password stored in vRA; edit without removing          │
│  Force delete      = vRA admin can hard-delete stuck deployments via API or UI override               │
│  Orphaned resource = Deployment record in vRA with no matching resource in cloud account              │
│  Data collection   = vRA polls cloud accounts for resource inventory; trigger via UI or API           │
│  Lease expiry      = Automated deletion triggered by lease policy when deployment exceeds TTL         │
│  ABX log retention = Action run logs stored 30 days; older logs purged automatically                  │
│  Unpublish item    = Remove catalog item from consumer view without deleting the template             │
│  Service account   = vRA uses a service account to authenticate to AD, vCenter, and NSX               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Cloud Account Connectivity Failure

1. Verify network connectivity from the Aria Automation appliance to the target system:

```bash
ssh root@vra-prod-01.example.local
curl -sk -o /dev/null -w "%{http_code}" https://vcenter-prod.example.local/rest/com/vmware/cis/session
# Expected: 401 (Unauthorised — server is reachable)
# Any other output (000, curl error) indicates network or DNS issue
```

2. Confirm the service account credentials have not expired:
   - vCenter: **vCenter → Administration → Single Sign On → Users and Groups → check account expiry**
   - NSX-T: **NSX-T → System → Users and Roles → check last password change**

3. Re-validate the cloud account in Aria Automation UI

4. If re-validation fails, check logs:

```bash
kubectl logs -n prelude -l app=vra-nginx --tail=100 | grep -i "error\|5[0-9][0-9]"
kubectl logs -n prelude -l app=iaas-gateway --tail=100 | grep -i "error\|vcenter\|cloud"
```

---

## Adding a New Cloud Zone to a Project

1. **Infrastructure → Cloud Zones → New Cloud Zone**:
   - Select cloud account
   - Select region/datacenter
   - Set tag-based placement constraints (e.g., `env:prod`, `tier:compute`)

2. **Infrastructure → Administration → Projects → select project → Cloud Zones → Add**:
   - Add the new cloud zone
   - Set CPU/memory/storage limits
   - Set priority (lower number = higher priority for placement)

3. Add image mappings and flavor mappings for the new cloud zone:

```text
Infrastructure → Configure → Image Mappings → add entry for new zone
Infrastructure → Configure → Flavor Mappings → add entry for new zone
```

4. Test by deploying a simple template targeted at the new cloud zone

---

## Adding an Approval Policy

Approval policies require a manager or team lead to approve requests before provisioning begins.

**Create a policy:**

```bash
Service Broker → Content & Policies → Policies → New Policy → Approval Policy
```

Configure:
- Name: `PROD VM Deployment Approval`
- Scope: apply to a specific project or catalog item
- Approver: AD group (e.g., `GG-VRA-Approvers`) — any member can approve
- Auto-expire: 5 business days — requests unapproved within this window are auto-rejected

**Assign to catalog item:**

```bash
Service Broker → Content → Catalog Items → select item → Policy → assign the approval policy
```

Test by requesting the catalog item as a non-admin user — an approval request notification should be sent to the approver group.

---

## Importing an ABX Action

Action-Based Extensibility (ABX) actions are scripts (Python, Node.js, or PowerShell) that execute in response to event broker triggers.

```text
Extensibility → Actions → New Action
```

1. Select language (Python 3 recommended)
2. Paste or upload the action script
3. Set dependencies in the requirements field (e.g., `requests==2.28.0`)
4. Add input constants (environment variables accessible within the action)
5. Test via **Test** tab before assigning to an event broker subscription

**Example: Slack notification on deployment success:**

```python
import requests

def handler(context, inputs):
    webhook_url = inputs.get("slackWebhook")
    deployment_name = inputs["deploymentName"]
    owner = inputs["owner"]
    
    message = {
        "text": f":white_check_mark: Deployment *{deployment_name}* succeeded for {owner}"
    }
    resp = requests.post(webhook_url, json=message)
    return {"status": resp.status_code}
```

Assign to an event broker subscription:

```text
Extensibility → Subscriptions → New Subscription
```

- Event topic: `Deployment Success`
- Action: select the ABX action
- Condition: filter by project or deployment name if needed
