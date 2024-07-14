from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse
from config import templates, get_current_user
import joblib
import pandas as pd
from database import prediction_table

router = APIRouter()

lb = joblib.load("label_encoders.pkl")
model = joblib.load("Gradient Boosting Regression.pkl")


@router.get("/prediction", response_class=HTMLResponse)
async def get_prediction(request: Request, user: dict = Depends(get_current_user)):
    jb_title = lb['Job Title'].classes_
    gender = lb['Gender'].classes_
    education = lb['Education Level'].classes_
    return templates.TemplateResponse("prediction.html", {
        "request": request,
        "jb_title": jb_title.tolist(),
        "gender": gender.tolist(),
        "education": education.tolist()
    })


@router.post("/prediction", response_class=HTMLResponse)
async def post_prediction(request: Request,
                          name: str = Form(...),
                          job_title: str = Form(...),
                          gender: str = Form(...),
                          education: str = Form(...),
                          age: int = Form(...),
                          years_of_experience: int = Form(...)):
    job_title = lb['Job Title'].transform([job_title])[0]
    gender = lb['Gender'].transform([gender])[0]
    education = lb['Education Level'].transform([education])[0]

    make_prediction = pd.DataFrame({
        'Age': [age],
        'Gender': [gender],
        'Education Level': [education],
        'Job Title': [job_title],
        'Years of Experience': [years_of_experience]
    })

    prediction = model.predict(make_prediction)
    prediction_table.insert({
        "ID": len(prediction_table) + 1,
        "Date": pd.to_datetime("today").strftime("%d/%m/%Y"),  # "01/01/2021"
        "Name": name,
        "Job_title": lb['Job Title'].inverse_transform([job_title])[0],
        "Gender": lb['Gender'].inverse_transform([gender])[0],
        "Education": lb['Education Level'].inverse_transform([education])[0],
        "Age": age,
        "Years_of_Experience": years_of_experience,
        "Prediction": int(prediction[0].round(0))
    })
    return templates.TemplateResponse("prediction.html", {
        "request": request,
        "prediction": int(prediction[0].round(0))
    })
