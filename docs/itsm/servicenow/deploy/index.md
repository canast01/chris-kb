---
tags:
  - deployment
  - servicenow
---
# ServiceNow — Initial Instance Setup

<div class="kb-summary">
Step-by-step guide to requesting a ServiceNow developer instance, configuring admin settings, connecting LDAP, importing users, configuring email and MID Server, and validating the instance.

*Applies to: ServiceNow (Washington / Xanadu)*
</div>

```text
┌───────────────────────────────────────── ServiceNow — Deploy ─────────────────────────────────────────┐
│                                                                                                       │
│   Delivery: SaaS — no on-premises app tier; instances provisioned by ServiceNow                       │
│   Instance URL: https://<instance-name>.service-now.com                                               │
│   PDI (developer): free from developer.servicenow.com; provisioned in 10-30 min                       │
│   Enterprise: ordered via ServiceNow account team; delivered through hi.service-now.com               │
│                                                                                                       │
│   Initial configuration sequence                                                                      │
│   1. First login → change admin password immediately; store in team password manager                  │
│   2. System Properties: set instance name, timezone, SMTP server, company logo                        │
│   3. Enable MFA for admin and security_admin roles (System Properties → MFA)                          │
│   4. LDAP: System LDAP → Servers → New; configure LDAPS (port 636); test connection                   │
│   5. Import users + groups: LDAP Listeners → Load All Records; schedule sync (every 4h)               │
│   6. Configure SMTP (port 587 STARTTLS or 25); test email delivery                                    │
│   7. Activate plugins: ITSM, CMDB, Discovery, Service Portal, Flow Designer, Integrations Hub         │
│   8. Deploy MID Server for on-premises network reach (LDAP, Discovery, JDBC)                          │
│                                                                                                       │
│   MID Server                                                                                          │
│   Agent runs on Windows or Linux VM with outbound HTTPS to the ServiceNow instance                    │
│   Config: config.xml — instance URL, mid.server.svc credentials, server name                          │
│   Validate: MID Server → Servers → click record → Validate; status changes to Up                      │
│                                                                                                       │
│   Validation checks                                                                                   │
│   Admin + LDAP user login; LDAP users visible under User Administration → Users                       │
│   Create incident → assign → resolve → confirm email notification sent                                │
│   MID Server status = Up; no critical errors in MID Server logs (last 30 min)                         │
│                                                                                                       │
│   Key terms:                                                                                          │
│   PDI          = Personal Developer Instance; free sandbox at developer.servicenow.com                │
│   MID Server   = Management, Instrumentation, Discovery agent; runs on-prem, proxies to cloud         │
│   config.xml   = MID Server configuration file; contains instance URL and service account creds       │
│   LDAP Listener= ServiceNow component that maps AD attributes to ServiceNow user fields               │
│   Flow Designer= no-code/low-code workflow automation tool within ServiceNow                          │
│   hi.service-now.com = ServiceNow Customer Success Portal for enterprise instance management          │
│   Import Set   = staging table used during LDAP or CSV data import into ServiceNow                    │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Request Development Instance

ServiceNow is delivered as a SaaS product. Instances are provisioned by ServiceNow and accessed via a browser — there is no software to install on-premises for the application tier.

**Development/personal developer instance (PDI):**

1. Navigate to `https://developer.servicenow.com` and sign in or create a free account.
2. Click **Request Instance** and select the desired ServiceNow release (e.g. Xanadu, Yokohama).
3. The instance is provisioned within 10–30 minutes.
4. You receive an email with the instance URL (`https://<instance-name>.service-now.com`) and initial admin credentials.

**Enterprise production/sub-production instance:**

1. Work with your ServiceNow account team to order the required subscription.
2. ServiceNow provisions the instance and delivers access credentials via the ServiceNow Customer Success Portal (`https://hi.service-now.com`).
3. Note the instance URL, admin username, and initial password from the provisioning email.

**First login:**

1. Open a browser to `https://<instance-name>.service-now.com`.
2. Log in with the provided admin credentials.
3. You are prompted to change the admin password immediately — set a strong password and store it in the team password manager.

