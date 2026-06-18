#!/usr/bin/env python3
"""Generate missing @kb_diagram functions and append to the right module files.
Run from chris-kb root: python3 scripts/gen_missing_diagrams.py
"""
import os, sys, textwrap

W2 = 103
IW = 95  # inner width of full-width box (L=3,R=99)
HW = 46  # inner width of half-width box

# ── Product knowledge ────────────────────────────────────────────────────────

PRODUCTS = {

  'netbackup': {
    'name': 'Veritas NetBackup', 'short': 'NetBackup',
    'tag': 'dr-netbackup', 'path': 'docs/disaster-recovery/netbackup',
    'outfile': 'scripts/diagrams/disaster_recovery_backup.py',
    'desc': 'Enterprise backup and recovery — master/media/client architecture with deduplication',
    'comp1': 'Master Server     — scheduler, catalog, policy engine, job controller',
    'comp2': 'Media Server      — data mover, dedup engine, storage unit management',
    'comp3': 'Client Agent      — installed on protected host; sends data to media server',
    'comp4': 'NetBackup Web UI  — browser admin portal on port 443, RBAC enforced',
    'comp5': 'Catalog           — PostgreSQL DB tracking all images, policies, host IDs',
    'cmd1': 'bpbackup / bprestore', 'cmd2': 'bplist / bpdbjobs', 'cmd3': 'nbpemreq / bpps',
    'cmd4': 'tpconfig / nbstlutil', 'cmd5': 'bpexpdate / bpimmediate',
    'port1': '443 (Web UI)', 'port2': '1556 (vnetd)', 'port3': '13724 (bprd)',
    'auth': 'NBU CA host-ID certificates; AD/LDAP for web UI login; RBAC roles',
    'enc': 'AES-256 backup encryption; KMS key management; TLS 1.2+ on all channels',
    'phys': 'Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection',
    'terms': [
      ('Master Server',   'central controller: scheduler, catalog, job manager, policy engine'),
      ('Media Server',    'data mover between client and storage; can be co-located with master'),
      ('MSDP',           'Media Server Deduplication Pool; inline variable-length block dedup'),
      ('Storage Unit',   'logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'),
      ('Policy',         'defines what, when, and where to back up; contains schedules and clients'),
      ('Schedule',       'full / differential-incremental / cumulative-incremental timing within policy'),
      ('Retention',      'how long an image is kept; set per schedule, enforced by catalog expiry'),
      ('Catalog',        'internal PostgreSQL DB tracking all image metadata, host IDs, and config'),
      ('NBU CA',         'auto-issued certificate authority; signs host IDs for secure comms'),
      ('vnetd',          'NetBackup network daemon; multiplexes all client-master-media on port 1556'),
      ('bpdbjobs',       'CLI to query job history: status, duration, exit code, errors'),
      ('bplist',         'CLI to list available backup images for a client, policy, or date range'),
      ('KMS',            'Key Management Service for encryption keys used in backup data encryption'),
      ('NDMP',           'Network Data Management Protocol; direct NAS-to-storage backup path'),
    ],
    'issues': [
      ('Status 96',   'client not responding',    'ping + bpps on client',    'restart nbclient',   'bpps -x'),
      ('Status 2106', 'MSDP pool full',           'bpexpdate / nbstlutil',    'expand or expire',   'nbstlutil list'),
      ('Status 58',   'media write error',        'check disk/tape health',   'new storage unit',   'tpconfig -d'),
      ('Status 84',   'media manager down',       'check ltid process',       'restart ltid',       'vmquery'),
    ],
  },

  'rasr': {
    'name': 'Dell PowerProtect Cyber Recovery (RASR)', 'short': 'RASR',
    'tag': 'dr-rasr', 'path': 'docs/disaster-recovery/rasr',
    'outfile': 'scripts/diagrams/disaster_recovery_backup.py',
    'desc': 'Ransomware Air-gap Secure Recovery — isolated vault with CyberSense analytics',
    'comp1': 'Vault Appliance      — air-gapped PowerStore/DD in isolated network segment',
    'comp2': 'CyberSense Engine    — ML-based malware and corruption detection on vault data',
    'comp3': 'PowerProtect Manager — orchestrates replication jobs, retention, and recovery',
    'comp4': 'Vault Lock           — immutable WORM lock applied after each replication cycle',
    'comp5': 'Clean Room           — isolated vCenter + workstations for validated recovery',
    'cmd1': 'cr_vault_cli sync', 'cmd2': 'cr_vault_cli status', 'cmd3': 'cybersense scan',
    'cmd4': 'vault lock / unlock', 'cmd5': 'ppdm recover vm',
    'port1': '443 (PPDM REST API)', 'port2': '2049 (NFS vault)', 'port3': '9080 (CyberSense)',
    'auth': 'Vault operator role; 2-person integrity for unlock; AD integration for PPDM UI',
    'enc': 'AES-256 at rest on vault; TLS 1.3 for all management; vault lock enforces immutability',
    'phys': 'Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts',
    'terms': [
      ('RASR',          'Ransomware Air-gap Secure Recovery; full workflow from detection to clean restore'),
      ('Vault',         'isolated, air-gapped storage appliance receiving periodic replication copies'),
      ('Vault Lock',    'WORM lock applied after sync; prevents modification or deletion of vault copies'),
      ('CyberSense',    'ML analytics engine scanning vault data for corruption, encryption signatures'),
      ('PPDM',         'PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'),
      ('Air Gap',       'physical or logical network isolation preventing attacker lateral movement to vault'),
      ('Delta Set',     'incremental changed blocks replicated from production to vault each cycle'),
      ('Clean Room',    'isolated recovery environment: separate vCenter, network, and workstations'),
      ('Recovery Point','specific vault snapshot timestamp from which clean recovery is performed'),
      ('Integrity Lock','two-person authorization required to open vault; prevents insider unlock attacks'),
      ('Journal',       'write-order-consistent journal on vault enabling point-in-time recovery'),
      ('Scan Report',   'CyberSense output: clean/suspect classification per file and block'),
      ('Retention',     'vault copy lifespan; typically 30–90 days of daily snapshots kept'),
      ('RTO',           'Recovery Time Objective; time from failover decision to restored service'),
    ],
    'issues': [
      ('Sync failed',     'vault unreachable',     'check airgap switch',    'verify VLAN path',  'ping vault mgmt'),
      ('Lock error',      'vault already locked',  'cr_vault_cli status',    'force unlock+relock','vault logs'),
      ('CyberSense hang', 'scan job stalled',      'cs_diag collect',        'restart cs service','cs_status'),
      ('Restore fail',    'clean room nic error',  'check clean-room vlan',  're-map portgroup',  'vmnic check'),
    ],
  },

  'recoverpoint': {
    'name': 'Dell RecoverPoint for VMs', 'short': 'RecoverPoint',
    'tag': 'dr-recoverpoint', 'path': 'docs/disaster-recovery/recoverpoint',
    'outfile': 'scripts/diagrams/disaster_recovery_replication.py',
    'desc': 'Continuous data protection — journal-based replication with any-point-in-time recovery',
    'comp1': 'RPA Cluster       — RecoverPoint Appliance pair; handles replication and journaling',
    'comp2': 'Splitter          — intercepts host writes at array level; sends copies to RPA',
    'comp3': 'Journal           — continuous write-order journal enabling any point-in-time access',
    'comp4': 'Consistency Group — set of volumes protected together in crash-consistent writes',
    'comp5': 'Bookmark          — named point in journal for DR testing or scheduled recovery',
    'cmd1': 'get all cgs', 'cmd2': 'set group / set bookmark', 'cmd3': 'image access enable/disable',
    'cmd4': 'failover / reverse', 'cmd5': 'get compression stats',
    'port1': '443 (mgmt HTTPS)', 'port2': '2222 (RPA SSH)', 'port3': '8888 (splitter API)',
    'auth': 'RPA admin / monitor roles; LDAP integration; certificate-based inter-RPA auth',
    'enc': 'AES-256 WAN compression+encryption; data at rest on journal volumes unencrypted by default',
    'phys': 'RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites',
    'terms': [
      ('RPA',              'RecoverPoint Appliance — virtual appliance managing journal and replication'),
      ('Splitter',         'intercepts host I/O at hypervisor or array level; sends copy to RPA'),
      ('Journal',          'write-order-consistent storage capturing all writes for point-in-time access'),
      ('Consistency Group','set of volumes protected together; writes are applied in order across all'),
      ('Bookmark',         'named marker in journal; enables deterministic recovery to a known state'),
      ('Image Access',     'mounting a journal point-in-time image to a host for testing or recovery'),
      ('Failover',         'activating the replica at the recovery site; breaks replication relationship'),
      ('Test Copy',        'non-disruptive image access for validation without breaking replication'),
      ('RPO',              'Recovery Point Objective; how much data loss is acceptable; CDP = near-zero'),
      ('RTO',              'Recovery Time Objective; time from failover to service restored'),
      ('Reverse',          'after failover, replicates from recovery site back to re-sync production'),
      ('Splitter Lag',     'delay between host write and journal commit; monitor for replication health'),
      ('CDP',              'Continuous Data Protection; every write journaled, not just scheduled snaps'),
      ('Distributed CG',   'consistency group spanning volumes on multiple storage arrays'),
    ],
    'issues': [
      ('High lag',         'WAN congestion',       'get compression stats',  'throttle or upgrade WAN', 'get all rpas'),
      ('CG suspended',     'journal full',          'check journal capacity',  'expand journal vol',    'get journal stats'),
      ('Splitter offline', 'ESXi host restart',     'vSphere events log',      're-register splitter',  'get splitter info'),
      ('Image stuck',      'stale image access',    'image access disable',    'force release',         'get all groups'),
    ],
  },

  'srdf-a': {
    'name': 'Dell EMC SRDF/A', 'short': 'SRDF/A',
    'tag': 'dr-srdf-a', 'path': 'docs/disaster-recovery/srdf-a',
    'outfile': 'scripts/diagrams/disaster_recovery_replication.py',
    'desc': 'Asynchronous replication for PowerMax/VMAX — delta-set cycle-based RPO in seconds',
    'comp1': 'R1 Volume (Source)  — primary data on production PowerMax; host writes here',
    'comp2': 'R2 Volume (Target)  — replica on DR PowerMax; receives delta sets asynchronously',
    'comp3': 'SRDF/A Engine       — delta-set formation: groups writes per cycle, ships to R2',
    'comp4': 'PowerMax Mgmt       — Unisphere for PowerMax; symrdf CLI for failover operations',
    'comp5': 'SRDF Link           — dedicated FC or FCIP channel between R1 and R2 arrays',
    'cmd1': 'symrdf establish', 'cmd2': 'symrdf failover / failback', 'cmd3': 'symrdf query',
    'cmd4': 'symrdf suspend / resume', 'cmd5': 'symrdf verify',
    'port1': 'FC dark fiber / DWDM', 'port2': 'FCIP (TCP 3225)', 'port3': '9443 (Unisphere HTTPS)',
    'auth': 'Symmetrix/PowerMax admin credentials; Solutions Enabler (SYMAPI); role-based Unisphere',
    'enc': 'SRDF encryption at the FA/RF port level; Unisphere HTTPS; SE service TLS',
    'phys': 'Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports',
    'terms': [
      ('SRDF',       'Symmetrix Remote Data Facility; EMC array-based replication technology'),
      ('R1',         'source SRDF volume on production array; host writes flow here'),
      ('R2',         'target SRDF volume on DR array; receives replicated data asynchronously'),
      ('Delta Set',  'batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'),
      ('Cycle Time', 'SRDF/A replication interval (15–60 seconds); determines maximum RPO'),
      ('symrdf',     'Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'),
      ('SRDF Link',  'FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'),
      ('Suspended',  'SRDF pair state where replication is paused; R2 data frozen at last cycle'),
      ('Failover',   'SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'),
      ('Restore',    'after failover resolution, re-establishes replication with R1 as source'),
      ('Establish',  'initial sync or re-sync operation that copies R1 to R2 in full'),
      ('Split',      'breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'),
      ('FCIP',       'Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'),
      ('Unisphere',  'Dell PowerMax management GUI; REST API; array health and provisioning'),
    ],
    'issues': [
      ('High RPO',    'cycle time exceeded',   'symrdf query -cycle',   'increase bandwidth',  'symrdf -v'),
      ('Link down',   'RF port failure',       'symrdf query state',    'failover ports',      'symcfg list -rdfg'),
      ('Pair invalid','R1/R2 mismatch',        'symrdf verify',         're-establish pair',   'symrdf establish'),
      ('Failover fail','R2 not ready',          'check R2 state',        'split then failover', 'symrdf -sid'),
    ],
  },

  'srdf-s': {
    'name': 'Dell EMC SRDF/S', 'short': 'SRDF/S',
    'tag': 'dr-srdf-s', 'path': 'docs/disaster-recovery/srdf-s',
    'outfile': 'scripts/diagrams/disaster_recovery_replication.py',
    'desc': 'Synchronous replication for PowerMax/VMAX — RPO=0, write not acknowledged until R2 confirms',
    'comp1': 'R1 Volume (Source)  — production PowerMax; write holds until R2 acknowledges',
    'comp2': 'R2 Volume (Target)  — DR PowerMax; must confirm write before host I/O completes',
    'comp3': 'SRDF/S Engine       — synchronous write mirroring; adds WAN RTT to write latency',
    'comp4': 'PowerMax Mgmt       — Unisphere + symrdf; failover/failback orchestration',
    'comp5': 'SRDF Link           — ultra-low-latency FC/dark-fiber; RTT budget typically <5 ms',
    'cmd1': 'symrdf establish -type s', 'cmd2': 'symrdf failover', 'cmd3': 'symrdf query',
    'cmd4': 'symrdf -rdfg list', 'cmd5': 'symrdf restore',
    'port1': 'Dark fiber FC (< 5 ms RTT)', 'port2': 'DWDM long-haul FC', 'port3': '9443 (Unisphere)',
    'auth': 'Symmetrix admin credentials; Solutions Enabler; Unisphere role-based access',
    'enc': 'Data identical to R1 at R2; FA port encryption optional; Unisphere TLS/HTTPS',
    'phys': 'Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports',
    'terms': [
      ('SRDF/S',       'Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'),
      ('R1',           'source volume; write is held pending R2 confirmation — adds WAN RTT to latency'),
      ('R2',           'target volume; must acknowledge each write; acts as synchronous mirror'),
      ('RTT',          'Round-Trip Time between R1 and R2 arrays; directly added to host write latency'),
      ('RPO=0',        'zero recovery point objective; no data loss possible under normal operation'),
      ('RTO',          'Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min auto'),
      ('symrdf',       'CLI for all SRDF operations: establish, split, suspend, failover, restore, verify'),
      ('Pair State',   'Synchronized | Consistent | Suspended | Failed Over | Split'),
      ('Consistent',   'transient state where R1 write is in transit but not yet confirmed on R2'),
      ('Failover',     'makes R2 read-write; production continues from DR site after R1 failure'),
      ('Restore',      're-synchronises after failover; direction is reversed until R1 catches up'),
      ('RDFG',         'RDF Group: logical grouping of SRDF pairs sharing same link and parameters'),
      ('FA Port',      'Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'),
      ('RF Port',      'Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'),
    ],
    'issues': [
      ('Write latency', 'RTT > budget',           'symrdf query -perf',     'distance / bandwidth',  'symstat'),
      ('Pair Consistent','transient congestion',  'symrdf query',            'monitor; usually clears','symrdf -v'),
      ('Link failure',   'RF port down',          'symcfg list -rdfg',       'failover immediately',  'symrdf failover'),
      ('R2 not ready',   'array fault',           'check R2 Unisphere',      'fix array, re-establish','symrdf establish'),
    ],
  },

  'srm': {
    'name': 'VMware Site Recovery Manager', 'short': 'SRM',
    'tag': 'dr-srm', 'path': 'docs/disaster-recovery/srm',
    'outfile': 'scripts/diagrams/disaster_recovery_replication.py',
    'desc': 'VMware DR orchestration — protection groups, recovery plans, automated failover/failback',
    'comp1': 'SRM Server (Protected) — vCenter plugin at production site; manages protection groups',
    'comp2': 'SRM Server (Recovery)  — vCenter plugin at DR site; runs recovery plans',
    'comp3': 'SRA (Storage Replication Adapter) — translates SRM calls to array replication commands',
    'comp4': 'Protection Group      — set of VMs protected together; maps to replication group',
    'comp5': 'Recovery Plan         — ordered steps: pre-scripts, VM power-on, IP remap, post-scripts',
    'cmd1': 'srm-cli vm list', 'cmd2': 'srm-cli recovery run', 'cmd3': 'srm-cli plan test',
    'cmd4': 'srm-cli pg list', 'cmd5': 'srm-cli history',
    'port1': '443 (SRM HTTPS)', 'port2': '9086 (SRM-SRM pairing)', 'port3': '443 (vCenter)',
    'auth': 'vCenter SSO / AD integration; SRM admin role; site-pairing certificate exchange',
    'enc': 'SRM management TLS; replication encryption controlled by array/SRA layer',
    'phys': 'Two vCenter instances (protected + recovery site) · SRA installed on SRM server · Array replication link',
    'terms': [
      ('SRM',              'Site Recovery Manager; VMware product for DR orchestration and testing'),
      ('SRA',              'Storage Replication Adapter; plugin linking SRM to specific array replication'),
      ('Protection Group', 'logical grouping of VMs covered by a single replication consistency group'),
      ('Recovery Plan',    'automated DR runbook: power-off order, datastore failover, IP customization'),
      ('IP Customization', 'per-VM network settings applied at recovery site (different subnet/gateway)'),
      ('Test Failover',    'non-disruptive plan validation using snapshot; production unaffected'),
      ('Planned Migration','graceful workload movement; VMs shutdown at protected, started at recovery'),
      ('Emergency Failover','disaster scenario; VMs powered on from latest available replica'),
      ('Failback',         'after recovery, re-protect VMs and migrate back to production site'),
      ('Re-protect',       'reverses replication direction; DR site becomes new protected site'),
      ('Recovery Point',   'specific replication snapshot used for VM recovery; RPO = interval'),
      ('vCenter Pair',     'SRM connection between two vCenter instances enables cross-site orchestration'),
      ('Startup Priority', 'ordering within recovery plan; lower number = powers on first'),
      ('Site Pair',        'trust relationship between protected and recovery SRM servers'),
    ],
    'issues': [
      ('Plan fails', 'SRA timeout',           'check array replication',   're-run or fix SRA',    'srm-cli history'),
      ('VM no IP',   'customization error',   'check IP customization',    'fix NIC mapping',      'vmware.log'),
      ('Test stuck',  'snapshot not released', 'srm cleanup',              'force cleanup',         'srm-cli cleanup'),
      ('Pair broken', 'cert mismatch',         'check SRM pairing cert',    're-pair sites',         'srm-cli site info'),
    ],
  },

  'superna-eyeglass': {
    'name': 'Superna Eyeglass', 'short': 'Superna Eyeglass',
    'tag': 'dr-superna', 'path': 'docs/disaster-recovery/superna-eyeglass',
    'outfile': 'scripts/diagrams/disaster_recovery_replication.py',
    'desc': 'NAS DR and ransomware protection for Dell PowerScale — SyncIQ integration and failover automation',
    'comp1': 'Eyeglass Appliance   — VM monitoring PowerScale clusters; REST API-driven',
    'comp2': 'RAPA Engine          — Ransomware Protection with Automated Response; quarantine on detect',
    'comp3': 'DFS Namespace Mgr    — Windows DFS-N failover automation; transparent client redirect',
    'comp4': 'Sync Jobs            — configuration replication: shares, exports, quotas between clusters',
    'comp5': 'DR Assistant         — guided failover workflow: pre-checks, failover, validation steps',
    'cmd1': 'igls quota list', 'cmd2': 'igls dr runbook', 'cmd3': 'igls sync status',
    'cmd4': 'igls rapa status', 'cmd5': 'igls failover start',
    'port1': '443 (Eyeglass web UI)', 'port2': '8080 (REST API)', 'port3': '8116 (Isilon/PowerScale mgmt)',
    'auth': 'Eyeglass admin roles; PowerScale admin credentials; AD integration for DFS-N management',
    'enc': 'HTTPS/TLS for all management; SyncIQ data replication encryption (AES-256 in transit)',
    'phys': 'ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link',
    'terms': [
      ('Eyeglass',     'Superna Eyeglass; software appliance for NAS DR and ransomware protection'),
      ('RAPA',         'Ransomware Protection with Automated Response; detects and quarantines threats'),
      ('SyncIQ',       'PowerScale built-in replication; Eyeglass monitors and orchestrates policies'),
      ('DFS-N',        'Windows Distributed File System Namespace; Eyeglass automates failover of DFS targets'),
      ('Failover',     'Eyeglass-orchestrated shift of NAS access from production to DR cluster'),
      ('Failback',     'reversing failover; Eyeglass re-syncs DR changes back and cuts back to production'),
      ('Quota Sync',   'Eyeglass replicates SmartQuotas from source to DR to preserve user limits'),
      ('Export Sync',  'NFS exports and SMB shares replicated so clients can reconnect at DR site'),
      ('Quarantine',   'RAPA isolation of suspect directory; blocks writes, alerts ops team'),
      ('Shadow Copy',  'Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS shares'),
      ('Runbook',      'Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'),
      ('igls',         'Eyeglass CLI; used for status, sync, DR, and RAPA operations'),
      ('SmartConnect', 'PowerScale DNS load balancing; failover changes SmartConnect zone delegation'),
      ('Configuration','shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'),
    ],
    'issues': [
      ('Sync lag',      'SyncIQ policy slow',    'igls sync status',       'check bandwidth',       'isi sync policy'),
      ('RAPA alert',    'ransomware detected',   'igls rapa status',       'quarantine + escalate', 'rapa report'),
      ('DFS broken',    'namespace not updated', 'igls dfs status',        'retry DFS update',      'dfsutil view'),
      ('Failover fail', 'pre-check error',       'igls dr precheck',       'fix issue + re-run',    'igls log'),
    ],
  },

  'veeam': {
    'name': 'Veeam Backup & Replication', 'short': 'Veeam',
    'tag': 'dr-veeam', 'path': 'docs/disaster-recovery/veeam',
    'outfile': 'scripts/diagrams/disaster_recovery_replication.py',
    'desc': 'VM backup and DR — agentless VMware/Hyper-V backup with instant recovery and replication',
    'comp1': 'Veeam Backup Server — scheduler, job engine, catalog, REST API (port 9419)',
    'comp2': 'Backup Proxy        — data mover; VMware VADP for CBT snapshots; SAN/NAS/LAN modes',
    'comp3': 'Backup Repository   — target storage: SOBR, CIFS/NFS, S3 object, dedup appliance',
    'comp4': 'Mount Server        — used for instant VM recovery; presents backup as vSphere datastore',
    'comp5': 'Veeam ONE           — optional monitoring: job success rate, capacity, compliance reports',
    'cmd1': 'Add-VBRJob / Start-VBRJob', 'cmd2': 'Get-VBRRestorePoint', 'cmd3': 'Start-VBRInstantVMRecovery',
    'cmd4': 'Get-VBRJob | fl', 'cmd5': 'Invoke-VBRHealthCheck',
    'port1': '9419 (Veeam REST API)', 'port2': '6160 (Veeam Agent)', 'port3': '443 (vCenter)',
    'auth': 'Windows/AD auth for Veeam console; service account with vSphere admin; repo credentials',
    'enc': 'AES-256 backup encryption (key stored in Veeam config DB); TLS on all management; WORM repos',
    'phys': 'Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN',
    'terms': [
      ('Backup Server',    'central Veeam component: scheduler, job engine, catalog, REST API'),
      ('Backup Proxy',     'data mover between vSphere and repository; runs in virtual-appliance mode or HotAdd'),
      ('CBT',             'Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'),
      ('VADP',            'VMware vSphere APIs for Data Protection; enables agentless VM backup'),
      ('SOBR',            'Scale-Out Backup Repository; tiers extents; moves cold data to object storage'),
      ('Instant Recovery', 'mounts VM disks from backup directly to ESXi; VM live in seconds'),
      ('SureBackup',       'automated backup verification; test-restores VM in isolated virtual lab'),
      ('Replication',      'creates VM replica at DR site; enables failover without full restore time'),
      ('GFS Retention',    'Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'),
      ('Immutable Repo',   'object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protection'),
      ('Mount Server',     'Windows host presenting backup as iSCSI/NFS datastore for instant recovery'),
      ('VeeamZIP',         'ad-hoc compressed portable backup of a single VM; no job required'),
      ('Health Check',     'periodic backup integrity scan; verifies restore points are readable'),
      ('Forward Incremental','default mode; one full + daily incrementals; synthetic full created periodically'),
    ],
    'issues': [
      ('Snapshot not released', 'proxy error mid-job',   'check proxy logs',       'run snapshot cleanup',  'Get-VBRJob'),
      ('CBT reset',             'VMware tools update',   'rescan VM disks',         'force full backup',     'Reset-VBRVMCBTData'),
      ('Repo full',             'retention not deleting', 'check GFS config',       'expire old points',     'Remove-VBRBackup'),
      ('Instant recovery slow', 'NFS mount latency',     'check mount server NIC',  'migrate to datastore',  'veeam log'),
    ],
  },
}

