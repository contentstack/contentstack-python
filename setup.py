# !/usr/bin/env python
# distutils/setuptools install script.

import setuptools
import os
import re

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_version():
    init = open(os.path.join(ROOT, 'contentstack', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


package = 'contentstack'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = [
    'requests>=2.20.0,<3.0',
    'python-dateutil'
]

setuptools.setup(

    name='contentstack',

    version=get_version(),
    py_modules=['contentstack'],
    scripts=['dokr'],

    url='https://github.com/contentstack/contentstack-python.git',

    license='MIT License',
    author='Shailesh Mishra',
    author_email='mshaileshr@gmail.com',

    description='Create python-based applications and use the python '
                'SDK to fetch and deliver content from '
                'Contentstack. The SDK uses Content Delivery APIs. ',

    install_requires=['requests', 'asset'],
    tests_require=['pytest'],
    long_description=read('README.md'),

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
