# Machine learning app that automatically detects Ads and cuts them out

##### Has a threaded M3U8 playlist streamer which you can pick out which quality stream used. Scripts to generate images from downloaded videos and classify them, and a script which takes a video as a video as input and cuts out all the ads.

### Setup project structure: 
   - Run `pip install -r requirements.txt` in the root folder
   - Run `python scripts/setup_folders.py` to create the project structure

#### Scripts:
   - **Classify:** used to check whether the model is trained correctly for the images being used
     - arguments: + -i (path to image) 
		  + -m (path to model)
   - **Cut video:** used to cut a video into segments
     - arguments: + -s (start time in format minutes:seconds or hours:minutes:seconds) 
		  + -d (duration of clip in same format as start time)
		  + -f (filename path)
		  + -g (whether to cut images from section True or False)
		  + -c (how many times per second to cut images from section in seconds)
		  + -a (whether the images being cut are from ad section or not either True or False)
   - **Download Video:** used to download videos from overwatchleague.com
     - arguments: none
   - **Get images:** used to cut images from a video
     - arguments: + -s (images cut per second in seconds)
		  + -a (whether the images are ads or not True or False)
		  + -c (whether to choose a video from cuts folder)
   - **Prediction images:** used to cut images used for testing model
     - arguments: + -v (path to video file)
		  + -s (how many times per second to cut images from section in seconds)
		  + -a (whether images are ads or not True or False)
   - **Video classify:** used to cut out ad sections from whole video (main file)
     - arguments: + -v (path to video file)
		  + -c (how many sections of the video to sample)
		  + -m (model to use to classify)
		  + -o (offset for section of video sample from beginning)
