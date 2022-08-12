from os import stat
from .. import models, schemas, oauth2
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from typing import List, Optional

from app import database

router = APIRouter(prefix='/vote', tags=['Vote'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def Vote(vote: schemas.Vote, db: Session = Depends(database.get_db), currentUser = Depends(oauth2.GetCurrentUser)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {vote.post_id} does not exist')

    voteQuery = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == currentUser.id)
    foundVote = voteQuery.first()
    if vote.dir == 1:
        if foundVote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {currentUser.id} has already voted on post {vote.post_id}')
        newVote = models.Vote(post_id = vote.post_id, user_id = currentUser.id)
        db.add(newVote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not foundVote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exist')
        voteQuery.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}