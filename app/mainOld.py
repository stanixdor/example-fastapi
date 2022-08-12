from cgi import test
from os import stat
from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
import secrets

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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

@app.get('/postsOld')
def GetPosts():
    return {'data' : 'this is your post'}

@app.get('/posts')
def GetPosts():
    return {'data' : myPosts}

@app.post('/createpostsOld')
def CreatePost(testData: dict = Body(...)):
    print(testData)
    return {"newPost" : f"title: {testData['title']} content: {testData['content']}"}

#title str, content str
@app.post('/createposts')
def CreatePostOld(post: Post):
    #convert pydantic model to dict
    #newPost.dict()
    print(post.title)
    print(post.published)
    print(post.rating)
    return {"data": post}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def CreatePost(post: Post):
    postDict = post.dict()
    postDict['id'] = secrets.randbelow(1000000)
    myPosts.append(postDict)
    return {"data": postDict}

@app.get('/posts/{id}')
def GetPost(id: int): #checkea si es convertible a int y convierte
    post = FindPost(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    return {"postDetail" : post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def DeletePost(id: int):
    index = FindPostIndex(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    myPosts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def UpdatePost(id: int, post: Post):
    index = FindPostIndex(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    postDict = post.dict()
    postDict['id'] = id
    myPosts[index] = postDict
    print(post)
    return {'data': postDict}