---

## Configure Admin Account

1. After first login, navigate to **System Properties → Basic Configuration** (or use the filter navigator: type `sys_properties.list`).
2. Set the following system properties:

| Property | Value | Notes |
|---|---|---|
| `glide.instance.name` | your instance name | Displayed in the browser tab and emails |
| `glide.email.smtp.server` | SMTP server FQDN | Required for outbound email |
| `glide.timezone` | e.g. `Europe/London` | Set to the primary user timezone |

3. Navigate to **System Properties → UI16** and set the company name and logo.
4. Navigate to **User Administration → Users** and open the `admin` user record:
   - Set **Email** to an active mailbox (admin notifications are sent here)
   - Set **Time zone** to the correct timezone
   - Set **First name** and **Last name** appropriately

**Enable multi-factor authentication for admin:**

1. Navigate to **System Properties → Multi-Factor Authentication**.
2. Enable MFA and set the required roles (at minimum, require MFA for `admin` and `security_admin` roles).

---

## Connect LDAP/Active Directory

1. Navigate to **System LDAP → LDAP Servers**.
2. Click **New** to create a new LDAP server configuration.
3. Configure the server:
   - **Name:** descriptive name (e.g. `AD - company.local`)
   - **Server URL:** `ldaps://dc01.company.local:636` (LDAPS recommended) or `ldap://dc01.company.local:389`
   - **Bind DN:** service account DN (e.g. `CN=svc-snow,OU=ServiceAccounts,DC=company,DC=local`)
   - **Bind password:** service account password
4. Click **Test Connection** — must return **Connection Successful** before proceeding.
5. Under **LDAP Listener → OU**, set the base DN for user search (e.g. `OU=Users,DC=company,DC=local`).
6. Configure the **Target field** mappings to map AD attributes to ServiceNow user fields:

| ServiceNow field | LDAP attribute |
|---|---|
| `user_name` | `sAMAccountName` |
| `first_name` | `givenName` |
| `last_name` | `sn` |
| `email` | `mail` |
| `phone` | `telephoneNumber` |
| `department` | `department` |
| `manager` | `manager` |

7. Click **Save**.

---

## Import Users and Groups

**Create an LDAP Import Set:**

1. Navigate to **System LDAP → LDAP Listeners**.
2. Open the listener for the LDAP server configured above.
3. Click **Load All Records** to trigger a full import of all users matching the configured OU.
4. Navigate to **System Import Sets → Import Sets** and monitor the import progress.
5. Once the import completes, verify: **User Administration → Users** — AD users should appear in the user list.

**Import groups:**

1. Add a second listener (or extend the existing one) to import from the groups OU.
2. Set the **Target table** to `sys_user_group`.
3. Map LDAP attributes:
   - `cn` → `name`
   - `member` → group member (handled by ServiceNow transform map — use the built-in LDAP group transform)
4. Run the group import and confirm groups appear under **User Administration → Groups**.

**Schedule recurring LDAP sync:**

1. Navigate to **System LDAP → LDAP Listeners** and open the listener.
2. Under **Scheduled Import**, set a sync frequency (recommended: every 4 hours).
3. Click **Save**.

---

## Configure Email (SMTP)

**Outbound email (SMTP):**

1. Navigate to **System Properties → Email**.
2. Set the following properties:
   - `glide.email.smtp.server` — SMTP server FQDN (e.g. `smtp.company.local`)
   - `glide.email.smtp.port` — `25` (unauthenticated) or `587` (STARTTLS)
   - `glide.email.smtp.user` — SMTP auth username (if required)
   - `glide.email.smtp.password` — SMTP auth password (if required)
   - `glide.email.from.name` — display name for outbound emails (e.g. `ServiceNow`)
   - `glide.email.reply_to` — reply-to address (e.g. `snow-noreply@company.local`)
3. Click **Send test email** and confirm delivery to the admin mailbox.

**Inbound email (IMAP/POP3 for email-to-ticket):**

