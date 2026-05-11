from Users.user import User
from Vehicles.vehicle import Vehicle
from Exceptions.exceptions import VehicleNotFoundError, ClientAlreadyHasVehicleError

class Client(User):
    def __init__(self, name, date_of_birth, user_id):
        super().__init__(name, date_of_birth, user_id)
        self.__vehicles = []

    @property
    def vehicles(self):
        return list(self.__vehicles)

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Only Vehicle objects can be added.")

        if vehicle in self.__vehicles:
            raise ClientAlreadyHasVehicleError(
                f"{vehicle.license_plate} already belongs to this client.")
        self.__vehicles.append(vehicle)

    def remove_vehicle(self, license_plate):
        vehicle = self._find_vehicle(license_plate)
        self.__vehicles.remove(vehicle)

    def _find_vehicle(self, license_plate):
        if not isinstance(license_plate, str):
            raise VehicleNotFoundError(
                "License plate must be text." )
        plate = license_plate.upper().strip()

        for vehicle in self.__vehicles:
            if vehicle.license_plate == plate:
                return vehicle

        raise VehicleNotFoundError(f"Vehicle {license_plate} not found.")

    def update_vehicle_mileage(self, license_plate, new_mileage):
        vehicle = self._find_vehicle(license_plate)
        vehicle.update_mileage(new_mileage)

    def update_vehicle_color(self, license_plate, new_color):
        vehicle = self._find_vehicle(license_plate)
        vehicle.update_color(new_color)

    def check_next_itv(self, license_plate):
        vehicle = self._find_vehicle(license_plate)
        return vehicle.next_itv()

    def check_next_maintenance(self, license_plate):
        vehicle = self._find_vehicle(license_plate)
        return vehicle.next_maintenance()

    def get_info(self):
        plates = [v.license_plate for v in self.__vehicles]

        return (
            f"Client | {self.name} | ID: {self.user_id} "
            f"| Vehicles: {plates}")

    def to_csv_row(self): #creates a method that converts the object into a dictionary for CSV saving
        row = super().to_csv_row() #gets the dictionary from the parent class (User)
        row["vehicles"] = ";".join(v.license_plate for v in self.__vehicles ) #takes all the client’s vehicle plates and joins them into one string separated by ;
        return row