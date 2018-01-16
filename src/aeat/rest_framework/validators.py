from django.conf import settings
from rest_framework import serializers as rf

from . import complex_types_v1 as v1
from . import complex_types_v4 as v4
from . import fields


class ValidatorBase(rf.Serializer):
    service_name = None
    include_test_mode = True

    def to_representation(self, instance):
        instance = super().to_representation(instance)

        if self.include_test_mode and settings.AEAT_TEST_MODE:
            instance['TesIndMES18'] = '0'

        return instance


class ENSQueryValidator(ValidatorBase):
    service_name = 'ens_query'
    include_test_mode = False

    TraModAtBorHEA76 = fields.RequiredStr(help_text='Transport mode at border. EG 1')
    ExpDatOfArr = fields.RequiredStr(help_text='Estimated date of arrival. EG 20110809')
    ConRefNum = fields.RequiredStr(help_text='Transport identifier. EG 9294408')


class ENSForkValidator(ValidatorBase):
    service_name = 'ens_fork'


class ENSPresentationValidator(v4.BaseMixin, ValidatorBase):
    service_name = 'ens_presentation'

    MesTypMES20 = fields.NotRequiredStr(default='CC315A', read_only=True,
                                        help_text='Message type. EG CC315A')
    HEAHEA = v4.ENSPresentationHeader(required=True)


class ENSModificationValidator(v4.BaseMixin, ValidatorBase):
    service_name = 'ens_modification'
    NOTPAR670 = v4.NotifyParty(required=False)
    MesTypMES20 = fields.NotRequiredStr(default='CC313A', read_only=True,
                                        help_text='Message type. EG CC313A')
    HEAHEA = v4.ENSModificationHeader(required=True)


class EXSPresentationValidator(v1.BaseMixin, ValidatorBase):
    service_name = 'exs_common'

    HEAHEA = v1.EXSHeader(required=True)


class EXSModificationValidator(v1.BaseMixin, ValidatorBase):
    service_name = 'exs_common'

    HEAHEA = v1.EXSHeaderModification(required=True)


class EXSCancellationValidator(v1.BaseMixin, ValidatorBase):
    service_name = 'exs_common'

    HEAHEA = v1.EXSHeaderCancellation(required=True)
