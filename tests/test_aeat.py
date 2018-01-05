from unittest.mock import Mock, PropertyMock, patch

import pytest

from tests import factories
from zeep import exceptions as zeep_exceptions
from zeep import xsd

from aeat import Config, Controller, wsdl


def test_config_as_str():
    config = Config('ens_presentation', test_mode=True)
    assert 'Servicio de Presentación ENS V4.0' in config.__str__()


@patch('aeat.Client')
def test_controller_is_built_from_config_obj(client):
    config = Mock(signed=True)
    ctrl = Controller.build_from_config(config, Mock(), Mock())
    assert isinstance(ctrl, Controller)
    assert ctrl.config.signed


@pytest.mark.parametrize('test_mode,expected_port', [
    (True, 'IE313V4Pruebas'),
    (False, 'IE313V4'),
])
def test_config_is_built_from_service_name(test_mode, expected_port):
    config = Config('ens_presentation', test_mode=test_mode)
    assert config.wsdl.endswith('IE313V4.wsdl')
    assert 'IE313V4' == config.operation
    assert 'IE313V4Service' == config.service
    assert expected_port == config.port


@patch('aeat.Controller.operation', new_callable=PropertyMock)
def test_controller_ens_query_with_valid_response(operation_patch, zeep_response):
    response = zeep_response(
        'wsdl_ens_query_ConsENSV3.wsdl', 'ens_query_valid.xml', 'ConsENSV3'
    )

    operation_patch.return_value = lambda **kwargs: response
    ctrl = Controller(Mock(), Mock())
    result = ctrl.request(factories.ENSQueryFactory())

    assert result.valid
    assert 2 == len(result.data['IMPOPE'])


@patch('aeat.Controller.operation')
def test_controller_marks_signature_as_skip_if_config_is_signed(operation_patch):
    config = Mock(signed=True)
    ctrl = Controller(Mock(), config)
    ctrl.request({'arg': 'x'})

    operation_patch.assert_called_with(arg='x', Signature=xsd.SkipValue)


@patch('aeat.Controller.operation', new_callable=PropertyMock)
def test_controller_with_99999_error(operation_patch, zeep_response):
    def response():
        return zeep_response('wsdl_ens_presentation_IE313V4.wsdl',
                             'ens_presentation_error_99999.xml', 'IE313V4')

    operation_patch.return_value = lambda **kwargs: response()
    ctrl = Controller(Mock(), Mock())
    result = ctrl.request(factories.ENSQueryFactory())

    assert not result.valid
    assert 'Mensaje REENVIABLE. Codigo[99999].' == result.error
    assert result.data is None


@patch('aeat.Controller.operation', new_callable=PropertyMock)
def test_controller_with_html_error(operation_patch, zeep_response):
    def response():
        return zeep_response('wsdl_ens_query_ConsENSV3.wsdl', 'unknown_certificate.html',
                             'ConsENSV3')

    operation_patch.return_value = lambda **kwargs: response()
    ctrl = Controller(Mock(), Mock())
    result = ctrl.request(factories.ENSQueryFactory())

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
        return zeep_response('wsdl_ens_presentation_IE313V4.wsdl',
                             'ens_presentation_success_IE328V5Sal.xml', 'IE313V4')

    operation_patch.return_value = lambda **kwargs: response()
    ctrl = Controller(Mock(), Mock(operation='IE313V4'))
    result = ctrl.request(factories.ENSPresentationFactory())

    assert result.valid
    assert '17ES004311Z0000010' == result.data


@pytest.mark.parametrize('response_xml', [
    'ens_presentation_error_IE316V4Sal.xml',
    'ens_presentation_error_IE917V4Sal.xml',
])
@patch('aeat.Controller.operation', new_callable=PropertyMock)
def test_controller_with_incorrect_responses(operation_patch, zeep_response, response_xml):
    def response():
        return zeep_response('wsdl_ens_presentation_IE313V4.wsdl', response_xml, 'IE313V4')

    operation_patch.return_value = lambda **kwargs: response()
    ctrl = Controller(Mock(), Mock(operation='IE313V4'))
    result = ctrl.request(factories.ENSPresentationFactory())

    assert not result.valid
    assert result.data is None
    assert 'AEAT response error' == result.error
