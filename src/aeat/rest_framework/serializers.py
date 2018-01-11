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


class DequeToDictMixin:
    def to_internal_value(self, data):
        return {raw_tag(item): lxml_to_dict(item) for item in data}


class ENSSerializer(DequeToDictMixin, rf.Serializer):
    mrn = rf.CharField(source='HEAHEA.DocNumHEA5')


class EXSSerializer(DequeToDictMixin, rf.Serializer):
    mrn = rf.CharField(source='HEAHEA.DocNumHEA5')
    item_number_involved = rf.IntegerField(source='RISANA.IteNumInvRKA1')
    customs_intervention_code = rf.CharField(source='RISANA.CusIntCodRKA1')
