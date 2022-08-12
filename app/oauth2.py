from fastapi import Depends, Security, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import schemas, database, models
from .config import settings

oauth2Scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#Algorithm
#Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCES_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def createAccessToken(data: dict):
    toEnconde = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    toEnconde.update({"exp": expire})

    encodedJwt = jwt.encode(toEnconde, SECRET_KEY, algorithm=ALGORITHM)

    return encodedJwt

def VerifyAccessToken(token: str, credentialsException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('userID')
        if id is None:
            raise credentialsException
        tokenData = schemas.TokenData(id=id)
    except JWTError:
        raise credentialsException

    return tokenData

def GetCurrentUser(token: str = Depends(oauth2Scheme), db: Session = Depends(database.get_db)):
    credentialsException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials', headers={"WWW-Authenticate": "Brearer"})

    token = VerifyAccessToken(token, credentialsException)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
    #return VerifyAccessToken(token, credentialsException)