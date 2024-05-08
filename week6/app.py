# -*- coding: utf-8 -*-
from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key = "my_secret_key")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 連接資料庫
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "11111111",
    database = "website"
)
mycursor = mydb.cursor()

# 訪問首頁
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html"
    )

# 註冊帳號
@app.post("/signup", response_class=RedirectResponse)
async def signUP(name: Annotated[str, Form()],username: Annotated[str, Form()] = "none", password: Annotated[str, Form()] = "none"):
    mycursor.execute("SELECT `username` FROM `member`;")
    myresult = list(mycursor)
    username_list = []
    for r in myresult:
        username_list.append(r[0])
    if username in username_list:
        return RedirectResponse("/error?message=帳號已重複", status_code=303)
    else:
        sql = ("INSERT INTO `member`(`name`, `username`, `password`) VALUES(%s, %s, %s);")
        val = (name, username, password)
        mycursor.execute(sql, val)
        mydb.commit()
        return RedirectResponse("/", status_code=303)

# 登入帳號
@app.post("/signin", response_class=RedirectResponse)
async def signIN(request: Request, username: Annotated[str, Form()] = "none", password: Annotated[str, Form()] = "none"):
    mycursor.execute("SELECT `username` FROM `member`;")
    myresult = mycursor.fetchall()
    username_list =[]
    for r in myresult:
        username_list.append(r[0])
    sql = ("SELECT `id`,`name`,`password` FROM `member` WHERE `username` = %s;")
   
    if username in username_list:
        mycursor.execute(sql, [username])
        myresult = mycursor.fetchall()[0]
        current_user = {"id":"","name":"","username":username, "signed-in":False}

    if password == myresult[2]:
        current_user["id"] = myresult[0]
        current_user["name"] = myresult[1]
        current_user["signed-in"] = True
        request.session["user"] = current_user
        return RedirectResponse("/member",status_code=303)
    else:
        return RedirectResponse("/error?message=帳號或密碼輸入錯誤", status_code=303)
    
# 登入成功
@app.get("/member", response_class=HTMLResponse)
async def allow(request: Request):
    current_user = request.session.get("user")
    # 抓留言板資料
    mycursor.execute("SELECT `message`.`id`,`message`.`member_id`,`member`.`name`, `message`.`content` FROM `message` JOIN `member` ON `message`.`member_id` = `member`.`id` ORDER BY `message`.`time` DESC;")
    myresult = mycursor.fetchall()
    content = ""
    for r in myresult:
        if current_user["id"] == r[1]:
            content += "<div class='message'><form action='/deleteMessage' method='post'><p class='bolder'>"+ r[2]+"："+"</p>"+"<p>"+ r[3]+"</p><button class='delete' name='id' value="+str(r[0])+">&#10005;</button></form></div>"
        else:
            content += "<div class='message'><p class='bolder'>"+ r[2]+"："+"</p>"+"<p>"+ r[3]+"</p></div>"

    # 檢查登入狀態
    name = current_user["name"]
    if current_user["signed-in"]:
        return templates.TemplateResponse(
            request=request, name="member.html", context={"name":name,"content":content})
    else:
        return RedirectResponse("/")

# 新增留言
@app.post("/createMessage", response_class=RedirectResponse)
async def comment(request:Request, content:Annotated[str, Form()] = "none"):
    currnet_id = request.session.get("user")["id"]
    sql = ("INSERT INTO `message`(`member_id`, `content`) VALUES(%s, %s)")
    text = content
    if content == "none":
        text = ""
    val = (currnet_id, text)
    mycursor.execute(sql, val)
    mydb.commit()
    return RedirectResponse("/member",status_code=303,)
#刪除留言
@app.post("/deleteMessage", response_class=RedirectResponse)
async def delete_comment(id:Annotated[str, Form()]):
    member_id = id
    sql = ("DELETE FROM `message` WHERE `id` = %s")
    mycursor.execute(sql, [member_id])
    mydb.commit()
    return RedirectResponse("/member",status_code=303,)

# 登入失敗
@app.get("/error", response_class=HTMLResponse)
async def refuse(request: Request, message):
    return templates.TemplateResponse(
        request=request, name="error.html", context={"message":message}
    )

# 登出
@app.get("/signout", response_class=RedirectResponse)
async def signOUT(request: Request):
    current_user = {"id":"","name":"","username":"", "signed-in":False}
    request.session["user"] = current_user
    return RedirectResponse("/")