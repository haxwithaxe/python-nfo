"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import os
from setuptools import setup, find_packages


__version__ = __maintainer__ = __contact__ = __license__ = __doc__ = None

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'nfo', '__init__.py'), 'r') as initfile:
	exec(initfile.read())

setup(
    name='nfo',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,
    description=__doc__.split('\n', 1)[0],
    long_description=__doc__.split('\n',1)[-1],
	url='https://github.com/haxwithaxe.net/python-nfo',
    author=__maintainer__,
    author_email=__contact__,
    license=__license__,
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
		'Topic :: Software Development :: ',
		'Topic :: Software Development :: Libraries',
		'Topic :: Text Processing :: Markup :: XML',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='kodi nfo xml development',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['lxml'],
)
