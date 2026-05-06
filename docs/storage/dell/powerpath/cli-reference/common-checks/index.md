# Common Check Sequences

> Part of the Dell PowerPath CLI Reference.

---

```bash
# Quick health check sequence
powermt display dev=all | grep -c "alive"
powermt display dev=all | grep -c "dead"
powermt display dead
powermt check
powermt restore

# Count paths per device
powermt display dev=all | awk '/emcpower/{dev=$1} /alive/{count++} /dead/{dead++} /^$/{if(dev) print dev, "alive:"count, "dead:"dead; dev=""; count=0; dead=0}'
```
