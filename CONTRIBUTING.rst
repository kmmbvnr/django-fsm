Development and Contributing
============================

Running Tests
-------------

.. code-block:: console

    python -m pip install -e '.[test]'
    python tests/manage.py test testapp django_fsm.tests

The pure-Python API has to work without Django. That is checked in an
environment without it:

.. code-block:: console

    python -m pip install .
    python tests/test_standalone.py

To test across multiple Python and Django versions using ``tox``:

.. code-block:: console

    tox

Building and Checking Packages
------------------------------

.. code-block:: console

    python -m pip install build twine
    python -m build
    python -m twine check dist/*

Type Checking
-------------

The package includes ``py.typed``. The core and consumer examples are checked
with mypy and pyright:

.. code-block:: console

    python -m pip install -e '.[test,typing]'
    python -m mypy
    pyright
    PYTHONPATH=.:tests python -m mypy --config-file tests/typing/mypy-plugin.ini tests/typing/usage.py
