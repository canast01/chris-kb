# FOD — Common Issues

> Part of the [Flex on Demand](../../) reference.

---

| Symptom | Likely Cause | Action |
|---|---|---|
| Unexpected burst charges on FOD bill | Workload spike or snapshot/backup growth pushed usage above committed baseline | Review CloudIQ capacity trend for the billing period; identify the growth driver; adjust committed baseline if sustained |
| CloudIQ reports no telemetry for a FOD-enrolled system | Secure Connect Gateway offline or CloudIQ agent not running | Check SCG appliance health; verify outbound HTTPS connectivity to Dell CloudIQ endpoints |
| FOD capacity ceiling reached (no more burst available) | All pre-installed burst capacity is consumed | Contact Dell account team to install additional physical capacity under the FOD agreement |
| Committed baseline appears incorrect in APEX Console | Baseline was set at contract time and workload changed | Submit a baseline adjustment request through APEX Console or Dell account team |
