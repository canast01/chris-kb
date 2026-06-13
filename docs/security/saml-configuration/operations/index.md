---
tags:
  - operations
  - security
---
# SAML Configuration — Procedures

<div class="kb-summary">
Step-by-step procedures for configuring SAML SSO with Azure Entra ID and Okta, managing attribute mappings, rotating signing certificates, and troubleshooting assertion failures.
</div>

```text
┌─────────────────────────────────── SAML Configuration — Operations ───────────────────────────────────┐
│                                                                                                       │
│   IdP options: Azure Entra ID (Enterprise Applications) or Okta (SAML 2.0 app integration)            │
│   Key URLs: Entity ID (Identifier), ACS URL (Reply URL), Sign-on URL; must match exactly SP-side      │
│   Signing cert: rotate before expiry; dual-cert trust allows zero-downtime cut-over                   │
│   Testing: always validate with SAML-tracer (browser extension) before marking complete               │
│                                                                                                       │
│   Azure Entra ID configuration                                                                        │
│   App: Enterprise Applications > New > Create your own; select non-gallery app                        │
│   SAML config: Identifier = SP Entity ID; Reply URL = ACS endpoint; Sign-on URL = app login           │
│   Metadata: download Federation Metadata XML; import into SP SAML IdP configuration screen            │
│   Assign: Users and groups → assign AD group to the Entra ID application                              │
│                                                                                                       │
│   Okta configuration                                                                                  │
│   Create: Applications > Create App Integration > SAML 2.0                                            │
│   Config: SSO URL = ACS URL; Audience URI = Entity ID; Name ID format = EmailAddress                  │
│   Attributes: add firstName, lastName, groups in Attribute Statements section                         │
│   Export: View Setup Instructions → download IdP metadata XML or note SSO URL + cert                  │
│                                                                                                       │
│   Attribute mappings and signing certificate                                                          │
│   Azure: Attributes & Claims > Add new claim; source = user.assignedroles or directory extension      │
│   Okta: Sign On > Edit > Attribute Statements; value = Okta expression (user.roles)                   │
│   Cert rotation: generate new cert in IdP; import to SP as secondary; make active; verify; remove old │
│                                                                                                       │
│   Key terms:                                                                                          │
│   SAML          = Security Assertion Markup Language; XML-based SSO federation protocol               │
│   ACS URL       = Assertion Consumer Service URL; SP endpoint that receives SAMLResponse              │
│   Entity ID     = unique identifier for the SP in SAML metadata; must match IdP configuration         │
│   SAMLResponse  = Base64-encoded XML assertion; contains NameID, attributes, and signature            │
│   NameID        = user identifier in the assertion; format must match SP expectation (email / UPN)    │
│   clock skew    = time diff between IdP and SP; >5 min causes SAML assertion validation failure       │
│   SAML-tracer   = browser extension for capturing and decoding SAML requests and responses            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Configure SAML SSO with Azure Entra ID

Register an application in Azure Entra ID and configure it as a SAML identity provider.

1. In Azure Entra ID admin centre, navigate to **Enterprise applications > New application > Create your own application**. Name the app (e.g., `vSphere-SAML`) and select **Integrate any other application you don't find in the gallery**.
2. Go to **Single sign-on > SAML** and click **Edit** on **Basic SAML Configuration**:
   - **Identifier (Entity ID)**: `https://vcenter.corp.local/websso/SAML2/Metadata/vsphere.local`
   - **Reply URL (ACS URL)**: `https://vcenter.corp.local/websso/SAML2/SSO/vsphere.local`
   - **Sign on URL**: `https://vcenter.corp.local/ui`
3. Under **Attributes & Claims**, configure the required claim mappings (see "Add a New SAML Attribute Mapping").
4. Download the **Federation Metadata XML** from the **SAML Signing Certificate** section.
5. Import the metadata XML into the service provider (vCenter, Aria, or other app) via its SAML IdP configuration screen.
6. Assign the Entra ID application to the relevant user groups under **Users and groups**.
7. Test SSO by clicking **Test** in the Azure portal — confirm the sign-in flow completes and the correct attributes are passed.

---

## Configure SAML SSO with Okta

Set up an Okta application integration to provide SAML 2.0 SSO for an enterprise platform.

1. In Okta Admin, navigate to **Applications > Applications > Create App Integration** and select **SAML 2.0**.
2. Name the app and click **Next**. On the **Configure SAML** tab, enter:
   - **Single sign-on URL**: `https://app.corp.local/saml/acs`
   - **Audience URI (SP Entity ID)**: `https://app.corp.local/saml/metadata`
   - **Name ID format**: `EmailAddress`
   - **Application username**: `Email`
3. Add attribute statements as required (e.g., `firstName`, `lastName`, `groups`).
4. Click **Next > Finish**. On the **Sign On** tab, click **View Setup Instructions** and download the IdP metadata XML or note the SSO URL and certificate.
5. Import the Okta IdP metadata into the service provider's SAML configuration.
6. Under **Assignments**, assign the application to the relevant Okta groups.
7. Open a private browser window, navigate to the app URL, and confirm the SAML redirect to Okta and back completes successfully.

