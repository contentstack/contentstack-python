# !/usr/bin/env python
# distutils/setuptools install script.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys
import setuptools
import os
import re

ROOT = os.path.dirname(__file__)

VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

with open("README.md", "r") as fh:
    long_description = fh.read()

package = 'contentstack'
requirements = [
    "requests",
    "python-dateutil"
]


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    get_file = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", get_file, re.MULTILINE).group(1)


def get_author(package):
    """
    Return package author as listed in `__author__` in `init.py`.
    """
    get_file = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__author__ = ['\"]([^'\"]+)['\"]",
                     get_file, re.MULTILINE).group(1)


def get_email(package):
    """
    Return package email as listed in `__email__` in `init.py`.
    """
    get_file = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__email__ = ['\"]([^'\"]+)['\"]",
                     get_file, re.MULTILINE).group(1)


# python setup.py publish
if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    args = {'version': get_version(package)}
    print("Pushing tags to GitHub:")
    os.system("git tag -a %(version)s -m 'version %(version)s'" % args)
    os.system("git push --tags")
    os.system("git push")
    sys.exit()

setuptools.setup(
    name=package,
    version=get_version(package),
    author=get_author(package),
    author_email='mshaileshr@gmail.com',
    description="Python SDK for Contentstack's Content Delivery API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    keywords='contentstack content delivery API, CMS',
    url='https://github.com/contentstack/contentstack-python.git',
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.6',
    py_modules=['contentstack'],
    license='MIT License',
    tests_require=['pytest'],
    include_package_data=True,
    test_suite='tests',
)
