# Aria Operations Capacity Planning

## Cluster CPU and Memory

- Review CPU demand vs capacity per cluster
- Identify clusters approaching the threshold where HA failover capacity would be impacted
- Track CPU ready — high CPU ready indicates overcommitment

## Datastore and vSAN Capacity

- Review datastore usage — alert when free space drops below 20%
- For vSAN, track usable capacity and thin-provisioned risk
- Review snapshot growth contribution to capacity

## VM Growth Trends

- Use Aria Operations capacity reports to forecast VM count growth
- Review which clusters are projected to run out of capacity soonest

## Rightsizing

- Review oversized VMs — high CPU and memory allocation with consistently low usage
- Review undersized VMs — high CPU ready or memory ballooning under normal load
- Use Aria Operations rightsizing recommendations as a starting point — validate before making changes

## Monthly Review Process

1. Run the capacity dashboard in Aria Operations
2. Review cluster headroom report
3. Review datastore free space report
4. Review top growth VMs
5. Review rightsizing recommendations
6. Identify clusters or datastores needing action
7. Document findings and recommendations in the monthly capacity review
