import argparse
import random
import cv2
import os

VIDEO_FOLDER = "videos/"
PREDICTION_FOLDER = "images/pred"

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True)
ap.add_argument("-r", "--random_percentage", required=True)
ap.add_argument("-a", "--ad", required=True)
args = vars(ap.parse_args())

extra_name = "ad_" if args["ad"] == "True" else "notad_"

vidcap = cv2.VideoCapture(args["video"])
current_frame = 0
while(True):
    ret,frame = vidcap.read()
    if ret:
        if random.random() < (float(args["random_percentage"])/1000):
            cv2.imwrite(f"{PREDICTION_FOLDER}/{extra_name}{current_frame}.jpg", frame)
        current_frame += 1
    else: 
        break
vidcap.release()
cv2.destroyAllWindows()


