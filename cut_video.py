from moviepy.video.io.VideoFileClip import VideoFileClip
import random
import cv2
import sys
import os

VIDEO_FOLDER = "videos/"

print("Format:\n Start Time: \"Hours:Minutes.Seconds\" or 4.50 in seconds, End Time: Same as Start Time, Random Photo Percentage: 0-100")
start_time, end_time, random_percentage = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
random_percentage = int(random_percentage) / 100

video_folder = os.path.join(os.getcwd(), VIDEO_FOLDER)
files = [x for x in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, x))]
video_file = random.choice(files)
video_path = os.path.join(video_folder, video_file)

video_clip = VideoFileClip(video_path)
print(f"Start Time: {start_time} , End Time: {end_time}")
cut_clip = video_clip.subclip(start_time, end_time)
cut_clip.write_videofile(os.path.join(video_folder+'cuts', f'{video_file[:-3]}_{str(start_time).replace(".", "")}_{str(end_time).replace(".","")}.mp4'))

#vidcap = cv2.VideoCapture(os.path.join(VIDEO_FOLDER, video_file))
#current_frame = 0
#while(True):
#	ret,frame = vidcap.read()
#	if ret:
#		if random.random() < 0.05:
#			cv2.imwrite('images/{}'.format(str(current_frame) + ".jpg"), frame)
#		current_frame+=1
#
#vidcap.release()
#cv2.destroyAllWindows()
