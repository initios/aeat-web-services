=================
AEAT-WEB-SERVICES
=================

.. list-table::

    * - Master
      - .. image:: https://travis-ci.org/initios/aeat-web-services.svg?branch=master
            :target: https://travis-ci.org/initios/aeat-web-services
      - .. image:: https://coveralls.io/repos/github/initios/aeat-web-services/badge.svg?branch=master
            :target: https://coveralls.io/github/initios/aeat-web-services?branch=master


Prerequisites
=============

Install xmlsec prerequisites.
Check https://github.com/mehcode/python-xmlsec

Develop
=======

This project is using `pipenv <https://docs.pipenv.org/>`_ to manage dependencies.

To start to work just use ``pipenv install``.
This command will take care of creating the virtual environment
and installing required packages
and to activate it.

.. code:: console

    $ pipenv install --dev

To activate this project's virtualenv, run the following:

.. code:: console

    $ pipenv shell

To deactivate just type ``exit`` or Control+D.

It is also possible to run on a command basis:

.. code:: console

    $ pipenv run python manage.py runserver


Testing
=======

.. code:: console

    $ pytest
    $ flake8 .
    $ isort
