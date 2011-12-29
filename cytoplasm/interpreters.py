'''
These are some utilites used when writing and handling interpreters.
'''

import shutil
from cytoplasm import configuration
from cytoplasm.errors import InterpreterError

def interpreted_filename(file):
    "Intelligently return the interpreted filename of a file."
    # get the last suffix:
    suffix = file.split(".")[-1]
    # if the suffix is in interpreters.keys() the destination is everything but that last suffix
    if suffix in configuration.get_config().interpreters.keys():
        return ".".join(file.split(".")[:-1])
    # otherwise, it's the whole thing.
    else:
        return file

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

@SaveReturned
def default_interpreter(source, **kwargs):
    f = open(source)
    source_string = f.read()
    f.close()
    return source_string

def interpret(file, destination, **kwargs):
    "Interpret a file with an interpreter according to its suffix."
    # get the list of interpreters from the configuration
    interpreters = configuration.get_config().interpreters
    # figure out the suffix of the file, to use to determine which interpreter to use
    ending = file.split(".")[-1]
    interpreters.get(ending, default_interpreter)(file, destination, **kwargs)

