from ../scripts/constants import TMP_PATH
from ../scripts/constants import TMP_PATH
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urlparse
import subprocess
import requests
import pyprind
import urllib
import os
import re

class M3U8:
    """  
        M3U8 Downloader using Multiprocessing to speed up download
    """

    M3U8_TAG = "#EXT-X-I-FRAME-STREAM-INF:"
    RES_REGEX = "([0-9]{0,5})x([0-9]{0,5})"
    URI_REGEX = 'URI="(.*?)"'
    NUM_THREAD = 1000

    # Init function initializes all variables
    def __init__(self, m3u8_playlist_page,video_name):
            self.playlist_page = m3u8_playlist_page
            self.m3u8_url = ''
            self.m3u8_body = ''
            self.video_name = video_name
            self.progress_bar = None
            self.download_percentage = 0
            parsed_playlist_path = os.path.basename(urlparse(m3u8_playlist_page).path)
            self.basepath = m3u8_playlist_page.split(parsed_playlist_path)[0]
    
    # Function which chooses the playlist e.g. the quality of the stream and saves the URL into self.m3u8_url
    def choose_playlist(self, index):
            req = requests.get(self.playlist_page)
            split_response = req.text.split('\n')
            m3u8_lines = []
            # Split the m3u8 of any unecessary tags
            for line in split_response:
                    if self.M3U8_TAG in line:
                            m3u8_lines.append(line.split(self.M3U8_TAG)[1])
            # Sort the m3u8 playlists in orser of resolution 
            m3u8_lines = sorted(m3u8_lines, key=lambda x: int(re.search(re.compile(self.RES_REGEX), x).group(1)), reverse=True)
            print(f"[INFO] You have chosen the stream with resolution: {re.search(re.compile(self.RES_REGEX),m3u8_lines[index]).group(0)}")
            print(f"[INFO] The URL is: {re.search(re.compile(self.URI_REGEX),m3u8_lines[index]).group(1)}")
            print(f"[INFO] The Video Title is: {m3u8_lines[index]}")
            # Select the m3u8 playlist and extract the url from the line
            self.m3u8_url = self.basepath+re.search(re.compile(self.URI_REGEX), m3u8_lines[index]).group(1)

    # Function which geoes through the chosen URL and saves the mp4 file URL's in the variable self.m3u8_body
    def get_m3u8_body(self):
            url_identifier = os.path.basename(self.m3u8_url).split('.')[0]
            req = requests.get(self.m3u8_url)
            regex = url_identifier + '.*?.ts'
            results = re.findall(re.compile(regex), req.text)
            # Skip every 2 because there are two urls per video section
            results = [self.basepath + x for x in results][::2]
            self.m3u8_body = results
            self.progress_bar = pyprind.ProgBar(len(results))
            print(f'[INFO] Number of .ts files: {len(results)}')
    
    # Function which downloads a video from given URL and outputs the current % downloaded
    def download_url(self, url, index):
            self.download_percentage += 1
            self.progress_bar.update()
            data = urllib.request.urlopen(url).read()
            with open(f'{TMP_PATH}/{index}.ts', 'wb') as f:
                f.write(data)
    
    # Main Download function which initiates a pool of workers to download the ts stream by multiprocessing
    def download(self):
            print("[STATUS] Downloading...")
            pool = ThreadPool(14)
            # Using starmap as it accepts a tuple for the function arguments
            results = pool.starmap(self.download_url, zip(self.m3u8_body, range(len(self.m3u8_body))))
            pool.close()
            pool.join()
            print('[STATUS] Joining files into single video')
            self.cleanup_writefile()

    # Cleanup tmp folder and turn into one video
    def cleanup_writefile(self):
            pattern = re.compile('([0-9]*?).ts')
            files = [x for x in os.listdir('{TMP_PATH}/') if 'DS_Store' not in x]
            # Sort list of files into the video number
            files = sorted(files, key=lambda x: int(re.search(pattern, x).group(1)))
            files = [os.path.join(TMP_PATH, x) for x in files]
            
            previous_data = b''
            with open(f'{VIDEO_PATH}/{self.video_name.strip()}.ts', 'wb') as video_file:
                for f in files:
                    with open(f, 'rb') as sub_file:
                        data = sub_file.read()
                        if data != previous_data:
                            video_file.write(data)
                        previous_data = data
                    os.remove(f) 
