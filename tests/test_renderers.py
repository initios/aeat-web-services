from lxml import etree
from aeat import renderers


def test_xml_renderer():
    payload = {
        '__attrs__': {'Id': '12345'},
        'MesSenMES3': '89890001K',
        'HEAD': [{'TraModAtBorHEA76': '5'}],
        'FOOT': {'foot1': 'foot2'},
    }
    qname = '{https://www.example.xsd}CC315A'
    nsmap = {'ie': 'https://www.example.xsd'}

    renderer = renderers.XMLRenderer(qname, nsmap)
    xml = renderer.render(payload)
    el = etree.fromstring(bytes(xml, 'UTF-8'))

    assert xml.startswith('<?xml')
    assert el.attrib.get('Id') == '12345'
