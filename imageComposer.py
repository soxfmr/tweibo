# -*- coding: UTF-8 -*-
from requests import get
from os import mkdir
from os.path import exists
import re

_save_folder = 'images'

_image_cdn_url = 'http://t1.qpic.cn/mblogpic/%s/2000'

def init():
    global _save_folder

    folder = raw_input('Save image to folder (default to ./IMAGES): ')
    if folder != '':
        _save_folder = folder

    if not exists(_save_folder):
        mkdir(_save_folder)

def compose(data):
    global _image_cdn_url

    resources = extractImgUrl(data)
    if resources == False:
        print 'No images found.\n'
        return False

    for url in resources:
        fn = extractFilename(url)
        download(_image_cdn_url % fn, fn)

def extractFilename(url):
    fnText = re.search('mblogpic/.+?/\d+', url)
    if fnText == None: return False

    fn = fnText.group(0)
    return fn.split('/')[1]

def extractImgUrl(data):
    imgTagText = re.findall('<img\sclass="crs"\sshow="\d+"\scrs=".+?"', data)
    if imgTagText == None: return False

    resources = []
    for imgTag in imgTagText:
        urlText = re.search('crs=".+?"', imgTag)
        if urlText == None: continue

        resources.append(urlText.group(0).replace('crs="', "").replace('"', ""))

    return resources

def download(url, fn):
    global _save_folder

    res = get(url, stream=True)
    if res.status_code != 200: return False
    # Static image
    fn = "%s/%s.jpg" % (_save_folder, fn)

    print 'Crawling image %s to %s...\n' % (url, fn)

    with open(fn, "wb") as handle:
        for buf in res.iter_content(chunk_size=1024):
            if buf: handle.write(buf)
