import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

exec(open('rubix/version.py').read()) # loads __version__

setup(name='rubix',
      version=__version__,
      author='Amit',
    description='',
    long_description=open('README.rst').read(),
    license='see LICENSE.txt',
    keywords="",
    packages= find_packages(exclude='docs'))
