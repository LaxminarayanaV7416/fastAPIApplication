from jose import jwt, JWTError
from passlib.context import CryptContext
import datetime
from config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM
)
from fastapi import ( 
        HTTPException, 
        status,
        Depends
    )
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import datetime
from utilities.data_base_connectivity_utils import SingletonDataBaseConnectivitySQLIte
from database_models.users_models import Users

GLOBAL_PWD_HASH = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = AccessTokenGenerator.decode_access_token(token)
    except JWTError:
        raise credentials_exception
    username: str = payload.get("user")
    if username is None:
        raise credentials_exception
        # check for expiration as well
    expiration_time = payload.get("exp")
    current_time = datetime.datetime.timestamp(datetime.datetime.utcnow())
    if expiration_time <= current_time:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired, please login again",
                headers={"WWW-Authenticate": "Bearer"},
            )

    session = SingletonDataBaseConnectivitySQLIte.get_session()
    user = session.query(Users).filter(Users.email == username).first()
    if user is None:
        raise credentials_exception
    return user

class HashingJose:

    def __init__(self):
        self.pwd_context = GLOBAL_PWD_HASH

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    

class AccessTokenGenerator:

    @staticmethod
    def create_access_token(data: dict, 
                            expires_delta: datetime.timedelta = datetime.timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
                            ) -> str:
        to_encode = data.copy()
        expire = datetime.datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_access_token(token) -> dict:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])