'''
This module imports everything from the user's `_config.py` into its namespace.
So to get configuration of the current working directory, `import cytoplasm.configuration`.
'''
import os, imp
from .errors import CytoplasmError

# This a global variable to be shared and possibly changed across all of the cytoplasm modules.
source_dir = "."

def get_config():
    # If the user has a file called _config.py, import that and return the module.
    # The user's _config.py should "from cytoplasm.defaults import *" if they want to use
    # some of the defaults.
    if os.path.exists(os.path.join(source_dir, "_config.py")):
        imp.load_source("_config", "_config.py")
        import _config
        return _config
    else:
        raise CytoplasmError("You don't seem to have a configuration file at '_config.py'.")
