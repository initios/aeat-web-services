from aeat.rest_framework import serializers
from aeat.rest_framework import validators
from aeat.wsdl import ADUANET_SERVICES


class ENSPresentationService:
    service_name = 'ens_presentation'
    wsdl = ADUANET_SERVICES['ens_presentation']  # TODO
    serializer = serializers.ENSSerializer
    validator = validators.ENSPresentationValidator
    qname = '{https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/enswsv5/IE315V5Ent.xsd}CC315A'  # noqa
    nsmap = {'ie': 'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/enswsv5/IE315V5Ent.xsd'}  # noqa


def get_service(self):
    return {
        'ens_presentation': ENSPresentationService,
    }
