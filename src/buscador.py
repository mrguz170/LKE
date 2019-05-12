"""
Gustavo Bañuelos Ochoa
LKE BUAP

Script para buscar las imagenes en las carpetas, cargarlas al buffer y etiquetarlas tomando el nombre de su carpeta.

"""

import os
import numpy as np

class Buscador():
    def __init__(self, path, numero_clases, listaClases):
        self.path = path
        self.numero_clases = numero_clases
        self.listaClases = listaClases
        self.dictOfWords = []
        self.X_dataXML = []

    def encuentra_conjuntos_entrenamiento_test_desde_path(self):
        for root, dirs, files in os.walk(self.path):
            for file_name in files:
                if (file_name.endswith(".xml")):

                    full_pathXML = os.path.join(root, file_name)
                    self.X_dataXML.append(full_pathXML)





