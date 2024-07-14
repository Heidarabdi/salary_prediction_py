from fastapi import APIRouter, Request, Depends
from config import templates
from fastapi.responses import HTMLResponse
from database import prediction_table,User
from config import get_current_user

router = APIRouter()


@router.get("/previous-prediction", response_class=HTMLResponse)
async def get_previous_prediction(request: Request, user: dict = Depends(get_current_user)):
    details = prediction_table.all()
    return templates.TemplateResponse("previous-prediction.html", {"request": request, "details": details})
