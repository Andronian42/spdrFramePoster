# spdrFramePoster
A not-so-dead-simple Python script for posting random video frames to social media services. Originally developed for [@SpidrVrseFrames](twitter.com/spidrVrseFrames).
## Features:
 - Uses FFMPEG, supports what FFMPEG supports
 - HDR tonemapping
 - Fast and accurate extraction
 - Support for multiple videos and services with command arguments
 - Database to prevent repeat postings
 - Support for Twitter, Tumblr, Mastodon, and Bluesky/ATP
 - Tag support on Tumblr
 - Alt text support on Twitter, Mastodon, and Bluesky/ATP
 - Video auto-configuration script
## WARNING:
This script comes with no warranty, and no promise of quality. This project is poorly coded, and it'll likely stay that way.

This is my first public repository, and also isn't necessarily a normal script release. I apologize if I'm not doing any of this right.

I am not responsible for DMCA takedowns, account suspensions, accidental file deletions, spider-related accidents, etc. caused by this script or its usage.

This script may be used however you want (GPL and all that jazz) but, though it's not a requirement, I would appreciate being informed of other accounts that use this script. Because that would be cool.
## Usage
### Syntax
> python frameposter.py \<film number(s)\> \<service(s)\>
 
`<video(s)>` - One or more videos to post. Must first be configured in the `movies.toml` config file. Every video has a number in `movies.toml`; that number is what this argument takes. To post randomly between multiple videos, list multiple numbers separated by commas (without spaces). 

`<service>` - One or more services to post to, separated by commas (without spaces). Should be one or more of the following:
- Twitter - `tw`
- Tumblr - `tu`
- Mastodon - `ma`
- Bluesky/ATP - `bs`
- File (generate the frame in the script folder) - `file`
#### Options and Flags
- `-f <frame number>` - Specify an exact frame to extract
- `-w <weights>` - Comma-separated list of weights for weighted randomization between multiple input videos. Must input the same number of weights as videos. (e.g. weight of 80,20 means 80% chance of first option and 20% chance of second option, weight of 4,1 would be the exact same)
- `--nodb` - Refrain from writing to the local database when posting
### Dependencies
- Python 3\.* with pip (newest version recommended, tested 3.9-3.12)
- FFMPEG built with libzimg (for tonemapping; if your source videos aren't HDR, libzimg shouldn't be a requirement)
- API access for any site you want to post to
#### video.toml config
- mediainfo ([https://mediaarea.net/en/MediaInfo](https://mediaarea.net/en/MediaInfo))
### Setup
1. Clone the repository to any working directory (don't be that weirdo who runs their scripts from their downloads folder)
2. Install remaining dependencies by running `pip install -r requirements.txt` in said working directory
3. Add video files to repository folder
4. Run `videos.setup.py` and follow the instructions to add a video configuration, or rename `secrets.example.py` to `secrets.py` and populate it with all relevant metadata.
5. Rename `secrets.example.py` to `secrets.py` and populate it with all relevant API credentials (platform-specific instructions below). You can safely ignore credentials for any services you won't be using.
6. Run the main frameposter.py script manually or with your favorite scheduling application, e.g. cron, using the syntax below
### APIs
#### Twitter
Twitter's API situation is currently unstable due to new leadership. These instructions are accurate as of when I'm writing them, but there's a fair chance you'll be on your own for this one.
1. Log into dev.twitter.com
2. Create a project and app [here](https://developer.twitter.com/en/portal/projects-and-apps)
3. Go to "Keys and Tokens" under your app
4. Insert the `API Key and Secret` and the `Access Token and Secret` into secrets.py. Make sure the access token has at least read and write permissions.
#### Tumblr
1. Log into Tumblr
2. Register an application [here](https://www.tumblr.com/oauth/apps)
3. Copy the `OAuth Consumer Key` and `Secret Key` into secrets.py
4. Log into [here](https://api.tumblr.com/console/calls/user/info)
5. Copy the `token` and `token_secret` into secrets.py
#### Mastodon
1. Log into the Mastodon of your choice. For bots, I would highly recommend [BotsIn.Space](https://botsin.space)
2. Enter the main URL for your instance into secrets.py
3. Go to your account settings, then click "Developer" on the settings sidebar.
4. Register an application with `write:media` and `write:statuses` scopes
5. Copy `Your access token` into secrets.py
#### Bluesky/ATP
1. Grab the `url` of the instance your profile is on (e.g. if you're `spidrvrseframes.bsky.social`, you'd want `https://bsky.social`)
2. Enter your profile's `username` and `password` into secrets.py (I'd recommend [generating an app password](https://bsky.app/settings/app-passwords) for this step)
### Result
If everything works out, you'll get a bunch of output from FFMPEG (that I'll figure out how to remove in the future) and a frame will soon be posted on the account of your choice. 
### Troubleshooting
I haven't implemented a lot of error handling yet, and I'm not sure how well this'll work on other machines. If you get an error and don't know what it means, double check the following:
 - secrets.py
 - movies.toml
 - Dependencies (make sure you have all of them properly installed for Python 3)
 - Python version (make sure you're on Python 3)
 - Account (make sure everything's alright there)
 
If none of these work or you're just generally pissed about the sorry state of this program, submit a GitHub issue and I'll happily try to get your problem resolved.
