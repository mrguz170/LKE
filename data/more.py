"""
Script para crear imagenes espejo en la base de datos

Solo debes cambiar la direccion path por la tuya

"""

import os
import cv2


path = os.path.join(os.path.basename()os.getcwd(), '/data/{}')


class Buscador():
    def __init__(self, path, numero_clases):
        self.path = path
        self.numero_clases = numero_clases
        self.X_img = []

    def encuentra_conjuntos_entrenamiento_test_desde_path(self):
    	for root, dirs, files in os.walk(self.path):
    		for file_name in files:
    			if(file_name.endswith(".bmp")):
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

