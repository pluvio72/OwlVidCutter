import os

# Video and image constants
VIDEO_EXT = '.mp4'
ASPECT_RATIO = 1080/1920
IMAGE_DIMS = (128, int(128*ASPECT_RATIO))

# Path constants
WORKING_DIR = os.path.abspath(os.path.join(os.getcwd(), '../'))
TMP_PATH = os.path.join(WORKING_DIR, 'tmp')
IMAGE_PATH = os.path.join(WORKING_DIR, 'images')
VIDEO_PATH = os.path.join(WORKING_DIR, 'videos')
VIDEO_CUT_PATH = os.path.join(VIDEO_PATH, 'cuts')
VIDEO_FINAL_PATH = os.path.join(VIDEO_PATH, 'final_videos')

# Learning constants
MAX_IMAGES = 1000
BATCH_SIZE = 32
INIT_LR = 1e-3
EPOCHS = 50
