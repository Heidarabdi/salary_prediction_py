from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
from config import templates
from database import user_table, Query

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
    # validate user registration
    status, message = validate_user_registration(fullname, phone, password, email)
    if status:
        user_table.insert({
            "fullname": fullname,
            "phone": phone,
            "password": password,
            "email": email
        })
        return RedirectResponse(url="/user-login", status_code=302)
    else:
        return templates.TemplateResponse("user-registration.html", {
            "request": request,
            "messages": message
        })


# validations for user registration
# 1. Fullname should not be empty and shoud 5 characters long
# 2. Phone should be 9 characters long
# 3. Password should be 8 characters long
# 4. Email should be valid
# 5. Email should be unique
# 6. Phone should be unique

def validate_user_registration(fullname: str, phone: str, password: str, email: str):
    # 1. Fullname should not be empty and shoud 5 characters long
    if len(fullname) < 5:
        message = "Fullname should be at least 5 characters long"
        return False, message
    # 2. Phone should be 9 characters long
    if len(phone) != 9:
        message = "Phone number should be 9 characters long"
        return False, message
    # 3. Password should be 8 characters long
    if len(password) < 8:
        message = "Password should be at least 8 characters long"
        return False, message
    # 4. Email should be valid
    if not email.count("@") == 1:
        message = "Email should be valid"
        return False, message
    # 5. Email should be unique
    if user_table.search(Query.email == email):
        message = "Email already exists"
        return False, message
    # 6. Phone should be unique
    if user_table.search(Query.phone == phone):
        message = "Phone already exists"
        return False, message
    return True, None

