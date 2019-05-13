# LKE Computer Vision Framework

Sistema de escritorio para el entrenamiento de redes neuronales usando [Google's TensorFlow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection)

![License](http://img.shields.io/:license-mit-blue.svg)

## Comenzar:
1. Crear anaconda environment

	`conda env create -f anaconda-LKE.yml`

2. Guardar variables entorno

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
4. Editar .\etc\conda\deactivate.d\env_vars.bat, copia y pega la siguiente linea:
	```
	unset PYTHONPATH
	```
	#### NOTA: 
	Cuando se active el entorno, las variables de entorno PYTHONPATH son cambiadas a los valores escritos dentro del 	archivo. Al desactivar el entorno, estos valores son borrados.
	
5. Instalar Tensorflow, para una instalacion detallada seguir [Tensorflow instrucciones de instalacion](https://www.tensorflow.org/install/). Un usuario tipico puede instalar Tensorflow usando uno de los dos comandos siguientes:

```
# Por CPU
pip install tensorflow
# Por GPU
pip install tensorflow-gpu
```



## Requirements
- [Anaconda / Python 3.5](https://www.anaconda.com/distribution/)
- [TensorFlow 1.12](https://www.tensorflow.org/)
- [OpenCV 3.0](http://opencv.org/)

## Compilar protobuf:



## Instalar COCO API

COCO es una gran base de datos para deteccion y segmentacion de objetos, debido a que los ultimos papers de investigacion usan el dataset COCO, 
asi como sus metricas para evaluar la precision (mAP), es necesario instalar su API. 
Mayor informacion sobre estas metricas puedes ser encontradas [aqui](https://medium.com/@timothycarlen/understanding-the-map-evaluation-metric-for-object-detection-a07fe6962cf3)
Ir a carpeta LKE/tools/Tensorflow/research, y corre:

	git clone https://github.com/cocodataset/cocoapi.git
	cd cocoapi/PythonAPI
	make

al finalizar corre el siguiente comando, nota que debes cambiar <path-de-descarga> por el directorio donde se encuentra almacenado el repositorio:

	cp -r pycocotools <path-de-descarga>/LKE/tools/Tensorflow/research
	
### ejemplo:
	cp -r pycocotools /media/gustavo/gusgus/Machinelearning/LKE/tools/Tensorflow/research
	
	


## Licencia

The MIT License (MIT). Please see the [LICENSE](https://github.com/mrguz170/LKE/blob/master/LICENSE.md) for more information.

