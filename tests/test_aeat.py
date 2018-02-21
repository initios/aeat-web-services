from unittest.mock import Mock, PropertyMock, patch

import pytest

import factories_v5
from zeep import exceptions as zeep_exceptions
from zeep import xsd

from aeat import Config, Controller, wsdl


def test_config_as_str():
    config = Config('ens_presentation', test_mode=True)
    assert 'Servicio de Presentación ENS V5.0' in config.__str__()


def test_controller_is_built_from_service_name():
    ctrl = Controller.build_for_service('ens_presentation', 'cert.pem', 'key.pem', True)
    assert isinstance(ctrl, Controller)
    assert 'IE315P5SOAP' in ctrl.url


@patch('aeat.Controller.operation', new_callable=PropertyMock)
def test_controller_with_99999_error(operation_patch, zeep_response):
    def response():
        return zeep_response('enswsv5', 'ens_presentation_IE315V5.wsdl',
                             'ens_presentation_error_99999.xml', 'IE315V5')

    operation_patch.return_value = lambda **kwargs: response()
    ctrl = Controller(Mock(), Mock())
    result = ctrl.request(factories_v5.ENSPresentationFactory())

    assert not result.valid
    assert 'Mensaje REENVIABLE. Codigo[99999].' == result.error
    assert result.data is None


@patch('aeat.Controller.operation', new_callable=PropertyMock)
def test_controller_with_html_error(operation_patch, zeep_response):
    def response():
        return zeep_response('enswsv5', 'ens_presentation_IE315V5.wsdl',
                             'unknown_certificate.html',
                             'IE315V5')

    operation_patch.return_value = lambda **kwargs: response()
    ctrl = Controller(Mock(), Mock())
    result = ctrl.request(factories_v5.ENSPresentationFactory())

    assert not result.valid
    assert 'Wrong AEAT response' == result.error
    assert result.data is None


def test_controller_operation():
    service = Mock()
    service.myoperation = Mock()
    ctrl = Controller(Mock(service=service), Mock(operation='myoperation'))
    assert service.myoperation == ctrl.operation


@pytest.mark.parametrize('service_name', [
    name for name, _ in wsdl.ADUANET_SERVICES.items()
])
def test_aduanet_services_configuration(service_name):
    config = Config(service_name, True)
    assert isinstance(config, Config)
    assert config.verbose_name is not None
    assert config.wsdl is not None
    assert config.operation is not None
    assert config.port is not None
    assert config.service is not None
    assert config.signed is not None
    assert config.port.endswith('Pruebas')


@pytest.mark.parametrize('detail,exception_cls', [
    ('Wrong AEAT response', zeep_exceptions.XMLSyntaxError),
    ('Wrong AEAT response', zeep_exceptions.ValidationError),
    ('Unknown error', Exception),
])
@patch('aeat.Controller.operation', new_callable=PropertyMock)
def test_controller_operation_request_exception_handling(operation_patch, detail, exception_cls):
    def operation(arg, Signature):
        raise exception_cls

    operation_patch.return_value = operation

    config = Mock(signed=True)
    ctrl = Controller(Mock(), config)

    result = ctrl.request({'arg': 'x'})

    assert not result.valid
    assert detail == result.error


@patch('aeat.Controller.operation', new_callable=PropertyMock)
def test_controller_with_ens_presentation_success_message(operation_patch, zeep_response):
    def response():
        return zeep_response('enswsv5', 'ens_presentation_IE315V5.wsdl',
                             'ens_presentation_success_IE328V5Sal.xml', 'IE315V5')

    operation_patch.return_value = lambda **kwargs: response()
    ctrl = Controller(Mock(), Mock(operation='IE315V4'))
    result = ctrl.request(factories_v5.ENSPresentationFactory())

    assert result.valid


@patch('aeat.Controller.operation', new_callable=PropertyMock)
def test_controller_result_includes_raw_request_and_response(operation_patch, zeep_response):
    def response():
        return zeep_response('enswsv5,' 'ens_presentation_IE315V5.wsdl',
                             'ens_presentation_success_IE328V5Sal.xml', 'IE315V5')

    operation_patch.return_value = lambda **kwargs: response()
    history_plugin = Mock(last_sent='xyz', last_received='zyx')
    ctrl = Controller(Mock(), Mock(operation='IE315V4'), history_plugin)
    result = ctrl.request(factories_v5.ENSPresentationFactory())

    assert 'xyz' == result.raw_request
    assert 'zyx' == result.raw_response


@pytest.mark.parametrize('response_xml', [
    'ens_presentation_error_IE316V5Sal.xml',
    'ens_presentation_error_IE917V5Sal.xml',
])
@patch('aeat.Controller.operation', new_callable=PropertyMock)
def test_controller_with_incorrect_responses(operation_patch, zeep_response, response_xml):
    def response():
        return zeep_response('enswsv5', 'ens_presentation_IE315V5.wsdl',
                             response_xml, 'IE315V5')

    operation_patch.return_value = lambda **kwargs: response()
    ctrl = Controller(Mock(), Mock(operation='IE315V5'))
    result = ctrl.request(factories_v5.ENSPresentationFactory())

    # Response is Valid
    assert result.valid
    assert result.data is not None
    assert not result.error
