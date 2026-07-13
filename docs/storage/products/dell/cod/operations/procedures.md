---
tags:
  - dell
  - operations
description: "Procedures reference covering COD Activation Procedure, Incident Triage."
---
# COD — Procedures

<div class="kb-summary">
Procedures reference covering COD Activation Procedure, Incident Triage.

*Applies to: Cloud for Desktop (COD)*
</div>

> Part of the [COD](../index.md) reference.

---

```d2
direction: right

cod_activation_procedure: "COD Activation Procedure" {shape: rectangle}
incident_triage: "Incident Triage" {shape: rectangle}
create_an_object_storage_bucket: "Create an Object Storage Bucket" {shape: rectangle}
configure_bucket_lifecycle_policy: "Configure Bucket Lifecycle Policy" {shape: rectangle}
create_access_keys_for_an_applicatio: "Create Access Keys for an Application" {shape: rectangle}
enable_bucket_replication: "Enable Bucket Replication" {shape: rectangle}

cod_activation_procedure -> incident_triage
incident_triage -> create_an_object_storage_bucket
create_an_object_storage_bucket -> configure_bucket_lifecycle_policy
configure_bucket_lifecycle_policy -> create_access_keys_for_an_applicatio
create_access_keys_for_an_applicatio -> enable_bucket_replication
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## COD Activation Procedure

1. Confirm the COD activation is required and the change ticket is approved
2. Log in to Unisphere and navigate to Settings > License > Capacity on Demand
3. Submit the activation request specifying the number of additional TB required
4. Monitor the activation status in Unisphere — expect propagation within 10-15 minutes
5. Validate the new capacity is visible via SYMCLI:
   ```bash
   symcfg -sid <sid> show -capacity -gb
   symlmf -sid <sid> list
   ```
6. Confirm the new capacity is available to the SRP and workloads are not impacted
7. Update the change ticket with the post-activation capacity figures

## Incident Triage

**On alert or issue:**
1. Log in to Unisphere or connect via SYMCLI to identify the exact utilization and licensing state
2. Check SYMCLI event log for any licensing-related errors: `symelog -sid <sid> list -type license`
3. Confirm the COD activation request was submitted via the correct channel (Unisphere > Settings > License > Activate Capacity)
4. If activation is rejected, verify the Dell account is current and the COD entitlement has not expired
5. Open a Dell support case if the activation cannot proceed through Unisphere

| Symptom | Likely Cause | Action |
|---|---|---|
| Unexpected capacity consumption spike | Workload growth or new provisioning without capacity planning | Run `symcfg -sid <sid> list -srp -detail`, identify which SRP/SG consumed capacity, review provisioning activity |
| COD activation rejected in Unisphere | Entitlement expired or account issue | Check license entitlement via `symlmf -sid <sid> list`, contact Dell account team |
| Licensing error in SYMCLI | Expired or invalid license file | Run `symlmf -sid <sid> list` to show license state, check expiry, open Dell support case |
| COD capacity not visible after activation | Activation not yet propagated | Wait up to 15 minutes, then re-run `symcfg -sid <sid> show -capacity -gb` |
| Unisphere cannot reach Dell licensing backend | Proxy or firewall blocking outbound HTTPS | Check SCG connectivity, verify proxy settings in Unisphere |

---

## Create an Object Storage Bucket

1. Log in to the COD management portal and navigate to **Buckets → New Bucket**
2. Specify the bucket name (must be globally unique within the namespace), storage class, and whether versioning should be enabled
3. Configure a retention policy if required (WORM / compliance mode)
4. Set the access policy: private (default), authenticated read, or public — apply the principle of least privilege
5. Click **Save** — the bucket is immediately available for object PUT/GET operations
6. Test by uploading a small test object using the portal or S3 CLI: `aws s3 cp test.txt s3://<bucket-name>/ --endpoint-url <cod-endpoint>`

## Configure Bucket Lifecycle Policy

1. In the COD portal, navigate to **Buckets** and select the target bucket
2. Click **Lifecycle → Add Rule**
3. Configure a transition rule: move objects to the cold storage tier after N days of last access
4. Configure an expiration rule: permanently delete objects after N days (or N days after transition)
5. Set a rule scope: apply to all objects or to objects matching a specific prefix or tag
6. Click **Save** — lifecycle rules are evaluated daily; changes take effect within 24 hours
7. Monitor the **Analytics → Storage Tiers** view to confirm objects are transitioning as expected

## Create Access Keys for an Application

1. In the COD portal, navigate to **Users/Applications** and select or create a service account dedicated to the application
2. Click **Generate Access Key** — the portal displays the Access Key ID and Secret Access Key once
3. Save both values securely in the organisation's secret management store (e.g. HashiCorp Vault) immediately — the secret cannot be retrieved again
4. Configure the application with the endpoint URL, Access Key ID, and Secret Access Key
5. Test connectivity: `aws s3 ls s3://<bucket-name>/ --endpoint-url <cod-endpoint>`
6. Rotate access keys on the schedule defined in the security policy; delete old keys after rotation is confirmed

## Enable Bucket Replication

1. In the COD portal, navigate to **Buckets** and select the source bucket
2. Click **Replication → Configure Replication**
3. Enter the destination bucket name and target endpoint/region
4. Specify the replication scope: all objects, or objects matching a prefix or tag
5. Enable replication and save — the portal starts replicating new objects immediately
6. Test replication: upload a test object to the source bucket and confirm it appears in the destination bucket within the expected replication lag window

## Restore a Previous Object Version

1. In the COD portal, navigate to **Buckets** and select the bucket (versioning must be enabled)
2. Click **Objects** and locate the object to restore
3. Click the object name to open the version history — all versions are listed with timestamp and size
4. Select the desired previous version and click **Restore** — COD copies the selected version as the new current version
5. Verify the restored content is accessible: download and confirm the object content is as expected
6. The previous (overwritten) version is retained in history unless a lifecycle expiration rule removes it

## Generate Capacity Utilisation Report

1. In the COD portal, navigate to **Analytics → Capacity**
2. Set the date range for the report period
3. Review the breakdown by bucket, storage class (hot vs cold), and total namespace usage
4. Click **Export CSV** to download the report for capacity planning, chargeback, or finance review
5. Schedule recurring exports if the portal supports it, or automate via the COD S3 API to pull usage metrics on a schedule

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Cod — Health Checks](../health-checks/)
- [Cod — CLI Reference](../cli-reference/)
- [Cod — Common Issues](../../troubleshooting/common-issues/)
