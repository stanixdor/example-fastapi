from calendar import c
from cgi import test
from os import stat
from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
import secrets
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='aritz1997', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database conecction was succesfull')
        break
    except Exception as error:
        print('Connecting to database failed')
        print("Error: ", error)
        time.sleep(2)

myPosts = [{"title" : "title1", "content" : "content1", "id" : 1}]


def FindPost(id):
    for p in myPosts:
        if p['id'] == id:
            return p

def FindPostIndex(id):
    for i, p in enumerate(myPosts):
        if p['id'] == id:
            return i


@app.get("/")
def Root():
    return {"message": "Best APIzzz"}


@app.get('/posts')
def GetPosts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {'data' : posts}



@app.post('/posts', status_code=status.HTTP_201_CREATED)
def CreatePost(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    newPost = cursor.fetchone()
    conn.commit()
    return {"data": newPost}


@app.get('/posts/{id}')
def GetPost(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    return {"postDetail" : post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def DeletePost(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deletedPost = cursor.fetchone()
    conn.commit()
    if deletedPost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def UpdatePost(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING*""", (post.title,post.content,post.published, str(id)))
    updatedPost = cursor.fetchone()
    conn.commit()
    if updatedPost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
   
    return {'data': updatedPost}