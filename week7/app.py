# -*- coding: utf-8 -*-
from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

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
async def signUP(name: Annotated[str, Form()], username: Annotated[str, Form()] = "none", password: Annotated[str, Form()] = "none"):
    sql = ("SELECT `username` FROM `member` WHERE `username` = %s;")
    mycursor.execute(sql, [username])
    username_check = mycursor.fetchall()

    if username_check != []:
        return RedirectResponse("/error?message=帳號已被註冊", status_code=303)
    else:
        sql = ("INSERT INTO `member`(`name`, `username`, `password`) VALUES(%s, %s, %s);")
        val = (name, username, password)
        mycursor.execute(sql, val)
        mydb.commit()
        return RedirectResponse("/", status_code=303)

# 登入帳號
@app.post("/signin", response_class=RedirectResponse)
async def signIN(request: Request, username: Annotated[str, Form()] = "none", password: Annotated[str, Form()] = "none"):
    current_user = {"id":"","name":"","username":username, "signed-in":False}
    
    val = (username, password)
    sql = ("SELECT `id`,`name` FROM `member` WHERE `username` = %s AND `password` = %s")
    mycursor.execute(sql, val)
    user_check = mycursor.fetchall()

    if user_check != []:
        current_user["id"] = user_check[0][0]
        current_user["name"] = user_check[0][1]
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
            content += "<div class='message'><form action='/deleteMessage' method='post'><p class='bolder_real'>"+ r[2]+"："+"</p>"+"<p>"+ r[3]+"</p><button class='delete' name='id' value="+str(r[0])+">&#10005;</button></form></div>"
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
    text = content
    if content == "none":
        text = ""   
    val = (currnet_id, text)
    sql = ("INSERT INTO `message`(`member_id`, `content`) VALUES(%s, %s)")
    mycursor.execute(sql, val)
    mydb.commit()
    return RedirectResponse("/member",status_code=303,)
#刪除留言
@app.post("/deleteMessage", response_class=RedirectResponse)
async def delete_comment(request:Request,id:Annotated[str, Form()]):
    message_id = id
    sql = ("SELECT `id`,`member_id` FROM `message` WHERE `id` = %s;")
    mycursor.execute(sql, [message_id])
    myresult = mycursor.fetchall()
    
    member_id = myresult[0][1]
    current_user = request.session.get("user")
    
    if member_id == current_user["id"] :
        sql = ("DELETE FROM `message` WHERE `id` = %s")
        mycursor.execute(sql, [message_id])
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

# Member Query API
@app.get("/api/member", response_class=JSONResponse)
async def usernameQuery(request:Request, username):
    sql = ("SELECT `id`,`name` FROM `member` WHERE `username` = %s")
    mycursor.execute(sql, (username,))
    myresult = mycursor.fetchall()
    currentUser = request.session.get("user")
    if currentUser["signed-in"]:
        if myresult != []:
            response = {"data":
                {
                    "id":myresult[0][0],
                    "name":myresult[0][1],
                    "username":username
                }
            }
        else:
            response = {"data":None}
    else:
        response = {"data":None}
    
    return JSONResponse(response)

# Name Update API
class Name(BaseModel):
    name: str

@app.patch("/api/member", response_class=JSONResponse)
async def updateName(request:Request,name:Name):
    success_info = {
        "ok":True
    }
    error_info = {
        "error":True
    }

    current_user = request.session.get("user")

    if current_user["signed-in"]:
        try:
            current_id = current_user["id"]
            new_name = jsonable_encoder(name)["name"]
            current_user["name"] = new_name
            sql = ("UPDATE `member` SET `name`=%s WHERE `id` =%s")
            val = (new_name, current_id)
            mycursor.execute(sql, val)
            mydb.commit()
        except:
            return JSONResponse(error_info)
        return JSONResponse(success_info)
    else:
        return JSONResponse(error_info)