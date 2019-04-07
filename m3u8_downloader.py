from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process, Pool
from urllib.parse import urlparse
import subprocess
import requests
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

    def __init__(self, m3u8_playlist_page,video_name):
            self.playlist_page = m3u8_playlist_page
            self.m3u8_url = ''
            self.m3u8_body = ''
            self.video_name = video_name
            self.download_percentage = 0
            parsed_playlist_path = os.path.basename(urlparse(m3u8_playlist_page).path)
            self.basepath = m3u8_playlist_page.split(parsed_playlist_path)[0]
    
    def choose_playlist(self, index):
            req = requests.get(self.playlist_page)
            split_response = req.text.split('\n')
            m3u8_lines = []
            #split the m3u8 of any unecessary tags
            for line in split_response:
                    if self.M3U8_TAG in line:
                            m3u8_lines.append(line.split(self.M3U8_TAG)[1])
            #sort the m3u8 playlists in orser of resolution 
            m3u8_lines = sorted(m3u8_lines, key=lambda x: int(re.search(re.compile(self.RES_REGEX), x).group(1)), reverse=True)
            print(f"[INFO] You have chosen the stream with resolution: {re.search(re.compile(self.RES_REGEX),m3u8_lines[index]).group(0)}")
            print(f"[INFO] The URL is: {re.search(re.compile(self.URI_REGEX),m3u8_lines[index]).group(1)}")
            print(f"[INFO] The Video Title is: {m3u8_lines[index]}")
            #select the m3u8 playlist and extract the url from the line
            self.m3u8_url = self.basepath+re.search(re.compile(self.URI_REGEX), m3u8_lines[index]).group(1)

    def get_m3u8_body(self):
	    url_identifier = os.path.basename(self.m3u8_url).split('.')[0]
	    req = requests.get(self.m3u8_url)
	    regex = url_identifier + '.*?.ts'
	    results = re.findall(re.compile(regex), req.text)
	    results = [self.basepath + x for x in results]
	    self.m3u8_body = results

    def write_playlist_to_file(self):
        with open('links.txt', 'w') as f:
            for link in self.m3u8_body:
                f.write(link+'\n')

    def first_download_url(self, url):
        print("[INFO] Downloading first chunk...")
        req = requests.get(url)
        binfile = open(f'./videos/{self.video_name}.ts', 'wb')
        binfile.write(req.content)
        binfile.close()

    def download_url(self, url):
            print('[INFO] Current Download Percentage: {}'.format((self.download_percentage/len(self.m3u8_body))*100))
            self.download_percentage += 1
            data = urllib.request.urlopen(url).read()
            with open(f'./videos/{self.video_name}.ts', 'ab') as f:
                f.write(data)

    def download(self):
            print("[INFO] Downloading...")
            self.first_download_url(self.m3u8_body[0])

            pool = ThreadPool(10)
            results = pool.map(self.download_url, self.m3u8_body)
            pool.close()
            pool.join()
