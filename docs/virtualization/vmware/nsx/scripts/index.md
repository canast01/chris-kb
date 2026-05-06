# Scripts

> Part of the [NSX](../) reference.

---

## NSX-T System Health Check (Python)

Query key NSX-T REST API endpoints to assess cluster, transport node, and edge cluster health, and report any open alarms.

~~~python
#!/usr/bin/env python3
"""
nsxt_health_check.py
Usage: python3 nsxt_health_check.py
Deps: pip install requests urllib3
"""

import os, sys, json
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

NSX_HOST = os.environ.get("NSX_HOST", "nsx-manager.local")
NSX_USER = os.environ.get("NSX_USER", "admin")
NSX_PASS = os.environ.get("NSX_PASS", "")

BASE_URL = f"https://{NSX_HOST}"
AUTH     = (NSX_USER, NSX_PASS)
HEADERS  = {"Content-Type": "application/json", "Accept": "application/json"}
overall  = 0


def get(path):
    r = requests.get(f"{BASE_URL}{path}", auth=AUTH, headers=HEADERS,
                     verify=False, timeout=15)
    r.raise_for_status()
    return r.json()


def check(label, status, detail=""):
    global overall
    icons = {"PASS": "\033[32mPASS\033[0m", "WARNING": "\033[33mWARN\033[0m", "CRITICAL": "\033[31mCRIT\033[0m"}
    print(f"  [{icons.get(status, status)}] {label:<45} {detail}")
    if status == "CRITICAL": overall = max(overall, 2)
    if status == "WARNING":  overall = max(overall, 1)


print(f"\n=== NSX-T System Health Check: {NSX_HOST} ===\n")

# --- Cluster status ---
try:
    cluster = get("/api/v1/cluster/status")
    mgmt_status = cluster.get("mgmt_cluster_status", {}).get("status", "UNKNOWN")
    ctrl_status  = cluster.get("control_cluster_status", {}).get("status", "UNKNOWN")
    check("Management cluster", "PASS" if mgmt_status == "STABLE" else "CRITICAL", mgmt_status)
    check("Control cluster",    "PASS" if ctrl_status  == "STABLE" else "CRITICAL", ctrl_status)
    for node in cluster.get("detailed_cluster_status", {}).get("groups_status", []):
        for member in node.get("members", []):
            ns = "PASS" if member.get("status") == "UP" else "CRITICAL"
            check(f"  Node: {member.get('display_name', member.get('component_id','?'))}", ns,
                  member.get("status", "UNKNOWN"))
except Exception as e:
    check("Cluster status", "CRITICAL", str(e)[:80])

# --- Transport node health ---
try:
    tn_status = get("/api/v1/transport-nodes/status")
    total = tn_status.get("total_count", 0)
    up    = tn_status.get("up_count",    0)
    down  = tn_status.get("down_count",  0)
    degrad = tn_status.get("degraded_count", 0)
    s = "PASS" if down == 0 and degrad == 0 else ("WARNING" if degrad > 0 else "CRITICAL")
    check("Transport nodes", s, f"total={total}  up={up}  down={down}  degraded={degrad}")
except Exception as e:
    check("Transport nodes", "WARNING", str(e)[:80])

# --- Edge clusters ---
try:
    edges = get("/api/v1/edge-clusters")
    for ec in edges.get("results", []):
        ec_id   = ec.get("id")
        ec_name = ec.get("display_name", ec_id)
        members = ec.get("members", [])
        check(f"Edge cluster: {ec_name}", "PASS", f"{len(members)} member(s)")
except Exception as e:
    check("Edge clusters", "WARNING", str(e)[:80])

