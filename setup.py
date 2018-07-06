import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name='rubix',
    version='0.0.4',
    author='Amit Rathi',
    description='Python package to enables DevOps tasks in Jupyter Notebooks',
    long_description=open('README.md').read(),
    license='GNU Lesser General Public License v3.0',
    keywords=['DevOps', 'Jupyter', 'nurtch'],
    packages=find_packages(),
    package_data={'rubix': ['rubix/assets/css/*.css']},
    include_package_data=True,
    install_requires=[
        'plotly',
        'pandas',
        'boto3',
        'kubernetes'
    ]
)