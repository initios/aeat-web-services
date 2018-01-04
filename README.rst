=================
AEAT-WEB-SERVICES
=================

.. list-table::

    * - Master
      - .. image:: https://travis-ci.org/initios/aeat-web-services.svg?branch=master
            :target: https://travis-ci.org/initios/aeat-web-services
      - .. image:: https://coveralls.io/repos/github/initios/aeat-web-services/badge.svg?branch=master
            :target: https://coveralls.io/github/initios/aeat-web-services?branch=master


Spanish Tax Agency Electronic Office (AEAT) Integration.

Make requests `AEAT Web Services <https://www2.agenciatributaria.gob.es/ADUA/internet/ws.html>`_
and sign your connection and xml using your certificate.

-----

*Integración con la Agencia Estatal de Administración Tributaria Española*

*Realiza peticiones a los* `Servicios Web de AEAT <https://www2.agenciatributaria.gob.es/ADUA/internet/ws.html>`_
*y firma tu conexión y mensajes XML utilizando tu certificado.*

Usage (English)
===============

**Example for requesting a list of ENS's.**

Initialize a Config object with the desired preconfigured service and if you want to request AEAT test or production endpoints (test_mode).
Finally initialize controller with the config and the desired certificate and make the request with your payload.

If you need more control just build the controller by hand, see build_from_config method for inspiration.

* `Preconfigured aduanet services <src/aeat/wsdl.py>`_.
* `Official AEAT Web Services <https://www2.agenciatributaria.gob.es/ADUA/internet/ws.html>`_

.. code:: python

    import aeat

    config = aeat.Config('ens_query', test_mode=True)
    ctrl = aeat.Controller.build_from_config(config, 'key.pem', 'cert.pem')
    payload = {'TraModAtBorHEA76': '1', 'ExpDatOfArr': '20110809',  'ConRefNum': '9294408'}
    result = ctrl.request(payload)

    assert result.valid, f'Error requesting aeat: {result.data}'
    assert result.data is not None


Usage (Spanish)
===============

**Ejemplo de consulta de ENSs.**

*Inicializa el objecto Config con el servicio preconfigurado y si quieres usar los endpoints de AEAT de test o de producción (test_mode).*
*Por último inicializa el controlador con la config y el certificado que gustes y realiza la petición pasándole los datos que necesites.*

*Si necesitas un mayor control simplemente construye el controlador a mano, puedes inspirarte en el método build_from_config.*

* `Lista de Servicios Preconfigurados <src/aeat/wsdl.py>`_.
* `Servicios Web oficial de AEAT <https://www2.agenciatributaria.gob.es/ADUA/internet/ws.html>`_

.. code:: python

    import aeat

    config = aeat.Config('ens_query', test_mode=True)
    ctrl = aeat.Controller.build_from_config(config, 'key.pem', 'cert.pem')
    payload = {'TraModAtBorHEA76': '1', 'ExpDatOfArr': '20110809',  'ConRefNum': '9294408'}
    result = ctrl.request(payload)

    assert result.valid, f'Error requesting aeat: {result.data}'
    assert result.data is not None


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

    $ pip install -e .
    $ pip install -r requirements_test.txt


Test
=======

.. code:: console

    $ pip install tox
    $ tox


Changelog
=========

.. list-table::

    * - 2018-04-01 Release 1.0.0-pre.1
      - Versión inicial


Usefull Links
=============

- `AEAT Web Services <https://www2.agenciatributaria.gob.es/ADUA/internet/ws.html>`_
- `Available preconfigured services <src/aeat/wsdl.py>`_
