from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers as rf
from rest_framework.serializers import ValidationError

import aeat

from . import complex_types, fields


def make_aeat_request(service_name, data):
    '''
    Helper to make AEAT requests

    :rtype: aduanet.aeat.Result
    '''

    cert_path = settings.AEAT_CERT_PATH
    key_path = settings.AEAT_KEY_PATH

    if not cert_path:
        raise ImproperlyConfigured('AEAT_CERT_PATH required')

    if not key_path:
        raise ImproperlyConfigured('AEAT_KEY_PATH required')

    config = aeat.Config(service_name, test_mode=settings.AEAT_TEST_MODE)
    ctrl = aeat.Controller.build_from_config(config, cert_path, key_path)
    return ctrl.request(data)


class AEATRequest(rf.Serializer):
    service_name = None

    def save(self):
        result = make_aeat_request(self.service_name, self.data)

        if not result.valid:
            raise ValidationError(result.error)

        return {'data': result.data, 'raw_response': result.raw_response}

    def to_representation(self, instance):
        instance = super().to_representation(instance)

        if settings.AEAT_TEST_MODE:
            instance['TesIndMES18'] = '0'

        return instance


class ENSQuerySerializer(AEATRequest):
    service_name = 'ens_query'

    TraModAtBorHEA76 = fields.RequiredStr(help_text='Transport mode at border. EG 1')
    ExpDatOfArr = fields.RequiredStr(help_text='Estimated date of arrival. EG 20110809')
    ConRefNum = fields.RequiredStr(help_text='Transport identifier. EG 9294408')


class ENSForkSerializer(AEATRequest):
    service_name = 'ens_fork'


class ENSMixin(rf.Serializer):
    MesSenMES3 = fields.NotRequiredStr(max_length=35, read_only=True,
                                       default=settings.AEAT_VAT_NUMBER,
                                       help_text='Message Sender (VAT Number). EG. 89890001K')
    MesRecMES6 = fields.NotRequiredStr(max_length=35, default='NICA.ES', read_only=True,
                                       help_text='EG NICA.ES (default)')
    DatOfPreMES9 = fields.AEATDateField(required=True, allow_null=False,
                                        help_text='Date of preparation. EG 101010 (YYMMDD)')
    TimOfPreMES10 = fields.AEATTimeField(required=True, allow_null=False,
                                         help_text='Time of preparation. EG 1010 (HHMM)')
    MesIdeMES19 = fields.RequiredStr(max_length=14, help_text='Message identification. '
                                                              'EG 09ES112222110 (like Id)')

    # Nested fields
    HEAHEA = complex_types.ENSHeader(required=True)
    TRACONCO1 = complex_types.TraderConsignor(required=True)
    TRACONCE1 = complex_types.TraderConsignee(required=True)
    NOTPAR670 = complex_types.NotifyParty()
    GOOITEGDS = complex_types.GoodsItem(required=True, many=True)
    ITI = complex_types.Itinerary(required=False, many=True)
    TRAREP = complex_types.TraderRepresentative(required=False)
    PERLODSUMDEC = complex_types.PersonLodgingSummaryDeclaration(required=False)
    SEAID529 = complex_types.SealsIdentity(required=False, many=True)
    CUSOFFFENT730 = complex_types.CustomsOfficeFirstEntry(required=True)
    CUSOFFSENT740 = complex_types.CustomsOfficeSubsequentEntry(many=True)
    TRACARENT601 = complex_types.TraderEntryCarrier(required=False)


class ENSPresentationSerializer(ENSMixin, AEATRequest):
    service_name = 'ens_presentation'

    MesTypMES20 = fields.NotRequiredStr(default='CC315A', read_only=True,
                                        help_text='Message type. EG CC315A')


class ENSModificationSerializer(ENSMixin, AEATRequest):
    service_name = 'ens_modification'

    MesTypMES20 = fields.NotRequiredStr(default='CC313A', read_only=True,
                                        help_text='Message type. EG CC313A')


class EXSPresentationSerializer(AEATRequest):
    service_name = 'exs_presentation'
