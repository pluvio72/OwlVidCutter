from moviepy.video.io.VideoFileClip import VideoFileClip
import subprocess
import random
import cv2
import sys
import os

VIDEO_FOLDER = "videos/"

print('*' * 32)
print('\n\tArguments: \n\t Start Time (Hours:Minutes:Seconds)\n\t End Time (Same) \n\t Cut Images (Bool) \n\t Image Cut Percentage (float) \n\t Ad Section (Bool)\n')
print('*' * 32)

filename, start_time, end_time = sys.argv[1], sys.argv[2], sys.argv[3]
#start/end time is in the format '14.30' in minutes and subclip takes it in seconds so multiply mins by 60

#if you want to generate images is the section being cut an ad section or not ads
image_extra_path = ''
get_images = False
random_percentage = ''
if len(sys.argv) > 3:
	get_images = True if sys.argv[4] == 'True' else False
	random_percentage = sys.argv[5]
	image_extra_path = 'ad' if sys.argv[6] == 'True' else 'notad'
	#percentage is in 1-100 and random is between 0 and 1 so / 100
	random_percentage = float(random_percentage) / 100
	

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
    print("[INFO] Cutting Images...")
    vidcap = cv2.VideoCapture(new_video_path)
    current_frame = 0
    while(True):
        ret,frame = vidcap.read()
        if ret:
            if random.random() < random_percentage:
                cv2.imwrite('images/{}/{}'.format(image_extra_path, str(current_frame) + ".jpg"), frame)
            current_frame+=1
        else:
            break
	# release video and destroy process	
    vidcap.release()
    cv2.destroyAllWindows()
