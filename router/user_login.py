from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from config import templates
from database import user_table, Query
router = APIRouter()


@router.get("/user-login", response_class=HTMLResponse)
async def get_user_login(request: Request):
    return templates.TemplateResponse("user-login.html", {"request": request})


@router.post("/user-login", response_class=HTMLResponse)
async def post_user_login(request: Request,
                          email: str = Form(...),
                          password: str = Form(...)):
    # Process login data
    user = user_table.get(Query.email == email)
    if user and (user["password"] == password):
        # Set session
        request.session["user"] = {
            "fullname": user["fullname"],
            "email": user["email"]
        }
        request.session["logged_in"] = True
        return RedirectResponse("/", status_code=302)
    else:
        return templates.TemplateResponse("user-login.html", {
            "request": request,
            "messages": "Invalid email or password"
        })


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)