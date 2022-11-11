###############
Getting Started
###############

1. Prerequisites
----------------

- Java (1.8, 1.11)
- Python (3.7, 3.8, 3.9, 3.10)

If you do not have Java, you might install it with your operating system's package manager.

For example, on Ubuntu:

.. code-block:: bash

    sudo apt-get install openjdk-8-jdk

macOS:

.. code-block:: bash

    brew install openjdk

Windows (with `Chocolately <https://chocolatey.org/>`_):

.. code-block:: bash

    choco install openjdk

`Jenv <https://www.jenv.be/>`_ might be a helpful way to manage Java versions as well.
If you're on MacOS it's also failry easy to set up with Homebrew.

2. Installation
---------------

The package can be installed from the Python Package Index (PyPi) with ``pip``.

.. code-block:: python

    pip install srlearn

3. Test Installation
--------------------

A simple test should be whether ``srlearn`` can be imported:

.. code-block:: python

    >>> import srlearn

If you've reached this point, you should be ready for the `User Guide <user_guide.html>`_.
