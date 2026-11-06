from datetime import datetime, timedelta

from sqlalchemy import and_, delete, select

from database import SessionLocal
from models import Base, Booking, Hall, Seat, Show, Status, User


def seed():
    db = SessionLocal()
    
    db.execute(delete(Booking))
    db.execute(delete(Hall))
    db.execute(delete(Seat))
    db.execute(delete(Show))
    db.execute(delete(User))
    
    db.commit()
    

    user = User(name='Admin', surname='Admin', email="admin@cinema.ru", password="password123")
    db.add(user) 
    db.commit()

    hall = Hall(
        number=1,
        rows_count=10,
        seats_per_row=10
    )
    db.add(hall)
    db.commit()
    

    seats_to_add = []
    for row in range(1, hall.rows_count + 1):
        for number in range(1, hall.seats_per_row + 1):
            seats_to_add.append(
                Seat(
                    hall_id=hall.id,
                    row=row,
                    number=number,
                    is_booked=False
                )
            )
    db.add_all(seats_to_add)
    db.commit()


    show = Show(
        film_title="Чебурашка (Повторный прокат)",
        hall_id=hall.id,
        start_time=datetime.now() + timedelta(days=1, hours=19) # Завтра в 19:00
    )
    db.add(show)
    db.commit()


    seat_a1 = db.execute(select(Seat).where(and_(Seat.hall_id == hall.id, Seat.row == 1, Seat.number == 1))).scalars().first()
    seat_a2 = db.execute(select(Seat).where(and_(Seat.hall_id == hall.id, Seat.row == 1, Seat.number == 2))).scalars().first()

    if seat_a1 and seat_a2:
        seat_a1.is_booked = True
        seat_a2.is_booked = True
        
        booking1 = Booking(
            show_id=show.id,
            seat_id=seat_a1.id,
            user_id=user.id,
            status=Status.confirmed
        )
        booking2 = Booking(
            show_id=show.id,
            seat_id=seat_a2.id,
            user_id=user.id,
            status=Status.confirmed
        )
        db.add(booking1)
        db.add(booking2)

    db.commit()
    db.close()
    
    
seed()