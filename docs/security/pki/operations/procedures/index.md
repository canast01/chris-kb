# PKI — Standard Procedures

<div class="kb-summary">
Standard operating procedures for managing the internal Certificate Authority: issuing, renewing, revoking, and backing up certificates, plus CA configuration tasks.
</div>

---

## Request and Issue a Certificate

Request a certificate from the internal CA using a Certificate Signing Request (CSR), then download the signed certificate for installation.

1. Generate a CSR and private key on the target server:
   ```cmd
   certreq -new request.inf request.csr
   ```
   where `request.inf` specifies Subject, KeyLength, and EnhancedKeyUsage.

2. Submit the CSR to the CA:
   ```cmd
   certreq -submit -attrib "CertificateTemplate:<TemplateName>" -config "<CA-Server>\<CA-Name>" request.csr response.cer
   ```

3. If the CA is configured for manager approval, approve the pending request in the Certificate Authority MMC under **Pending Requests**.

4. Once issued, retrieve the signed certificate:
   ```cmd
   certreq -retrieve <RequestID> response.cer
   ```

5. Accept and install the certificate:
   ```cmd
   certreq -accept response.cer
   ```

6. Verify the certificate appears in the local machine certificate store:
   ```powershell
   Get-ChildItem Cert:\LocalMachine\My | Where-Object Subject -like "*<CN>*"
   ```

---

## Issue a Certificate via Web Enrollment

Use the AD CS Web Enrollment interface for manual certificate issuance when `certreq` is not available or for user certificates.

1. Open a browser and navigate to `https://<ca-server>/certsrv`.

2. Click **Request a certificate** → **Advanced certificate request**.

3. Select **Create and submit a request to this CA** or **Submit a certificate request by using a base-64-encoded CMC or PKCS #10 file** if you already have a CSR.

4. Select the appropriate template from the **Certificate Template** drop-down.

5. Fill in the subject details (Common Name, organisation, SANs if applicable) and click **Submit**.

6. If auto-approved, click **Download certificate** and save the `.cer` file.

7. Import the certificate into the relevant store:
   ```cmd
   certutil -importcert <cert-file>.cer
   ```

---

## Renew an Expiring Certificate

Renew a certificate before expiry to avoid service interruption; most CAs allow renewal within 6 weeks of expiry.

1. Identify certificates expiring within 30 days:
   ```powershell
   Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.NotAfter -lt (Get-Date).AddDays(30) } | Select Subject, NotAfter
   ```

2. Generate a renewal request using the existing certificate's serial number:
   ```cmd
   certreq -enroll -machine -cert <Thumbprint> renew
   ```
   Or for a new CSR-based renewal, generate a fresh CSR with the same subject details (see **Request and Issue a Certificate**).

3. Submit the renewal request to the CA:
   ```cmd
   certreq -submit -attrib "CertificateTemplate:<TemplateName>" -config "<CA-Server>\<CA-Name>" renewal.csr renewed.cer
   ```

4. Accept the renewed certificate:
   ```cmd
   certreq -accept renewed.cer
   ```

5. Confirm the new expiry date:
   ```powershell
   Get-ChildItem Cert:\LocalMachine\My | Where-Object Subject -like "*<CN>*" | Select NotAfter
   ```

6. Update any service bindings (IIS, LDAPS, etc.) to reference the new certificate thumbprint.

---

## Revoke a Certificate

Revoke a certificate immediately when a private key is compromised, a system is decommissioned, or the certificate details are no longer valid.

1. Open the **Certificate Authority** MMC snap-in on the CA server (`certsrv.msc`).

2. Expand the CA node and click **Issued Certificates**.

3. Locate the certificate by serial number or subject name. Right-click → **All Tasks** → **Revoke Certificate**.

4. Select the appropriate reason code (e.g., Key Compromise, Affiliation Changed, Superseded, Cessation of Operation) and click **Yes**.

5. Alternatively, revoke via command line using the serial number:
   ```cmd
   certutil -revoke <SerialNumber> <ReasonCode>
   ```
   Reason codes: 0=Unspecified, 1=KeyCompromise, 3=Superseded, 5=CessationOfOperation.

6. Publish an updated CRL immediately after revocation (see **Publish the CRL**).

7. Verify the certificate appears in **Revoked Certificates** in the CA MMC.

---

## Publish the CRL (Certificate Revocation List)

Manually publish an updated CRL to distribution points after any revocation, or on a scheduled basis.

1. Open the **Certificate Authority** MMC snap-in (`certsrv.msc`).

2. Right-click the CA node → **All Tasks** → **Publish** → select **New CRL** → click **OK**.

3. Alternatively, publish from the command line:
   ```cmd
   certutil -crl
   ```

4. Verify the CRL was published to all configured distribution points (CDP):
   ```cmd
   certutil -getreg CA\CRLPublicationURLs
   ```

5. Confirm the CRL is accessible at each HTTP CDP URL:
   ```cmd
   certutil -verify -urlfetch <path-to-any-cert>.cer
   ```
   All CRL and OCSP checks should return `CRL signature verified` and `OCSP response verified`.

6. Check the new CRL's next-publish date does not exceed your CA policy window:
   ```cmd
   certutil -dump <path-to-crl>.crl
   ```

---

## Add a Certificate Template

Duplicate and publish a new certificate template to AD CS when a new certificate type is required (e.g., a new application, code signing, or LDAPS).

1. Open the **Certificate Templates** console (`certtmpl.msc`).

2. Right-click an existing template that is closest to the required use case → **Duplicate Template**.

