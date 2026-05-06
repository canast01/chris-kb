# Brocade Fabric OS Lifecycle

Fabric OS versions are tracked against Broadcom's published end-of-support schedule, with upgrade decisions driven by the HCL requirements of connected hosts and storage. Firmware upgrades use the non-disruptive `firmwaredownload` command, which stages the new image and activates it on the next reboot (HA chassis) or via a hitless upgrade (supported platforms). The HCL is verified before any firmware upgrade to confirm compatibility with connected host HBA drivers and storage array microcode. G-series and X-series platforms have separate version tracks and end-of-sale/end-of-support dates.

| Platform | Current FOS Track | End-of-Support Notes |
|---|---|---|
| G620 / G720 | FOS 9.x | Check Broadcom portal for exact dates |
| X7-4 / X7-8 | FOS 9.x | Director-class, extended support window |
| Legacy 6505/6510 | FOS 8.x | End-of-sale; plan migration |
