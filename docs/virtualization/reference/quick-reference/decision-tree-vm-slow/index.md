# VM Slow Decision Tree

```
                         VM reported slow
                               │
                               ▼
                    ┌────────────────────┐
                    │  CPU Ready > 5%?   │
                    └────────────────────┘
               Yes ▼                    No ▼
     ┌────────────────────┐    ┌────────────────────┐
     │ CPU contention     │    │ Memory balloon/    │
     │ Check host CPU     │    │ swap active?       │
     │ utilisation        │    └────────────────────┘
     │ Check DRS          │    Yes ▼         No ▼
     └────────────────────┘  ┌──────────┐  ┌──────────────────┐
                              │ Add mem  │  │ Storage latency? │
                              │ or move  │  │ DAVG/GAVG high?  │
                              │ workload │  └──────────────────┘
                              └──────────┘  Yes ▼       No ▼
                                         ┌──────────┐  ┌────────────────┐
                                         │ Storage  │  │ Network drops? │
                                         │ decision │  │ Check NIC/vDS  │
                                         │ tree     │  │ packet stats   │
                                         └──────────┘  └────────────────┘
```

## First Decision


Is CPU high?

Yes → Check CPU Ready

No → Check Memory

Is Memory Ballooning?

Yes → Add memory or move workload

No → Check Storage Latency

If latency high → Investigate storage
