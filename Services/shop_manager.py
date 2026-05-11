from Data.csv_handler import CSVHandler
from Services.rental import Rental
from Vehicles.vehicle import Vehicle
from Vehicles.car import Car
from Vehicles.motorbike import Motorbike
from Vehicles.truck import Truck
from Users.client import Client
from Users.admin import Admin
from Exceptions.exceptions import(
    DuplicateLicensePlateError,
    DuplicateIDError,
    VehicleNotFoundError,
    UserNotFoundError,
    RentalNotFoundError,
    VehicleAlreadyRentedError)


class ShopManager:
    VEHICLES_CSV = "vehicles.csv"
    CLIENTS_CSV = "clients.csv"
    WORKERS_CSV = "workers.csv"
    RENTALS_CSV = "rentals.csv"

    def __init__(self):
        self.__csv_handler = CSVHandler()

        self.__vehicles = self.__csv_handler.load_vehicles(self.VEHICLES_CSV)
        self.__clients = self.__csv_handler.load_clients(
            self.CLIENTS_CSV,
            self.__vehicles)
        self.__workers = self.__csv_handler.load_workers(self.WORKERS_CSV)
        self.__rentals = self.__csv_handler.load_rentals(
            self.RENTALS_CSV,
            self.__vehicles,
            self.__clients)

    def save_all(self):
        self.save_vehicles()
        self.save_clients()
        self.save_workers()
        self.save_rentals()

    def save_vehicles(self):
        self.__csv_handler.save_vehicles(self.VEHICLES_CSV, self.__vehicles)

    def save_clients(self):
        self.__csv_handler.save_clients(self.CLIENTS_CSV, self.__clients)

    def save_workers(self):
        self.__csv_handler.save_workers(self.WORKERS_CSV, self.__workers)

    def save_rentals(self):
        self.__csv_handler.save_rentals(self.RENTALS_CSV, self.__rentals)

    def _normalise_plate(self, plate):
        return plate.upper().strip()

    def _normalise_id(self, user_id):
        return str(user_id).strip()

    def _find_vehicle_by_plate(self, plate):
        plate = self._normalise_plate(plate)

        for vehicle in self.__vehicles:
            if vehicle.license_plate == plate:
                return vehicle
        return None

    def _find_client_by_id(self, user_id):
        user_id = self._normalise_id(user_id)

        for client in self.__clients:
            if client.user_id == user_id:
                return client
        return None

    def _find_worker_by_id(self, user_id):
        user_id = self._normalise_id(user_id)

        for worker in self.__workers:
            if worker.user_id == user_id:
                return worker
        return None

    def _user_id_exists(self, user_id):
        return (
            self._find_client_by_id(user_id) is not None
            or self._find_worker_by_id(user_id) is not None)

    def _rental_periods_overlap(self, start1, end1, start2, end2):
        return start1 <= end2 and start2 <= end1

    def add_vehicle(
        self,
        vehicle_or_type,
        brand=None,
        color=None,
        plate=None,
        model=None,
        matriculation_date=None,
        mileage=None):
        if isinstance(vehicle_or_type, Vehicle):
            vehicle = vehicle_or_type

        else:
            vehicle_type = vehicle_or_type

            if vehicle_type == "1":
                vehicle = Car(
                    brand,
                    color,
                    plate,
                    model,
                    matriculation_date,
                    mileage)

            elif vehicle_type == "2":
                vehicle = Motorbike(
                    brand,
                    color,
                    plate,
                    model,
                    matriculation_date,
                    mileage)

            elif vehicle_type == "3":
                vehicle = Truck(
                    brand,
                    color,
                    plate,
                    model,
                    matriculation_date,
                    mileage)

            else:
                raise ValueError("Invalid vehicle type. Please choose 1, 2 or 3.")

        if self._find_vehicle_by_plate(vehicle.license_plate) is not None:
            raise DuplicateLicensePlateError(
                f"A vehicle with plate '{vehicle.license_plate}' already exists.")

        self.__vehicles.append(vehicle)
        self.save_vehicles()

    def remove_vehicle(self, plate):
        vehicle = self.get_vehicle(plate)

        for rental in self.__rentals:
            if (
                rental.vehicle.license_plate == vehicle.license_plate
                and not rental.is_finished()):
                raise VehicleAlreadyRentedError(f"Cannot remove vehicle '{plate}' because it has an active or upcoming rental.")

        for client in self.__clients:
            try:
                client.remove_vehicle(vehicle.license_plate)
            except Exception:
                pass

        self.__vehicles.remove(vehicle)
        self.save_all()

    def get_vehicle(self, plate):
        vehicle = self._find_vehicle_by_plate(plate)

        if vehicle is None:
            raise VehicleNotFoundError(f"No vehicle with plate '{plate}' found.")
        return vehicle

    def get_all_vehicles(self):
        return list(self.__vehicles)

    def update_vehicle_color(self, plate, new_color):
        vehicle = self.get_vehicle(plate)
        vehicle.update_color(new_color)
        self.save_vehicles()

    def update_vehicle_mileage(self, plate, new_mileage):
        vehicle = self.get_vehicle(plate)
        vehicle.update_mileage(new_mileage)
        self.save_vehicles()

    def check_vehicle_itv(self, plate):
        vehicle = self.get_vehicle(plate)
        return vehicle.next_itv()

    def check_vehicle_maintenance(self, plate):
        vehicle = self.get_vehicle(plate)
        return vehicle.next_maintenance()

    def add_client(self, client_or_name, date_of_birth=None, user_id=None):
        if isinstance(client_or_name, Client):
            client = client_or_name
        else:
            client = Client(client_or_name, date_of_birth, user_id)

        if self._user_id_exists(client.user_id):
            raise DuplicateIDError(
                f"A user with ID '{client.user_id}' already exists.")

        self.__clients.append(client)
        self.save_clients()

    def remove_client(self, user_id):
        client = self.get_client(user_id)
        for rental in self.__rentals:
            if (
                rental.client.user_id == client.user_id
                and not rental.is_finished()):
                raise VehicleAlreadyRentedError(f"Cannot remove client '{user_id}' because they have an active or upcoming rental.")
        self.__clients.remove(client)
        self.save_clients()

    def get_client(self, user_id):
        client = self._find_client_by_id(user_id)

        if client is None:
            raise UserNotFoundError(f"No client with ID '{user_id}' found.")
        return client

    def get_all_clients(self):
        return list(self.__clients)

    def update_client_name(self, user_id, new_name):
        client = self.get_client(user_id)
        client.update_name(new_name)
        self.save_clients()


    def add_worker(self, worker_or_name, date_of_birth=None, user_id=None, role=None):
        if isinstance(worker_or_name, Admin):
            worker = worker_or_name
        else:
            worker = Admin(worker_or_name, date_of_birth, user_id, role)

        if self._user_id_exists(worker.user_id):
            raise DuplicateIDError(f"A user with ID '{worker.user_id}' already exists.")

        self.__workers.append(worker)
        self.save_workers()

    def remove_worker(self, user_id):
        worker = self.get_worker(user_id)
        self.__workers.remove(worker)
        self.save_workers()

    def get_worker(self, user_id):
        worker = self._find_worker_by_id(user_id)

        if worker is None:
            raise UserNotFoundError(f"No worker with ID '{user_id}' found.")
        return worker

    def get_all_workers(self):
        return list(self.__workers)

    def update_worker_role(self, user_id, new_role):
        worker = self.get_worker(user_id)
        worker.update_role(new_role)
        self.save_workers()

    def assign_vehicle_to_client(self, plate, client_id):
        vehicle = self.get_vehicle(plate)
        client = self.get_client(client_id)

        client.add_vehicle(vehicle)
        self.save_clients()

    def remove_vehicle_from_client(self, plate, client_id):
        client = self.get_client(client_id)
        client.remove_vehicle(plate)
        self.save_clients()

    def create_rental(
        self,
        vehicle_plate,
        client_id,
        start_date,
        end_date,
        kms_allowed,
        insurance_type):
        vehicle = self.get_vehicle(vehicle_plate)
        client = self.get_client(client_id)

        for rental in self.__rentals:
            same_vehicle = rental.vehicle.license_plate == vehicle.license_plate

            overlaps = self._rental_periods_overlap(
                rental.start_date,
                rental.end_date,
                start_date,
                end_date)

            if same_vehicle and overlaps:
                raise VehicleAlreadyRentedError(
                    f"Vehicle '{vehicle_plate}' is already rented during this period.")

        rental = Rental(
            vehicle,
            client,
            start_date,
            end_date,
            kms_allowed,
            insurance_type)

        self.__rentals.append(rental)
        self.save_rentals()
        return rental

    def get_rental(self, vehicle_plate, client_id, start_date):
        plate = self._normalise_plate(vehicle_plate)
        client_id = self._normalise_id(client_id)

        for rental in self.__rentals:
            if (
                rental.vehicle.license_plate == plate
                and rental.client.user_id == client_id
                and rental.start_date == start_date):
                return rental

        raise RentalNotFoundError("Rental not found.")

    def modify_rental(
        self,
        vehicle_plate,
        client_id,
        start_date,
        new_end_date=None,
        new_kms_allowed=None,
        new_insurance_type=None):
        rental = self.get_rental(vehicle_plate, client_id, start_date)

        if new_end_date is not None:
            for other in self.__rentals:
                if other == rental:
                    continue

                same_vehicle = (
                    other.vehicle.license_plate
                    == rental.vehicle.license_plate)

                overlaps = self._rental_periods_overlap(
                    other.start_date,
                    other.end_date,
                    rental.start_date,
                    new_end_date)

                if same_vehicle and overlaps:
                    raise VehicleAlreadyRentedError("This modification would overlap with another rental.")

        rental.modify_rental(
            new_end_date,
            new_kms_allowed,
            new_insurance_type)
        self.save_rentals()

    def add_kms_to_rental(self, vehicle_plate, client_id, start_date, kms):
        rental = self.get_rental(vehicle_plate, client_id, start_date)
        rental.add_kms_done(kms)

        self.save_rentals()
        self.save_vehicles()

    def get_all_rentals(self):
        return list(self.__rentals)

    def get_active_rentals(self):
        return [rental for rental in self.__rentals if rental.is_active()]

    def get_finished_rentals(self):
        return [rental for rental in self.__rentals if rental.is_finished()]

    def __str__(self):
        return (
            f"ShopManager | "
            f"{len(self.__clients)} clients | "
            f"{len(self.__workers)} workers | "
            f"{len(self.__vehicles)} vehicles | "
            f"{len(self.__rentals)} rentals")