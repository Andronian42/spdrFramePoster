import sys
try:
    from tomlkit.toml_file import TOMLFile
    from tomlkit import parse
    from ffprobe import FFProbe
except:
    print("One or more prerequisites for this script and/or spdrFramePoster have not been found. Attempting to install now...\n")
    import sys
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
    print(" videos.toml has " + str(len(vtoml)) + " entries.")
    print(" | Enter 'n' to add a new entry | Enter 'x' to exit this script |")
    while True:
        selection = input("Entry: ").lower()
        if selection == 'n':
            tomlappend(len(vtoml))
        if selection == 'x':
            sys.exit()
        else:
            print("ERROR: Not a valid option. Please try again.")

def tomlappend(vnum):
    null

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