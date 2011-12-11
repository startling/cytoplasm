# This module contains the user's configurations, to be accessed like:
# `print cytoplasm.configuration.build_dir`
import os, imp

# If the user has a file called _config.py, import that.
# The user's _config.py should "from cytoplasm.defaults import *" if they want to use
# some of the defaults.
if os.path.exists("_config.py"):
    imp.load_source("_config", "_config.py")
    from _config import *
