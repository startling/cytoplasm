import imp, os

def controllerclass(name):
    "Given the name of a controller's module, return that controller's class."
    fp, pathname, description = imp.find_module(name, ["_controllers/"])
    try:
        controller = imp.load_module(name, fp, pathname, description)
        return controller.info["class"]
    finally:
        if fp != None: fp.close

class Controller(object):
    "Controllers take data from some files, do stuff with it, and write it to the build directory."
    def __init__(self, data, build):
        # where this controller finds its data
        self.data_directory = data
        # where it should write files to...
        self.destination_directory = build
        # create the destination directort, if it doesn't exist
        if not os.path.exists(self.destination_directory): os.mkdir(self.destination_directory)
    
    def __call__(self):
        # do whatever needs to be done here...
        pass
