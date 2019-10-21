#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='django-jsonfield-schema',
    version='0.1.0',
    author='Mikhail Podgurskiy',
    author_email='kmmbvnr@gmail.com',
    description='Expose JSONField data as a virtual django model fields.',
    long_description=open('README.rst').read(),
    platforms=['Any'],
    keywords=['workflow', 'django', 'bpm', 'automaton'],
    url='http://github.com/viewflow/jsonfield-schema',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    ],
    install_requires=[
        'Django>=1.11',
    ],
    packages=['jsonfield_schema'],
    include_package_data=True,
    zip_safe=False
)
