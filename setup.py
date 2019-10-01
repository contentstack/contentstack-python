# !/usr/bin/env python
# distutils/setuptools install script.
import sys
import setuptools
import os
import re

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

with open("README.md", "r") as fh:
    long_description = fh.read()

readme = 'Contentstack Python Content Delivery API SDK.\nRead full docs at: ' \
         'https://github.com/contentstack/contentstack-python.git/ '

# def get_version():
# init = open(os.path.join(ROOT, 'contentstack', '__init__.py')).read()
# return VERSION_RE.search(init).group(1)

# def read(fname):
# return open(os.path.join(os.path.dirname(__file__), fname)).read()

package = 'contentstack'

requirements = [
    'requests>=2.20.0,<3.0',
    'python-dateutil'
    'enum'
]


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)


def get_author(package):
    """
    Return package author as listed in `__author__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__author__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)


def get_email(package):
    """
    Return package email as listed in `__email__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__email__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)


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

    name='contentstack',
    version=get_version(package),
    py_modules=['contentstack'],
    scripts=['dokr'],
    url='https://github.com/contentstack/contentstack-python.git',
    license='MIT License',
    author=get_author(package),
    author_email='mshaileshr@gmail.com',
    description='Contentstack. Content Delivery APIs. ',
    tests_require=['pytest'],
    long_description=readme,
    include_package_data=True,
    test_suite='tests',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
