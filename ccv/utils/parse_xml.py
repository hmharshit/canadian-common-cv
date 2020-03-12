# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

def parse_xml_file(filename):
    tree = ET.parse(filename)
    root_element = tree.getroot()
    return root_element

