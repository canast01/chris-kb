---
tags:
  - linux
  - troubleshooting
search:
  boost: 1.5
description: "High CPU Troubleshooting reference covering Overview, CPU Threshold Reference, Diagnostic Flowchart, Windows CPU Diagnosis, VMware ESXi: esxtop CPU..."
---
# High CPU Troubleshooting

<div class="kb-summary">
High CPU Troubleshooting reference covering Overview, CPU Threshold Reference, Diagnostic Flowchart, Windows CPU Diagnosis, VMware ESXi: esxtop CPU Analysis and 4 more sections.

*Applies to: RHEL / Ubuntu LTS*
</div>

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Overview

High CPU utilization causes application latency, request queuing, and service instability. Effective diagnosis requires platform-specific tools to distinguish user-space runaway processes, kernel-level contention, JVM thread saturation, and hypervisor-level CPU ready time — each with different remediation paths.

---

## CPU Threshold Reference

| Platform | Metric | Warning | Critical | Action |
|---|---|---|---|---|
| Linux | Overall CPU % (top) | >70% sustained 5 min | >90% sustained 2 min | Identify top process; check recent deploy |
| Linux | Load average vs vCPU count | Load > vCPU count | Load > 2x vCPU count | Check for blocked I/O or CPU-bound tasks |
| Windows | CPU % (Task Manager) | >80% sustained | >95% sustained | perfmon; process tree analysis |
| VMware ESXi host | Overall host CPU % | >70% | >85% | Check VM density; DRS balancing |
| VMware VM | %RDY (CPU Ready) | >5% | >10% | Reduce vCPU count; migrate VM; DRS |
| VMware VM | %CSTP (Co-Stop) | >3% | >5% | Reduce vCPU count on SMP VMs |
| JVM | GC CPU overhead | >10% of CPU | >25% of CPU | Heap analysis; GC tuning |
| Database | CPU during query | Spikes >80% | Sustained >90% | Slow query log; missing indexes |

---

## Diagnostic Flowchart

```d2
direction: right

A: "High CPU Alert" {shape: rectangle}
C: "top / htop — identify PID\nps aux --sort=-%cpu" {shape: rectangle}
E: "perf top — identify kernel function\nCheck for storage I/O wait driving ksoftirqd" {shape: rectangle}
G: "Identify process\nCheck parent: pstree -p PID" {shape: rectangle}
I: "kill -15 PID\nMonitor recovery" {shape: rectangle}
J: "Notify app owner\nCapture thread dump first" {shape: rectangle}
K: "Check if same binary\nPossibly fork bomb or worker threads" {shape: rectangle}
L: "Get-Process sort CPU\nperfmon counter: % Processor Time" {shape: rectangle}
N: "Check service dependencies\nEvent log for errors" {shape: rectangle}
O: "Capture process dump\nDebug or rollback" {shape: rectangle}
P: "esxtop — check %RDY %CSTP\nFilter: G for group, H for host" {shape: rectangle}
R: "Host overcommitted\nDRS / migrate VM / reduce vCPU" {shape: rectangle}
S: "CPU issue is inside guest\nFollow Linux or Windows path" {shape: rectangle}
T: "jstack PID — thread dump\nCheck for BLOCKED threads" {shape: rectangle}
V: "jstat -gcutil PID 1000\nAnalyze heap usage" {shape: rectangle}
W: "Find CPU-burning thread\nCorrelate thread ID hex to jstack output" {shape: rectangle}

```

### perf — Deeper Kernel Analysis

```bash
# Record 30 seconds of CPU activity
perf record -g -a sleep 30

# Generate report
perf report --stdio | head -40

# Flame graph approach
perf script | stackcollapse-perf.pl | flamegraph.pl > cpu_flame.svg
```


```text title="Expected output"
[ perf record: Woken up 12 times to write data ]
[ perf record: Captured and wrote 3.842 MB perf.data (8734 samples) ]
# To display the perf.data file, run:
# perf report
# If some subcommands were not dispatched correctly, you may want to report it to linux-kernel@vger.kernel.org.

Samples: 8.7K of event 'cycles:ppp', Event count (approx.): 2847362918
Overhead  Command          Shared Object       Symbol
  12.45%  java             libc-2.31.so        [.] __memcpy_avx_unaligned
   8.92%  python3          libpython3.9.so.1.0 [.] _PyEval_EvalFrameDefault
   7.34%  nginx            libpthread-2.31.so  [.] pthread_mutex_lock
   6.18%  systemd-journal  [kernel.kallsyms]   [k] copy_user_enhanced_fast_string
   5.67%  java             libjvm.so           [.] JIT_CompilationThread
   4.89%  postgres         [kernel.kallsyms]   [k] _raw_spin_lock_irqsave
   3.45%  node             libv8.so            [.] v8::internal::Isolate::Throw
...

Wrote SVG output to cpu_flame.svg (487 KB)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `command not found: perf` | Install linux-tools package with `apt-get install linux-tools-generic` (Ubuntu/Debian) or `yum install perf` (RHEL/CentOS). |
    | `command not found: stackcollapse-perf.pl` | Clone FlameGraph tools with `git clone https://github.com/brendangregg/FlameGraph.git` and add the directory to your PATH. |
    | `Permission denied writing to perf.data` | Run the perf record command with `sudo` or ensure your user is in the `perf_event_paranoid` group. |
