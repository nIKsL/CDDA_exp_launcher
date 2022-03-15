"""
List of constants
"""



# subj
MAIN_URL = "https://github.com/CleverRaven/Cataclysm-DDA/releases"

# local storage for experimental releases
RELEASE_FOLDER = "./exp_release/"

# distro type e.g. with tiles or no
# DISTRO_TYPE = "cdda-linux-curses-x64-"
DISTRO_TYPE = "cdda-linux-tiles-x64-"

# Game folder - need full path
#GAME_FOLDER = "~/MyDocs/cataclysmdda-0.F/"
GAME_FOLDER = "/home/n/MyDocs/cataclysmdda-0.F/"


# Get current game version
with open(f"{GAME_FOLDER}VERSION.txt", "r") as f:
    CURRENT_VERSION = f.readlines()[1].split()[-1]
