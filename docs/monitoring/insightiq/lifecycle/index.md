# InsightIQ Lifecycle

InsightIQ version compatibility with OneFS must be validated before any cluster OS upgrade — refer to the NetApp Interoperability Matrix Tool (IMT). The upgrade procedure for the InsightIQ appliance is: back up the PostgreSQL database, replace the OVA (or upgrade the Linux package), and verify all cluster connections re-establish post-upgrade. Where organisations have upgraded to OneFS 9.x, native OneFS performance views (via the OneFS web UI and CLI) may partially replace InsightIQ functionality for simple use cases. EOL dates are published on the NetApp support portal.

| Activity | Method |
|---|---|
| Version compatibility check | NetApp IMT |
| Pre-upgrade DB backup | `pg_dump` on appliance |
| Upgrade | OVA replacement or package upgrade |
| Post-upgrade validation | Verify cluster connections in IIQ UI |
| EOL tracking | NetApp Support Portal lifecycle page |
