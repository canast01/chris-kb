# ESXi Performance Troubleshooting
## Common Symptoms

- High CPU ready time
- High memory ballooning or swapping
- High storage latency
- Slow VM response
- VM time drift
- Host contention alarms

## Key Metrics

CPU Ready: < 5% normal  
Memory Ballooning: Should be near zero  
Swap: Should be zero in steady state  
Datastore Latency:  
- < 10 ms normal  
- 10–20 ms caution  
- > 20 ms problem

## Commands

esxtop

Press:
c = CPU
m = Memory
d = Disk
n = Network

resxtop

## First Actions

1. Identify the affected VM or host.
2. Check CPU ready.
3. Check memory ballooning or swap.
4. Check datastore latency.
5. Check network packet drops.
6. Review recent changes.
