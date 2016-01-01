# -*- coding: UTF-8 -*-

result = {'ERR_USER_NOT_FOUND' : u'信息提示_腾讯微博',
            'INFO_BRAODCAST_COUNT' : u'<span class="text_count" >\d+</span><span class="text_atr">广播</span>',
            'INFO_TALKLIST' : u'<ul\sid="talkList"[\s\S]+?</ul>',
            'INFO_TALKLIST_ITEM' : u'<li[\s\S]+?</li>',
            'INFO_BRAODCAST_CONTENT' : u'<div class="msgBox">[\s\S]+</div>',
            'INFO_NEXT_PAGE' : u'<a href="\?mode=0.+?">%d</a>',
            'INFO_NEXT_PAGE_META_DATA' : u'\?.+time=\d+',
            'INFO_RELAY_POST' : u'<div class="replyBox">'}

def adjust_encoding(charset):
    for k,v in result.items():
        result[k] = v.encode(charset)

def match_result(data, keyword):
    if data == None or data == '': return false
    if keyword == None or keyword == '': return false

    return data.find(keyword) != -1
