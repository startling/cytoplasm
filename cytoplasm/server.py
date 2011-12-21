import os, cytoplasm, sys

# make this work in either Python 2.x or 3.x
if sys.version_info.major >= 3:
    from http.server import SimpleHTTPRequestHandler
else:
    from SimpleHTTPServer import SimpleHTTPRequestHandler

def handler(rebuild):
    # build once first...
    cytoplasm.build()
    # change to the build directory, where things are to be served from.
    os.chdir(cytoplasm.configuration.build_dir)
    if rebuild:
        # if rebuild is true, return the RebuildHandler
        return RebuildHandler
    else:
        # otherwise, just return the SimpleHTTPRequestHandler
        return SimpleHTTPRequestHandler

class RebuildHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        "Send a GET request, and, if anything has changed, rebuild the site."
        # overwrite the do_GET method in SimpleHTTPRequestHandler with this.
        # it's mostly the same except for the little 'build' part here.
        f = self.send_head()
        if f:
            # ugly hack: move up one directory, build, and move back down to the build directory.
            os.chdir("..")
            # always rebuild the site. This can make things slow.
            cytoplasm.build()
            os.chdir(cytoplasm.configuration.build_dir)
            # copy the file to self.wfile...
            self.copyfile(f, self.wfile)
            f.close()


