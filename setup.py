from distutils.core import setup

setup(
    name = "cytoplasm",
    version = "0.01",
    description = "A static, blog-aware website generator written in python.",
    package_dir = {'': 'source'},
    packages = ['cytoplasm'],
    scripts = ['cytoplasm'],
    install_requires=['mako', 'argparse']
)
        
