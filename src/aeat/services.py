from aeat.rest_framework import serializers, validators


class ENSPresentationService:
    service_name = 'ens_presentation'
    serializer = serializers.ENSSerializer
    validator = validators.ENSPresentationValidator
    qname = '{https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/enswsv5/IE315V5Ent.xsd}CC315A'  # noqa
    nsmap = {'ie': 'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/enswsv5/IE315V5Ent.xsd'}  # noqa


def get_service(self):
    return {
        'ens_presentation': ENSPresentationService,
    }
