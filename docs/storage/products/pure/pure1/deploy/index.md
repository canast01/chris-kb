---
tags:
  - deployment
  - pure
search:
  boost: 1.5
description: "Step-by-step guide to enabling Phone Home on Pure Storage FlashArray and FlashBlade, verifying array registration in the Pure1 cloud portal, and..."
---
# Pure1 — Initial Setup

<div class="kb-summary">
Step-by-step guide to enabling Phone Home on Pure Storage FlashArray and FlashBlade, verifying array registration in the Pure1 cloud portal, and configuring access and alerting.

*Applies to: Pure1*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
prerequisites: "Prerequisites" {shape: rectangle}
enable_phone_home_on_flasharray: "Enable Phone Home on FlashArray" {shape: rectangle}
enable_phone_home_on_flashblade: "Enable Phone Home on FlashBlade" {shape: rectangle}
verify_array_appears_in_pure1: "Verify Array Appears in Pure1" {shape: rectangle}
configure_user_access: "Configure User Access" {shape: rectangle}
configure_alert_notifications: "Configure Alert Notifications" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> enable_phone_home_on_flasharray
enable_phone_home_on_flasharray -> enable_phone_home_on_flashblade
enable_phone_home_on_flashblade -> verify_array_appears_in_pure1
verify_array_appears_in_pure1 -> configure_user_access
configure_user_access -> configure_alert_notifications
configure_alert_notifications -> validate
```

## Before you begin

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

## Prerequisites

Before starting Pure1 setup, confirm the following.

**Internet-connected FlashArray/FlashBlade:**

- FlashArray running Purity//FA 5.3.0 or later (Purity 6.x recommended)
- FlashBlade running Purity//FB 3.2.0 or later
- Array management IP must have outbound HTTPS (443/TCP) access to `pure1.purestorage.com`
- DNS resolution must work from the array management interface
- If an outbound proxy is in use, the proxy hostname, port, and credentials are required

**Pure Storage support account:**

- Active Pure Storage support account at `support.purestorage.com`
- The account must be linked to the organisation that owns the arrays
- Arrays must have an active support contract

**NTP:**

- Array NTP must be synchronised — time skew causes Phone Home authentication failures

**Network checklist:**

| Destination | Port | Protocol | Purpose |
|---|---|---|---|
| `pure1.purestorage.com` | 443 | HTTPS | Phone Home and API |
| `support.purestorage.com` | 443 | HTTPS | Support case integration |

---

## Enable Phone Home on FlashArray

Phone Home is the mechanism by which FlashArray sends telemetry and configuration data to Pure1.

**Via the FlashArray UI:**

1. Open a browser to `https://<flasharray-management-ip>` and log in as `pureuser` or an array admin account.
2. Navigate to **Settings → Support → Phone Home**.
3. Toggle **Phone Home** to **On**.
4. If a proxy is required, click **Proxy** and enter the proxy server address and port.
5. Click **Test Phone Home** — the test must return **Success** before proceeding.
6. Confirm the **Last Phone Home** timestamp updates to the current time.

**Via the FlashArray CLI:**

```bash
# SSH to the array
ssh pureuser@<flasharray-ip>

# Enable Phone Home
puresupport phonehome --enable

# Set proxy if required
puresupport phonehome --proxy https://proxy.company.local:3128

# Test Phone Home
puresupport phonehome --test

# Confirm status
puresupport phonehome
```


```text title="Expected output"
pureuser@flasharray-ip's password: 
Pure Storage FlashArray//X20 (10.0.0.1)
purity> puresupport phonehome --enable
Phone Home: enabled
purity> puresupport phonehome --proxy https://proxy.company.local:3128
Proxy: https://proxy.company.local:3128
purity> puresupport phonehome --test
Phone Home test initiated
Contacting support.purestorage.com... OK
Connection successful
purity> puresupport phonehome
Phone Home: enabled
Proxy: https://proxy.company.local:3128
Last successful contact: 2024-01-15 14:32:18 UTC
Next scheduled contact: 2024-01-16 02:32:18 UTC
purity>
```

!!! warning "Common errors"
    **`Phone Home: disabled`** — Run `puresupport phonehome --enable` before testing to activate the feature.
    **`Connection failed: Unable to reach proxy`** — Verify the proxy URL and port are correct with your network team, then re-run `puresupport phonehome --proxy <url>`.
Expected output from `puresupport phonehome` after enabling:

```text
Enabled:   True
Status:    Connected
Proxy:     -
```

---

## Enable Phone Home on FlashBlade

**Via the FlashBlade UI:**

1. Open a browser to `https://<flashblade-management-ip>` and log in as an admin account.
2. Navigate to **Settings → Support → Phone Home**.
3. Toggle **Phone Home** to **On**.
4. Click **Send Now** to initiate an immediate Phone Home and confirm the status shows **Sent**.

**Via the FlashBlade CLI:**

```bash
# SSH to the FlashBlade
ssh pureuser@<flashblade-ip>

# Check Phone Home status
purefb support

# Enable Phone Home
purefb support set --phonehome-enabled true

# Test Phone Home
purefb support test

# Confirm last send time
purefb support
```


