# Aria Automation — Procedures

## Rotate Service Account Passwords

When rotating vCenter or NSX service account passwords:

1. Update the password in the target system (vCenter/NSX)
2. In Aria Automation, navigate to **Infrastructure > Connections > Cloud Accounts**
3. Edit each affected cloud account and update the credentials
4. Click **Validate** to confirm connectivity is restored

## Stale Deployment Cleanup

Review **Deployments > All Deployments** and delete or expire deployments that are orphaned or past their lease date.

## Blueprint and Template Versioning

Review **Design > Cloud Templates** for templates with no recent activity. Archive unused versions. Ensure all active templates have a description and are version-controlled in the connected SCM repository.

## Cloud Account Connectivity Failure

1. Test network connectivity from appliance to vCenter/NSX management plane
2. Confirm service account credentials have not expired
3. Re-validate cloud account in Aria Automation UI
4. If re-validation fails, check logs: `kubectl logs -n prelude -l app=vra-nginx`
