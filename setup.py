# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

setup(
    name='pserver.mailer',
    version=open('VERSION').read().strip(),
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGELOG.rst').read()),
    classifiers=[
        'Framework :: Plone :: 7.0',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url='https://pypi.python.org/pypi/pserver.elasticsearch',
    setup_requires=[
        'pytest-runner',
    ],
    license='BSD',
    zip_safe=True,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['pserver'],
    install_requires=[
        'setuptools',
        'plone.server',
        'repoze.sendmail>=4.1',
        'transaction',
        'html2text'
    ],
    tests_require=[
        'pytest',
    ],
    entry_points={
        'plone.server': [
            'include = pserver.mailer',
        ]
    }
)
