from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.booking import BookingResponse, BookingUpdate
from services.booking_service import (
    create_booking, get_booking, get_user_bookings, update_booking, delete_booking
)

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/{user_id}/{session_id}", response_model=BookingResponse)
def create_booking_route(user_id: int, session_id: int, db: Session = Depends(get_db)):
    """
    API Endpoint to create a new booking.
    Accepts `user_id` and `session_id` as route parameters.
    """
    return create_booking(db, user_id, session_id)

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking_route(booking_id: int, db: Session = Depends(get_db)):
    """
    API Endpoint to get a booking by ID.
    """
    return get_booking(db, booking_id)

@router.get("/user/{user_id}", response_model=list[BookingResponse])
def get_user_bookings_route(user_id: int, db: Session = Depends(get_db)):
    """
    API Endpoint to get all bookings for a user.
    """
    return get_user_bookings(db, user_id)

@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking_route(booking_id: int, booking_data: BookingUpdate, db: Session = Depends(get_db)):
    """
    API Endpoint to update a booking status.
    """
    return update_booking(db, booking_id, booking_data)

@router.delete("/{booking_id}")
def delete_booking_route(booking_id: int, db: Session = Depends(get_db)):
    """
    API Endpoint to delete a booking.
    """
    return delete_booking(db, booking_id)