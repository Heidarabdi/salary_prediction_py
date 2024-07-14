from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from config import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    user = request.session.get("user")
    return templates.TemplateResponse("home.html", {"request": request, "user": user})
