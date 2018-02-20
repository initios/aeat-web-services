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

    config = aeat.Config('ens_presentation', test_mode=True)
    ctrl = aeat.Controller.build_from_config(config, 'cert.pem', 'key.pem')
    result = ctrl.request(payload)  # See factories for examples

    assert result.valid, f'Error requesting aeat: {result.error}'
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

    config = aeat.Config('ens_presentation', test_mode=True)
    ctrl = aeat.Controller.build_from_config(config, 'cert.pem', 'key.pem')
    result = ctrl.request(payload)  # Ver factories para ejemplos

    assert result.valid, f'Error requesting aeat: {result.error}'
    assert result.data is not None


Django Rest Framework
=====================

Several AEAT Validators and Serializers are provided.

- Validators: Validate input data to send to AEAT
- Serializers: Serialize AEAT request

.. code:: python

    from aeat.rest_framework import validators

    validator = validators.ENSPresentationValidator(data=payload)
    assert validator.is_valid(raise_exception=True)

    # Send the request to AEAT
    import aeat

    config = aeat.Config(service_name, test_mode=settings.AEAT_TEST_MODE)
    ctrl = aeat.Controller.build_from_config(config, cert_path, key_path)
    result = ctrl.request(validator.data)
    assert result.valid

    # Parse the response
    from aeat.rest_framework import serializers

    serializer = serializers.get_class_for_aeat_response(data=result.data)
    assert serializer.is_valid(raise_exception=False)
    assert {'mrn': 'XXXX'} == serializer.data
    assert not serializer.is_error


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

    $ python setup.py develop
    $ pip install -r requirements_test.txt


Test
=======

.. code:: console

    $ pip install tox
    $ tox


Releases
=========

https://github.com/initios/aeat-web-services/releases


Usefull Links
=============

- `AEAT Web Services <https://www2.agenciatributaria.gob.es/ADUA/internet/ws.html>`_
- `Available preconfigured services <src/aeat/wsdl.py>`_
- `Structure, rules and conditions <http://www.agenciatributaria.es/static_files/AEAT/Aduanas/Contenidos_Privados/Procedimientos_aduaneros/Proyecto_ICS/Descripcion_tecnica_del_proyecto/Estructurav950.pdf>`_
