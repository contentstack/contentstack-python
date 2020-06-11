# https://packaging.python.org/tutorials/packaging-projects/#creating-setup-py
# setup.py is the build script for setuptools.
# It tells setuptools about your package (such
# as the name and version) as well as which code files to include

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    long_description = readme.read()

import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="contentstack",
    keywords='contentstack-python',
    version="1.0.0",
    author="contentstack",
    author_email="mshaileshr@gmail.com",
    description="Contentstack is a headless CMS with an API-first approach.",
    long_description="Contentstack is a headless CMS with an API-first approach. It is a CMS that developers can use "
                     "to build powerful cross-platform applications in their favorite languages. Build your "
                     "application frontend, and Contentstack will take care of the rest",
    long_description_content_type="text/markdown",
    url="https://github.com/contentstack/contentstack-python",
    # packages=setuptools.find_packages(),
    packages=['contentstack'],
    license='MIT',
    test_suite='tests.all_tests',
    install_requires=['requests>=1.1.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Development Status :: 1 - Production/Stable',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.7',
    zip_safe=False,
)