from distutils.core import setup

setup(
    name = "cytoplasm",
    version = "0",
    description = "A static, blog-aware website generator written in python.",
    package_dir = {'': 'source'},
    packages = ['cytoplasm'],
    scripts = ['cytoplasm']
)
        
