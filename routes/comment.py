from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.comments import CommentCreate, CommentUpdate, CommentResponse
from services.comment_service import (
    create_comment_service,
    get_comments_in_post_service,
    get_comment_service,
    update_comment_service,
    delete_comment_service
)

router = APIRouter(prefix="/comments", tags=["Comments"])

#  Create a Comment
@router.post("/post/{post_id}/user/{user_id}", response_model=CommentResponse)
def create_comment(post_id: int, user_id: int, comment_data: CommentCreate, db: Session = Depends(get_db)):
    return create_comment_service(db, post_id, user_id, comment_data)


#  Get All Comments in a Post
@router.get("/post/{post_id}", response_model=list[CommentResponse])
def get_comments_in_post(post_id: int, db: Session = Depends(get_db)):
    return get_comments_in_post_service(db, post_id)


# Get a Specific Comment by ID
@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    return get_comment_service(db, comment_id)


# Update a Comment
@router.put("/{comment_id}/user/{user_id}", response_model=CommentResponse)
def update_comment(comment_id: int, user_id: int, comment_data: CommentUpdate, db: Session = Depends(get_db)):
    return update_comment_service(db, comment_id, user_id, comment_data)

# Delete a Comment
@router.delete("/{comment_id}/user/{user_id}")
def delete_comment(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    return delete_comment_service(db, comment_id, user_id)
