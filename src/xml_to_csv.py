"""
Gustavo Bañuelos Ochoa
LKE BUAP

clase xml convierte archivo xml a csv, crea 2 archivos "train/test_labels.csv" en el directorio especificado

"""
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

class xmltocsv():
    def __init__(self, dirXML):
        self.dirXML = dirXML

    def xml_to_csv(self, path):
        xml_list = []
        for xml_file in glob.glob(path + '/*.xml'):
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for member in root.findall('object'):
                value = (root.find('filename').text,
                         int(root.find('size')[0].text),
                         int(root.find('size')[1].text),
                         member[0].text,
                         int(member[4][0].text),
                         int(member[4][1].text),
                         int(member[4][2].text),
                         int(member[4][3].text)
                         )
                xml_list.append(value)
        column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
        xml_df = pd.DataFrame(xml_list, columns=column_name)
        print('xml to csv completado')
        return xml_df

