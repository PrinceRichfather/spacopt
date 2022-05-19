#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['pandas>=0.24.2',
                'hyperactive>=4.1.1', 
                'matplotlib>=3.1', 
                'numpy>=1.20', 
                'root_numpy>=4.8.0']

test_requirements = [ ]

setup(
    author="Shakhzod Dadabaev Urazalievich",
    author_email='misis.dsu@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="spacopt is a package for bringing optimization techniques to spacal-simulation application",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown', 
    include_package_data=True,
    keywords='spacopt',
    name='spacopt',
    packages=find_packages(include=['spacopt', 'spacopt.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/PrinceRichfather/spacopt',
    version='0.3.1',
    zip_safe=False,
)
