"""
ANDROW presents: spdrFramePoster (aka Spider-Verse Bot) 3.0
Code first touched on July 30th, 2019 [https://twitter.com/Andronian42/status/1156018491150876672]
I am not responsible for any fires, death, spider-related accidents, etc. that this software may cause.
I *will* try to help, though. If you have trouble, check out the github page:
https://github.com/Andronian42/spdrFramePoster
"""

"""
This file is part of spdrFramePoster.

spdrFramePoster is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

spdrFramePoster is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with spdrFramePoster.  If not, see <https://www.gnu.org/licenses/>.
"""
## Import all necessary dependencies
import random
import json
import ffmpeg
import os
import sys
import shutil
import math
from fractions import Fraction
from tomlkit.toml_file import TOMLFile
from tinydb import TinyDB, Query
## Check arguments/options
if len(sys.argv[1:])==0:
    raise SystemExit("frameposter.py - the frame posting script part of spdrFramePoster, made by Androw with <3\n\nUsage: python frameposter.py <video(s)> <service>\n\n <video(s)> - One or more videos to post. Must first be configured in the movies.toml config file. Every video has a number in movies.toml; that number is what this argument takes. To post randomly between multiple videos, list multiple numbers separated by commas (without spaces).\n <service> - Service being posted to. See readme for a list of services.\n")
else:
    arguments = []
    options = {}
    del sys.argv[:1]
    while len(sys.argv)>0:
        if not sys.argv[0].startswith("-"):
            arguments.append(sys.argv.pop(0))
        elif sys.argv[0].startswith("--"):
            options[sys.argv.pop(0)[2:]] = True
        else:
            if sys.argv[0][1:] in ['?','v']:
                options[sys.argv.pop(0)[1:]] = True
            else:
                options[sys.argv.pop(0)[1:]] = sys.argv.pop(1)
    if ('help' in options and options['help'] == True) or ('?' in options and options['?'] == True):
        raise SystemExit("\nUsage: python frameposter.py <video(s)> <service>\n\n <video(s)>    One or more videos to post. Must first be configured in the movies.toml config file. Every video has a number in movies.toml; that number is what this argument takes. To post randomly between multiple videos, list multiple numbers separated by commas (without spaces).\n <service>     Service being posted to. See readme for a list of services.\n\nOptions:\n --help   -?         List arguments and options\n -f <frame number>   Specify exact frame number\n -w <weights>        Comma separated list of weights, if you're picking from multiple videos and want to weight the randomization (e.g. weight of 80,20 means 80% chance of first option and 20% chance of second option)\n")
    elif len(arguments)<2:
        raise ValueError('Needs at least two arguments')
    elif len(arguments)>2:
        raise ValueError('Only accepts two arguments')
films = arguments[0].split(',')
if 'w' in options:
    weight = options['w'].split(',')
    for value in range(len(weight)):
        weight[value] = float(weight[value])
    if len(weight) == len(films):
        film = random.choices(films, weight)[0]
    else:
        raise ValueError('Must provide the same number of weights as videos')
else:
    film = random.choice(films)
soc = arguments[1].lower().split(',')
## Initialize database
db = TinyDB('frinfo.json')
## Get film info
filminfo = TOMLFile('videos.toml').read()
if isinstance(filminfo[str(film)]['framerate'], str):
    framerate = float(Fraction(filminfo[str(film)]['framerate']))
else:
    framerate = float(filminfo[str(film)]['framerate'])
## Make sure nopost is set up
nopost = []
for frange in filminfo[str(film)]['nopost']:
    nopost.extend(range(frange[0]-1,frange[1]))
## Get frame number
if 'f' in options:
    rand = int(options['f'])
else:
    while True:
        rand = random.randint(0,filminfo[str(film)]['frames']-1)
        brk = True
        for plat in soc:
            if (rand in nopost) or db.get((Query().frame == rand) & (Query().film == film) & (Query().platform == plat)) != None:
                brk = False
        if brk == True:
            break
## Calculate frame time
hours = math.floor((rand/framerate)/3600)
minutes = math.floor(((rand/framerate)-(hours*3600))/60)
seconds = math.floor((rand/framerate)-(hours*3600)-(minutes*60))
time = str(hours) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
## Make sure a frame does not currently exist in the folder the program is being run in
try:
    os.remove('temp.jpg')
except:
    pass
try:
    os.remove('temp.png')
except:
    pass
