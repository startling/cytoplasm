'''This is a default configuration file, that should be imported in the
user's configuration.
'''

import os
import imp
import sys
from cytoplasm import controllers


# Specify the build directory, where the built site will be copied to
build_dir = "_build"

from .interpreters import SaveReturned
# A dictionary where the key of a suffix is the function that should handle
# that file. The function is given two arguments, the filename and where that
# file should be put after it's finished.
interpreters = {}


# This is a decorator that can be prepended to an interpreter function, so
# that you don't need to have the manually add each to the interpreters
# dictionary.
def Interpreter(*keys):
    # You can have as many suffixes as you want.
    def Add(fn):
        for suffix in keys:
            interpreters[suffix] = fn
    return Add


# An interpreter for mako, which will be pretty essential both for "static"
# files and for controllers to use.
import mako.lookup
import mako.template
# Mako should look for templates to include in the current directory.
# This should let you include things like "_templates/site.mako"
mako_lookup = mako.lookup.TemplateLookup(directories=['.'])


# Mako doesn't come with an easy built-in way to save the output to a
# certain file; this decorator does that.
@Interpreter("mako")
@SaveReturned
def mako_interpreter(file, **kwargs):
    # pass kwargs to the mako template
    page = mako.template.Template(file.read(), lookup=mako_lookup,
            input_encoding='utf-8')
    # this is dumb but it's the only way I can make it work.
    if sys.version_info.major == 2:
        # if it's python 2, use .encode('utf-8', 'replace')
        return page.render_unicode(**kwargs).encode('utf-8', 'replace')
    elif sys.version_info.major == 3:
        # otherwise, just render it...
        return page.render_unicode(**kwargs)


# This is a list of controllers to be used.
# Each item should be a 2-tuple containing:
# * The controller's module's name; i.e, the thing in _controllers
# * The list of arguments to use when instantiating the controller class;
#   usually at least the controller's source directory and where files
#   should be output to, in the build directory.
controllers = []
