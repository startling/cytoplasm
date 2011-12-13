import os, shutil, errors, interpreters, configuration
from controllers import controllerclass

def copy_over():
    "Copy the files not beginning with '_' to the site directory"
    interpreter_dictionary = configuration.interpreters
    # All of the files and directories that don't begin with '_' or '.'
    to_copy = [file for file in os.listdir(".") if not file.startswith(("_", "."))]
    files = [file for file in to_copy if not os.path.isdir(file)]
    for file in files:
        handled = False
        for ending in interpreter_dictionary.keys():
            # if the file has a suffix that matches any of the interpreters,
            # parse that file with that interpreter
            if file.endswith(".%s" %(ending)): 
                # give the interpreter two variables -- the original place and hte destination
                # of the interpreted file.
                destination = "%s/%s" %(configuration.build_dir, file.replace(".%s" %(ending), ""))
                interpreter_dictionary[ending](file, destination)
                handled = True
                break
        if not handled:
            # otherwise, simply copy the file over
            shutil.copy2(file, configuration.build_dir)
    directories = [file for file in to_copy if os.path.isdir(file)]
    for dir in directories:
        # copy all the directories that don't start with "." or "_" completely.
        shutil.copytree(dir, "%s/%s" %(configuration.build_dir, dir))

def build():
    # Create the build directory, if it doesn't exist
    if not os.path.exists(configuration.build_dir):
        os.mkdir(configuration.build_dir)
    copy_over()
    for controller, arguments in configuration.controllers:
        # create a controller object of the class returned by controllerclass
        controller_object = apply(controllerclass(controller), arguments)
        # call the controller object 
        controller_object()
        

