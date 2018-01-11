import setup_django  # NOQA

from aeat.rest_framework import serializers


def test_mrn_serializer(zeep_response):
    aeat_response = zeep_response(
        'wsdl_ens_presentation_IE315V4.wsdl', 'ens_presentation_success_IE328V4Sal.xml', 'IE315V4'
    )

    serializer = serializers.MRNSerializer(data=aeat_response)
    assert serializer.is_valid(raise_exception=False), serializer.errors

    raise Exception(serializer.data)
    assert {'mrn': '17ES004311Z0000010'} == serializer.data
