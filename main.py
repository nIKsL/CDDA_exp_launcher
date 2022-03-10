"""
выводим список эксперименталок
и краткое описание - что изменилось в какой
"""
import requests
from bs4 import BeautifulSoup
import sys


MAIN_URL = "https://github.com/CleverRaven/Cataclysm-DDA/releases"


def get_page(URL):
    """
    переходим по адресу и возвращаем содержимое

    Args:
        URL (string): адрес http(s)

    Returns:
        [HTML]: возвращаем содержимое страницы
    """

    try:
        page = requests.get(URL).text
    except:
        page = None
        print("Ошибка")
        sys.exit()  # TODO: убрать выход из программы - обрабатывать исключения

    return page

def get_desc_commit(URL):
    """
    текстовое описание коммита

    Arguments:
        URL -- url коммита

    Returns:
        str -- сабж
    """
    html = get_page(URL)
    soup = BeautifulSoup(html, "lxml")
    commit_desc = soup.find("div", class_="commit-desc")
    try:
        return commit_desc.pre.text
    except:
        return ""

def get_items(page):
    """
    передаём страницу, её соупим и ищем карточки релизов
    из них вытаскиваем дату, №билда, краткое описание

    Arguments:
        page {HTML} -- результат выполнения requests.get()

    Returns:
        [dict] -- возвращаем словарь, ключ - название, значение - описание        
    """
    soup = BeautifulSoup(page, "lxml")

    # парсим все "карточки релизов"
    all_release = soup.find_all("div", class_="Box-body")

    # перебираем их
    items = {}
    for release in all_release:
        # название релиза типа 'Cataclysm-DDA experimental build 2022-02-21-2034'
        release_name = release.find("h1").text
        # получаем url с этим коммитом (дальше будем дёргать оттуда описание)
        url_commit = release.find("div", class_="markdown-body").p.a.get('href')
        # собственно текстовое описание этого коммита получаем
        release_desc = get_desc_commit(url_commit)
        items[release_name] = release_desc
        # print(release.find("h1").text) # это название билда
        # print(release.find("div", class_="markdown-body").p.a.get('href')) # это ссылка на коммит
    return items

def main():
    html = get_page(MAIN_URL)
    releases = get_items(html)
    for release_name, release_desc in releases.items():
        print(f"{release_name}\n{release_desc}\n")
    # for item in releases:
    #     print(f"{item[0]}\n{item[1]}\n")
    # print(releases)

if __name__ == "__main__":
    main()
