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
    payload = factories.ENSPresentationFactory(MesIdeMES19='TEST10001')
    serializer = serializers.ENSPresentationSerializer(data=payload)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    controller = make_aeat_test_controller('ens_presentation')
    result = controller.request(serializer.data)

    assert result.valid, f'Error: {result.error} | Raw \n: {result.raw_response}'
    assert result.data


@pytest.mark.functional
def test_ens_modification(make_aeat_test_controller):
    payload = factories.ENSModificationFactory(MesIdeMES19='TEST20001')
    serializer = serializers.ENSModificationSerializer(data=payload)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    controller = make_aeat_test_controller('ens_modification')
    result = controller.request(serializer.data)

    assert result.valid, f'Error: {result.error} | Raw \n: {result.raw_response}'
    assert result.data


@pytest.mark.functional
def test_ens_query(make_aeat_test_controller):
    payload = factories.ENSQueryFactory()
    serializer = serializers.ENSQuerySerializer(data=payload)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    controller = make_aeat_test_controller('ens_query')
    result = controller.request(serializer.data)

    assert result.valid, f'Error: {result.error} | Raw \n: {result.raw_response}'
    assert 770 == len(result.data.IMPOPE)


@pytest.mark.functional
def test_exs(make_aeat_test_controller):
    payload = factories.EXSFactory(MesIdeMES19='TEST30001')
    serializer = serializers.EXSSerializer(data=payload)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    controller = make_aeat_test_controller('exs_presentation')
    result = controller.request(serializer.data)

    assert result.valid, f'Error: {result.error} | Raw \n: {result.raw_response}'
    assert result.data
