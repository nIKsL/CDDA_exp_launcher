# Linux launcher for CDDA
## (Cataclysm Dark Days Ahead)

**Why did this program come about?**

I like CDDA, but it's annoying all the time to open the page with experimental releases and download updates :)

**This program:**
- shows how many new exerimetal versions have been released
- prints a list of changes from your current release
- downloads tiles version (can be corrected to cursed)
- starts the game (tiles version)
- unpacks (tar -xvzf) the downloaded release into the game folder

![Alt-текст](https://github.com/nIKsL/CDDA_exp_launcher/blob/master/img/scr_menu.png "Орк")


**TODO:**
- save game data
- load game data
- Launcher preferences - (may be genereate options.py on first start.. dunno.. mb delete it.. u can do all settings in options.py)
- check file size - while dl file from assets - need to check it`s size

____
You can use it as simple python scipt (main.py)
or you can find some instructions below
____

clone, make virtual enviroment, activate venv, install requierements, deactivate
```
git clone https://github.com/nIKsL/CDDA_exp_launcher.git && cd CDDA_exp_launcher && python3 -m venv venv && . ./venv/bin/activate && pip3 install -r requirements.txt && deactivate
```
____
**Edit options.py**

where does this program store downloaded releases
- RELEASE_FOLDER = "./exp_release/"
```
mkdir -p exp_release
```

game folder - full path
- GAME_FOLDER = "/home/n/MyDocs/cataclysmdda-0.F/"
____
you need to activate venv (next run) and start game - this is simle bash script
```
./start.sh
```

____
English is not my native language, so errors and inaccuracies are possible :)

I will be glad if it is useful to someone else :) good luck running in CDDA
