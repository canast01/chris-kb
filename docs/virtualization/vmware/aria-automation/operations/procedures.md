---
tags:
  - aria-automation
  - operations
  - vmware
---
# Aria Automation — Operational Procedures

<div class="kb-summary">
Day-2 operational procedures for Aria Automation — managing cloud accounts, projects, catalog items, extensibility actions, and deployment lifecycle. Covers UI workflows and YAML blueprint management.

*Applies to: Aria Automation 8.x*
</div>

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

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Cloud Account and Infrastructure

---

## Add a Cloud Account

Registers a vCenter, AWS, Azure, or NSX-T endpoint so vRA can discover resources and provision workloads against it. Run this when onboarding a new vCenter cluster, a new cloud region, or any new infrastructure target.

1. Navigate to **Infrastructure → Connections → Cloud Accounts → Add Cloud Account**.
2. Select the account type (vCenter, AWS, GCP, Azure, NSX-T).
3. Enter the hostname/FQDN and credentials. For vCenter, enter the service account UPN and password.
4. Click **Validate** — vRA tests the connection before saving.
5. Select which data centers or regions to associate with the account.
6. Optionally associate an NSX-T manager at this step (vCenter accounts only).
7. Click **Add**.
8. After saving, verify the account appears in the cloud accounts list with a green status indicator.

```bash
# Verify the cloud account is reachable from the vRA appliance
ssh root@vra-prod-01.example.local
curl -sk -o /dev/null -w "%{http_code}" https://vcenter-prod.example.local/rest/com/vmware/cis/session
# Expected: 401 (Unauthorised — server is reachable)
# Any other output (000, curl error) indicates network or DNS issue
```

---

## Update Cloud Account Credentials

Use when a service account password has been rotated or an AWS access key has been replaced. Updating credentials in place avoids removing and re-adding the account, which would break existing projects and resource tags.

1. Navigate to **Infrastructure → Connections → Cloud Accounts**.
2. Click the three-dot menu next to the target account and select **Edit**.
3. Update the username and/or password fields.
4. Click **Validate** to confirm the new credentials are accepted.
5. Click **Save**.
6. Trigger a manual data collection (see below) to confirm inventory syncs correctly after the credential change.

---

## Trigger Manual Data Collection

Data collection polls the cloud account for current resource inventory. Trigger manually after adding a new account, updating credentials, or when vRA shows stale or missing resources.

1. Navigate to **Infrastructure → Connections → Cloud Accounts**.
2. Click the three-dot menu next to the target account.
3. Select **Start Data Collection**.
4. Monitor the data collection status — it transitions from **Running** to **Completed**.
5. If data collection fails, check the iaas-gateway logs:

```bash
kubectl logs -n prelude -l app=iaas-gateway --tail=100 | grep -i "error\|vcenter\|cloud"
```

---

## Configure Image Mappings and Flavor Mappings

Image mappings translate an abstract OS name (e.g., `ubuntu-22`) to a concrete template per cloud zone. Flavor mappings translate a size name (e.g., `small`) to a vSphere CPU/memory configuration or an AWS instance type. Both must be configured for each cloud zone before blueprints can deploy.
**Image Mappings:**

1. Navigate to **Infrastructure → Configure → Image Mappings**.
2. Select an existing mapping (or create a new one).
3. Click **Add Image** and choose the cloud zone.
4. Select the template/AMI from the discovered inventory.
5. Save.

**Flavor Mappings:**

1. Navigate to **Infrastructure → Configure → Flavor Mappings**.
2. Select an existing mapping (or create a new one).
3. Click **Add Flavor** and choose the cloud zone.
4. For vSphere, specify CPU count and memory (MB). For AWS/Azure, select the instance type.
5. Save.

Repeat for every cloud zone that blueprints will target.

---

## Configure a Network Pool

A network pool provides a range of IP addresses that vRA allocates to deployed VMs when IPAM is managed internally (without an external IPAM integration). Configure a network pool before creating projects that require static IP assignment.

