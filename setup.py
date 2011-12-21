from distutils.core import setup

setup(
    name = "cytoplasm",
    version = "0.01",
    description = "A static, blog-aware website generator written in python.",
    packages = ['cytoplasm'],
    scripts = ['scripts/cytoplasm'],
    install_requires=['mako']
)
        
