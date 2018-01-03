from unittest.mock import patch

from aduanet import zeep_plugins
from lxml import etree
from zeep.wsdl import utils


def test_sign_message_egress(certificate_example):
    envelope = etree.Element('Envelope')
    body = etree.SubElement(envelope, 'Body')
    etree.SubElement(body, 'Message', Id='myid')

    plugin = zeep_plugins.SignMessage(*certificate_example)
    envelope, _ = plugin.egress(envelope, None, 'test', None)

    xml_str = utils.etree_to_string(envelope).decode()

    assert '<Signature xmlns="http://www.w3.org/2000/09/xmldsig#" Id="Firma">' in xml_str


@patch('aduanet.zeep_plugins.logger')
def test_logging_ingress(logger):
    zeep_plugins.Logging().ingress(etree.Element('Envelope'), None, None)
    assert logger.info.called


@patch('aduanet.zeep_plugins.logger')
def test_logging_egress(logger):
    zeep_plugins.Logging().egress(etree.Element('Envelope'), None, None, None)
    assert logger.info.called
