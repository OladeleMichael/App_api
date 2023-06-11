from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from .import models
from .database import engine
from .routers import post, user, auth , vote
from .config import Settings
 
#command for sql alchemy to run the create statement for all tables
models.Base.metadata.create_all(bind=engine) 

#check http://127.0.0.1:8000/docs#/ or http://127.0.0.1:8000/redoc for the api documentation

app = FastAPI()

#change origins to deployed app domain
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


my_posts = []

# #function to find post in my_posts varible
# def find_post_by_id(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# #Function to find post by indexed id 
# def find_index_post(id):
#     for i, p in enumerate (my_posts):
#         if p ['id']==id:
#             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

  
#root
@app.get("/")
async def root():
    return {"message": "Welcome to my world"}



