#Tianxi Zhou
#Last edited 04/06/2017
import numpy as np
import json
import pprint
import dicttoxml
from lxml import etree as ET
import lxml.builder

#This function is to uniqufiy the list and preserving the order.
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


#load
read_dictionary = np.load('my_file.npy').item()

#print
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(read_dictionary)

#Add all url in urls
urls = list()
for key, value in read_dictionary.items():
    urls.append(key)
    for k,v in value.items():
        for k in v:
            urls.append(k)

#Delete duplicates.
print (len(urls))
urls = f7(urls)
print(len(urls))
print (urls)

#Translate to xml.
root = ET.Element('AIMind')
features = ET.SubElement(root, 'Features')
for url in urls:
    feature = ET.SubElement(features, 'Feature')
    feature.attrib["data"] = url
    feature.attrib["zh-data"] = ""
    feature.attrib["id"] = str(urls.index(url)+1)
    feature.attrib["uri"] = ""
    neighbors = ET.SubElement(feature, 'neighbors')
    if url in read_dictionary.keys():
        for tags,sequence in read_dictionary[url].items():
            for item in sequence:
                neighbor = ET.SubElement(neighbors, 'neighbor')
                neighbor.attrib["dest"] = str(urls.index(item)+1)
                neighbor.attrib["relationship"] = tags
                neighbor.attrib["weight"] ="0"


    second = ET.SubElement(features, 'second')
    second.text = '01'



tree = ET.ElementTree(root)
tree.write('output.xml', pretty_print=True, xml_declaration=True,encoding="UTF-8",standalone="yes")