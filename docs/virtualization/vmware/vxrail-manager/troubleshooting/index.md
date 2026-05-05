# VxRail Manager Health Troubleshooting

## Confirm VxRail Manager VM is Powered On

- In vCenter, locate the VxRail Manager VM
- Confirm it is powered on and VMware Tools is running
- Confirm the VM is not in a suspended or error state

## Confirm IP and DNS Resolution

```bash
ping <vxrail-manager-ip>
nslookup <vxrail-manager-fqdn>
```

## Confirm vCenter Registration

- Log into VxRail Manager and confirm it shows vCenter as connected
- If registration is lost, review the vCenter credentials and re-register

## Check VxRail Manager Services

- Log into VxRail Manager → **System** → **Health**
- Review all service states
- SSH to VxRail Manager and check service logs if accessible

## Review Recent Activity

- Check if an upgrade or patch was recently started
- Review VxRail Manager logs for the time the issue started
- Check vCenter tasks and events for related activity

## Check Certificate Trust

- Confirm VxRail Manager trusts the vCenter certificate
- If certificates were recently replaced, VxRail Manager may need re-registration

## Check Disk Space

- SSH to VxRail Manager and check disk usage: `df -h`
- Full log partitions can cause service failures

## Collecting VxRail Manager Logs

- Log into VxRail Manager → **Support** → **Log Bundle**
- Collect the bundle and save for Dell support

## Escalation

- If VxRail Manager cannot be recovered, open a Dell support case
- Provide the support bundle, vCenter events, and a description of what changed
