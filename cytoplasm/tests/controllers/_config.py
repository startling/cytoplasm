# import the defaults from cytoplasm
from cytoplasm.defaults import *

# have some example controllers that just copy stuff.
controllers = [
    ("copier", ["_copy", "_build"]),
    ("copier", ["_copy", "_build/copied"]),
]
