from aeat import renderers


def test_xml_renderer():
    payload = {
        'MesSenMES3': '89890001K',
        'HEAD': [{'TraModAtBorHEA76': '5'}],
        'FOOT': {'foot1': 'foot2'},
    }
    qname = '{https://www.example.xsd}CC315A'
    nsmap = {'ie': 'https://www.example.xsd'}

    renderer = renderers.XMLRenderer(qname, nsmap)
    print(renderer.render(payload))
    assert renderer.render(payload).startswith('<?xml')
