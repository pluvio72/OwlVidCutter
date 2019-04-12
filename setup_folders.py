import os

def check_create_path(path):
    if not os.path.exists(path):
        print(f'[STATUS] {path} doesn\'t exists -> creating it')
        os.makedirs(path)
    else:
        print(f'[INFO] {path} already exists')

check_create_path('./videos/final_videos')
check_create_path('./videos/cuts')
check_create_path('./tmp')
check_create_path('./images')
