"""contentstack - decorator heavy REST client library for Python."""

from setuptools import setup, find_packages
import os
import re

package = 'contentstack'


def read(fname):
    """Read description from local file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = [
    'requests>=2.20.0,<3.0',
    'python-dateutil'
]


def get_version():
    """Return package version as listed in `__version__` in `init.py`."""
    init_py = open('decorest/__init__.py').read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version()

setup(
    name='contentstack-python',
    version=version,
    packages=find_packages(exclude=['tests']),
    url='https://www.contentstack.com',
    license='MIT License',
    author='Shailesh Mishra',
    author_email='shailesh.mishra@contentstack.com',
    description='Create python-based applications and use the python SDK to fetch and deliver content from Contentstack. The SDK uses Content Delivery APIs. ',
    install_requires=['requests'],
    tests_require=['pytest'],
    long_description=read('README.rst'),
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'
    ]
)
