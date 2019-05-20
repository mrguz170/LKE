# LKE Computer Vision Framework

Sistema de escritorio para el entrenamiento de redes neuronales usando [Google's TensorFlow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection)

![Py versions](https://img.shields.io/pypi/pyversions/donkeycar.svg)
![License](http://img.shields.io/:license-mit-blue.svg)


![LKE](https://camo.githubusercontent.com/7be7005a5bd74bb4bbb6058be5706870053a2a1e/68747470733a2f2f692e696d6775722e636f6d2f366f6b65446a7a2e6a7067)
![LKE](https://sigmoidal.io/wp-content/uploads/2017/11/object_detection_using_faster_rcnn.png)

## En LINUX:

## Comenzar:
1. Crear entorno de anaconda: 

	`conda env create -f anaconda-LKE.yml`
	
	#### NOTA: 
	Si no existe Anaconda instalado en tu equipo, puedes descargarlo desde [aqui](https://www.anaconda.com/distribution/).

2. Editar y Guardar variables de entorno.

	Localizar el directorio en tu Anaconda Prompt corriendo en terminal:
	
	`echo $CONDA_PREFIX`
	
	Introduce ese directorio y crea los subdirectorios y archivos con:
	```
	cd $CONDA_PREFIX
	mkdir -p ./etc/conda/activate.d
	mkdir -p ./etc/conda/deactivate.d
	touch ./etc/conda/activate.d/env_vars.sh
	touch ./etc/conda/deactivate.d/env_vars.sh
	```

3. Editar ./etc/conda/activate.d/env_vars.sh, copia y pega la siguiente linea:
	```
	export PYTHONPATH=$PYTHONPATH:`pwd`/tools/Tensorflow/research:`pwd`/tools/Tensorflow/research/slim
	```
4. Editar ./etc/conda/deactivate.d/env_vars.bat, copia y pega la siguiente linea:
	```
	unset PYTHONPATH
	```
	#### NOTA: 
	Cuando se active el entorno, la variable de entorno PYTHONPATH es cambiada al valor escrito dentro del archivo. Al desactivar el entorno, toda variable es eliminada.
	
5. Instalar Tensorflow

	Para una instalacion detallada seguir las [instrucciones de instalacion](https://www.tensorflow.org/install/) oficial. 
	Este sistema se creo usando la version 1.12, asi que se recomienda descargar tal version.
	Un usuario tipico puede instalar Tensorflow usando uno de los dos comandos siguientes:

	```
	# Por CPU
	pip install tensorflow==1.12
	# Por GPU
	pip install tensorflow-gpu==1.12
	```
	
	#### NOTA:
	La instalacion usando GPU requiere la activacion de los nucleos CUDA de la tarjeta, [aqui](https://medium.com/@zhanwenchen/install-cuda-and-cudnn-for-tensorflow-gpu-on-ubuntu-79306e4ac04e) una guia al respecto.
	
6. Re-compilar labelImg tool

	Para el etiquetado de las imagenes el sistema utiliza una herramienta llamada [labelImg](https://github.com/tzutalin/labelImg). Antes de comenzar es necesario recompilar sus archivos. Escribe en el directorio raiz del proyecto:
	```
	make -C `pwd`/tools/labelImg qt5py3
	```


## Requerimientos
- [Anaconda / Python 3.5](https://www.anaconda.com/)
- [TensorFlow 1.12](https://www.tensorflow.org/)
- [OpenCV 3.0](http://opencv.org/)


## Instalar COCO API

COCO es una gran base de datos para deteccion y segmentacion de objetos, debido a que los ultimos papers de investigacion usan el dataset COCO, 
asi como sus metricas para evaluar la precision (mAP), es necesario instalar su API. 
Mayor informacion sobre estas metricas puedes ser encontradas [aqui](https://medium.com/@timothycarlen/understanding-the-map-evaluation-metric-for-object-detection-a07fe6962cf3).

Ir a carpeta LKE/tools/Tensorflow/research, y corre:

	git clone https://github.com/cocodataset/cocoapi.git
	cd cocoapi/PythonAPI
	make

al finalizar corre el siguiente comando, nota que debes cambiar `<path-de-descarga>` por la ruta donde se encuentra almacenado el repositorio:

	cp -r pycocotools <path-de-descarga>/LKE/tools/Tensorflow/research
	
	#ejemplo:
	cp -r pycocotools /media/gustavo/gusgus/Machinelearning/LKE/tools/Tensorflow/research
	
## Guia de uso

Proporcionamos una [guia](https://docs.google.com/document/d/1CrtmGBZoLcD9aYmGgZjE_WwnHVdBgeOBcgIQe0GvO1s/edit?usp=sharing) para que puedas entrenar tus propios modelos.

## Licencia

The MIT License (MIT). Porfavor ir a [LICENSE](https://github.com/mrguz170/LKE/blob/master/LICENSE.md) para más información.

