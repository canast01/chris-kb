# Nexus Dashboard Operations

Daily operational checks begin on the Nexus Dashboard health page to confirm all cluster nodes are green and all installed services are running. Review fabric health scores for all onboarded fabrics and sort active faults by severity to triage any P1 or P2 items. Check endpoint connectivity anomalies in NDI and review NDFC policy deployment status for any failed deployments. Weekly, review fabric utilisation metrics and capacity headroom across all fabrics.

**Daily Checklist**
- ND Admin > System Health — all nodes green, all services running
- Fabric health scores — flag any fabric below acceptable threshold
- Active faults — sort by severity, triage P1/P2 immediately
- NDI Endpoint Connectivity — review anomaly alerts
- NDFC — check policy deployment job status, resolve any failures

**Weekly Tasks**
- Review fabric utilisation and capacity metrics in NDI
- Check for new ND or NDFC software updates
- Review audit log for unexpected policy changes
