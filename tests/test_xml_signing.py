from lxml import etree

from aeat import xml_signing


def test_sign_without_root_id(certificate_example):
    root = etree.Element('Data')

    xml_signing.sign(root, *certificate_example)

    assert xml_signing.verify(root, *certificate_example)
    assert 'MessageRoot' == root.attrib['Id']


def test_verify_simple_signature(certificate_example):
    root = etree.Element('Data', Id='myid')
    xml_signing.sign(root, *certificate_example)

    assert xml_signing.verify(root, *certificate_example)


def test_verify_wrong_signature(certificate_example):
    root = etree.Element('Data', Id='myid')

    xml_signing.sign(root, *certificate_example)
    etree.SubElement(root, 'KeyAfterSigning')

    assert xml_signing.verify(root, *certificate_example) is False


def test_sign_complete_xades_epel(certificate_example):
    root = etree.Element('Data', Id='myid')

    xml_signing.sign(root, *certificate_example)
    assert xml_signing.verify(root, *certificate_example)