## Use FFMPEG to get and save a specific frame
def render(file, rss, rhdr, crop, out):
    movie = ffmpeg.input(file, ss=rss, vsync=0)
    if rhdr == True:
        movie = ffmpeg.filter(movie, 'zscale', tin='smpte2084',min='bt2020nc',pin='bt2020',rin='tv',t='smpte2084',m='bt2020nc',p='bt2020',r='tv')
        movie = ffmpeg.filter(movie, 'zscale', t='linear',npl=60)
        movie = ffmpeg.filter(movie, 'format', 'gbrpf32le')
        movie = ffmpeg.filter(movie, 'zscale', t='linear',p='bt709')
        movie = ffmpeg.filter(movie, 'tonemap', 'hable', desat=0)
        movie = ffmpeg.filter(movie, 'zscale', t='bt709',m='bt709',r='tv')
        movie = ffmpeg.filter(movie, 'format', 'yuv420p')
    movie = ffmpeg.filter(movie, 'crop', 'in_w-'+crop[0], 'in_h-'+crop[1])
    if out == 'jpg':
        movie = ffmpeg.output(movie, 'temp.jpg', qscale=0, vframes=1)
    elif out == 'png':
        movie = ffmpeg.output(movie, 'temp.png', pred='mixed', vframes=1)
    ffmpeg.run(movie)
if 'tw' in soc or 'co' in soc:
    render(filminfo[str(film)]['filename'], rand/framerate, filminfo[str(film)]['hdr'], [str(filminfo[str(film)]['croplr']),str(filminfo[str(film)]['croptb'])], 'jpg')
if 'tu' in soc or 'ma' in soc or 'file' in soc:
    render(filminfo[str(film)]['filename'], rand/framerate, filminfo[str(film)]['hdr'], [str(filminfo[str(film)]['croplr']),str(filminfo[str(film)]['croptb'])], 'png')
## Post/Save Frame
if soc != ['file']:
    from secrets import credentials
for serv in soc:
    if serv == 'tw': ## Twitter
        tc = credentials['twitter']
        import tweepy
        t1 = tweepy.API(tweepy.OAuth1UserHandler(tc['consumer_key'], tc['consumer_secret'],tc['access_token_key'],tc['access_token_secret']))
        t2 = tweepy.Client(consumer_key=tc['consumer_key'], consumer_secret=tc['consumer_secret'], access_token=tc['access_token_key'], access_token_secret=tc['access_token_secret'])
        img = t1.simple_upload('temp.jpg')
        t1.create_media_metadata(img.media_id, alt_text="[" + filminfo[str(film)]['videoname'] + ", " + time + ", Frame " + str(rand) + "]")
        post = t2.create_tweet(media_ids=[img.media_id])
        postid = post.data['id']
    elif serv == 'tu': ## Tumblr
        tc = credentials['tumblr']
        import pytumblr
        tclient = pytumblr.TumblrRestClient(tc['consumer_key'], tc['consumer_secret'],tc['access_token_key'],tc['access_token_secret'])
        post = tclient.create_photo('spidrvrseframes', state="published", tags=filminfo[str(film)]['tags'], data='temp.png', caption=filminfo[str(film)]['videoname'] + ", " + time + ", Frame " + str(rand))
        postid = post['id']
    elif serv == 'ma': ## Mastodon
        mc = credentials['mastodon']
        from mastodon import Mastodon
        mclient = Mastodon(access_token = mc['access_token'], api_base_url = mc['url'])
        img = mclient.media_post('temp.png', description="[" + filminfo[str(film)]['videoname'] + ", " + time + ", Frame " + str(rand) + "]")
        post = mclient.status_post('', media_ids=img, visibility='public')
        postid = post['id']
    elif serv == 'co': ## Cohost
        cc = credentials['cohost']
        from cohost.models.user import User as CUser
        from cohost.models.block import AttachmentBlock
        ccuser = CUser.login(cc['username'], cc['password'])
        cclient = ccuser.getProject(cc['handle'])
        img = [AttachmentBlock('temp.jpg', alt_text="[" + filminfo[str(film)]['videoname'] + ", " + time + ", Frame " + str(rand) + "]")]
        post = cclient.post('', img, tags=filminfo[str(film)]['tags'])
        postid = post.postId
    elif serv == 'file': ## Straight to file
        shutil.copyfile('temp.png', str(film)+'-'+str(rand) + '.png')
        print("Generated: {0}\n[{1}]".format(str(film)+'-'+str(rand)+'.png',filminfo[str(film)]['videoname'] + ", " + time + ", Frame " + str(rand)))
        postid = None
    else:
        raise ValueError(f'The listed service "{serv}" is invalid. Options are as follows: tw,tu,ma,co,file')
    if not (postid == None or ('nodb' in options and options['nodb'] == True)):
        db.insert({'id': postid, 'film' : film, 'frame': rand, 'platform':soc})
if ('nodb' in options and options['nodb'] == True) and soc != ['file']:
    print("Database has not been modified")
## Once again, make sure a frame does not currently exist in the folder the program is being run in
try:
    os.remove('temp.jpg')
except:
    pass
try:
    os.remove('temp.png')
except:
    pass
## End script