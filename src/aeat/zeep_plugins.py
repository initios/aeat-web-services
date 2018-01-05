import logging

from zeep import Plugin
from zeep.wsdl import utils

from aeat import xml_signing

logger = logging.getLogger(__name__)


class SignMessage(Plugin):
    def __init__(self, cert_path, key_path):
        self.cert_path = cert_path
        self.key_path = key_path

    def egress(self, envelope, http_headers, operation, binding_options):
        args = envelope, self.cert_path, self.key_path
        xml_signing.sign(*args)
        return envelope, http_headers


class Logging(Plugin):
    def envelope_to_str(self, envelope):
        return utils.etree_to_string(envelope).decode()

    def ingress(self, envelope, http_headers, operation):
        '''
        Server SOAP response just before is parsed by zeep
        '''
        logger.info('Ingress: envelope %s | headers %s | operation %s',
                    self.envelope_to_str(envelope), http_headers, operation)
        return envelope, http_headers

    def egress(self, envelope, http_headers, operation, binding_options):
        '''
        The SOAP request just before sending it's sent to SOAP Server
        '''
        logger.info('Egress: envelope %s | headers %s | operation %s | binding_opts %s',
                    self.envelope_to_str(envelope), http_headers, operation, binding_options)

        return envelope, http_headers
