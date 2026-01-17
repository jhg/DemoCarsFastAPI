import json
from time import monotonic_ns
from typing import Annotated

from fastapi import FastAPI, Query, Response
from fastapi.responses import StreamingResponse

from datetime import date

from .models import CarBooking
from .repositories import BaseRepository

import logging

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def availability(start_date: Annotated[date, Query()], end_date: Annotated[date, Query()]):
    def iter_response():
        logger.debug(f"Streaming available cars from {start_date} to {end_date}.")
        yield '['
        is_first = True
        for car in BaseRepository.repo().get_cars(start_date, end_date):
            if not is_first:
                yield ','
            else:
                is_first = False
            yield json.dumps(car.model_dump())
        yield ']'
    return StreamingResponse(iter_response(), media_type="application/json")


@app.post("/{car_id}", responses={409: {"description": "Car not available"}, 404: {"description": "Car does not exist"}})
async def book(car_id: str, start_date: Annotated[date, Query()], end_date: Annotated[date, Query()], response: Response):
    if not BaseRepository.repo().exists_car(car_id):
        response.status_code = 404
        logger.warning(f"Booking failed: Car {car_id} does not exist.")
        return { "error": "Car does not exist." }

    if not BaseRepository.repo().is_car_available(car_id, start_date, end_date):
        response.status_code = 409
        logger.warning(f"Booking {car_id} not available from {start_date} to {end_date}.")
        return { "error": "Car not available for the selected dates, maybe it was just booked." }

    booking = CarBooking(
        id=str(monotonic_ns()),
        car_id=car_id,
        start_date=start_date,
        end_date=end_date,
    )
    BaseRepository.repo().book_car(booking)
    logger.info(f"Car {car_id} booked successfully from {start_date} to {end_date} with booking ID {booking.id}.")
    return { "booking_id": booking.id }
