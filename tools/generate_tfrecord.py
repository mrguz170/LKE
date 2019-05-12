"""
Usage:
  # From tensorflow/models/

Antes de crear los TFRecords es necesario insertar:

# From LKE/
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

#crear para sets de train
python3 generate_tfrecord.py --csv_input=projects/mesas/labels/train_labels.csv --output_path=projects/mesas/labels/train.record --image_dir=data/classification/sets/train
python3 generate_tfrecord.py --csv_input=/home/gustavo/Documentos/LKE_framework/projects/mesas/labels/train_labels.csv --output_path=/home/gustavo/Documentos/LKE_framework/projects/mesas/labels/train.record --image_dir=/home/gustavo/Documentos/LKE_framework/data/classification/sets/train

#crear para sets de test
python generate_tfrecord.py --csv_input=projects/mesas/labels/test_labels.csv --output_path=projects/mesas/labels/test.record --image_dir=data/classification/sets/test
python3 generate_tfrecord.py --csv_input=/home/gustavo/Documentos/LKE_framework/projects/mesas/labels/test_labels.csv --output_path=/home/gustavo/Documentos/LKE_framework/projects/mesas/labels/test.record --image_dir=/home/gustavo/Documentos/LKE_framework/data/classification/sets/test

"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import codecs
import os
import io
import pandas as pd
import tensorflow as tf
import sys

from PIL import Image
from Tensorflow.research.object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('image_dir', '', 'Path to images')
#flags.DEFINE_string('labels', '', 'Path to images')

FLAGS = flags.FLAGS

#aqui es necesario reemplazar la etiqueta con la correspondiente para el entrenamiento
def class_text_to_int2(row_label, clname):
    #print("clname" , clname)
    ind = clname.index(row_label)
    return ind
#----------------------------------------------------------------------------------

# Obtener numero de clases en la dir proporcionada
def getClases(_dir):
	cont = 0
	clssname = []
	clssnum  = []
	for _, dirs, _ in os.walk(_dir):
         for d in dirs:
                clssname.append(d)
                clssnum.append(cont)
                cont+=1
	return clssname, clssnum
#-------------------------------------------------------------------

def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path, clname):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int2(row['class'], clname=clname))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    #pasar por args directorio
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    path = os.path.join(os.getcwd(), FLAGS.image_dir)
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples, 'filename')

    #Se abre el archivo 'clasesFile' y se leen las etiquetas grabadas en el
    clasesFile = 'predefined_classes.txt'
    path_file = os.path.join(os.getcwd(), 'labelImg/data', clasesFile)
    labelHist = []

    if os.path.exists(path_file) is True:
        with codecs.open(path_file, 'r', 'utf8') as f:
            for line in f:
                line = line.strip()
                if labelHist is None:
                    labelHist = [line]
                else:
                    labelHist.append(line)

    print("CLASES = {}".format(len(labelHist)))
        
    for group in grouped:
        tf_example = create_tf_example(group, path, labelHist)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))

if __name__ == '__main__':
    tf.app.run()