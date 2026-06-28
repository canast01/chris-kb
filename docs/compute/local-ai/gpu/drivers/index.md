---
tags:
  - gpu
  - ai
  - local-ai
---
# NVIDIA GPU Drivers

<div class="kb-summary">
Installing and maintaining NVIDIA drivers correctly is critical for GPU workloads. A driver mismatch between the kernel, CUDA toolkit, and frameworks is the most common source of GPU failures.
</div>

```d2
direction: down

checking_current_state: "Checking Current State" {shape: rectangle}
installing_drivers_on_ubuntudebian: "Installing Drivers on Ubuntu/Debian" {shape: rectangle}
installing_drivers_on_rhelrocky_linu: "Installing Drivers on RHEL/Rocky Linux" {shape: rectangle}
cuda_toolkit_installation: "CUDA Toolkit Installation" {shape: rectangle}
driver_and_cuda_compatibility_matrix: "Driver and CUDA Compatibility Matrix" {shape: rectangle}
updating_drivers: "Updating Drivers" {shape: rectangle}

checking_current_state -> installing_drivers_on_ubuntudebian: uses
installing_drivers_on_ubuntudebian -> installing_drivers_on_rhelrocky_linu: uses
installing_drivers_on_rhelrocky_linu -> cuda_toolkit_installation: uses
cuda_toolkit_installation -> driver_and_cuda_compatibility_matrix: uses
driver_and_cuda_compatibility_matrix -> updating_drivers: uses
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
