from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers as rf

import aeat

from . import complex_types_v2 as v2, complex_types_v4 as v4, fields


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
    include_test_mode = True

    def save(self):
        return make_aeat_request(self.service_name, self.data)

    def to_representation(self, instance):
        instance = super().to_representation(instance)

        if self.include_test_mode and settings.AEAT_TEST_MODE:
            instance['TesIndMES18'] = '0'

        return instance


class ENSQuerySerializer(AEATRequest):
    service_name = 'ens_query'
    include_test_mode = False

    TraModAtBorHEA76 = fields.RequiredStr(help_text='Transport mode at border. EG 1')
    ExpDatOfArr = fields.RequiredStr(help_text='Estimated date of arrival. EG 20110809')
    ConRefNum = fields.RequiredStr(help_text='Transport identifier. EG 9294408')


class ENSForkSerializer(AEATRequest):
    service_name = 'ens_fork'


class ENSPresentationSerializer(v4.BaseV4Mixin, AEATRequest):
    service_name = 'ens_presentation'

    MesTypMES20 = fields.NotRequiredStr(default='CC315A', read_only=True,
                                        help_text='Message type. EG CC315A')
    HEAHEA = v4.ENSPresentationHeader(required=True)


class ENSModificationSerializer(v4.BaseV4Mixin, AEATRequest):
    service_name = 'ens_modification'
    NOTPAR670 = v4.NotifyParty(required=True)
    MesTypMES20 = fields.NotRequiredStr(default='CC313A', read_only=True,
                                        help_text='Message type. EG CC313A')
    HEAHEA = v4.ENSModificationHeader(required=True)


class EXSPresentationSerializer(v2.BaseV2Mixin, AEATRequest):
    service_name = 'exs_common'

    Id = rf.ReadOnlyField(source='MesIdeMES19', help_text='Message identification')
    MesTypMES20 = rf.ReadOnlyField(default='CC615A', help_text='Message type')

    HEAHEA = v2.EXSHeader(required=True)
