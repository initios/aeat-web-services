import logging

from .wsdl import ADUANET_SERVICES
from .xml_signing import sign
from . import utils

import requests


logger = logging.getLogger(__name__)


class Config:
    def __init__(self, service_name, test_mode):
        self.payload = ADUANET_SERVICES[service_name]
        self.test_mode = test_mode

    def __getattr__(self, name):
        if name == 'url':
            test, prod = self.payload['url_test'], self.payload['url_production']
            return test if self.test_mode else prod

        return self.payload[name]

    def __str__(self):
        return f'''
        Config: {self.verbose_name}
        URL: {self.url}
        '''


class Result:
    default_context = {
        'raw_request': None,
        'raw_response': None,
        'exception': None,
    }

    def __init__(self, data, error, context=None):
        self.context = context or {}

        for k, v in self.default_context.items():
            self.context[k] = self.context.get(k, v)

        self.data = data
        self.error = error

    def __getattr__(self, name):
        return self.context[name]

    @property
    def valid(self):
        return self.error is None


class Controller:
    def __init__(self, url, cert, key):
        self.url = url
        self.cert = cert
        self.key = key

    @classmethod
    def build_for_service(cls, service_name, cert, key, test_mode):
        mapping = ADUANET_SERVICES[service_name]
        url = mapping['url_test'] if test_mode else mapping['url_production']
        return cls(url, cert, key)

    def request(self, unsigned_xml: str):
        '''Receives unsigned xml and sends a signed SOAP enveloped payload'''
        logger.info("Preparing payload %s to send", unsigned_xml)

        el = utils.string_to_lxml(unsigned_xml)
        signed_xml = sign(el, self.cert, self.key)
        enveloped = utils.lxml_to_enveloped_string(signed_xml)

        logger.info("About to send request to %s", self.url)
        logger.info(enveloped)

        headers = {'content-type': 'text/xml'}
        cert = (self.cert, self.key)
        response = requests.post(self.url, data=enveloped, headers=headers, cert=cert)
        context = {'raw_request': unsigned_xml, 'raw_response': response.data}

        if response.status_code == '200':
            result = Result(response.content, None, context=context)
        else:
            logger.info('AEAT returned status code %s.', response.status_code)
            result = Result(None, 'Wrong AEAT response',  context=context)

        return result
