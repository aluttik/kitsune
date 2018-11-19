#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import setuptools
import shutil
import sys

from kitsune import (
    __author__,
    __email__,
    __license__,
    __summary__,
    __title__,
    __url__,
    __version__,
)

here = os.path.abspath(os.path.dirname(__file__))


def get_readme():
    path = os.path.join(here, "README.md")
    with io.open(path, encoding="utf-8") as f:
        return "\n" + f.read()


class UploadCommand(setuptools.Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            shutil.rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        sys.exit()


setuptools.setup(
    name=__title__,
    version=__version__,
    description=__summary__,
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    author=__author__,
    author_email=__email__,
    url=__url__,
    packages=["kitsune"],
    license=__license__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points={"console_scripts": ["kitsune = kitsune.__main__:main"]},
    cmdclass={"upload": UploadCommand},
)
