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

# Infrastrucuture to use on the generalized tests.
def delete_build_dir(fn):
    "A decorator to delete the '_build' directory in `directory` before and after a test."
    def delete_build_dir_decorated_function(directory):
        build_dir = os.path.join(directory, "_build")
        if os.path.exists(build_dir): shutil.rmtree(build_dir)
        fn(directory)
        if os.path.exists(build_dir): shutil.rmtree(build_dir)
    return delete_build_dir_decorated_function

def check(fn):
    "A decorator to check whether a built site is in good shape."
    def check_decorated_function(directory):
        fn(directory)
        build_dir = os.path.join(directory, "_build")
        # check that the build directory was created
        assert os.path.exists(build_dir)
        # test that the build directory is a directory.
        assert os.path.isdir(build_dir)
    return check_decorated_function

# Generalized tests: things to use in actual tests. 
@delete_build_dir
@check
def site_by_chdir(directory):
    "Test whether Cytoplasm works on these sites while in the sites' directories."
    os.chdir(directory)
    cytoplasm.build()

@delete_build_dir
@check
def site_at_a_distance(directory):
    "Test whether Cytoplasm works when you give cytoplasm.build a directory."
    cytoplasm.build(directory)
    check(directory)

# Actual Tests:

# This is an example site with a completely empty _config.py, but for importing the defaults.
empty_site =os.path.join(examples_directory, "empty")

def test_empty_site_by_chdir():
    "Test whether Cytoplasm works on the empty site while in the site's directory."
    site_by_chdir(empty_site)

def test_empty_site_at_a_distance():
    "Test whether Cytoplasm works when you give the empty site's directory to cytoplasm.build."
    site_at_a_distance(empty_site)

