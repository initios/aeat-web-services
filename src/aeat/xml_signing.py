import datetime as dt
import logging
from datetime import timezone as tz

import xmlsec
from lxml import etree

logger = logging.getLogger(__name__)


def aeat_object_with_qualifying_properties():
    now_iso_format = dt.datetime.now(tz.utc).astimezone().isoformat(timespec='seconds')

    return etree.fromstring(f'''
        <Object xmlns="http://www.w3.org/2000/09/xmldsig#">
            <etsi:QualifyingProperties
                xmlns:ds="http://www.w3.org/2000/09/xmldsig#"
                xmlns:etsi="http://uri.etsi.org/01903/v1.2.2#" Target="#Firma">
                <etsi:SignedProperties Id="SignatureProperties">
                    <etsi:SignedSignatureProperties>
                        <etsi:SigningTime>{now_iso_format}</etsi:SigningTime>
                        <etsi:SignaturePolicyIdentifier>
                            <etsi:SignaturePolicyId>
                                <etsi:SigPolicyId>
                                    <etsi:Identifier>http://administracionelectronica.gob.es/es/ctt/politicafirma/politica_firma_AGE_v1_8.pdf</etsi:Identifier>
                                </etsi:SigPolicyId>
                                <etsi:SigPolicyHash>
                                    <ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
                                    <ds:DigestValue>VYICYpNOjso9g1mBiXDVxNORpKk=</ds:DigestValue>
                                </etsi:SigPolicyHash>
                            </etsi:SignaturePolicyId>
                        </etsi:SignaturePolicyIdentifier>
                    </etsi:SignedSignatureProperties>
                </etsi:SignedProperties>
            </etsi:QualifyingProperties>
        </Object>
        ''')  # NOQA


def sign(root, cert, key):
    '''
    Sign LXMLElement node with specified certificate
    '''
    root_id = root.get('Id')

    if not root_id:
        root.attrib['Id'] = 'MessageRoot'
        root_id = 'MessageRoot'

    elem_uri = "#%s" % root_id
    signature = xmlsec.template.create(root,
                                       c14n_method=xmlsec.constants.TransformInclC14NWithComments,
                                       sign_method=xmlsec.constants.TransformRsaSha1)
    signature.attrib['Id'] = 'Firma'
    # Main reference
    ref = xmlsec.template.add_reference(signature,
                                        xmlsec.constants.TransformSha1,
                                        uri=elem_uri)
    xmlsec.template.add_transform(ref, xmlsec.constants.TransformEnveloped)

    # Keyinfo reference
    ref = xmlsec.template.add_reference(signature,
                                        xmlsec.constants.TransformSha1,
                                        uri='#CertificadoFirmante')
    # SignedProperties reference
    ref = xmlsec.template.add_reference(signature,
                                        xmlsec.constants.TransformSha1,
                                        uri='#SignatureProperties')

    # Add x509 keyinfo
    ki = xmlsec.template.ensure_key_info(signature, id="CertificadoFirmante")
    xmlsec.template.add_x509_data(ki)

    # Add external object
    signature.append(aeat_object_with_qualifying_properties())
    root.append(signature)

    ctx = xmlsec.SignatureContext()
    ctx.register_id(root, id_attr="Id")

    ctx.key = xmlsec.Key.from_file(key,
                                   format=xmlsec.constants.KeyDataFormatPem)
    ctx.key.load_cert_from_file(cert, xmlsec.constants.KeyDataFormatPem)

    ctx.sign(signature)
    return root


def verify(root, cert, key):
    signed = xmlsec.tree.find_node(root, xmlsec.constants.NodeSignature)
    ctx1 = xmlsec.SignatureContext()
    ctx1.key = xmlsec.Key.from_file(key,
                                    format=xmlsec.constants.KeyDataFormatPem)
    ctx1.key.load_cert_from_file(cert,
                                 xmlsec.constants.KeyDataFormatPem)

    try:
        ctx1.verify(signed)
    except xmlsec.Error:
        logger.error("Invalid signature", exc_info=True)
        return False
    else:
        return True
