'''
A unittest test suite for Cytoplasm.
These work on the example sites in `cytoplasm/tests`.
'''

import os
import imp
import shutil
import unittest
import mako
import cytoplasm
from cytoplasm import server, configuration

# Figure out where the examples are, in the cytoplasm package.
_, cytoplasm_directory, _ = imp.find_module("cytoplasm")
# this is the directory
examples_directory = os.path.join(cytoplasm_directory, "tests")


class Base(unittest.TestCase):
    """A base for testing all of the example sites. Default to the 'empty'
    example site.
    """
    def setUp(self, directory=os.path.join(examples_directory, "empty")):
        "Figure out the directories and build the site."
        self.directory = directory
        # get the site's configuration from the directory specified.
        self.configuration = configuration.get_config(self.directory)
        # get the build directory from the site's configuration
        self.build_dir = os.path.join(self.directory,
                self.configuration.build_dir)
        # delete the build directory, just in case there's something there.
        self.delete_build_dir()
        # and, finally, build the site
        cytoplasm.build(self.directory)

    def delete_build_dir(self):
        "Delete the build directory."
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

    def tearDown(self):
        "Delete the build directory after all the tests are done."
        self.delete_build_dir()

    def test_basic(self):
        "Check for basic decency in a built cytoplasm site."
        # check that the build directory was created
        self.assertTrue(os.path.exists(self.build_dir))
        # check that the build directory is, in fact, a directory
        self.assertTrue(os.path.isdir(self.build_dir))

    def test_copy_html(self):
        """Test whether building a cytoplasm site correctly copies over the
        uninterpreted files."""
        # a filter to tell whether files are html files and are not
        # configuration files.
        filter = lambda x: x.endswith(".html") and not x.startswith("_")
        # the html files in the source directory:
        in_source_dir = [file for file in os.listdir(self.directory) if
                filter(file)]
        # the html files in the build dir:
        in_build_dir = [file for file in os.listdir(self.build_dir) if
                filter(file)]
        # If nothing bad has happenned, everything in in_source_dir should be
        # in in_build_dir
        self.assertTrue(set(in_source_dir) <= set(in_build_dir))
        # Furthermore, the contents of each of these files should be the same.
        for source_path in in_source_dir:
            # open each of these files from their respective directories
            source_file = open(os.path.join(self.directory, source_path), "rb")
            built_file = open(os.path.join(self.build_dir, source_path), "rb")
            # assert that their contents are the same
            self.assertEqual(source_file.read(), built_file.read())
            # and then close each file
            source_file.close()
            built_file.close()


class TestSomeHTML(Base):
    "Test the somehtml example site."
    def setUp(self):
        Base.setUp(self, os.path.join(examples_directory, "somehtml"))

    def test_interpreter(self):
        "Test that the interpreters basically work."
        # I'm not going to do any content testing, because that's mako's job.
        # Still, I'm going to test the files are copied over and interpreted.
        # for each .mako file in the source directory.
        for file in [file for file in os.listdir(self.directory) if
                file.endswith(".mako")]:
            # the corresponding file will be the same, but without the last
            # dotted section.
            corresponding = ".".join(file.split(".")[:-1])
            # assert that there exists a corresponding file in the build
            # directory:
            self.assertTrue(os.path.exists(os.path.join(self.build_dir,
                                                        corresponding)))


class TestControllers(Base):
    "Test the controllers example site."
    def setUp(self):
        Base.setUp(self, os.path.join(examples_directory, "controllers"))

    def test_basic_controller(self):
        # for each controller configured:
        for _, [source_dir, build_dir] in self.configuration.controllers:
            # make sure the build directories were created.
            self.assertTrue(os.path.exists(os.path.join(self.directory,
                                                        build_dir)))

    def test_copier_controller(self):
        # get the controllers whose names are "copier"
        copiers = [c for c in self.configuration.controllers if
                c[0] == "copier"]
        for _, [source_dir, build_dir] in copiers:
            # for each of the files in the build directory...
            for file in os.listdir(os.path.join(self.directory, source_dir)):
                source_file = open(os.path.join(self.directory, source_dir,
                                                file), "rb")
                built_file = open(os.path.join(self.directory, source_dir,
                                                file), "rb")
                # check that they were copied correctly.
                self.assertEqual(source_file.read(), built_file.read())
                # and then close them.
                source_file.close()
                built_file.close()

if __name__ == '__main__':
    unittest.main()
