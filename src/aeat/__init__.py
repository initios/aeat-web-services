import logging

from . import zeep_plugins
from .wsdl import ADUANET_SERVICES
from requests import Session
from zeep import exceptions as zeep_exceptions
from zeep import Client, Transport, xsd


logger = logging.getLogger(__name__)


class Config:
    def __init__(self, service_name, test_mode):
        self.payload = ADUANET_SERVICES[service_name]
        self.test_mode = test_mode

    def __getattr__(self, name):
        if name == 'port':
            test, prod = self.payload['port_test'], self.payload['port_production']
            return test if self.test_mode else prod

        return self.payload[name]

    def __str__(self):
        return f'''
        Config: {self.verbose_name}
        WSDL: {self.wsdl}
        Operation: {self.operation}
        Port: {self.port}
        Service: {self.service}
        '''


class Result:
    def __init__(self, data, error, raw_request=None, raw_response=None):
        self.data = data
        self.error = error
        self.raw_request = raw_request
        self.raw_response = raw_response

    @property
    def valid(self):
        return self.error is None


class Controller:
    def __init__(self, client, config, raw_xml_plugin=None):
        self.client = client
        self.config = config
        self.raw_xml_plugin = raw_xml_plugin
        logger.info('Controller initialized with config %s', config)

    @classmethod
    def build_from_config(cls, config, pub_cert, priv_cert):
        '''
        Builds AEAT Controller with Plugins

        :param config: Preconfigured Config object
        :param pub_cert: Public certificate file path
        :param priv_cert: Private certificate file path

        :rtype: Controller
        '''
        session = Session()
        session.cert = (pub_cert, priv_cert)
        transport = Transport(session=session, operation_timeout=60)

        raw_xml_plugin = zeep_plugins.RawXMLPlugin()

        if config.signed:
            sign_plugin = zeep_plugins.SignMessage(pub_cert, priv_cert)
            plugins = [sign_plugin, raw_xml_plugin]
        else:
            plugins = [raw_xml_plugin]

        client = Client(config.wsdl, service_name=config.service, port_name=config.port,
                        transport=transport, strict=False, plugins=plugins)

        return cls(client, config, raw_xml_plugin=raw_xml_plugin)

    @property
    def operation(self):
        return getattr(self.client.service, self.config.operation)

    def request(self, payload):
        if self.config.signed:
            # Skip WSDL validation. Is added later by zeep_plugins.SignMessage
            payload['Signature'] = xsd.SkipValue

        try:
            data = self.operation(**payload)
        except zeep_exceptions.Fault as e:
            logger.info('AEAT request failed.', exc_info=True)
            result = Result(None, e.message)
        except zeep_exceptions.Error as e:
            logger.info('AEAT request failed.', exc_info=True)
            result = Result(None, 'Wrong AEAT response')
        except Exception as e:
            logger.critical('Unexpected exception', exc_info=True)
            result = Result(None, 'Unknown error')
        else:
            result = Result(data, None)

        if self.raw_xml_plugin:
            result.raw_request = self.raw_xml_plugin.last_sent
            result.raw_response = self.raw_xml_plugin.last_received

        return result
