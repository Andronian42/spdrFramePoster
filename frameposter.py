"""
ANDROW presents: spdrFramePoster (aka Spider-Verse Bot) 2.0
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
import twitter
import ffmpeg
import os
import sys
import math
from fractions import Fraction
import toml
from tinydb import TinyDB, Query
if len(sys.argv[1:])<2:
    raise ValueError('Please make sure you have given a film and a service as arguments. For more information, refer to the readme.')
film = int(sys.argv[1:][0])
soc = lower(sys.argv[1:][1])
if soc not in ('tw'):
    raise ValueError('That service does not exist, or you mistyped it. Please refer to the readme for acceptable names.')
## Initialize database
db = TinyDB('frinfo.json')
## Log into any necessary APIs
from secrets import credentials
## Get film info
filminfo = toml.load("movies.toml")
framerate = float(Fraction(filminfo[str(film)]['framerate']))
## Make sure nopost is set up
nopost = []
for frange in filminfo[str(film)]['filmnopost']:
    nopost.extend(range(frange[0]-1,frange[1]))
## Get frame number
while True:
    rand = random.randint(0,filminfo[str(film)]['filmframes']-1)
    if (rand not in nopost) and db.get(Query().frame == rand) == None:
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
## Use FFMPEG to get and save a specific frame
movie = ffmpeg.input(filminfo[str(film)]['filename'], ss=rand/framerate, vsync=0)
if filminfo[str(film)]['filmhdr'] == True:
    movie = ffmpeg.filter(movie, 'zscale', tin='smpte2084',min='bt2020nc',pin='bt2020',rin='tv',t='smpte2084',m='bt2020nc',p='bt2020',r='tv')
    movie = ffmpeg.filter(movie, 'zscale', t='linear',npl=60)
    movie = ffmpeg.filter(movie, 'format', 'gbrpf32le')
    movie = ffmpeg.filter(movie, 'zscale', t='linear',p='bt709')
    movie = ffmpeg.filter(movie, 'tonemap', 'hable', desat=0)
    movie = ffmpeg.filter(movie, 'zscale', t='bt709',m='bt709',r='tv')
    movie = ffmpeg.filter(movie, 'format', 'yuv420p')
movie = ffmpeg.filter(movie, 'crop', 'in_w-'+str(filminfo[str(film)]['filmcroplr']), 'in_h-'+str(filminfo[str(film)]['filmcroptb']))
movie = ffmpeg.output(movie, 'temp.jpg', qscale=0, vframes=1)
ffmpeg.run(movie)
## Post photo to Twitter
img = api.UploadMediaChunked("temp.jpg")
api.PostMediaMetadata(img, alt_text="[" + filminfo[str(film)]['filmname'] + ", " + time + ", Frame " + str(rand) + "]")
twitpost = api.PostUpdate("", media=img)
## Update DB
db.insert({'id': twitpost._json["id"], 'repid' : 0, 'film' : film, 'frame': rand})
## Once again, make sure a frame does not currently exist in the folder the program is being run in
os.remove('temp.jpg')
