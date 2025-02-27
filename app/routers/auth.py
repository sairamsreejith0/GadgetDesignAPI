from fastapi import APIRouter,Depends,HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import User
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.utils import get_hashed_password,verify_pwd
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta,timezone
import jwt
from jose import JWTError

# Load environment variables
load_dotenv()

router = APIRouter() 

secret_key = os.getenv("SECRET_KEY","secret")
access_token_expire = os.getenv("ACCESS_TOKEN_EXPIRE")
oauth2scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
class TokenResponse(BaseModel):
    access_token: str
    user:str

def create_access_token(data:dict,expires_delta:timedelta=None):
    user_data = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=int(access_token_expire))
    expire = datetime.now(timezone.utc) + expires_delta
    user_data.update({"exp": expire})
    return jwt.encode(user_data, secret_key, algorithm="HS256")

def verify_token(token:str):
    try:
        payload = jwt.decode(token, secret_key, algorithms="HS256")
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
def get_current_user(token: str = Depends(oauth2scheme)):
    username = verify_token(token)
    return username
    
# Example Route
@router.get("/test")
def test_route():
    return {"message": "Auth module is working!"}

class Usersignup(BaseModel):
    username:str
    password:str
@router.post("/register",response_model=dict)
def user_registration(user:Usersignup,db: Session=Depends(get_db)):
    user1 = db.query(User).filter(User.username==user.username).first()
    if user1:
        return HTTPException(status_code=400,detail="Username exists")
    hashed_pwd = get_hashed_password(user.password)
    new_user = User(username = user.username,hashed_password = hashed_pwd)
    db.add(new_user)
    db.commit()
    return {"message":"user registered successfully"}
    
    

@router.post("/token",response_model=TokenResponse)
def user_login(form_data : OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db),response_model = dict):
    user = db.query(User).filter(User.username==form_data.username).first()
    if user:
        flag = verify_pwd(form_data.password,user.hashed_password)
        if flag:
            access_token = create_access_token(data={"sub":user.username})
        
            return {"user":user.username,"access_token":access_token}
        else:
            raise HTTPException(status_code=401,detail="user doesn't exist")
    else:
        raise HTTPException(status_code=401,detail="user doesn't exist")