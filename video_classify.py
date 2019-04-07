from moviepy.video.io.VideoFileClip import VideoFileClip
from keras.models import load_model
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import argparse
import cv2
import os

ASPECT_RATIO = 1080/1920
IMAGE_DIMS = (128,int(128*ASPECT_RATIO))

ap=argparse.ArgumentParser()
ap.add_argument('-v', '--video', required=True)
ap.add_argument('-c', '--count', type=int, required=True)
ap.add_argument('-m', '--model', required=True)
args = vars(ap.parse_args())

print(f"Cutting images every {args['count']} seconds...")

#load the video
video_f = VideoFileClip(args["video"])

vidcap = cv2.VideoCapture(args['video'])
current_frame = 0
image_data = []

multiplier = args['count'] * round(vidcap.get(cv2.CAP_PROP_FPS))
print(f"[INFO] Multiplier: {multiplier}")
print(f"[INFO] FPS: {round(vidcap.get(cv2.CAP_PROP_FPS))}")

if os.path.isfile(f"tmp/{str(current_frame)}.jpg") != True:
    print('[INFO] Cutting...')
    while True:
        ret,frame = vidcap.read()
        if ret:
            #if current frame is correct offset e.g. 10s then save data
            if current_frame % multiplier == 0:
                cv2.imwrite('tmp/{}'.format(str(current_frame)+'.jpg'), frame)
            current_frame += 1
    vidcap.release()
    cv2.destroyAllWindows()

print(f"[INFO] Pre-processing Image Data...")
tmp_dir = os.path.join(os.getcwd(), 'tmp')
images = [os.path.join(tmp_dir,x) for x in os.listdir('tmp/') if 'DS_Store' not in x]
print(f"[INFO] {len(images)} Images")
#proprocess image data
for image in images:
    img = cv2.imread(image, 0)
    img = cv2.resize(img,IMAGE_DIMS)
    d = np.array(img)
    image_data.append(d)

    #plt.imshow(img)
    #plt.show()

#turn image data into numpy array
image_data = np.array(image_data) / 255.0
#reshape from (65, image_dims) to (65, image_dims, 1) -> add color channel
image_data = image_data.reshape(image_data.shape[0], IMAGE_DIMS[0], IMAGE_DIMS[1], -1)

cut_times = []

#load kera model
model = load_model(args['model'])

predictions = model.predict(image_data)

for x in range(len(images)):
    #current_img = image_data[x].reshape(IMAGE_DIMS[0], IMAGE_DIMS[1])
    label = str(np.argmax(predictions[x]))
    img = np.array(Image.open(images[x]))
    cv2.putText(img, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
	0.7, (255,255,255))
    cv2.imshow('Output', img)
    cv2.waitKey(0)

for x in images:
    os.remove(x)

#################################################################
#### COMMENT MY CODE SO I CAN UNDERSTAND IT LATER ###############
#################################################################
#### ALSO MAKE FASTER WAY TO DO THE IMAGE CUTTING PART ##########
#################################################################
