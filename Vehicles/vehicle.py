from abc import ABC, abstractmethod
from datetime import date
from dateutil.relativedelta import relativedelta
import re
from Exceptions.exceptions import InvalidLicensePlateError, InvalidMileageError, InvalidDateError

class Vehicle(ABC):
    def __init__(self, brand, color, license_plate, model, matriculation_date, mileage):
        self.__brand = self.validate_text_field(brand, "Brand")
        self.__color = self.validate_text_field(color, "Color")
        self.__license_plate = self.validate_license_plate(license_plate)
        self.__model = self.validate_text_field(model, "Model")
        self.__matriculation_date = self.validate_date(matriculation_date)
        self.__mileage = self.validate_mileage(mileage)

    @property
    def brand(self):
        return self.__brand

    @property
    def color(self):
        return self.__color

    @property
    def license_plate(self):
        return self.__license_plate

    @property
    def model(self):
        return self.__model

    @property
    def matriculation_date(self):
        return self.__matriculation_date

    @property
    def mileage(self):
        return self.__mileage

    def validate_text_field(self, value, field_name):
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string.")

        if value.strip() == "":
            raise ValueError(f"{field_name} cannot be empty.")
        return value.strip()

    def validate_license_plate(self, plate):
        if not isinstance(plate, str):
            raise InvalidLicensePlateError("License plate must be a string.")
        plate = plate.strip().upper()

        if not re.fullmatch(r"\d{4}[A-Z]{3}", plate):
            raise InvalidLicensePlateError("License plate must have 4 digits followed by 3 letters.")
        return plate

    def validate_mileage(self, mileage):
        if not isinstance(mileage, (int, float)):
            raise InvalidMileageError("Mileage must be numeric.")

        if mileage < 0:
            raise InvalidMileageError("Mileage cannot be negative.")
        return float(mileage)

    def validate_date(self, matriculation_date):
        if not isinstance(matriculation_date, date):
            raise InvalidDateError("Matriculation date must be a date object.")

        if matriculation_date > date.today():
            raise InvalidDateError("Matriculation date cannot be in the future.")
        return matriculation_date

    def update_brand(self, new_brand):
        self.__brand = self.validate_text_field(new_brand,"Brand")

    def update_color(self, new_color):
        self.__color = self.validate_text_field(new_color,"Color")

    def update_model(self, new_model):
        self.__model = self.validate_text_field(new_model,"Model")

    def update_mileage(self, new_mileage):
        new_mileage = self.validate_mileage(new_mileage)

        if new_mileage < self.__mileage:
            raise InvalidMileageError("Mileage cannot decrease.")
        self.__mileage = new_mileage

    def years_since_matriculation(self):
        return relativedelta(
            date.today(),
            self.__matriculation_date).years

    @abstractmethod
    def next_itv(self):  
        pass

    @abstractmethod
    def next_maintenance(self):  
        pass

    def to_csv_row(self):
        return {
            "type": self.__class__.__name__,
            "brand": self.brand,
            "color": self.color,
            "license_plate": self.license_plate,
            "model": self.model,
            "matriculation_date": self.matriculation_date.isoformat(),
            "mileage": self.mileage}

    def __eq__(self, other):
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self.license_plate == other.license_plate

    def __str__(self):
        return (
            f"{self.__class__.__name__} | "
            f"{self.brand} {self.model} | "
            f"Plate: {self.license_plate} | "
            f"Color: {self.color} | "
            f"Mileage: {self.mileage}")