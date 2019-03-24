from keras.models import Sequential 
from keras.layers import Dense, Conv2D, Flatten
from sklearn.model_selection import train_test_split
import cv2
import os

ad_directory = os.path.join(os.getcwd(), 'images/ad')
notad_directory = os.path.join(os.getcwd(), 'images/notad')

ad_images = [os.path.join(os.getcwd()+ad_directory, x) for x in os.listdir(ad_directory) if 'DS_Store' not in x]
notad_images = [os.path.join(os.getcwd()+notad_directory, x) for x in os.listdir(notad_directory) if 'DS_Store' not in x]
all_images = ad_images + notad_images

print(ad_images)
ad_labels = [True for x in ad_images]
notad_labels = [False for x in notad_images]
all_labels = ad_labels + notad_labels

all_image_data = [cv2.imread(x) for x in all_images]



#model = Sequential()
#
#model.add(Conv2D(64, kernal_size=3, activation='relu', input_shape=(input_shape)))



