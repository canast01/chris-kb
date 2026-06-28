---
tags:
  - operations
  - security
---
# Multi-Factor Authentication — Procedures

<div class="kb-summary">
Step-by-step procedures for enrolling users in MFA, resetting credentials, configuring MFA across vCenter and Azure AD, and reviewing MFA adoption.
  <a class="kb-card" href="faq/"><strong>FAQ</strong><span>Frequently asked questions, common issues, and quick answers for day-to-day operations.</span></a>
</div>

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Enrol a User in MFA

Register a new user's authenticator device so they can complete MFA challenges at login.

1. Instruct the user to download and open the Microsoft Authenticator (or Okta Verify) app on their mobile device.
2. In Azure Entra ID admin centre, navigate to **Users > All Users**, open the user's profile, and select **Authentication methods**.
3. Click **Add authentication method**, choose **Microsoft Authenticator**, and select **Send notification**.
4. The user scans the QR code displayed on screen with the Authenticator app and approves the test notification.
5. Confirm the device appears as a registered method under the user's authentication methods with status **Active**.
6. Advise the user to also register a backup method (e.g., phone number for SMS) in case they lose access to the primary device.

---

## Reset MFA for a User (Helpdesk)

Re-register MFA for a user who has lost their device or been locked out of their authenticator.

1. Verify the user's identity through an approved out-of-band channel (video call, in-person with ID, or manager confirmation) before making any changes.
2. In Azure Entra ID admin centre, go to **Users > All Users**, open the user's profile, and select **Authentication methods**.
3. Delete all existing authentication methods by selecting each entry and clicking **Delete**.
4. Click **Require re-register multifactor authentication** — the user will be prompted to set up MFA at their next login.
5. Notify the user via their primary email (or phone if email is inaccessible) that their MFA has been reset and they must re-enrol at next login.
6. Log the reset action in the helpdesk ticketing system including the identity verification method used and the approving manager.

---

## Configure MFA for vCenter SSO (RADIUS)

Integrate a RADIUS-based MFA solution (e.g., Cisco Duo, RSA) with vCenter Single Sign-On.

1. Deploy and configure the RADIUS proxy on a dedicated server in the management network; obtain the RADIUS server IP and shared secret.
2. Log in to vCenter as `administrator@vsphere.local` and navigate to **Administration > Single Sign On > Configuration > Smart Card Authentication**.
3. Select **RADIUS** as the authentication mechanism and enter:
   - **RADIUS server IP/hostname**: `radius.corp.local`
   - **Port**: `1812`
   - **Shared secret**: (from vault)
   - **Timeout**: `30` seconds
4. Apply the configuration and log out; test login with an AD account — after entering the AD password you should receive a push notification or OTP prompt.
5. Configure a bypass group in the RADIUS proxy for service accounts that must not receive MFA prompts.
6. Document the RADIUS server details and shared secret rotation schedule in the integration runbook.

---

## Configure Conditional Access MFA (Azure AD)

Create an Azure Entra ID Conditional Access policy to enforce MFA for specific user groups or applications.

1. In Azure Entra ID admin centre, navigate to **Security > Conditional Access > Policies** and click **New policy**.
2. Name the policy clearly, e.g., `Require MFA for All Users - Exclude Break-Glass`.
3. Under **Assignments**:
   - **Users**: select the target group (e.g., `All Users`) and exclude the break-glass account.
   - **Target resources**: select `All cloud apps` or specific apps (e.g., vSphere, Aria Suite).
   - **Conditions**: optionally restrict by location (exclude trusted corporate IP ranges) or device platform.
4. Under **Access controls > Grant**: select `Grant access` and check `Require multifactor authentication`.
5. Set the policy to **Report-only** mode first; review the sign-in logs for 7 days to confirm no unexpected impact.
6. Switch the policy to **On** mode and monitor the sign-in logs for MFA failures in the first 48 hours.
7. Document the policy configuration, exclusions, and business justification in the access policy register.

---

## Exclude a Service Account from MFA

Apply a formal exemption for a service account that cannot support interactive MFA challenges.

1. Identify the service account and confirm it is non-interactive (used only by scripts or applications, never by humans).
2. Create or update an exclusion group in Entra ID (e.g., `CA-Exclusions-ServiceAccounts`) and add the service account.
3. Edit the relevant Conditional Access policy and add the exclusion group under **Assignments > Users > Exclude**.
4. As a compensating control, restrict the service account to sign in only from specific trusted IP addresses or named locations under **Conditions > Locations**.
5. Raise a formal risk acceptance record documenting the exemption reason, compensating control, and approving risk owner.
6. Review the exclusion at least annually to confirm the account is still non-interactive and the compensating control is still effective.

---

## Test MFA Authentication Flow

Validate the end-to-end MFA experience for a given application after configuration changes.

1. Use a non-privileged test account enrolled in MFA for all testing.
2. Open a private/incognito browser window and navigate to the application login page.
3. Enter the test account credentials (username and password) and confirm the MFA challenge is presented (push notification, OTP, or RADIUS passcode prompt).
4. Approve the MFA challenge and confirm successful login and correct role assignment within the application.
5. Test the failure path: deny the MFA push and confirm the login is blocked with an appropriate error message.
6. Test the bypass/exclusion path if applicable: log in with a service account from the excluded IP range and confirm MFA is not prompted.
7. Record the test results (pass/fail for each scenario) in the change ticket or test log.

---

## Review MFA Adoption Report

Monitor the percentage of users enrolled in MFA and identify accounts still lacking a second factor.

1. In Azure Entra ID admin centre, navigate to **Identity > Overview > Authentication methods > User registration details**.
2. Export the report: **Download** > CSV — the file includes columns for MFA capable, MFA registered, and method types.
3. Calculate the adoption rate: `(MFA Registered / Total Users) * 100`.
4. Filter for users where `MFA Registered = No` and `Account Enabled = Yes` — these are the gap accounts.
5. Group gap accounts by department and send targeted communications to the department heads with a 30-day enrolment deadline.
6. For accounts still not enrolled after the deadline, enforce MFA registration at next login via a Conditional Access policy set to `Block access` until MFA is registered.
7. Present the adoption trend (month-over-month) to the Security steering committee at the monthly review.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Security — Overview](../)