1. Navigate to **System Mailboxes → Inbound**.
2. Click **New** and configure:
   - **Server:** IMAP server FQDN
   - **Port:** 993 (IMAPS) or 143
   - **Mailbox:** the shared mailbox address (e.g. `helpdesk@company.local`)
   - **Type:** IMAP (recommended)
3. Click **Test** to confirm connection and authentication.
4. Set the **Target table** to `incident` or the appropriate table for inbound emails to create records.

---

## Install Required Plugins

Plugins extend ServiceNow functionality. Most production instances require the following.

1. Navigate to **System Applications → All Available Applications → All**.
2. Search for and activate the following (activation requires admin privileges and may take 10–30 minutes per plugin):

| Plugin | Purpose |
|---|---|
| **ITSM (IT Service Management)** | Incident, Problem, Change, Service Catalog — core ITSM |
| **CMDB** | Configuration Management Database — CI tracking |
| **Discovery** | Automated infrastructure discovery to populate the CMDB |
| **Service Portal** | Modern end-user self-service portal |
| **Flow Designer** | No-code/low-code workflow automation |
| **Integrations Hub** | Pre-built integration spokes (Slack, Teams, Jira, etc.) |

3. After activation, navigate to **System Applications → Applications** and confirm each plugin shows **Active**.

---

## Configure MID Server

The MID (Management, Instrumentation, and Discovery) Server is a Windows or Linux agent that runs on-premises, enabling ServiceNow to reach internal network resources (for Discovery, LDAP, JDBC, etc.).

**Install the MID Server:**

1. Navigate to **MID Server → Downloads** in the ServiceNow instance.
2. Download the installer for the target OS (Windows .exe or Linux .zip).
3. On the MID Server host (a VM with outbound HTTPS access to the instance):

**Linux:**

```bash
# Extract the MID Server package
unzip agent.zip -d /opt/servicenow/mid

# Edit the config file
vi /opt/servicenow/mid/agent/config.xml
```

Edit `config.xml` with the instance details:

```xml
<parameter name="url" value="https://<instance-name>.service-now.com"/>
<parameter name="mid.instance.username" value="mid.server.svc"/>
<parameter name="mid.instance.password" value="<service-account-password>"/>
<parameter name="name" value="mid-server-prod-01"/>
```

```bash
# Start the MID Server
sudo /opt/servicenow/mid/agent/bin/mid.sh start

# Check status
sudo /opt/servicenow/mid/agent/bin/mid.sh status
```

4. In the ServiceNow instance, navigate to **MID Server → Servers**.
5. The new MID Server appears with status **Validating**.
6. Click the MID Server record and click **Validate** to approve it.
7. After validation, the MID Server status changes to **Up**.

**Assign MID Server to applications:**

1. Navigate to **MID Server → Applications** and assign the MID Server to Discovery, LDAP, and any other applications that require on-premises access.

---

## Validate Instance

Run through the following checks before handing the instance to users.

**Authentication:**

- Log in as admin — dashboard loads successfully
- Log in as an LDAP-imported user — login succeeds with the correct name and email shown
- Confirm MFA prompts for admin login if MFA was enabled

**Email:**

- Send a test email from **System Properties → Email → Send test email**
- Create a test incident and confirm the assigned user receives an email notification
- If inbound email is configured, send an email to the mailbox and confirm a ticket is created

**LDAP:**

- Navigate to **User Administration → Users** — LDAP-imported users are present
- Navigate to **User Administration → Groups** — LDAP-imported groups are present and membership is correct

**MID Server:**

- Navigate to **MID Server → Servers** — all MID Servers show **Up**
- Navigate to **MID Server → MID Server Logs** — no critical errors in the last 30 minutes

**Incident workflow:**

1. Create a new incident: **Incident → Create New**
2. Assign it to a user and a group
3. Resolve the incident and confirm the state changes to **Resolved**
4. Confirm the requester receives an email notification at each state change

**Plugins:**

- Navigate to **System Applications → Applications** — all activated plugins show **Active**, none show **Error**

---

## Verify

- Confirm the service or component is running and reachable
- Check management UI for any errors or warnings
- Run a basic functional test (login, read, write) to confirm end-to-end operation
