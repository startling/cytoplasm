'''
These are all the functions that are used when you `cytoplasm build`.
'''

import os
import shutil
from cytoplasm import errors, interpreters, configuration
from cytoplasm.controllers import controllerclass


def copy_over(config):
    "Copy the files not beginning with '_' to the site directory"
    interpreter_dictionary = config.interpreters
    # All of the files and directories that don't begin with '_' or '.'
    to_copy = [file for file in os.listdir(".") if not
            file.startswith(("_", "."))]
    files = [file for file in to_copy if not os.path.isdir(file)]
    for file in files:
        destination = interpreters.interpreted_filename(file)
        # and pass the origin and destination to interpreters.interpret.
        interpreters.interpret(file,
                os.path.join(config.build_dir, destination))
    directories = [file for file in to_copy if os.path.isdir(file)]
    for dir in directories:
        if os.path.exists(os.path.join(config.build_dir, dir)):
            # if the directory exists, delete it.
            shutil.rmtree(os.path.join(config.build_dir, dir))
        # copy all the directories that don't start with "." or "_" completely.
        shutil.copytree(dir, os.path.join(config.build_dir, dir))


def build(dir="."):
    # Set the directory in cytoplasm.configuration, so everything gets the
    # same configuration.
    configuration.source_dir = os.path.join(os.getcwd(), dir)
    # Get the configuration file...
    config = configuration.get_config()
    # save the current working directory, so we can return to it later.
    oldwd = os.getcwd()
    # and then change directories, to the source directory.
    os.chdir(configuration.source_dir)
    # Create the build directory, if it doesn't exist
    if not os.path.exists(config.build_dir):
        os.mkdir(config.build_dir)
    copy_over(config)
    for controller, arguments in config.controllers:
        # create a controller object of the class returned by controllerclass
        controller_object = controllerclass(controller)(*arguments)
        # call the controller object
        controller_object()
    # change back to the old directory.
    os.chdir(oldwd)
