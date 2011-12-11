def ImportInterpreters():
    import os, imp
    from configuration import interpreters
    if os.path.exists("_interpreters.py"):
        interpreters_module = imp.load_source("_interpreters", "_interpreters.py")
        try:
            from _interpreters import interpreters as interpreters_imported
        except ImportError:
            # raise this error if _interpreters.py doesn't have a variable called "interpreters"
            raise errors.InterpreterError("Your _interpreters.py doesn't have anything I can use.")
        # overwrite the default interpreters dictionary with the user's
        interpreters.update(interpreters_imported)
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

