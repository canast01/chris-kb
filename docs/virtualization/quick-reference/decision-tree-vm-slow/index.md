# VM Slow Decision Tree

## First Decision


Is CPU high?

Yes → Check CPU Ready

No → Check Memory

Is Memory Ballooning?

Yes → Add memory or move workload

No → Check Storage Latency

If latency high → Investigate storage
