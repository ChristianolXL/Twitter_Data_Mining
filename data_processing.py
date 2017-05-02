#Tianxi Zhou
#Last updated 04/26/2017
#This program is going to convert the twitter data from dictionary format to the xml format.

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
read_speak = np.load('speak_file.npy').item()

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
#print (urls)

#Translate to xml.
#We can add speak context later
root = ET.Element('AIMind')
rroot = ET.SubElement(root, 'Root')
rroot.attrib["id"] = "0"
features = ET.SubElement(root, 'Features')

#Fill in the features
for url in urls:
    feature = ET.SubElement(features, 'Feature')
    feature.attrib["data"] = url
    feature.attrib["zh-data"] = ""
    feature.attrib["id"] = str(urls.index(url)+1)
    feature.attrib["uri"] = ""
    neighbors = ET.SubElement(feature, 'neighbors')

    #Find the neighbor in the dict.
    if url in read_dictionary.keys():
        for tags,sequence in read_dictionary[url].items():
            for item in sequence:
                neighbor = ET.SubElement(neighbors, 'neighbor')
                neighbor.attrib["dest"] = str(urls.index(item)+1)
                neighbor.attrib["relationship"] = tags

                #Actually I'm not sure what the weight is.
                neighbor.attrib["weight"] ="0"
    speak = ET.SubElement(feature, 'speak')
    if url in read_speak.keys():
        speak.attrib["Tweets"] = read_speak[url]
    zhspeak = ET.SubElement(feature, 'zh-speak')

#Completed the XML
tree = ET.ElementTree(root)

#The output file named: output.xml
tree.write('Musk_big.xml', pretty_print=True, xml_declaration=True,encoding="UTF-8",standalone="yes")