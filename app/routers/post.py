from pyexpat import model
from .. import models, schemas, oauth2
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. database import get_db
from typing import List, Optional

router = APIRouter(prefix='/posts', tags=['Posts'])

#@router.get('/', response_model=List[schemas.PostResponse])
@router.get('/', response_model=List[schemas.PostVote])
def GetPosts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #models.Post es la tabla en este caso
    #posts = db.query(models.Post).all()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, 
    isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
                                                                        #porque cojones ha puesto que sea int xd
def CreatePost(post: schemas.PostCreate, db: Session = Depends(get_db), currentUser = Depends(oauth2.GetCurrentUser)):
    #newPost = models.Post(title=post.title, content=post.content, published=post.published)
    newPost = models.Post(owner_id=currentUser.id, **post.dict())
    db.add(newPost)
    db.commit()
    #refresh recibe la respuesta de la base de datos
    db.refresh(newPost)
    return newPost


#@router.get('/{id}', response_model=schemas.PostResponse)
@router.get('/{id}', response_model=schemas.PostVote)
def GetPost(id: int, db: Session = Depends(get_db)):

    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, 
    isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def DeletePost(id: int, db: Session = Depends(get_db), currentUser = Depends(oauth2.GetCurrentUser)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)

    post = postQuery.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')

    if post.owner_id != currentUser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')

    postQuery.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.PostResponse)
def UpdatePost(id: int, updatedPost: schemas.PostCreate, db: Session = Depends(get_db), currentUser = Depends(oauth2.GetCurrentUser)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    post = postQuery.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')

    if post.owner_id != currentUser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')
    
    postQuery.update(updatedPost.dict(),synchronize_session=False)
    db.commit()
    return postQuery.first()