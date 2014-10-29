from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(
    name='ckanext-virtual-library',
    version=version,
    description="WET 4.0 templates for the Canada.ca theme",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='http://github.com/thriuin',
    author_email='ross.thompson@statcan.gc.ca',
    url='http://open.canada.ca',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.virtual_library'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        virtual_library=ckanext.virtual_library.plugins:VirtualLibrary
    ''',
)
