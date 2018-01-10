import os

import pytest

import factories
import setup_django  # NOQA

import aeat
import aeat.rest_framework.serializers as serializers


'''
Test tagged as functional are are not run by default (see setup.cfg)
Copy .env-sample to .env and set the certificate paths

Enable the env vars with ```export `cat .env````
then run pytest specifiying the tag ```pytest -m functional```

Be aware that they are run against the AEAT (in test mode) with your REAL certificate.
'''


@pytest.fixture
def make_aeat_test_controller(certificate_real):
    def make_controller_for_service(service_name):
        config = aeat.Config(service_name, test_mode=True)
        return aeat.Controller.build_from_config(config, *certificate_real)

    return make_controller_for_service


@pytest.mark.functional
def test_ens_presentation(make_aeat_test_controller):
    ctrl = make_aeat_test_controller('ens_presentation')
    result = ctrl.request(factories.ENSPresentationFactory(
        MesSenMES3=os.environ.get('AEAT_VAT_NUMBER', 'X12345678')
    ))
    assert result.valid, result.error

    assert 'OK' == result.data  # WIP. Not sure what the response is yet


@pytest.mark.functional
def test_ens_modification(make_aeat_test_controller):
    ctrl = make_aeat_test_controller('ens_modification')
    result = ctrl.request(factories.ENSPresentationFactory(
        MesSenMES3=os.environ.get('AEAT_VAT_NUMBER', 'X12345678')
    ))
    assert result.valid, result.error

    assert 'OK' == result.data  # WIP. Not sure what the response is yet


@pytest.mark.functional
def test_ens_query(make_aeat_test_controller):
    ctrl = make_aeat_test_controller('ens_query')

    result = ctrl.request(factories.ENSQueryFactory())

    assert result.valid
    assert result.data['TraModAtBorHEA76'] == '1'
    assert result.data.ExpDatOfArr == '20110809'
    assert result.data['ConRefNum'] == '9294408'
    assert 770 == len(result.data.IMPOPE)


@pytest.mark.functional
def test_exs(make_aeat_test_controller):
    payload = factories.EXSFactory(MesSenMES3=os.environ.get('AEAT_VAT_NUMBER', 'X12345678'))
    serializer = serializers.EXSSerializer(data=payload)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    # ctrl = make_aeat_test_controller('exs_presentation')
    # result = ctrl.request(factories.ENSPresentationFactory(
    #     MesSenMES3=os.environ.get('AEAT_VAT_NUMBER', 'X12345678')
    # ))
    # assert result.valid, result.error

    # assert 'OK' == result.data  # WIP. Not sure what the response is yet
