# Aria Operations Operations

Daily operational checks ensure the Aria Operations platform is healthy and collecting data from all monitored endpoints. Review the Active Alerts dashboard each morning and verify cluster node health via Admin > Cluster Management. Confirm all adapters are in a Collecting state under Admin > Solutions, and check disk utilisation on analytics and data nodes to prevent collection gaps. Weekly, generate a capacity report for infrastructure review to surface trending issues before they become incidents.

**Daily Checklist**
- Review Active Alerts dashboard — triage any Critical or Immediate alerts
- Admin > Cluster Management — confirm all nodes are Online
- Admin > Solutions — all adapters show status Collecting
- Check disk space on analytics and data nodes (alert threshold: 80%)

**Weekly Tasks**
- Generate Capacity Overview report for infrastructure review meeting
- Review top-N VMs by CPU/memory contention and escalate if needed
- Validate Remote Collector connectivity for distributed sites
