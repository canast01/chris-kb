"""Import all diagram submodules to populate the DIAGRAMS registry."""
from . import cloud
from . import other
from . import storage
from . import vmware_apps
from . import vmware_aria
from . import vmware_core
from . import vxrail

from ._core import DIAGRAMS
