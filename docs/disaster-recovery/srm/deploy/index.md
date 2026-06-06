# VMware SRM — Initial Deployment

VMware Site Recovery Manager (SRM) is VMware's orchestrated disaster recovery solution. It automates failover of vSphere workloads from a protected site to a recovery site using either vSphere Replication or array-based replication (ABR). This page covers a greenfield paired-site deployment from installation through to a validated test recovery plan.

---

## Prerequisites

Confirm the following before starting the deployment:

**Infrastructure:**

- vCenter Server deployed and operational at both the protected site and the recovery site (linked-mode optional but not required)
- vSphere version and SRM version compatibility verified against the VMware Interoperability Matrix
- Sufficient compute and storage at the recovery site to run protected workloads under DR conditions
- Shared storage (for ABR) or vSphere Replication capability at both sites

**Replication choice — decide before installing:**

- **vSphere Replication (VR):** Built-in, hypervisor-based, no storage vendor dependency. Suitable for RPO 15 minutes or greater.
- **Array-Based Replication (ABR):** Storage array replicates LUNs/volumes. Requires a Storage Replication Adapter (SRA) from the array vendor (e.g., Dell PowerStore SRA, NetApp SRA). RPO limited only by array capability.

**SRM appliance form factor (version-dependent):**

- SRM 8.x and later: Linux OVA (recommended)
- SRM pre-8.x: Windows Server installer (Windows Server 2016/2019)

**Networking:**

- TCP 443 open between SRM at protected site and SRM at recovery site
- TCP 9086 open between SRM appliances (inter-site SRM communication)
- TCP 443 open from each SRM to its local vCenter
- DNS resolvable FQDNs for both vCenters and both SRM appliances from either site

---

## Deploy SRM at Protected Site

**For OVA (SRM 8.x+):**

1. Download the SRM OVA from the VMware Customer Connect portal.
2. Log in to the protected-site vCenter → **Actions → Deploy OVF Template** → select the SRM OVA.
3. Assign to a management cluster and datastore — do not place SRM on a datastore that is itself replicated (SRM cannot protect itself).
4. Complete OVF properties:
   - Hostname (FQDN), IP address, subnet mask, default gateway, DNS, NTP
   - Admin password (record in credentials store)
5. Power on and wait for first-boot (~5 minutes).
6. Open `https://<srm-appliance-ip>:5480` → SRM Appliance Management Interface → complete configuration wizard:
   - Set NTP sync
   - Connect to vCenter: enter protected-site vCenter FQDN, SSO credentials → **Save and Restart Services**
7. Open vCenter → **Menu → Site Recovery** → confirm SRM appears with status **OK** and site name displayed.

**For Windows installer (pre-8.x):**

1. Install SRM on a Windows Server VM joined to domain.
2. Run `VMware-srm-<version>.exe` → accept defaults → provide vCenter FQDN and credentials when prompted.
3. SRM registers as a vCenter extension — verify in vCenter → **Menu → Site Recovery**.

---

## Deploy SRM at Recovery Site

1. Repeat the identical deployment process at the recovery-site vCenter (OVA or Windows, matching version exactly).
2. Connect the recovery-site SRM to the recovery-site vCenter using the same procedure.
3. In both vCenters, navigate to **Menu → Site Recovery** → confirm SRM shows status **OK** at each site independently before proceeding to pairing.

Key check: both SRM instances must run the same version. Version mismatch blocks pairing.

---

## Pair the Sites

Site pairing establishes the trust relationship between the two SRM instances.

1. Log in to the **protected-site vCenter** → **Menu → Site Recovery → Sites → New Site Pair**.
2. Enter the recovery-site vCenter FQDN and SSO administrator credentials → **Next**.
3. SRM presents the SSL certificate thumbprint of the recovery-site vCenter — review and **Accept**.
4. SRM presents the SSL certificate thumbprint of the recovery-site SRM appliance — review and **Accept**.
5. Pairing completes → both sites now appear in the Site Recovery UI with status **Connected**.
6. Verify from the recovery site: open recovery-site vCenter → **Menu → Site Recovery → Sites** → protected site listed as the peer with status **Connected**.

---

## Configure Replication

**vSphere Replication path:**

1. Download the VR appliance OVA from VMware Customer Connect.
2. Deploy VR appliance at the protected site → connect to protected-site vCenter (same OVA deploy procedure as SRM).
3. Deploy VR appliance at the recovery site → connect to recovery-site vCenter.
4. Pair VR appliances: protected-site vCenter → **Menu → Site Recovery → Replication → Configure Replication** → enter recovery-site VR FQDN → authenticate → **Pair**.
5. Configure per-VM replication:
   - Select a VM → right-click → **All Site Recovery Actions → Configure Replication**
   - Choose target site, target datastore, RPO (minimum 15 minutes for VR)
   - Enable **Guest OS quiescing** for application-consistent copies (requires VMware Tools)
   - Confirm replication status shows **OK** in the VR inventory

