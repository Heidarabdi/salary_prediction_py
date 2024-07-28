from fastapi import APIRouter, Request, Depends, HTTPException
from starlette.responses import RedirectResponse

from config import templates
from fastapi.responses import HTMLResponse
from database import prediction_table, Query
from config import get_current_user

router = APIRouter()


@router.get("/previous-prediction", response_class=HTMLResponse)
async def get_previous_prediction(request: Request, user: dict = Depends(get_current_user)):
    details = prediction_table.all()
    details = sorted(details, key=lambda x: x["ID"], reverse=True)
    return templates.TemplateResponse("previous-prediction.html", {"request": request, "details": details})


# delete prediction method
# @router.post("/delete/{ID}")
# async def delete_prediction(_id: int, user: dict = Depends(get_current_user)):
#     if not prediction_table.get(Query.ID == _id):
#         raise HTTPException(status_code=404, detail="Prediction not found")
#     prediction_table.remove(Query.ID)
#     return RedirectResponse(url="/previous-prediction", status_code=303)
