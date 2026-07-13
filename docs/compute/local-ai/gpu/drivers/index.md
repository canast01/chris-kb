---
tags:
  - gpu
  - ai
  - local-ai
description: "Installing and maintaining NVIDIA drivers correctly is critical for GPU workloads. A driver mismatch between the kernel, CUDA toolkit, and frameworks is..."
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


```text title="Expected output"
Fri Jan 17 14:32:45 2025
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 550.90.07    Driver Version: 550.90.07       CUDA Version: 12.4             |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| 0    NVIDIA A100-PCIE-40GB  Off         | 00:1E.0       Off   |                  0   |
+----------------------------------------+------------------------+----------------------+
| Processes:                                                       GPU Memory             |
|  GPU   GI   CI        PID   Type   Process name             Usage                      |
|  0    N/A  N/A      1847    G   /usr/lib/xorg/Xvfb       38MiB                       |
+-----------------------------------------------------------------------------------------+

NVRM version: NVIDIA UNIX x86_64 Kernel Module  550.90.07  Wed Jan 15 18:22:14 UTC 2025
GCC version:  gcc version 11.4.0 (Ubuntu 11.4.0-1ubuntu1~22.04)

nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2024 NVIDIA Corporation
Built on Thu_Jan__2_11:59:59_PST_2025
Cuda compilation tools, release 12.4, V12.4.131

ii  libnvidia-common-550:amd64           550.90.07-1ubuntu1              amd64        NVIDIA common files
ii  libnvidia-compute-550:amd64          550.90.07-1ubuntu1              amd64        NVIDIA compute utils
ii  nvidia-driver-550                    550.90.07-1ubuntu1              amd64        NVIDIA driver metapackage
ii  nvidia-utils                         550.90.07-1ubuntu1              amd64        NVIDIA driver utilities
```

!!! warning "Common errors"
    **`NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver.`** — Reload the kernel module with `sudo modprobe -r nvidia && sudo modprobe nvidia`.
    **`cat: /proc/driver/nvidia/version: No such file or directory`** — Ensure the NVIDIA kernel module is loaded by running `sudo modprobe nvidia`.
    **`nvcc: command not found`** — Install the CUDA toolkit with `sudo apt install nvidia-cuda-toolkit` or download it from NVIDIA's developer site.
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


```text title="Expected output"
Get:1 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb [13.3 kB]
Saved 13.3 kB in 2.4s
Selecting previously unselected package cuda-keyring.
Unpacking cuda-keyring (1.1-1) ...
Setting up cuda-keyring (1.1-1) ...
Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease
Get:2 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64 InRelease [1,581 B]
Reading package lists... Done
Building dependency tree... Reading state information... Done
The following packages will be upgraded:
  nvidia-driver-535 nvidia-utils
2 upgraded, 0 newly installed, 0 removed.
Processing triggers for initramfs-tools (0.142ubuntu16.1) ...
update-initramfs: Generating /boot/initramfs-img-6.1.0-21-generic.img
System rebooting...

(system reboots)

Fri Jan 17 14:32:18 2025
+-------------------------+----------------------+
| NVIDIA-SMI 535.104.05   Driver Version: 535.104.05 |
+-------------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A |
| 0  NVIDIA RTX 4090      Off  | 00:1E.0     Off |
+-------------------------+----------------------+
| GPU Memory |
| GPU   Name      Usage / Total |
| 0   NVIDIA RTX 4090   2048MiB / 24576MiB |
+-------------------------+----------------------+
```

!!! warning "Common errors"
    **`E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)`** — Run the entire script with `sudo` or prepend `sudo` to each apt command.
    **`ERROR: Unable to locate package nvidia-driver-535`** — Run `apt-get update` after adding the CUDA repository keyring before attempting to install the driver package.
    **`NVIDIA-SMI has FAILED because it couldn't communicate with the NVIDIA driver`** — Reboot the system to load the newly installed kernel module, or check `/var/log/nvidia-installer.log` for installation failures.
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


```text title="Expected output"
Adding repo from: https://developer.download.nvidia.com/compute/cuda/repos/rhel9/x86_64/cuda-rhel9.repo
repo saved to /etc/yum.repos.d/cuda-rhel9.repo

Dependencies resolved.
================================================================================
 Package                    Arch       Version           Repository      Size
================================================================================
Installing:
 nvidia-driver              x86_64     535.104.05-1      cuda-rhel9     185 M
 nvidia-driver-devel        x86_64     535.104.05-1      cuda-rhel9     892 M
 nvidia-driver-libs         x86_64     535.104.05-1      cuda-rhel9      45 M

Transaction Summary
================================================================================
Install  3 Packages

Total download size: 1.1 G
Installed size: 3.2 G
Is this ok? [y/N]: y
Downloading Packages:
[100%] Complete!
Running transaction
Installing : nvidia-driver-libs-535.104.05-1.x86_64                      1/3
Installing : nvidia-driver-535.104.05-1.x86_64                           2/3
Installing : nvidia-driver-devel-535.104.05-1.x86_64                     3/3
Complete!

(no output — command completes silently)

Fri Jan 17 14:32:45 2025
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.104.05    Driver Version: 535.104.05    CUDA Version: 12.2             |
+-----------------------------------------------------------------------------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC           |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M.            |
|   0  NVIDIA A100-PCIE-40GB  Off  | 00:1E.0     Off |                  0 |
| N/A   32C    P0    42W / 250W |      0MiB / 40960MiB |      0%      Default |
+-----------------------------------------------------------------------------------------+
```

