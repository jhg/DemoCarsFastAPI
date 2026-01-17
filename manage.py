#!/usr/bin/env python3
import os
import sys

from app.models import Car
from app.repositories import FileSystemRepository

data_directory = os.path.abspath("./data")
os.environ.setdefault("DATA_DIRECTORY", data_directory)

if __name__ == "__main__":
    if len(sys.argv) != 5 or sys.argv[1] != "add":
        print("Usage: manage.py add <car_id> <car_model> <car_seats>")
        sys.exit(1)

    _, command, car_id, car_model, car_seats = sys.argv

    if command == "add":
        repo = FileSystemRepository(base_path="./data")
        car = Car(id=car_id, model=car_model, seats=int(car_seats))
        repo.add_car(car)
        print(f"Car {car_id} added successfully.")
    else:
        print("Unknown command.")
        sys.exit(1)
