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


Install
=======

.. code:: console

    $ pip install aeat-web-services


Develop
=======

.. code:: console

    $ python setup.py install test


Testing
=======

.. code:: console

    $ pytest
    $ flake8 .
    $ isort