**Array-Based Replication path:**

1. Obtain the SRA package from the storage vendor (must match array firmware and SRM version).
2. Install SRA on the SRM appliance:
   - SRM 8.x OVA: SRM Appliance Management Interface → **Storage Replication Adapters → Upload SRA** → upload the vendor-provided SRA tar.gz
   - Windows SRM: run the SRA installer on the Windows Server hosting SRM
3. Install SRA at the recovery site using the same process.
4. Configure array credentials: SRM UI → **Configure → Array Managers → Add** → enter array management IP, username, password for both protected and recovery arrays → **Discover Arrays**.
5. Verify SRM discovers replicated datastore pairs under **Configure → Array Pairs**.

---

## Configure Mappings

Mappings define how protected-site objects translate to recovery-site equivalents when a recovery plan executes.

**Network Mappings:**

1. SRM UI (protected site) → **Configure → Network Mappings → Add Mapping**.
2. Map each production port group to the corresponding DR port group at the recovery site.
3. Add a **Test Network** mapping: each production port group → isolated bubble network (used during test runs only — prevents test VMs from reaching production).

**Resource Mappings:**

1. SRM UI → **Configure → Resource Mappings → Add Mapping**.
2. Map protected-site cluster or resource pool → recovery-site cluster or resource pool.

**Folder Mappings:**

1. SRM UI → **Configure → Folder Mappings → Add Mapping**.
2. Map protected-site VM folders to recovery-site VM folders (controls where recovered VMs appear in the vCenter inventory).

**Placeholder Datastore:**

1. SRM UI → **Configure → Placeholder Datastores → Add**.
2. Select a small datastore at the recovery site — SRM uses this to register placeholder VMs that represent protected workloads.

---

## Create a Protection Group

A protection group defines which VMs are protected together and how they replicate.

1. SRM UI → **Protection Groups → New Protection Group**.
2. Name the group (e.g., `PG-Tier1-VMs`).
3. Select replication type:
   - **vSphere Replication:** select VMs individually from the list of configured VR replicas
   - **Array-Based Replication:** select a replicated datastore — SRM automatically includes all VMs on that datastore
4. Review detected VMs and confirm.
5. Click **Next → Finish** → SRM runs validation.
6. Resolve any validation warnings (common: missing placeholder datastore assignment, missing folder mapping for a VM).
7. Confirm protection group status shows **OK** (green) with all VMs listed as **Protected**.

---

## Create a Recovery Plan

A recovery plan defines the ordered sequence of steps to recover a set of protection groups.

1. SRM UI → **Recovery Plans → New Recovery Plan**.
2. Name the plan (e.g., `RP-Tier1-Failover`).
3. Add one or more protection groups to the plan.
4. Configure priority groups:
   - **Priority 1:** infrastructure VMs (DNS, AD, database servers) — these power on first
   - **Priority 2:** application-tier VMs
   - **Priority 3:** non-critical workloads
   - Within each priority, set per-VM startup delay and IP customisation if performing real failover (not required for test)
5. Add custom recovery steps as needed:
   - Pre-power-on scripts (e.g., mount NFS exports, update DNS)
   - Post-power-on scripts (e.g., notify monitoring, send alert)
6. Configure IP property mappings if VMs need different IPs at the recovery site (SRM → **Configure → IP Address Mappings**).
7. Click **Finish** → SRM validates the plan.
8. Resolve all validation errors before proceeding. Warnings should be reviewed but do not block testing.

---

## Test the Recovery Plan

Testing runs recovery in an isolated bubble network and is non-disruptive to production. It is the only way to confirm the plan works.

1. SRM UI → **Recovery Plans** → select the plan.
2. Click **Test** → confirm the test network mappings are in place → **Next → Finish**.
3. Monitor execution in the **Steps** panel:
   - Storage: test snapshots created from replicated data
   - VMs: powered on at recovery site on isolated test networks
   - Custom steps: scripts execute in configured order
4. Verify each VM powers on and the OS boots correctly:
   - Check vCenter at recovery site → confirm VMs visible in test state
   - RDP or SSH into test VMs if accessible from the isolated network to verify application health
5. Review the SRM test report: **Recovery Plans → History → view last run** — check for step failures or warnings.
6. Click **Cleanup** when testing is complete — SRM powers off test VMs, removes test snapshots, and resets protection group state to **Protected**.
7. Document the test result: date, plan name, steps executed, any failures and resolution, tester sign-off.

Regular testing cadence recommendation: full test every 90 days, partial validation monthly.
