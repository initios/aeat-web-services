import logging

from zeep import Plugin

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
