from moviepy.video.io.VideoFileClip import VideoFileClip
from multiprocessing.dummy import Pool as ThreadPool
from PIL import Image, ImageFont, ImageDraw
from keras.models import load_model
from constants import VIDEO_EXT
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import threading
import argparse
import time
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

def cut_images(start, end):
    for x in range(start, end+1):
        video_f.save_frame(f'tmp/{str(x)}.jpg', t=x*multiplier)

total_frame_count = video_f.duration
image_cut_count = int(total_frame_count/multiplier)

num_threads = 8

for x in range(num_threads):
    th = threading.Thread(target=cut_images, args=(int(image_cut_count*(x/num_threads)), int(image_cut_count*((x+1)/num_threads))))
    th.start()
    th.join()

#for x in range(image_cut_count):
#    video_f.save_frame(f'tmp/{str(x)}.jpg', t=x*multiplier)
#    print(f'\r[INFO] {image_cut_count-x} Images Left to Cut', end='')

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

print('[STATUS] Making predictions on where to cut video')

# Turn image data into numpy array
image_data = np.array(image_data) / 255.0
# Reshape from (65, image_dims) to (65, image_dims, 1) -> add color channel
image_data = image_data.reshape(image_data.shape[0], IMAGE_DIMS[0], IMAGE_DIMS[1], -1)

# First section will always be an AD
cut_times = []

# Load keras model
model = load_model(args['model'])
predictions = model.predict(image_data)

# If its not an AD and it was previously append Current Time, True to 
# cut_times array, if it was not previously and AD and now is append
# Current Time, False to the array
prev_label = 0
count = 0
ad_count = 0

print('[STATUS] Sorting out where to cut video')

current_item = []
for x in range(len(images)):
    label = int(np.argmax(predictions[x]))
    # Cut times shoudl be [(start_time, duration), (start_time, duration)]
    if label == 0:
        ad_count = 0
        if prev_label == 1 or count > 0:
            if count == 2:
                if not len(current_item) > 0:
                    current_item.append((x-2)*multiplier)
            count += 1
    if label == 1:
        if x != len(images)-1 and not int(np.argmax(predictions[x+1])) == 0:
            count = 0
        if not prev_label or ad_count > 0:
            if ad_count == 1:
                if len(current_item) > 0:
                    current_item.append((x-1)*multiplier)
                    cut_times.append(current_item.copy())
                    current_item.clear()
            ad_count += 1 
    prev_label = label

cut_videos = []
def cut_video_part(start_time, end_time, filename, output_filename):
    subprocess.call(['ffmpeg', '-ss', f'{start_time}', '-i', f'{filename}', '-to', f'{end_time}', 
        '-c', 'copy', f'videos/final_videos/{output_filename}{VIDEO_EXT}', '-f', 'ts','-loglevel', 'panic'])
    cut_videos.append(f'{output_filename}{VIDEO_EXT}')


#for x in cut_times:
#    label = 
#    img = Image.open(images[int(x[0]/multiplier)])
#    draw = ImageDraw.Draw(img)
#    font = ImageFont.truetype('/Libary/Fonts/Courier New.ttf', 100)
#    draw.text((0,0), str(label), (255,255,255), font=font)
#    plt.imshow(img)
#    plt.show()

print('[STATUS] Cutting video')

# Cut the video
start_time = 0
end_time = 0
for x in range(len(cut_times)):
    start_time = cut_times[x][0]
    end_time = cut_times[x][1]
    cut_video_part(start_time, int(end_time-start_time), args['video'], str(x)) 
     
print('[STATUS] Combining vut videos')

final_videos = []
pattern = re.compile(f'([0-9]*?){VIDEO_EXT}')
cut_videos = sorted(cut_videos, key=lambda x: int(re.search(pattern, x).group(1)))
cut_videos = [os.path.join(os.getcwd(), 'videos', 'final_videos', x) for x in cut_videos]

input_filename = str(int(time.time())) + '.txt'
with open(input_filename, 'w') as f:
    for vid in cut_videos:
        f.write(f'file \'videos/final_videos/{os.path.basename(vid)}\'\n')

subprocess.call(['ffmpeg', '-f', 'concat', '-i', f'{input_filename}', '-c', 'copy', '-y', '-loglevel', 'panic',
    f'videos/final_videos/{os.path.basename(args["video"])[:-3]}{VIDEO_EXT}'])


for vid in cut_videos:
    os.remove(vid)
for x in images:
    os.remove(x)
os.remove(input_filename)

print('[STATUS] Complete')    

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

