import pytest

import setup_django  # NOQA

from aeat.rest_framework import serializers


def test_ens_serializer(zeep_response):
    aeat_response = zeep_response(
        'wsdl_ens_presentation_IE315V4.wsdl', 'ens_presentation_success_IE328V4Sal.xml', 'IE315V4'
    )

    serializer = serializers.ENSSerializer(data=aeat_response)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    assert {'mrn': '17ES004311Z0000010'} == serializer.data


def test_exs_serializer(zeep_response):
    aeat_response = zeep_response(
        'wsdl_exs_IE615V2.wsdl', 'exs_presentation_success_IE628V2Sal.xml', 'IE615V2'
    )

    serializer = serializers.EXSSerializer(data=aeat_response)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    assert {'mrn': '17ES00361160001234',
            'item_number_involved': 0, 'customs_intervention_code': 'V'} == serializer.data


@pytest.mark.parametrize('url,response,operation,expected,is_error,expected_data', [
    # ENS
    ('wsdl_ens_presentation_IE315V4.wsdl', 'ens_presentation_success_IE328V4Sal.xml', 'IE315V4',
     serializers.ENSSerializer, False, {'mrn': '17ES004311Z0000010'}),

    ('wsdl_ens_presentation_IE315V4.wsdl', 'ens_presentation_error_IE316V4Sal.xml', 'IE315V4',
     serializers.ENSFunctionalErrorSerializer, True,
     {'type': '12', 'pointer': 'MES.MesSenMES3', 'reason': '1234-Message Sender is not valid'}),

    # EXS
    ('wsdl_exs_IE615V2.wsdl', 'exs_presentation_success_IE628V2Sal.xml', 'IE615V2',
     serializers.EXSSerializer, False,
     {'mrn': '17ES00361160001234', 'customs_intervention_code': 'V', 'item_number_involved': 0}),
])
def test_get_serializer_for_mapped_response(zeep_response, url, response, operation, expected,
                                            is_error, expected_data):
    aeat_response = zeep_response(url, response, operation)
    serializer_cls = serializers.get_class_for_aeat_response(aeat_response)
    assert expected == serializer_cls

    # It should parse the response without errors
    serializer = serializer_cls(data=aeat_response)
    assert is_error == serializer.is_error
    assert serializer.is_valid(), serializer.errors
    assert expected_data == serializer.data


def test_get_serializer_for_unmapped_response():
    aeat_response = {}
    serializer_cls = serializers.get_class_for_aeat_response(aeat_response)
    assert serializers.UnknownResponseSerializer == serializer_cls
    serializer = serializer_cls(data=aeat_response)
    assert serializer.is_valid(), serializer.errors
    assert {'reason': 'Unknown AEAT response'} == serializer.data
