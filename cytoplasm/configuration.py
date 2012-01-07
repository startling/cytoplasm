'''This module imports everything from the user's `_config.py` into its
namespace. So to get configuration of the current working directory,
`import cytoplasm.configuration`.
'''

import os
import imp
from cytoplasm.errors import CytoplasmError


# This a global variable to be shared and possibly changed across all
# of the cytoplasm modules.
source_dir = "."


def get_config(dir=None):
    # if there isn't a specified directory in the arguments,
    # use the global source_dir.
    if dir == None:
        dir = source_dir
    # If the user has a file called _config.py, import that and return the
    # module. The user's _config.py should "from cytoplasm.defaults import *"
    # if they want to use some of the defaults.
    config_file = os.path.join(dir, "_config.py")
    if os.path.exists(config_file):
        imp.load_source("_config", config_file)
        import _config
        return _config
    else:
        raise CytoplasmError(
                "You don't seem to have a configuration file at '%s'." %
                (source_dir))
