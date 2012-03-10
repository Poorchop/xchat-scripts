import urllib
import json
import xchat
import re

__module_name__        = "Get Youtube Video Info"
__module_version__     = "0.2"
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
    params                = urllib.urlencode(params)

    f = urllib.urlopen('http://gdata.youtube.com/feeds/api/videos?%s' % params)
    data = json.load(f)

    info = {}
    info['id']        = id
    info['title']     = data['feed']['entry'][0]['title']['$t']
    info['views']     = data['feed']['entry'][0]['yt$statistics']['viewCount']
    info['favorites'] = data['feed']['entry'][0]['yt$statistics']['favoriteCount']
    info['likes']     = data['feed']['entry'][0]['yt$rating']['numLikes']
    info['dislikes']  = data['feed']['entry'][0]['yt$rating']['numDislikes']

    return info

def show_yt_info(info):
    print \
    ("\0033\002::\003 YouTube\002 %s " + \
    "\0033\002::\003 URL:\002 http://youtu.be/%s " + \
    "\0033\002::\003 Views:\002 %s " + \
    "\0033\002:: [+]\002 %s likes " + \
    "\002\0034[-]\002 %s dislikes " + \
    "\0033\002::\002") % \
          (info['title'], info['id'], group(info['views']), group(info['likes']), group(info['dislikes']))

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
        print "/yt <url> to get video info"
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

