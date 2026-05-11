import csv
from datetime import date
from Vehicles.car import Car
from Vehicles.motorbike import Motorbike
from Vehicles.truck import Truck
from Users.client import Client
from Users.admin import Admin
from Services.rental import Rental

class CSVHandler:
    def __init__(self):
        pass

    def save_vehicles(self, filename, vehicles):
        fieldnames = [
            "type", "brand", "color", "license_plate",
            "model", "matriculation_date", "mileage"]

        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for vehicle in vehicles:
                writer.writerow(vehicle.to_csv_row())

    def load_vehicles(self, filename):
        vehicles = []

        try:
            with open(filename, newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    vehicle_type = row["type"]
                    matriculation_date = date.fromisoformat(row["matriculation_date"])
                    mileage = float(row["mileage"])

                    if vehicle_type == "Car":
                        vehicle = Car(
                            row["brand"], row["color"], row["license_plate"],
                            row["model"], matriculation_date, mileage)

                    elif vehicle_type == "Motorbike":
                        vehicle = Motorbike(
                            row["brand"], row["color"], row["license_plate"],
                            row["model"], matriculation_date, mileage)

                    elif vehicle_type == "Truck":
                        vehicle = Truck(
                            row["brand"], row["color"], row["license_plate"],
                            row["model"], matriculation_date, mileage)

                    else:
                        continue
                    vehicles.append(vehicle)

        except FileNotFoundError:
            pass
        return vehicles

    def save_clients(self, filename, clients):
        fieldnames = ["type", "name", "date_of_birth", "user_id", "vehicles"]

        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for client in clients:
                writer.writerow(client.to_csv_row())

    def load_clients(self, filename, vehicles):
        clients = []

        try:
            with open(filename, newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    client = Client(
                        row["name"],
                        date.fromisoformat(row["date_of_birth"]),
                        row["user_id"])

                    if row.get("vehicles"):
                        for plate in row["vehicles"].split(";"):
                            plate = plate.strip().upper()

                            for vehicle in vehicles:
                                if vehicle.license_plate == plate:
                                    client.add_vehicle(vehicle)
                    clients.append(client)

        except FileNotFoundError:
            pass
        return clients

    def save_workers(self, filename, workers):
        fieldnames = ["type", "name", "date_of_birth", "user_id", "role"]

        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for worker in workers:
                writer.writerow(worker.to_csv_row())

    def load_workers(self, filename):
        workers = []

        try:
            with open(filename, newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    worker = Admin(
                        row["name"],
                        date.fromisoformat(row["date_of_birth"]),
                        row["user_id"],
                        row["role"])

                    workers.append(worker)

        except FileNotFoundError:
            pass

        return workers

    def save_rentals(self, filename, rentals):
        fieldnames = [
            "vehicle_plate", "client_id", "start_date",
            "end_date", "kms_allowed", "kms_done", "insurance_type"]

        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for rental in rentals:
                writer.writerow(rental.to_csv_row())

    def load_rentals(self, filename, vehicles, clients):
        rentals = []

        try:
            with open(filename, newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    vehicle = None
                    client = None

                    for v in vehicles:
                        if v.license_plate == row["vehicle_plate"].strip().upper():
                            vehicle = v
                            break

                    for c in clients:
                        if c.user_id == row["client_id"].strip():
                            client = c
                            break

                    if vehicle is not None and client is not None:
                        rental = Rental(
                            vehicle,
                            client,
                            date.fromisoformat(row["start_date"]),
                            date.fromisoformat(row["end_date"]),
                            float(row["kms_allowed"]),
                            row["insurance_type"])

                        rental.set_kms_done_from_csv(float(row["kms_done"]))
                        rentals.append(rental)

        except FileNotFoundError:
            pass
        return rentals

