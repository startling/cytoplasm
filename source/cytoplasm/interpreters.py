def SaveReturned(fn):
    '''Some potential interpreters, like Mako, don't give you an easy way to save to a destination.
    In these cases, simply use this function as a decorater.'''
    def InterpreterWithSave(file, destination, **kwargs):
        f = open(destination, "w")
        # pass **kwargs to this function.
        f.write(fn(file, **kwargs))
        f.close()
    return InterpreterWithSave
