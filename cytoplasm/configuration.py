'''
This module imports everything from the user's `_config.py` into its namespace.
So to get configuration of the current working directory, `import cytoplasm.configuration`.
'''

import os, imp
from .errors import CytoplasmError

# If the user has a file called _config.py, import that.
# The user's _config.py should "from cytoplasm.defaults import *" if they want to use
# some of the defaults.
if os.path.exists("_config.py"):
    imp.load_source("_config", "_config.py")
    from _config import *
else:
    raise CytoplasmError("You don't seem to have a configuration file at '_config.py'.")
