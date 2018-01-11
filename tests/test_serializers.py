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


# @pytest.mark.parametrize('response_xml', [
#     'ens_presentation_error_IE316V4Sal.xml',
#     'ens_presentation_error_IE917V4Sal.xml',
# ])
# @patch('aeat.Controller.operation', new_callable=PropertyMock)
# def test_controller_with_incorrect_responses(operation_patch, zeep_response, response_xml):
#     def response():
#         return zeep_response('wsdl_ens_presentation_IE315V4.wsdl', response_xml, 'IE315V4')

#     operation_patch.return_value = lambda **kwargs: response()
#     ctrl = Controller(Mock(), Mock(operation='IE315V4'))
#     result = ctrl.request(factories_v4.ENSPresentationFactory())

#     print(result.data)
#     assert not result.valid
#     assert result.data is None
#     assert 'AEAT response error' == result.error
