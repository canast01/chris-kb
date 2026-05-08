# SRM Troubleshooting — Escalation

VMware SRM support cases are opened via the Broadcom Support Portal (support.broadcom.com) under the VMware vSphere product family. For production DR failures, open a Critical (Severity 1) case to engage 24×7 response. Collect the SRM support bundle before calling — it includes SRM server logs, vSphere Replication logs, and configuration exports.

**Required information for SR:**

| Item | How to Collect |
|---|---|
| SRM version | SRM UI → Summary tab or `SRM-support-bundle` |
| vCenter version | vCenter UI → About |
| SRA name and version | SRM UI → Array Managers |
| Protection group count and states | SRM UI → Protection Groups (screenshot or export) |
| SRM support bundle | vCenter UI → SRM plugin → Support Bundle → Generate |
| vSphere Replication logs | vSphere Replication appliance → Support → Download Log Bundle |

**Support process:**
- **Broadcom Support Portal**: support.broadcom.com → My Cases → Create Case.
- **Severity 1 (Critical)**: Production DR system down; 24×7 engineer engagement; 30-minute callback SLA.
- **Severity 2 (Major)**: DR degraded with workaround; business hours response.
- **Premier Support**: Designated support account manager; faster escalation path for P1.
