def ImportInterpreters():
    import os, imp
    # If the user has a file called _config.py, import that.
    # The user's _config.py should "from cytoplasm.configuration import *" if they want to use
    # some of the defaults.
    if os.path.exists("_config.py"):
        imp.load_source("_config", "_config.py")
        try:
            from _config import interpreters
        except ImportError:
            # raise this error if _interpreters.py doesn't have a variable called "interpreters"
            raise errors.InterpreterError("Your _config.py doesn't have anything I can use.")
    else:
        # otherwise, just import the default interpreters
        from configuration import interpreters
    return interpreters

def SaveReturned(fn):
    '''Some potential interpreters, like Mako, don't give you an easy way to save to a destination.
    In these cases, simply use this function as a decorater.'''
    def InterpreterWithSave(file, destination, **kwargs):
        f = open(destination, "w")
        # pass **kwargs to this function.
        f.write(fn(file, **kwargs))
        f.close()
    return InterpreterWithSave

