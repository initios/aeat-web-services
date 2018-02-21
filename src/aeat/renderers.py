from lxml import etree


class XMLRenderer:
    def __init__(self, qname, root_nsmap):
        self.root = etree.Element(qname, nsmap=root_nsmap)

    def append_to_element(self, element, data):
        for k, v in data.items():
            if isinstance(v, list):
                for child in v:
                    parent = etree.SubElement(element, k)
                    self.append_to_element(parent, child)
            elif isinstance(v, dict):
                parent = etree.SubElement(element, k)
                self.append_to_element(parent, v)
            else:
                parent = etree.SubElement(element, k)
                parent.text = v

    def render(self, data, root_attributes=None):
        root_attributes = [] if not root_attributes else root_attributes

        for attr in root_attributes:
            self.root.attrib[attr] = data.pop(attr)

        self.append_to_element(self.root, data)
        stream = etree.tostring(self.root, xml_declaration=True,
                                encoding='UTF-8')
        return stream.decode()
