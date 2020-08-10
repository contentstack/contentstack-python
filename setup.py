# https://packaging.python.org/tutorials/packaging-projects/#creating-setup-py
# setup.py is the build script for setuptools.
# It tells setuptools about your package (such
# as the name and version) as well as which code files to include

import os

import contentstack

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    long_description = readme.read()

setup(
    title="contentstack-python",
    name="Contentstack",
    status="Active",
    type="process",
    created="17 Jun",
    keywords=contentstack.__title__,
    version=contentstack.__version__,
    author="Contentstack",
    author_email="shailesh.mishra@contentstack.com",
    description="Contentstack is a headless CMS with an API-first approach.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/contentstack/contentstack-python",
    packages=['contentstack'],
    license='MIT',
    test_suite='tests.all_tests',
    install_requires=['requests>=1.1.0'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.6',
    zip_safe=False,
)
