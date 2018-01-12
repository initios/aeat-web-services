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


class UnknownResponseSerializer(rf.Serializer):
    is_error = True

    def to_representation(self, obj):
        return {'reason': 'Unknown AEAT response'}


class ENSFunctionalErrorSerializer(rf.Serializer):
    is_error = True

    type = rf.CharField(source='FUNERRER1.ErrTypER11')
    pointer = rf.CharField(source='FUNERRER1.ErrPoiER12')
    reason = rf.CharField(source='FUNERRER1.OriAttValER14')


def parse_xsd(data):
    # Try V2 Style
    try:
        xsd = data[0].nsmap[None]
    except (IndexError, KeyError):
        pass
    else:
        return xsd

    # Try V4 Style
    try:
        xsd = data[0].nsmap['ie']
    except (IndexError, KeyError):
        pass
    else:
        return xsd


def get_class_for_aeat_response(data):
    xsd = parse_xsd(data)

    ens = 'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/enswsv4/'
    exs = 'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/adrx/ws/'

    return {
        f'{ens}IE328V4Sal.xsd': ENSSerializer,
        f'{exs}IE628V2Sal.xsd': EXSSerializer,
    }.get(xsd, UnknownResponseSerializer)
