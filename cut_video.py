from moviepy.video.io.VideoFileClip import VideoFileClip
import subprocess
import argparse
import random
import cv2
import sys
import os

VIDEO_FOLDER = "videos/"

ap = argparse.ArgumentParser()
ap.add_argument('-s', '--start_time', required=True)
ap.add_argument('-d', '--duration', required=True)
ap.add_argument('-f', '--filename', required=True)
ap.add_argument('-g', '--get_images', type=bool)
ap.add_argument('-c', '--count', type=float)
ap.add_argument('-a', '--ad')
args = vars(ap.parse_args())

print('*' * 32)
print('\n\tArguments: \n\t Start Time (Hours:Minutes:Seconds)\n\t End Time (Same) \n\t Cut Images (Bool) \n\t Image Cut Percentage (float) \n\t Ad Section (Bool)\n')
print('*' * 32)

filename, start_time, end_time = args['filename'], args['start_time'], args['duration'] 
#start/end time is in the format '14.30' in minutes and subclip takes it in seconds so multiply mins by 60

#if you want to generate images is the section being cut an ad section or not ads
image_extra_path = ''
get_images = False
every_second = 0
if len(args) > 3:
    get_images = args['get_images']
    every_second = args['count']
    image_extra_path = 'ad' if args['ad'].strip() == 'True' else 'notad'
	

video_folder = os.path.join(os.getcwd(), VIDEO_FOLDER)
video_path = os.path.join(video_folder, os.path.basename(filename))

print(f"* Start Time: {start_time} , End Time: {end_time} *\n")
video_name = f'{os.path.basename(filename)[:-3].replace(" ", "")}_{str(start_time).replace(":", "-")}_{str(end_time).replace(":","-")}_{image_extra_path}' 
new_video_path = os.path.join(video_folder+'cuts', video_name + '.mp4')

#video_clip = VideoFileClip(video_path)
#new_clip = video_clip.subclip(start_time, end_time)
#new_clip.write_videofile(new_video_path, audio_codec='aac')

subprocess.call(['ffmpeg', '-ss', f'{start_time}','-i',  f'{filename}','-to',f'{end_time}',
    '-c','copy', f'videos/cuts/{video_name}.mp4'])

if get_images:
    video_f = VideoFileClip(new_video_path) 
    total_frame_count = video_f.duration
    # Calculate how many images i need to cut (total seconds/images to cut per seconds)
    image_cut_count = int(total_frame_count/every_second)
    print(f'[STATUS] Cutting {image_cut_count} Images')
    for image in range(image_cut_count):
        print(f'\r [STATUS] {image_cut_count-image} Images Left', end='')
        video_f.save_frame(f'images/{image_extra_path}/{os.path.basename(filename.strip())[0:3]}{random.randrange(1,1000000)}.jpg', t=image*every_second)

   # print("[INFO] Cutting Images...")
   # vidcap = cv2.VideoCapture(new_video_path)
   # current_frame = 0
   # while(True):
   #     ret,frame = vidcap.read()
   #     if ret:
   #         if random.random() < random_percentage:
   #             cv2.imwrite('images/{}/{}'.format(image_extra_path, str(current_frame) + ".jpg"), frame)
   #         current_frame+=1
   #     else:
   #         break
   #     # release video and destroy process	
   # vidcap.release()
   # cv2.destroyAllWindows()
