"""
ANDROW presents: spdrFramePoster (aka Spider-Verse Bot)
Code first touched on July 30th, 2019 [https://twitter.com/Andronian42/status/1156018491150876672]
I am not responsible for any fires, death, spider-related accidents, etc. that this software may cause.
I *will* try to help, though. If you have trouble, check out the github page:
https://github.com/Andronian42/spdrFramePoster
"""

version = ["Andronian42", "spdrFramePoster", "videos.setup.py", "v4.0", "November 24th 2023"]

"""
This script is part of spdrFramePoster.

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


import sys
import os
try:
    from tomlkit.toml_file import TOMLFile
    from tomlkit import table
    from pymediainfo import MediaInfo
except:
    print("One or more prerequisites for this script and/or spdrFramePoster have not been found. Attempting to install now...\n")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    print("\nPrerequisites have finished installing, seemingly! Unless there's an error above, in which case you should probably take care of that. If the above was successful, please rerun this script")
    sys.exit()

def preamble():
    print("\n < videos.setup.py - 2023, Made by Androw with <3 >")
    print("This script is a companion to spdrFramePoster. spdrFramePoster requires information about the videos it posts from in order to work quickly and efficiently. Some of the information needed is hard to obtain without using esoteric commands and the like, so this companion script attempts to make it easier.")
    print("Issues? Questions? Report them here: https://github.com/Andronian42/spdrFramePoster/issues\n")
    
def tomlread():
    vtoml = TOMLFile('videos.toml').read()
    print(" {-videos.toml has " + str(len(vtoml)) + " entries-}")
    print(" |-Enter 'n' to add a new entry-|-Enter 'x' to exit this script-|")
    while True:
        selection = input("Entry: ").strip().lower()
        if selection == 'n':
            tomlappend(len(vtoml))
        if selection == 'x':
            sys.exit()
        else:
            print("ERROR: Not a valid option. Please try again.")

def tomlappend(vnum):
    vtoml = TOMLFile('videos.toml').read()
    vdata = []
    # Filename
    print("\nPlease start by providing the filename of the video you'd like to add. It muat be in the same folder this is being run in.")
    while True:
        filename = input("Filename: ")
        if os.path.dirname(filename) == '':
            vdata.append(filename)
            break
        else:
            print("File is not in this folder! Please move the file to this folder and give the filename again.")
    # Automated values
    print("If the filename you gave wasn't a real file in this folder, the next steps may fail. Just move the file into the folder and run the script again.\nThe script will now make a few calculations on the video file. This may take a moment...")
    try:
        video = MediaInfo.parse(vdata[0])
    except:
        print("\nOuch, Something went wrong. Either the file you gave wasn't a real file in this folder, MediaInfo isn't installed to your system (https://mediaarea.net/en/MediaInfo), or something has gone horrificly wrong and I'd recommend reporting it as an error. If, for whatever reason, you'd rather not use mediainfo, you can always manually enter the neccesary info into the videos.toml configuration file.")
        sys.exit()
    for track in video.tracks:
        if track.track_type == "Video":
            vdata.append(int(track.frame_count)) # Frames
            if int(float(track.frame_rate)) == track.frame_rate: # Framerate
                vdata.append(int(track.frame_rate))
            else:
                vdata.append(track.framerate_num + "/" + track.framerate_den)
            print("Frame count and framerate acquired!")
            # HDR
            hdrguess = False
            if track.color_primaries == "BT.2020":
                hdrguess = True
            print("\nBased on the metadata in the video, I believe it {0} in HDR. Does this sound correct?\n(For reference, if you ripped this video from a Blu-Ray/DVD or from an internet video it is most likely NOT in HDR, but if you ripped this directly from a 4K UHD it probably is in HDR.)".format(["IS NOT", "IS"][hdrguess]))
            while True:
                yn = input("y/n: ").strip()
                if yn.lower() == 'y':
                    break
                elif yn.lower() == 'n':
                    hdrguess = not hdrguess
                    break
                else:
                    print("Invalid response. Please enter 'y' for yes or 'n' for no.")
            print('HDR will be set to {0}. If this turns out to be incorrect, you can always manually edit the videos.toml file to correct it.'.format(hdrguess))
            vdata.append(hdrguess)
            break
    # Tags
    print('\nWhen posting to sites such as Cohost and Tumblr, tags can be added for search term visibility. To set them, just type them here one by one. When finished, press "Enter" without entering anything. Since tags are optional, you can skip this by pressing "Enter" immediately.')
    while True:
        tags = []
        while True:
            tag = input("Tag {0}: ".format(len(tags)+1)).strip()
            if tag == '':
                break
            else:
                tags.append(tag)
        if len(tags) == 0:
            print("No tags have been entered.")
        else:
            print("{0} tags have been entered. They are as follows: ".format(len(tags)) + str(tags))
        print("Is this acceptable? Responding with 'n' will prompt you to reenter your tag selection")
        br = False
        while True:
            yn = input("y/n: ").strip()
            if yn.lower() == 'y':
                vdata.append(tags)
                br = True
                break
            elif yn.lower() == 'n':
                break
            else:
                print("Invalid response. Please enter 'y' for yes or 'n' for no.")
        if br == True:
            break
    # Name
    print("\nIf you'd like to implement automatic cropping and specify sections of the video file not to post from, you'll have to edit the videos.toml configuration file directly.\nFinally, enter the name to use for the video file.")
    vdata.append(input('Name: '))
    print("\nThat should do it. Writing to configuration file...")
    # WRITE
    newtab = table()
    newtab.add('filename', vdata[0])
    newtab.add('videoname', vdata[5])
    newtab.add('frames', vdata[1])
    newtab.add('framerate', vdata[2])
    newtab.add('hdr', vdata[3])
    newtab.add('croptb', 0)
    newtab.add('croplr', 0)
    newtab.add('nopost', [])
    newtab.add('tags', vdata[4])
    vtoml.add(str(vnum), newtab)
    TOMLFile('videos.toml').write(vtoml)
    print("Configuration has been written as video number {0}. This number is what you'll throw into frameposter.py to pick that video, e.g. \"python frameposter.py {0} tw\".\n".format(vnum))
    tomlread()
        
def main():
    preamble()
    try:
        open('videos.toml','r')
    except:
        print("videos.toml does not exist. Either this is the first time this script has been run, or the file has been deleted. Either way, we'll go ahead and make an entry.")
        open('videos.toml', 'x')
        tomlappend(0)
    else:
        tomlread()
    
if __name__ == "__main__": main()