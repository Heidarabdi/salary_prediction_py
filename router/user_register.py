from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
from config import templates
from database import user_table

router = APIRouter()


@router.get("/user-registration", response_class=HTMLResponse)
async def get_user_registration(request: Request):
    current_time = datetime.now().strftime("%Y-%m-%d")
    return templates.TemplateResponse("user-registration.html", {"request": request, "current_time": current_time})


@router.post("/user-registration", response_class=HTMLResponse)
async def post_user_registration(request: Request,
                                 fullname: str = Form(...),
                                 phone: str = Form(...),
                                 password: str = Form(...),
                                 email: str = Form(...)):
    # Process registration data
    user_table.insert({
        "fullname": fullname,
        "phone": phone,
        "password": password,
        "email": email
    })
    # go to login page
    return RedirectResponse(url="/user-login", status_code=302)