# ── DR misc pages ────────────────────────────────────────────────────────────

DR_MISC = [
  ('dr-root',        'docs/disaster-recovery/index.md',
   'Disaster Recovery — overview of all DR tools, replication methods, and recovery procedures'),
  ('dr-failover',    'docs/disaster-recovery/failover-procedure/index.md',
   'DR Failover Procedure — declare disaster, activate DR site, redirect hosts, validate'),
  ('dr-failback',    'docs/disaster-recovery/failback-procedure/index.md',
   'DR Failback Procedure — reverse replicate, re-sync, validate, cut back to production'),
  ('dr-runbook',     'docs/disaster-recovery/runbook/index.md',
   'DR Runbook — pre-defined response steps for declared disaster across all DR tools'),
  ('dr-ire',         'docs/disaster-recovery/isolated-recovery-environment-ire/index.md',
   'Isolated Recovery Environment — air-gapped clean-room for ransomware recovery'),
  ('dr-ire-cleanroom','docs/disaster-recovery/isolated-recovery-environment-ire/clean-room/index.md',
   'IRE Clean Room — isolated ESXi + vCenter + workstations for validated recovery'),
  ('dr-ire-isolation','docs/disaster-recovery/isolated-recovery-environment-ire/isolation/index.md',
   'IRE Network Isolation — air-gap switch config, VLAN separation, no production routes'),
  ('dr-ire-restore', 'docs/disaster-recovery/isolated-recovery-environment-ire/restore/index.md',
   'IRE Restore — step-by-step clean restore from vault to clean-room environment'),
  ('dr-ire-security','docs/disaster-recovery/isolated-recovery-environment-ire/security/index.md',
   'IRE Security — access control, two-person integrity, audit logging in the vault'),
  ('dr-ire-validation','docs/disaster-recovery/isolated-recovery-environment-ire/validation/index.md',
   'IRE Validation — application testing, data integrity checks, sign-off before cutback'),
]

