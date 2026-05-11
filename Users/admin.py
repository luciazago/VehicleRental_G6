from Users.user import User
from Exceptions.exceptions import InvalidRoleError

class Admin(User):

    VALID_ROLES = ("mechanic","rental manager","administrator")

    def __init__(self, name, date_of_birth, user_id, role):
        super().__init__(name, date_of_birth, user_id)

        if not isinstance(role, str):
            raise InvalidRoleError("Role must be text.")
        role = role.strip().lower()

        if role not in self.VALID_ROLES:
            raise InvalidRoleError(
                f"Invalid role. Choose from {self.VALID_ROLES}")
        self.__role = role

    @property
    def role(self):
        return self.__role

    def update_role(self, new_role):
        if not isinstance(new_role, str):
            raise InvalidRoleError("Role must be text.")
        new_role = new_role.strip().lower()

        if new_role not in self.VALID_ROLES:
            raise InvalidRoleError(
                f"Invalid role. Choose from {self.VALID_ROLES}")
        self.__role = new_role

    def get_info(self):
        return (
            f"Admin | {self.name} | ID: {self.user_id} "
            f"| Role: {self.role}")

    def to_csv_row(self): #creates a method that converts the object into a dictionary for CSV storage
        row = super().to_csv_row() #gets the dictionary from the parent class (User) --> and stores it in row
        row["role"] = self.role #adds the worker/admin role to the dictionary
        return row