# Superna Eyeglass CLI Reference

Eyeglass provides a REST API and a CLI (`igls`) accessible from the appliance shell for status checks, failover initiation, failback, synchronisation, and report generation. OneFS SyncIQ CLI commands are used in conjunction with Eyeglass operations to verify the underlying replication state.

**Eyeglass CLI (`igls`):**

```bash
# Check overall Eyeglass system status
igls adm status

# Initiate a DR failover for a configuration group
igls dr failover --config-group <group-name>

# Initiate failback after a failover
igls dr failback --config-group <group-name>

# Force a sync of share/quota/DNS configuration
igls sync

# Generate a DR readiness report
igls report --type readiness
```

**OneFS SyncIQ CLI:**

```bash
# List all SyncIQ policies
isi sync policies list

# View running SyncIQ jobs
isi sync jobs list

# View SyncIQ replication reports
isi sync reports list

# View details for a specific policy
isi sync policies view <policy-name>

# Manually start a SyncIQ policy job
isi sync jobs start <policy-name>
```
