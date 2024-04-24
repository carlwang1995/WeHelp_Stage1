from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key = "my_secret_key")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.post("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.post("/signin", response_class=RedirectResponse)
async def signIN(request:Request, username: Annotated[str, Form()] = "none", password: Annotated[str, Form()] = "none"):
    user = {"username":username, "password":password, "signed-in":False}
    if user["username"] == "test" and user["password"] == "test":
        user["signed-in"] = True
        request.session["user"] = user
        return RedirectResponse("/member", status_code=303) # 狀態碼303，讓原本的POST方法在重新導向後改為GET方法(預設狀態碼為307)
    elif user["username"] == "none" or user["password"] == "none":
        return RedirectResponse("/error?message=請輸入帳號、密碼", status_code=303)
    else:
        return RedirectResponse("/error?message=帳號或密碼輸入錯誤", status_code=303)
    
@app.get("/member", response_class=HTMLResponse)
async def get_member_page(request: Request):
    user = request.session.get("user")
    if user["signed-in"]:
        return templates.TemplateResponse(
            request=request, name="member.html"
        )
    return RedirectResponse("/")

@app.get("/error", response_class=HTMLResponse)
async def get_error_page(request: Request, message):
    return templates.TemplateResponse(
        request=request, context={"message":message} ,name="error.html"
    )

@app.get("/signout",  response_class=RedirectResponse)
async def signOUT(request: Request):
    user = request.session.get("user")
    user["signed-in"] = False
    print(user)
    return RedirectResponse("/")

@app.get("/square/{square}",response_class=HTMLResponse)
async def calculateSquare(request:Request,square: int):
    answer = square ** 2
    return templates.TemplateResponse(
        request=request, context={"answer":answer}, name="square.html"
    )