import configuration

class Controller(object):
    "Controllers take data from some files, do stuff with it, and write it to the build directory."
    def __init__(self, data, build):
        # where this controller finds its data
        self.data_directory = data
        # where it should write files to...
        self.build_dir = build
    
    def __call__(self):
        # do whatever needs to be done here...
        pass
