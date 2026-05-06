# NetBackup Operations

Daily operational checks form the baseline for a healthy NetBackup environment. Run `bpjobs -summary` each morning to get a count of successful, failed, and active jobs, then investigate any failed jobs using `bpdbjobs -report -failed` to retrieve detailed status codes and error messages. Verify the catalog backup completed successfully — catalog loss is unrecoverable — and review storage unit disk usage via `bpstulist -label <stu>` to ensure no units are near capacity. Confirm media server connectivity by checking `bptestbpcd` against each media server from the master.

**Daily Checklist**

- [ ] `bpjobs -summary` — review totals; zero failed is the target
- [ ] `bpdbjobs -report -failed -hoursago 24` — investigate each failure
- [ ] Confirm catalog backup job completed successfully
- [ ] `bpstulist` — check `Total Capacity` vs `Free Space` on all disk STUs
- [ ] `nbemmcmd -listhosts` — verify all media servers are registered and reachable
- [ ] OpsCenter / Admin Console — review any active alerts

**Weekly**

- Verify tape media inventory if tape library in use (`tpconfig -d`, `vmquery -b`)
- Review policy schedule calendar for upcoming full backup windows
- Confirm deduplication ratio on OST storage units (Data Domain DDOS UI)
