from datetime import date

from pydantic import BaseModel


class Car(BaseModel):
    id: str
    model: str
    seats: int

class CarBooking(BaseModel):
    id: str
    car_id: str
    start_date: date
    end_date: date
