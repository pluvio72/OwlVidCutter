from moviepy.video.io.VideoFileClip import VideoFileClip
from multiprocessing.dummy import Pool as ThreadPool
from keras.models import load_model
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import subprocess
import argparse
import cv2
import os
import re

"""
    Main File which takes a video as input and cuts the AD sections out
"""

ASPECT_RATIO = 1080/1920
IMAGE_DIMS = (128,int(128*ASPECT_RATIO))

ap=argparse.ArgumentParser()
ap.add_argument('-v', '--video', required=True)
ap.add_argument('-c', '--count', type=int, required=True)
ap.add_argument('-m', '--model', required=True)
ap.add_argument('-o', '--offset')
args = vars(ap.parse_args())

print(f'[STATUS] Cutting images every {args["count"]} seconds')

# Load video
video_f = VideoFileClip(args['video'])
image_data = []
multiplier = args['count']

total_frame_count = video_f.duration
image_cut_count = int(total_frame_count/multiplier)
for x in range(image_cut_count):
    video_f.save_frame(f'tmp/{str(x)}.jpg', t=x*multiplier)

print(f'[STATUS] Pre-processing Image Data')
pattern = re.compile('([0-9]*?).jpg')
tmp_dir = os.path.join(os.getcwd(), 'tmp')
# Sort the images in order of their number
images = [x for x in os.listdir('tmp/') if 'DS_Store' not in x]
images = sorted(images, key=lambda x: int(re.search(pattern, x).group(1)))
images = [os.path.join(tmp_dir, x) for x in images]

print(f'[INFO] {len(images)} Images')
# Preprocess image data
for image in images:
    img = cv2.imread(image, 0)
    img = cv2.resize(img,IMAGE_DIMS)
    d = np.array(img)
    image_data.append(d)


# Turn image data into numpy array
image_data = np.array(image_data) / 255.0
# Reshape from (65, image_dims) to (65, image_dims, 1) -> add color channel
image_data = image_data.reshape(image_data.shape[0], IMAGE_DIMS[0], IMAGE_DIMS[1], -1)

# First section will always be an AD
cut_times = [(0, False)]

# Load keras model
model = load_model(args['model'])
predictions = model.predict(image_data)

# If its not an AD and it was previously append Current Time, True to 
# cut_times array, if it was not previously and AD and now is append
# Current Time, False to the array
prev_ad = False
count = 0
ad_count = 0

for x in range(len(images)):
    label = int(np.argmax(predictions[x]))

    if label == 0:
        ad_count = 0
        if prev_ad or (count > 0 and count < 2):
            count += 1
            if count == 2:
                cut_times.append(((x-3)*multiplier, True))
    if label == 1:
        count = 0
        if not prev_ad or ad_count > 0:
            if ad_count == 1:
                cut_times.append(((x-1)*multiplier, False))
            ad_count += 1
    prev_ad = label

print(cut_times)

def cut_video_part(start_time, end_time, filename, output_filename):
    subprocess.call(['ffmpeg', '-ss', f'{start_time}', '-i', f'{filename}', '-to', f'{end_time}', 
        '-c', 'copy', f'videos/final_videos/{output_filename}.mp4'])


for x in cut_times:
    label = x[1]
    img = Image.open(images[int(x[0]/multiplier)])
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('/Libary/Fonts/Courier New.ttf', 100)
    draw.text((0,0), str(label), (255,255,255), font=font)
    plt.imshow(img)
    plt.show()

# Cut the video
start_time = 0
end_time = 0
for x in range(1, len(cut_times)):
    end_time = cut_times[x][0]
    cut_video_part(start_time, int(end_time-start_time), args['video'], str(x)) 
    start_time = cut_times[x][0]

final_videos = []
cut_videos = [x for x in os.listdir(os.path.join(os.getcwd(), 'videos', 'final_videos')) if '.DS_Store' not in x]

for x in range(len(cut_videos)):
    if not cut_times[x][1]:
        final_videos.append(cut_videos[x])

print(final_videos)

removable = set(cut_videos) - set(final_videos)
for remove in removable:
    os.remove(os.path.join(os.getcwd(), 'videos' ,'final_videos', remove))

#print('Removed ad videos')


# Look at images and their label
#for x in range(len(images)):
#    #current_img = image_data[x].reshape(IMAGE_DIMS[0], IMAGE_DIMS[1])
#    label = str(np.argmax(predictions[x]))
#    img = Image.open(images[x])
#    draw = ImageDraw.Draw(img)
#    font =  ImageFont.truetype('/Libary/Fonts/Courier New.ttf', 100)
#    draw.text((0,0), label, (255,255,255), font=font)
#    plt.imshow(img)
#    plt.show()

for x in images:
    os.remove(x)