### Safe Process Termination

```bash
# Send SIGTERM first (graceful)
kill -15 14321

# Wait 10 seconds; if still running:
kill -9 14321

# For a runaway cgroup (containerised service):
systemctl stop application-service

# Throttle CPU via cgroup without killing (temporary relief)
systemctl set-property application.service CPUQuota=50%
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `kill: (14321) - No such process` | Verify the PID is correct with `ps aux | grep <process-name>` before attempting to kill it. |
    | `Failed to set property: Unit application.service not found.` | Ensure the service name is correct and exists by running `systemctl list-units --type=service | grep application`. |
---

## Windows CPU Diagnosis

```powershell
# Top CPU consumers — snapshot
Get-Process | Sort-Object CPU -Descending | Select-Object -First 15 |
    Select-Object Name, Id, CPU, WorkingSet, Description | Format-Table -AutoSize

# Example output:
# Name          Id      CPU WorkingSet Description
# java        4512  48923.4  845557760 Java Platform SE
# sqlservr    1024  12401.2 2147483648 SQL Server Windows NT

# Per-core CPU utilization
Get-WmiObject Win32_Processor | Select-Object Name, LoadPercentage

# perfmon — collect CPU counter
$query = "select PercentProcessorTime from Win32_PerfFormattedData_PerfOS_Processor where Name='_Total'"
(Get-WmiObject -Query $query).PercentProcessorTime

# Continuous monitoring via typeperf
typeperf "\Processor(_Total)\% Processor Time" -si 5 -sc 12

# Check CPU affinity for a process
$proc = Get-Process -Id 4512
$proc.ProcessorAffinity
```

---

## VMware ESXi: esxtop CPU Analysis

```bash
# Connect via SSH to ESXi host or run esxtop from vCenter
esxtop

# In esxtop, press 'c' for CPU view
# Key columns:
# %USED — percentage of physical CPU used
# %RDY  — CPU Ready: VM waiting for physical CPU (guest vCPUs scheduled but host busy)
# %CSTP — Co-Stop: SMP VMs waiting for all vCPUs to be scheduled simultaneously
# %MLMTD — Hard limit reached (resource pool limit)
# %SWPWT — Swap wait: memory swapping causing CPU stall

# Export esxtop batch data for analysis
esxtop -b -d 2 -n 30 > /tmp/esxtop_$(date +%Y%m%d_%H%M).csv

# Filter for specific VM by name (press 'f' then select GID)
```


```text title="Expected output"
Starting esxtop...

PCPU USED(%): 45.2  UTIL(%): 89.4  SYS(%): 12.1  WAIT(%): 2.3
 GID  NAME                           %USED  %RDY  %CSTP  %MLMTD  %SWPWT
   1  vm-prod-web-01                 38.5   8.2    0.0    0.0     0.0
   2  vm-prod-db-02                  42.1  15.3    2.1    0.0     1.2
   3  vm-dev-app-03                  18.7   3.1    0.0    0.0     0.0
   4  vm-test-batch-04               12.3   0.5    0.0   12.5     0.0
   5  vm-prod-cache-05               28.9   6.7    0.0    0.0     0.3
...
(Press 'q' to quit, 'c' for CPU, 'f' to filter)

esxtop -b -d 2 -n 30 > /tmp/esxtop_20240115_143022.csv
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `esxtop: command not found` | Run esxtop directly on the ESXi host via SSH or use vCenter's embedded esxtop client; it is not available on standard Linux systems. |
    | `Permission denied` | Ensure your user account has Administrator or equivalent privileges on the ESXi host; non-root users cannot access esxtop. |
    | `/tmp/esxtop_*.csv: Read-only file system` | Verify /tmp has write permissions and sufficient free space; try writing to /var/tmp or a mounted datastore instead. |
### CPU Ready Time Interpretation

