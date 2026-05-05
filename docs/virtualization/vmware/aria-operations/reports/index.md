# Aria Operations Reports

## Aria Operations Rightsizing Review

Use Aria Operations to identify VMs that are oversized or undersized.

### Oversized VMs

- High CPU and memory allocation with consistently low demand
- Review the CPU demand and memory demand charts over the last 30 days
- Use Aria Operations rightsizing recommendations as a starting point
- Validate with application owner before reducing resources

### Undersized VMs

- High CPU ready or memory ballooning under normal load
- Indicates the VM needs more CPU or memory
- Review trend data before increasing resources

### Resize Process

1. Identify the VM and its application owner
2. Review Aria Operations recommendations
3. Get change approval from the application owner
4. Schedule a maintenance window if a reboot is required
5. Resize the VM
6. Monitor CPU ready, memory, and application performance after resize
7. Document before and after metrics

### Monthly Review

- Run the rightsizing report monthly
- Review top 10 oversized VMs
- Review top 10 undersized VMs
- Track progress on recommendations from previous months
