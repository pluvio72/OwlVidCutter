import argparse
import random
import os 
import cv2 
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--random_percentage', type=float, required=True)
parser.add_argument('-a', '--ad', type=bool, required=True)
parser.add_argument('-c', '--cuts', required=False)
args = vars(parser.parse_args())

ad_directory = os.path.join(os.getcwd(), 'images/ad')
notad_directory = os.path.join(os.getcwd(), 'images/notad')

random_percentage, ad = args['random_percentage'] / 100, args['ad']
directory = 'ad' if ad else 'notad'

cuts = '/cuts' if args['cuts'] else ''

files = [x for x in os.listdir(os.path.join(os.getcwd(), 'videos'+cuts)) if 'DS_Store' not in x] 
index = 1
for file in files:
    print(f"{index}: {file.strip()}")
    index += 1

file_choice = int(input("Choose File by Index: ")) - 1
filepath = os.path.join(os.path.join(os.getcwd(), 'videos' + cuts), files[file_choice])

print('[INFO] Cutting images with random percentage {}'.format(random_percentage*100))

video_file = cv2.VideoCapture(filepath)
current_frame = 0
while(True):
    ret,frame = video_file.read()
    if ret:
        if random.random() < random_percentage:
            cv2.imwrite(f'images/{directory}/{str(current_frame)}.jpg', frame) 
        current_frame += 1
    else:
        break
