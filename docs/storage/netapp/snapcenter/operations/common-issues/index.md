# SnapCenter — Known Issues

> Part of the [SnapCenter Operations](../index.md) reference.

---

## Incident Triage

- [ ] Navigate to SnapCenter GUI → Monitor → Jobs — identify the failing job and review the error message in the job detail
- [ ] Check the application plugin on the target host: in Settings → Hosts, select the host and click Refresh to test connectivity
- [ ] If plugin unreachable: log onto the target host and verify the SnapCenter agent service is running (Windows: `SnapCenter Plug-in for Windows`; Linux: check `snapcenter_linux_host_plugin` process)
- [ ] Check ONTAP snapshot space on the source volume: `snapshot show -vserver <svm> -volume <vol>` — ensure the volume has space for new snapshots
- [ ] If a SnapVault update is failing: check the secondary relationship from the destination cluster: `snapmirror show -destination-path <svm:vol>` — look for `broken-off` or `lag-time` issues
- [ ] Review the SnapCenter log files on the server for detailed stack traces: `C:\Program Files\NetApp\SnapCenter\SMCore\logs\`
- [ ] If a restore or clone is failing: check igroup membership and LUN mapping on ONTAP — ensure the target igroup matches the host's WWN/IQN

| Question | Answer |
|---|---|
| Which resource group and job failed? | |
| What is the error message in the job detail? | |
| Is the plugin host reachable from SnapCenter? | |
| Is the ONTAP source volume out of snapshot space? | |
| Is the secondary SnapVault relationship healthy? | |

## Common Issues Reference

| Symptom | Likely Cause | Action |
|---|---|---|
| Plugin not connecting to host | SnapCenter Agent service stopped or firewall blocking TCP 8145 | Settings → Hosts → Refresh host; check agent service: `Get-Service SnapCenter*` (Windows) or `systemctl status spl` (Linux); verify firewall rules |
| Backup job failing with quiesce error | Application not responding to pre-backup script; VSS writer error (SQL/Exchange) | Check application logs on the host; test script manually; on Windows, check VSS writer state: `vssadmin list writers` |
| Clone operation failing with space error | Insufficient free space on destination aggregate; FlexClone license not present | Check aggregate capacity on ONTAP: `storage aggregate show`; verify FlexClone license: `system license show` |
| SnapVault update failing — source snapshot missing | Source snapshot deleted before XDP transfer completed; retention policy mismatch | On destination cluster: `snapmirror show -destination-path`; run `snapmirror resync` or re-initialize the XDP relationship |
| Restore job failing with LUN mapping error | LUN already mapped to another host; igroup mismatch during restore | Check igroup membership: `lun mapping show` on ONTAP; unmount LUN on conflicting host; remap to correct igroup |
| Resource group stuck in running state | Agent crash or hung pre/post script on target host | Kill job from Jobs → Monitor → Cancel; restart SnapCenter agent on host (`Restart-Service SnapCenter*` or `systemctl restart spl`); investigate script exit codes |
| SnapCenter Server unavailable (GUI 503 error) | IIS app pool crashed; SnapCenter web service stopped | On server: `iisreset`; check Windows services: `SnapCenter_WebApp`, `SchedulerSvc`; review IIS error logs |
| Backup succeeds but no snapshot visible on ONTAP | ONTAP storage connection uses wrong SVM credentials; snapshot naming mismatch | Re-verify ONTAP credentials in Settings → Storage Systems; check `snapshot show -volume <vol>` on ONTAP directly |
