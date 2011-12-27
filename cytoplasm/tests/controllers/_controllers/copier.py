'''
A controller for testing that simply copies all of the files in its directory.
'''
import os, shutil
import cytoplasm.controllers

class CopierController(cytoplasm.controllers.Controller):
    def __call__(self):
        for file in os.listdir(self.data_directory):
            source = os.path.join(self.data_directory, file)
            destination = os.path.join(self.destination_directory, file)
            shutil.copy(source, destination)

info = {"class": CopierController}
