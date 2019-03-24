from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import random
import cv2
import sys
import os

VIDEO_FOLDER = "videos/"

print('*' * 32)
print('\n\tArguments: \n\t Start Time (Seconds)\n\t End Time (Seconds) \n\t Cut Images (Bool) \n\t Image Cut Percentage (float) \n\t Ad Section (Bool)\n')
print('*' * 32)

start_time, end_time = sys.argv[1], sys.argv[2]
#start/end time is in the format '14.30' in minutes and subclip takes it in seconds so multiply mins by 60
start_time = int(start_time.split('.')[0]) * 60 + int(start_time.split('.')[1])
end_time = int(end_time.split('.')[0]) * 60 + int(end_time.split('.')[1])

#if you want to generate images is the section being cut an ad section or not ads
image_extra_path = ''
get_images = False
random_percentage = ''
if len(sys.argv) > 3:
	get_images = bool(sys.argv[3])
	random_percentage = sys.argv[4]
	image_extra_path = 'ad' if sys.argv[5] else 'notad'
	#percentage is in 1-100 and random is between 0 and 1 so / 100
	random_percentage = int(random_percentage) / 100
	

video_folder = os.path.join(os.getcwd(), VIDEO_FOLDER)
files = [x for x in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, x))]
video_file = random.choice(files)
video_path = os.path.join(video_folder, video_file)

print(f"* Start Time: {start_time} , End Time: {end_time} *\n")
video_name = f'{video_file[:-3]}_{str(start_time).replace(".", "")}_{str(end_time).replace(".","")}' 
new_video_path = os.path.join(video_folder+'cuts', video_name + '.mp4')

ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=new_video_path)

if get_images:
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
