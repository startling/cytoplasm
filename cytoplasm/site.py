# -*- Coding: utf-8 -*-

import os
import imp
import shutil
from cytoplasm import interpreters
from cytoplasm.errors import CytoplasmError


class Site(object):
    "The most basic representation of a cytoplasm site."
    def __init__(self, source_directory):
        """Given a source directory, collect information about the site there,
        including configuration files, controllers, and so on.
        """
        self.source = os.path.abspath(source_directory)
        self.config = self._get_config()
        self.build_dir = os.path.join(self.source, self.config.build_dir)

    def _get_config(self):
        """Get the configuration file named `_config.py` from this site's 
        source directory.
        """
        config_file = os.path.join(self.source, "_config.py")
        if os.path.exists(config_file):
            # load the source file as a module and import it.
            imp.load_source("_config", config_file)
            import _config
            return _config
        else:
            # if there's no configuration file, raise an error.
            raise Cytoplasm_Error("You don't seem to have a configuration"
                    "file at %s" % config_file)

    def build(self, target_directory=None):
        "Optionally given a target directory, build the site."
        # if we weren't given a target directory, build into the target
        # directory specified by the configuration file.
        if target_directory == None:
            target_directory = os.path.join(self.source,
                    self.config.build_dir)
        # Create the build directory, if it doesn't exist
        if not os.path.exists(target_directory):
            os.mkdir(target_directory)
        # and copy things over
        self._copy_over(target_directory)
        # and then call all of the controllers
        for controller, arguments in self.config.controllers:
            # create a controller object of the class returned by
            # `self._get_controller` given the site and the name of the
            # controller.
            controller_class = self._get_controller(controller)
            controller_object = controller_class(self, *arguments)
            # call the controller object.
            controller_object()

    def _get_controller(self, name):
        "Given the name of a controller, return the controller's class."
        controller_dir = os.path.join(self.source, "_controllers")
        module = imp.find_module(name, [controller_dir])
        controller = imp.load_module(name, *module)
        return controller.info["class"]

    def _copy_over(self, target_directory):
        """Copy the files and directories not beginning with '_' in the source
        directory to the build directory. If they match an interpreter,
        interpret them first.
        """
        files = ((f, os.path.join(self.source, f)) for f in 
                os.listdir(self.source) if not f.startswith(("_", ".")))
        for base, full in files:
            if os.path.isfile(full):
                destination = interpreters.interpreted_filename(base, self)
                interpreters.interpret(full, 
                        os.path.join(self.build_dir, destination), self)
            elif os.path.isdir(full):
                destination = os.path.join(self.build_dir, base)
                # if the directory exists in the build directory, delete it
                if os.path.exists(destination):
                    shutil.rmtree(destination)
                # and then copy it completely to the build directory
                shutil.copytree(full, destination)
