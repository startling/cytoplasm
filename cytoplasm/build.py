'''
These are all the functions that are used when you `cytoplasm build`.
'''

import os, shutil
from . import errors, interpreters, configuration
from .controllers import controllerclass

def copy_over(config):
    "Copy the files not beginning with '_' to the site directory"
    interpreter_dictionary = config.interpreters
    # All of the files and directories that don't begin with '_' or '.'
    to_copy = [file for file in os.listdir(".") if not file.startswith(("_", "."))]
    files = [file for file in to_copy if not os.path.isdir(file)]
    for file in files:
        # first, try to interpret each of these files with one of the interpreters
        # if none of the interpreters match, it returns False
        # the destination, if interpreted, should be the filename without that last suffix
        destination = file.rsplit('.', 1)[0]
        if not interpreters.interpret(file, "%s/%s" %(config.build_dir, destination)):
            # otherwise, simply copy the file over
            shutil.copy2(file, config.build_dir)
    directories = [file for file in to_copy if os.path.isdir(file)]
    for dir in directories:
        if os.path.exists("%s/%s" %(config.build_dir, dir)):
            # if the directory exists, delete it.
            shutil.rmtree("%s/%s" %(config.build_dir, dir))
        # copy all the directories that don't start with "." or "_" completely.
        shutil.copytree(dir, "%s/%s" %(config.build_dir, dir))

def build():
    # Get the configuration file...
    config = configuration.get_config()
    # Create the build directory, if it doesn't exist
    if not os.path.exists(config.build_dir):
        os.mkdir(config.build_dir)
    copy_over(config)
    for controller, arguments in config.controllers:
        # create a controller object of the class returned by controllerclass
        controller_object = controllerclass(controller)(*arguments)
        # call the controller object 
        controller_object()

