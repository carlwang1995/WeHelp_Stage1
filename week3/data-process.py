import urllib.request as req
import json
import csv

# =====================================================Task 1=====================================================
srcSpot = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
srcMrt = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

# 讀取sopt裡的資料，存在"spotList"變數裡
with req.urlopen(srcSpot) as response:
    data = json.load(response)
    spotList = data["data"]["results"]

# 讀取mrt裡的資料，存在"mrtList"變數裡
with req.urlopen(srcMrt) as response:
    data = json.load(response)
    mrtList = data["data"]

# 抓圖片的第一個網址，放回spotlist中
for i in range(0, len(spotList)):
    imageUrl = spotList[i]["filelist"].lower() #把文字都轉成小寫
    firstUrl = imageUrl.split(".jpg")[0] + ".jpg"
    spotList[i]["filelist"] = firstUrl
    
#將spot與mrt的SERIAL_NO配對，將district放到soptList中
for i in range(0, len(spotList)):
    district = 0
    for j in range(0, len(mrtList)):
        if spotList[i]["SERIAL_NO"] == mrtList[j]["SERIAL_NO"]:
            district = mrtList[j]["address"][5:8]
    spotList[i]["district"] = district

#將spotlist取出需要的資料，寫到csv檔案中
with open("spot.csv", mode= "w", newline = "", encoding = "utf-8") as file:
    writer = csv.writer(file)
    for i in range(len(spotList)):
        writer.writerow([spotList[i]["stitle"],spotList[i]["district"],spotList[i]["longitude"],spotList[i]["latitude"],spotList[i]["filelist"]])

#捷運站與景點的"SERIAL_NO"配對，並存放對應的景點名稱
for i in range(0, len(mrtList)):
    for j in range(0,len(spotList)):
        if mrtList[i]["SERIAL_NO"] == spotList[j]["SERIAL_NO"]:
            mrtList[i]["stitle"] = spotList[j]["stitle"]

#用一個list暫時存放各捷運站(有重複)對應的景點
temporary = []
for i in range(0, len(mrtList)):
    mrtSpotPair = []
    mrtSpotPair.append(mrtList[i]["MRT"])
    for j in range(0, len(mrtList)):
        if mrtList[i]["MRT"] == mrtList[j]["MRT"]:
            mrtSpotPair.append(mrtList[j]["stitle"])
    temporary.append(mrtSpotPair)

#篩掉上述list中 重複的資料
mrt_spot = []
for i in range(0, len(temporary)):
    if temporary[i] not in mrt_spot:
        mrt_spot.append(temporary[i])

#篩掉重複資料後，寫到csv檔案中
with open("mrt.csv", mode = "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for i in range(0, len(mrt_spot)):
        writer.writerow(mrt_spot[i])

# =====================================================Task 2=====================================================
final = []
def getData(url):
    request = req.Request(url, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    import bs4
    root = bs4.BeautifulSoup(data, "html.parser")
    titles = root.find_all("div", class_="title")
    pushNums = root.find_all("div", class_="nrec")

    # 將該頁文章標題放到一個陣列
    titleList = []
    for title in titles:
        if title.a != None:
            titleList.append(title.a.string)
        else:
            titleList.append("文章已被刪除")
            
    # 將該頁文章的推/噓數量放到一個陣列
    numList = []
    for pushNum in pushNums:
        if pushNum.span != None:
            numList.append(pushNum.span.string)
        else:
            numList.append(0)

    # 將該頁文章內容的發文時間放到一個陣列
    timeList = []
    articleLink = ""
    for title in titles:
        if title.a != None:
            articleLink = "https://www.ptt.cc/" + title.a["href"]
            request = req.Request(articleLink, headers={
                "cookie":"over18=1",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            })
            with req.urlopen(request) as response:
                article = response.read().decode("utf-8")
            artRoot = bs4.BeautifulSoup(article, "html.parser")
            spans = artRoot.find_all("span", class_="article-meta-value")
            if len(spans) != 0:
                timeList.append(spans[3].string)
            else:
                timeList.append("")
        else:
            timeList.append("文章被刪除，無文章網址")
    
    # 將該頁所有標題文章對應相關資訊組成一個陣列，再放到一陣列中
    for i in range(0, len(titleList)):
        if titleList[i] != "文章已被刪除":
            final.append([titleList[i], numList[i], timeList[i]])
    
    #抓取上一頁的網址
    nextLink = root.find("a", string="‹ 上頁")
    return nextLink["href"]

pageUrl = "https://www.ptt.cc/bbs/Lottery/index.html"
count = 0
while count < 3:
    pageUrl = "https://www.ptt.cc" + getData(pageUrl)
    count += 1
        
if count == 3:
    with open("article.csv", mode="w", newline="",encoding="utf-8") as file:
        writer = csv.writer(file)
        for pttTitle in final:
            writer.writerow(pttTitle)