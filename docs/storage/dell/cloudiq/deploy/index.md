---
tags:
  - dell
  - deployment
search:
  boost: 1.5
---
# CloudIQ — Initial Setup

<div class="kb-summary">
Step-by-step guide to connecting Dell storage systems to CloudIQ via the Secure Connect Gateway, verifying telemetry, and configuring alerts and notifications.

*Applies to: CloudIQ*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
prerequisites: "Prerequisites" {shape: rectangle}
install_secure_connect_gateway_scg: "Install Secure Connect Gateway (SCG)" {shape: rectangle}
register_storage_systems_with_scg: "Register Storage Systems with SCG" {shape: rectangle}
verify_telemetry_in_cloudiq_portal: "Verify Telemetry in CloudIQ Portal" {shape: rectangle}
configure_alert_notifications: "Configure Alert Notifications" {shape: rectangle}
add_additional_storage_systems: "Add Additional Storage Systems" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> install_secure_connect_gateway_scg
install_secure_connect_gateway_scg -> register_storage_systems_with_scg
register_storage_systems_with_scg -> verify_telemetry_in_cloudiq_portal
verify_telemetry_in_cloudiq_portal -> configure_alert_notifications
configure_alert_notifications -> add_additional_storage_systems
add_additional_storage_systems -> validate
```

## Before you begin

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

## Prerequisites

Before starting CloudIQ setup, confirm the following are available.

**Internet access:**

- The Secure Connect Gateway (SCG) appliance requires outbound HTTPS (443/TCP) to `cloudiq.dell.com`
- Proxy is supported — note proxy hostname, port, and credentials if required
- Outbound port 8443/TCP is also required for SCG-to-cloud telemetry

**Dell array access:**

- Administrative credentials for each storage array to be registered
- Arrays must have a valid support contract — CloudIQ requires active SupportAssist entitlement
- Array management IP reachable from the SCG VM

**Supported arrays (at deployment time):**

- Dell PowerStore, PowerMax, PowerFlex, PowerScale (Isilon), Unity XT
- VxRail, PowerEdge servers, and networking (optional)

**VM for SCG:**

- 4 vCPU, 8 GB RAM, 100 GB disk
- RHEL/CentOS 7+ or OVA-based deployment
- Static IP, DNS resolution, NTP sync

---

## Install Secure Connect Gateway (SCG)

The SCG is the on-premises component that collects telemetry from storage systems and forwards it to the CloudIQ cloud portal.

**OVA deployment (recommended):**

1. Download the SCG OVA from the Dell Support site (`dell.com/support`) under **Drivers & Downloads → Secure Connect Gateway**.
2. Deploy the OVA to vCenter using **Deploy OVF Template**.
3. On **Customize template**, set the static IP address, subnet, gateway, DNS, and NTP.
4. Power on the SCG VM and wait for first-boot configuration to complete (5–10 minutes).

**Initial SCG configuration:**

1. Open a browser to `https://<scg-ip>:9443` and log in with default credentials (`admin` / `admin`) — change immediately on first login.
2. Navigate to **Settings → Network** and confirm IP, DNS, and NTP settings are correct.
3. Navigate to **Settings → Connectivity** and enter proxy settings if required.
4. Click **Test Connection** to verify outbound connectivity to `cloudiq.dell.com` — the test must return **Success** before proceeding.
5. Navigate to **Settings → Registration** and sign in with your Dell Technologies (MyDell) account credentials to register the SCG instance with the CloudIQ portal.

---

## Register Storage Systems with SCG

1. In the SCG UI, navigate to **Devices → Add Device**.
2. Select the device type (e.g. PowerStore, Unity XT, PowerScale).
3. Enter the management IP or FQDN of the array and the array admin credentials.
4. Click **Test Connection** — the SCG must successfully authenticate to the array before saving.
5. Click **Save**.
6. The device appears in the **Devices** list with status **Registered**.
7. Repeat for each array.

**PowerScale (Isilon) specific:**

- Use the cluster management IP (SmartConnect zone or primary node)
- Credentials must be an account with the `ISI_PRIV_LOGIN_PAPI` privilege

**PowerMax specific:**

- Use the Unisphere management IP
- Ensure the Solutions Enabler or Unisphere API service is reachable from the SCG

---

## Verify Telemetry in CloudIQ Portal

1. Open a browser to `https://cloudiq.dell.com` and sign in with your Dell Technologies account.
2. Navigate to **Infrastructure → Storage**.
3. Newly registered arrays appear within 15–30 minutes of SCG registration.
4. Click on an array to open its detail view and confirm the following fields are populating:
   - **Capacity** — used, available, and total capacity with trend
   - **Performance** — IOPS, throughput, and latency charts
   - **Health score** — appears as a numeric score (0–100) with contributing issues listed
5. If an array does not appear after 30 minutes, check the SCG device list for errors and verify outbound connectivity from the SCG.

---

## Configure Alert Notifications

1. In the CloudIQ portal, navigate to **Settings → Notifications**.
2. Click **Add Notification Rule**.
3. Configure the rule:
   - **Name:** descriptive name (e.g. `Critical Storage Alerts - Ops Team`)
   - **Trigger:** select alert severity (Critical, Warning, or both)
   - **Resource scope:** all infrastructure, or filter to specific arrays or sites
   - **Notification channel:** email addresses or webhook URL
4. Click **Save**.
5. Test the rule by clicking **Send Test Notification** — confirm the test email or webhook payload is received.

**Recommended rules to create:**

- Critical alerts to on-call distribution list
- Warning alerts to storage team distribution list
- Capacity threshold alerts (e.g. >80% used) to capacity planning team

---

## Add Additional Storage Systems

To add more arrays after initial setup:

1. In the SCG UI, navigate to **Devices → Add Device** and repeat the registration process for each new array.
2. Verify each new array appears in the CloudIQ portal within 30 minutes.
3. If adding a new array type not previously registered, confirm the SCG software version supports that array model — update SCG from **Settings → Software Update** if required.

**SCG update process:**

```bash
# SSH to SCG appliance
ssh admin@<scg-ip>

# Check current version
sudo /opt/dell/scg/bin/scg-version.sh

# Apply available update from the SCG UI:
# Settings → Software Update → Check for Updates → Install
```

---

## Validate Data Collection

Run through the following checks to confirm the deployment is functioning correctly.

**SCG health:**

- SCG UI **Dashboard** — all registered devices show **Connected**
- SCG UI **Settings → Connectivity** — cloud connection shows **Active**
- No error entries in **SCG UI → Logs → System Logs**

**CloudIQ portal:**

- All arrays appear under **Infrastructure → Storage**
- Health scores are populated for all arrays (may take up to 2 hours for initial score)
- Performance graphs show recent data points (within the last collection interval — typically 5 minutes)
- Capacity data shows correct values matching array management UI

**Alerts:**

- At least one test notification has been sent and received for each notification rule
- Review **CloudIQ → Alerts** to confirm open issues are visible and match what is expected for the environment

**Ongoing:**

- Review **Recommendations** tab weekly — CloudIQ AI surfaces configuration, capacity, and performance improvement recommendations
- Check **Health → Wellness** monthly for proactive hardware replacement recommendations

---

## See also

- [Cloudiq — Procedures](../operations/procedures/)
- [Cloudiq — Common Issues](../troubleshooting/common-issues/)
- [Cloudiq — How It Works](../architecture/how-it-works/)
