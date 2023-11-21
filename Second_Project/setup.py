# setup.py
from setuptools import setup, find_packages

setup(
    name='code_parser',
    version='1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas',
        'lxml',
        'requests',
        'beautifulsoup4',
        'seaborn'
    ]
)