```text title="Expected output"
pureuser@flashblade-ip's password: 
Connected to FlashBlade (192.168.1.50)

Phone Home Status:
  Enabled: false
  Last Send: 2024-01-15 09:32:14 UTC
  Next Send: 2024-01-22 09:32:14 UTC

Phone Home enabled successfully.

Test message sent successfully.
  Message ID: msg-7f3a9c2e-b1d4-4a2f-91e3-5c8d2a1b9f6e
  Timestamp: 2024-01-18 14:22:47 UTC
  Status: Delivered

Phone Home Status:
  Enabled: true
  Last Send: 2024-01-18 14:22:47 UTC
  Next Send: 2024-01-25 14:22:47 UTC
```

!!! warning "Common errors"
    **`Permission denied (publickey,password).`** — Verify the FlashBlade IP address is correct and the pureuser credentials are valid in your environment.
    **`purefb: command not found`** — SSH directly to the FlashBlade management interface (not a jump host) where the purefb CLI is available.
    **`Phone Home test failed: No network connectivity`** — Ensure the FlashBlade has outbound HTTPS access to Pure Storage's support servers (typically port 443).
**Proxy configuration for FlashBlade:**

```bash
purefb support set --proxy https://proxy.company.local:3128
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Invalid proxy URL format`** — Ensure the proxy URL follows the format `scheme://host:port` and use a valid port number between 1-65535.
    **`Error: Unable to reach proxy server at https://proxy.company.local:3128`** — Verify the proxy server is reachable from the FlashBlade management network and that firewall rules allow outbound connections on port 3128.
---

## Verify Array Appears in Pure1

1. Open a browser to `https://pure1.purestorage.com` and sign in with your Pure Storage support account.
2. Navigate to **Fleet → Arrays**.
3. Arrays that have successfully completed Phone Home appear in the list within 15–30 minutes of enabling Phone Home.
4. If an array does not appear after 30 minutes:
   - Confirm Phone Home is enabled and the last send timestamp is recent.
   - Check that outbound HTTPS to `pure1.purestorage.com` is not blocked by firewall.
   - Review the array syslog for Phone Home errors.

**What to verify per array:**

- **Status:** shows **Normal**, **Warning**, or **Critical**
- **Capacity:** used and free capacity values match the array UI
- **Performance:** IOPS and throughput graphs are populating
- **Health:** no critical alerts that were not already known

---

## Configure User Access

1. In the Pure1 portal, navigate to **Settings → Users**.
2. Click **Invite User**.
3. Enter the user's email address.
4. Assign the appropriate role:
   - **Administrator:** full access including billing and account management
   - **Array Admin:** can manage arrays and alerts but not account settings
   - **Viewer:** read-only access to all dashboards and data
5. Click **Send Invitation**.
6. The invited user receives an email to create or link their Pure Storage account.

**SAML SSO (if configured at the organisation level):**

1. Navigate to **Settings → Security → SSO**.
2. Click **Configure SSO** and enter the IdP metadata URL or upload the IdP metadata XML.
3. Map the IdP attribute for email to the Pure1 user identity field.
4. Test SSO login with a non-admin account before enabling for all users.

---

## Configure Alert Notifications

1. In the Pure1 portal, navigate to **Settings → Notifications**.
2. Click **Add Notification Rule**.
3. Configure the rule:
   - **Name:** descriptive label (e.g. `Critical Alerts - Storage Team`)
   - **Severity:** Critical, Warning, or both
   - **Arrays:** all arrays, or select specific arrays
   - **Channel:** Email (enter comma-separated addresses) or Webhook (enter endpoint URL)
4. Click **Save**.
5. Click **Send Test** to confirm the notification channel is working.

**Recommended notification rules:**

| Rule name | Severity | Channel |
|---|---|---|
| Critical storage alerts | Critical | On-call distribution list |
| Warning alerts | Warning | Storage team distribution list |
| Capacity forecast | Informational (capacity) | Capacity planning team |

**Webhook (PagerDuty / Slack example):**

- PagerDuty: use the PagerDuty Events API v2 URL as the webhook endpoint
- Slack: create an incoming webhook in Slack and paste the webhook URL into the notification rule

---

## Validate Telemetry

Run through the following checks to confirm the setup is complete and data is flowing correctly.

**Phone Home status:**

- FlashArray: `puresupport phonehome` shows `Enabled: True` and a recent **Last Phone Home** time
- FlashBlade: `purefb support` shows Phone Home enabled and a recent **Last Sent** time

**Pure1 portal:**

- All arrays appear under **Fleet → Arrays** with a valid health status
- Performance charts show data for at least the last hour
- Capacity values match the array management UI (within 1%)
- No arrays show **Data Collection Error** or **Disconnected** status

**Notifications:**

- At least one test notification has been sent and received for each notification rule
- Review **Pure1 → Alerts** to confirm active alerts are visible and match the array state

**Access:**

- Invite at least one non-admin user and confirm they can sign in and view the assigned arrays
- If SSO is configured, confirm SSO login completes successfully for a test user account

---

## See also

- [Pure1 — How It Works](../architecture/how-it-works/)
