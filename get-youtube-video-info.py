import urllib.request, urllib.parse
import json
import xchat
import re
import sys

__module_name__        = "Get Youtube Video Info"
__module_version__     = "0.4"
__module_description__ = "Reads and displays video info from an URL."
__module_author__      = "demi_alucard <alysson87@gmail.com>"

def get_yt_info(id):
    params                = {}
    params['v']           = '2.1'
    params['alt']         = 'json'
    params['safeSearch']  = 'none'
    params['restriction'] = '255.255.255.255'
    params['q']           = '"%s"' % id
    params['fields']      = 'entry[media:group/yt:videoid="%s"]' % id
    params                = urllib.parse.urlencode(params)

    f = urllib.request.urlopen('http://gdata.youtube.com/feeds/api/videos?%s' % params)
    data = json.loads(f.read().decode('utf-8'))
    if 'entry' not in data['feed']:
        return {}
    data = data['feed']['entry'][0]

    info = {}
    info['id']            = id
    if 'title' in data:
        info['title']     = data['title'].get('$t', 'Untitled')
    else:
        info['title']     = 'Untitled'
    if 'yt$statistics' in data:
        info['views']     = data['yt$statistics'].get('viewCount', 0)
        info['favorites'] = data['yt$statistics'].get('favoriteCount', 0)
    else:
        info['views']     = 0
        info['favorites'] = 0
    if 'yt$rating' in data:
        info['likes']     = data['yt$rating'].get('numLikes', 0)
        info['dislikes']  = data['yt$rating'].get('numDislikes', 0)
    else:
        info['likes']     = 0
        info['dislikes']  = 0

    return info

def show_yt_info(info):
    msg = u"\0033\002::\003 YouTube\002 %s " + \
    u"\0033\002::\003 URL:\002 http://youtu.be/%s " + \
    u"\0033\002::\003 Views:\002 %s " + \
    u"\0033\002:: [+]\002 %s likes " + \
    u"\002\0034[-]\002 %s dislikes " + \
    u"\0033\002::\002"

    msg = (msg) % (info['title'], info['id'], group(info['views']), group(info['likes']), group(info['dislikes']))

    xchat.prnt(msg)

def get_id_from_url(text):
    check = re.compile(r"(?:https?\://)?(?:\w+\.)?(?:youtube|youtu)(?:\.\w+){1,2}/")
    normal = re.compile(r"(?:=|%3F)?v(?:=|%3D)([\w\-]+)")
    short = re.compile(r"(?:(?:https?\://)?(?:\w+\.)?(?:youtube|youtu)(?:\.\w+){1,2}/)([\w\-]+)")
    vid = ""

    if check.search(text):
        normal = normal.search(text)
        short = short.search(text)
        if normal != None:
            vid = normal.group(1)
        elif short != None:
            vid = short.group(1)

    return vid

def group(n):
    return (','.join(re.findall(r"\d{1,3}", str(n)[::-1])))[::-1]

def privmsg_cb(word, word_eol, userdata):
    id = get_id_from_url(word_eol[3])
    if len(id) == 0:
        return xchat.EAT_NONE
    info = get_yt_info(id)
    if len(info) == 0:
        return xchat.EAT_NONE
    show_yt_info(info)
    return xchat.EAT_NONE

def ytcmd_cb(word, word_eol, userdata):
    if len(word) < 2:
        xchat.prnt("/yt <url> to get video info")
        return xchat.EAT_NONE
    id = get_id_from_url(word_eol[0])
    if len(id) == 0:
        return xchat.EAT_NONE
    info = get_yt_info(id)
    if len(info) == 0:
        return xchat.EAT_NONE
    show_yt_info(info)
    return xchat.EAT_NONE

xchat.hook_command("yt", ytcmd_cb, help="/yt <url> to get video info")
xchat.hook_server("PRIVMSG", privmsg_cb)

print("\0034", __module_name__, __module_version__, "has been loaded\003")