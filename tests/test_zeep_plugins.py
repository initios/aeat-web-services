import pytest

from lxml import etree
from zeep.wsdl import utils

from aeat import zeep_plugins


@pytest.fixture
def envelope():
    envelope = etree.Element('Envelope')
    body = etree.SubElement(envelope, 'Body')
    etree.SubElement(body, 'Message', Id='myid')
    return envelope


def test_sign_message_egress(certificate_example, envelope):
    plugin = zeep_plugins.SignMessagePlugin(*certificate_example)
    envelope, _ = plugin.egress(envelope, None, 'test', None)

    xml_str = utils.etree_to_string(envelope).decode()

    assert '<Signature xmlns="http://www.w3.org/2000/09/xmldsig#" Id="Firma">' in xml_str


def test_raw_xml_plugin(envelope):
    plugin = zeep_plugins.RawXMLPlugin()

    plugin.ingress(envelope, None, None)
    plugin.egress(envelope, None, None, None)

    expected = '<Envelope>\n  <Body>\n    <Message Id="myid"/>\n  </Body>\n</Envelope>\n'
    assert expected == plugin.last_sent == plugin.last_received
