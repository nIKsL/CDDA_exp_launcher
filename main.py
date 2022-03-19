"""
work with experimental releases of CDDA
list of changes
auto download experimental releases for linux
"""
import requests
from bs4 import BeautifulSoup
import sys
import os

# some CONSTANTS for us
from options import *

# https://github.com/aegirhall/console-menu   
from consolemenu import *
from consolemenu.items import *


def get_page(URL):
    """
    Trying to dowload html page
    Args:
        URL (string): http(s) url
    Returns:
        [HTML]: returning page sources
    """

    try:
        page = requests.get(URL).text
    except:
        page = None
        print("Error getting page")
        sys.exit()  # TODO: убрать выход из программы - обрабатывать исключения
    return page

def get_desc_commit(URL):
    """
    Text description of commit 
    Arguments:
        URL -- commit url
    Returns:
        str -- subj
    """
    html = get_page(URL)
    soup = BeautifulSoup(html, "lxml")
    commit_desc = soup.find("div", class_="commit-desc")
    try:
        return commit_desc.pre.text
    except:
        return "Empty"

def save_release(url, release_file_name):
    """
    save release with url
    return:
        1 = all ok
        0 = can`t download
    """
    if os.path.exists(f"{RELEASE_FOLDER}{release_file_name}"):
        print("We already have this file") 
        print(f"{RELEASE_FOLDER}{release_file_name}")
        release_file_size = round((os.stat(f'{RELEASE_FOLDER}{release_file_name}').st_size)/(1024*1024),1)
        print(f"File size: {release_file_size}Mb \n")
        input("Press Enter")
        return 1
    else:
        print("Starting download") 

    with open(f'{RELEASE_FOLDER}{release_file_name}',"wb") as f:
        try:
            ufr = requests.get(url)
            f.write(ufr.content)
        except:
            print('Error - we can`t download (mb have no this build)')
            input("Press Enter")
            return 0
        finally:
            print("Done!")
            print(f"{RELEASE_FOLDER}{release_file_name}")
            release_file_size = round((os.stat(f'{RELEASE_FOLDER}{release_file_name}').st_size)/(1024*1024),1)
            print(f"File size: {release_file_size}Mb \n")
            input("Press Enter")
            return 1

def get_items(page):
    """
    soup page > find release div > get data, build number, short description
    run while current build == release or page

    Arguments:
        page {HTML} -- result of runing requests.get()
    Returns:
        [dict] -- returning dictionary ; key - name, value - description     
    """
    soup = BeautifulSoup(page, "lxml")

    # парсим все "карточки релизов"
    all_release = soup.find_all("div", class_="Box-body")

    # перебираем их
    items = {}
    for release in all_release:
        # название релиза типа 'Cataclysm-DDA experimental build 2022-02-21-2034'
        release_name = release.find("h1").text
        if release_name.split()[-1] <= CURRENT_VERSION:
            break
        # получаем url с этим коммитом (дальше будем дёргать оттуда описание)
        url_commit = release.find("div", class_="markdown-body").p.a.get('href')
        # собственно текстовое описание этого коммита получаем
        release_desc = get_desc_commit(url_commit)
        items[release_name] = release_desc
        # print(release.find("h1").text) # это название билда
        # print(release.find("div", class_="markdown-body").p.a.get('href')) # это ссылка на коммит
        # адрес скомпилированного релиза


    return items

def get_new_releases():
    """
    Check last 10 releases (1page)
    return:
        list of releases with desc
        0..11 nnumber = release diff count (11 == more then 10)
    """
    html = get_page(MAIN_URL)
    releases = get_items(html)
#     for release_name, release_desc in releases.items():
#         print(f"{release_name}\n{release_desc}\n")
    return releases

def print_list_of_changes(releases):
    """
    print all changes from our game relize to last
    or last 10 descriptions
    releases = dict{release name: description} 
    """
    for item in releases:
        if item.split()[-1] == CURRENT_VERSION:
            input("Press Enter")
            return
        else:
            print(item)
            print(releases[item])
            print()
    input("Press Enter")
    return


def main():
    print("Trying to get new data from github. Plz wait ;)")
    releases = get_new_releases()
    i = 0
    for item in releases:
        if item.split()[-1] == CURRENT_VERSION:
            break
        else:
            i += 1
#             print(item.split()[-1])
    if i >= 10:
        X = 'More then 10'
    else:
        X = str(i)
    try:
        last_release = list(releases.keys())[0].split()[-1]
    except IndexError:
        last_release = CURRENT_VERSION

    # release_file_name = f"{DISTRO_TYPE}{last_release}.tar.gz"
    # release_https_file = f"{MAIN_URL}/download/cdda-experimental-{last_release}/{DISTRO_TYPE}{last_release}.tar.gz"
    # # release_https_file = 'https://github.com/CleverRaven/Cataclysm-DDA/releases/download/cdda-experimental-2022-03-19-0426/cdda-linux-tiles-x64-2022-03-19-0426.tar.gz'
    # release_file_size = round((os.stat(f'{RELEASE_FOLDER}{release_file_name}').st_size)/(1024*1024),1)
    # 
    # res = requests.head(release_https_file)
    # http_file_size = int(res.headers['content-length'])
    # if release_file_size > 0000000:
    #     print(f'Размер файла: {release_file_size}')
    #     # print(f'Адрес файла: {release_https_file}')
    #     print(f'Размер файла на сервере: {http_file_size}')
    # else:
    #     print('С размером файла что-то не так.. попробуйте позже')
    # sys.exit()

    release_https_file = f"{MAIN_URL}/download/cdda-experimental-{last_release}/{DISTRO_TYPE}{last_release}.tar.gz"
    release_file_name = f"{DISTRO_TYPE}{last_release}.tar.gz"
    # Create the menu
    menu = ConsoleMenu("CDDA game Launcher", f"Our game version is {CURRENT_VERSION}\nIn release {X} new version(s)")
    # Create some items
    # A FunctionItem runs a Python function when selected
    dl_item = FunctionItem("Dowload last experimental build", save_release, [release_https_file, release_file_name])
    list_item = FunctionItem("List of changes", print_list_of_changes, [releases])
    start_item = CommandItem("Start GAME", f"cd {GAME_FOLDER} && ./cataclysm-tiles", should_exit=True)
    string = "Press_Enter__and_you_need_to_restart_launcher now"
#     string working wrong (read -p string) dunno why... just left it mb later I fix it
    # check tar archive -> if ok unppack it in game folder
    tar_command = f"tar -tzf {RELEASE_FOLDER}{release_file_name} 1>/dev/null && tar -C {GAME_FOLDER}.. -xvzf {RELEASE_FOLDER}{release_file_name} && read -p {string}"
    install_item = CommandItem("Install new build", f"{tar_command}", should_exit=True)
    save_item = FunctionItem("Save game data and preferences", input, ["working on it"])
    load_item = FunctionItem("Load game data and preferences", input, ["working on it"])
    pref_item = FunctionItem("Launcher preferences", input, ["Please redo options.py"])
    # Once we're done creating them, we just add the items to the menu
    menu.append_item(dl_item)
    menu.append_item(list_item)
    menu.append_item(start_item)
    menu.append_item(install_item)
    # menu.append_item(save_item)
    # menu.append_item(load_item)
    # menu.append_item(pref_item)
    # Finally, we call show to show the menu and allow the user to interact
    menu.show()






if __name__ == "__main__":
    main()
