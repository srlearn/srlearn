"""
Setup file for srlearn

Refer to https://github.com/hayesall/srlearn
"""

from setuptools import setup
from setuptools import find_packages
from codecs import open
from os import path

# Get __version__ from _meta.py
with open(path.join("srlearn", "_meta.py")) as f:
    exec(f.read())

_here = path.abspath(path.dirname(__file__))
with open(path.join(_here, "README.rst"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="srlearn",
    packages=find_packages(exclude=["tests"]),
    package_dir={"srlearn": "srlearn"},
    author="Alexander L. Hayes (hayesall)",
    author_email="alexander@batflyer.net",
    version=__version__,
    description="Python wrappers for using BoostSRL jar files.",
    long_description=LONG_DESCRIPTION,
    include_package_data=True,
    package_data={"srlearn": ["*.jar"]},
    url="https://hayesall.com",
    download_url="https://github.com/hayesall/srlearn",
    license="GPL-3.0",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="machine-learning-algorithms machine-learning statistical-learning pattern-classification artificial-intelligence",
    install_requires=["graphviz", "numpy", "scipy", "scikit-learn"],
    extras_require={
        "tests": ["coverage", "pytest"],
        "docs": ["sphinx", "sphinx_rtd_theme", "sphinx_gallery", "numpydoc", "matplotlib"],
    },
)
