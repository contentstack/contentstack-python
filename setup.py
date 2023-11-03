# https://packaging.python.org/tutorials/packaging-projects/#creating-setup-py
# setup.py is the build script for setuptools.
# It tells setuptools about your package (such
# as the name and version) as well as which code files to include

import os
import re
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

package = "contentstack"

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    long_description = readme.read()

requirements = [
    'requests>=2.20.0,<3.0',
    'python-dateutil'
]

setup(
    title="contentstack-python",
    name="Contentstack",
    status="Active",
    type="process",
    created="09 Jun 2020",
    keywords="contentstack-python",
    version=get_version(package),
    author="Contentstack",
    author_email="shailesh.mishra@contentstack.com, sunil.lakshman@contentstack.com" ,
    description="Contentstack is a headless CMS with an API-first approach.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/contentstack/contentstack-python",
    packages=['contentstack'],
    license='MIT',
    test_suite='tests',
    install_requires=requirements,
    include_package_data=True,
    universal=1,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    zip_safe=False,
)