# --- Open alarms ---
try:
    alarms = get("/api/v1/alarms?status=OPEN&severity=CRITICAL")
    crit_count = alarms.get("result_count", 0)
    if crit_count > 0:
        check("Open CRITICAL alarms", "CRITICAL", f"{crit_count} alarm(s) open")
        for alarm in alarms.get("results", [])[:5]:
            print(f"       {alarm.get('alarm_source',{}).get('display_name','?')}  —  {alarm.get('summary','')[:80]}")
    else:
        check("Open CRITICAL alarms", "PASS", "None")

    alarms_warn = get("/api/v1/alarms?status=OPEN&severity=MEDIUM")
    warn_count  = alarms_warn.get("result_count", 0)
    s = "WARNING" if warn_count > 0 else "PASS"
    check("Open MEDIUM alarms", s, f"{warn_count} alarm(s)")
except Exception as e:
    check("Alarms", "WARNING", str(e)[:80])

print(f"\nOverall: {'PASS' if overall == 0 else 'WARNING' if overall == 1 else 'CRITICAL'}")
sys.exit(overall)
~~~

---

## Transport Node Status Monitor (Python)

Enumerate all transport nodes, check tunnel health and BFD state for each, and flag any nodes with DOWN tunnels.

~~~python
#!/usr/bin/env python3
"""
nsxt_transport_node_monitor.py
Usage: python3 nsxt_transport_node_monitor.py
Deps: pip install requests
"""

import os, sys
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

NSX_HOST = os.environ.get("NSX_HOST", "nsx-manager.local")
NSX_USER = os.environ.get("NSX_USER", "admin")
NSX_PASS = os.environ.get("NSX_PASS", "")
BASE_URL  = f"https://{NSX_HOST}"
AUTH      = (NSX_USER, NSX_PASS)
HEADERS   = {"Accept": "application/json"}


def get(path, params=None):
    r = requests.get(f"{BASE_URL}{path}", auth=AUTH, headers=HEADERS,
                     params=params, verify=False, timeout=15)
    r.raise_for_status()
    return r.json()


# Fetch all transport nodes
nodes_resp = get("/api/v1/transport-nodes", params={"page_size": 500})
nodes = nodes_resp.get("results", [])

print(f"=== NSX-T Transport Node Status Monitor: {NSX_HOST} ===")
print(f"Transport nodes found: {len(nodes)}\n")

header = "{:<40} {:<10} {:<10} {:<12} {:<10} {}"
print(header.format("Node Name", "Type", "State", "Tunnels", "TunnelDown", "Status"))
print("-" * 95)

issues = []
overall = 0

for node in sorted(nodes, key=lambda x: x.get("display_name", "")):
    node_id   = node["id"]
    node_name = node.get("display_name", node_id)

    # Determine type
    node_type = "Unknown"
    td = node.get("node_deployment_info", {})
    if "ESXiHostNode" in str(td.get("resource_type", "")):
        node_type = "ESXi"
    elif "EdgeNode" in str(td.get("resource_type", "")):
        node_type = "Edge"

    # Connection state
    try:
        state_resp = get(f"/api/v1/transport-nodes/{node_id}/state")
        conn_state = state_resp.get("state", "unknown")
    except Exception:
        conn_state = "error"

    # Tunnel status
    tunnel_total = 0
    tunnel_down  = 0
    try:
        tunnels_resp = get(f"/api/v1/transport-nodes/{node_id}/tunnels")
        tunnels = tunnels_resp.get("tunnels", [])
        tunnel_total = len(tunnels)
        tunnel_down  = sum(1 for t in tunnels if t.get("status", "").upper() != "UP")
    except Exception:
        tunnel_total = -1

    status = "OK"
    if conn_state not in ("success", "in_sync"):
        status = "NODE_ISSUE"
        overall = max(overall, 2)
    elif tunnel_down > 0:
        status = "TUNNEL_DOWN"
        overall = max(overall, 2)
    elif tunnel_total == 0:
        status = "NO_TUNNELS"
        overall = max(overall, 1)

    if status != "OK":
        issues.append(f"  {node_name}  [{node_type}]  conn={conn_state}  tunnels={tunnel_total}  down={tunnel_down}")

    td_str = str(tunnel_down) if tunnel_total >= 0 else "ERR"
    print(header.format(node_name[:40], node_type, conn_state[:10],
                        tunnel_total, td_str, status))

