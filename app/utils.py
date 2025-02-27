from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")   
def get_hashed_password(password):
    hashed_pwd = pwd_context.hash(password)
    return hashed_pwd

def verify_pwd(plain_pwd,hashed_pwd):
     return pwd_context.verify(plain_pwd, hashed_pwd)