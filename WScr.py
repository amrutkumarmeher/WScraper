import requests
import bs4
import os
import sys
import pathlib

def scrapeImgsLiks(link):
    website = requests.get(link).text
    website = bs4.BeautifulSoup(website,features="html.parser")
    ImgLi = list(website.find_all("img"))
    OnlyLinks = []
    for linkI in ImgLi:
        linkI = str(linkI)
        chunks = linkI.split(" ") # split between diff attributes.
        for chunk in chunks:
            if chunk.startswith('src="'):     # check if it's the src link.
                chunk = chunk.replace('src="',"")         # removing src=".
                chunk = chunk.replace('"',"")             # removing back quote.
                OnlyLinks.append(chunk)
                break
    return OnlyLinks
def delStr(str1:str,str2:str):
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

def SetDirs(Path:str):
    initP = pathlib.Path().absolute().as_uri().replace("file:///","")
    Path = pathlib.Path(Path).absolute().as_uri().replace("file:///","")
    Path = delStr(Path,initP)
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
    

def findExt(link):
    ext = link.split(".")[-1]
    if len(ext) > 5:
        return None
    else:
        return ext

def saveImgs(ScrabedLList:list,targetLoc=".",format:str="jpg"):
    con = 0
    SetDirs(targetLoc)
    print("Path set! \n\n")
    for link in ScrabedLList:
        photo = requests.get(link).content
        if sys.getsizeof(photo) < 50:
            print(f"Scraping Failed! | Image Name: {con}.{format} | size: {sys.getsizeof(photo)} | from: {link}\n")
            continue
        print(f"Scraping Successful! | Image Name: {con}.{format} | size: {sys.getsizeof(photo)} | from: {link}\n")
        with open(f"{targetLoc}//{con}.{format}","xb") as f:
               f.write(photo)
               con += 1
        

if __name__ == "__main__":
    li = scrapeImgsLiks("https://unsplash.com/s/photos/gallery")
    saveImgs(li,format="avif",targetLoc=".//Newfol//Amrut")
    pass