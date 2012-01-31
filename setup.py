from distutils.core import setup

setup(
    name = "Cytoplasm",
    version = "0.05.1",
    author = "startling",
    author_email = "tdixon51793@gmail.com",
    url = "http://cytoplasm.somethingsido.com",
    keywords = ["blogging", "site compiler", "blog compiler"],
    description = "A static, blog-aware website generator written in python.",
    packages = ['cytoplasm'],
    scripts = ['scripts/cytoplasm'],
    install_requires = ['Mako'],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
        ]
)
        
