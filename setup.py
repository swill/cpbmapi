from setuptools import setup, find_packages
from codecs import open
from os import path

description = 'A minimalist wrapper around the CPBM BSS API.'
long_description = description

if path.exists('README.md'):
    import shutil
    shutil.copyfile('README.md', 'README.txt')
    # Get the long description from the README file
    with open(path.join(path.abspath(path.dirname(__file__)), 'README.txt'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='cpbmapi',
    version='0.0.2',

    description=description,
    long_description=long_description,

    url='https://github.com/swill/cpbmapi',
    author='Will Stevens',
    author_email='wstevens@cloudops.com',
    license='Apache Licence v2.0',

    packages=find_packages(exclude=['docs', 'tests*']),

    install_requires=['requests', 'docopt'],
)