---

## Add a New SAML Attribute Mapping

Add or update attribute statements passed in the SAML assertion to support application role assignment.

1. Identify the attribute name and format required by the service provider (check the SP's documentation or SAML trace).
2. In Azure Entra ID, navigate to the enterprise application > **Single sign-on > Attributes & Claims > Edit**.
3. Click **Add new claim** and enter:
   - **Name**: e.g., `role`
   - **Source**: `Attribute`
   - **Source attribute**: e.g., `user.assignedroles` or a directory extension attribute
4. Click **Save**.
5. In Okta, navigate to the app > **Sign On > Edit > Attribute Statements** and add:
   - **Name**: `role`
   - **Value**: `user.roles` (or appropriate Okta expression)
6. Test the updated assertion using a browser SAML tracer extension (e.g., SAML-tracer for Chrome/Firefox) to confirm the attribute appears with the expected value.
7. Verify the service provider recognises the new attribute and grants the expected role.

---

## Rotate SAML Signing Certificate

Replace the SAML signing certificate before expiry to avoid SSO outages.

1. Check the current certificate expiry date in Azure Entra ID: **Enterprise application > Single sign-on > SAML Signing Certificate > Expiration date**.
2. In the Azure portal, click **New Certificate** — this generates a new certificate without yet activating it.
3. Download the new certificate (Base64 format) and import it into the service provider as a secondary/pending IdP certificate. (Most SPs support dual-certificate trust to allow a seamless cut-over.)
4. In the Azure portal, click the three-dot menu on the new certificate and select **Make active** — from this point all assertions will be signed with the new certificate.
5. Test SSO immediately after activation: log in via the SP and confirm the assertion validates without error.
6. Remove the old certificate from the SP's trust store once SSO is confirmed working with the new certificate.
7. Update the certificate expiry date in the asset register and set a reminder 60 days before the new certificate expires.

---

## Test SAML Authentication Flow

Validate the full SAML authentication flow for an application after any configuration change.

1. Install the SAML-tracer browser extension (Firefox or Chrome) and open it in the browser developer panel.
2. Open a private browser window, navigate to the SP-initiated SSO URL (e.g., `https://app.corp.local/saml/login`), and log in with a test account.
3. In SAML-tracer, capture the SAML request (SAMLRequest) sent to the IdP and the SAML response (SAMLResponse) returned to the ACS URL.
4. Decode the SAMLResponse (Base64 → XML) and verify:
   - `<Issuer>` matches the IdP entity ID
   - `<NameID>` contains the expected user identifier
   - All required attributes are present with correct values
   - `NotBefore` and `NotOnOrAfter` timestamps are within the valid window
5. Confirm the SP accepts the assertion and the user lands on the correct page with the expected role.
6. Test the IdP-initiated flow if supported: log in to the IdP portal and launch the app from the app tile.
7. Record the test results in the change ticket.

---

## Troubleshoot SAML Assertion Failures

Diagnose and resolve errors in the SAML authentication flow reported by users or applications.

1. Ask the affected user for the exact error message displayed by the application (e.g., "SAML assertion signature invalid", "Unknown user", "Attribute mapping failure").
2. Capture a SAML trace from a failing session using the SAML-tracer extension and decode the SAMLResponse.
3. Common failure causes and resolutions:
   - **Signature invalid**: The SP is using a cached copy of the old signing certificate — re-import the current IdP certificate into the SP.
   - **Unknown NameID / user not found**: The NameID format does not match what the SP expects — align the format (email vs. UPN vs. persistent identifier) between IdP and SP.
   - **Clock skew**: The SP's system clock differs from the IdP by more than the allowed tolerance — synchronise NTP on the SP server: `w32tm /resync /force`.
   - **Attribute missing**: A required attribute is not included in the assertion — add the attribute mapping in the IdP (see "Add a New SAML Attribute Mapping").
4. After applying the fix, re-run the authentication test and confirm success.
5. Document the root cause and resolution in the incident record.

---

## Disable SAML for a Specific Application

Revert an application from SAML SSO to local authentication as part of decommissioning or emergency access recovery.

1. Log in to the application using a local administrator account (bypass SSO — typically a break-glass account or direct URL such as `https://app.corp.local/local-login`).
2. In the application's authentication settings, disable or remove the SAML IdP configuration.
3. Re-enable local authentication or an alternative identity source (LDAP) as the fallback.
4. In Azure Entra ID or Okta, navigate to the application and disable SSO: set the SSO mode to `Disabled` or delete the application integration if the app is being decommissioned.
5. Unassign users and groups from the IdP application to prevent orphaned assignments.
6. Notify affected users of the authentication method change and provide new login instructions.
7. Update the SSO application register and remove the entry from the SAML configuration documentation.
