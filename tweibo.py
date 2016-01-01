# -*- coding: UTF-8 -*-

from requests import get
from settings import adjust_encoding
from settings import match_result
from settings import result
from imageComposer import init
from imageComposer import compose
import re

# Golbal data container to reduce the network request
_data = ''
# Page meta data
_next_page = ''

_max_page = 0

_current_user = ''

_crawl_relay = True

_crawl_limit = False
_crawl_limit_page = 0

def main():
    global _current_user
    global _max_page
    global _crawl_limit
    global _crawl_limit_page

    userId = raw_input('Tencent Weibo Id: ')
    if userId == '': return -1

    crawlAll = raw_input('Do you want to crawl the post of relay? (Y/n)')
    if crawlAll != '' and crawlAll.lower() != 'y':
        _crawl_relay = False

    crawlLimit = raw_input('Crawl post in range of page instead of all post (Let it empty that will crawl all of post): ')
    if crawlLimit != '':
        _crawl_limit = True
        _crawl_limit_page = int(crawlLimit)

    # Initialzied callback function
    init()

    # Server tranfer enconding
    adjust_encoding('utf-8')

    if not hasUser(userId):
        raise ValueError("User %s doesn't exist.\n" % userId)

    broadcastCount = getBroadcastCount()
    if broadcastCount <= 0:
        raise ValueError('No any broadcast for current user yet.\n')

    _current_user = userId
    _max_page = broadcastCount / 15

    # Crawl the post data in range
    if _crawl_limit: _max_page = _crawl_limit_page

    for i in range(1, _max_page):
        crawl(i)    

def hasUser(userId):
    global _data

    _data = get("http://t.qq.com/%s/mine" % userId)
    return not match_result(_data.content, result['ERR_USER_NOT_FOUND'])

def getBroadcastCount():
    global _data

    countText = re.search(result['INFO_BRAODCAST_COUNT'], _data.content)
    if countText == None: return -1

    count = re.search('\d+', countText.group(0)).group(0)
    return int(count)

def crawl(index):
    global _data
    global _current_user
    global _next_page
    global _max_page
    global _crawl_relay

    if index > 1:
        _data = get('http://t.qq.com/%s/mine%s' % (_current_user, _next_page))

        if _data.status_code != 200:
            print 'Server response status: %d\n' % _data.status_code
            return False

    # Calculate the broadcast of this page
    talkList = re.search(result['INFO_TALKLIST'], _data.content)
    if talkList == None:
        print "No broadcast found in page %d\n" % index
        return False

    # Extract the next page meta data
    if index < _max_page:
        #pdb.set_trace()
        nextPageText = re.search(result['INFO_NEXT_PAGE'] % (index + 1), _data.content)
        nextPageMetaText = re.search(result['INFO_NEXT_PAGE_META_DATA'], nextPageText.group(0))
        if nextPageMetaText != None:
            _next_page = nextPageMetaText.group(0)

    broadcastList = re.findall(result['INFO_TALKLIST_ITEM'], talkList.group(0))
    for broadcast in broadcastList:
        info = re.search(result['INFO_BRAODCAST_CONTENT'], broadcast)
        if info == None: continue

        data = info.group(0)
        # skip the relay post if the _crawl_relay option is false
        if not _crawl_relay and data.find(result['INFO_RELAY_POST']) != -1: continue
        # Callback function
        compose(data)

'''
#Take care your broadcast here
def compose(data):
    print data
    return 0
'''

if __name__ == '__main__':
    main()
