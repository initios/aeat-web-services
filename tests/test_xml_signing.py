from lxml import etree

from aeat import xml_signing


def test_sign_without_root_id(certificate_example):
    root = etree.Element('Data')

    signed = xml_signing.sign(root, *certificate_example)

    assert xml_signing.verify(signed, *certificate_example)
    assert 'MessageRoot' == signed.attrib['Id']


def test_verify_simple_signature(certificate_example):
    root = etree.Element('Data', Id='myid')
    signed = xml_signing.sign(root, *certificate_example)

    assert xml_signing.verify(signed, *certificate_example)


def test_verify_wrong_signature(certificate_example):
    root = etree.Element('Data', Id='myid')

    signed = xml_signing.sign(root, *certificate_example)
    etree.SubElement(signed, 'KeyAfterSigning')

    assert xml_signing.verify(signed, *certificate_example) is False


def test_sign_complete_xades_epel(certificate_example):
    root = etree.Element('Data', Id='myid')

    signed = xml_signing.sign(root, *certificate_example)
    assert xml_signing.verify(signed, *certificate_example)
