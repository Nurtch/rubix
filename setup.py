import ez_setup
ez_setup.use_setuptools()

from setuptools import setup

setup(
    name='rubix',
    version='0.0.1',
    author='Amit Rathi',
    description='Python package to enables DevOps tasks in Jupyter Notebooks',
    long_description=open('README.rst').read(),
    license='GNU Lesser General Public License v3.0',
    keywords=['DevOps', 'Jupyter', 'nurtch'],
    packages=['rubix']
)