# ── Standard sub-page types ──────────────────────────────────────────────────

STD_PAGES = [
  ('index',             '',                         'index.md'),
  ('architecture',      'architecture/',            'index.md'),
  ('arch-how',          'architecture/how-it-works/','index.md'),
  ('arch-design',       'architecture/design-standards/','index.md'),
  ('arch-integrations', 'architecture/integrations/','index.md'),
  ('operations',        'operations/',              'index.md'),
  ('ops-backup',        'operations/backup-restore/','index.md'),
  ('ops-cli',           'operations/cli-reference/','index.md'),
  ('ops-health',        'operations/health-checks/','index.md'),
  ('ops-install',       'operations/install-upgrade/','index.md'),
  ('ops-procedures',    'operations/procedures/',   'index.md'),
  ('ops-scripts',       'operations/scripts/',      'index.md'),
  ('security',          'security/',                'index.md'),
  ('sec-access',        'security/access-control/', 'index.md'),
  ('sec-auth',          'security/authentication/', 'index.md'),
  ('sec-enc',           'security/encryption/',     'index.md'),
  ('sec-hardening',     'security/hardening/',      'index.md'),
  ('troubleshooting',   'troubleshooting/',         'index.md'),
  ('ts-issues',         'troubleshooting/common-issues/','index.md'),
  ('ts-diag',           'troubleshooting/diagnostics/','index.md'),
  ('ts-escalation',     'troubleshooting/escalation/','index.md'),
]

