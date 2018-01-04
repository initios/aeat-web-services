=================
AEAT-WEB-SERVICES
=================

Spanish Tax Agency Electronic Office (AEAT) Integration

*Integración con la Agencia Estatal de Administración Tributaria*

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


Usage
=====

See list of `preconfigured aduanet services`_.

.. _relative link: src/aeat/wsdl.py

.. code:: python

    # Make a Config object based on a AEAT SOAP endpoint to configure the controller
    config = Config('ens_query', test_mode=True)

    # Pass your cert and key to sign the XML and the HTTP Conection
    ctrl = Controller.build_from_config(config, 'key.pem', 'cert.pem')
    payload = {'TraModAtBorHEA76': '1', 'ExpDatOfArr': '20110809',  'ConRefNum': '9294408'}
    result = ctrl.request(**payload)

    assert result.valid, 'Error requesting aeat: %s', result.data
    assert result.data is not None


Install
=======

.. code:: console

    $ pip install aeat-web-services


Develop
=======

.. code:: console

    $ pip install -e .
    $ pip install -r requirements_test.txt


Testing
=======

.. code:: console

    $ pip install tox
    $ tox


Changelog
=========

.. list-table::

    * - 2018-04-01 Release 1.0.0-pre.1
      - Versión inicial
