#!/usr/bin/env python3

import sys
from setuptools import setup
from setuptools import find_packages

if sys.version_info[:3] < (3, 7):
    raise SystemExit("You need Python 3.7+")

requirements = [
    "migen",
    "pytest",
    "jsonschema"
]

setup(
    name="unitbench",
    version="0.0.1",
    long_description_content_type="text/plain",
    description="Python hardware unit testing library for Migen modules",
    long_description=open("README.org").read(),
    author="Maxence Caron-Lasne",
    author_email="maxence.caron-lasne@lse.epita.fr",
    download_url="https://github.com/MaxenceCaronLasne/unitbench",
    packages=find_packages(),
    install_requires=requirements,
    test_suite="unitbench.tests",
    license="BSD",
    platforms=["Any"],
    keywords=["hardware", "FPGA", "HDL", "test", "migen"]
)