# pages that only have security + troubleshooting remaining
REMAINING_PAGES = [
  ('security',          'security/',                'index.md'),
  ('sec-access',        'security/access-control/', 'index.md'),
  ('sec-auth',          'security/authentication/', 'index.md'),
  ('sec-enc',           'security/encryption/',     'index.md'),
  ('sec-hardening',     'security/hardening/',      'index.md'),
  ('troubleshooting',   'troubleshooting/',         'index.md'),
  ('ts-issues',         'troubleshooting/common-issues/','index.md'),
  ('ts-diag',           'troubleshooting/diagnostics/','index.md'),
  ('ts-escalation',     'troubleshooting/escalation/','index.md'),
]

# ── Template builders ─────────────────────────────────────────────────────────

def q(s):
    """Escape single quotes for Python string literals."""
    return s.replace("'", "\\'")

def center_pad(text, width):
    """Ensure text fits within width; truncate if needed."""
    if len(text) > width:
        text = text[:width-1]
    return text

def fn_body(p, page_type):
    """Return the body of a diagram function for product p and page_type suffix."""
    tag = p['tag']
    path = p['path']
    short = p['short']

    if page_type == 'index':
        key  = tag
        file = f"{path}/index.md"
        desc = p['desc']
        title = f"{short} — Overview"
        fn   = f"def _{tag.replace('-','_')}_overview():"
        body = _overview(p)

    elif page_type == 'architecture':
        key  = f"{tag}-architecture"
        file = f"{path}/architecture/index.md"
        desc = f"{short} — architecture overview, components, data flow"
        title = f"{short} — Architecture"
        fn   = f"def _{tag.replace('-','_')}_architecture():"
        body = _architecture(p)

    elif page_type == 'arch-how':
        key  = f"{tag}-arch-how-it-works"
        file = f"{path}/architecture/how-it-works/index.md"
        desc = f"{short} — how replication or backup data flows step by step"
        title = f"{short} — How It Works"
        fn   = f"def _{tag.replace('-','_')}_arch_how():"
        body = _arch_how(p)

    elif page_type == 'arch-design':
        key  = f"{tag}-arch-design"
        file = f"{path}/architecture/design-standards/index.md"
        desc = f"{short} — sizing, design rules, capacity, HA guidelines"
        title = f"{short} — Design Standards"
        fn   = f"def _{tag.replace('-','_')}_arch_design():"
        body = _arch_design(p)

    elif page_type == 'arch-integrations':
        key  = f"{tag}-arch-integrations"
        file = f"{path}/architecture/integrations/index.md"
        desc = f"{short} — integration points with external systems and APIs"
        title = f"{short} — Architecture Integrations"
        fn   = f"def _{tag.replace('-','_')}_arch_integrations():"
        body = _arch_integrations(p)

    elif page_type == 'operations':
        key  = f"{tag}-operations"
        file = f"{path}/operations/index.md"
        desc = f"{short} — operations overview, key tasks, day-to-day procedures"
        title = f"{short} — Operations"
        fn   = f"def _{tag.replace('-','_')}_operations():"
        body = _operations(p)

    elif page_type == 'ops-backup':
        key  = f"{tag}-ops-backup"
        file = f"{path}/operations/backup-restore/index.md"
        desc = f"{short} — backup and restore procedures"
        title = f"{short} — Backup & Restore"
        fn   = f"def _{tag.replace('-','_')}_ops_backup():"
        body = _ops_backup(p)

    elif page_type == 'ops-cli':
        key  = f"{tag}-ops-cli"
        file = f"{path}/operations/cli-reference/index.md"
        desc = f"{short} — CLI commands reference"
        title = f"{short} — CLI Reference"
        fn   = f"def _{tag.replace('-','_')}_ops_cli():"
        body = _ops_cli(p)

    elif page_type == 'ops-health':
        key  = f"{tag}-ops-health"
        file = f"{path}/operations/health-checks/index.md"
        desc = f"{short} — health check procedures and monitoring commands"
        title = f"{short} — Health Checks"
        fn   = f"def _{tag.replace('-','_')}_ops_health():"
        body = _ops_health(p)

    elif page_type == 'ops-install':
        key  = f"{tag}-ops-install"
        file = f"{path}/operations/install-upgrade/index.md"
        desc = f"{short} — install and upgrade procedures"
        title = f"{short} — Install & Upgrade"
        fn   = f"def _{tag.replace('-','_')}_ops_install():"
        body = _ops_install(p)

    elif page_type == 'ops-procedures':
        key  = f"{tag}-ops-procedures"
        file = f"{path}/operations/procedures/index.md"
        desc = f"{short} — operational procedures and runbooks"
        title = f"{short} — Procedures"
        fn   = f"def _{tag.replace('-','_')}_ops_procedures():"
        body = _ops_procedures(p)

    elif page_type == 'ops-scripts':
        key  = f"{tag}-ops-scripts"
        file = f"{path}/operations/scripts/index.md"
        desc = f"{short} — automation scripts and examples"
        title = f"{short} — Scripts"
        fn   = f"def _{tag.replace('-','_')}_ops_scripts():"
        body = _ops_scripts(p)

    elif page_type == 'security':
        key  = f"{tag}-security"
        file = f"{path}/security/index.md"
        desc = f"{short} — security overview, controls, compliance posture"
        title = f"{short} — Security"
        fn   = f"def _{tag.replace('-','_')}_security():"
        body = _security(p)

    elif page_type == 'sec-access':
        key  = f"{tag}-sec-access"
        file = f"{path}/security/access-control/index.md"
        desc = f"{short} — RBAC, permissions, service accounts"
        title = f"{short} — Access Control"
        fn   = f"def _{tag.replace('-','_')}_sec_access():"
        body = _sec_access(p)

    elif page_type == 'sec-auth':
        key  = f"{tag}-sec-auth"
        file = f"{path}/security/authentication/index.md"
        desc = f"{short} — authentication methods, certificate management"
        title = f"{short} — Authentication"
        fn   = f"def _{tag.replace('-','_')}_sec_auth():"
        body = _sec_auth(p)

    elif page_type == 'sec-enc':
        key  = f"{tag}-sec-enc"
        file = f"{path}/security/encryption/index.md"
        desc = f"{short} — encryption at rest and in transit"
        title = f"{short} — Encryption"
        fn   = f"def _{tag.replace('-','_')}_sec_enc():"
        body = _sec_enc(p)

    elif page_type == 'sec-hardening':
        key  = f"{tag}-sec-hardening"
        file = f"{path}/security/hardening/index.md"
        desc = f"{short} — hardening guide, CIS controls, secure configuration"
        title = f"{short} — Hardening"
        fn   = f"def _{tag.replace('-','_')}_sec_hardening():"
        body = _sec_hardening(p)

    elif page_type == 'troubleshooting':
        key  = f"{tag}-troubleshooting"
        file = f"{path}/troubleshooting/index.md"
        desc = f"{short} — troubleshooting overview and triage approach"
        title = f"{short} — Troubleshooting"
        fn   = f"def _{tag.replace('-','_')}_troubleshooting():"
        body = _troubleshooting(p)

    elif page_type == 'ts-issues':
        key  = f"{tag}-ts-issues"
        file = f"{path}/troubleshooting/common-issues/index.md"
        desc = f"{short} — common issues, root causes, and fixes"
        title = f"{short} — Common Issues"
        fn   = f"def _{tag.replace('-','_')}_ts_issues():"
        body = _ts_issues(p)

    elif page_type == 'ts-diag':
        key  = f"{tag}-ts-diag"
        file = f"{path}/troubleshooting/diagnostics/index.md"
        desc = f"{short} — diagnostic commands and log collection"
        title = f"{short} — Diagnostics"
        fn   = f"def _{tag.replace('-','_')}_ts_diag():"
        body = _ts_diag(p)

    elif page_type == 'ts-escalation':
        key  = f"{tag}-ts-escalation"
        file = f"{path}/troubleshooting/escalation/index.md"
        desc = f"{short} — escalation path, vendor support, and SLA"
        title = f"{short} — Escalation"
        fn   = f"def _{tag.replace('-','_')}_ts_escalation():"
        body = _ts_escalation(p)

    else:
        return ''

    lines = [
        '',
        f"@kb_diagram(",
        f"    '{key}',",
        f"    '{file}',",
        f"    '{q(desc)}',",
        f")",
        fn,
        f"    W2 = 103",
        f"    R, txt_row = make_helpers(W2)",
        f"    lines = []",
    ]
    lines += body
    lines += [
        f"    lines.append('\\u2514' + '\\u2500' * W2 + '\\u2518')",
        f"    return lines",
    ]
    return '\n'.join(lines)


