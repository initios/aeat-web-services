import pytest

import setup_django  # NOQA

from aeat.rest_framework import serializers


def test_ens_serializer(zeep_response):
    aeat_response = zeep_response(
        'enswsv5',
        'ens_presentation_IE315V5.wsdl', 'ens_presentation_success_IE328V5Sal.xml', 'IE315V5'
    )

    serializer = serializers.ENSSerializer(data=aeat_response)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    assert {'mrn': '17ES004311Z0000010'} == serializer.data


def test_exs_serializer(zeep_response):
    aeat_response = zeep_response(
        'exswsv2', 'exs_presentation_IE615V2.wsdl', 'exs_presentation_success_IE628V2Sal.xml',
        'IE615V2'
    )

    serializer = serializers.EXSSerializer(data=aeat_response)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    assert {'mrn': '17ES00361160001234',
            'item_number_involved': 0, 'customs_intervention_code': 'V'} == serializer.data


@pytest.mark.parametrize('ver,url,response,operation,expected,is_error,expected_data', [
    # ENS
    ('enswsv5', 'ens_presentation_IE315V5.wsdl', 'ens_presentation_success_IE328V5Sal.xml',
     'IE315V5', serializers.ENSSerializer, False, {'mrn': '17ES004311Z0000010'}),

    ('enswsv5', 'ens_modification_IE313V5.wsdl', 'ens_modification_success_IE304V5Sal.xml',
     'IE313V5', serializers.ENSSerializer, False, {'mrn': '18ES003611Z0123456'}),

    ('enswsv5', 'ens_presentation_IE315V5.wsdl', 'ens_presentation_error_IE316V5Sal.xml',
     'IE315V5', serializers.ENSFunctionalErrorSerializer, True,
     {'type': '12', 'pointer': 'MES.MesSenMES3', 'code': '',
      'reason': '1234-Message Sender is not valid'}),

    ('enswsv5', 'ens_presentation_IE315V5.wsdl', 'ens_presentation_error_IE316V5Sal_v2.xml',
     'IE315V5', serializers.ENSFunctionalErrorSerializer, True,
     {'type': '12', 'pointer': 'ITI.ITI', 'code': 'R879',
      'reason': 'No error message supplied'}),

    # EXS
    ('exswsv2', 'exs_presentation_IE615V2.wsdl', 'exs_presentation_success_IE628V2Sal.xml',
     'IE615V2', serializers.EXSSerializer, False,
     {'mrn': '17ES00361160001234', 'customs_intervention_code': 'V', 'item_number_involved': 0}),

    ('exswsv2', 'exs_presentation_IE615V2.wsdl', 'exs_presentation_error_IE919V2Sal.xml',
     'IE615V2', serializers.UnknownResponseSerializer, True, {'reason': 'Unknown AEAT response'}),
])
def test_get_serializer_for_mapped_response(ver, zeep_response, url, response, operation, expected,
                                            is_error, expected_data):
    aeat_response = zeep_response(ver, url, response, operation)
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


@pytest.mark.parametrize('filename,expected', [
    ('exs_presentation_success_IE628V2Sal.xml',
     'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/adrx/ws/IE628V2Sal.xsd'),

    ('exs_presentation_error_IE919V2Sal.xml',
     'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/adrx/ws/IE919V2Sal.xsd'),

    ('ens_presentation_success_IE328V5Sal.xml',
     'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/enswsv5/IE328V5Sal.xsd'),  # NOQA

    ('ens_modification_success_IE304V5Sal.xml',
     'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/enswsv5/IE304V5Sal.xsd'),  # NOQA

    ('ens_presentation_error_IE917V5Sal.xml',
     'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/enswsv5/IE917V5Sal.xsd'),  # NOQA
])
def test_parse_xsd(response_etree_element, filename, expected):
    xml = response_etree_element(filename)
    assert expected == serializers.parse_xsd(xml)