| %RDY Value | Interpretation | Action |
|---|---|---|
| 0–5% | Healthy | No action required |
| 5–10% | Warning — minor contention | Monitor; check host CPU utilization |
| 10–20% | Significant contention | Reduce vCPU count; DRS migration |
| >20% | Critical | Immediate VM migration; host overloaded |
| >30% | Severe | Emergency: evacuate VMs; add capacity |

```bash
# PowerCLI: get CPU Ready for all VMs on a host
Get-VM | Get-Stat -Stat cpu.ready.summation -MaxSamples 5 -Realtime |
    Group-Object Entity |
    Select-Object @{N='VM';E={$_.Name}},
                  @{N='CPUReady_ms';E={($_.Group | Measure-Object Value -Average).Average}} |
    Sort-Object CPUReady_ms -Descending | Select-Object -First 10

# Convert ms to %: Ready% = (Ready_ms / (20000 * vCPU_count)) * 100
```


```text title="Expected output"
VM                          CPUReady_ms
--                          -----------
web-app-prod-01             1847.32
db-cluster-node-02          1523.68
cache-redis-primary         892.45
api-gateway-01              756.21
monitoring-agent-03         634.89
backup-service-02           512.34
logging-forwarder-04        387.12
mail-relay-01               245.67
dns-secondary-02            178.43
ntp-sync-01                 156.21
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Get-VM : The term 'Get-VM' is not recognized as the name of a cmdlet, function, script file, or operable program.` | Load the VMware PowerCLI module with `Import-Module VMware.PowerCLI` before running the command. |
    | `Get-Stat : A parameter cannot be found that matches parameter name 'Realtime'.` | Use `-Real` instead of `-Realtime` for real-time statistics in your PowerCLI version. |
    | `The property "Value" cannot be found on this object.` | Verify the CPU ready statistic exists by running `Get-Stat -Stat cpu.ready.summation` alone to confirm the metric name and data availability. |
---

## Java/JVM High CPU Troubleshooting

```bash
# Identify which Java thread is consuming CPU
# Step 1: get PID
ps aux | grep java
# PID = 14321

# Step 2: get top threads within that PID (Linux)
top -H -p 14321
# Note the TID of the highest CPU thread (e.g., TID 14456)

# Step 3: convert TID to hex
printf '%x\n' 14456
# Output: 3878

# Step 4: capture thread dump
jstack 14321 > /tmp/jstack_$(date +%H%M%S).txt

# Step 5: find thread 0x3878 in jstack output
grep -A 20 "nid=0x3878" /tmp/jstack_$(date +%H%M%S).txt

# Step 6: check GC overhead
jstat -gcutil 14321 1000 10
# Output:
#   S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT
#  0.00  95.32  88.12  99.01  97.64  95.52    854  120.412   42  310.897  431.309
# ^ FGC=42 Full GCs, FGCT=310s → GC overhead is very high → heap exhaustion
```


```text title="Expected output"
root@prod-app-01:~# ps aux | grep java
root      14321  87.3 45.2 8589934592 3758096 ?   Sl   14:22   127:45 java -Xmx8g -Xms8g -jar application.jar
root      14456     0  0.0      1024     512 ?   S    14:22    0:00 grep java

root@prod-app-01:~# top -H -p 14321
top - 14:35:22 up 18 days, 3:42, 1 user, load average: 8.24, 7.91, 6.53
Tasks:  127 total,   3 running, 124 sleeping,   0 stopped,   0 zombie
%Cpu(s): 89.2 us,  8.1 sy,  0.0 ni,  2.1 id,  0.6 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :  64000.0 total, 58234.5 free,  4123.2 used,  1642.3 buff/cache
MiB Swap:  16384.0 total, 16384.0 free,     0.0 used. 57891.2 avail Mem

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
  14456 root      20   0 8589934592 3758096 245120 R  94.2 45.2 127:52 java
  14457 root      20   0 8589934592 3758096 245120 S  12.1  0.0   8:23 java
  14458 root      20   0 8589934592 3758096 245120 S   3.4  0.0   2:15 java

root@prod-app-01:~# printf '%x\n' 14456
3878

root@prod-app-01:~# jstack 14321 > /tmp/jstack_143522.txt

root@prod-app-01:~# grep -A 20 "nid=0x3878" /tmp/jstack_143522.txt
"GC task thread#0 (ParallelGC)" os_prio=0 tid=0x00007f8a2c001000 nid=0x3878 runnable
   java.lang.Thread.State: RUNNABLE
        at java.lang.Object.wait(Native Method)
        at com.sun.org.apache.xerces.internal.impl.XMLDocumentFragmentScannerImpl.scanDocument(XMLDocumentFragmentScannerImpl.java:378)
        at com.sun.org.apache.xerces.internal.parsers.XML11Configuration.parse(XML11Configuration.java:848)
        at com.sun.org.apache.xerces.internal.parsers.XMLParser.parse(XMLParser.java:141)
        at javax.xml.parsers.SAXParser.parse(SAXParser.java:195)

root@prod-app-01:~# jstat -gcutil 14321 1000
```
---