# ── Page type template functions ─────────────────────────────────────────────

def _make_term_rows(terms):
    """Generate glossary txt_row lines from term list."""
    rows = ["    lines.append(txt_row('Key terms:'))", "    lines.append(txt_row())"]
    for term, defn in terms:
        label = f"{term:<14}"
        entry = f"= {defn}"
        full = f"{label}{entry}"
        if len(full) > 95:
            full = full[:94]
        rows.append(f"    lines.append(txt_row('{q(full)}'))")
    rows.append("    lines.append(txt_row())")
    return rows

def _make_phys(phys):
    return [
        "    lines.append(txt_row())",
        f"    lines.append(txt_row('Physical Infrastructure:'))",
        f"    lines.append(txt_row('{q(phys)}'))",
    ]

def _overview(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Overview'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)}')))",
        f"    lines.append(R(bMid(3, 99, '{q(p['desc'][:92])}')))",
        f"    lines.append(R(bMid(3, 99, '{q(p['comp1'][:92])}')))",
        f"    lines.append(R(bMid(3, 99, '{q(p['comp2'][:92])}')))",
        f"    lines.append(R(bMid(3, 99, '{q(p['comp3'][:92])}')))",
        f"    lines.append(R(bMid(3, 99, 'Management: {q(p['port1'])} · Auth: {q(p['auth'][:50])}')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        f"    lines.append(txt_row('  Architecture: components work together to deliver {q(s)} capabilities'))",
        "    lines.append(txt_row())",
        "    lines.append(R(arrow([26, 76])))",
        "    lines.append(txt_row())",
        "    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Architecture'), bMid(53, 99, 'Operations'))))",
        f"    lines.append(R(merge(bMid(3, 50, '{q(p['comp1'][:43])}'), bMid(53, 99, '{q(p['cmd1'][:43])}'))))",
        f"    lines.append(R(merge(bMid(3, 50, '{q(p['comp2'][:43])}'), bMid(53, 99, '{q(p['cmd2'][:43])}'))))",
        f"    lines.append(R(merge(bMid(3, 50, '{q(p['comp3'][:43])}'), bMid(53, 99, '{q(p['cmd3'][:43])}'))))",
        f"    lines.append(R(merge(bMid(3, 50, '{q(p['comp4'][:43])}'), bMid(53, 99, '{q(p['cmd4'][:43])}'))))",
        f"    lines.append(R(merge(bMid(3, 50, '{q(p['comp5'][:43])}'), bMid(53, 99, '{q(p['cmd5'][:43])}'))))",
        "    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _architecture(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Architecture'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — Component Architecture')))",
        f"    lines.append(R(bMid(3, 99, '{q(p['comp1'][:92])}')))",
        f"    lines.append(R(bMid(3, 99, '{q(p['comp2'][:92])}')))",
        f"    lines.append(R(bMid(3, 99, '{q(p['comp3'][:92])}')))",
        f"    lines.append(R(bMid(3, 99, 'Ports: {q(p['port1'])} · {q(p['port2'])} · {q(p['port3'])}')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(txt_row('  Three-tier component model — control plane, data plane, and management'))",
        "    lines.append(txt_row())",
        "    lines.append(R(arrow([26, 51, 76])))",
        "    lines.append(txt_row())",
        "    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Control Plane'), bMid(36, 66, 'Data Plane'), bMid(69, 99, 'Management'))))",
        f"    lines.append(R(merge(bMid(3, 33, '{q(p['comp1'][:28])}'), bMid(36, 66, '{q(p['comp2'][:28])}'), bMid(69, 99, '{q(p['comp4'][:28])}'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Scheduling'), bMid(36, 66, 'Replication/Backup'), bMid(69, 99, '{q(p['port1'][:28])}'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Policy mgmt'), bMid(36, 66, 'Data movement'), bMid(69, 99, 'REST API'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Catalog/DB'), bMid(36, 66, 'Dedup/compress'), bMid(69, 99, 'RBAC'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Job engine'), bMid(36, 66, '{q(p['port2'][:28])}'), bMid(69, 99, 'Alerting'))))",
        "    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _arch_how(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — How It Works'))",
        "    lines.append(txt_row())",
        f"    lines.append(txt_row('  {q(s)} data flow — from source to target through the protection pipeline:'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '1  Source / Production System')))",
        f"    lines.append(R(bMid(3, 99, '   {q(p['comp1'][:88])}')))",
        f"    lines.append(R(bMid(3, 99, '   Host writes are intercepted or snapshotted by the {q(s)} agent/proxy')))",
        f"    lines.append(R(bMid(3, 99, '   Changed blocks tracked via CBT / journal / delta-set mechanism')))",
        f"    lines.append(R(bMid(3, 99, '   Consistency ensured at quiesce point before data transfer begins')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        f"    lines.append(txt_row('  Changed data forwarded to the {q(s)} engine — compression and encryption applied in transit'))",
        "    lines.append(txt_row())",
        "    lines.append(R(arrow([51])))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '2  {q(s)} Engine')))",
        f"    lines.append(R(bMid(3, 99, '   {q(p['comp2'][:88])}')))",
        f"    lines.append(R(bMid(3, 99, '   Data compressed, deduplicated, and encrypted before storage')))",
        f"    lines.append(R(bMid(3, 99, '   Metadata catalog updated; job status reported to control plane')))",
        f"    lines.append(R(bMid(3, 99, '   {q(p['cmd1'][:88])}')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(arrow([51])))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '3  Target / Repository')))",
        f"    lines.append(R(bMid(3, 99, '   {q(p['comp3'][:88])}')))",
        f"    lines.append(R(bMid(3, 99, '   Recovery point written; retention policy applied automatically')))",
        f"    lines.append(R(bMid(3, 99, '   Restore: {q(p['cmd2'][:80])}')))",
        f"    lines.append(R(bMid(3, 99, '   RTO driven by target storage performance and data volume')))",
        "    lines.append(R(bBot(3, 99)))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _arch_design(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Design Standards'))",
        "    lines.append(txt_row())",
        "    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Sizing Guidelines'), bMid(53, 99, 'HA Requirements'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Deduplicate where supported'), bMid(53, 99, 'N+1 component redundancy'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Bandwidth: 10 GbE minimum'), bMid(53, 99, 'Heartbeat / health monitor'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Storage: 130% of raw data'), bMid(53, 99, 'Separate mgmt / data VLANs'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Latency: < 10 ms to storage'), bMid(53, 99, 'Out-of-band access (IPMI)'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'CPU: 8+ vCPU for engine'), bMid(53, 99, 'Anti-affinity VM placement'))))",
        "    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))",
        "    lines.append(txt_row())",
        f"    lines.append(txt_row('  Ports: {q(p['port1'])} · {q(p['port2'])} · {q(p['port3'])}'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, 'Standard {q(s)} Design Rules')))",
        f"    lines.append(R(bMid(3, 99, 'RPO target drives snapshot/cycle frequency — document in service design')))",
        f"    lines.append(R(bMid(3, 99, 'RTO target drives recovery tier: instant, warm standby, or cold restore')))",
        f"    lines.append(R(bMid(3, 99, 'Dedicated backup network VLAN — no shared production traffic')))",
        f"    lines.append(R(bMid(3, 99, 'Encryption enabled on all channels: {q(p['enc'][:70])}')))",
        f"    lines.append(R(bMid(3, 99, 'Service accounts: minimum privilege; rotate credentials quarterly')))",
        "    lines.append(R(bBot(3, 99)))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _arch_integrations(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Architecture Integrations'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — External Integration Points')))",
        f"    lines.append(R(bMid(3, 99, 'Auth: {q(p['auth'][:88])}')))",
        f"    lines.append(R(bMid(3, 99, 'Storage: connected via {q(p['port1'])} · {q(p['port2'])}')))",
        f"    lines.append(R(bMid(3, 99, 'Monitoring: SNMP traps / syslog / REST API to ITSM and alerting systems')))",
        f"    lines.append(R(bMid(3, 99, 'Encryption: {q(p['enc'][:88])}')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(arrow([26, 51, 76])))",
        "    lines.append(txt_row())",
        "    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Identity'), bMid(36, 66, 'Storage'), bMid(69, 99, 'Monitoring'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'AD / LDAP'), bMid(36, 66, '{q(p['port1'][:28])}'), bMid(69, 99, 'SNMP / syslog'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'SAML SSO'), bMid(36, 66, '{q(p['port2'][:28])}'), bMid(69, 99, 'REST webhook'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'RBAC roles'), bMid(36, 66, 'NFS / iSCSI / FC'), bMid(69, 99, 'Email alerts'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'MFA optional'), bMid(36, 66, 'Dedup appliance'), bMid(69, 99, 'ServiceNow'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Cert auth'), bMid(36, 66, 'Object storage'), bMid(69, 99, 'Prometheus'))))",
        "    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _operations(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Operations'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — Day-to-Day Operations')))",
        f"    lines.append(R(bMid(3, 99, 'Daily: review job status · check health alerts · verify last backup/replica')))",
        f"    lines.append(R(bMid(3, 99, 'Weekly: review capacity trends · test restore sample · review error logs')))",
        f"    lines.append(R(bMid(3, 99, 'Monthly: full restore test · review retention · audit service accounts')))",
        f"    lines.append(R(bMid(3, 99, 'Quarterly: DR failover test · firmware review · update documentation')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(arrow([26, 51, 76])))",
        "    lines.append(txt_row())",
        "    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Backup/Replicate'), bMid(36, 66, 'Monitor'), bMid(69, 99, 'Recover'))))",
        f"    lines.append(R(merge(bMid(3, 33, '{q(p['cmd1'][:28])}'), bMid(36, 66, '{q(p['cmd3'][:28])}'), bMid(69, 99, '{q(p['cmd2'][:28])}'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Schedule jobs'), bMid(36, 66, 'Health checks'), bMid(69, 99, 'Instant restore'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Retention mgmt'), bMid(36, 66, 'Capacity alerts'), bMid(69, 99, 'Failover test'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Consistency grp'), bMid(36, 66, 'Log review'), bMid(69, 99, 'DR runbook'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Policy updates'), bMid(36, 66, 'SLA tracking'), bMid(69, 99, 'Validate RTO'))))",
        "    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _ops_backup(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Backup & Restore'))",
        "    lines.append(txt_row())",
        f"    lines.append(txt_row('  Backup flow: quiesce source → snapshot/copy → transfer → write to target → catalog'))",
        "    lines.append(txt_row())",
        "    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Backup (Protection)'), bMid(53, 99, 'Restore (Recovery)'))))",
        f"    lines.append(R(merge(bMid(3, 50, '{q(p['cmd1'][:43])}'), bMid(53, 99, '{q(p['cmd2'][:43])}'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Quiesce source I/O'), bMid(53, 99, 'Select recovery point'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Take snapshot / CBT'), bMid(53, 99, 'Mount or copy to target'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Transfer changed blocks'), bMid(53, 99, 'Validate integrity'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Commit to repository'), bMid(53, 99, 'Restart application'))))",
        "    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, 'Key {q(s)} Commands')))",
        f"    lines.append(R(bMid(3, 99, '  Backup trigger  : {q(p['cmd1'][:80])}')))",
        f"    lines.append(R(bMid(3, 99, '  List points     : {q(p['cmd2'][:80])}')))",
        f"    lines.append(R(bMid(3, 99, '  Health status   : {q(p['cmd3'][:80])}')))",
        f"    lines.append(R(bMid(3, 99, '  Retention mgmt  : {q(p['cmd5'][:80])}')))",
        "    lines.append(R(bBot(3, 99)))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _ops_cli(p):
    s = p['short']
    cmds = [p['cmd1'], p['cmd2'], p['cmd3'], p['cmd4'], p['cmd5']]
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — CLI Reference'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — Command Reference')))",
        f"    lines.append(R(bMid(3, 99, 'Use these commands for routine operations, scripting, and troubleshooting')))",
    ]
    for cmd in cmds:
        rows.append(f"    lines.append(R(bMid(3, 99, '  {q(cmd[:90])}')))")
    rows += [
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        f"    lines.append(txt_row('  Ports: {q(p['port1'])} · {q(p['port2'])} · {q(p['port3'])}'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, 'Command Categories')))",
        f"    lines.append(R(bMid(3, 99, '  Status / Query  — check current state, list jobs, show config')))",
        f"    lines.append(R(bMid(3, 99, '  Operations      — start, stop, failover, restore, sync, expire')))",
        f"    lines.append(R(bMid(3, 99, '  Configuration   — add/modify policies, schedules, storage targets')))",
        f"    lines.append(R(bMid(3, 99, '  Diagnostics     — collect logs, run health checks, test connectivity')))",
        f"    lines.append(R(bMid(3, 99, '  Scripting       — REST API or CLI for automation and reporting')))",
        "    lines.append(R(bBot(3, 99)))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _ops_health(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Health Checks'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — Health Check Procedures')))",
        f"    lines.append(R(bMid(3, 99, 'Run these checks daily/weekly to confirm protection is working')))",
        f"    lines.append(R(bMid(3, 99, '  {q(p['cmd3'][:88])}')))",
        f"    lines.append(R(bMid(3, 99, '  Review job completion rate — target 100%; investigate failures')))",
        f"    lines.append(R(bMid(3, 99, '  Check replication/backup lag against RPO target')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(sections(3, 99, [22, 41, 61, 80],",
        f"        ['Check', 'What to verify', 'Expected', 'Frequency', 'Action if bad'])))",
        "    lines.append(R(sections(3, 99, [22, 41, 61, 80],",
        f"        ['Job status', 'All jobs complete', '100% success', 'Daily', 'Triage failures'])))",
        "    lines.append(R(sections(3, 99, [22, 41, 61, 80],",
        f"        ['Lag / RPO', 'Replication lag', '< RPO target', 'Daily', 'Tune bandwidth'])))",
        "    lines.append(R(sections(3, 99, [22, 41, 61, 80],",
        f"        ['Capacity', 'Repo space used', '< 80% full', 'Weekly', 'Expand or expire'])))",
        "    lines.append(R(sections(3, 99, [22, 41, 61, 80],",
        f"        ['Restore test', 'Random restore', 'Data intact', 'Monthly', 'Fix backup chain'])))",
        "    lines.append(R(bBot(3, 99)))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _ops_install(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Install & Upgrade'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — Installation Prerequisites')))",
        f"    lines.append(R(bMid(3, 99, '  OS: supported Linux or Windows Server (see vendor compatibility matrix)')))",
        f"    lines.append(R(bMid(3, 99, '  Network: {q(p['port1'])} · {q(p['port2'])} — ensure firewall allows these')))",
        f"    lines.append(R(bMid(3, 99, '  Auth: {q(p['auth'][:88])}')))",
        f"    lines.append(R(bMid(3, 99, '  Storage: {q(p['phys'][:88])}')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(arrow([51])))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, 'Install Sequence')))",
        f"    lines.append(R(bMid(3, 99, '  1  Deploy control plane component and configure network access')))",
        f"    lines.append(R(bMid(3, 99, '  2  Configure storage and network connectivity')))",
        f"    lines.append(R(bMid(3, 99, '  3  Install agent/proxy/splitter on protected hosts')))",
        f"    lines.append(R(bMid(3, 99, '  4  Register sources and configure protection policies')))",
        f"    lines.append(R(bMid(3, 99, '  5  Run first job; verify completion; test restore')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, 'Upgrade Sequence')))",
        f"    lines.append(R(bMid(3, 99, '  1  Review release notes and compatibility matrix before upgrade')))",
        f"    lines.append(R(bMid(3, 99, '  2  Snapshot or backup the control plane VM before upgrading')))",
        f"    lines.append(R(bMid(3, 99, '  3  Upgrade control plane first, then proxies/agents/appliances')))",
        f"    lines.append(R(bMid(3, 99, '  4  Validate jobs resume automatically after upgrade')))",
        f"    lines.append(R(bMid(3, 99, '  5  Document version change and update CMDB record')))",
        "    lines.append(R(bBot(3, 99)))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _ops_procedures(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Procedures'))",
        "    lines.append(txt_row())",
        "    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Routine Procedures'), bMid(53, 99, 'DR Procedures'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Add new protection source'), bMid(53, 99, 'Initiate failover'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Modify retention policy'), bMid(53, 99, 'Validate replica'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Expire old recover points'), bMid(53, 99, 'Redirect host I/O'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Add storage capacity'), bMid(53, 99, 'Test failover (non-disrupt)'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Service account rotation'), bMid(53, 99, 'Failback to production'))))",
        "    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, 'Change Control Requirements for {q(s)}')))",
        f"    lines.append(R(bMid(3, 99, '  All changes to protection policies require change ticket with rollback plan')))",
        f"    lines.append(R(bMid(3, 99, '  Failover tests must be scheduled in maintenance window')))",
        f"    lines.append(R(bMid(3, 99, '  Firmware/software upgrades need 48 h pre-approval and backup snapshot')))",
        f"    lines.append(R(bMid(3, 99, '  Post-change: verify jobs run successfully for 2 backup cycles')))",
        "    lines.append(R(bBot(3, 99)))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _ops_scripts(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Scripts'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — Automation Scripts')))",
        f"    lines.append(R(bMid(3, 99, 'Scripts automate routine {q(s)} operations — run via cron or CI/CD')))",
        f"    lines.append(R(bMid(3, 99, 'Always store credentials in vault (not in script); log all output')))",
        f"    lines.append(R(bMid(3, 99, 'Test scripts in non-production before scheduling in production')))",
        f"    lines.append(R(bMid(3, 99, 'Scope scripts to least-privilege service account')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Status / Reporting Scripts'), bMid(53, 99, 'Automation Scripts'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Job success rate report'), bMid(53, 99, 'Auto-expire old points'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Capacity trending'), bMid(53, 99, 'Auto-add new VMs to policy'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'SLA compliance report'), bMid(53, 99, 'Nightly DR test validation'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'RPO / RTO dashboard'), bMid(53, 99, 'Alert on job failure'))))",
    ]
    c3 = q(p['cmd3'][:43]); c4 = q(p['cmd4'][:43])
    rows.append(f"    lines.append(R(merge(bMid(3, 50, '{c3}'), bMid(53, 99, '{c4}'))))")
    rows.append("    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))")
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _security(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Security'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — Security Posture')))",
        f"    lines.append(R(bMid(3, 99, 'Authentication: {q(p['auth'][:88])}')))",
        f"    lines.append(R(bMid(3, 99, 'Encryption: {q(p['enc'][:88])}')))",
        f"    lines.append(R(bMid(3, 99, 'Network: management VLAN separated; {q(p['port3'])} management port')))",
        f"    lines.append(R(bMid(3, 99, 'Audit: all admin actions logged; log retention minimum 1 year')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(arrow([26, 51, 76])))",
        "    lines.append(txt_row())",
        "    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Access Control'), bMid(36, 66, 'Encryption'), bMid(69, 99, 'Audit'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'RBAC roles'), bMid(36, 66, 'AES-256 at rest'), bMid(69, 99, 'Admin actions'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Least privilege'), bMid(36, 66, 'TLS in transit'), bMid(69, 99, 'Login events'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'MFA optional'), bMid(36, 66, 'Key rotation'), bMid(69, 99, 'Syslog export'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'SVC acct rotate'), bMid(36, 66, 'WORM / immutable'), bMid(69, 99, 'SIEM forward'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Just-In-Time'), bMid(36, 66, 'KMS managed'), bMid(69, 99, 'Quarterly review'))))",
        "    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _sec_access(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Access Control'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — RBAC and Access Control')))",
        f"    lines.append(R(bMid(3, 99, 'Auth: {q(p['auth'][:88])}')))",
        f"    lines.append(R(bMid(3, 99, 'Principle of least privilege: each role gets only required permissions')))",
        f"    lines.append(R(bMid(3, 99, 'Service accounts: dedicated, non-interactive; rotation every 90 days')))",
        f"    lines.append(R(bMid(3, 99, 'Emergency break-glass: documented, monitored, time-limited access')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(sections(3, 99, [22, 41, 61, 80],",
        f"        ['Role', 'Access Level', 'Typical User', 'Review Freq', 'Granted By'])))",
        "    lines.append(R(sections(3, 99, [22, 41, 61, 80],",
        f"        ['Admin', 'Full config/ops', 'Sr Backup Eng', 'Quarterly', 'Security team'])))",
        "    lines.append(R(sections(3, 99, [22, 41, 61, 80],",
        f"        ['Operator', 'Start/stop jobs', 'Backup Eng', 'Quarterly', 'Team lead'])))",
        "    lines.append(R(sections(3, 99, [22, 41, 61, 80],",
        f"        ['Monitor', 'Read-only view', 'NOC / L1', 'Quarterly', 'Team lead'])))",
        "    lines.append(R(sections(3, 99, [22, 41, 61, 80],",
        f"        ['Service Acct', 'API / headless', 'Automation', 'Per rotation', 'Security team'])))",
        "    lines.append(R(bBot(3, 99)))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _sec_auth(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Authentication'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — Authentication Methods')))",
        f"    lines.append(R(bMid(3, 99, '{q(p['auth'][:92])}')))",
        f"    lines.append(R(bMid(3, 99, 'Management UI: HTTPS on {q(p['port1'])} — browser-based login')))",
        f"    lines.append(R(bMid(3, 99, 'API: bearer token or service account; rotate credentials quarterly')))",
        f"    lines.append(R(bMid(3, 99, 'Inter-component: certificate-based mutual TLS between engines')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Human Access'), bMid(53, 99, 'Machine Access'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'AD / LDAP integration'), bMid(53, 99, 'Service account'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'SAML SSO optional'), bMid(53, 99, 'API key / token'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'MFA via IdP'), bMid(53, 99, 'Certificate auth'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Session timeout 15 min'), bMid(53, 99, 'Rotate every 90 d'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Audit login events'), bMid(53, 99, 'Vault-stored secrets'))))",
        "    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _sec_enc(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Encryption'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — Encryption Configuration')))",
        f"    lines.append(R(bMid(3, 99, '{q(p['enc'][:92])}')))",
        f"    lines.append(R(bMid(3, 99, 'In-transit: TLS 1.2+ for all management; data channel also encrypted')))",
        f"    lines.append(R(bMid(3, 99, 'At-rest: AES-256 on repository or vault storage; key managed by KMS')))",
        f"    lines.append(R(bMid(3, 99, 'Key lifecycle: generate → use → rotate (annual) → retire → destroy')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))",
        f"    lines.append(R(merge(bMid(3, 50, 'In-Transit'), bMid(53, 99, 'At-Rest'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'TLS 1.2+ (minimum)'), bMid(53, 99, 'AES-256 encryption'))))",
        f"    lines.append(R(merge(bMid(3, 50, '{q(p['port1'])} HTTPS'), bMid(53, 99, 'KMS key management'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Mutual TLS internal'), bMid(53, 99, 'WORM / immutable'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Cert rotation annual'), bMid(53, 99, 'Key rotation annual'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'No plain-text admin'), bMid(53, 99, 'Audit key access'))))",
        "    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _sec_hardening(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Hardening'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — Hardening Checklist')))",
        f"    lines.append(R(bMid(3, 99, '  [ ] Disable default/admin accounts; create named admin accounts only')))",
        f"    lines.append(R(bMid(3, 99, '  [ ] Enable MFA for all interactive logins via IdP / SAML SSO')))",
        f"    lines.append(R(bMid(3, 99, '  [ ] Restrict management port ({q(p['port1'])}) to jump host / management VLAN')))",
        f"    lines.append(R(bMid(3, 99, '  [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)')))",
        f"    lines.append(R(bMid(3, 99, '  [ ] Apply all security patches within 30 days of vendor release')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, 'Network Hardening')))",
        f"    lines.append(R(bMid(3, 99, '  [ ] Separate backup VLAN — no direct production host access to repo')))",
        f"    lines.append(R(bMid(3, 99, '  [ ] Firewall: allow only {q(p['port1'])} · {q(p['port2'])} · {q(p['port3'])}')))",
        f"    lines.append(R(bMid(3, 99, '  [ ] Disable unused ports and protocols on management interface')))",
        f"    lines.append(R(bMid(3, 99, '  [ ] Immutable repository: enable WORM or object lock on backup target')))",
        f"    lines.append(R(bMid(3, 99, '  [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+')))",
        "    lines.append(R(bBot(3, 99)))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _troubleshooting(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Troubleshooting'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — Troubleshooting Approach')))",
        f"    lines.append(R(bMid(3, 99, '1  Identify: which job, component, or resource is failing')))",
        f"    lines.append(R(bMid(3, 99, '2  Scope: single job vs all jobs; one source vs all sources')))",
        f"    lines.append(R(bMid(3, 99, '3  Collect: logs and run status command; review recent change history')))",
        f"    lines.append(R(bMid(3, 99, '4  Diagnose: match symptoms to known issues; check error codes')))",
        f"    lines.append(R(bMid(3, 99, '5  Fix: apply resolution; verify fix; monitor next run')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(arrow([26, 51, 76])))",
        "    lines.append(txt_row())",
        "    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Infrastructure'), bMid(36, 66, 'Application'), bMid(69, 99, 'Data'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Network checks'), bMid(36, 66, 'Log analysis'), bMid(69, 99, 'Catalog check'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Storage space'), bMid(36, 66, 'Job error codes'), bMid(69, 99, 'Consistency'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Process health'), bMid(36, 66, 'Auth failures'), bMid(69, 99, 'Corruption scan'))))",
        f"    lines.append(R(merge(bMid(3, 33, '{q(p['port1'][:25])}'), bMid(36, 66, 'Timeout errors'), bMid(69, 99, 'Restore test'))))",
        f"    lines.append(R(merge(bMid(3, 33, 'Firewall rules'), bMid(36, 66, 'Version compat'), bMid(69, 99, 'RPO drift'))))",
        "    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _ts_issues(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Common Issues'))",
        "    lines.append(txt_row())",
        "    lines.append(R(sections(3, 99, [22, 41, 61, 80],",
        f"        ['Symptom', 'Likely Cause', 'First Check', 'Fix', 'Verify'])))",
    ]
    for issue in p.get('issues', []):
        sym, cause, check, fix, verify = (issue + ('', '', '', '', ''))[:5]
        rows.append("    lines.append(R(sections(3, 99, [22, 41, 61, 80],")
        rows.append(f"        ['{q(sym[:18])}', '{q(cause[:17])}', '{q(check[:17])}', '{q(fix[:17])}', '{q(verify[:14])}'])))")
    rows += [
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, 'General Triage Pattern')))",
        f"    lines.append(R(bMid(3, 99, '  Is the issue new or recurring? New = recent change; Recurring = config problem')))",
        f"    lines.append(R(bMid(3, 99, '  Is it isolated to one source or all? Isolated = agent; All = server/repo')))",
        f"    lines.append(R(bMid(3, 99, '  Check logs first: {q(p['cmd3'][:70])}')))",
        f"    lines.append(R(bMid(3, 99, '  If unresolved in 2h: open vendor case with full log bundle')))",
        "    lines.append(R(bBot(3, 99)))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _ts_diag(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Diagnostics'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — Diagnostic Commands')))",
        f"    lines.append(R(bMid(3, 99, 'Collect these before opening a vendor support case')))",
        f"    lines.append(R(bMid(3, 99, '  {q(p['cmd3'][:88])}')))",
        f"    lines.append(R(bMid(3, 99, '  {q(p['cmd4'][:88])}')))",
        f"    lines.append(R(bMid(3, 99, '  Check system logs: /var/log/ or Windows Event Viewer')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Log Collection'), bMid(53, 99, 'Live Diagnostics'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Application log bundle'), bMid(53, 99, 'Network connectivity'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'OS syslog (journalctl)'), bMid(53, 99, 'Storage path check'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Core dump if crashed'), bMid(53, 99, 'Process list check'))))",
        f"    lines.append(R(merge(bMid(3, 50, 'Config export/backup'), bMid(53, 99, 'Port reachability'))))",
    ]
    c3 = q(p['cmd3'][:43]); c4 = q(p['cmd4'][:43])
    rows.append(f"    lines.append(R(merge(bMid(3, 50, '{c3}'), bMid(53, 99, '{c4}'))))")
    rows.append("    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))")
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows

