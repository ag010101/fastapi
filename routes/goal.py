from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from services.goal_service import (
    create_goal_service,
    get_goals_service,
    get_goal_service,
    update_goal_service,
    delete_goal_service
)

router = APIRouter(prefix="/goals", tags=["Goals"])

# Create a Goal
@router.post("/user/{user_id}", response_model=GoalResponse)
def create_goal(user_id: int, goal_data: GoalCreate, db: Session = Depends(get_db)):
    return create_goal_service(db, user_id, goal_data)

# Get All Goals for a User
@router.get("/user/{user_id}", response_model=list[GoalResponse])
def get_goals(user_id: int, db: Session = Depends(get_db)):
    return get_goals_service(db, user_id)

# Get a Specific Goal
@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    return get_goal_service(db, goal_id)

# Update a Goal
@router.put("/{goal_id}/user/{user_id}", response_model=GoalResponse)
def update_goal(goal_id: int, user_id: int, goal_data: GoalUpdate, db: Session = Depends(get_db)):
    return update_goal_service(db, goal_id, user_id, goal_data)

# Delete a Goal
@router.delete("/{goal_id}/user/{user_id}")
def delete_goal(goal_id: int, user_id: int, db: Session = Depends(get_db)):
    return delete_goal_service(db, goal_id, user_id)