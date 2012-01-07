'''Some errors that can be raised...'''


class CytoplasmError(Exception):
    pass


class ControllerError(CytoplasmError):
    pass


class InterpreterError(CytoplasmError):
    pass
