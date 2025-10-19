from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserVisit
import uuid

router = APIRouter(prefix="/user", tags=["User Tracking"])

@router.get("/track")
def track_user(request: Request, response: Response, db: Session = Depends(get_db)):
    # check if user has cookie
    user_cookie = request.cookies.get("user_id")
    
    if user_cookie:
        # user already tracked
        user = db.query(UserVisit).filter_by(user_id=user_cookie).first()
        if user:
            return {"message": "User already tracked"}
    else:
        # new user: generate cookie
        user_cookie = str(uuid.uuid4())
        response.set_cookie(key="user_id", value=user_cookie, max_age=60*60*24*365)  # 1 year

    # fallback: get IP
    ip = request.client.host

    # check if already exists by IP or user_id
    user = db.query(UserVisit).filter((UserVisit.user_id == user_cookie) | (UserVisit.ip == ip)).first()
    if not user:
        new_user = UserVisit(user_id=user_cookie, ip=ip)
        db.add(new_user)
        db.commit()

    return {"message": "User tracked successfully"}
