from unittest.mock import Mock, patch

import pytest

import setup_django  # NOQA

from django.core.exceptions import ImproperlyConfigured  # isort:skip # NOQA
from django.test.utils import override_settings  # isort:skip # NOQA

from rest_framework import serializers as rf  # isort:skip # NOQA

from aeat import Result  # isort:skip # NOQA
from aeat.rest_framework import validators  # isort:skip # NOQA


@patch('aeat.rest_framework.validators.aeat.Config', Mock())
@patch('aeat.rest_framework.validators.aeat.Controller')
def test_make_aeat_request(ctrl_builder):
    ctrl_mock = Mock()
    ctrl_builder.build_from_config.return_value = ctrl_mock
    validators.make_aeat_request('ens_query', {'count': '2'})
    assert ctrl_mock.request.called_with({'count': '2'})


@override_settings(AEAT_CERT_PATH=None)
@patch('aeat.rest_framework.validators.aeat.Config', Mock())
@patch('aeat.rest_framework.validators.aeat.Controller')
def test_make_aeat_request_without_cert_path_env_var_fails(ctrl_builder):
    with pytest.raises(ImproperlyConfigured):
        validators.make_aeat_request('test_service', data={})


@override_settings(AEAT_KEY_PATH=None)
@patch('aeat.rest_framework.validators.aeat.Config', Mock())
@patch('aeat.rest_framework.validators.aeat.Controller')
def test_make_aeat_request_without_key_path_env_var_fails(ctrl_builder):
    with pytest.raises(ImproperlyConfigured):
        validators.make_aeat_request('test_service', data={})


@patch('aeat.rest_framework.validators.make_aeat_request',
       lambda x, y: Result(data=None, error='NO REENVIABLE'))
def test_aeat_request_serializer_returns_result_failed_when_request_fails():
    serializer = validators.AEATRequest()
    result = serializer.save()
    assert not result.valid


@patch('aeat.rest_framework.validators.make_aeat_request',
       lambda x, y: Result(data='xyz', error=None, raw_response='xml...'))
def test_aeat_request_serializer_returns_result_if_request_is_successfull():
    serializer = validators.AEATRequest()
    result = serializer.save()
    assert result.valid


def test_adds_test_indicator_when_test_mode_is_enabled():
    class TestSerializer(validators.AEATRequest, rf.Serializer):
        pass

    serializer = TestSerializer(data={})
    serializer.is_valid(raise_exception=True)

    assert '0' == serializer.data['TesIndMES18']


@override_settings(AEAT_TEST_MODE=False)
def test_does_not_adds_test_indicator_in_production():
    class TestSerializer(validators.AEATRequest, rf.Serializer):
        pass

    serializer = TestSerializer(data={})
    serializer.is_valid(raise_exception=True)

    assert 'TesIndMES18' not in serializer.data