## Database CPU Spikes

### MySQL / MariaDB

```sql
-- Show currently running queries
SHOW FULL PROCESSLIST;

-- Find long-running queries
SELECT id, user, host, db, command, time, state, info
FROM information_schema.processlist
WHERE time > 10
ORDER BY time DESC;

-- Check slow query log
-- my.cnf: slow_query_log=1, long_query_time=2
SHOW VARIABLES LIKE 'slow_query_log%';
```

### Microsoft SQL Server

```sql
-- Find top CPU queries
SELECT TOP 10
    qs.total_worker_time/qs.execution_count AS avg_cpu_us,
    qs.execution_count,
    SUBSTRING(qt.text, qs.statement_start_offset/2,
        (CASE qs.statement_end_offset WHEN -1 THEN LEN(CONVERT(nvarchar(max), qt.text)) * 2
         ELSE qs.statement_end_offset END - qs.statement_start_offset)/2) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY avg_cpu_us DESC;

-- Check for blocking
SELECT blocking_session_id, session_id, wait_type, wait_time, cpu_time
FROM sys.dm_exec_requests
WHERE blocking_session_id <> 0;
```

---

## Recent Change Correlation

```bash
# Check for deployments, package installs, or cron jobs at time of spike
grep "Install\|deploy\|update" /var/log/dpkg.log | tail -20   # Debian/Ubuntu
grep "Install\|deploy\|update" /var/log/yum.log | tail -20    # RHEL

# Check cron jobs that ran during the spike window
grep "CMD" /var/log/cron | grep "08:00\|08:05\|08:10"

# Check systemd service start times
systemctl list-units --state=active --type=service |
    xargs -I{} systemctl show {} --property=ActiveEnterTimestamp
```


```text title="Expected output"
2024-01-15 08:02:47 install postgresql-client:amd64 <none> 14.2-1.pgdg110+1
2024-01-15 08:03:12 install libpq5:amd64 <none> 14.2-1.pgdg110+1
2024-01-15 08:04:33 install postgresql-contrib:amd64 14.1-1.pgdg110+1 14.2-1.pgdg110+1
2024-01-15 08:05:18 status half-configured postgresql-contrib:amd64 14.1-1.pgdg110+1
2024-01-15 08:06:02 status unpacked postgresql-contrib:amd64 14.2-1.pgdg110+1
Jan 15 08:05:22 prod-app-01 CRON[4521]: (root) CMD (cd /opt/backup && ./daily-sync.sh >> /var/log/backup.log 2>&1)
Jan 15 08:10:14 prod-app-01 CRON[4687]: (deploy) CMD (/usr/local/bin/health-check.sh)
ActiveEnterTimestamp=Mon 2024-01-15 08:02:15 UTC
ActiveEnterTimestamp=Mon 2024-01-15 08:04:22 UTC
ActiveEnterTimestamp=Mon 2024-01-15 07:58:43 UTC
ActiveEnterTimestamp=Mon 2024-01-15 08:06:11 UTC
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: /var/log/dpkg.log: No such file or directory` | Check the correct log path for your distribution; RHEL/CentOS systems use `/var/log/yum.log` or `/var/log/dnf.log` instead. |
    | `xargs: unterminated quote` | Escape special characters in the systemctl show command or use `systemctl list-units --state=active --type=service --no-pager` with a simpler follow-up query. |
    | `permission denied` | Run the commands with `sudo` to access system logs and systemd service details. |
---

## Escalation Criteria

Escalate to application team, platform team, or vendor when:

- CPU utilization sustained >90% for >15 minutes with no identified runaway process
- %RDY >20% on multiple VMs across the same ESXi host simultaneously (capacity event)
- JVM thread dump shows deadlock or all threads BLOCKED (application bug)
- CPU spike correlates with a database query that cannot be killed without data risk
- Kernel CPU (sy%) >50% indicating potential kernel bug or driver issue
- CPU throttling via cgroup/resource pool is masking an unresolved application fault
- Security scan or crypto mining suspected (unexpected processes, outbound connections)
- Host hardware fault suspected: check `esxcli hardware cpu list` and IPMI/iLO SEL logs

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Linux — Common Issues](../common-issues/)
- [Linux — Diagnostics](../diagnostics/)
- [Linux — Escalation](../escalation/)
- [Linux — Procedures](../../operations/procedures/)
