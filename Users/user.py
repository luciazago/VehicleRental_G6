from abc import ABC, abstractmethod
from datetime import date
from dateutil.relativedelta import relativedelta
from Exceptions.exceptions import InvalidIDError, InvalidAgeError

class User(ABC):
    def __init__(self, name, date_of_birth, user_id):
        self._validate_name(name)
        self._validate_date_of_birth(date_of_birth)
        self._validate_user_id(user_id)
        self.__name = name.strip()
        self.__date_of_birth = date_of_birth
        self.__user_id = str(user_id).strip()

    def _validate_name(self, name):
        if not isinstance(name, str):
            raise ValueError("Name must be text.")
        if not name.strip():
            raise ValueError("Name cannot be empty.")

    def _validate_date_of_birth(self, dob):
        if not isinstance(dob, date):
            raise InvalidAgeError("Date of birth must be a date object." )
        if dob > date.today():
            raise InvalidAgeError("Date of birth cannot be in the future.")

    def _validate_user_id(self, user_id):
        if user_id is None:
            raise InvalidIDError("User ID cannot be empty.")
        if not str(user_id).strip(): #removes spaces and checks if nothing is left
            raise InvalidIDError("User ID cannot be empty.")

    @property
    def name(self):
        return self.__name

    @property
    def date_of_birth(self):
        return self.__date_of_birth

    @property
    def user_id(self):
        return self.__user_id

    def update_name(self, new_name):
        self._validate_name(new_name)
        self.__name = new_name.strip()

    def update_date_of_birth(self, new_dob):
        self._validate_date_of_birth(new_dob)
        self.__date_of_birth = new_dob

    def get_age(self):
        return relativedelta(
            date.today(),
            self.__date_of_birth).years

    @abstractmethod
    def get_info(self):
        pass

    def to_csv_row(self):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "date_of_birth": self.date_of_birth.isoformat(),
            "user_id": self.user_id}

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.user_id == other.user_id

    def __str__(self):
        return (
            f"{self.__class__.__name__} | "
            f"{self.name} | "
            f"ID: {self.user_id}")