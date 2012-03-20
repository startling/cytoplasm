# Cytoplasm
Hey! This is Cytoplasm, a simple static blogging-and-other-things generator. Cytoplasm takes some posts and templates and outputs a bunch of HTML files.  

Here are some things I think are exciting about it:

* Cytoplasm makes really portable websites. It just outputs a bunch of HTML files that you can put pretty much anywhere. The build script, `cytoplasm`, will run anywhere you have Python installed. It's tested in 2.7.2.

* It's really configurable. Almost everything Cytoplasm does is defined by your site's interpreters and controllers, which live in `_config.py` and `_controllers`, respectively. You can change anything there; interpreters are just functions with a certain decorator and controllers are just classes that inherit from `cytoplasm.controllers.Controller`.

* Cytoplasm sites work really well as Git repositories. New controllers can be installed as git submodules.

* There's a testing server that automatically rebuilds your site whenever you make a change to it -- `cytoplasm serve -r`. This makes playing with templates and controllers really simple and painless.

## Instructions

### Install
Cytoplasm is mostly beta right now. Things might change very frequently and then not at all for a few weeks. Most of the time, though, it works; if you have any questions or problems, ask!

You can install the version on PyPI, which might get a little out of date:

    pip install cytoplasm

Or you can install directly from this Git repository:

    pip install git+git://github.com/startling/cytoplasm.git

### Use
You can start a blank site in an empty directory by running `cytoplasm init bare` (though note that you must have Git installed for this to work). Cytoplasm will start you with a minimal configuration file at `_config.py` and the [blog controller](https://github.com/startling/cytoplasm-blog-controller), though you won't have any posts yet.

Posts go in `_posts` and start with a header that looks like this:

    title: An Example Post
    date: 2011/12/17
    tags: [category1, category2]

`cytoplasm build` will build your site and put the output in `_build`.

The first thing you'll want to do after you have some posts is to copy the templates from the blog controller's example templates (`_controllers/blog/templates`) to a new directory called `_templates`. In order to tell your blog controller to use these new templates, change in `_config.py`:

    ("blog", ["_posts", "_build/blog", "_controllers/blog/templates"]),

to

    ("blog", ["_posts", "_build/blog", "_templates"]),

Mess with your templates to your heart's content.

### Test
Cytoplasm comes with a built-in server for testing things locally. To use it, `cytoplasm serve`. To get Cytoplasm to rebuild the site whenever you make a change, `cytoplasm serve -r`.

### Develop
For development, you should probably clone this repository and install it with `pip install -e .`. You can test that you didn't break anything with `cytoplasm test`.

If you're messing with a controller and there's a Cytoplasm site in the current working directory, you can run all of the controllers' tests with `cytoplasm test -c`.

