#!/usr/bin/env python
# pylint: disable=missing-docstring
import os
from setuptools import setup


def get_version():
    version_py_path = os.path.join("tcms_tap_plugin", "version.py")
    with open(version_py_path, encoding="utf-8") as version_file:
        version = version_file.read()
        return (
            version.replace(" ", "")
            .replace("__version__=", "")
            .strip()
            .strip("'")
            .strip('"')
        )


with open("README.rst", encoding="utf-8") as readme:
    LONG_DESCRIPTION = readme.read()

with open("requirements.txt", encoding="utf-8") as requirements:
    REQUIREMENTS = requirements.readlines()


setup(
    name="kiwitcms-tap-plugin",
    version=get_version(),
    packages=["tcms_tap_plugin"],
    scripts=["tcms-tap-plugin"],
    description="Test Anything Protocol (TAP) plugin for "
    "Kiwi TCMS test case management system",
    long_description=LONG_DESCRIPTION,
    author="Kiwi TCMS",
    author_email="info@kiwitcms.org",
    license="GPLv3+",
    url="https://github.com/kiwitcms/tap-plugin",
    install_requires=REQUIREMENTS,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
)
