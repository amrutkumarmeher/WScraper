import requests
import bs4
import os
import sys
import pathlib


def getwebsite(link):
    return bs4.BeautifulSoup(requests.get(link).text, features="html.parser")


def scrapeImgsLiks(link):
    website = getwebsite(link)
    ImgLi = list(website.find_all("img"))
    OnlyLinks = []
    for linkI in ImgLi:
        linkI = str(linkI)
        chunks = linkI.split(" ")  # split between diff attributes.
        for chunk in chunks:
            if chunk.startswith('src="'):     # check if it's the src link.
                chunk = chunk.replace('src="', "")         # removing src=".
                # removing back quote.
                chunk = chunk.replace('"', "")
                OnlyLinks.append(chunk)
                break
    return OnlyLinks


def scrapeVidLinks(link):
    website = getwebsite(link)
    VidLi = list(website.find_all("video"))
    OnlyLinks = []
    for linkI in VidLi:
        linkI = str(linkI)
        chunks = linkI.split(" ")  # split between diff attributes.
        for chunk in chunks:
            if chunk.startswith('src="'):     # check if it's the src link.
                # removing src=".
                chunk = chunk.replace('src="', "")
                # removing back quote.
                chunk = chunk.replace('"', "")
                if ">" in chunk:
                    # if its the last attribute of the tag
                    chunk = chunk[:chunk.index(">")]
                if "https:" not in chunk or "http:" not in chunk:
                    chunk = "".join(["http:", getdomain(link), "/", chunk])
                    if "//" not in chunk:
                        chunk = chunk.replace("http:", "http://")
                        chunk = chunk.replace("https:", "https://")
                OnlyLinks.append(chunk)
                break

    return OnlyLinks


def getdomain(link: str):
    linkli = link.split("//")
    linkli = linkli[1].split("/")
    return linkli[0]


def delStr(str1: str, str2: str):
    cou = len(str1)
    if len(str1) > len(str2):
        con = len(str2)
        p = 0
        for i in range(con):
            if not (str1[i] == str2[i]):
                return str1[i:]
            else:
                pass
            p = i
        return str1[p+1:]

    elif len(str2) > len(str1):
        con = len(str1)
        p = 0
        for i in range(con):
            if not (str1[i] == str2[i]):
                return str2[i:]
            else:
                pass
            p = i
        return str2[p+1:]


def SetDirs(Path: str):
    if (Path != ".") or (Path == ""):
        initP = pathlib.Path().absolute().as_uri().replace("file:///", "")
        Path = pathlib.Path(Path).absolute().as_uri().replace("file:///", "")
        Path = delStr(Path, initP)
        if "//" in Path:
            DirLi = Path.split("//")
        elif "\\" in Path:
            DirLi = Path.split("\\")
        else:
            DirLi = [Path[1:]]
        for i in DirLi:
            try:
                os.mkdir(i)
                os.chdir(i)
            except:
                os.chdir(i)
        os.chdir(initP)
    else:
        pass


def saveVids(ScrabedLList: list, targetLoc=".", format: str = "mp4"):
    con = 0
    SetDirs(targetLoc)
    print("Path set! \n\n")
    for link in ScrabedLList:
        vid = requests.get(link).content
        if sys.getsizeof(vid) < 50:
            print(
                f"Scraping Failed! | Image Name: {con}.{format} | size: {sys.getsizeof(vid)} | from: {link}\n")
            continue
        print(
            f"Scraping Successful! | Image Name: {con}.{format} | size: {sys.getsizeof(vid)} | from: {link}\n")
        with open(f"{targetLoc}//{con}.{format}", "wb") as f:
            f.write(vid)
            con += 1


def saveImgs(ScrabedLList: list, targetLoc=".", format: str = "jpg"):
    con = 0
    SetDirs(targetLoc)
    print("Path set! \n\n")
    for link in ScrabedLList:
        photo = requests.get(link).content
        if sys.getsizeof(photo) < 50:
            print(
                f"Scraping Failed! | Image Name: {con}.{format} | size: {sys.getsizeof(photo)} | from: {link}\n")
            continue
        print(
            f"Scraping Successful! | Image Name: {con}.{format} | size: {sys.getsizeof(photo)} | from: {link}\n")
        with open(f"{targetLoc}//{con}.{format}", "xb") as f:
            f.write(photo)
            con += 1


if __name__ == "__main__":
    i = scrapeVidLinks("http://127.0.0.1:5500/index.html")
    saveVids(i, targetLoc="CapturedFiles", format="mp4")
