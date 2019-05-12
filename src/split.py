"""
Gustavo Bañuelos Ochoa
LKE BUAP

Separa los datos almacenados, etiquetados en la carpeta data, y crea los conjuntos:
Por default:
	- TRAIN - 70 %
	- TEST  - 30 %
"""
from src import buscador
from src.TensorFlowUtils import pt
import tensorflow as tf
import sys
import random
import shutil
import glob
from sklearn.model_selection import train_test_split
import os
import cv2

class Split():
    def __init__(self, train, test, dir, dTrain, dTest):
        """
        Constructor
        :param train: valor en % para el conjunto de train
        :param test: valor en % para el conjunto de test
        :param dir: direccion que contiene las imagenes
        :param dTrain: direccion para el conjunto de train
        :param dTest: direccionn para el conjunto de test
        """
        self.train = train
        self.test = test
        self.dir = dir
        self.dTrain = dTrain
        self.dTest = dTest

    def correr(self, lblH):
        """
        Script para correr el proceso de dividir los datos
        :param lblH: array que contiene las etiquetas leidas desde la lista
        :return: None
        """
        try:
            print("path de imagenes: {}".format(self.dir))

            searcher = buscador.Buscador(path=self.dir, numero_clases=len(lblH), listaClases=lblH)
            searcher.encuentra_conjuntos_entrenamiento_test_desde_path()

            print("Imagenes cargadas!")

            x_dataXML = searcher.X_dataXML
            data_train, data_test = train_test_split(x_dataXML, test_size=self.test, random_state=101, shuffle=True)

            #Limpia la carpeta de train y test para no sobreescribir los datos
            self.limpiarbuffers(self.dTrain, self.dTest)

            #copiar archivo .xml a carpeta 'train'
            for y1 in data_train:
                if not os.path.exists(self.dTrain):
                    os.makedirs(self.dTrain)
                shutil.copy2(y1, self.dTrain)
            #copiar archivo .xml a carpeta 'test'
            for y2 in data_test:
                if not os.path.exists(self.dTest):
                    os.makedirs(self.dTest)
                shutil.copy2(y2, self.dTest)

            print("****** Datos dividios con EXITO ******** ")

        except Exception as ex:
            print(ex)


    def limpiarbuffers(self,dr1,dr2):
        """
        Limpiar las carpetas de train/test antes de sobreescribir los datos divididos
        :param dr1: path train
        :param dr2: path test
        :return:
        """
        if not os.path.exists(dr1):
            os.makedirs(dr1)
        if not os.path.exists(dr2):
            os.makedirs(dr2)

        folder = dr1
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

        folder = dr2
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)