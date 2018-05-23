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
    is_error = False

    mrn = rf.CharField(source='HEAHEA.DocNumHEA5')


class EXSSerializer(DequeToDictMixin, rf.Serializer):
    is_error = False

    mrn = rf.CharField(source='HEAHEA.DocNumHEA5')
    item_number_involved = rf.IntegerField(source='RISANA.IteNumInvRKA1')
    customs_intervention_code = rf.CharField(source='RISANA.CusIntCodRKA1')


class UnknownResponseSerializer(rf.Serializer):
    is_error = True

    def __init__(self, *args, **kwargs):
        kwargs.pop('data') if 'data' in kwargs else None
        data = {}
        super().__init__(self, *args, data=data, **kwargs)

    def to_representation(self, obj):
        return {'reason': 'Unknown AEAT response'}


class ENSFunctionalErrorSerializer(DequeToDictMixin, rf.Serializer):
    is_error = True

    code = rf.CharField(source='FUNERRER1.ErrReaER13', default='')
    type = rf.CharField(source='FUNERRER1.ErrTypER11')
    pointer = rf.CharField(source='FUNERRER1.ErrPoiER12')
    reason = rf.CharField(source='FUNERRER1.OriAttValER14', default='No error message supplied')


def parse_xsd(data):
    try:
        body = data.find('.//soapenv:Body', namespaces=data.nsmap)
    except AttributeError:
        body = data

    # Try V2 Style
    try:
        xsd = body[0].nsmap[None]
    except (IndexError, KeyError):
        pass
    else:
        print("Estilo V2", xsd)
        return xsd

    # Try V4 Style
    try:
        xsd = body[0].nsmap['ie']
    except (IndexError, KeyError):
        pass
    else:
        print("Estilo V5", xsd)
        return xsd


def get_class_for_aeat_response(data):
    xsd = parse_xsd(data)

    ens = 'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/enswsv5/'
    exs = 'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/adrx/ws/'

    return {
        f'{ens}IE328V5Sal.xsd': ENSSerializer,
        f'{ens}IE304V5Sal.xsd': ENSSerializer,
        f'{ens}IE316V5Sal.xsd': ENSFunctionalErrorSerializer,
        f'{exs}IE628V2Sal.xsd': EXSSerializer,
    }.get(xsd, UnknownResponseSerializer)
