import os
from unittest.mock import Mock, patch

import pytest

import django

# Setup Django as soon as possible
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.django_test_app.settings')
django.setup()


from django.test.utils import override_settings

from rest_framework import serializers as rf

from aeat import Result
from aeat.rest_framework import serializers


@patch('aeat.rest_framework.serializers.aeat.Config', Mock())
@patch('aeat.rest_framework.serializers.aeat.Controller')
def test_make_aeat_request(ctrl_builder):
    ctrl_mock = Mock()
    ctrl_builder.build_from_config.return_value = ctrl_mock
    serializers.make_aeat_request('ens_query', {'count': '2'})
    assert ctrl_mock.request.called_with({'count': '2'})


@patch('aeat.rest_framework.serializers.make_aeat_request', lambda x, y: Result(data=None, error='NO REENVIABLE'))
def test_aeat_request_serializer_raises_validation_error_if_request_fails():
    serializer = serializers.AEATRequest()

    with pytest.raises(serializers.ValidationError, match='NO REENVIABLE'):
        serializer.save()


@patch('aeat.rest_framework.serializers.make_aeat_request', lambda x, y: Result(data={'data': 'xyz'}, error=None))
def test_aeat_request_serializer_returns_aeat_response_if_request_succeed():
    serializer = serializers.AEATRequest()
    assert {'data': 'xyz'} == serializer.save()


def test_adds_test_indicator_when_test_mode_is_enabled():
    class TestSerializer(serializers.TestIndicatorMixin, rf.Serializer):
        pass

    serializer = TestSerializer(data={})
    serializer.is_valid(raise_exception=True)

    assert '0' == serializer.data['TesIndMES18']


@override_settings(AEAT_TEST_MODE=False)
def test_does_not_adds_test_indicator_in_production():
    class TestSerializer(serializers.TestIndicatorMixin, rf.Serializer):
        pass

    serializer = TestSerializer(data={})
    serializer.is_valid(raise_exception=True)

    assert 'TesIndMES18' not in serializer.data