1. Navigate to **Infrastructure → Configure → Networks**.
2. Select the **Network IP Ranges** tab and click **Add**.
3. Enter the network CIDR, gateway, DNS servers, and the usable IP range.
4. Assign the IP range to the appropriate network.
5. Navigate to **Infrastructure → Configure → Network Profiles**.
6. Create or edit the network profile for the target cloud zone.
7. Add the network to the profile and set the IP range as the allocation source.
8. Save the profile and verify it appears in the cloud zone configuration.

---

## Projects and Governance

---

## Create a Project

Projects are the primary isolation boundary in vRA. All deployments belong to a project, which controls which cloud zones are available, which users can consume, and what cost/quota limits apply.

1. Navigate to **Infrastructure → Administration → Projects → New Project**.
2. Enter a project name and optional description.
3. Under **Users**, add the project administrators and members (see next procedure).
4. Under **Provisioning**, add the cloud zones the project may deploy to. Set a priority for each zone if multiple are assigned.
5. Optionally set a custom naming template for VMs provisioned in this project.
6. Click **Create**.

---

## Add Users to a Project

Assign users or groups to a project to grant them the ability to deploy and manage resources. Roles within a project are: **Administrator**, **Member**, and **Viewer**.

1. Navigate to **Infrastructure → Administration → Projects**.
2. Click the project name to open it.
3. Select the **Users** tab.
4. Click **Add Users**.
5. Search for the user or group by name or email. vRA searches the configured vIDM directory.
6. Select the appropriate role: **Administrator** (full project control), **Member** (can deploy), or **Viewer** (read-only).
7. Click **Add**.

Group membership is resolved at login time; changes in the directory are reflected on next user authentication.

---

## Configure an Approval Policy

Approval policies intercept catalog requests and require one or more approvers to sign off before provisioning begins. Configure policies to enforce change control on production deployments or high-cost catalog items.
1. Navigate to **Service Broker → Content & Policies → Policies**.
2. Click **New Policy** and select **Approval Policy**.
3. Enter a name, description, and the scope (organization-wide or per-project).
4. Under **Approvers**, add individual users or groups who will receive approval requests.
5. Set the approval mode: **Any** (any one approver is sufficient) or **All** (every approver must approve).
6. Optionally set an auto-expiry timeout — requests not acted on within this window are auto-rejected.
7. Click **Create**.

---

## Assign an Approval Policy to a Catalog Item

After creating an approval policy, link it to one or more catalog items so that requests for those items trigger the approval workflow.
1. Navigate to **Service Broker → Content → Catalog Items**.
2. Click the target catalog item.
3. Select the **Policies** tab.
4. Click **Assign Policy** and select the approval policy from the list.
5. Save.

From this point, any request for that catalog item enters a pending state until the designated approvers act on it.

---

## Configure a Lease Policy

Lease policies automatically reclaim deployments after a defined time-to-live. Use lease policies to prevent resource sprawl in development and test projects.

1. Navigate to **Service Broker → Content & Policies → Policies**.
2. Click **New Policy** and select **Lease Policy**.
3. Enter a name and set the scope (organization-wide or per-project).
4. Set the **Maximum Lease Duration** — the hard limit on how long any deployment in scope can exist.
5. Set the **Maximum Total Lease Duration** — the upper bound including any user-requested extensions.
6. Optionally allow users to request lease extensions and set the maximum extension period.
7. Click **Create**.
8. vRA sends expiry notification emails to deployment owners before the lease ends. Confirm the SMTP relay is configured under **Administration → Email Servers** before enabling lease policies.

---

## Catalog and Blueprints

---

## Publish a Blueprint to the Catalog

Publishing makes a blueprint available to project members through the Service Broker catalog. The blueprint must be version-committed before it can be published.

1. Navigate to **Design → Blueprints**.
2. Open the target blueprint.
3. Click **Version** to commit the current state, entering a version number and change notes.
4. Click **Release** on the version to mark it as the active release.
5. Navigate to **Service Broker → Content → Content Sources**.
6. Ensure the Automation Assembler content source is configured and click **Sync** if needed.
7. Navigate to **Service Broker → Content → Catalog Items**.
8. Locate the blueprint and click **Configure** to set the icon, description, and access project.
9. Confirm the item is visible to the intended project members by checking the catalog as a member user.

---

## Unpublish a Catalog Item

Unpublishing removes a catalog item from consumer view without deleting the underlying blueprint or template. Use when a blueprint is being revised or retired.

