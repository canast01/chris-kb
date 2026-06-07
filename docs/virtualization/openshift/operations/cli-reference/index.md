# OpenShift — CLI Reference

<div class="kb-summary">
oc command reference: resource management, log collection, exec, adm commands, debugging, and context management. oc extends kubectl with OpenShift-specific resources and shortcuts.
</div>

```text
┌─────────────────────────────────── OpenShift oc CLI Reference ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   oc is a superset of kubectl — all kubectl commands work; oc adds OCP-specific shortcuts     │   │
│   │   Context: set KUBECONFIG or use oc login; switch projects with oc project <name>             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Core Commands         │  │       Admin Commands         │  │     Debug Commands          │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  oc get / describe / edit   │  │  oc adm node-logs            │  │  oc debug node/<name>       │  │
│   │  oc logs / exec / rsh       │  │  oc adm certificate approve  │  │  oc debug deployment/<name> │  │
│   │  oc apply / delete / patch  │  │  oc adm drain / cordon       │  │  oc adm inspect             │  │
│   │  oc project / new-project   │  │  oc adm policy               │  │  must-gather collection     │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Project      = OpenShift namespace with additional metadata; oc project switches context           │
│    oc adm       = Administrative subcommand; node management, certificate ops, policy                 │
│    oc debug     = Spawns a debug pod from a node/deployment image for interactive troubleshooting     │
│    must-gather  = Collects full cluster state (logs, configs, events) into a tarball for Red Hat      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Authentication & Context

```bash
# Login
oc login https://api.ocp.example.com:6443 -u admin -p password
oc login --token=<token> --server=https://api.ocp.example.com:6443

# Who am I / current context
oc whoami
oc whoami --show-token
oc config current-context

# Switch project (namespace)
oc project openshift-monitoring
oc new-project my-app
oc projects          # list all accessible projects
```

## Resource Management

```bash
# Get resources
oc get nodes -o wide
oc get pods -n openshift-etcd
oc get pods --all-namespaces | grep -v "Running\|Completed"
oc get co            # cluster operators
oc get csr           # certificate signing requests

# Describe and inspect
oc describe node <node-name>
oc describe pod <pod> -n <ns>
oc get events -n <ns> --sort-by='.lastTimestamp'

# Apply / delete
oc apply -f manifest.yaml
oc delete pod <pod> -n <ns>
oc delete pod <pod> -n <ns> --grace-period=0 --force

# Patch resources
oc patch deployment/myapp -p '{"spec":{"replicas":3}}'
oc patch node <node> -p '{"spec":{"unschedulable":true}}'
```

## Logs

```bash
# Pod logs
oc logs <pod> -n <ns>
oc logs <pod> -n <ns> -c <container>    # specific container
oc logs <pod> -n <ns> --previous        # previous container instance
oc logs <pod> -n <ns> --follow          # stream
oc logs <pod> -n <ns> --tail=100        # last 100 lines

# Node logs (systemd journal)
oc adm node-logs <node> -u crio         # CRI-O container runtime
oc adm node-logs <node> -u kubelet      # kubelet
oc adm node-logs <node> --path=/var/log/messages
```

## Exec and Remote Shell

```bash
# Execute command in pod
oc exec <pod> -n <ns> -- ls /var/log
oc exec <pod> -n <ns> -c <container> -- cat /etc/config.yaml

# Interactive shell
oc rsh <pod>                          # opens shell
oc rsh -n <ns> <pod>

# Debug node (spawns privileged pod on host network/PID)
oc debug node/<node-name>
# Inside debug pod:
chroot /host                          # access node filesystem
systemctl status kubelet
crictl ps                             # list containers
```

## Administrative Commands

```bash
# Node management
oc adm cordon <node>                  # mark unschedulable
oc adm uncordon <node>
oc adm drain <node> --ignore-daemonsets --delete-emptydir-data

# Certificate management
oc get csr | grep Pending
oc adm certificate approve <csr-name>
oc get csr -o name | xargs oc adm certificate approve  # approve all

# RBAC
oc adm policy add-role-to-user admin <username> -n <project>
oc adm policy add-cluster-role-to-user cluster-admin <username>
oc adm policy who-can get pods -n <ns>
```

## must-gather

```bash
# Collect full cluster state (takes 5-10 minutes)
oc adm must-gather                    # default collection
oc adm must-gather --image=<custom>   # product-specific (e.g. ODF, ACM)
oc adm must-gather --dest-dir=/tmp/mg

# Inspect a specific operator
oc adm inspect clusteroperator/etcd --dest-dir=/tmp/etcd-inspect
oc adm inspect namespace/openshift-monitoring --dest-dir=/tmp/mon-inspect

# Quick cluster state snapshot
oc adm top nodes
oc adm top pods --all-namespaces
```

## Useful Aliases

```bash
alias k=kubectl
alias oc-all='oc get pods --all-namespaces | grep -v "Running\|Completed"'
alias oc-co='oc get co | grep -E "False|True.*True|True.*False.*True"'
alias oc-events='oc get events --all-namespaces --sort-by=.lastTimestamp | tail -30'
```
