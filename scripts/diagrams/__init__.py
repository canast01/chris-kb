"""Import all diagram submodules to populate the DIAGRAMS registry."""
from . import cloud
from . import other
from . import san
from . import storage
from . import storage_dell
from . import storage_netapp
from . import vmware_apps
from . import vmware_aria
from . import vmware_core
from . import vxrail

from ._core import DIAGRAMS
