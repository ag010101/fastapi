from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.program import ProgramCreate, ProgramResponse
from services.program_service import (
    create_program, get_programs, get_program_by_id, update_program, delete_program
)

router = APIRouter(prefix="/programs", tags=["Programs"])

# Create a new program
@router.post("/{user_id}/create", response_model=ProgramResponse)
def create_new_program(user_id:int,program_data: ProgramCreate, db: Session = Depends(get_db)):
    return create_program(db,user_id, program_data)

# Get all programs
@router.get("/", response_model=list[ProgramResponse])
def list_programs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_programs(db, skip, limit)

# Get a single program by ID
@router.get("/{program_id}", response_model=ProgramResponse)
def read_program(program_id: int, db: Session = Depends(get_db)):
    program = get_program_by_id(db, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program

# Update a program
@router.put("/{program_id}", response_model=ProgramResponse)
def update_existing_program(program_id: int, updated_data: ProgramCreate, db: Session = Depends(get_db)):
    program = update_program(db, program_id, updated_data)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program

# Delete a program
@router.delete("/{program_id}")
def remove_program(program_id: int, db: Session = Depends(get_db)):
    success = delete_program(db, program_id)
    if not success:
        raise HTTPException(status_code=404, detail="Program not found")
    return {"message": "Program deleted successfully"}
