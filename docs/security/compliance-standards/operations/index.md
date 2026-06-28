---
tags:
  - operations
  - security
---
# Compliance Standards — Procedures

<div class="kb-summary">
Step-by-step procedures for assessing controls against CIS, ISO 27001, NIST, and PCI-DSS frameworks, collecting audit evidence, and managing control gaps to closure.
  <a class="kb-card" href="faq/"><strong>FAQ</strong><span>Frequently asked questions, common issues, and quick answers for day-to-day operations.</span></a>
</div>

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run CIS Benchmark Assessment

Evaluate infrastructure against the CIS Benchmark for the relevant OS or platform to produce a scored compliance baseline.

1. Download the CIS-CAT Pro Assessor tool and the appropriate benchmark profile (e.g., CIS Microsoft Windows Server 2022 Benchmark Level 1).
2. Run the assessor against the target host:
   ```bash
   ./Assessor-CLI.sh -b benchmarks/CIS_Microsoft_Windows_Server_2022_Benchmark_v2.0.0-xccdf.xml \
     -p "Level 1 - Member Server" --nts -rd /reports
   ```
3. Review the HTML report; note the overall score and any `FAIL` findings.
4. Export the findings CSV and import it into the GRC platform linked to the relevant control set.
5. Prioritise Level 1 failures for immediate remediation; log Level 2 failures as improvement items.
6. Schedule a re-assessment within 30 days of applying remediations to confirm the score improvement.

---

## Map Controls to Frameworks (ISO/NIST/PCI)

Cross-reference internal controls against multiple regulatory frameworks to identify coverage and gaps.

1. Open the control register in the GRC platform (ServiceNow GRC, Archer, or a spreadsheet).
2. For each internal control, apply framework tags using the mapping reference:
   - ISO 27001:2022 Annex A control number (e.g., A.8.2)
   - NIST SP 800-53 rev 5 control ID (e.g., AC-2)
   - PCI-DSS v4.0 requirement number (e.g., 8.2.1)
3. Identify controls where coverage is missing for one framework but present for another — these are framework-specific gaps.
4. For each gap, create a remediation task assigned to the control owner with a target closure date.
5. Generate a coverage heatmap (Compliant / Partial / Gap) per framework for the monthly compliance dashboard.
6. Review the mapping at least annually or when a new framework version is published.

---

## Collect Evidence for Audit

Gather and organise the artefacts required to demonstrate control effectiveness to internal or external auditors.

1. For each in-scope control, identify the required evidence type: screenshot, log export, policy document, configuration file, or signed record.
2. Collect automated evidence from tooling where available:
   ```powershell
   # Example: export Windows event logs for logon events
   Get-WinEvent -LogName Security -FilterXPath "*[System[EventID=4624]]" |
     Select-Object TimeCreated,Id,Message | Export-Csv C:\Audit\logon-events.csv
   ```
3. Label every artefact with: control ID, collection date, system name, and collector name.
4. Store artefacts in the GRC platform evidence repository or in `\\fileserver\Audit\<Framework>\<Year>\<ControlID>\`.
5. Obtain a manager attestation signature for any manually collected evidence.
6. Compile the final evidence package index listing all artefacts, their control mapping, and retention date.

---

## Track Control Exceptions

Manage situations where a control cannot be fully implemented and a formal exception must be recorded.

1. Raise an exception request in the GRC platform with: control ID, reason for exception, risk owner, compensating control, and requested exception period.
2. Assess the residual risk using the organisation's risk matrix (Likelihood × Impact).
3. Route the exception for approval: control owner → Security Manager → CISO (for High/Critical risk exceptions).
4. If approved, link the exception record to the control in the control register and set a review date no more than 12 months away.
5. Implement any agreed compensating controls and document them in the exception record.
6. Review all open exceptions quarterly; close or renew before the expiry date.

---

## Close a Control Gap

Remediate a control gap identified during assessment or audit and update the control register accordingly.

1. Open the gap record in the GRC platform and review the gap description, affected systems, and closure criteria.
2. Agree on a remediation plan with the control owner, including implementation steps and target date.
3. Implement the remediation (e.g., apply GPO, update firewall rule, deploy configuration via Ansible):
   ```bash
   ansible-playbook -i inventory/prod site.yml --tags cis-hardening --limit webservers
   ```
4. Collect post-remediation evidence demonstrating the control is now effective.
5. Submit the evidence to the assessor or auditor for validation.
6. Update the control status in the register to `Implemented` and attach the evidence reference; close the gap record.

---

## Prepare for External Audit

Organise the team and documentation ahead of a scheduled external audit engagement.

1. Confirm the audit scope, timeframe, and auditor contact with the audit firm at least 4 weeks in advance.
2. Assemble the audit readiness team: control owners, IT leads, and a compliance coordinator.
3. Run a pre-audit internal assessment: re-execute CIS assessments and review the evidence repository for completeness.
4. Prepare the following artefact bundles: policy documents, risk register, previous audit findings and closure evidence, and the current control register.
5. Schedule a kick-off call with the auditors; confirm the interview schedule and evidence request list.
6. Create a shared document portal (SharePoint, Confluence) where auditors can access artefacts without accessing production systems directly.
7. Brief all staff who will be interviewed on their area of responsibility and the audit process.

---

## Respond to Audit Findings

Process and remediate findings issued by internal or external auditors within the agreed response window.

1. Receive the audit finding report and log each finding in the GRC platform with: finding ID, severity (Critical/High/Medium/Low), control reference, and auditor description.
2. For each finding, assign a remediation owner and a target date aligned to the agreed SLA (Critical: 30 days, High: 60 days, Medium: 90 days).
3. Draft a formal management response for each finding, acknowledging the gap and stating the remediation action.
4. Implement the remediation and collect evidence of completion.
5. Submit the management response and evidence to the auditor for acceptance.
6. Track open findings in the GRC dashboard; escalate any finding approaching SLA breach to the CISO.

---

## Maintain Control Register

Keep the organisation's control register current to ensure it accurately reflects the implemented security posture.

1. Open the control register spreadsheet or GRC module and review the last-updated date for each control.
2. For controls older than 6 months, contact the control owner to confirm the implementation status is still accurate.
3. Add new controls arising from regulatory changes, new systems, or audit recommendations, including: control ID, description, framework mapping, owner, implementation status, and evidence link.
4. Archive retired controls with a closure date and reason; do not delete them, as they may be referenced in historical audits.
5. Publish the updated register to the internal compliance portal after each quarterly review.
6. Present the register summary (total controls, compliant %, gap count) to the Security steering committee quarterly.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Security — Overview](../)