!!! warning "Common errors"
    **`Error: Unable to find a match: nvidia-driver:535`** — Verify the CUDA repo was added successfully with `dnf repolist` and check your RHEL 9 architecture matches x86_64.
    **`modprobe: FATAL: Module nvidia not found in /lib/modules/5.14.0-427.el9.x86_64/kernel/`** — Rebuild the kernel module with `dkms install nvidia/535.104.05` or reinstall the driver with `dnf reinstall nvidia-driver`.
    **`NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver`** — Reboot the system with `reboot` to fully load the kernel module and reinitialize the GPU.
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


```text title="Expected output"
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following NEW packages will be installed:
  cuda-toolkit-12-3 cuda-runtime-12-3 cuda-libraries-12-3
Processing triggers for libc-bin (2.35-0ubuntu3.4) ...
Setting up cuda-toolkit-12-3 (12.3.107-1) ...
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2023 NVIDIA Corporation
Built on Sep_8_2023
Cuda compilation tools, release 12.3, V12.3.107
Build cuda_12.3.r12.3/compiler.33567101_0
```

!!! warning "Common errors"
    **`E: Unable to locate package cuda-toolkit-12-3`** — Ensure the NVIDIA CUDA repository is added with `apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC` and `add-apt-repository ppa:graphics-drivers/ppa` before running apt-get.
    **`nvcc: command not found`** — Run `source ~/.bashrc` to reload the environment variables, or verify the CUDA installation path matches your system with `ls /usr/local/cuda/bin/nvcc`.
    **`error while loading shared libraries: libcuda.so.1`** — Install the NVIDIA GPU driver separately with `apt-get install -y nvidia-driver-545` before or after the toolkit installation.
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


```text title="Expected output"
nvidia-driver - NVIDIA driver metapackage
nvidia-driver-390 - NVIDIA driver metapackage
nvidia-driver-418 - NVIDIA driver metapackage
nvidia-driver-535 - NVIDIA driver metapackage
nvidia-driver-550 - NVIDIA driver metapackage
nvidia-driver-560 - NVIDIA driver metapackage
...
Reading package lists... Done
Building dependency tree... Done
The following packages will be removed:
  nvidia-driver-535 nvidia-driver-535-server nvidia-dkms-535
Processing triggers for initramfs-tools (0.142ubuntu16.04.1) ...
update-initramfs: Generating /boot/initrd.img-5.15.0-1234-generic
Setting up nvidia-driver-550 (550.127.05-1~ubuntu22.04.1) ...
nvidia-smi
NVIDIA-SMI 550.127.05    Driver Version: 550.127.05
GPU Name                 Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
GPU 0: NVIDIA A100 80GB  On   | 00:1E.0     Off |                  0 |
GPU 1: NVIDIA A100 80GB  On   | 00:1F.0     Off |                  0 |
```

!!! warning "Common errors"
    **`E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)`** — Run the command with `sudo` or as root user.
    **`ERROR: Unable to locate package nvidia-driver-550`** — Run `apt-get update` first to refresh the package cache, then retry the installation.
    **`Error: No matching Modules to switch to`** — Verify the module stream exists with `dnf module list nvidia-driver` and use the correct version string (e.g., `550-dkms` instead of `550`).
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


```text title="Expected output"
nvidia-driver-535, 6.1.0-13-generic, x86_64: installed
nvidia-driver-535, 6.1.0-14-generic, x86_64: built
nvidia-driver-535, 6.1.0-15-generic, x86_64: installed
amdgpu-dkms, 6.1.0-15-generic, x86_64: installed
amdgpu-dkms, 6.1.0-14-generic, x86_64: installed
Autoinstalling DKMS modules...
Building module: nvidia-driver-535
Kernel preparation unnecessary for this kernel. Skipping...
Building module for kernel 6.1.0-15-generic
Module build completed successfully.
Installing module: nvidia-driver-535
Kernel preparation unnecessary for this kernel. Skipping...
Installing module for kernel 6.1.0-15-generic
Module install completed successfully.
linux-image-generic set to manually installed.
linux-headers-generic set to manually installed.
```

!!! warning "Common errors"
    **`Error! Could not locate dkms.conf file.`** — Verify the driver package is installed with `apt install nvidia-driver-535` and contains `/usr/src/nvidia-driver-535/dkms.conf`.
    **`E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)`** — Run the entire block with `sudo` or as root user.
    **`WARNING: apt-mark does not have a stable CLI interface. Use with caution in scripts.`** — This is informational; the hold command still succeeds, but consider using `apt-mark hold --quiet` in automation.