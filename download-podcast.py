#!/usr/bin/python3

import os
import sys
import requests
import xml.etree.ElementTree as ET

podcastUrl = "https://djgrind.podomatic.com/rss2.xml"

# download file from url, if it's not on the filesystem
def downloadFile(url):
    # trim the URL down to the filename
    # assume the filename is everything after the last slash
    fileName = url.rsplit('/',1)[-1]

    # if the file doesn't exist, then download it
    if (not os.path.isfile(fileName)):
        print ("\tSaving " + fileName)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(fileName, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
    else:
        print ("\tAlready downloaded " + fileName)
# end downloadFile(url)


# download and parse the podcast feed
print("Downloading and parsing podcast feed", end='...')
root = ET.ElementTree(ET.fromstring(requests.get(podcastUrl).text)).getroot()
print("done!")
# find all podcasts in the feed and download, if the file hasn't been previously downloaded
for item in root.findall('channel/item/enclosure'):
    url = item.get('url')
    size = int(item.get('length')) / (1024 * 1024)

    print("{0}\t{1:.2f}MB".format(url, size))
    downloadFile(url)