print()
if issues:
    print(f"ISSUES ({len(issues)}):")
    for i in issues:
        print(i)
    sys.exit(1)
else:
    print("All transport nodes and tunnels healthy.")
    sys.exit(0)
~~~

---

## DFW Rule Audit (Bash)

Authenticate to the NSX-T Policy API and retrieve all DFW security policies and rules, flagging overly permissive allow-any rules.

~~~bash
#!/bin/bash
# nsxt_dfw_audit.sh
# Usage: NSX_HOST=nsx.local NSX_USER=admin NSX_PASS=secret ./nsxt_dfw_audit.sh

NSX_HOST="${NSX_HOST:-nsx-manager.local}"
NSX_USER="${NSX_USER:-admin}"
NSX_PASS="${NSX_PASS:-}"
BASE_URL="https://${NSX_HOST}"
CURL_OPTS="-sk --user '${NSX_USER}:${NSX_PASS}' -H 'Accept: application/json'"

warn_count=0
total_rules=0

echo "=== NSX-T DFW Rule Audit ==="
echo "Manager: ${NSX_HOST}"
echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo

# Get all security policies in the default domain
policies=$(curl $CURL_OPTS \
  "${BASE_URL}/policy/api/v1/infra/domains/default/security-policies?page_size=200" 2>/dev/null)

