Cada proyecto contiene:


-/labels: 
	-/sets/			 	# Carpeta que contien los XML's correspondientes a los conjuntos de train/test (se crea al dividir los datos)
	train_labels.csv	# etiquetas en formato .csv		(se crea al convertir los datos)
	test_labels.csv		# etiquetas en formato .csv 	(se crea al convertir los datos)
	train.record		# entrada para la API (TRAIN) 	(se crea al convertir los datos)
	test.record			# entrada para la API (TEST) 	(se crea al convertir los datos)

	Aqui se generaran las etiquetas en formato (estas funcionan para TF API)

-/training: Contiene todos los archivos correspondientes al entrenamiento, labelmap.pbtxt, archivo de cofiguracion (file.config), events para mostrar los resultados del entrenamiento usando tensorboard. Cada cierto tiempo de entrenamiento el sistema genera una captura de sus resultados, estos 3 archivos son: 

      - .index
      - .meta
      - .data

