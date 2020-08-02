#!/usr/bin/env python

from distutils.core import setup

setup(
    name='cexio',
    version='0.1.6',
    packages=['cexio'],
    description='Python wrapper for CEX.IO',
    url='https://github.com/fasetto/python-cexio',
    author='fasetto',
    author_email='serkanbircan21@yandex.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Topic :: Office/Business :: Financial',
    ],
    include_package_data=True,
    zip_safe=False
)
