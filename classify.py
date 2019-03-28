from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import pickle
import cv2 
import os

ASPECT_RATIO = 1080/1920
INPUT_SHAPE = (128, int(128*ASPECT_RATIO))

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True)
ap.add_argument("-m", "--model", required=True)
args = vars(ap.parse_args())

#load the image
image = cv2.imread(args["image"], 0)
output = image.copy()

#pre-process image for classification
#[::-1] because otherwise it reshaped with 
#(input_shape[1], input_shape[0]) as new dim
image = cv2.resize(image,INPUT_SHAPE[::-1])
image = image.astype('float') / 255.0
image = img_to_array(image)
#change shape to an array e.g. (72,72,1) to (1,72,72,1)
image = np.expand_dims(image, axis=0)

#load model
model = load_model(args["model"])

#classify the input image
print('[INFO] Classifying image...')
prb = model.predict(image)[0]
idx = np.argmax(prb)
print(idx)

