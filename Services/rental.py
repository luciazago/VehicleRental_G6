from datetime import date
from Exceptions.exceptions import(
    InvalidRentalPeriodError,
    RentalAlreadyFinishedError,
    KmsExceededError,
    InvalidKmsAllowedError)
from Vehicles.vehicle import Vehicle
from Users.client import Client

class Rental:

    VALID_INSURANCE = ("basic", "premium", "full")

    def __init__(self, vehicle, client, start_date, end_date, kms_allowed, insurance_type):
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Vehicle must be a Vehicle object.")

        if not isinstance(client, Client):
            raise TypeError("Client must be a Client object.")

        if not isinstance(start_date, date) or not isinstance(end_date, date):
            raise InvalidRentalPeriodError("Start date and end date must be date objects.")

        if end_date < start_date:
            raise InvalidRentalPeriodError("End date cannot be before start date.")

        if not isinstance(kms_allowed, (int, float)) or kms_allowed <= 0:
            raise InvalidKmsAllowedError("Kms allowed must be a positive number.")

        if not isinstance(insurance_type, str):
            raise ValueError("Insurance type must be text.")

        insurance_type = insurance_type.lower().strip()

        if insurance_type not in self.VALID_INSURANCE:
            raise ValueError(
                f"Invalid insurance type. Choose from: {self.VALID_INSURANCE}" )

        self.__vehicle = vehicle
        self.__client = client
        self.__start_date = start_date
        self.__end_date = end_date
        self.__kms_allowed = float(kms_allowed)
        self.__kms_done = 0.0
        self.__insurance_type = insurance_type

    @property
    def vehicle(self):
        return self.__vehicle

    @property
    def client(self):
        return self.__client

    @property
    def start_date(self):
        return self.__start_date

    @property
    def end_date(self):
        return self.__end_date

    @property
    def kms_allowed(self):
        return self.__kms_allowed

    @property
    def kms_done(self):
        return self.__kms_done

    @property
    def insurance_type(self):
        return self.__insurance_type

    def is_active(self):
        return self.__start_date <= date.today() <= self.__end_date

    def is_finished(self):
        return date.today() > self.__end_date

    def is_upcoming(self):
        return date.today() < self.__start_date

    def modify_rental(self, new_end_date=None, new_kms_allowed=None, new_insurance_type=None):
        if self.is_finished():
            raise RentalAlreadyFinishedError("Cannot modify a finished rental.")

        if new_end_date is not None:
            if not isinstance(new_end_date, date):
                raise InvalidRentalPeriodError("New end date must be a date object.")

            if new_end_date < self.__start_date:
                raise InvalidRentalPeriodError("New end date cannot be before start date.")

            self.__end_date = new_end_date

        if new_kms_allowed is not None:
            if not isinstance(new_kms_allowed, (int, float)) or new_kms_allowed <= 0:
                raise InvalidKmsAllowedError("Kms allowed must be a positive number.")

            if new_kms_allowed < self.__kms_done:
                raise InvalidKmsAllowedError(
                    "Kms allowed cannot be lower than kms already done.")

            self.__kms_allowed = float(new_kms_allowed)

        if new_insurance_type is not None:
            if not isinstance(new_insurance_type, str):
                raise ValueError("Insurance type must be text.")

            new_insurance_type = new_insurance_type.lower().strip()

            if new_insurance_type not in self.VALID_INSURANCE:
                raise ValueError(
                    f"Invalid insurance type. Choose from: {self.VALID_INSURANCE}")

            self.__insurance_type = new_insurance_type

    def add_kms_done(self, kms):
        if self.is_finished():
            raise RentalAlreadyFinishedError("Cannot add kms to a finished rental.")

        if not isinstance(kms, (int, float)) or kms <= 0:
            raise InvalidKmsAllowedError("Kms to add must be a positive number.")

        if self.__kms_done + kms > self.__kms_allowed:
            raise KmsExceededError(
                f"Adding {kms} km would exceed the allowed {self.__kms_allowed} km.")

        self.__kms_done += kms
        self.__vehicle.update_mileage(self.__vehicle.mileage + kms)

    def kms_remaining(self):
        return self.__kms_allowed - self.__kms_done
    
    def set_kms_done_from_csv(self, kms_done):
        if not isinstance(kms_done, (int, float)) or kms_done < 0:
            raise ValueError("Kms done must be a non-negative number.")

        if kms_done > self.__kms_allowed:
            raise KmsExceededError("Kms done cannot be higher than kms allowed.")

        self.__kms_done = float(kms_done)

    def to_csv_row(self):
        return {
            "vehicle_plate": self.vehicle.license_plate,
            "client_id": self.client.user_id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "kms_allowed": self.kms_allowed,
            "kms_done": self.kms_done,
            "insurance_type": self.insurance_type,}

    def __eq__(self, other):
        if not isinstance(other, Rental):
            return NotImplemented

        return (
            self.vehicle.license_plate == other.vehicle.license_plate
            and self.client.user_id == other.client.user_id
            and self.start_date == other.start_date)

    def __str__(self):
        if self.is_active():
            status = "ACTIVE"
        elif self.is_finished():
            status = "FINISHED"
        else:
            status = "UPCOMING"

        return (
            f"Rental [{status}] | Vehicle: {self.vehicle.license_plate} "
            f"| Client: {self.client.user_id} "
            f"| {self.start_date} to {self.end_date} "
            f"| {self.kms_done:.0f}/{self.kms_allowed:.0f} km "
            f"| Insurance: {self.insurance_type}")