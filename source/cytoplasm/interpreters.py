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
    from .configuration import interpreters
    for ending in interpreters.keys():
        # if the file has a suffix that matches any of the interpreters,
        # parse that file with that interpreter
        if file.endswith(".%s" %(ending)):
            # give the interpreter two variables -- the original place and hte destination
            # of the interpreted file.
            interpreters[ending](file, destination, **kwargs)
            handled = True
            return True
    return False

