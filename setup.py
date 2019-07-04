# !/usr/bin/env python
# distutils/setuptools install script.

from setuptools import setup, find_packages
import os
import re

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')


def get_version():
    init = open(os.path.join(ROOT, 'contentstack', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


package = 'contentstack'


def read(fname):
    """Read description from local file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = [
    'requests>=2.20.0,<3.0',
    'python-dateutil'
]

setup(

    name='contentstack',
    version=get_version(),
    packages=find_packages(exclude=['tests']),
    url='https://github.com/contentstack/contentstack-python',
    license='MIT License',
    author='Shailesh Mishra',
    author_email='shailesh.mishra@contentstack.com',
    description='Create python-based applications and use the python SDK to fetch and deliver content from Contentstack. The SDK uses Content Delivery APIs. ',
    install_requires=['requests', 'asset'],
    tests_require=['pytest'],
    long_description=read('README.rst'),
    include_package_data=True,

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
)
