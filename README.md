# LKE Computer Vision Framework

Sistema de escritorio para el entrenamiento de redes neuronales usando [Google's TensorFlow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection)

![License](http://img.shields.io/:license-mit-blue.svg)

## Getting Started:
1. Crear anaconda environment

	'conda env create -f anaconda-LKE.yml'

2. Saving environment variables

	Localizar el directorio en tu Anaconda Prompt corriendo en terminal:
	
	%CONDA_PREFIX%
	
	Enter that directory and create these subdirectories and files:
	
	cd %CONDA_PREFIX%
	mkdir .\etc\conda\activate.d
	mkdir .\etc\conda\deactivate.d
	type NUL > .\etc\conda\activate.d\env_vars.bat
	type NUL > .\etc\conda\deactivate.d\env_vars.bat

3. Edit .\etc\conda\activate.d\env_vars.bat as follows:

	export PYTHONPATH=$PYTHONPATH:`pwd`/tools/Tensorflow/research:`pwd`/tools/Tensorflow/research/slim

4. Edit .\etc\conda\deactivate.d\env_vars.bat as follows:
	
	unset PYTHONPATH

NOTA: When you run conda activate analytics, the environment variables MY_KEY and MY_FILE are set to the values you wrote into the file. When you run conda deactivate, those variables are erased.


#Compilar protobuf:



#Instalar COCO API

COCO es una gran base de datos para deteccion y segmentacion de objetos, debido a que los ultimos papers de investigacion usan el dataset COCO, 
asi como sus metricas para evaluar la precision (mAP), es necesario instalar su API. 
Mayor informacion sobre estas metricas puedes ser encontradas [aqui](https://medium.com/@timothycarlen/understanding-the-map-evaluation-metric-for-object-detection-a07fe6962cf3)


	git clone https://github.com/cocodataset/cocoapi.git
	cd cocoapi/PythonAPI
	make
	cp -r pycocotools /media/gustavo/gusgus/Docs_tesis/LKE/tools/Tensorflow/research/models/research/





----------------------------------------------------------

-instalar Protobuf (checar)
conda install -c anaconda protobuf
