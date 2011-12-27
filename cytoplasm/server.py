'''
These are the things that are used when you `cytoplasm serve`.
'''

import os, cytoplasm, sys

# make this work in either Python 2.x or 3.x
if sys.version_info.major >= 3:
    from http.server import SimpleHTTPRequestHandler, HTTPServer
else:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer

# keep track of when things were last built in this global variable
most_recent_time = 0

# does some beginning things and returns the handler to use;
# you should give it a boolean meaning whether you want it to rebuild or not.
def initialize(rebuild):
    # build once first...
    cytoplasm.build()
    # and save the most recent time
    global most_recent_time
    most_recent_time = most_recent(".")
    # change to the build directory, where things are to be served from.
    os.chdir(cytoplasm.configuration.get_config().build_dir)
    if rebuild:
        # if rebuild is true, return the RebuildHandler
        return RebuildHandler
    else:
        # otherwise, just return the SimpleHTTPRequestHandler
        return SimpleHTTPRequestHandler

def most_recent(directory):
    "Determine the most recent modified time in the source directory, ignoring dotfiles and _build."
    build_dir = cytoplasm.configuration.get_config().build_dir
    # get the candidate files:
    files = [f for f in os.listdir(directory) if f != build_dir and not f.startswith(".")]
    # get each of their times
    times = [os.stat(os.path.join(directory, f)).st_mtime for f in files]
    # the highest time here is the most recent; return that.
    return max(times)


class RebuildHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        "Send a GET request, and, if anything has changed, rebuild the site."
        # overwrite the do_GET method in SimpleHTTPRequestHandler with this.
        # it's mostly the same except for the 'build' part here.
        # declare most_recent_time global; we'll be changing it later.
        global most_recent_time
        f = self.send_head()
        if f:
            # figure out what the most recent time edited is in the source directory
            new_recent = most_recent("..")
            # only build the site if the new most recent is more recent than the old one,
            # i.e. if one or more of the files has been edited.
            if new_recent > most_recent_time:
                # update most_recent_time
                most_recent_time = new_recent
                # Build the site from the source directory
                cytoplasm.build("..")
                # and move back down to the build directory to continue serving.
                os.chdir(config.build_dir)
            # Copy the file to self.wfile...
            self.copyfile(f, self.wfile)
            # and then close it.
            f.close()

def serve(port, rebuild, event=None):
    "Serve the Cytoplasm site."
    # (optionally take an event argument that will be set when the server is done initializing,
    # for use in testing)
    # get the handler according to whether rebuild is true or false.
    handler = initialize(rebuild)
    # make a server with the handler and the port
    httpd = HTTPServer(('', port), handler)
    # done initializing; set the event.
    if event != None: event.set()
    while True:
        httpd.handle_request()


