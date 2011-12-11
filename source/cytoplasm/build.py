import os, shutil, imp, errors
from configuration import *

def copy_over():
    "Copy the files not beginning with '_' to the site directory"
    # All of the files that don't begin with '_':
    to_copy = [file for file in os.listdir(".") if not file.startswith("_")]
    for file in to_copy: 
        handled = False
        for ending in interpreters.keys():
            # if the file has a suffix that matches any of the interpreters,
            # parse that file with that interpreter
            if file.endswith(".%s" %(ending)): 
                interpeters[ending](file)
                handled = True
                break
        if not handled:
            # otherwise, simply copy the file over
            shutil.copy2(file, build_dir)

def build():
    # Import the user's _interpreters.py, if it exists in this directory
    if os.path.exists("_interpreters.py"): 
        interpreters_module = imp.load_source("_interpreters", "_interpreters.py")
        try:
            from _interpreters import interpreters as interpreters_imported
        except ImportError:
            # raise this error if _interpreters.py doesn't have a variable called "interpreters"
            raise errors.InterpreterError("Your _interpreters.py doesn't have anything I can use.")
        # overwrite the default interpreters dictionary with the user's
        interpreters.update(interpreters_imported)
    # Create the build directory, if it doesn't exist
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)
    copy_over()
