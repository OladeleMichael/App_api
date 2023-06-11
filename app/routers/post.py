from fastapi import FastAPI, Response, Request, status, HTTPException,Depends, APIRouter
from typing  import List, Optional
from ..import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi_responseschema import AbstractResponseSchema, SchemaAPIRoute, wrap_app_responses


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#Return new post as a dictionary by adding dict to the response (this is a good way to get a stuctured response from the server)
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    print (current_user.email)
    new_post = models.Post(owner_id=current_user.id , **post.dict()) # another way to do this is (title= post.title, content= post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post # this is the response  returned to the client on success.


    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #(post.title,post.content, post.published))
   # new_post =cursor.fetchone()

    #conn.commit()
   
    #return {"data": new_post} # this is the response  returned to the client on success.

#gets post with specific id using find_post function
@router.get("/{id}" , response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found")

#use the below if statement if you want post to be only visible to the logged in user - Like a notepad app
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    
    #print (post.owner_id)
    return post

    #def get_post(id: int, response: Response):
    #cursor.execute( """select * FROM posts WHERE id = %s """, (str(id),))
   # post = cursor.fetchone()
    #print (post)


#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user),limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()    
    
    #use below code if you want only the logged in user to fetch specific posts created by the user.
    # filter(
    #     models.Post.owner_id== current_user.id).all()
    #print(limit)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results)
    return posts

#regular sql expression below
    #cursor.execute( """select * FROM posts """)
    #posts= cursor.fetchall()
    #print (posts)
    

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post=post_query.first()
    #cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    #deleting post
    #find teh index in the array{my_posts} that has the required ID
    if post == None:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")

    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}", response_model=schemas.Post)
def update_post (id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    #cursor.execute( """UPDATE posts SET title = %s, content = %s , published = %s WHERE id = %s returning * """,
    #(post.title,post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #print(updated_post)
    
    
    if post == None:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()

    return post_query.first()
