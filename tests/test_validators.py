from django.test.utils import override_settings
from rest_framework import serializers as rf

from aeat.rest_framework import validators


def test_adds_test_indicator_when_test_mode_is_enabled():
    class TestSerializer(validators.ValidatorBase, rf.Serializer):
        pass

    serializer = TestSerializer(data={})
    serializer.is_valid(raise_exception=True)

    assert '0' == serializer.data['TesIndMES18']


@override_settings(AEAT_TEST_MODE=False)
def test_does_not_adds_test_indicator_in_production():
    class TestSerializer(validators.ValidatorBase, rf.Serializer):
        pass

    serializer = TestSerializer(data={})
    serializer.is_valid(raise_exception=True)

    assert 'TesIndMES18' not in serializer.data
