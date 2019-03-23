from bs4 import BeautifulSoup as soup
from urllib.parse import urlparse
import subprocess
import requests
import argparse
import m3u8_downloader
import json
import os
import re

URL = "https://overwatchleague.com/en-gb/videos?v=XVrFmBDW2pP"

headers = {
    'authority': "overwatchleague.com",
    'cache-control': "max-age=0,no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    'dnt': "1",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'referer': "https://overwatchleague.com/en-gb/schedule",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en-GB,en-US;q=0.9,en;q=0.8",
    'cookie': "locale=en_GB; optimizelyEndUserId=oeu1550218223756r0.2747767037296329; _ga=GA1.2.1054216460.1550218224; _cb_ls=1; showSpoilers=true; _cb=BRYHJDCpz3rqBQ0dRl; __cfduid=ddf4186d24f9805e516c775a2cbdcab541550771447; session=jCRjuNS_4sTtazUOZi_-ug._hY9Xk1qwzVG1poL79tuhXOSBaJLUaEli4oeyknMvz3fxCcUh_oeL5IuI2DG5w4wf3IBYxbRWhC8uoXA_u3UXQ.1551982450964.86400000.jpokG5wnTF9qWh9s9wtjMO195w9Xvjon93dbbsvZKJs; _gid=GA1.2.1606585728.1551982452; _chartbeat2=.1550218225376.1551982462841.0000111001000001.BN9zODC8Ei_YKosLBCfQrCwBTXfPr.1; _cb_svref=https%3A%2F%2Foverwatchleague.com%2Fen-gb%2Fschedule",
    'Postman-Token': "14b6702a-d5f6-45b5-bd28-59fe7d21ac82"
}

req = requests.get(URL, headers=headers)

variable = re.compile('data-mlg-embed="(.*?)"')
url = variable.search(req.text).group(1)
url.replace("https", 'http')

req = requests.get(url)
variable = re.compile('streamUrl":"(.*?)(.m3u8)')
url = variable.search(req.text).group(1) + variable.search(req.text).group(2)
#parse url to get basepath for once i get the m3u8 url as it only has relative path
parsed_url = urlparse(url)
file_path = parsed_url.path
basepath = 'http://' + parsed_url.netloc + file_path.split(os.path.basename(file_path))[0]
#add http: beacuse the url is //m3u8urlhere
general_m3u8 = 'http:' + url
print("General URL: " + general_m3u8)

#variable = re.compile('URI="(.*?)"')
#req = requests.get(general_m3u8)
#search_result = re.search(variable, req.text)
#m3u8_playlist_url = basepath + search_result.group(1)

downloader = m3u8_downloader.M3U8(general_m3u8)
downloader.choose_playlist(0)
downloader.get_m3u8_body()
downloader.download()
