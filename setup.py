# -*- coding: utf-8 -*-

"""
Newgistics Python Client
~~~~~~~~~~~~~~~~~~~~~~~~
Setup for Newgistics Python Client
"""

from setuptools import setup, find_packages

setup(
    name="newgistics",
    version="0.2",
    description="A python client library for Newgistics Web API and Fulfillments API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sameerkumar18/newgistics",
    author="Sameer Kumar",
    author_email="sam@sameerkumar.website",
    license="Apache 2.0",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="api wrapper client library newgistics rest web api fulfillments pitneybowes",
    packages=find_packages(exclude=["contrib", "docs", "tests", "venv"]),
    install_requires=["requests==2.22.0", "xmltodict==0.12.0"],
    test_suite="tests",
    test_require=["python-dotenv"],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev]
    extras_require={"dev": ["sphinx", "sphinx-autobuild"], "test": ["python-dotenv"]},
)
