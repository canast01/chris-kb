#!/usr/bin/env python3
"""
Inject D2, PlantUML, and Vega-Lite diagrams into architecture/how-it-works pages.

Each entry in DIAGRAMS specifies:
  - file: relative path under docs/
  - type: d2 | plantuml | vega-lite
  - position: "after_svg" (before first H2) | "in_section:Section Name" (after that H2 heading line)
  - content: the diagram source

Idempotent: skips injection if the fence type already appears in the file.
"""

import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent / "docs"

# ---------------------------------------------------------------------------
# Diagram registry
# ---------------------------------------------------------------------------

DIAGRAMS = [

    # ── vSAN ────────────────────────────────────────────────────────────────

    {
        "file": "virtualization/vmware/vsan/architecture/how-it-works.md",
        "type": "d2",
        "position": "after_svg",
        "content": """\
```d2
direction: right

cluster: vSAN Cluster {
  host1: ESXi Host 1 {
    dg1: "Cache SSD + 3× Capacity" {shape: cylinder}
  }
  host2: ESXi Host 2 {
    dg2: "Cache SSD + 3× Capacity" {shape: cylinder}
  }
  host3: ESXi Host 3 {
    dg3: "Cache SSD + 3× Capacity" {shape: cylinder}
  }
}

vcenter: vCenter Server {shape: rectangle}
witness: Witness Appliance\\n(stretched only) {shape: diamond}

vcenter -> cluster.host1: ESXi management
vcenter -> cluster.host2: ESXi management
vcenter -> cluster.host3: ESXi management

cluster.host1 -> cluster.host2: vSAN VMkernel (UDP 2233)
cluster.host2 -> cluster.host3: vSAN VMkernel (UDP 2233)
cluster.host1 -> cluster.host3: vSAN VMkernel (UDP 2233)
```
""",
    },

    {
        "file": "virtualization/vmware/vsan/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "in_section:Write Path",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "VM / App" as VM
participant "vSAN Kernel\\n(local host)" as KERNEL
participant "Object Manager\\n(OM)" as OM
participant "CLOM\\n(cluster placement)" as CLOM
participant "DOM\\n(distributed I/O)" as DOM
participant "Cache Tier\\n(SSD)" as CACHE
participant "Capacity Tier\\n(HDD / NVMe)" as CAP

VM -> KERNEL: Write I/O
KERNEL -> OM: Policy-based placement
OM -> CLOM: FTT compliance check
CLOM -> DOM: Distribute components across hosts
DOM -> CACHE: Write to cache (SSD)
CACHE --> DOM: ACK (write acknowledged to VM)
DOM --> VM: Write complete
...async destage...
CACHE -> CAP: Destage to capacity tier
@enduml
```
""",
    },

    # ── SRM ─────────────────────────────────────────────────────────────────

    {
        "file": "virtualization/vmware/srm/architecture/how-it-works.md",
        "type": "d2",
        "position": "in_section:Site Topology",
        "content": """\
```d2
direction: right

protected: Protected Site {
  vc_p: vCenter Server {shape: rectangle}
  srm_p: SRM Server {shape: rectangle}
  vms: Protected VMs {shape: rectangle}
  storage_p: Production Storage {shape: cylinder}
  vc_p -> srm_p
  srm_p -> vms: protect
  vms -> storage_p
}

recovery: Recovery Site {
  vc_r: vCenter Server {shape: rectangle}
  srm_r: SRM Server {shape: rectangle}
  placeholders: Placeholder VMs {shape: rectangle}
  storage_r: Recovery Storage {shape: cylinder}
  vc_r -> srm_r
  srm_r -> placeholders
}

protected.srm_p -> recovery.srm_r: SRM pairing (TCP 443)
protected.storage_p -> recovery.storage_r: Replication (SRA / vSphere Replication)
```
""",
    },

    {
        "file": "virtualization/vmware/srm/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "in_section:Disaster Recovery Failover",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "SRM Admin" as Admin
participant "SRM\\n(Protected Site)" as SRM_P
participant "SRM\\n(Recovery Site)" as SRM_R
participant "Storage SRA" as SRA
participant "vCenter\\n(Recovery)" as VC_R
participant "Recovered VMs" as VMS

Admin -> SRM_R: Execute Recovery Plan
SRM_R -> SRM_P: Notify protected site (if reachable)
SRM_R -> SRA: Invoke failover snapshot
SRA --> SRM_R: Storage volumes ready
SRM_R -> VC_R: Remove placeholder VMs
SRM_R -> VC_R: Register recovered VMs (priority order)
VC_R -> VMS: Power on — highest priority first
VMS --> SRM_R: VM heartbeat OK
SRM_R -> Admin: Recovery report (RPO achieved)
@enduml
```
""",
    },

    # ── ESXi ────────────────────────────────────────────────────────────────

    {
        "file": "virtualization/vmware/esxi/architecture/how-it-works.md",
        "type": "d2",
        "position": "in_section:VMkernel Architecture",
        "content": """\
```d2
direction: down

hardware: Physical Hardware {
  cpu: CPUs {shape: rectangle}
  mem: Memory {shape: rectangle}
  nic: Network (NICs) {shape: rectangle}
  hba: Storage (HBAs / NVMe) {shape: rectangle}
}

vmkernel: VMkernel (Hypervisor) {
  scheduler: CPU Scheduler {shape: rectangle}
  memctl: Memory Manager {shape: rectangle}
  netstack: TCP/IP Network Stack {shape: rectangle}
  psa: Storage Stack (PSA/NMP) {shape: rectangle}
}

userworld: User World (Processes) {
  hostd: hostd (host agent) {shape: rectangle}
  vpxa: vpxa (vCenter agent) {shape: rectangle}
  ntpd: ntpd / syslog {shape: rectangle}
}

vms: Virtual Machines {
  vm1: VM 1 (vCPU / vMEM / vNIC / vDisk) {shape: rectangle}
  vm2: VM 2 {shape: rectangle}
  vmn: VM N {shape: rectangle}
}

hardware -> vmkernel: direct hardware access
vmkernel -> userworld: system calls
vmkernel -> vms: virtualised resources
```
""",
    },

    # ── NetApp ONTAP ────────────────────────────────────────────────────────

    {
        "file": "storage/netapp/ontap/architecture/how-it-works.md",
        "type": "d2",
        "position": "in_section:HA Pair Architecture",
        "content": """\
```d2
direction: right

node_a: Controller A (Active) {shape: rectangle}
node_b: Controller B (HA Partner) {shape: rectangle}
shelves: Disk Shelves {shape: cylinder}
clients: Clients {shape: person}
svms: SVMs (Data LIFs) {shape: rectangle}

node_a -> node_b: HA interconnect\\n(NVRAM mirror, RDMA)
node_a -> shelves: SAS / NVMe (owns aggregates)
node_b -> shelves: SAS / NVMe (takeover path)
clients -> svms: NFS / CIFS / iSCSI / NVMe-oF
svms -> node_a: served via aggregates
node_b -> svms: serves LIFs during takeover
```
""",
    },

    {
        "file": "storage/netapp/ontap/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "in_section:SnapMirror and SnapVault",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Source SVM\\n(Primary)" as SRC
participant "Source Volume" as SVOL
participant "SnapMirror Engine" as SM
participant "Destination SVM\\n(Secondary)" as DST
participant "Destination Volume\\n(DP — read-only)" as DVOL

SRC -> SM: Initialize relationship
SM -> SVOL: Create baseline Snapshot
SM -> DST: Transfer baseline (full copy)
DST -> DVOL: Write baseline
DVOL --> SM: Baseline complete

loop Scheduled update (hourly / daily)
  SM -> SVOL: Create new Snapshot
  SM -> SM: Compute incremental delta from last transfer Snapshot
  SM -> DST: Transfer delta blocks
  DST -> DVOL: Apply delta
  DVOL --> SM: Update complete
  SM -> SVOL: Delete previous transfer Snapshot
end

note over SM,DST: On DR activation — break relationship, promote DVOL to R/W
@enduml
```
""",
    },

    # ── Brocade Fabric OS ───────────────────────────────────────────────────

    {
        "file": "san/brocade/fabric-os/architecture/how-it-works.md",
        "type": "d2",
        "position": "after_svg",
        "content": """\
```d2
direction: right

hosts: Servers {
  h1: Server 1 (dual HBA) {shape: rectangle}
  h2: Server 2 (dual HBA) {shape: rectangle}
  h3: Server 3 (dual HBA) {shape: rectangle}
}

fabric_a: Fabric A (primary) {
  sw1: Switch A1\\n(principal) {shape: rectangle}
  sw2: Switch A2 {shape: rectangle}
  sw1 -> sw2: ISL (E_Port)
}

fabric_b: Fabric B (redundant) {
  sw3: Switch B1\\n(principal) {shape: rectangle}
  sw4: Switch B2 {shape: rectangle}
  sw3 -> sw4: ISL (E_Port)
}

storage: Storage Arrays {
  arr1: Array 1 (target ports) {shape: cylinder}
  arr2: Array 2 (target ports) {shape: cylinder}
}

hosts.h1 -> fabric_a.sw1: F_Port
hosts.h1 -> fabric_b.sw3: F_Port
hosts.h2 -> fabric_a.sw2: F_Port
hosts.h2 -> fabric_b.sw4: F_Port
hosts.h3 -> fabric_a.sw1: F_Port
hosts.h3 -> fabric_b.sw3: F_Port

fabric_a.sw1 -> storage.arr1: F_Port
fabric_a.sw2 -> storage.arr2: F_Port
fabric_b.sw3 -> storage.arr1: F_Port
fabric_b.sw4 -> storage.arr2: F_Port
```
""",
    },

    # ── Pure FlashArray ─────────────────────────────────────────────────────

    {
        "file": "storage/pure/flasharray/architecture/how-it-works.md",
        "type": "d2",
        "position": "after_svg",
        "content": """\
```d2
direction: right

hosts: Hosts {
  host1: Host 1 {shape: rectangle}
  host2: Host 2 {shape: rectangle}
}

fa1: FlashArray //X (site A) {
  ct0: Controller 0 {shape: rectangle}
  ct1: Controller 1 {shape: rectangle}
  nvme: NVMe Flash Modules {shape: cylinder}
  ct0 -> ct1: Active/Active (NVRAM sync)
  ct0 -> nvme
  ct1 -> nvme
}

fa2: FlashArray //X (site B, ActiveCluster) {
  ct0b: Controller 0 {shape: rectangle}
  ct1b: Controller 1 {shape: rectangle}
  nvme2: NVMe Flash Modules {shape: cylinder}
  ct0b -> ct1b: Active/Active (NVRAM sync)
  ct0b -> nvme2
  ct1b -> nvme2
}

mediator: Pure1 Mediator\\n(quorum arbitration) {shape: diamond}

hosts.host1 -> fa1.ct0: FC / iSCSI / NVMe-oF
hosts.host2 -> fa2.ct0b: FC / iSCSI / NVMe-oF

fa1 -> fa2: ActiveCluster sync replication
fa1 -> mediator: heartbeat
fa2 -> mediator: heartbeat
```
""",
    },

    # ── Nutanix ─────────────────────────────────────────────────────────────

    {
        "file": "virtualization/nutanix/architecture/how-it-works.md",
        "type": "d2",
        "position": "after_svg",
        "content": """\
```d2
direction: right

cluster: Nutanix HCI Cluster {
  node1: Node 1 {
    cvm1: CVM 1 {shape: rectangle}
    vm1: Guest VMs {shape: rectangle}
    disk1: Local NVMe/SSD/HDD {shape: cylinder}
    cvm1 -> disk1: manages
  }
  node2: Node 2 {
    cvm2: CVM 2 {shape: rectangle}
    vm2: Guest VMs {shape: rectangle}
    disk2: Local NVMe/SSD/HDD {shape: cylinder}
    cvm2 -> disk2: manages
  }
  node3: Node 3 {
    cvm3: CVM 3 {shape: rectangle}
    vm3: Guest VMs {shape: rectangle}
    disk3: Local NVMe/SSD/HDD {shape: cylinder}
    cvm3 -> disk3: manages
  }
}

prism: Prism Central\\n(management) {shape: rectangle}
ad: Active Directory {shape: rectangle}

prism -> cluster.node1.cvm1: manage
prism -> cluster.node2.cvm2: manage
prism -> cluster.node3.cvm3: manage
prism -> ad: auth

cluster.node1.cvm1 -> cluster.node2.cvm2: DSF replication
cluster.node2.cvm2 -> cluster.node3.cvm3: DSF replication
cluster.node1.cvm1 -> cluster.node3.cvm3: DSF replication
```
""",
    },

    # ── Cisco MDS ───────────────────────────────────────────────────────────

    {
        "file": "san/cisco/mds/architecture/how-it-works.md",
        "type": "d2",
        "position": "after_svg",
        "content": """\
```d2
direction: right

hosts: Servers {
  h1: Host 1 (HBA) {shape: rectangle}
  h2: Host 2 (HBA) {shape: rectangle}
}

director_a: MDS Director A\\n(Fabric A) {
  linecard1: Line Card 1 (32×32G) {shape: rectangle}
  linecard2: Line Card 2 (32×32G) {shape: rectangle}
  sup: Supervisor Module {shape: rectangle}
  linecard1 -> sup: backplane
  linecard2 -> sup: backplane
}

director_b: MDS Director B\\n(Fabric B) {
  linecard3: Line Card 3 (32×32G) {shape: rectangle}
  linecard4: Line Card 4 (32×32G) {shape: rectangle}
  sup2: Supervisor Module {shape: rectangle}
  linecard3 -> sup2: backplane
  linecard4 -> sup2: backplane
}

storage: Storage Arrays {
  arr: Target Ports {shape: cylinder}
}

dcnm: Cisco DCNM\\n(management) {shape: rectangle}

hosts.h1 -> director_a.linecard1: F_Port (32G FC)
hosts.h1 -> director_b.linecard3: F_Port (dual fabric)
hosts.h2 -> director_a.linecard1: F_Port
hosts.h2 -> director_b.linecard3: F_Port

director_a.linecard2 -> storage.arr: F_Port
director_b.linecard4 -> storage.arr: F_Port

dcnm -> director_a.sup: SNMP / SSH
dcnm -> director_b.sup2: SNMP / SSH
```
""",
    },

    # ── Dell PowerMax ───────────────────────────────────────────────────────

    {
        "file": "storage/dell/powermax/architecture/how-it-works.md",
        "type": "d2",
        "position": "after_svg",
        "content": """\
```d2
direction: right

hosts: Hosts {
  h1: Host A {shape: rectangle}
  h2: Host B {shape: rectangle}
}

pm1: PowerMax (Site A) {
  fe_a: Front-End Directors\\n(FC / iSCSI / NVMe) {shape: rectangle}
  be_a: Back-End Directors\\n(NVMe-oF to flash) {shape: rectangle}
  rdf_a: RDF Directors {shape: rectangle}
  flash_a: NVMe Flash Bays {shape: cylinder}
  fe_a -> be_a: internal fabric
  be_a -> flash_a
}

pm2: PowerMax (Site B) {
  fe_b: Front-End Directors {shape: rectangle}
  rdf_b: RDF Directors {shape: rectangle}
  flash_b: NVMe Flash Bays {shape: cylinder}
  fe_b -> flash_b
}

unisphere: Unisphere\\n(management) {shape: rectangle}

hosts.h1 -> pm1.fe_a: FC / NVMe-oF
hosts.h2 -> pm2.fe_b: FC / NVMe-oF

pm1.rdf_a -> pm2.rdf_b: SRDF replication\\n(sync / async / STAR)

unisphere -> pm1.fe_a: manage
unisphere -> pm2.fe_b: manage
```
""",
    },

]

