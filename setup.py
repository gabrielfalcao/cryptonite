# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ast
import os
import sys
from setuptools import setup, find_packages

reload(sys)
sys.setdefaultencoding('utf-8')


local_file = lambda *f: \
    open(os.path.join(os.path.dirname(__file__), *f), 'rb').read()


class VersionFinder(ast.NodeVisitor):
    VARIABLE_NAME = 'version'

    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        try:
            if node.targets[0].id == self.VARIABLE_NAME:
                self.version = node.value.s
        except:
            pass


def read_version():
    finder = VersionFinder()
    finder.visit(ast.parse(local_file('cryptonite', 'version.py')))
    return finder.version


dependencies = filter(bool, map(bytes.strip, local_file('requirements.txt').splitlines()))

# https://setuptools.readthedocs.io/en/latest/setuptools.html#adding-setup-arguments
setup(
    name='cryptonite',
    version=read_version(),
    description="\n".join([
        'Create/Manage/List GPG Keys and Encrypt/Decrypt things with them'
    ]),
    entry_points={
        'console_scripts': [
            'cryptonite-aes = cryptonite.console.main:aes',
            'cryptonite-gpg = cryptonite.console.main:gnupg',
            'cryptonite-pgp = cryptonite.console.main:gnupg',
        ],
    },
    author=u'Gabriel Falcão',
    author_email='gabriel@nacaolivre.org',
    url='https://github.com/gabrielfalcao/cryptonite',
    packages=find_packages(exclude=['*tests*']),
    install_requires=dependencies,
    include_package_data=True,
    package_data={
        'cryptonite': 'COPYING *.rst *.txt docs/source/* docs/*'.split(),
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
    ]
)


# Development Status :: 1 - Planning
# Development Status :: 2 - Pre-Alpha
# Development Status :: 3 - Alpha
# Development Status :: 4 - Beta
# Development Status :: 5 - Production/Stable
# Development Status :: 6 - Mature
# Development Status :: 7 - Inactive
