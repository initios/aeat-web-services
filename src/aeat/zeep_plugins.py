import logging

from lxml import etree
from zeep import Plugin

from aeat import utils, xml_signing

logger = logging.getLogger(__name__)


class SignMessagePlugin(Plugin):
    def __init__(self, cert_path, key_path):
        self.cert_path = cert_path
        self.key_path = key_path

    def egress(self, envelope, http_headers, operation, binding_options):
        '''Sign enveloped message'''
        args = envelope[0][0], self.cert_path, self.key_path
        signed = xml_signing.sign(*args)

        data = '''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Header/>
        <soapenv:Body>{}</soapenv:Body>
        </soapenv:Envelope>'''.format(
            etree.tostring(signed).decode())

        envelope = etree.fromstring(data)
        return envelope, http_headers


class RawXMLPlugin(object):
    '''
    Stores last request and response as str
    '''
    def __init__(self):
        self.last_sent = None
        self.last_received = None

    def ingress(self, envelope, http_headers, operation):
        self.last_received = utils.lxml_to_string(envelope)
        logging.info(self.last_received)
        return envelope, http_headers

    def egress(self, envelope, http_headers, operation, binding_options):
        self.last_sent = utils.lxml_to_string(envelope)
        logging.info(self.last_sent)
        return envelope, http_headers
