'''
Multi Model Evaluate Tool 
2019 Shinkansan
Just for Keras hdf5 format

CHANGE Params
	mypath
	photo_loads
	label_loads
'''
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import StratifiedKFold
from keras.models import load_model
import numpy as np
import cv2
import os
import tensorflow as tf
from keras.utils import np_utils
from os import listdir
from os.path import isfile, join
import uuid
import os


# Suppress some level of logs
os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '3'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

emotions = {0:'Angry',1:'Disgust', 2:'Fear', 3:'Happy',
                            4:'Sad', 5:'Surprised',6: 'Neutral'}

seed = 7
np.random.seed(seed)
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)


def faceNorm(pics): # This for Normal images, npy files is already normalized
	pics = cv2.cvtColor(pics.reshape(48,48, 3), cv2.COLOR_BGR2GRAY)
	#pics = pics.reshape(-1)
	new_extracted = pics.astype(np.float32)
	new_extracted  /= float(new_extracted.max())
	return new_extracted.reshape(48, 48, 1)

def mPredict(model, pics):
	result_raw = model.predict(faceNorm(pics).reshape(1, 48, 48, 1))
	topFace = (prediction_result.argmax(axis=-1),
				prediction_result.max()*100)
	return topFace



photo_loads = np.load('dataset/test_dataset/ck_test_img920.npy')
label_loads = np.load('dataset/test_dataset/ck_test_label920.npy')
label_loads = np_utils.to_categorical(label_loads)
if __name__ == "__main__":
	mypath = 'models/da09/'
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and 'hdf5' in f]
	model_list = onlyfiles
	scoreslist = []
	print(len(onlyfiles), 'models ready to test')

	for modelN in model_list:
		model = load_model(os.path.join(mypath, modelN))
		norm_pic = []
		for pic in photo_loads:
			norm_pic.append(faceNorm(pic))
		norm_pic = np.array(norm_pic).reshape(920, 48, 48,1)
		label_loads
		try:
			scores = model.evaluate(norm_pic,  label_loads, verbose =1)
		except:
			continue
		print(modelN)
		print("%s: %.3f%%" % (model.metrics_names[1], scores[1]*100))
		print("%s: %.3f" % (model.metrics_names[0], scores[0]))
		scoreslist.append(scores[1]*100)
		sess = K.get_session()
		K.clear_session()
		sess.close()
		del model
		

	reportID = str(uuid.uuid4())[:5]
	TopModel = [(x, _) for _,x in sorted(zip(scoreslist,model_list), reverse=True)]
	reportF = open(f'./report-{reportID}', 'w')
	
	for rank, data in enumerate(TopModel):
		print(f' {rank} : {data}\n')
		reportF.writelines(f' {rank} : {data}\n')
	reportF.close()
	
	print(f'Report id of this session is {reportID}\nReport File is saved\nJob Done.')
	
	
	


	
