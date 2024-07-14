from fastapi.templating import Jinja2Templates
from fastapi import Request, HTTPException, Depends
from typing import Optional, Dict


templates = Jinja2Templates(directory="template")


def get_current_user(request: Request) -> Optional[Dict]:
    user = request.session.get("user")
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    return user