policy_count=$(echo "$policies" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result_count',0))" 2>/dev/null)
echo "Policies found: ${policy_count}"
echo

# Iterate policies
policy_ids=$(echo "$policies" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for p in d.get('results', []):
    print(p['id'] + '\t' + p.get('display_name', p['id']))
" 2>/dev/null)

while IFS=$'\t' read -r pol_id pol_name; do
    rules=$(curl $CURL_OPTS \
      "${BASE_URL}/policy/api/v1/infra/domains/default/security-policies/${pol_id}/rules?page_size=1000" 2>/dev/null)

    echo "Policy: ${pol_name} (${pol_id})"
    echo "  $(echo "$rules" | python3 -c "import sys,json; d=json.load(sys.stdin); print(str(d.get('result_count',0))+' rules')" 2>/dev/null)"

    # Parse rules and flag permissive allows
    echo "$rules" | python3 - <<'PYEOF'
import sys, json
data = json.load(sys.stdin)
for rule in data.get('results', []):
    name    = rule.get('display_name', rule.get('id', '?'))
    action  = rule.get('action', '?')
    sources = rule.get('source_groups', [])
    dests   = rule.get('destination_groups', [])
    applied = rule.get('scope', [])

    flag = ""
    if action == "ALLOW" and "ANY" in sources and "ANY" in dests:
        flag = "  *** OVERLY_PERMISSIVE: ALLOW ANY->ANY ***"
    elif action == "ALLOW" and "ANY" in sources:
        flag = "  ** WARN: ALLOW from ANY source"
    elif action == "ALLOW" and "ANY" in dests:
        flag = "  ** WARN: ALLOW to ANY destination"

    src_str  = ', '.join(sources[:3]) + ('...' if len(sources) > 3 else '')
    dst_str  = ', '.join(dests[:3])   + ('...' if len(dests) > 3 else '')
    apl_str  = ', '.join(applied[:2]) + ('...' if len(applied) > 2 else '')
    print(f"    [{action:<7}] {name:<40}  src={src_str}  dst={dst_str}  scope={apl_str}{flag}")
PYEOF
    echo
done <<< "$policy_ids"

echo "Audit complete."
~~~

---

## Segment and Gateway Health Check (Python)

Query NSX-T Policy API for all segments, Tier-0/Tier-1 gateways, and BGP neighbor state, and report connectivity health.

~~~python
#!/usr/bin/env python3
"""
nsxt_gateway_health.py
Usage: python3 nsxt_gateway_health.py
Deps: pip install requests
"""

import os, sys
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

NSX_HOST = os.environ.get("NSX_HOST", "nsx-manager.local")
NSX_USER = os.environ.get("NSX_USER", "admin")
NSX_PASS = os.environ.get("NSX_PASS", "")
BASE_URL  = f"https://{NSX_HOST}"
AUTH      = (NSX_USER, NSX_PASS)
HEADERS   = {"Accept": "application/json"}
overall   = 0


def get(path, params=None):
    r = requests.get(f"{BASE_URL}{path}", auth=AUTH, headers=HEADERS,
                     params=params, verify=False, timeout=15)
    r.raise_for_status()
    return r.json()


def status_mark(ok):
    return "\033[32mPASS\033[0m" if ok else "\033[31mFAIL\033[0m"


# --- Segments ---
print(f"\n=== NSX-T Segment and Gateway Health: {NSX_HOST} ===\n")
print("--- Segments ---")
try:
    segs = get("/policy/api/v1/infra/segments", params={"page_size": 500})
    for seg in sorted(segs.get("results", []), key=lambda x: x.get("display_name", "")):
        name    = seg.get("display_name", seg["id"])
        state   = seg.get("admin_state", "unknown")
        subnet  = seg.get("subnets", [{}])[0].get("gateway_address", "N/A") if seg.get("subnets") else "N/A"
        conn_to = seg.get("connectivity_path", "none")
        ok = state.upper() == "UP"
        if not ok:
            global overall
            overall = max(overall, 1)
        print(f"  [{status_mark(ok)}] {name:<40}  state={state:<6}  subnet={subnet:<20}  gw={conn_to.split('/')[-1]}")
except Exception as e:
    print(f"  [WARN] Could not retrieve segments: {e}")

# --- Tier-0 Gateways ---
print("\n--- Tier-0 Gateways ---")
t0_ids = []
try:
    t0s = get("/policy/api/v1/infra/tier-0s")
    for t0 in t0s.get("results", []):
        t0_id   = t0["id"]
        t0_name = t0.get("display_name", t0_id)
        t0_ids.append(t0_id)
        ha_mode = t0.get("ha_mode", "N/A")
        state   = t0.get("failover_mode", "PREEMPTIVE")
        print(f"  [INFO ] {t0_name:<40}  ha_mode={ha_mode}  failover={state}")

        # BGP neighbors via management plane API
        try:
            # Get logical router ID for this T0
            lr_list = get("/api/v1/logical-routers", params={"router_type": "TIER0"})
            for lr in lr_list.get("results", []):
                if lr.get("display_name") == t0_name or lr.get("id") == t0_id:
                    lr_id = lr["id"]
                    bgp = get(f"/api/v1/logical-routers/{lr_id}/routing/bgp/neighbors/summary")
                    for nbr in bgp.get("results", []):
                        for n in nbr.get("bgp_neighbors_table_entry", []):
                            nbr_ip   = n.get("neighbor_address", "?")
                            nbr_state = n.get("connection_state", "?")
                            ok = nbr_state.upper() == "ESTABLISHED"
                            if not ok:
                                overall = max(overall, 2)
                            print(f"       BGP [{status_mark(ok)}] {nbr_ip:<20} state={nbr_state}")
        except Exception:
            pass
except Exception as e:
    print(f"  [WARN] Could not retrieve Tier-0 gateways: {e}")

# --- Tier-1 Gateways ---
print("\n--- Tier-1 Gateways ---")
try:
    t1s = get("/policy/api/v1/infra/tier-1s")
    for t1 in sorted(t1s.get("results", []), key=lambda x: x.get("display_name", "")):
        t1_name = t1.get("display_name", t1["id"])
        linked  = t1.get("tier0_path", "none").split("/")[-1]
        route_adv = t1.get("route_advertisement_types", [])
        print(f"  [INFO ] {t1_name:<40}  linked_t0={linked:<20}  adv={','.join(route_adv)}")
except Exception as e:
    print(f"  [WARN] Could not retrieve Tier-1 gateways: {e}")

print(f"\nOverall: {'PASS' if overall == 0 else 'WARNING' if overall == 1 else 'CRITICAL'}")
sys.exit(overall)
~~~

---

## Ansible NSX-T Operational Playbook

Check NSX-T cluster, transport node, and edge health using the `uri` module, and assert no open critical alarms.

~~~yaml
---
# nsxt_operational.yml
# Usage: ansible-playbook nsxt_operational.yml
# Vars: nsx_host, nsx_user, nsx_pass

- name: NSX-T Operational Health Check
  hosts: localhost
  gather_facts: false
  vars:
    nsx_host: nsx-manager.local
    nsx_user: "{{ lookup('env','NSX_USER') }}"
    nsx_pass: "{{ lookup('env','NSX_PASS') }}"
    nsx_base: "https://{{ nsx_host }}"

  tasks:

    - name: Check NSX-T cluster status
      ansible.builtin.uri:
        url:            "{{ nsx_base }}/api/v1/cluster/status"
        method:         GET
        user:           "{{ nsx_user }}"
        password:       "{{ nsx_pass }}"
        force_basic_auth: true
        validate_certs: false
        return_content: true
      register: cluster_status

    - name: Assert cluster management status is STABLE
      ansible.builtin.assert:
        that: >
          cluster_status.json.mgmt_cluster_status.status == 'STABLE'
        fail_msg: "NSX-T management cluster is NOT stable: {{ cluster_status.json.mgmt_cluster_status.status }}"
        success_msg: "NSX-T management cluster is STABLE"

    - name: Check transport node status
      ansible.builtin.uri:
        url:            "{{ nsx_base }}/api/v1/transport-nodes/status"
        method:         GET
        user:           "{{ nsx_user }}"
        password:       "{{ nsx_pass }}"
        force_basic_auth: true
        validate_certs: false
        return_content: true
      register: tn_status

    - name: Report transport node health
      ansible.builtin.debug:
        msg: >
          Transport nodes: total={{ tn_status.json.total_count }},
          up={{ tn_status.json.up_count }},
          down={{ tn_status.json.down_count }},
          degraded={{ tn_status.json.degraded_count }}

    - name: Assert no transport nodes are down
      ansible.builtin.assert:
        that: tn_status.json.down_count == 0
        fail_msg: "{{ tn_status.json.down_count }} transport node(s) are DOWN"
        success_msg: "All transport nodes are UP"

    - name: Check edge clusters
      ansible.builtin.uri:
        url:            "{{ nsx_base }}/api/v1/edge-clusters"
        method:         GET
        user:           "{{ nsx_user }}"
        password:       "{{ nsx_pass }}"
        force_basic_auth: true
        validate_certs: false
        return_content: true
      register: edge_clusters

    - name: Report edge clusters found
      ansible.builtin.debug:
        msg: "Edge clusters: {{ edge_clusters.json.result_count }}"

    - name: Check for open critical alarms
      ansible.builtin.uri:
        url:            "{{ nsx_base }}/api/v1/alarms?status=OPEN&severity=CRITICAL"
        method:         GET
        user:           "{{ nsx_user }}"
        password:       "{{ nsx_pass }}"
        force_basic_auth: true
        validate_certs: false
        return_content: true
      register: critical_alarms

    - name: Assert no open critical alarms
      ansible.builtin.assert:
        that: critical_alarms.json.result_count == 0
        fail_msg: >
          {{ critical_alarms.json.result_count }} CRITICAL alarm(s) open on {{ nsx_host }}.
          First alarm: {{ critical_alarms.json.results[0].summary | default('N/A') }}
        success_msg: "No open critical alarms"

    - name: Output health summary
      ansible.builtin.debug:
        msg:
          - "NSX-T health check complete for {{ nsx_host }}"
          - "Cluster: {{ cluster_status.json.mgmt_cluster_status.status }}"
          - "Transport nodes up: {{ tn_status.json.up_count }}/{{ tn_status.json.total_count }}"
          - "Critical alarms: {{ critical_alarms.json.result_count }}"
~~~
