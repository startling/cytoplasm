'''
A nose tests suite for Cytoplasm. 
Run these by going into the cytoplasm package directory and running `nosetests`.
These work on the example sites in `cytoplasm/tests`.
'''

import os, imp, shutil
import nose, mako
import cytoplasm
from cytoplasm import server, configuration

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
        self.configuration = configuration.get_config(directory)
    
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

    def copy_html_test(self):
        "Test whether building a cytoplasm site correctly copies over the uninterpreted files."
        # a filter to tell whether files are html files and are not configuration files.
        filter = lambda x: x.endswith(".html") and not x.startswith("_")
        # the html files in the source directory:
        in_source_dir = [file for file in self.directory if filter(file)]
        # the html files in the build dir:
        in_build_dir = [file for file in self.build_dir if filter(file)]
        # If nothing bad has happened, both of these lists should be equal.
        assert in_source_dir == in_build_dir
        # Furthermore, the contents of each of these files should be the same.
        for source_file, built_file in zip(in_source_dir, in_build_dir):
            # open each of these files from their respective directories
            source_file = open(os.path.join(self.directory, source_file))
            built_file = open(os.path.join(self.build_dir, built_file))
            # assert that their contents are the same
            assert source_file.read() == built_file.read()
            # and then close each file
            source_file.close()
            built_file.close()

# The classes for different example sites:
# I'd love for this to be generator that acts as a class factory, but I can't even find if I can do
# it in nose. Sigh.

class TestEmpty(Base):
    "Test the empty site."
    def __init__(self):
        Base.__init__(self, os.path.join(examples_directory, "empty"))

class TestSomeHTML(Base):
    "Test the somehtml example site."
    def __init__(self):
        Base.__init__(self, os.path.join(examples_directory, "somehtml"))
    
    def interpreter_test(self):
        "Test that the interpreters basically work."
        # I'm not going to do any content testing, because that's mako's job.
        # Still, I'm going to test the files are copied over and interpreted.
        # for each .mako file in the source directory.
        for file in [file for file in os.listdir(self.directory) if file.endswith(".mako")]:
            # the corresponding file will be the same, but without the last dotted section.
            corresponding = ".".join(file.split(".")[:-1])
            # assert that there exists a corresponding file in the build directory:
            assert os.path.exists(os.path.join(self.build_dir, corresponding))

class TestControllers(Base):
    "Test the controllers example site."
    def __init__(self):
        Base.__init__(self, os.path.join(examples_directory, "controllers"))

    def basic_controller_test(self):
        # for each controller configured:
        for controller, [source_dir, build_dir] in self.configuration.controllers:
            # make sure the build directories were created.
            assert os.path.exists(os.path.join(self.directory, build_dir))

    def copier_controller_test(self):
        # get the controllers whose names are "copier"
        copiers = [c for c in self.configuration.controllers if c[0] == "copier"]
        for _, [source_dir, build_dir] in copiers:
            # for each of the files in the build directory...
            for file in os.listdir(os.path.join(self.directory, source_dir)):
                source_file = open(os.path.join(self.directory, source_dir, file))
                built_file = open(os.path.join(self.directory, source_dir, file))
                # check that they were copied correctly.
                assert source_file.read() == built_file.read()

