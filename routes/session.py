from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.session import SessionCreate, SessionResponse
from services.session_service import (
    create_session, get_sessions, get_session_by_id, update_session, delete_session
)

router = APIRouter(prefix="/sessions", tags=["Sessions"])

# Create a new session (user_id is provided as a path parameter)
@router.post("/{user_id}/{program_id}/create", response_model=SessionResponse)
def create_new_session(user_id: int,program_id:int, session_data: SessionCreate, db: Session = Depends(get_db)):
    return create_session(db,program_id, user_id, session_data)

# Get all sessions
@router.get("/", response_model=list[SessionResponse])
def list_sessions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_sessions(db, skip, limit)

# Get a single session by ID
@router.get("/{program_id}/{session_id}", response_model=SessionResponse)
def read_session(program_id: int, session_id: int, db: Session = Depends(get_db)):
    session = get_session_by_id(db, program_id, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

# Update a session
@router.put("/{program_id}/{session_id}", response_model=SessionResponse)
def update_existing_session(program_id: int, session_id: int, updated_data: SessionCreate, db: Session = Depends(get_db)):
    session = update_session(db, program_id, session_id, updated_data)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.delete("/{program_id}/{session_id}")
def remove_session(program_id: int, session_id: int, db: Session = Depends(get_db)):
    success = delete_session(db, program_id, session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}
