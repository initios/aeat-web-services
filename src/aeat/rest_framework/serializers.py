from rest_framework import serializers as rf


def raw_tag(item):
    '''Returns item tag without namespace'''
    return item.tag.partition('}')[2] or item.tag


def lxml_to_dict(node):
    '''Convert an lxml.etree node tree into a dict recursively'''
    storage = {}

    for child in node.iterchildren():
        key = raw_tag(child)
        storage[key] = child.text if child.text else lxml_to_dict(child)

    return storage


def deque_to_dict(data):
    return {raw_tag(item): lxml_to_dict(item) for item in data}


class DequeToDictMixin:
    def to_internal_value(self, data):
        return deque_to_dict(data)


class ENSSerializer(DequeToDictMixin, rf.Serializer):
    mrn = rf.CharField(source='HEAHEA.DocNumHEA5')


class EXSSerializer(DequeToDictMixin, rf.Serializer):
    mrn = rf.CharField(source='HEAHEA.DocNumHEA5')
    item_number_involved = rf.IntegerField(source='RISANA.IteNumInvRKA1')
    customs_intervention_code = rf.CharField(source='RISANA.CusIntCodRKA1')


class UnknownSerializer(rf.Serializer):
    def validate(self, data):
        raise rf.ValidationError('Unknown AEAT response')


def get_class_for_aeat_response(data):
    try:
        xsd = data[0].nsmap[None]
    except KeyError:
        xsd = None

    ENSV4Base = 'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/enswsv4/'
    EXSV2Base = 'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/adrx/ws/'

    return {

        f'{ENSV4Base}IE315V4Ent.xsd': ENSSerializer,
        # xmlns:IE316V4Sal="https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/enswsv4/IE316V4Sal.xsd"
        # xmlns:IE328V4Sal="https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/enswsv4/IE328V4Sal.xsd"
        # xmlns:IE351V4Sal="https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/enswsv4/IE351V4Sal.xsd"
        # xmlns:IE917V4Sal="https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/enswsv4/IE917V4Sal.xsd"

        f'{EXSV2Base}IE628V2Sal.xsd': EXSSerializer,
    }.get(xsd, UnknownSerializer)
