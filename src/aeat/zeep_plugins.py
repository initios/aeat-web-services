import logging

from zeep import Plugin

from aeat import utils, xml_signing

logger = logging.getLogger(__name__)


class SignMessagePlugin(Plugin):
    def __init__(self, cert_path, key_path):
        self.cert_path = cert_path
        self.key_path = key_path

    def egress(self, envelope, http_headers, operation, binding_options):
        args = envelope, self.cert_path, self.key_path
        xml_signing.sign(*args)
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
        return envelope, http_headers

    def egress(self, envelope, http_headers, operation, binding_options):
        self.last_sent = utils.lxml_to_string(envelope)
        return envelope, http_headers
