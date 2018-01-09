from lxml import etree


def lxml_to_string(el):
    return etree.tostring(el, pretty_print=True).decode()