1. Navigate to **Service Broker → Content → Catalog Items**.
2. Click the three-dot menu next to the target item.
3. Select **Unshare** or remove the item from the content source scope.
4. The item disappears from the consumer catalog immediately. Existing deployments created from this item are not affected.
5. If the item should be permanently retired, also archive the blueprint in Design → Blueprints to prevent accidental republishing.

---

## Import a Blueprint (YAML)

Use when migrating blueprints between vRA environments (dev → prod) or restoring from a backup export.

1. Navigate to **Design → Blueprints**.
2. Click **Import**.
3. Select the YAML file from the local filesystem.
4. Review the import summary — vRA highlights any resource types or cloud zones referenced in the YAML that do not exist in the target environment.
5. Resolve any missing references (update image/flavor mapping names to match the target environment).
6. Click **Import** to confirm.
7. Open the imported blueprint, verify the YAML renders correctly, and commit a version before publishing.

---

## Export a Blueprint (YAML)

Exports the current blueprint definition as a YAML file. Use for backup, version control storage, or migration to another environment.

1. Navigate to **Design → Blueprints**.
2. Open the target blueprint.
3. Click the three-dot menu and select **Export**.
4. Save the downloaded `.yaml` file. The export captures the current editor state; commit a version first if you want the export to match a specific release.

---

## Extensibility (ABX)

---

## Create an ABX Action

ABX (Action Based Extensibility) actions are event-driven scripts that run in response to vRA lifecycle events. Use them to integrate with external systems, send notifications, or enforce post-deployment configuration.
1. Navigate to **Extensibility → Actions → New Action**.
2. Enter a name, select the runtime (Python 3, Node.js, or PowerShell), and choose the execution context (on-premises FaaS or cloud).
3. Paste or write the action handler. The entry point must be `handler(context, inputs)`.

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

4. Add any required dependencies under **Dependencies** (pip packages for Python, npm packages for Node.js).
5. Define the expected input schema under **Inputs** — this allows vRA to pass event properties into the action.
6. Click **Save**.

---

## Create an Extensibility Subscription

Subscriptions bind an ABX action (or vRO workflow) to a specific lifecycle event. The subscription determines when the action fires (e.g., on deployment success, before VM power-off).
1. Navigate to **Extensibility → Subscriptions → New Subscription**.
2. Enter a name and select the event topic (e.g., `Deployment Completed`, `Compute Provision`).
3. Select the runnable: choose **Action** and pick the ABX action created above (or choose **Workflow** for vRO).
4. Optionally add a filter condition using a JEXL expression to restrict when the subscription fires (e.g., only for a specific project).
5. Set the subscription to **Blocking** if vRA must wait for the action to complete before proceeding, or **Non-blocking** for fire-and-forget.
6. Click **Save**.
7. Trigger a test deployment to confirm the subscription fires and the action executes without errors.

---

## Test an ABX Action Manually

Run an action outside of a subscription to validate logic and debug input/output before wiring it into a live event.

1. Navigate to **Extensibility → Actions** and open the target action.
2. Click **Test**.
3. In the test input panel, provide a JSON payload that mimics the properties the subscription would pass. Example:

```json
{
  "deploymentName": "test-deploy-01",
  "owner": "jsmith@example.local",
  "slackWebhook": "https://hooks.slack.com/services/TEST/TEST/TEST"
}
```

4. Click **Run Test**.
5. Review the **Execution Log** and **Output** tabs. A successful run shows `"status": 200` in the output.
6. Check **Extensibility → Action Runs** for the full execution history and any error stack traces.

---

## Day-2 Operations

---

## Force-Delete a Stuck Deployment

A deployment stuck in `CREATE_FAILED`, `DELETE_FAILED`, or `UPDATE_FAILED` cannot be removed through the normal UI delete flow. Use the API to force-delete it.

```bash
# Obtain a bearer token
TOKEN=$(curl -sk -X POST \
  "https://vra-prod-01.example.local/csp/gateway/am/api/login?access_token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","domain":"System Domain"}' | \
  jq -r '.access_token')

# List failed deployments
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/deployment/api/deployments?status=CREATE_FAILED&size=50" | \
  jq '.content[] | {id: .id, name: .name, owner: .ownedBy, status: .status}'

# Force-delete a specific deployment
DEPLOYMENT_ID="<id>"
curl -sk -X DELETE -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/deployment/api/deployments/$DEPLOYMENT_ID"
```

