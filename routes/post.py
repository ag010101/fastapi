from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.post import PostCreate, PostUpdate, PostResponse
from services.post_service import (
    create_post_service,
    get_posts_in_community_service,
    get_post_service,
    update_post_service,
    delete_post_service
)

router = APIRouter(prefix="/posts", tags=["Posts"])

#  Create a Post
@router.post("/community/{community_id}/user/{user_id}", response_model=PostResponse)
def create_post(community_id: int, user_id: int, post_data: PostCreate, db: Session = Depends(get_db)):
    return create_post_service(db, community_id, user_id, post_data)


# Get All Posts in a Community
@router.get("/community/{community_id}", response_model=list[PostResponse])
def get_posts_in_community(community_id: int, db: Session = Depends(get_db)):
    return get_posts_in_community_service(db, community_id)


#  Get a Specific Post by ID
@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return get_post_service(db, post_id)


# Update a Post
@router.put("/{post_id}/user/{user_id}", response_model=PostResponse)
def update_post(post_id: int, user_id: int, post_data: PostUpdate, db: Session = Depends(get_db)):
    return update_post_service(db, post_id, user_id, post_data)

# Delete a Post
@router.delete("/{post_id}/user/{user_id}")
def delete_post(post_id: int, user_id: int, db: Session = Depends(get_db)):
    return delete_post_service(db, post_id, user_id)