def _ts_escalation(p):
    s = p['short']
    rows = [
        f"    lines.append(title_border(W2, '{q(s)} — Escalation'))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, '{q(s)} — Escalation Path')))",
        f"    lines.append(R(bMid(3, 99, 'L1 Triage: review logs, match to known issues in runbook (0–30 min)')))",
        f"    lines.append(R(bMid(3, 99, 'L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)')))",
        f"    lines.append(R(bMid(3, 99, 'Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)')))",
        f"    lines.append(R(bMid(3, 99, 'Sev1 (data loss / production impact): page on-call + open critical case')))",
        "    lines.append(R(bBot(3, 99)))",
        "    lines.append(txt_row())",
        "    lines.append(R(bTop(3, 99)))",
        f"    lines.append(R(bMid(3, 99, 'Information to Collect Before Escalating')))",
        f"    lines.append(R(bMid(3, 99, '  Product version: {q(s)} version string from About / version command')))",
        f"    lines.append(R(bMid(3, 99, '  Full log bundle: {q(p['cmd3'][:70])}')))",
        f"    lines.append(R(bMid(3, 99, '  Symptom timeline: when first occurred; any changes made')))",
        f"    lines.append(R(bMid(3, 99, '  Scope: single job / all jobs / all components — narrows root cause')))",
        f"    lines.append(R(bMid(3, 99, '  Error codes: exact error messages and exit codes from logs')))",
        "    lines.append(R(bBot(3, 99)))",
    ]
    rows += _make_phys(p['phys'])
    rows += _make_term_rows(p['terms'])
    return rows


