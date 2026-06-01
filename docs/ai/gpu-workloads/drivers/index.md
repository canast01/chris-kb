# NVIDIA GPU Drivers


<div class="kb-summary">
Installing and maintaining NVIDIA drivers correctly is critical for GPU workloads. A driver mismatch between the kernel, CUDA toolkit, and frameworks is the most common source of GPU failures.
</div>
```
┌────────────────────────────────────── Ai Gpu Workloads Drivers ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        Gpu Workloads: Ai Gpu Workloads Drivers platform                       │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                    Management: Ai Gpu Workloads Drivers management console                    │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Ai Gpu Workloads Drivers infrastructure · management network · monitoring                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Gpu Workloads      = Ai Gpu Workloads Drivers platform overview and core concepts                  │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Checking Current State

```bash
# Check installed driver version
nvidia-smi

# Check kernel module version
cat /proc/driver/nvidia/version

# Check CUDA toolkit version (separate from driver)
nvcc --version

# List installed NVIDIA packages
dpkg -l | grep -i nvidia
rpm -qa | grep -i nvidia   # RHEL/CentOS
```

The NVIDIA driver includes a CUDA driver (minimum CUDA version). The CUDA toolkit is installed separately and must be compatible but can be newer than the driver's minimum.

## Installing Drivers on Ubuntu/Debian

```bash
# Add NVIDIA repository
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
dpkg -i cuda-keyring_1.1-1_all.deb
apt-get update

# Install the recommended driver (auto-detects GPU)
ubuntu-drivers autoinstall

# Or install a specific driver version
apt-get install -y nvidia-driver-535

# Reboot required after driver install
reboot

# Verify after reboot
nvidia-smi
```

## Installing Drivers on RHEL/Rocky Linux

```bash
# Add CUDA repo for RHEL 9
dnf config-manager --add-repo \
  https://developer.download.nvidia.com/compute/cuda/repos/rhel9/x86_64/cuda-rhel9.repo

# Install driver
dnf module install nvidia-driver:535

# Load kernel module
modprobe nvidia

# Verify
nvidia-smi
```

## CUDA Toolkit Installation

```bash
# Install CUDA 12.3 toolkit (Ubuntu 22.04)
apt-get install -y cuda-toolkit-12-3

# Add to PATH and LD_LIBRARY_PATH
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# Verify
nvcc --version
```

## Driver and CUDA Compatibility Matrix

| Driver Version | Max CUDA Version | Notes |
|---|---|---|
| 525.x | CUDA 12.0 | LTS branch |
| 535.x | CUDA 12.2 | Recommended stable |
| 545.x | CUDA 12.3 | |
| 550.x | CUDA 12.4 | Current LTS |
| 560.x | CUDA 12.6 | Latest production |

PyTorch and TensorFlow have their own CUDA requirements — check framework docs before choosing a driver version.

## Updating Drivers

```bash
# Check available driver versions
apt-cache search nvidia-driver

# Remove old driver before installing new one
apt-get purge nvidia-driver-535
apt-get install -y nvidia-driver-550

# On RHEL, switch module stream
dnf module switch-to nvidia-driver:550
```

Never update drivers mid-workload. Schedule updates during maintenance windows and test thoroughly — driver updates occasionally require CUDA toolkit and framework updates as well.

## DKMS and Kernel Updates

NVIDIA drivers use DKMS to rebuild the kernel module when the kernel is updated.

```bash
# Check DKMS status
dkms status

# Manually rebuild if needed
dkms autoinstall

# Pin kernel to prevent unplanned updates breaking drivers
apt-mark hold linux-image-generic linux-headers-generic
```
