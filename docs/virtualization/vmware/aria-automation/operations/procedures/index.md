# Aria Automation — Procedures

```
┌─────────────────────────────────────────────────────────────┐
│         Aria Automation — Common Operational Tasks          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Service Account Rotation                                   │
│  vCenter/NSX password changed → Cloud Account → Validate    │
│                                                             │
│  Stale Deployment Cleanup                                   │
│  API: status=CREATE_FAILED → DELETE  ·  UI: Force Delete    │
│                                                             │
│  Blueprint Versioning                                       │
│  Design → Cloud Templates → Git Content Source → Sync       │
│                                                             │
│  Cloud Zone → Project                                       │
│  New Cloud Zone → Add to Project → Image/Flavor Mappings    │
│                                                             │
│  Approval Policy                                            │
│  Policies → Approval Policy → AD Approver Group             │
│  auto-reject after 5 business days                          │
│                                                             │
│  ABX Action (Extensibility)                                 │
│  Actions (Python/Node/PS) → Test → Subscription             │
│  Event topic: Deployment Success / Failure / etc.           │
└─────────────────────────────────────────────────────────────┘
```

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
  "https://vra-prod-01.corp.local/deployment/api/deployments?status=CREATE_FAILED&size=50" | \
  jq '.content[] | {id: .id, name: .name, owner: .ownedBy, status: .status}'

# Delete a specific deployment (Day-2 action — fires the destroy workflow)
DEPLOYMENT_ID="<id>"
curl -sk -X DELETE -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.corp.local/deployment/api/deployments/$DEPLOYMENT_ID"
```

In the UI: select the deployment → **Actions → Delete** (or **Force Delete** if the deployment is stuck).

---

## Blueprint and Template Versioning

Review **Design → Cloud Templates** monthly:

1. Archive unused templates: set status to **Draft** and add `[ARCHIVED]` to the name
2. Ensure all active templates have a description, owner, and version tag
3. Connect templates to a Git content source for version history:

```
Infrastructure → Connections → Integrations → Add Git Integration
```

Provide GitHub/GitLab URL, branch, and personal access token. Templates are then sync'd from the repository.

Template naming convention:
```
<team>-<resource-type>-<os/platform>-<size>
# Examples:
platform-vm-rhel9-small
app-vm-win2022-medium
shared-k8s-namespace-standard
```

---

## Cloud Account Connectivity Failure

1. Verify network connectivity from the Aria Automation appliance to the target system:

```bash
ssh root@vra-prod-01.corp.local
curl -sk -o /dev/null -w "%{http_code}" https://vcenter-prod.corp.local/rest/com/vmware/cis/session
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

```
Infrastructure → Configure → Image Mappings → add entry for new zone
Infrastructure → Configure → Flavor Mappings → add entry for new zone
```

4. Test by deploying a simple template targeted at the new cloud zone

---

## Adding an Approval Policy

Approval policies require a manager or team lead to approve requests before provisioning begins.

**Create a policy:**

```
Service Broker → Content & Policies → Policies → New Policy → Approval Policy
```

Configure:
- Name: `PROD VM Deployment Approval`
- Scope: apply to a specific project or catalog item
- Approver: AD group (e.g., `GG-VRA-Approvers`) — any member can approve
- Auto-expire: 5 business days — requests unapproved within this window are auto-rejected

**Assign to catalog item:**

```
Service Broker → Content → Catalog Items → select item → Policy → assign the approval policy
```

Test by requesting the catalog item as a non-admin user — an approval request notification should be sent to the approver group.

---

## Importing an ABX Action

Action-Based Extensibility (ABX) actions are scripts (Python, Node.js, or PowerShell) that execute in response to event broker triggers.

```
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

```
Extensibility → Subscriptions → New Subscription
```

- Event topic: `Deployment Success`
- Action: select the ABX action
- Condition: filter by project or deployment name if needed
