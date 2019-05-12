import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import cv2

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

from utils import ops as utils_ops

#if tf.__version__ < '1.4.0':
#  raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')

from utils import label_map_util
from utils import visualization_utils as vis_util


flags = tf.app.flags
flags.DEFINE_string('image_dir', '', 'Path del video')
flags.DEFINE_string('graph_exported', '', 'Path del grafico exportado')
flags.DEFINE_string('label_map', '', 'Path label_map')
flags.DEFINE_string('numClass', '', 'Numero de objetos')

FLAGS = flags.FLAGS

def main(_):
	cap = cv2.VideoCapture(FLAGS.image_dir)

	graph_exportado = os.path.join(os.getcwd(), FLAGS.graph_exported)
	print('graph_exportado FLAG = {}'.format(graph_exportado))
	MODEL_NAME = graph_exportado	#'/home/gustavo/Documentos/LKE_framework/projects/mesas/training/mesas_graph_2898'

	# Path to frozen detection graph. This is the actual model that is used for the object detection.
	PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

	# List of the strings that is used to add correct label for each box
	PATH_TO_LABELS = FLAGS.label_map
	NUM_CLASSES = int(FLAGS.numClass)


	# ## Load a (frozen) Tensorflow model into memory.

	# In[6]:

	detection_graph = tf.Graph()
	with detection_graph.as_default():
	  od_graph_def = tf.GraphDef()
	  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
	    serialized_graph = fid.read()
	    od_graph_def.ParseFromString(serialized_graph)
	    tf.import_graph_def(od_graph_def, name='')


	# ## Loading label map
	# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

	# In[7]:

	label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
	categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
	category_index = label_map_util.create_category_index(categories)


	# # Detection

	# For the sake of simplicity we will use only 2 images:
	# image1.jpg
	# image2.jpg
	# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
	path = os.path.join(os.getcwd(), FLAGS.image_dir)
	print('path FLAG = {}'.format(path))

	# Size, in inches, of the output images.
	IMAGE_SIZE = (12, 8)



	with detection_graph.as_default():
		with tf.Session(graph=detection_graph) as sess:
			while True:
				if not cap.grab():
					cap.release()
					cv2.destroyAllWindows()
					break

				else:
					ret, image_np = cap.retrieve()

					# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
					image_np_expanded = np.expand_dims(image_np, axis=0)
					image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
					# Each box represents a part of the image where a particular object was detected.
					boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
					# Each score represent how level of confidence for each of the objects.
					# Score is shown on the result image, together with the class label.
					scores = detection_graph.get_tensor_by_name('detection_scores:0')
					classes = detection_graph.get_tensor_by_name('detection_classes:0')
					num_detections = detection_graph.get_tensor_by_name('num_detections:0')
					# Actual detection.
					(boxes, scores, classes, num_detections) = sess.run(
					 [boxes, scores, classes, num_detections],
					 feed_dict={image_tensor: image_np_expanded})
					# Visualization of the results of a detection.
					vis_util.visualize_boxes_and_labels_on_image_array(
						  image_np,
						  np.squeeze(boxes),
						  np.squeeze(classes).astype(np.int32),
						  np.squeeze(scores),
						  category_index,
						  use_normalized_coordinates=True,
						  line_thickness=8)

					cv2.imshow('object detection', cv2.resize(image_np, (800,600)))

				if cv2.waitKey(0) & 0xFF == 27:
					cv2.destroyAllWindows()
					break


if __name__ == '__main__':
    tf.app.run()