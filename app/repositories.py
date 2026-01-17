import os
from datetime import date

from filelock import FileLock

from app.config import settings
from app.models import Car, CarBooking

import logging


logger = logging.getLogger(__name__)


class BaseRepository:
    """
    Base repository interface for car rental operations.
    """

    def add_car(self, car: Car):
        logger.error("add_car method not implemented.")
        raise NotImplementedError("Subclasses must implement this method")

    def is_car_available(self, car_id: str, start_date: date, end_date: date) -> bool:
        logger.error("is_car_available method not implemented.")
        raise NotImplementedError("Subclasses must implement this method")

    def exists_car(self, car_id: str) -> bool:
        logger.error("exists_car method not implemented.")
        raise NotImplementedError("Subclasses must implement this method")

    def get_cars(self, start_date: date, end_date: date):
        logger.error("get_cars method not implemented.")
        raise NotImplementedError("Subclasses must implement this method")

    def book_car(self, booking: CarBooking):
        logger.error("book_car method not implemented.")
        raise NotImplementedError("Subclasses must implement this method")

    @classmethod
    def repo(cls) -> BaseRepository:
        logger.info("Creating FileSystemRepository instance.")
        return FileSystemRepository(base_path=settings.data_directory)


class FileSystemRepository(BaseRepository):
    """
    A repository that uses the file system to store and retrieve car data like:

    - /cars/{car_id}/info.json
    - /cars/{car_id}/bookings/{booking_id}.json

    The info.json contains car details and each booking file contains booking details.

    For write operations a lockfile is used before to read/write data to mitigate race conditions.
    But it is not used when only reading data to keep it simple and fast, as often it is written
    more often than read.
    """

    def __init__(self, base_path: str):
        self.base_path = base_path
        cars_dir = os.path.join(self.base_path, "cars")
        os.makedirs(cars_dir, exist_ok=True)

    def _car_lock_path(self, car_id: str) -> str:
        return os.path.join(self.base_path, "cars", car_id, 'lock')

    def add_car(self, car: Car):
        with FileLock(self._car_lock_path(car.id)):
            car_dir = os.path.join(self.base_path, "cars", car.id)
            os.makedirs(car_dir, exist_ok=True)
            info_file = os.path.join(self.base_path, "cars", car.id, "info.json")
            with open(info_file, "w") as f:
                f.write(car.model_dump_json())
                logger.info(f"Car {car.id} added with info: {car.model_dump_json()}")

    def is_car_available(self, car_id: str, start_date: date, end_date: date) -> bool:
        car_dir = os.path.join(self.base_path, "cars", car_id)
        bookings_dir = os.path.join(car_dir, "bookings")
        if not os.path.exists(bookings_dir):
            return True

        for booking_file in os.listdir(bookings_dir):
            with open(os.path.join(bookings_dir, booking_file), "r") as bf:
                booking_info = CarBooking.model_validate_json(bf.read())
                if not (end_date < booking_info.start_date or start_date > booking_info.end_date):
                    return False  # overlapping booking found
        # This is not optimal, a reverse index would be better for performance,
        # but for that the simplest way is to use a database instead of this.
        return True

    def exists_car(self, car_id: str) -> bool:
        car_dir = os.path.join(self.base_path, "cars", car_id)
        return os.path.isdir(car_dir)

    def get_cars(self, start_date: date, end_date: date):
        cars_path = os.path.join(self.base_path, "cars")
        for car_id in os.listdir(cars_path):
            car_dir = os.path.join(cars_path, car_id)
            if not os.path.isdir(car_dir):
                logger.warning(f"Car {car_id} is a file instead of a directory, skipping.")
                continue
            info_file = os.path.join(car_dir, "info.json")
            with open(info_file, "r") as f:
                car = Car.model_validate_json(f.read())
            if self.is_car_available(car.id, start_date, end_date):
                yield car

    def book_car(self, booking: CarBooking):
        with FileLock(self._car_lock_path(booking.car_id)):
            if not self.is_car_available(booking.car_id, booking.start_date, booking.end_date):
                logger.error(f"Car {booking.car_id} is not available for booking from {booking.start_date} to {booking.end_date}.")
                raise Exception("Car is not available for the selected dates")

            car_dir = os.path.join(self.base_path, "cars", booking.car_id)
            bookings_dir = os.path.join(car_dir, "bookings")
            os.makedirs(bookings_dir, exist_ok=True)

            booking_file = os.path.join(bookings_dir, f"{booking.id}.json")
            with open(booking_file, "w") as f:
                f.write(booking.model_dump_json())
                logger.info(f"Booking {booking.id} created for car {booking.car_id} from {booking.start_date} to {booking.end_date}.")
