# SRM Troubleshooting

SRM issues commonly involve protection group state errors, recovery plan failures at specific steps, or SRA communication problems. Always collect the SRM support bundle from vCenter before engaging Broadcom support. Logs are located on the SRM server at `C:\ProgramData\VMware\VMware vCenter Site Recovery Manager\Logs\` (Windows) or via `vim-cmd vmsvc/get.summary` on vCenter.

| Symptom | Likely Cause | Diagnostic Steps |
|---|---|---|
| VM not in protection group / `Not Ready` | vSphere Replication sync error | Check vSphere Replication status for the VM; confirm replication appliance health |
| Recovery plan fails at network step | Network mapping incorrect or port group missing on recovery site | Verify network mappings in SRM UI; confirm port groups exist on recovery site ESXi hosts |
| SRA communication failure | Array credential mismatch or SRA service stopped | Check SRM UI → Array Managers; verify SRA service is running; re-enter array credentials |
| Test failover VMs not accessible | Bubble network misconfigured | Confirm test network port group is created and mapped; check VM IP customisation rules |
| Recovery plan stuck `Running` | Custom script step timeout | Check script log output in SRM task details; increase step timeout or fix script |
| Site Pair shows `Error` | Certificate mismatch or vCenter connectivity issue | Verify vCenter FQDN resolution from SRM server; check certificate trust between sites |