After the API call returns, refresh the deployments view in the UI to confirm the record is removed. If the underlying VMs were not cleaned up by the destroy workflow, delete them directly from vCenter.

---

## Find and Clean Up Orphaned Deployments

An orphaned deployment has a vRA record but no matching resource in the cloud account. This occurs when a VM is deleted directly in vCenter or AWS without going through vRA.

```bash
# List all deployments via API and cross-reference with vCenter
TOKEN=<your-token>
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/deployment/api/deployments?size=200" | \
  jq '.content[] | {id: .id, name: .name, status: .status, owner: .ownedBy}'
```

1. Export the deployment list from the API (above).
2. Cross-reference against the vCenter VM inventory or AWS EC2 instance list.
3. Identify deployment IDs with no corresponding resource.
4. For each orphaned deployment, attempt a normal UI delete first — vRA may clean up the record even if the resource is gone.
5. If the UI delete fails, use the force-delete API call from the procedure above.
6. After cleanup, trigger a manual data collection on the affected cloud account to reconcile inventory.

---

## Rotate Certificates (via LCM)

TLS certificates on vRA must be replaced before expiry. LCM manages certificate distribution across all products in an environment. Run this procedure 30 days before certificate expiry.

1. Generate a new certificate with the correct SAN entries (vRA FQDN and any load-balancer VIPs).
2. Log in to **LCM** (`https://lcm.example.local`).
3. Navigate to **Lifecycle Operations → Certificate Management**.
4. Click **Import Certificate** and paste the certificate chain and private key in PEM format.
5. Navigate to **Lifecycle Operations → Environments** and open the vRA environment.
6. Click **Edit** and under the product configuration, select the newly imported certificate.
7. Click **Trigger Certificate Update** — LCM redeploys the certificate to vRA and vIDM.
8. After LCM reports the operation as complete, validate:
   - Browse to the vRA UI and confirm the browser shows the new certificate with the correct expiry date.
   - Confirm SSO login works (vIDM relies on the same cert chain).
   - Confirm the Service Broker catalog loads and deployments can be submitted.

```bash
# Verify the new certificate expiry from the vRA appliance
echo | openssl s_client -connect vra-prod-01.example.local:443 -servername vra-prod-01.example.local 2>/dev/null \
  | openssl x509 -noout -dates
```

---

## Rotate the Postgres Password

vRA stores its configuration database password in `vracli`. Rotate this password when following periodic credential rotation policy or after a Postgres administrator password change.

```bash
# SSH to the vRA primary appliance
ssh root@vra-prod-01.example.local

# Update the Postgres password in vracli config
vracli pg password set --password '<new-password>'

# Restart the vRA services to pick up the new credentials
vracli rcs restart
```

After the restart, verify the vRA UI is accessible and that data collection runs complete without database connection errors. Check the Postgres-related logs if services fail to come up:

```bash
kubectl logs -n prelude -l app=vra-nginx --tail=100 | grep -i "error\|5[0-9][0-9]"
```

---

## Rotate the Admin Account Password

The vRA administrator account password is managed through the VAMI (Virtual Appliance Management Interface). Rotate this password when following credential rotation policy.

1. Open a browser and navigate to `https://vra-prod-01.example.local:5480`.
2. Log in with the current `root` or `admin` credentials.
3. Navigate to **Administration → Local Users**.
4. Select the `admin` or `root` account and click **Edit**.
5. Enter and confirm the new password.
6. Click **Save**.
7. If the admin account is also used as the vRA **System Domain** administrator:
   - Log in to the vRA UI (`https://vra-prod-01.example.local`) as the admin user with the new password.
   - Confirm access to **Infrastructure**, **Design**, and **Extensibility** tabs.
8. Update any automation scripts, monitoring integrations, or API callers that authenticate with this account.

---

## See also

- [Aria Automation — Health Checks](health-checks/)
- [Aria Automation — Common Issues](../troubleshooting/common-issues/)
- [Aria Automation — CLI Reference](cli-reference/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
