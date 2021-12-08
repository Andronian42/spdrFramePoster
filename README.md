# spdrFramePoster
A not-so-dead-simple Python script for posting random video frames to a Twitter account. Currently used on (and mainly developed for) [@SpidrVrseFrames](twitter.com/spidrVrseFrames).
## Features:
 - Just enough customization!
 - Support for whatever ffmpeg supports!
 - HDR tonemapping support for some reason!
 - Faster extraction than before!
 - Selecting between multiple videos!
 - Database to keep from posting repeat frames!
## WARNING:
This script comes with no warranty, and no promise of quality. This project is poorly coded, and it'll likely stay that way.

This is my first public repository, and also isn't necessarily a normal script release. I apologize if I'm not doing any of this right.

I am not responsible for DMCA takedowns, account suspensions, accidental file deletions, spider-related accidents, etc. caused by this script or its usage.

This script may be used however you want (GPL and all that jazz) but, though it's not a requirement, I would like to be informed of other accounts that use this script. Because that would be cool.
## Usage
(this section is a work in progress, and I wouldn't necessarily recommend listening to its advice until I'm completely sure I'm doing this right)
### Dependencies
- Python 3\.*
- [python-twitter](https://pypi.org/project/python-twitter/)
- [ffmpeg-python](https://pypi.org/project/ffmpeg-python/)
- [tinydb](https://pypi.org/project/tinydb/)
- [toml](https://pypi.org/project/toml/)
- [A Twitter Developer account](https://developer.twitter.com)
### Setup
1. Clone the repository to any working directory (don't be that weirdo who runs their scripts from their downloads folder)
2. Add video files to repository folder
3. Add all necessary information to a movies.toml file regarding video files (read the documentation in that file for more information)
4. Create a secrets.py file with all relevant API credentials
5. Run the main frameposter.py script manually or with your favorite scheduling application, e.g. cron
### Syntax
> python frameposter.py \<film number\>
 
\<film number\> should be the number corresponding to one of the films you added to movies.toml
### Result
If everything works out, you'll get a bunch of output from FFMPEG (that I'll probably remove in the future) and a frame will soon be posted on your Twitter account. 
### Troubleshooting
I haven't implemented a lot of error handling yet, and I'm not sure how well this'll work on other machines. If you get an error and don't know what it means, double check the following:
 - secrets.py
 - movies.toml
 - Dependencies (make sure you have all of them properly installed for Python 3)
 - Python version (make sure you're on Python 3.*
 - Twitter account (make sure everything's alright there)
 
If none of these work or you're just generally pissed about the sorry state of this program, submit a GitHub issue and I'll happily try to get your problem resolved.
