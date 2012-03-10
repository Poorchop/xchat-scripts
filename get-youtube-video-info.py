import urllib
import json
import xchat
import re

__module_name__        = "Get Youtube Video Info"
__module_version__     = "0.1"
__module_description__ = "Reads and displays video info from an URL."

def get_yt_info(id):  
    params = {}
    params['v'] = '2.1'
    params['alt'] = 'json'
    params['safeSearch'] = 'none'
    params['restriction'] = '255.255.255.255'
    params['q'] = '"%s"' % id
    params['fields'] = 'entry[media:group/yt:videoid="%s"]' % id
    params = urllib.urlencode(params)
    
    f = urllib.urlopen('http://gdata.youtube.com/feeds/api/videos?%s' % params)
    data = json.load(f)
    
    info = {}
    info['title'] = data['feed']['entry'][0]['title']['$t']
    info['views'] = data['feed']['entry'][0]['yt$statistics']['viewCount']
    info['favorites'] = data['feed']['entry'][0]['yt$statistics']['favoriteCount']
    info['likes'] = data['feed']['entry'][0]['yt$rating']['numLikes']
    info['dislikes'] = data['feed']['entry'][0]['yt$rating']['numDislikes']
    
    return info

def show_yt_info(info):
    print "3:: YouTube: %s 3:: Views: %s 3:: [+] %s likes 4[-] %s dislikes 3::" % \
          (info['title'], info['views'], info['likes'], info['dislikes'])

def get_id_from_url(text):
    check = re.compile(r"(?:https?\://)?(?:\w+\.)?(?:youtube|youtu)(?:\.\w+){1,2}/")
    normal = re.compile(r"(?:=|%3F)?v(?:=|%3D)([\w\-]+)")
    fallback = re.compile(r"(?:(?:https?\://)?(?:\w+\.)?(?:youtube|youtu)(?:\.\w+){1,2}/)([\w\-]+)")
    vid = ""
    
    if re.search(check, text):
        normal = normal.search(text)
        fallback = fallback.search(text)
        if normal != None:
            vid = normal.group(1)
        elif fallback != None:
            vid = fallback.group(1)
            
    return vid

def privmsg_cb(word, word_eol, userdata):
    id = get_id_from_url(word_eol[3])
    if len(id) == 0:
        return xchat.EAT_NONE
    info = get_yt_info(id)
    if len(info) == 0:
        return xchat.EAT_NONE
    show_yt_info(info)
    return xchat.EAT_NONE

def yt_cb(word, word_eol, userdata):
    if len(word) < 2:
        return xchat.EAT_NONE
    id = get_id_from_url(word_eol[0])
    if len(id) == 0:
        return xchat.EAT_NONE
    info = get_yt_info(id)
    if len(info) == 0:
        return xchat.EAT_NONE
    show_yt_info(info)
    return xchat.EAT_NONE

xchat.hook_command("yt", yt_cb, help="/yt <url> to get video info")
xchat.hook_server("PRIVMSG", privmsg_cb)

