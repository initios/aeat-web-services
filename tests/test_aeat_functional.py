import pytest

from aduanet import aeat


'''
Test tagged as functional are are not run by default (see pytest.ini)
Copy .env-sample to .env and set the certificate paths

Enable the env vars with ```pipenv shell```
then run pytest specifiying the tag ```pytest -m functional```

Be aware that they are run against the AEAT (in test mode)  with your REAL certificate.
'''


@pytest.fixture
def make_aeat_test_controller(certificate_real):
    def make_controller_for_service(service_name):
        config = aeat.Config(service_name, test_mode=True)
        return aeat.Controller.build_from_config(config, *certificate_real)

    return make_controller_for_service


@pytest.mark.functional
def test_ens_presentation(make_aeat_test_controller, ens_presentation_payload):
    ctrl = make_aeat_test_controller('ens_presentation')
    result = ctrl.request(ens_presentation_payload)
    assert result.valid, result.error
    assert 'OK' == result.data  # WIP. Not sure what the response is yet


@pytest.mark.functional
def test_ens_query(make_aeat_test_controller, ens_query_payload):
    ctrl = make_aeat_test_controller('ens_query')

    result = ctrl.request(ens_query_payload)

    assert result.valid
    assert result.data['TraModAtBorHEA76'] == '1'
    assert result.data.ExpDatOfArr == '20110809'
    assert result.data['ConRefNum'] == '9294408'
    assert 770 == len(result.data.IMPOPE)
