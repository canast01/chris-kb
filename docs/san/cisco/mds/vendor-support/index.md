# Cisco MDS Vendor Support

MDS support cases are opened via the Cisco TAC portal (mycase.cisco.com) or by calling TAC, referencing the switch serial number and SmartNet contract. For NX-OS or hardware issues, collect `show tech-support` output and upload it to the case — this captures running config, logs, interface state, and fabric database. For FC frame-level issues, `ethanalyzer` can capture frames on the management interface; FC Analyzer or SPAN sessions can be used for data-plane capture. SmartNet contract coverage is validated via the Cisco Contract Center or the serial number lookup on cisco.com.

- TAC portal: mycase.cisco.com
- Diagnostic bundle: `show tech-support > tech-support.txt` — upload to case
- FC frame capture: `ethanalyzer` (management plane), FC SPAN (data plane)
- Required for case: NX-OS version (`show version`), VSAN topology, error log excerpts, affected WWPNs
- Serial number: `show inventory` or chassis label
- Contract check: Cisco Contract Center — cisco.com/go/contractcenter
