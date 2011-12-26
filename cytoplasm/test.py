import os, imp, shutil
import nose
import cytoplasm
'''
A nose tests suite for Cytoplasm. 
Run these by going into the cytoplasm package directory and running `nosetests`.
These work on the example sites in `cytoplasm/tests`.
'''

# Figure out where the examples are, in the cytoplasm package.
_, cytoplasm_directory, _ = imp.find_module("cytoplasm")
# this is the directory
examples_directory = os.path.join(cytoplasm_directory, "tests")

# Infrastructure to use on the generalized tests.
class Base(object):
    "This is the base that all the test classes will inherit from."
    def __init__(self, directory):
        self.directory = directory
        self.build_dir = os.path.join(directory, "_build")
    
    def delete_build_dir(self):
        "Delete the build directory."
        if os.path.exists(self.build_dir): shutil.rmtree(self.build_dir)

    def setup(self):
        "Delete all the files in the build directory already and build the site."
        self.delete_build_dir()
        cytoplasm.build(self.directory)

    def teardown(self):
        "Delete the build directory after all the tests are done."
        self.delete_build_dir()

    def basic_test(self):
        "Check for basic decency in a built cytoplasm site."
        # check that the build directory was created
        assert os.path.exists(self.build_dir)
        # check that the build directory is, in fact, a directory
        assert os.path.isdir(self.build_dir)

class TestEmpty(Base):
    "Test the empty site."
    def __init__(self):
        Base.__init__(self, os.path.join(examples_directory, "empty"))


