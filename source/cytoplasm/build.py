import os, shutil, errors, interpreters
from configuration import build_dir

def copy_over():
    "Copy the files not beginning with '_' to the site directory"
    interpreter_dictionary = interpreters.ImportInterpreters()
    # All of the files that don't begin with '_':
    to_copy = [file for file in os.listdir(".") if not file.startswith("_")]
    for file in to_copy: 
        handled = False
        for ending in interpreter_dictionary.keys():
            # if the file has a suffix that matches any of the interpreters,
            # parse that file with that interpreter
            if file.endswith(".%s" %(ending)): 
                # give the interpreter two variables -- the original place and hte destination
                # of the interpreted file.
                destination = "%s/%s" %(build_dir, file.replace(".%s" %(ending), ""))
                interpreter_dictionary[ending](file, destination)
                handled = True
                break
        if not handled:
            # otherwise, simply copy the file over
            shutil.copy2(file, build_dir)

def build():
    # Create the build directory, if it doesn't exist
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)
    copy_over()
