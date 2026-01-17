import json
from time import monotonic_ns
from typing import Annotated

from fastapi import FastAPI, Query, Response
from fastapi.responses import StreamingResponse

from datetime import date

from .models import CarBooking
from .repositories import BaseRepository

app = FastAPI()


@app.get("/")
async def availability(start_date: Annotated[date, Query()], end_date: Annotated[date, Query()]):
    def iterResponse():
        yield '['
        is_first = True
        for car in BaseRepository.repo().get_cars(start_date, end_date):
            if not is_first:
                yield ','
            else:
                is_first = False
            yield json.dumps(car.model_dump())
        yield ']'
    return StreamingResponse(iterResponse(), media_type="application/json")


@app.post("/{car_id}", responses={409: {"description": "Car not available"}})
async def book(car_id: str, start_date: Annotated[date, Query()], end_date: Annotated[date, Query()], response: Response):
    if not BaseRepository.repo().is_car_available(car_id, start_date, end_date):
        response.status_code = 409
        return { "error": "Car not available for the selected dates." }

    booking = CarBooking(
        id=str(monotonic_ns()),
        car_id=car_id,
        start_date=start_date,
        end_date=end_date,
    )
    BaseRepository.repo().book_car(booking)
    return { "booking_id": booking.id }
