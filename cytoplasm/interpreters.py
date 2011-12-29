'''
These are some utilites used when writing and handling interpreters.
'''

import shutil
from cytoplasm import configuration
from cytoplasm.errors import InterpreterError

def SaveReturned(fn):
    '''Some potential interpreters, like Mako, don't give you an easy way to save to a destination.
    In these cases, simply use this function as a decorater.'''
    def InterpreterWithSave(source, destination, **kwargs):
        # under some circumstances, this should be able to write to file-like objects;
        # so if destination is a string, assume it's a path; otherwise, it's a file-like object
        if isinstance(destination, str):
            f = open(destination, "w")
        else:
            f = destination
        # pass **kwargs to this function.
        f.write(fn(source, **kwargs))
        f.close()
    return InterpreterWithSave

def interpret(file, destination, **kwargs):
    "Interpret a file with an interpreter according to its suffix."
    # get the list of interpreters from the configuration
    interpreters = configuration.get_config().interpreters
    # figure out the suffix of the file, to use to determine which interpreter to use
    ending = ".".join(file.split(".")[:-1])
    try:
        interpreters.get(ending, shutil.copyfile)(file, destination, **kwargs)
    except Exception as exception:
        # if the interpreter chokes, raise an InterpreterError with some useful information.
        raise InterpreterError("%s on file '%s': %s" %(ending, file, exception))