3. Set the **Compatibility** tab to the minimum CA/recipient OS version in your environment.

4. On the **General** tab, set a unique **Template display name** and **Template name** (no spaces).

5. Configure the **Subject Name**, **Extensions** (EKU, Key Usage), **Security** (who can enrol), and **Request Handling** tabs as required.

6. Click **OK** to save the new template.

7. In the **Certificate Authority** MMC (`certsrv.msc`), right-click **Certificate Templates** → **New** → **Certificate Template to Issue**.

8. Select the new template and click **OK** — the template is now available for enrolment.

9. If auto-enrolment is needed, configure Group Policy (see **Configure Auto-Enrollment via Group Policy**).

---

## Configure Auto-Enrollment via Group Policy

Enable automatic certificate enrolment for domain computers or users so certificates are issued and renewed without manual intervention.

1. Open the **Group Policy Management Console** (`gpmc.msc`) and create or edit a GPO linked to the target OU.

2. Navigate to:
```text
   Computer Configuration → Windows Settings → Security Settings → Public Key Policies
   ```
   (For user certificates use the equivalent path under **User Configuration**.)

3. Double-click **Certificate Services Client – Auto-Enrollment**.

4. Set **Configuration Model** to **Enabled**.

5. Check both:
   - **Renew expired certificates, update pending certificates, and remove revoked certificates**
   - **Update certificates that use certificate templates**

6. Click **OK** and close the GPO editor.

7. Force a Group Policy update on a test machine to verify:
   ```cmd
   gpupdate /force
   ```

8. Check that the expected certificate has been issued:
   ```powershell
   Get-ChildItem Cert:\LocalMachine\My | Select Subject, NotAfter
   ```

---

## Backup the Certificate Authority

Back up the CA database, private key, and configuration to allow full restoration if the CA server fails.

1. On the CA server, open an elevated command prompt.

2. Back up the CA database and private key to a folder:
   ```cmd
   certutil -backup -p <BackupPassword> C:\CABackup
   ```
   This creates `DataBase\` (certificate database) and `p12` (CA key and certificate) under `C:\CABackup`.

3. Alternatively, use the CA MMC: right-click the CA → **All Tasks** → **Back up CA** → select both **Private key and CA certificate** and **Certificate database and certificate database log**.

4. Copy the backup folder to an off-server location (network share, backup system):
   ```powershell
   Copy-Item -Recurse C:\CABackup \\<backup-server>\CABackups\$(Get-Date -Format yyyyMMdd)
   ```

5. Export the CA registry configuration:
   ```cmd
   reg export HKLM\SYSTEM\CurrentControlSet\Services\CertSvc C:\CABackup\CertSvc.reg
   ```

6. Verify backup integrity by checking the `.p12` file opens with the backup password:
   ```cmd
   certutil -dump C:\CABackup\*.p12
   ```

7. Log the backup date and store the backup password securely in CyberArk or equivalent vault.

---

## Restore the Certificate Authority

Restore a CA from backup after server failure or migration to a new server.

1. Install the AD CS role on the replacement server without configuring it:
   ```powershell
   Install-WindowsFeature ADCS-Cert-Authority -IncludeManagementTools
   ```

2. Copy the backup folder from the off-server location to the new server (e.g., `C:\CARestore`).

3. Restore the CA private key and certificate:
   ```cmd
   certutil -restore -p <BackupPassword> C:\CARestore
   ```

4. Restore the CA registry configuration:
   ```cmd
   reg import C:\CARestore\CertSvc.reg
   ```

5. Configure the AD CS role using the existing CA name (must match exactly):
   ```powershell
   Install-AdcsCertificationAuthority -CAType EnterpriseSubordinateCA -CACommonName "<CA-Name>" -DatabaseDirectory "C:\Windows\System32\CertLog" -LogDirectory "C:\Windows\System32\CertLog" -Force
   ```

6. Start the CertSvc service:
   ```cmd
   net start certsvc
   ```

7. Verify the CA is operational and the database is intact:
   ```cmd
   certutil -getconfig
   certutil -ping
   ```

8. Publish an updated CRL immediately:
   ```cmd
   certutil -crl
   ```

9. Test certificate issuance by requesting a test certificate from the restored CA.

---

## Check CA Health and Expiry

Verify the CA certificate chain is valid, CRL distribution points are reachable, and the CA certificate is not approaching expiry.

1. Check the CA certificate expiry date:
   ```cmd
   certutil -store CA
   ```
   Look for `NotAfter` — plan renewal if expiry is within 6 months.

2. Verify a specific certificate including CRL and OCSP checks:
   ```cmd
   certutil -verify -urlfetch <cert-file>.cer
   ```
   All checks should return `verified`.

3. Confirm the CA service is running and accepting requests:
   ```cmd
   certutil -ping
   ```

4. Check the CA's own certificate chain validity:
   ```cmd
   certutil -verify -urlfetch C:\Windows\System32\CertSrv\CertEnroll\<CA-Name>.crt
   ```

5. List pending and recently-issued certificates to confirm normal issuance activity:
   ```cmd
   certutil -view -restrict "Disposition=20" -out "RequestId,CommonName,NotAfter"
   ```
   (Disposition 20 = Issued.)

6. Verify the current CRL is published and within its validity period:
   ```cmd
   certutil -getreg CA\CRLNextPublish
   ```

7. Check for CA-related event log warnings (Event IDs 6, 53, 70, 86):
   ```powershell
   Get-EventLog -LogName Application -Source "Microsoft-Windows-CertificationAuthority" -EntryType Warning,Error -Newest 20
   ```
