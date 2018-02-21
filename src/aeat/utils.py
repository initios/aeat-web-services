from lxml import etree


def lxml_to_string(el):
    return etree.tostring(el, pretty_print=True).decode()


def string_to_lxml(xml):
    return etree.fromstring(bytes(str, 'UTF-8'))


def lxml_to_enveloped_string(el):
    return '''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Header/>
        <soapenv:Body>{}</soapenv:Body>
        </soapenv:Envelope>'''.format(etree.tostring(el).decode())
