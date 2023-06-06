# spdrFramePoster
A not-so-dead-simple Python script for posting random video frames to social media services. Originally developed for [@SpidrVrseFrames](twitter.com/spidrVrseFrames).
## Features:
 - Just enough customization!
 - Support for whatever ffmpeg supports!
 - HDR tonemapping support for some reason!
 - Faster extraction than before!
 - Selecting between multiple videos!
 - Database to keep from posting repeat frames!
 - Frame information in alt/descriptive text format for some services.
 - [NEW] Support for Twitter, Tumblr, Mastodon, and Cohost
## WARNING:
This script comes with no warranty, and no promise of quality. This project is poorly coded, and it'll likely stay that way.

This is my first public repository, and also isn't necessarily a normal script release. I apologize if I'm not doing any of this right.

I am not responsible for DMCA takedowns, account suspensions, accidental file deletions, spider-related accidents, etc. caused by this script or its usage.

This script may be used however you want (GPL and all that jazz) but, though it's not a requirement, I would like to be informed of other accounts that use this script. Because that would be cool.
## Usage
### Dependencies
- Python 3\.* with pip
- FFMPEG built with libzimg (for tonemapping; if your source videos aren't HDR, libzimg shouldn't be a requirement)
- API access for any site you want to post to
### Setup
1. Clone the repository to any working directory (don't be that weirdo who runs their scripts from their downloads folder)
2. Install remaining dependencies by running `pip install -r requirements.txt` in said working directory
3. Add video files to repository folder
4. Rename `movies.example.toml` to `movies.toml` and add all necessary information regarding video files (read the documentation in that file for more information)
5. Rename `secrets.example.py` to `secrets.py` and populate it with all relevant API credentials (platform-specific instructions below). You can safely ignore credentials for any services you won't be using.
5. Run the main frameposter.py script manually or with your favorite scheduling application, e.g. cron, using the syntax below
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
#### Cohost
1. Enter your Cohost `username` (email) and `password` into secrets.py
2. Enter the handle of the page you want to post to as `handle` in secrets.py
### Syntax
> python frameposter.py \<film number\> \<service\>
 
`\<film number\>` should be the number corresponding to one of the films you added to movies.toml (whatever number you put in the brackets)

`\<service\>` should be one of the following based on the service you are posting to:
- Twitter - `tw`
- Tumblr - `tu`
- Mastodon - `ma`
- Cohost - `co`
- File (keep the frame in the script folder) - `file`
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
