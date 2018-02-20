import pytest

import factories_v2
import factories_v5
import setup_django  # NOQA

import aeat
import aeat.rest_framework.validators as validators


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
    payload = factories_v5.ENSPresentationFactory(MesIdeMES19='TEST10002')
    serializer = validators.ENSPresentationValidator(data=payload)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    controller = make_aeat_test_controller('ens_presentation')
    result = controller.request(serializer.data)

    assert result.valid, f'Error: {result.error} | Raw \n: {result.raw_response}'
    assert result.data


@pytest.mark.functional
def test_ens_modification(make_aeat_test_controller):
    payload = factories_v5.ENSModificationFactory(MesIdeMES19='TEST20001')
    serializer = validators.ENSModificationValidator(data=payload)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    controller = make_aeat_test_controller('ens_modification')
    result = controller.request(serializer.data)

    assert result.valid, f'Error: {result.error} | Raw \n: {result.raw_response}'
    assert result.data


@pytest.mark.functional
def test_exs_presentation(make_aeat_test_controller):
    payload = factories_v2.EXSPresentationFactory(MesIdeMES19='TEST30005')
    serializer = validators.EXSPresentationValidator(data=payload)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    controller = make_aeat_test_controller('exs_common')
    result = controller.request(serializer.data)

    assert result.valid, f'Error: {result.error} | Raw \n: {result.raw_response}'
    assert result.data


@pytest.mark.functional
def test_exs_modification(make_aeat_test_controller):
    payload = factories_v2.EXSModificationFactory(MesIdeMES19='TEST30003')
    serializer = validators.EXSModificationValidator(data=payload)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    controller = make_aeat_test_controller('exs_common')
    result = controller.request(serializer.data)

    assert result.valid, f'Error: {result.error} | Raw \n: {result.raw_response}'
    assert result.data


@pytest.mark.functional
def test_exs_cancellation(make_aeat_test_controller):
    payload = factories_v2.EXSCancellationFactory(MesIdeMES19='TEST30003')
    serializer = validators.EXSCancellationValidator(data=payload)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    controller = make_aeat_test_controller('exs_common')
    result = controller.request(serializer.data)

    assert result.valid, f'Error: {result.error} | Raw \n: {result.raw_response}'
    assert result.data
