from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/public", StaticFiles(directory="public"), name="public")

app.add_middleware(SessionMiddleware, secret_key="!secret")
from router import home, prediction, previous_prediction, user_login, user_register

app.include_router(home.router)
app.include_router(prediction.router)
app.include_router(previous_prediction.router)
app.include_router(user_login.router)
app.include_router(user_register.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
