from unittest.mock import Mock, PropertyMock, patch

import pytest

from aduanet import aeat, wsdl
from aduanet.tests import factories


@patch('aduanet.aeat.Client')
def test_controller_is_built_from_config_obj(client):
    assert isinstance(aeat.Controller.build_from_config(Mock(), Mock(), Mock()), aeat.Controller)


@pytest.mark.parametrize('test_mode,expected_port', [
    (True, 'IE315V4Pruebas'),
    (False, 'IE315V4'),
])
def test_config_is_built_from_service_name(test_mode, expected_port):
    config = aeat.Config('ens_presentation', test_mode=test_mode)
    assert config.wsdl.endswith('IE315V4.wsdl')
    assert 'IE315V4' == config.operation
    assert 'IE315V4Service' == config.service
    assert expected_port == config.port


@patch('aduanet.aeat.Controller.operation', new_callable=PropertyMock)
def test_controller_with_valid_response(operation_patch, zeep_response):
    response = zeep_response(
        'wsdl_ens_query_ConsENSV3.wsdl', 'ens_query_valid.xml', 'ConsENSV3'
    )

    operation_patch.return_value = lambda **kwargs: response
    ctrl = aeat.Controller(Mock(), Mock())
    result = ctrl.request(factories.ENSQuery())

    assert result.valid
    assert 2 == len(result.data['IMPOPE'])


@patch('aduanet.aeat.Controller.operation', new_callable=PropertyMock)
def test_controller_with_99999_error(operation_patch, zeep_response):
    def response():
        return zeep_response('wsdl_ens_presentation_IE315V4.wsdl',
                             'ens_presentation_error_99999.xml', 'IE313V4')

    operation_patch.return_value = lambda **kwargs: response()
    ctrl = aeat.Controller(Mock(), Mock())
    result = ctrl.request(factories.ENSQuery())

    assert not result.valid
    assert 'Mensaje REENVIABLE. Codigo[99999].' == result.error
    assert result.data is None


def test_controller_operation():
    service = Mock()
    service.myoperation = Mock()
    ctrl = aeat.Controller(Mock(service=service), Mock(operation='myoperation'))
    assert service.myoperation == ctrl.operation


@pytest.mark.parametrize('service_name', [
    name for name, _ in wsdl.ADUANET_SERVICES.items()
])
def test_aduanet_services_configuration(service_name):
    config = aeat.Config(service_name, True)
    assert isinstance(config, aeat.Config)
    assert config.verbose_name is not None
    assert config.wsdl is not None
    assert config.operation is not None
    assert config.port is not None
    assert config.service is not None
    assert config.signed is not None
    assert config.port.endswith('Pruebas')