# ── File generation ───────────────────────────────────────────────────────────

def generate_for_product(p, pages):
    """Return a string of all @kb_diagram functions for a product."""
    out = []
    for (page_type, _, _) in pages:
        block = fn_body(p, page_type)
        if block:
            out.append(block)
    return '\n'.join(out)

def append_to_file(path, content):
    with open(path, 'a') as f:
        f.write('\n')
        f.write(content)
        f.write('\n')
    print(f"  Appended to {path}")

def create_file(path, header, content):
    with open(path, 'w') as f:
        f.write(header)
        f.write('\n')
        f.write(content)
        f.write('\n')
    print(f"  Created {path}")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # 1 — Complete disaster_recovery_backup.py (netbackup + rasr)
    print("Generating netbackup + rasr...")
    for pname in ['netbackup', 'rasr']:
        p = PRODUCTS[pname]
        content = generate_for_product(p, STD_PAGES)
        append_to_file(p['outfile'], content)

    # 2 — Complete disaster_recovery_replication.py (recoverpoint remaining + srdf-a/s + srm + superna + veeam + misc)
    print("Generating DR replication remainder...")
    for pname in ['recoverpoint', 'srdf-a', 'srdf-s', 'srm', 'superna-eyeglass', 'veeam']:
        p = PRODUCTS[pname]
        pages = REMAINING_PAGES if pname == 'recoverpoint' else STD_PAGES
        content = generate_for_product(p, pages)
        append_to_file(p['outfile'], content)

    # DR misc pages (simple overview diagrams)
    print("Generating DR misc pages...")
    misc_funcs = []
    for key, fpath, desc in DR_MISC:
        fn_name = key.replace('-', '_')
        short_title = desc.split(' — ')[0] if ' — ' in desc else key
        body_lines = [
            f"@kb_diagram(",
            f"    '{key}',",
            f"    '{fpath}',",
            f"    '{q(desc)}',",
            f")",
            f"def _{fn_name}():",
            f"    W2 = 103",
            f"    R, txt_row = make_helpers(W2)",
            f"    lines = []",
            f"    lines.append(title_border(W2, '{q(short_title[:90])}'))",
            f"    lines.append(txt_row())",
            f"    lines.append(R(bTop(3, 99)))",
            f"    lines.append(R(bMid(3, 99, '{q(desc[:92])}')))",
            f"    lines.append(R(bMid(3, 99, 'See product-specific sub-sections for detailed procedures')))",
            f"    lines.append(R(bMid(3, 99, 'DR success depends on: documented runbooks · tested failover · validated RTO')))",
            f"    lines.append(R(bMid(3, 99, 'Minimum DR posture: defined RPO/RTO · tested backups · known escalation path')))",
            f"    lines.append(R(bMid(3, 99, 'Test DR procedures quarterly; document results; update runbooks after each test')))",
            f"    lines.append(R(bBot(3, 99)))",
            f"    lines.append(txt_row())",
            f"    lines.append(txt_row('Physical Infrastructure:'))",
            f"    lines.append(txt_row('Production site · DR site · Replication link · Management network · Vault network'))",
            f"    lines.append(txt_row())",
            f"    lines.append(txt_row('Key terms:'))",
            f"    lines.append(txt_row())",
            f"    lines.append(txt_row('RPO           = Recovery Point Objective; max acceptable data loss window'))",
            f"    lines.append(txt_row('RTO           = Recovery Time Objective; max acceptable downtime before restore'))",
            f"    lines.append(txt_row('Failover      = activating the DR site; redirecting hosts to replica resources'))",
            f"    lines.append(txt_row('Failback      = returning operations to production site after DR resolved'))",
            f"    lines.append(txt_row('Runbook       = step-by-step documented procedure for a specific DR scenario'))",
            f"    lines.append(txt_row('IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery'))",
            f"    lines.append(txt_row('Clean Room    = isolated vCenter + workstations for cyber recovery validation'))",
            f"    lines.append(txt_row('Air Gap       = network isolation preventing attacker lateral movement to vault'))",
            f"    lines.append(txt_row('DR Test       = planned failover test; validates RTO without real disaster'))",
            f"    lines.append(txt_row('Replication   = continuous or periodic data copy to secondary site or vault'))",
            f"    lines.append(txt_row('Recovery Tier = classification: hot/warm/cold based on RTO requirement'))",
            f"    lines.append(txt_row('BIA           = Business Impact Analysis; drives RPO/RTO targets per system'))",
            f"    lines.append(txt_row())",
            f"    lines.append('\\u2514' + '\\u2500' * W2 + '\\u2518')",
            f"    return lines",
        ]
        misc_funcs.append('\n'.join(body_lines))
    append_to_file('scripts/diagrams/disaster_recovery_replication.py', '\n\n'.join(misc_funcs))

    print("Done. Run: python3 scripts/ascii_diagram_gen.py --validate")
