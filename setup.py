'''
Setup file for boostsrl

Refer to https://github.com/batflyer/boostsrl-python-package
'''

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Description from README

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='boostsrl',
    packages=['boostsrl'],
    author='Alexander L. Hayes (batflyer)',
    author_email='alexander@batflyer.net',
    version='0.1',
    description='Python wrappers for using BoostSRL jar files.',
    long_description=long_description,

    # boostsrl_java stores files in the user's home directory by default.
    include_package_data = True,
    data_files=[(path.expanduser('~') + '/.boostsrl_data', ['boostsrl/v1-0.jar',
                                                            'boostsrl/auc.jar']),
                (path.expanduser('~') + '/.boostsrl_data/train', ['boostsrl/train/train_bk.txt']),
                (path.expanduser('~') + '/.boostsrl_data/test', ['boostsrl/test/test_bk.txt'])],

    # Project's main homepage.
    url='https://github.com/batflyer/boostsrl-python-package',
    download_url="https://github.com/batflyer/boostsrl-python-package/archive/0.1.tar.gz",

    # License
    license='GPL-3.0',

    classifiers=[
        # Current development status
        'Development Status :: 3 - Alpha',

        # Intended Audiences
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',

        # License
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # OS
        'Operating System :: POSIX :: Linux',

        # Supported Python Versions
        # Check build status: https://travis-ci.org/batflyer/boostsrl-python-package
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        # Topic
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],

    # Relevant keywords (from boost-starai/BoostSRL)
    keywords='machine-learning-algorithms machine-learning statistical-learning pattern-classification artificial-intelligence',

    install_requires = ['subprocess32', 'graphviz'],
    extras_require={
        'test': ['coverage']
    }

)
