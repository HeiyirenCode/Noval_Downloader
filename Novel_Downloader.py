import requests
import lxml.html
import lxml.cssselect
import os

def download(url,time=2):
    user_agent = "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.19 (\
                    KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19 "
    headers = {'User-agent': user_agent, "accept-language": "zh-CN,zh;q=0.9,en;q=0.8"}
    print("downloading...", url)
    if time > 0:
        try:
            text = requests.get(url,headers=headers)
            text.encoding = "utf-8"
        except Exception as e:
            print("downloading try again", url)
            dowmload(url,time-1)
        return text.text
    else:
        print("download faile", url)

def getLinks(html):
    retList = []
    tree = lxml.html.fromstring(html)
    data = tree.cssselect("dl")[0]
    for i in data:
        tag = i.cssselect("a")[0]
        page = {}
        page["title"] = tag.get("title")
        page["href"] = tag.get("href")
        retList.append(page)
    return retList

def writeText(text, dir, i):
    if not os.path.isdir(dir):
        os.mkdir(dir)
    with open(dir+"/"+str(i)+".txt", "w", encoding="utf-8") as data:
        data.truncate()
        data.write(text)
    with open(dir+"/0.txt", "w", encoding="utf-8") as data:
        data.truncate()
        data.write(i)

def ReadText(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)
    if os.path.exists(dir+"/0.txt"):
        with open(dir+"/0.txt", "r", encoding="utf-8") as data:
            return data.read()
    else:
        with open(dir+"/0.txt", "w", encoding="utf-8") as data:
            data.write("0")
        return 0

def getContent(page):
    html = download(page)
    tree = lxml.html.fromstring(html)
    data = tree.get_element_by_id("content", None)
    return data.text_content()

def getUrl(home, href):
    return home + href

def flashNovel(url,dir):
    text = download(url)
    list = getLinks(text)
    dNum = int(ReadText(dir))+1
    for i in range(dNum,len(list)):
        writeDic = {}
        writeDic["title"] = list[i]["title"]
        writeDic["content"] = getContent(getUrl(url, list[i]["href"]))
        writeText(str(writeDic).replace(r"\xa0\xa0\xa0\xa0","\r\n    ")\
            .replace(r"\n","\n"), dir, str(i))
    print("flash finish")

urlFrxxz = "http://www.biquke.com/bq/0/990/"
urlLwcs = "http://www.biquke.com/bq/22/22565/"
urlWldf = "http://www.biquke.com/bq/0/362/"
urlXhdtgs = "http://www.biquke.com/bq/0/98/"
flashNovel(urlFrxxz,"frxxz")
flashNovel(urlLwcs,"lwcs")
flashNovel(urlWldf,"wldf")
flashNovel(urlXhdtgs,"xhdtsgs")
