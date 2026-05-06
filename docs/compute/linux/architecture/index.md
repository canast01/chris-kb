# Linux Architecture

Linux servers fulfill multiple infrastructure roles: application servers running RHEL or Ubuntu, Ansible control plane nodes for automation, monitoring servers, NFS/SMB file hosts, and container hosts running Docker or Podman. The standard kernel is managed via the distribution's package repositories, with systemd as the init system providing service lifecycle management. Storage is managed with LVM, enabling flexible volume resizing and snapshot support. All servers follow a common baseline regardless of role, with role-specific configuration layered on top.

| Role | Typical OS | Notes |
|---|---|---|
| Application server | RHEL 8/9, Ubuntu 22.04 | Primary workload host |
| Automation node | RHEL 9 | Ansible control plane |
| Monitoring server | Ubuntu 22.04 | Prometheus, Grafana stack |
| NFS/SMB host | RHEL 9 | Shared storage services |
| Container host | RHEL 9 | Podman/Docker workloads |
