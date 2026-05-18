# Virtual Machines

> Part of the Azure CLI Reference.

```
┌──────────────────────────────────────────────────────────┐
│                    VM CLI Flow                           │
│                                                          │
│  az vm create ─────────────────────► Azure VM           │
│                                           │             │
│         ┌─────────────────────────────────┘             │
│         │          Lifecycle commands                   │
│         ▼                                               │
│  ┌─────────────┐  az vm start      ┌─────────────────┐  │
│  │  Stopped /  │──────────────────►│    Running      │  │
│  │ Deallocated │◄──────────────────│                 │  │
│  └─────────────┘  az vm stop       └────────┬────────┘  │
│                   az vm deallocate           │           │
│                                     az vm resize         │
│                                     az vm run-command    │
│                                             │           │
│                                             ▼           │
│                                    resized / cmd output │
└──────────────────────────────────────────────────────────┘
```

---

```bash
# List
az vm list --output table
az vm list --resource-group <rg> --output table
az vm list --resource-group <rg> --show-details --output table

# Start / stop / restart
az vm start --resource-group <rg> --name <vm>
az vm stop --resource-group <rg> --name <vm>
az vm deallocate --resource-group <rg> --name <vm>
az vm restart --resource-group <rg> --name <vm>

# Details
az vm show --resource-group <rg> --name <vm>
az vm get-instance-view --resource-group <rg> --name <vm>

# Create
az vm create --resource-group <rg> --name <vm> --image Ubuntu2204 --size Standard_D2s_v3 \
  --admin-username azureuser --ssh-key-values ~/.ssh/id_rsa.pub

# Resize
az vm resize --resource-group <rg> --name <vm> --size Standard_D4s_v3

# Run command
az vm run-command invoke --resource-group <rg> --name <vm> --command-id RunShellScript \
  --scripts "uptime"

# Open port
az vm open-port --resource-group <rg> --name <vm> --port 22
```
