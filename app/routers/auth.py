from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. database import get_db


router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def Login(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    #username = 
    #password =
    user = db.query(models.User).filter(models.User.email == userCredentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')

    if not utils.Verify(userCredentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')

    #create token
    accesToken = oauth2.createAccessToken(data= {"userID": user.id})
    #return token
    return {"accessToken": accesToken, "tokenType": "bearer"}