# SnapCenter — Common Issues

> Part of the [SnapCenter Troubleshooting](../) reference.

---

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
