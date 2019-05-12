# LKE Computer Vision Framework

Sistema de escritorio para el entrenamiento de redes neuronales usando [Google's TensorFlow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection)

![License](http://img.shields.io/:license-mit-blue.svg)

## Getting Started:
1. Crear anaconda environment

	`conda env create -f anaconda-LKE.yml`

2. Guardar variables entorno

	Localizar el directorio en tu Anaconda Prompt corriendo en terminal:
	
	`%CONDA_PREFIX%`
	
	Introduce ese directorio y crea los subdirectorios y archivos con:
	```
	cd %CONDA_PREFIX%`
	mkdir .\etc\conda\activate.d
	mkdir .\etc\conda\deactivate.d
	type NUL > .\etc\conda\activate.d\env_vars.bat
	type NUL > .\etc\conda\deactivate.d\env_vars.bat
	```

3. Editar .\etc\conda\activate.d\env_vars.bat, copia y pega la siguiente linea:
	```
	export PYTHONPATH=$PYTHONPATH:`pwd`/tools/Tensorflow/research:`pwd`/tools/Tensorflow/research/slim
	```
4. Editar .\etc\conda\deactivate.d\env_vars.bat de la siguiente forma:
	```
	unset PYTHONPATH
	```

NOTA: 
Cuando se active el entorno, las variables de entorno PYTHONPATH son cambiadas a los valores escritos dentro del archivo. Al desactivar el entorno, estos valores son borrados.

# Compilar protobuf:



# Instalar COCO API

COCO es una gran base de datos para deteccion y segmentacion de objetos, debido a que los ultimos papers de investigacion usan el dataset COCO, 
asi como sus metricas para evaluar la precision (mAP), es necesario instalar su API. 
Mayor informacion sobre estas metricas puedes ser encontradas [aqui](https://medium.com/@timothycarlen/understanding-the-map-evaluation-metric-for-object-detection-a07fe6962cf3)

	git clone https://github.com/cocodataset/cocoapi.git
	cd cocoapi/PythonAPI
	make
	cp -r pycocotools /media/gustavo/gusgus/Docs_tesis/LKE/tools/Tensorflow/research/models/research/


## License

The MIT License (MIT). Please see the [license file](LICENSE) for more information.

