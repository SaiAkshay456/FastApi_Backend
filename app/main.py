from fastapi import FastAPI,HTTPException
from app.schema import User,Post
app=FastAPI() 

myTextPost = {
    1: {"title": "First Post", "content": "This is my first post content"},
    2: {"title": "Second Post", "content": "This is my second post content"},
    3: {"title": "Third Post", "content": "This is my third post content"},
    4: {"title": "Fourth Post", "content": "This is my fourth post content"},
    5: {"title": "Fifth Post", "content": "This is my fifth post content"},
    6: {"title": "Sixth Post", "content": "This is my sixth post content"},
    7: {"title": "Seventh Post", "content": "This is my seventh post content"},
    8: {"title": "Eighth Post", "content": "This is my eighth post content"},
    9: {"title": "Ninth Post", "content": "This is my ninth post content"},
    10: {"title": "Tenth Post", "content": "This is my tenth post content"},
    11: {"title": "Eleventh Post", "content": "This is my eleventh post content"},
    12: {"title": "Twelfth Post", "content": "This is my twelfth post content"},
    13: {"title": "Thirteenth Post", "content": "This is my thirteenth post content"},
    14: {"title": "Fourteenth Post", "content": "This is my fourteenth post content"},
    15: {"title": "Fifteenth Post", "content": "This is my fifteenth post content"}
}

@app.get("/")
def root():
    return f'Server running at port 8080'

@app.get("/hii")
def hii():
    return {"message":"Hii from fastapi"}

@app.get("/get-all")
def get_all_posts(limitNo:int=None):
    if(limitNo and limitNo>0):
        return dict(list(myTextPost.items())[:limitNo])
    return myTextPost

@app.get("/get-post/{id}")
def getPost(id:int):
    if id not in myTextPost:
        raise HTTPException(status_code=404,detail="Post not does not exist")
    return myTextPost.get(id)

@app.post("/create/post")
def createPost(post:Post):
    myTextPost[post.id]={"title":post.title,"content":post.content}
    return myTextPost[post.id]