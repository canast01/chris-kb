# Data Domain — Common Issues

## Incident Triage

When backup jobs fail, replication falls behind, or DDBoost clients disconnect, work through this sequence first.

- [ ] Run `alerts show current` — identify any active hardware or software alerts that correspond to the start of the incident
- [ ] Run `filesys show space` — a filesystem at capacity (post-compression usage approaching 100%) will cause backup writes to fail; this is the most common cause of sudden backup failures
- [ ] Run `replication show` — check whether any replication context has entered `Error` state or is accumulating lag; replication errors can signal network issues or a full filesystem on the destination
- [ ] Run `ddboost show clients` — identify which DDBoost-connected backup servers are disconnected or reporting authentication errors
- [ ] Check `filesys status` — if the filesystem is not `Running`, backup writes will fail regardless of capacity
- [ ] Check disk health: `disk show state` — a faulted or absent disk reduces usable capacity and triggers alerts; do not replace a disk without a Dell support case
- [ ] Review backup application logs for the specific error code reported by the backup job — DDBoost error codes map to specific DD conditions
- [ ] If replication lag is growing: run `replication status` to confirm available bandwidth; check WAN utilisation and consider a temporary `replication throttle` adjustment

| Question | Answer |
|---|---|
| What is the current post-compression usage percentage? | |
| Which replication contexts are in Error or lagging? | |
| Which DDBoost clients are disconnected or erroring? | |
| Is the filesystem status Enabled and Running? | |
| Are there any faulted or absent disks? | |
