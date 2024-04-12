print("=== Task 1 ===")
def find_and_print(messages, current_station):
    stations1 = [
        "Songshan",
        "Nanjing Sanmin",
        "Taipei Arena",
        "Nanjing Fuxing",
        "Songjiang Nanjing",
        "Zhongshan",
        "Beimen",
        "Ximen",
        "Xiaonanmen",
        "Chiang Kai-Shek Memorial Hall",
        "Guting",
        "Taipower Building",
        "Gongguan",
        "Wanlong",
        "Jingmei",
        "Dapinglin",
        "Qizhang",
        "Xiaobitan"
        ]
    stations2 = [
        "Songshan",
        "Nanjing Sanmin",
        "Taipei Arena",
        "Nanjing Fuxing",
        "Songjiang Nanjing",
        "Zhongshan",
        "Beimen",
        "Ximen",
        "Xiaonanmen",
        "Chiang Kai-Shek Memorial Hall",
        "Guting",
        "Taipower Building",
        "Gongguan",
        "Wanlong",
        "Jingmei",
        "Dapinglin",
        "Xiaobitan",
        "Qizhang",
        "Xindian City Hall",
        "Xindian"
    ]
    
    friendArr = list(messages.keys())
    # print(friendArr)
    indexCurrent1 = 0
    indexCurrent2 = stations2.index(current_station)
    for i in range(0, len(stations1)):
        if current_station not in stations1:
            indexCurrent1 = -1
        else:
            indexCurrent1 = stations1.index(current_station)    

    if indexCurrent1 != -1:
        manInStationIndex = []
        say = list(messages.values())
        for i in range(0, len(say)):
            for j in range(0, len(stations1)):
                if stations1[j] in say[i]:
                    manInStationIndex.append(stations1.index(stations1[j]))
        # print(manInStationIndex)            

        nearestIndex = 0
        temperary = float("Inf")
        for i in range(0, len(manInStationIndex)):
            if abs(indexCurrent1 - manInStationIndex[i]) < temperary:
                temperary = abs(indexCurrent1 - manInStationIndex[i])
                nearestIndex = manInStationIndex[i]
            else:
                continue    

        for i in range(0, len(manInStationIndex)):
            if manInStationIndex[i] == nearestIndex:
                print(friendArr[i])
            else:
                continue
    else:
        manInStationIndex = []
        say = list(messages.values())
        for i in range(0, len(say)):
            for j in range(0, len(stations2)):
                if stations2[j] in say[i]:
                    manInStationIndex.append(stations2.index(stations2[j]))
        # print(manInStationIndex)            

        nearestIndex2 = 0
        temperary = float("Inf")
        for i in range(0, len(manInStationIndex)):
            if abs(indexCurrent2 - manInStationIndex[i]) < temperary:
                temperary = abs(indexCurrent2 - manInStationIndex[i])
                nearestIndex2 = manInStationIndex[i]
            else:
                continue    

        for i in range(0, len(manInStationIndex)):
            if manInStationIndex[i] == nearestIndex2:
                print(friendArr[i])
            else:
                continue

# 以下不動
messages={
"Leslie":"I'm at home near Xiaobitan station.",
"Bob":"I'm at Ximen MRT station.",
"Mary":"I have a drink near Jingmei MRT station.",
"Copper":"I just saw a concert at Taipei Arena.",
"Vivian":"I'm at Xindian station waiting for you."
}
find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian

print("=== Task 2 ===")
consultantHour = {}
def book(consultants, hour, duration, criteria):
  nameArr = []
  rateArr = []
  priceArr = []
  for i in range(0, len(consultants)):
    nameArr.append(consultants[i]["name"])
    rateArr.append(consultants[i]["rate"])
    priceArr.append(consultants[i]["price"])


  if len(consultantHour.keys()) == 0:
    for i in range(0, len(nameArr)):
      consultantHour[nameArr[i]] = []
  
  inputTime = []
  for i in range(0, duration):
    inputTime.append(hour + i)
  # print("輸入的時間", inputTime)

  if criteria == "price":
    avaliableName = []
    for i in range(0, len(nameArr)):
      n = 0
      for j in range(0, len(consultantHour[nameArr[i]])):
        for k in range(0, len(inputTime)):
          if (inputTime[k] == consultantHour[nameArr[i]][j]):
            n += 1
          else:
            continue
      if n == 0:
        avaliableName.append(nameArr[i])
  
    #找誰便宜
    lowerestPrice = float("Inf")
    if len(avaliableName) == 0:
      print("No Service")
    else:
      for i in range(0, len(avaliableName)):
        if priceArr[nameArr.index(avaliableName[i])] < lowerestPrice:
          lowerestPrice = priceArr[nameArr.index(str(avaliableName[i]))]
        else:
          continue
      
      hiredname = nameArr[priceArr.index(lowerestPrice)]
      for i in range(0, len(inputTime)):
        consultantHour[hiredname].append(inputTime[i])
      print(hiredname)

  elif criteria == "rate":
    avaliableName = []
    for i in range(0, len(nameArr)):
      n = 0
      for j in range(0, len(consultantHour[nameArr[i]])):
        for k in range(0, len(inputTime)):
          if (inputTime[k] == consultantHour[nameArr[i]][j]):
            n += 1
          else:
            continue
      if n == 0:
        avaliableName.append(nameArr[i])
  
    #找誰評分高
    highestRate = float("-Inf")
    if len(avaliableName) == 0:
      print("No Service")
    else:
      for i in range(0, len(avaliableName)):
        if rateArr[nameArr.index(str(avaliableName[i]))] > highestRate:
          highestRate = priceArr[nameArr.index(str(avaliableName[i]))]
        else:
          continue
      
      hiredname = nameArr[priceArr.index(highestRate)]
      for i in range(0, len(inputTime)):
        consultantHour[hiredname].append(inputTime[i])
      print(hiredname)


# 以下不動
consultants=[
{"name":"John", "rate":4.5, "price":1000},
{"name":"Bob", "rate":3, "price":1200},
{"name":"Jenny", "rate":3.8, "price":800}
]
book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John

print("=== Task 3 ===")
def func(*data):
  nameArr = [*data]
  onewordArr = []
  for i in range(0,len(nameArr)):
    if len(nameArr[i]) == 2 or len(nameArr[i]) == 3:
      onewordArr.append(nameArr[i][1])
    elif len(nameArr[i]) == 4 or len(nameArr[i]) == 5:
      onewordArr.append(nameArr[i][2])
  
  check = 0
  for i in range(0, len(onewordArr)):
    n = 0
    for j in range(0, len(onewordArr)):
      if onewordArr[i] == onewordArr[j]:
        n += 1
      else:
        continue
   
    if n == 1:
      print(nameArr[i])
    else:
      check += 1
  if check == len(onewordArr):
    print("沒有")
 
func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安

print("=== Task 4 ===")
def get_number(index):
  numArr = [0]
  n = 0
  for i in range(1,index+1):
    if i % 3 != 0:
      n += 4
      numArr.append(n)
    elif i % 3 == 0:
      n -= 1
      numArr.append(n)
  print(numArr[index])     

get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70

print("=== Task 5 ===")
def find(spaces, stat, n):
    check = float("Inf")
    finalIndex = 0
    for i in range(0, len(spaces)):
        if stat[i] == 1:
            if spaces[i] - n >= 0 and spaces[i] - n < check:
                check = spaces[i] - n
                finalIndex = i
            elif check == float("Inf"):
                finalIndex = -1
    print(finalIndex)

find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2) # print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4) # print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4) # print 2