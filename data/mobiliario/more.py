"""
Creado por:
Gustavo Bañuelos Ochoa

Script para crear imagenes espejo en la base de datos

Solo debes cambiar el nombre del dataset, y cambiar la extension del formato de tus imagenes (por ejemplo: '.png')
"""

import os
import cv2

nombre_Dataset = 'mobiliario'
file_format = '.bmp'


path = os.path.join(os.getcwd(), '/data/{}'.format(nombre_Dataset))
	

class Buscador():
    def __init__(self, path, numero_clases):
        self.path = path
        self.numero_clases = numero_clases
        self.X_img = []

    def encuentra_conjuntos_entrenamiento_test_desde_path(self):
    	for root, dirs, files in os.walk(self.path):
    		for file_name in files:
    			if(file_name.endswith("{}".format(file_format))):
    				full_pathXML = os.path.join(root, file_name)
    				self.X_img.append(full_pathXML)


searcher = Buscador(path=path, numero_clases=2)
searcher.encuentra_conjuntos_entrenamiento_test_desde_path()

x_imgs = searcher.X_img

for img in x_imgs:
    actual = cv2.imread(img)
    print(img)
    horizontal_img = actual.copy()
    horizontal_img = cv2.flip( horizontal_img, 1)
    cv2.imwrite('H-' + os.path.basename(img), horizontal_img)

