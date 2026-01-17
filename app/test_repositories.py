import os
import shutil
from datetime import date

import pytest

from .config import settings
from .models import Car, CarBooking
from .repositories import FileSystemRepository


@pytest.fixture
def repo():
    test_data_dir = os.path.join(settings.data_directory, "test_data")
    yield FileSystemRepository(base_path=test_data_dir)
    shutil.rmtree(test_data_dir)



def test_file_system_flow(repo):
    # Add and retrieve a car
    car = Car(id="testcar1", model="Test Model", seats=4)
    repo.add_car(car)
    cars = repo.get_cars("2024-01-01", "2024-01-10")
    assert any(c.id == "testcar1" for c in cars)

    # Book and check availability
    booking_id = "booking1"
    start_date = date.fromisoformat("2024-01-05")
    end_date = date.fromisoformat("2024-01-07")
    booking = CarBooking(
        id=booking_id,
        car_id="testcar1",
        start_date=start_date,
        end_date=end_date,
    )
    repo.book_car(booking)
    assert not repo.is_car_available("testcar1", date.fromisoformat("2024-01-05"), date.fromisoformat("2024-01-07"))
    assert repo.is_car_available("testcar1", date.fromisoformat("2024-01-08"), date.fromisoformat("2024-01-10"))