# ---------------------------------------------------------------------------
# Injection logic
# ---------------------------------------------------------------------------

FENCE_TYPE_MARKER = {
    "d2":         "```d2",
    "plantuml":   "```plantuml",
    "vega-lite":  "```vega-lite",
}


def already_has(lines: list[str], fence_type: str) -> bool:
    marker = FENCE_TYPE_MARKER[fence_type]
    return any(line.rstrip() == marker for line in lines)


def find_after_svg(lines: list[str]) -> int | None:
    """Return index of the line immediately before the first ## heading,
    after the SVG image line."""
    svg_seen = False
    for i, line in enumerate(lines):
        if not svg_seen and "![" in line and ".svg" in line:
            svg_seen = True
            continue
        if svg_seen and line.startswith("## "):
            return i
    return None


def find_in_section(lines: list[str], section: str) -> int | None:
    """Return index of the line immediately after the ## heading line."""
    target = f"## {section}"
    for i, line in enumerate(lines):
        if line.rstrip() == target:
            return i + 1  # insert right after heading
    return None


def inject(lines: list[str], pos: int, content: str) -> list[str]:
    """Insert content block at pos, preceded by a blank line if needed."""
    block = []
    if pos > 0 and lines[pos - 1].strip():
        block.append("\n")
    block.append(content if content.endswith("\n") else content + "\n")
    if pos < len(lines) and lines[pos].strip():
        block.append("\n")
    return lines[:pos] + block + lines[pos:]


