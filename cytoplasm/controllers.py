'''These are the things used in making and using controllers.
'''

import imp
import os


def controllerclass(name):
    "Given the name of a controller's module, return that controller's class."
    fp, pathname, description = imp.find_module(name, ["_controllers/"])
    try:
        controller = imp.load_module(name, fp, pathname, description)
        return controller.info["class"]
    finally:
        if fp != None:
            fp.close()


class Controller(object):
    """Controllers take data from some files, do stuff with it,
    and write it to the build directory."""
    def __init__(self, data, destination, templates="_templates"):
        # take three arguments: the source directory, the destination
        # directory, and optionally a directory wherein the templates reside.
        self.data_directory = data
        self.destination_directory = destination
        self.templates_directory = templates
        # create the destination directory, if it doesn't exist
        if not os.path.exists(self.destination_directory):
            os.mkdir(self.destination_directory)

    def __call__(self):
        # do whatever needs to be done here...
        pass

    def template(self, name):
        """Given a name, return the name of the file in the templates directory
        that fits it."""
        # list of files that fit:
        files = [f for f in os.listdir(self.templates_directory)
                if f.startswith(name + ".")]
        # return the first file that matches, with the directory prepended.
        return os.path.join(self.templates_directory, files[0])
