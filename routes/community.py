from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.community import CommunityCreate, CommunityResponse
from services.community_service import (
    create_community, get_communities, get_community_by_id, update_community, delete_community,
    add_user_to_community, remove_user_from_community
)

router = APIRouter(prefix="/communities", tags=["Communities"])

#  Create a new community (User ID as a param)
@router.post("/{user_id}", response_model=CommunityResponse)
def create_new_community(user_id: int, community_data: CommunityCreate, db: Session = Depends(get_db)):
    return create_community(db, user_id, community_data)

#  Get all communities
@router.get("/", response_model=list[CommunityResponse])
def list_communities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_communities(db, skip, limit)

#  Get a single community by ID
@router.get("/{community_id}", response_model=CommunityResponse)
def read_community(community_id: int, db: Session = Depends(get_db)):
    community = get_community_by_id(db, community_id)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    return community

#  Update a community
@router.put("/{community_id}", response_model=CommunityResponse)
def update_existing_community(community_id: int, updated_data: CommunityCreate, db: Session = Depends(get_db)):
    community = update_community(db, community_id, updated_data)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    return community

#  Delete a community
@router.delete("/{community_id}")
def remove_community(community_id: int, db: Session = Depends(get_db)):
    success = delete_community(db, community_id)
    if not success:
        raise HTTPException(status_code=404, detail="Community not found")
    return {"message": "Community deleted successfully"}

#  Add user to a community
@router.post("/{community_id}/users/{user_id}")
def join_community(community_id: int, user_id: int, db: Session = Depends(get_db)):
    success = add_user_to_community(db, community_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="User already in the community or community not found")
    return {"message": "User added to community successfully"}

#  Remove user from a community
@router.delete("/{community_id}/users/{user_id}")
def leave_community(community_id: int, user_id: int, db: Session = Depends(get_db)):
    success = remove_user_from_community(db, community_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="User not in the community or community not found")
    return {"message": "User removed from community successfully"}