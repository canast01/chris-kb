# Storage Latency Decision Tree

## First Decision


Is latency > 20 ms?

Yes → Check resync

If resync active → Wait

If not → Check storage array

If array healthy → Check network
