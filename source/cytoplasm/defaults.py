# This is a default configuration file, that will be imported before the user's configuration
import os, imp
from . import controllers

# Specify the build directory, where the built site will be copied to
build_dir = "_build"

from .interpreters import SaveReturned
# A dictionary where the key of a suffix is the function that should handle that file
# The function is given two arguments, the filename and where that file should be put 
# after it's finished
interpreters = {}

# An interpreter for mako, which will be prett essential both for "static" files and for controller
import mako.lookup, mako.template
# Mako should look for templates to include in the current directory.
# This should let you include things like "_templates/site.mako"
mako_lookup = mako.lookup.TemplateLookup(directories=['.'])
# Mako doesn't come with an easy built-in way to save the output to a certain file;
# this decorator does that.
@SaveReturned
def mako_interpreter(file, **kwargs):
    # pass kwargs to the mako template
    page = mako.template.Template(filename=file, lookup=mako_lookup)
    return page.render_unicode(**kwargs)

interpreters["mako"] = mako_interpreter

# This is a list of controllers to be used.
# Each item should be a 2-tuple containing:
# * The controller's module's name; i.e, the thing in _controllers
# * The list of arguments to use when instantiating the controller class; usually at least the 
#   controller's source directory and where files should be output to, in the build directory.
controllers = []

