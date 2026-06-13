"""Import all diagram submodules to populate the DIAGRAMS registry."""
from . import cloud
from . import other
from . import san
from . import storage
from . import storage_dell
from . import storage_netapp
from . import vmware_apps
from . import vmware_aria
from . import vmware_aria_part2
from . import vmware_core
from . import vxrail
from . import disaster_recovery_backup
from . import disaster_recovery_replication
from . import monitoring
from . import tools
from . import automation
from . import ops
from . import governance
from . import virtualization_ops
from . import openshift
from . import evs
from . import ceph
from . import powercli
from . import learning_paths

from ._core import DIAGRAMS
