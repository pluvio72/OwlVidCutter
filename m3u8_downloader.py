from urllib.parse import urlparse
from multiprocessing import Pool 
import threading
import urllib
import requests
import os
import re

class M3U8:
	M3U8_TAG = "#EXT-X-I-FRAME-STREAM-INF:"
	RES_REGEX = "([0-9]{0,5})x([0-9]{0,5})"
	URI_REGEX = 'URI="(.*?)"'

	def __init__(self, m3u8_playlist_page):
		self.playlist_page = m3u8_playlist_page
		self.m3u8_url = ''
		self.m3u8_body = ''
		parsed_playlist_path = os.path.basename(urlparse(m3u8_playlist_page).path)
		self.basepath = m3u8_playlist_page.split(parsed_playlist_path)[0]
	
	def choose_playlist(self, index):
		req = requests.get(self.playlist_page)
		split_response = req.text.split('\n')
		m3u8_lines = []
		for line in split_response:
			if self.M3U8_TAG in line:
				m3u8_lines.append(line.split(self.M3U8_TAG)[1])
		m3u8_lines = sorted(m3u8_lines, key=lambda x: int(re.search(re.compile(self.RES_REGEX), x).group(1)), reverse=True)
		print(f"You have chosen the stream with resolution: {re.search(re.compile(self.RES_REGEX),m3u8_lines[index]).group(0)}")
		self.m3u8_url = self.basepath+re.search(re.compile(self.URI_REGEX), m3u8_lines[index]).group(1)

	def get_m3u8_body(self):
		url_identifier = os.path.basename(self.m3u8_url).split('.')[0]
		req = requests.get(self.m3u8_url)
		regex = url_identifier + '.*?.ts'
		results = re.findall(re.compile(regex), req.text)
		results = [self.basepath + x for x in results]
		self.m3u8_body = results

	def download_url(self, url):
		req = urllib.request.urlopen(url)
		resp = req.read()
		binfile = open('video.ts', 'ab')
		binfile.write(resp)
		binfile.close()
#		with req as = open('video.ts', 'ab') as f:
#			for chunk in req.read():
#				if chunk:
#					f.write()

	def download(self):
		print("Downloading...")
		for url in self.m3u8_body:
			self.download_url(url)