def process(entry: dict, dry_run: bool) -> str:
    path = ROOT / entry["file"]
    if not path.exists():
        return "NOT FOUND"

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    if already_has(lines, entry["type"]):
        return "SKIP (already has diagram)"

    position = entry["position"]
    if position == "after_svg":
        pos = find_after_svg(lines)
    elif position.startswith("in_section:"):
        section = position[len("in_section:"):]
        pos = find_in_section(lines, section)
    else:
        return f"UNKNOWN position: {position}"

    if pos is None:
        return f"SKIP (insertion point not found: {position})"

    if not dry_run:
        new_lines = inject(lines, pos, entry["content"])
        path.write_text("".join(new_lines), encoding="utf-8")

    return "DRY RUN" if dry_run else "UPDATED"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--file", help="Process only entries matching this path substring")
    args = ap.parse_args()

    entries = DIAGRAMS
    if args.file:
        entries = [e for e in entries if args.file in e["file"]]

    updated = skipped = missing = 0
    for e in entries:
        result = process(e, args.dry_run)
        label = "DRY RUN" if args.dry_run and "UPDATED" in result else result.split()[0]
        print(f"[{label:8}] {e['file']}  ({e['type']}  @ {e['position']})")
        if "UPDATED" in result or "DRY RUN" in result:
            updated += 1
        elif "NOT FOUND" in result:
            missing += 1
        else:
            skipped += 1

    print()
    print("=" * 64)
    verb = "would update" if args.dry_run else "updated"
    print(f"{verb.capitalize()}: {updated}  |  Skipped: {skipped}  |  Not found: {missing}")
    print("=" * 64)


if __name__ == "__main__":
    main()
