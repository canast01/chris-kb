# Commvault — Escalation

CommVault support is accessed via the CommVault Support Portal at support.commvault.com. Cases are raised by selecting the product component, severity, and providing initial diagnostic information. Before opening a case, collect the support bundle using the `qsystem log export` command on the CommServe — this packages CommServe, MediaAgent, and client logs into a single archive for upload. Metallic SaaS support escalation follows a separate path via the Metallic portal for cloud-managed deployments.

**Collecting the diagnostic bundle**

```bash
# On CommServe (run as administrator)
qsystem log export -path C:\cv_support_bundle

# Alternatively via Command Center:
# Settings > Support > Generate Support Bundle
```
