from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Status(PyEnum):
    confirmed = 'confirmed'
    expired = 'expired'


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    surname: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    

class Hall(Base):
    __tablename__ = 'halls'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(unique=True, nullable=False)
    rows_count: Mapped[int] = mapped_column(nullable=False)
    seats_per_row: Mapped[int] = mapped_column(nullable=False)
    

class Seat(Base):
    __tablename__ = 'seats'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    hall_id: Mapped[int] = mapped_column(ForeignKey('halls.id'), nullable=False)
    row: Mapped[int] = mapped_column(nullable=False)
    number: Mapped[int] = mapped_column(nullable=False)
    is_booked: Mapped[bool] = mapped_column(default=False)
    

class Show(Base):
    __tablename__ = 'shows'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    film_title: Mapped[str] = mapped_column(String(255), nullable=False)
    hall_id: Mapped[int] = mapped_column(ForeignKey('halls.id'), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    

class Booking(Base):
    __tablename__ = 'booking'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    show_id: Mapped[int] = mapped_column(ForeignKey('shows.id'), nullable=False)
    seat_id: Mapped[int] = mapped_column(ForeignKey('seats.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status))
    
    
    
    
    
    
    