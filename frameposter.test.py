"""
ANDROW presents: spdrFramePoster (aka Spider-Verse Bot) 2.0
Code first touched on July 30th, 2019 [https://twitter.com/Andronian42/status/1156018491150876672]
Code last touched on December 7th, 2021
I am not responsible for any fires, death, spider-related accidents, etc. that this software may cause.
I *will* try to help, though. If you have trouble, check out the github page:
https://github.com/Andronian42/spdrFramePoster
"""
"""
THIS VERSION OF THE PROGRAM IS FOR TEST PURPOSES.
- No Twitter stuff (works without secrets.py)
- No deleting image file afterwards
- No database junk
This version should match the other one in the repository aside from those three things.
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
import math
from fractions import Fraction
import toml
film = int(sys.argv[1:][0])
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
    if rand not in nopost:
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
movie = ffmpeg.output(movie, 'temp.png', vframes=1)
ffmpeg.run(movie)
print("[" + filminfo[str(film)]['filmname'] + ", " + time + ", Frame " + str(rand) + "]")