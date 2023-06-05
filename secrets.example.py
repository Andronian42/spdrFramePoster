# This is where you'll want to put your social media service API credentials.
# If you're just planning on generating image files, you won't need any of these.
# You only need to fill in the sections for services you're planning on posting to. No need to touch anything else.
# For in-depth information on how to get API credentials to fill in below, please check the section in README.md titled "APIs"
# If you're currently modifying secrets.example.py, you'll want to exit your editor, make a new copy of this file, and rename it to just secrets.py before editing it. 
# DO NOT SHARE THE INFO YOU ENTER HERE WITH ANYBODY
# DO NOT PUSH YOUR EDITED secrets.py TO THE REPOSITORY! secrets.py IS IN gitignore FOR A REASON!
# Example (NOT REAL VALUES. DO NOT USE THESE):
#
# credentials = {
#   'service':{
#     'consumer_key':'hguioAJJGIGSHgUJGASUgjaigjioasg',
#     'consumer_secret':'JGIOJisjgijiasjgiejwaigjkidsajgaiojgwag',
#     'access_token_key':'jiAWuijgiujhuiowahUNWIOAJIOIOGiaosjfioawf',
#     'access_token_secret':'uwahtuiui83ytAEgt8GUIauiGHUISGUIAUJSGsf'
#    },
#   'service2':{
#     'url':'spider.man',
#     'access_token':'hasehesjzasHshesyhysuejfdjdrkodidrkjirkd'
#    }
# }
#
credentials = {
    'twitter':{                                             # 
        'consumer_key':'[insert consumer key here]',
        'consumer_secret':'[insert consumer secret here]',
        'access_token_key':'[insert token key here]',
        'access_token_secret':'[insert token secret here]'
    },
    'tumblr':{
        'consumer_key':'[insert consumer key here]',
        'consumer_secret':'[insert consumer secret here]',
        'access_token_key':'[insert token key here]',
        'access_token_secret':'[insert token secret here]'
    },
    'mastodon':{
        'url':'https://mastodon.example',
        'access_token':'[insert access token here]'
    }
}