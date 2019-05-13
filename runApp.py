#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
Creado por: 
Gustavo Bañuelos Ochoa
Benemerita Universidad Autonoma de Puebla
Language and Knowledge Engineering (LKE Lab)

email: banuelos.201021581@gmail.com
follow me: https://github.com/mrguz170

"""
import os
import sys
import threading
import time
import shlex
import numpy as np
import requests
import subprocess
import signal
import codecs
import datetime
import webbrowser
import multiprocessing
import re
import csv
import tensorflow as tf
import tarfile
import inspect
import tensorboard as tb

from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal

from src.GUI.Principal import *
from src.GUI.new import *
from src import split
from src import xml_to_csv

#linux
OBJECTDETECTIONPATH = os.path.join(os.getcwd(), 'tools/Tensorflow/research/object_detection')


class Main1(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.nameProject = ''
        QtWidgets.QMainWindow.__init__(self)
        self.ui1 = Ui_NewWindow()
        self.ui1.setupUi(self)
        self.ui1.lineE2.setText('{}'.format(os.path.join(os.path.basename(os.getcwd()), 'projects')))
        self.ui1.buttonBox.accepted.connect(self.accept)
        self.ui1.buttonBox.rejected.connect(self.reject)
        self.ui1.lineE1.textEdited.connect(self.uline1)
        self.ui1.pushb_abrir.clicked.connect(self.abrirP)

    def uline1(self):
        """
        :return: update linea con la ubicación del nuevo proyecto
        """
        self.ui1.lineE2.setText('{}'.format(os.path.join(
                            os.path.basename(os.getcwd()),
                            'projects/{}'.format(self.ui1.lineE1.text())
        )))

    def abrirP(self):
        """
        Selecciona carpeta de algun proyecto existente, y abre la ventana principal de la app
        """
        dirAll = QFileDialog.getExistingDirectory(
            self,
            "Open a folder",
            os.path.join(os.getcwd(), 'projects'),
            QFileDialog.ShowDirsOnly
        )
        # SI EL CONTENIDO ES CORRECTO -> CAMBIAR LABEL 'labelWait'
        if (dirAll):
            self.nameProject = str(os.path.basename(dirAll))
            self._createMain(namep=self.nameProject, desc=self.ui1.lineE3.text())

        else:
            self.nameProject = ''

    def accept(self):
        """
        aceptar y crear nuevo proyecto
        :return:
        """
        print('aceptado')
        if self.ui1.lineE1.text() != '':

            if not os.path.exists(os.path.join(os.getcwd(), 'projects/{}'.format(self.ui1.lineE1.text()))):

                self.nameProject = os.path.join(os.getcwd(), 'projects/{}'.format(self.ui1.lineE1.text()))
                os.mkdir(self.nameProject) #creamos folder para proyecto

                self._createMain(namep=self.ui1.lineE1.text(), desc=self.ui1.lineE3.text())

            else:
                print('ya existe un proyecto con ese nombre')
                self.statusBar().showMessage('proyecto existente con ese nombre')


        else:
            print('El proyecto necesita un nombre')
            self.statusBar().showMessage('Agregue nombre al proyecto')

    def reject(self):
        print('rechazado')
        self.close()

    def _createMain(self, namep, desc):
        """
        metodo que crea la app principal
        :param namep: nombre del proyecto
        :param desc:  descripcion del proyecto
        :return:
        """
        myApp = mainApp(nameProject=namep, parent=self, desc=desc)
        myApp.show()
        self.hide()


class mainApp(QtWidgets.QMainWindow):
    def __init__(self, nameProject, parent, desc):
        self.labelHist = []
        self.trainVal = .7
        self.testVal = .3
        self.nameProject = nameProject
        self.sets = ['train', 'test']
        self.desc = desc

        # Atributos del Modelo
        self.modelConfig = ''               # nombre del modelo que se usara
        self.dirModelConfig = None          # path del archivo de configuración abierto
        self.numClases = None
        self.url = None                     # Almacena la url del archivo a descargar
        self.checkpointPath = ''            # checkpoint tomado para hacer inferencia en el grafico computacional
        self.exportfiles = ''               # nombre carpeta = {}_graph_{}.format(self.nameProject, self.num)

        # listas que guardan la lectura del archivo que lleva a la descarga de los modelos
        self.arrayConfigs = []
        self.arrayName = []
        self.arrayURL = []

        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        print('Proyecto creado: ' + self.nameProject)
        self.ui.lineEConfig.setText(self.modelConfig)
        self.setWindowTitle('LKE AI - Computer vision framework - Proyecto: {}'.format( self.nameProject))

        # Hilos usados
        self.thread = hilo()
        self.thread2 = hilo2()
        self.thread3 = hilo3()

        # Conexion con GUI
        self.ui.ButtonAbrir.clicked.connect(self.openNew)
        self.ui.SliderPorcentaje.valueChanged.connect(self.setTestValue)
        self.ui.buttonSplit.clicked.connect(self.runSplit)
        self.ui.mbutton1.clicked.connect(self.abrirALL)
        self.ui.mbutton2.clicked.connect(self.abrirSets)
        self.ui.mbutton3.clicked.connect(self.abrirALLConvert)
        self.ui.mbutton6.clicked.connect(self.abrirConfigs)
        self.ui.mbutton7.clicked.connect(self.abrirPrConfig)

        self.ui.miniB3_1.clicked.connect(self.abrirTrain)
        self.ui.savebutton.clicked.connect(self.saveConfigFile)
        self.ui.downModel.clicked.connect(self.downloadModel)
        self.ui.pBCancelDown.clicked.connect(self.cancelDonwload)

        self.ui.buttonConvert.clicked.connect(self.convertFiles)

        self.ui.buttonTRAIN.clicked.connect(self.comenzarTrain)
        self.ui.buttonStop.clicked.connect(self.stopTrain)
        self.ui.pbshowgraphs.clicked.connect(self.verGraficas)
        self.ui.toolBStopgraphs.clicked.connect(self.stopTB)

        self.ui.bt_openfile.clicked.connect(self.abrirArchivo)
        self.ui.buttonPlay.clicked.connect(self.play)

        self.ui.button_exportG.clicked.connect(self.exportGraph)
        self.ui.b_loadconfig.clicked.connect(self.abrirTrain)

        self.ui.tb_OK_clases.clicked.connect(self.load_lblmap)
        self.ui.b_lbl_map.clicked.connect(self.save_lblmap)


        # Señales conectadas correspondientes al hilo1 - entrenar modelo
        self.thread.signal.connect(self.threadDone)
        self.thread.signal2.connect(self.breakTrain)
        self.thread.signal3.connect(self.sigClear)

        # Señales conectadas correspondientes al hilo3 - donwload model
        self.thread3.signal.connect(self.resetVals)
        self.thread3.signal2.connect(self.downloading)
        self.thread3.signal3.connect(self.updatePBar)
        self.thread3.signal4.connect(self.downloadComplete)
        self.thread3.signal5.connect(self.showError)

        self.saveDescription()

    # ---------------------------------------------------------------------------------------------------
    # -----------------------------			MIS METDOOS			-----------------------------------------
    # ---------------------------------------------------------------------------------------------------
    def saveDescription(self):
        """
        guarda descripcion en la carpeta del proyecto
        :return:
        """
        file = open('{}/projects/{}/DESCRIPCION.txt'.format(os.getcwd(), self.nameProject), 'w+')
        file.write(str('Proyecto: {} \nCreado: {}'.format(self.nameProject, datetime.datetime.now() )))

        file.write('\n\n')
        if not (self.desc.__eq__("")):
            file.write('DESC: \n')
            file.write(self.desc)
            file.close()

    # ----	1
    def openNew(self):
        """
        Abrir labelImg para etiquetar las imagenes
        :return:
        """
        try:
            limg = "LKE/tools/labelImg/"
            mydir = os.path.dirname(os.getcwd())
            mydir = str(os.path.join(mydir, limg))

            subprocess.call(["python", "labelImg.py"], cwd=mydir)

        except Exception as e:
            print(e)
            self.statusBar().showMessage(e)
        
    # ----	2
    def setTestValue(self):
        """
        cambiar valor en la etiqueta del porcentaje para test
        :return:
        """
        b = 100
        self.trainVal = self.ui.SliderPorcentaje.value() / b
        self.ui.labeltestval.setText(str(100 - self.ui.SliderPorcentaje.value()))
        self.testVal = (100 - self.ui.SliderPorcentaje.value()) / b

    def runSplit(self):
        """
        Ejecutar split para dividir los datos, carpetas donde estan guardadas los datos a separar
        y donde se guardaran los conjuntos de TRAIN/TEST
        :return:
        """
        try:
            if self.ui.lineE2.text() != '':
                # path donde se guardaran los sets
                pathSets = os.path.join(os.getcwd(), "projects/{}/labels/sets".format(self.nameProject))
                train = str(os.path.join(pathSets, self.sets[0]))
                test  = str(os.path.join(pathSets, self.sets[1]))

                path_data = self.ui.lineE2.text()   #path todos los datos

                folder = os.path.join(os.getcwd(), "projects/{}/labels/".format(self.nameProject))
                folder2 = os.path.join(os.getcwd(), 'projects/{}/training/'.format(self.nameProject))

                if not os.path.exists(folder):
                    os.makedirs(folder)
                    os.makedirs(folder2)

                sp = split.Split(train=self.trainVal, test=self.testVal, dir=path_data, dTrain=train, dTest=test)
                sp.correr(self.labelHist)

                self.statusBar().showMessage("Conjuntos creados correctamente en {}".format(pathSets))
                self.ui.lineE4.setText('{}'.format(pathSets))
                self.ui.buttonConvert.setEnabled(1)
                self.ui.frame_4.setEnabled(1)  # inhabilitar frame TFRECORD

            else:
                self.statusBar().showMessage("Abrir carpeta con imagenes etiquetadas")

        except Exception as ex:
            print(ex)
            self.statusBar().showMessage("error al dividir los datos")


    def abrirALL(self):
        """
        Selecciona carpeta donde se encuentran todas las imagenes y los xml's
        :return:
        """
        dirAll = QFileDialog.getExistingDirectory(
            self,
            "Open a folder",
            os.path.join(os.getcwd(), 'data'),
            QFileDialog.ShowDirsOnly
        )
        # SI EL CONTENIDO ES CORRECTO -> CAMBIAR LABEL 'labelWait'
        if(dirAll):
            #self.ui.labelWait.setText('Folder valido')
            self.ui.lineE2.setText(str(dirAll))
            self.ui.lineE5.setText(str(dirAll))
            self.ui.buttonSplit.setEnabled(1)

        else:
            self.ui.buttonSplit.setEnabled(0)
            self.ui.lineE2.setText('')


    def abrirSets(self):
        """
        Selecciona carpeta donde se guardaran los conjuntos de train/test para dividirlos segun el %
        :return:
        """
        pathSets = QFileDialog.getExistingDirectory(
            self,
            "Open a folder",
            os.path.join(os.getcwd(), 'projects/{}/labels'.format(self.nameProject)),
            QFileDialog.ShowDirsOnly
        )

        if (pathSets):
            self.ui.lineE4.setText(str(pathSets))
            self.ui.buttonConvert.setEnabled(1)

        else:
            self.ui.buttonConvert.setEnabled(0)
            self.ui.buttonConvert.setText('')


    # ----	3
    def convertFiles(self):
        """
        Metodo llamado al oprimir el boton de convertir a formato .CSV y TFRecord
        :return:
        """
        try:
            if self.ui.lineE4.text() != '' and self.ui.lineE5.text() != '':

                if self._toCSV():   

                    if(self._generarTFRecord()):     #crear TENSORFLOW RECORD
                        print('TFRecord creados con exito')
                    else:
                        print('algo salio mal al crear TFRecord')

                else:
                    print('algo salio mal al crear CSV')
            else:
                print('No se puede inciar')

        except Exception as ex:
            print(ex)

    def _toCSV(self):
        """
        convertir a csv
        :return:
        """
        try:
            for directory in self.sets:
                path = os.path.join(self.ui.lineE4.text(), directory)
                print(path)
                converter = xml_to_csv.xmltocsv(path)
                xml_df = converter.xml_to_csv(path=path)
                image_path = os.path.join(os.getcwd(),
                                          "projects/{}/labels/{}_labels.csv".format(self.nameProject, directory))
                folder = os.path.dirname(image_path)

                xml_df.to_csv(image_path, index=None)
                print('Conversión exitosa')

            self.statusBar().showMessage('Conversión exitosa, Guardado en: {}'.format(folder))
            return True

        except Exception as ex:
            print(ex)
            return False

    # ----  4
    def _generarTFRecord(self):
        """
        Metodo llamado al oprimir boton 'Generar TFRecord
        :return:
        """
        try:
            argslist = []
            mydir = str(os.path.join(os.getcwd(), 'tools'))
            dirTF = str(os.path.dirname(self.ui.lineE4.text()))

            for set in self.sets:
                #arg1 = str(os.environ['ENV1'])  
                arg1 = 'python'
                arg2 = 'generate_tfrecord.py'
                arg3 = '--csv_input={}/{}_labels.csv'.format(dirTF, set)
                arg4 = '--output_path={}/{}.record'.format(dirTF, set)
                arg5 = '--image_dir={}'.format(self.ui.lineE5.text())
                argslist = [arg1, arg2, arg3, arg4, arg5]
                subprocess.call(argslist, cwd=mydir)  # run
            
            self.statusBar().showMessage("TFRecord creados correctamente en: {}".format(
    															os.path.dirname(self.ui.lineE4.text())))
            return True

        except Exception as ex:
            print(ex)
            self.statusBar().showMessage("Error al crear TF Record")
            return False

    def abrirALLConvert(self):
        """
        Selecciona carpeta donde se encuentran todas las imagenes y los xml's
        :return:
        """
        dirAll = QFileDialog.getExistingDirectory(
            self,
            "Open a folder",
            os.path.join(os.getcwd(), 'data'),
            QFileDialog.ShowDirsOnly
        )
        if (dirAll):
            self.ui.lineE5.setText(str(dirAll))
        else:
            self.ui.lineE5.setText('')


    # 2 ---------------------- Configurar label_map.pbtxt y modelo EXISTENTE ----------------------
    #   -------------------------------------------------------------------------------------------
    def load_lblmap(self):
        """
        Se crea:
            "item {
                id: 1
                name: 'etiqueta 1'
            }"
        :return:
        """
        try:

            aux = self.ui.spinBox.value()
            aux = int(aux)  # la convertimos a int, si es una letra cae en la excepccion
            self.ui.textE_lblmap.clear()
            for x in range(aux):
                self.ui.textE_lblmap.append("item {")
                self.ui.textE_lblmap.append("   id: {}".format(x + 1))
                self.ui.textE_lblmap.append("   name: 'etiqueta {}'".format(x + 1))
                self.ui.textE_lblmap.append("}")
                self.ui.textE_lblmap.append("")

            self.statusBar().showMessage('{} Clases seran cargadas'.format(aux))

        except Exception as ex:
            print(ex)


    def save_lblmap(self):
        """
        Guardar archivo 'label_map.pbtxt'
        :return:
        """
        try:
            name, _ = QFileDialog.getSaveFileName(self,
                                                     'Save File',
                                                     os.path.join(os.getcwd(),
                                                     "projects/{}/training/label_map.pbtxt".format(self.nameProject)),
                                                     "label_map file (*.pbtxt)")

            if name:
                file = open(name, 'w')
                text = self.ui.textE_lblmap.toPlainText()
                file.write(text)
                file.close()
                self.statusBar().showMessage("Guardado exitosamente")
        except Exception as ex:
            print(ex)
            print('error al guardar label_map.pbtxt')



    def abrirConfigs(self):
        """
        Abre la carpeta '/object_detection/samples/' para elegir un modelo
        :return:
        """
        d = os.path.join(OBJECTDETECTIONPATH, "samples/configs/")

        dirconfigs, _ = QFileDialog.getOpenFileName(
            self,
            "Open a folder",
            d,
            "config(*.config)"
        )

        if dirconfigs:
            self.modelConfig = str(os.path.basename(dirconfigs))
            self.ui.lineE9.setText(self.modelConfig)
            self.statusBar().showMessage("Puedes DESCARGAR el Modelo seleccionado ahora")
            self.ui.progressBar.setValue(0)
            self.cargarConfigs()

    def cargarConfigs(self):
        """
        boton OK (default)
        carga el archivo especificado desde la carpeta ~/Documentos/LKE_framework/object_detection/samples/configs/
        :return:
        """
        try:

            self.dirModelConfig = os.path.join(OBJECTDETECTIONPATH, "samples/configs/{}".format(str(self.ui.lineE9.text())))

            print("Modelo NUEVO seleccionado: {}".format(str(self.dirModelConfig)))

            file = open(self.dirModelConfig, 'r')
            with file:
                text = file.read()
                self.ui.textEdit1.setText(text)

            self.ui.downModel.setEnabled(1)
            self.ui.pBCancelDown.setEnabled(1)
        except Exception as ex:
            print(ex)

    # 2.2 - Cargar modelo PREVIAMENTE GUARDADO
    def abrirPrConfig(self):
        """
        Abre la carpeta training de mi proyecto para elegir un modelo usado con anterioridad
        :return:
        """
        d = os.path.join(os.getcwd(), "projects/{}/training".format(self.nameProject))

        dirconfigs, _ = QFileDialog.getOpenFileName(
            self,
            "Open a folder",
            d,
            "config(*.config)"
        )

        if dirconfigs:
            self.modelConfig = str(os.path.basename(dirconfigs))
            self.ui.lineE10.setEnabled(1)
            self.ui.lineE10.setText(self.modelConfig)
            self.cargarConfigs2()


    def cargarConfigs2(self):
        """
        boton OK (personalizado)
        carga el archivo especificado desde la carpeta ~/Documentos/LKE_framework/object_detection/samples/configs/
        :return:
        """
        try:
            self.dirModelConfig = os.path.join(os.getcwd(),
                                 "projects/{}/training/{}".format(self.nameProject, str(self.ui.lineE10.text())))

            print("Modelo PREVIO seleccionado: {}".format(self.dirModelConfig))

            file = open(self.dirModelConfig, 'r')
            with file:
                text = file.read()
                self.ui.textEdit1.setText(text)
            self.ui.lineE3_1.setText(self.modelConfig)

        except Exception as ex:
            print(ex)

    def saveConfigFile(self):
        """
        guardar archivo cargado como copia: src -> carpeta /tools/object_detection/samples/configs/
                                            dest -> carpeta /projects/{name_project}/training/
        :return:
        """
        try:

            name, _ = QFileDialog.getSaveFileName(self,
                                                     'Save File',
                                                     os.path.join(os.getcwd(),
                                                                  "projects/{}/training/{}".format(self.nameProject,
                                                                                                   self.modelConfig)),
                                                     "Config files (*.config)"
                                                     )

            if name:
                file = open(name, 'w')
                text = self.ui.textEdit1.toPlainText()
                file.write(text)
                file.close()
                self.statusBar().showMessage("Guardado exitosamente")

        except Exception as ex:
            print(ex)
    
    #--------------
    def downloadModel(self):
        """
        descargar modelo
        buscar en el archivo '/src/model4download.csv' la ruta especificada de descarga del modelo segun el archivo de configuracion precargado
        """
        self.ui.downModel.setEnabled(0)

        m4d = os.path.join(os.getcwd(), "src/models4download.csv")
        flag = False
        url = None

        try:
            # abrir modelos para descarga
            with open(m4d, 'r') as csvFile:
                reader = csv.reader(csvFile)
                for row in reader:
                    if(self.ui.lineE9.text() in row):
                        print(row[1])
                        url = row[1]
                        flag = True

            csvFile.close()

            self.thread3.url = url  # pasamos url al hilo 3
            self.url = url         # pasamos url a ventana principal

        except Exception as ex:
            print(ex)
            flag = False

        if not flag:
            self.statusBar().showMessage("No se puede iniciar la descarga")
            self.ui.downModel.setEnabled(1)
        else:
            try:
                # lazamos thread para descargar el modelo
                self.thread3.start()

            except Exception as ex:
                print(ex)
                

    def cancelDonwload(self):
        """
        cancelar descarga del modelo seleccionado en la carpeta ~/models
        :return:
        """
        if self.thread3.isRunning():
            try:
                print("Hilo activado y listo para detener")
                self.ui.downModel.setEnabled(1)
                self.ui.progressBar.setValue(0)

                modelsDir = str(os.path.join(os.getcwd(), "models"))  # se guarda en carpeta models
                filename = os.path.join(modelsDir, os.path.basename(self.url))
                os.remove(filename)
                self.thread3.terminate()
                self.ui.downModel.setEnabled(1)

            except Exception as ex:
                print(ex)
                print('!error descargar modelo')
        else:
            print("Hilo inactivo")


# -------------------- Signals para thread3 (descargar modelo)
    def resetVals(self):
        """
        signal 1
        """
        self.ui.download.setText('Modelo actualmente descargado')
        self.statusBar().showMessage("Descargando...")
        self.ui.progressBar.setValue(100)
        self.ui.downModel.setEnabled(1)

    def downloading(self):
        """
        signal 2
        """
        #self.ui.download.setText('Descargando...')
        self.statusBar().showMessage("Descargando...")


    def updatePBar(self, ok):
        """
        signal 3
        """
        self.ui.progressBar.setValue(ok)

    def downloadComplete(self):
        """
        signal 4
        """
        #self.ui.download.setText("Descarga Completada!")
        self.statusBar().showMessage("Descarga Completada")
        self.ui.downModel.setEnabled(1)

    def showError(self):
        """
        signal 5
        """
        self.statusBar().showMessage("!error descargar modelo")
    #-----------------------

# --------------------------------------------------------------------------------------------------
# ----------------------------------------     TRAINING     ----------------------------------------
    def abrirTrain(self):
        """
        Asegurarse de cual .config se va a usar
        :return:
        """
        d = os.path.join(os.getcwd(), "projects/{}/training".format(self.nameProject))

        dirconfigs, _ = QFileDialog.getOpenFileName(
            self,
            "Open a folder",
            d,
        )

        if dirconfigs:
            self.ui.lineE3_1.setText(str(os.path.basename(dirconfigs)))
            self.modelConfig = str(os.path.basename(dirconfigs))
            self.ui.lineEConfig.setText(self.modelConfig)

        else:
            self.ui.lineE3_1.setText('')
            self.ui.lineEConfig.setText('')


    def comenzarTrain(self):
        """
        Se lanza thread para comenzar el entrenamiento
        :return:
        """
        if(str(self.ui.lineE3_1.text()) != ''):
            try:
                self.ui.buttonTRAIN.setEnabled(0)
                self.thread.nameP = self.nameProject          #pasar nombre de proyecto a hilo 1
                self.thread.fileCfg = self.ui.lineE3_1.text() #pasar file config a hilo 1
                self.thread.start()

            except Exception as ex:
                print(ex)
                print('Entrenamiento interrumpido')
        else:
            print('No se puede iniciar el entrenamiento. Seleccione un archivo valido de configuración')
            self.statusBar().showMessage('No se puede iniciar el entrenamiento. Seleccione un archivo valido de configuración')
            pass

    # -------------------- Signals para thread1 (Entrenamiento)
    def breakTrain(self):
        self.ui.buttonTRAIN.setEnabled(1)

    def stopTrain(self):
        """
        Detener TRAIN
        :return:
        """
        try:
            if self.thread.isRunning():
                print("Hilo activado y listo para detener")
                self.ui.buttonTRAIN.setEnabled(1)
                self.ui.textEdit_3.insertPlainText("------------ Training STOP ---------------")
                os.killpg(os.getpgid(self.thread.p.pid), signal.SIGKILL)
                self.thread.terminate()

            else:
                print("Hilo inactivo")
                self.ui.buttonTRAIN.setEnabled(1)

        except Exception as ex:
            print(ex)

    def threadDone(self, stdout):
        """
        Actualiza la salida que se muestra como consola
        :param stdout: Linea actual a imprimir en consola
        :return:
        """
        self.ui.textEdit_3.insertPlainText(str(stdout))
        self.ui.textEdit_3.insertPlainText("\n")
        self.ui.textEdit_3.moveCursor(QtGui.QTextCursor.End)
        self.ui.textEdit_3.ensureCursorVisible()

    def sigClear(self):
        """
        Limiar consola antes de volver a inciar Entrenamiento
        :return:
        """
        self.ui.buttonTRAIN.setEnabled(0)
        self.ui.textEdit_3.clear()


    def stopTB(self):
        """
        Detener hilo2 (TENSOBOARD)
        :return:
        """
        if not self.thread2.isRunning():
            print("Hilo inactivo")
        else:
            print("Hilo activado y listo para detener")
            self.thread2.terminate()
        


# --------------------------------------------------------------------------------------------------
# ------------------------------------    TESTING parte 1   ----------------------------------------

    def verGraficas(self):
        """
        Cargamos graficas usando TENSORBOPARD
        :return:
        """
        try:
            arg1 = 'python'
            arg2 = 'main.py'
            arg3 = '--logdir={}'.format(os.path.join(os.getcwd(), "projects/{}/training/".format(self.nameProject)))
            
            self.thread2.port = str(self.ui.spinBport.value())
            arg4 = '--port={}'.format(self.ui.spinBport.value())

            #modificamos las variables dentro del hilo para que tome esos valores
            #al momento de correr tensorboard

            self.thread2.list = [arg1, arg2, arg3, arg4]
            self.thread2.dir =str(os.path.dirname(inspect.getfile(tb)))

            self.thread2.start()

        except Exception as e:
            raise e
            

#------------------------------------    TESTING parte 2   ----------------------------------------
    def abrirArchivo(self):
        """
        :return:
        """
        if (self.ui.rb_imagen.isChecked()):
            self._abrirImagen()

        if (self.ui.rb_video.isChecked()):
            self._abrirVideo()


    def _abrirImagen(self):
        """
        Abrir video o imagen de alguna carpeta

        # /home/gustavo/Documentos/LKE_framework/tools/TensorFlow/research/object_detection/object_detection_test.py --image_dir=/home/gustavo/Documentos/LKE_framework/data/classification/image4.jpg
        :return:
        """
        dirconfigs, _ = QFileDialog.getOpenFileName(
            self,
            "Open a folder",
            os.path.join(os.getcwd(), 'data'),
            filter="Images (*.jpg *.png *.jpeg)"
        )

        try:
            if dirconfigs:
                self.ui.buttonPlay.setEnabled(1)
                self.ui.lineEpathvideo.setText(str(dirconfigs))
            else:
                self.ui.buttonPlay.setEnabled(0)

        except Exception as ex:
            print(ex)


    def _abrirVideo(self):
        """
        Abrir video o imagen de alguna carpeta

        # /home/gustavo/Documentos/LKE_framework/tools/TensorFlow/research/object_detection/object_detection_test.py --image_dir=/home/gustavo/Documentos/LKE_framework/data/classification/image4.jpg
        :return:
        """
        dirconfigs, _ = QFileDialog.getOpenFileName(
            self,
            "Open a folder",
            os.path.join(os.getcwd(), 'data'),
            filter="Video (*.avi *.mp4)"
        )

        try:
            if dirconfigs:
                self.ui.buttonPlay.setEnabled(1)
                self.ui.lineEpathvideo.setText(str(dirconfigs))
            else:
                self.ui.buttonPlay.setEnabled(0)

        except Exception as ex:
            print(ex)


    def play(self):
        """
        PLay video o imagen usando la red neuronal
        :return:
        """
        try:
            if (self._checkexport()): #checar valida este cargada

                self.numClases = self._checkclsslbl_map()  # obtiene el numero de clases

                if self.numClases.__eq__(-1):
                    print('error al leer labelmap.pbtxt')

                else:

                    if (self.ui.rb_imagen.isChecked()):
                        if(os.path.exists(self.ui.lineEpathvideo.text())):

                            arg1 = 'python'
                            arg2 = 'object_detection_test.py'
                            arg3 = '--image_dir={}'.format(self.ui.lineEpathvideo.text())
                            arg4 = '--graph_exported={}'.format(self.checkpointPath)
                            arg5 = '--label_map={}'.format(os.path.join(os.getcwd(),
                                                        "projects/{}/training/label_map.pbtxt".format(self.nameProject)))
                            arg6 = '--numClass={}'.format(self.numClases)

                            argslist = [arg1, arg2, arg3, arg4, arg5, arg6]
                            subprocess.call(argslist, cwd=OBJECTDETECTIONPATH)  # run
                            self.statusBar().showMessage('Cargado con exito')

                        else:
                            self.statusBar().showMessage('path {} no existe'.format(self.ui.lineEpathvideo.text()))

                    elif(self.ui.rb_video.isChecked()):

                        if (os.path.exists(self.ui.lineEpathvideo.text())):

                            arg1 = 'python'
                            arg2 = 'object_detection_test_video.py'
                            arg3 = '--image_dir={}'.format(self.ui.lineEpathvideo.text())
                            arg4 = '--graph_exported={}'.format(self.checkpointPath)
                            arg5 = '--label_map={}'.format(os.path.join(os.getcwd(),
                                                        "projects/{}/training/label_map.pbtxt".format(self.nameProject)))
                            arg6 = '--numClass={}'.format(self.numClases)

                            argslist = [arg1, arg2, arg3, arg4, arg5, arg6]
                            subprocess.call(argslist, cwd=OBJECTDETECTIONPATH)  # run

                            self.statusBar().showMessage('Cargado con exito')
                        else:
                            self.statusBar().showMessage('path {} no existe'.format(self.ui.lineEpathvideo.text()))

            else:
                self.statusBar().showMessage("error: exporte un checkpoint valido ")

        except Exception as ex:
            print(ex)


    def _checkexport(self):
        """
        permite verificar si ya ha sido asignado un numero de checkpoint valido
        :return:
        """
        if (self.checkpointPath.__eq__('')):
            print('Debe exportar primero un checkpoint valido')
            self.statusBar().showMessage('Debe exportar primero un checkpoint valido')
            return False
        else:
            return True #true porque no esta vacio

    def _checkclsslbl_map(self):
        """
        verificar si la cantidad de clases dentro del archivo lbl_map.pbtxt,
        y regresa el valor que se mandara como parametro a funcion 'play'
        :return:
        """
        try:

            lbl_map = os.path.join(os.getcwd(), "projects/{}/training/label_map.pbtxt".format(self.nameProject))
            cnt = 0

            with open(lbl_map, 'r') as l:
                for line in l:
                    aux = line.find('id')
                    if not aux.__eq__(-1):
                        cnt += 1

            return cnt

        except Exception as ex:
            print(ex)
            return -1


#-----------------

    def _checkModelConfig(self):
        """
        permite verificar si el archivo de configuracion esta cargado
        :return:
        """
        if (self.modelConfig.__eq__('')):
            print('Debe cargar primero el archivo de configuración')
            self.statusBar().showMessage('Debe cargar primero el archivo de configuración')
            return False
        else:
            return True #true porque no esta vacio


    def exportGraph(self):
        """
        exportar grafico computacional para poder usarlo con nuestros datos, se le pueden pasar como parametros el numero de entrenamiento
        especifico o por default tomar el ultimo guardado correctamente
        # Para exportar el grafico computacional despues del entrenamiento es necesario correr el siguiente codigo
        # From tensorflow/models/research/

            python3 export_inference_graph.py \
            --input_type image_tensor \
            --pipeline_config_path /home/gustavo/Documentos/LKE_framework/projects/mesas/training/ssd_mobilenet_v1_pets.config \
            --trained_checkpoint_prefix /home/gustavo/Documentos/LKE_framework/projects/mesas/training/model.ckpt-2898 \
            --output_directory /home/gustavo/Documentos/LKE_framework/projects/mesas/training/mesas_graph

        :return:
        """
        try:
            if(self._checkModelConfig()):
                num_check = ''
                b = 0       #si b = 1 los datos son validos y se puede exportar

                #cambiar el checkpoint segun sea el radioButton
                if(self.ui.rb_lastCheck.isChecked()):

                    num_check = self._findlastcheckp()  #buscar el ultimo
                    if num_check.__eq__(-1):    # regressa -1 si da error al buscar
                        b = 0

                    else:
                        print('checkpoint = {}'.format(num_check))
                        b = 1

                if(self.ui.rb_manualCheck.isChecked()):

                    if(str(self.ui.lineE_checkpoint.text()) == ''):
                        self.statusBar().showMessage('escribe un numero valido')
                        print('escribe un numero valido')
                        b = 0
                    else:
                        num_check = self.ui.lineE_checkpoint.text()
                        print('checkpoint = {}'.format(num_check))
                        # metodo buscar si el numero de checkpoint es valido
                        # si no es valido informamos, si lo es bandera = 1
                        b = self._validarCheckpoint(num_check)


                arg1 = 'python'
                arg2 = 'export_inference_graph.py'
                arg3 = '--input_type image_tensor'
                arg4 = '--pipeline_config_path {}/projects/{}/training/{}'.format(os.getcwd(), 
                													self.nameProject, self.modelConfig)

                #si la bandera == 1 entonces corremos el comando
                if(b.__eq__(1)):
                    self.exportfiles = '{}_graph_{}'.format(self.nameProject, num_check)

                    arg5 = '--trained_checkpoint_prefix {}/projects/{}/training/model.ckpt-{}'.format(
                    										os.getcwd(), self.nameProject, num_check)

                    arg6 = '--output_directory {}/projects/{}/training/{}'.format(
                    										os.getcwd(), self.nameProject, self.exportfiles)

                    path = os.path.join(os.getcwd(), 'projects/{}/training/{}'.format(
                    													self.nameProject, self.exportfiles))
                    
                    command = arg1 + ' ' + OBJECTDETECTIONPATH + '/' + arg2 + ' ' + arg3 + ' ' + arg4 + ' ' + arg5 + ' ' + arg6

                    self.statusBar().showMessage('Checkpoint valido')
                    self._exportar(path, command)
                else:
                    print('no se puede iniciar')
                    self.statusBar().showMessage('Error: Intente un checkpoint valido')

        except Exception as ex:
            print(ex)
            self.statusBar().showMessage('error al exportar')

    def _findlastcheckp(self):
        """
        busca ultimo checkpoint para exportarlo
        :return:
        """
        try:

            dirCheckpoint = os.path.join(os.getcwd(), 'projects/{}/training/'.format(self.nameProject))
            chkp = []
            aux = []
            for root, dirs, files in os.walk(dirCheckpoint):
                for file_name in files:
                    indexstr = file_name.find('model.ckpt-')
                    if not (indexstr.__eq__(-1)): # si es diferente de -1
                        #comparamos valor
                        [chkp.append(float(s)) for s in re.findall(r'-?\d+\.?\d*', file_name)] #se buscan los numeros de train
                        aux.append(int(chkp[0] * -1))  #el primer numero se agrega a una lista
                        chkp.clear() # se limpiar el vector de busqueda
            mayor = max(aux)   #se saca el mayor y ese es el ultimo

            print('LAST CHECKPOINT {}'.format(mayor))
            return mayor

        except Exception as ex:
            print(ex)
            return mayor == -1


    def _validarCheckpoint(self, num_check):
        """
        validar si el numero de checkpoint existe
        :param num_check:
        :return:
        """
        dirCheckpoint = os.path.join(os.getcwd(), 'projects/{}/training/'.format(self.nameProject))
        for root, dirs, files in os.walk(dirCheckpoint):
            for file_name in files:
                indexstr = file_name.find('model.ckpt-{}.meta'.format(num_check))
                if not (indexstr.__eq__(-1)): # si es diferente de -1
                    print('Si existe {}'.format('model.ckpt-{}.meta'.format(num_check)))
                    return 1      # regresamos 1 para informar que si exite
                else:
                    b = 0
        return b


    def _exportar(self, path, command):
        """
        :param path:
        :param command:
        :return:
        """
        # run comando
        if (os.path.exists(path)):
            self.statusBar().showMessage('Ya existe la carpeta'
                                         ' "{}" en: {}'.format(self.exportfiles, os.path.dirname(path)))
            self.checkpointPath = path
            self.ui.lineE_checkpoint_main.setText(os.path.basename(self.checkpointPath))

        else:
            print('Creando carpeta {}'.format(self.exportfiles))
            subprocess.Popen(shlex.split(command))
            time.sleep(5)
            self.checkpointPath = path
            self.ui.lineE_checkpoint_main.setText(os.path.basename(self.checkpointPath))
            self.statusBar().showMessage('Carpeta '
                                         '"{}" exportada'.format(self.exportfiles))


    
#  -------------------------    THREADS for DOWNLOAD MODEL  ----------------------------------
# ------------------------------------------------------------------------------------------
class hilo3(QtCore.QThread):
    """
    clase hilo que corre el proceso descargar el modelo
    """
    signal = pyqtSignal()
    signal2 = pyqtSignal()
    signal3 = pyqtSignal("int")
    signal4 = pyqtSignal()
    signal5 = pyqtSignal()

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent=app)
        self.url = None


    def run(self):
        """
        iniciar descarga del modelo, si ya exite en el dir modelos ya no se descarga, 
        si no comenzara automaticamente
        :return:
        """
        try:
            time.sleep(2)
            print('In thread')
            modelsDir = str(os.path.join(os.getcwd(), "models"))  # se guarda en carpeta models
            filename = self.url.split('/')[-1]
            m = os.path.join(modelsDir, os.path.basename(self.url))

            if os.path.exists(m):
                pass

            else:
                with open(os.path.join(modelsDir, filename), 'wb') as f:
                    self.signal2.emit()
                    response = requests.get(self.url, stream=True)
                    total = response.headers.get('content-length')
                    if total is None:
                        f.write(response.content)
                    else:
                        downloaded = 0
                        total = int(total)
                        for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                            downloaded += len(data)
                            f.write(data)
                            done = int(50 * downloaded / total)
                            ok = done * 2
                            self.signal3.emit(ok)
                            sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
                            sys.stdout.flush()

                self.signal4.emit()

                sys.stdout.write('\n')
                f.close()

                tar = tarfile.open(m)
                tar.extractall(path=os.path.dirname(m))
                tar.close()

            print('End thread 3')

        except Exception as ex:
            print(ex)
            print('!error descargar modelo')
            self.signal5.emit()

#  -------------------------    THREADS FOR TEST PHASE  ----------------------------------
# ------------------------------------------------------------------------------------------
class hilo2(QtCore.QThread):
    """
    clase hilo que corre el proceso de entrenamiento
    """
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent=app)
        self.list = None
        self.port = None
        self.dir  = None
        self.p = None

    def run(self):
        """
        Run hilo para visualizar graficas usando tensorboard
        :return:
        """
        time.sleep(2)
        print('In thread')
        self._launchTensorBoard()
        print('End thread2')

    def _launchTensorBoard(self):
        """
        lanza TB en el canvas para web
        :return:
        """
        try:

            subprocess.call(self.list, cwd=self.dir)
            #self.p = subprocess.Popen(shlex.split(self.list), cwd=self.dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid, shell=False)

            def_URL_test = 'http://127.0.0.1:{}'.format(self.port)
            print('Abrir TensorBoard ---> ' + def_URL_test)

            webbrowser.open_new_tab(def_URL_test) #abre nueva pestaña en el navegador
            return

        except Exception as ex:
            print(ex)

#  -------------------------    THREADS FOR TRAIN PHASE  ----------------------------------
# ------------------------------------------------------------------------------------------
class hilo(QThread):
    """
	Clase hilo que corre el proceso de entrenamiento
    Example usage:
    
    # From the tensorflow/models/research/ directory
    PIPELINE_CONFIG_PATH={path to pipeline config file}
    MODEL_DIR={path to model directory}
    NUM_TRAIN_STEPS=50000
    SAMPLE_1_OF_N_EVAL_EXAMPLES=1
    python object_detection/model_main.py \
        --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
        --model_dir=${MODEL_DIR} \
        --num_train_steps=${NUM_TRAIN_STEPS} \
        --sample_1_of_n_eval_examples=$SAMPLE_1_OF_N_EVAL_EXAMPLES \
        --alsologtostderr
    """
    signal = pyqtSignal("QString")
    signal2 = pyqtSignal()
    signal3 = pyqtSignal()


    def __init__(self, parent=None):
        QThread.__init__(self, parent=app)
        self.nameP = None
        self.fileCfg = None
        self.p = None

    def run(self):
        time.sleep(2)
        print('In THREAD TRAINING')
        self._runtrain()
        print('END THREAD TRAINING')

    def _runtrain(self):
        mydirpath = os.path.dirname(OBJECTDETECTIONPATH) #path Object_detection

        model = str(os.path.join(os.getcwd(), "projects/{}/training/".format(self.nameP)))
   
        arg1 = 'python'
        arg2 = 'object_detection/model_main.py'
        arg3 = '--pipeline_config_path={}{}'.format(model, self.fileCfg)
        arg4 = '--model_dir={}'.format(model)
        arg5 = '--num_train_steps={}'.format(50000)
        arg6 = '--sample_1_of_n_eval_examples={}'.format(100)
        arg7 = '--alsologtostderr'

        command = arg1 + ' ' + arg2 + ' ' + arg3 + ' ' + arg4 + ' ' + arg5 + ' ' + arg6 + ' ' + arg7

        print('Comando completo:' + command)

        self.signal.emit("Iniciando...")

        try:
            self.p = subprocess.Popen(shlex.split(command), cwd=mydirpath, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid, shell=False)

            print('-- proceso creado --')

            while True:
                line = self.p.stdout.readline()
                print(str(line))
                self.signal.emit(str(line))
                if line.__eq__("b""") and self.p.poll() != None:
                    self.signal2.emit()
                    break

        except Exception as ex:
            print(ex)


# ---------------------  	MAIN      -------------------------------
# --------------------------------------------------------------------
if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QtWidgets.QApplication([])

    newWin = Main1()
    newWin.show()
    sys.exit(app.exec_())
# --------------------------------------------------------------------
