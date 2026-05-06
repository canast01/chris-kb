# SRDF/A Architecture

SRDF/A is Dell EMC's asynchronous replication technology for PowerMax. Data is written to the source and acknowledged to the host before being transmitted to the target in delta sets (cycles). RPO is defined by cycle time, typically ranging from 30 seconds to several minutes depending on configuration and WAN capacity. Requires Symmetrix Remote Data Facility licenses on both source and target arrays.

- **Delta sets**: Captured changes are grouped per cycle and transmitted in order, maintaining write consistency across the group.
- **Cycle time**: Configurable interval (default 30s); shorter cycles reduce RPO but increase WAN bandwidth demand.
- **SRDF groups**: Logical groupings of device pairs sharing cycle boundaries for consistency.
- **Connectivity**: Typically FCIP over WAN or dark fibre between PowerMax backend directors.
