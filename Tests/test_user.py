import unittest
from datetime import date
from dateutil.relativedelta import relativedelta
from Users.user import User
from Users.client import Client
from Users.admin import Admin
from Vehicles.car import Car
from Vehicles.motorbike import Motorbike
from Exceptions.exceptions import InvalidIDError, InvalidAgeError, InvalidRoleError, VehicleNotFoundError, ClientAlreadyHasVehicleError

class TestUser(unittest.TestCase):

    def setUp(self):
        self.client = Client("Hanna Rathke", date(2006, 1, 27), "C001")
        self.admin = Admin("Lucia Zamora", date(2007, 11, 5), "A001", "mechanic")
        self.car = Car("Mercedes", "Black", "1234ABC", "C-Class", date(2015, 1, 1), 50000)
        self.car2 = Car("BMW", "Blue", "5678DEF", "X3", date(2018, 1, 1), 30000)
        self.motorbike = Motorbike("Yamaha", "Silver", "1111AAA", "MT-07", date(2019, 1, 1), 10000)

    def test_cannot_instantiate_user_directly(self):
        with self.assertRaises(TypeError):
            User("Hanna", date(2006, 1, 27), "U001")

    def test_client_created_correctly(self):
        self.assertEqual(self.client.name, "Hanna Rathke")
        self.assertEqual(self.client.user_id, "C001")
        self.assertEqual(self.client.date_of_birth, date(2006, 1, 27))

    def test_client_starts_with_empty_vehicles(self):
        self.assertEqual(len(self.client.vehicles), 0)

    def test_name_stripped_on_creation(self):
        client = Client("  Hanna  ", date(2006, 1, 27), "C002")
        self.assertEqual(client.name, "Hanna")

    def test_user_id_stored_as_string(self):
        client = Client("Hanna", date(2006, 1, 27), 123)
        self.assertEqual(client.user_id, "123")

    def test_empty_name_raises_error(self):
        with self.assertRaises(ValueError):
            Client("", date(2006, 1, 27), "C002")

    def test_blank_name_raises_error(self):
        with self.assertRaises(ValueError):
            Client("   ", date(2006, 1, 27), "C002")

    def test_name_not_string_raises_error(self):
        with self.assertRaises(ValueError):
            Client(123, date(2006, 1, 27), "C002")

    def test_future_dob_raises_error(self):
        with self.assertRaises(InvalidAgeError):
            Client("Hanna", date.today() + relativedelta(days=1), "C002")

    def test_dob_not_date_raises_error(self):
        with self.assertRaises(InvalidAgeError):
            Client("Hanna", "2006-01-27", "C002")

    def test_empty_id_raises_error(self):
        with self.assertRaises(InvalidIDError):
            Client("Hanna", date(2006, 1, 27), "")

    def test_blank_id_raises_error(self):
        with self.assertRaises(InvalidIDError):
            Client("Hanna", date(2006, 1, 27), "   ")

    def test_update_name(self):
        self.client.update_name("Maria")
        self.assertEqual(self.client.name, "Maria")

    def test_update_name_empty_raises_error(self):
        with self.assertRaises(ValueError):
            self.client.update_name("")

    def test_update_name_blank_raises_error(self):
        with self.assertRaises(ValueError):
            self.client.update_name("   ")

    def test_update_date_of_birth(self):
        new_dob = date(2005, 2, 2)
        self.client.update_date_of_birth(new_dob)
        self.assertEqual(self.client.date_of_birth, new_dob)

    def test_update_date_of_birth_future_raises_error(self):
        with self.assertRaises(InvalidAgeError):
            self.client.update_date_of_birth(date.today() + relativedelta(days=1))

    def test_update_date_of_birth_not_date_raises_error(self):
        with self.assertRaises(InvalidAgeError):
            self.client.update_date_of_birth("2005-02-02")

    def test_get_age_returns_integer(self):
        self.assertIsInstance(self.client.get_age(), int)

    def test_get_age_today_birthday_is_zero(self):
        client = Client("Baby", date.today(), "C004")
        self.assertEqual(client.get_age(), 0)

    def test_two_users_same_id_are_equal(self):
        client1 = Client("Hanna", date(2006, 1, 27), "C001")
        client2 = Client("Lucia", date(2007, 11, 5), "C001")
        self.assertEqual(client1, client2)

    def test_two_users_different_id_not_equal(self):
        client2 = Client("Hanna", date(2006, 1, 27), "C002")
        self.assertNotEqual(self.client, client2)

    def test_user_not_equal_to_non_user(self):
        self.assertEqual(self.client.__eq__("not a user"), NotImplemented)

    def test_client_to_csv_row_keys(self):
        row = self.client.to_csv_row()
        for key in ["type", "name", "date_of_birth", "user_id", "vehicles"]:
            self.assertIn(key, row)

    def test_client_to_csv_row_type(self):
        self.assertEqual(self.client.to_csv_row()["type"], "Client")

    def test_client_to_csv_row_vehicles_empty(self):
        self.assertEqual(self.client.to_csv_row()["vehicles"], "")

    def test_client_to_csv_row_vehicles_with_car(self):
        self.client.add_vehicle(self.car)
        row = self.client.to_csv_row()
        self.assertIn("1234ABC", row["vehicles"])

    def test_client_to_csv_row_multiple_vehicles(self):
        self.client.add_vehicle(self.car)
        self.client.add_vehicle(self.car2)
        row = self.client.to_csv_row()
        self.assertIn("1234ABC", row["vehicles"])
        self.assertIn("5678DEF", row["vehicles"])

    def test_admin_to_csv_row_has_role(self):
        row = self.admin.to_csv_row()
        self.assertIn("role", row)
        self.assertEqual(row["role"], "mechanic")

    def test_admin_to_csv_row_type(self):
        self.assertEqual(self.admin.to_csv_row()["type"], "Admin")

    def test_client_str_contains_name(self):
        self.assertIn("Hanna Rathke", str(self.client))

    def test_client_str_contains_id(self):
        self.assertIn("C001", str(self.client))

    def test_admin_str_contains_name(self):
        self.assertIn("Lucia Zamora", str(self.admin))

    def test_admin_valid_roles(self):
        for role in ["mechanic", "rental manager", "administrator"]:
            admin = Admin("Lucia", date(2007, 11, 5), "T001", role)
            self.assertEqual(admin.role, role)

    def test_admin_invalid_role_raises_error(self):
        with self.assertRaises(InvalidRoleError):
            Admin("Lucia", date(2007, 11, 5), "A002", "driver")

    def test_admin_role_stored_lowercase(self):
        admin = Admin("Lucia", date(2007, 11, 5), "A002", "MECHANIC")
        self.assertEqual(admin.role, "mechanic")

    def test_admin_update_role(self):
        self.admin.update_role("administrator")
        self.assertEqual(self.admin.role, "administrator")

    def test_admin_update_role_rental_manager(self):
        self.admin.update_role("rental manager")
        self.assertEqual(self.admin.role, "rental manager")

    def test_admin_update_role_invalid_raises_error(self):
        with self.assertRaises(InvalidRoleError):
            self.admin.update_role("driver")

    def test_admin_get_info_contains_role(self):
        self.assertIn("mechanic", self.admin.get_info())

    def test_admin_get_info_contains_name(self):
        self.assertIn("Lucia Zamora", self.admin.get_info())

    def test_admin_get_info_contains_id(self):
        self.assertIn("A001", self.admin.get_info())

    def test_client_add_vehicle(self):
        self.client.add_vehicle(self.car)
        self.assertIn(self.car, self.client.vehicles)

    def test_client_add_multiple_vehicles(self):
        self.client.add_vehicle(self.car)
        self.client.add_vehicle(self.car2)
        self.assertEqual(len(self.client.vehicles), 2)

    def test_client_add_vehicle_duplicate_raises_error(self):
        self.client.add_vehicle(self.car)
        with self.assertRaises(ClientAlreadyHasVehicleError):
            self.client.add_vehicle(self.car)

    def test_client_add_non_vehicle_raises_error(self):
        with self.assertRaises(TypeError):
            self.client.add_vehicle("not a vehicle")

    def test_client_add_none_raises_error(self):
        with self.assertRaises(TypeError):
            self.client.add_vehicle(None)

    def test_client_remove_vehicle(self):
        self.client.add_vehicle(self.car)
        self.client.remove_vehicle("1234ABC")
        self.assertNotIn(self.car, self.client.vehicles)

    def test_client_remove_vehicle_not_found_raises_error(self):
        with self.assertRaises(VehicleNotFoundError):
            self.client.remove_vehicle("9999ZZZ")

    def test_client_remove_vehicle_case_insensitive(self):
        self.client.add_vehicle(self.car)
        self.client.remove_vehicle("1234abc")
        self.assertNotIn(self.car, self.client.vehicles)

    def test_client_vehicles_returns_copy(self):
        self.client.add_vehicle(self.car)
        vehicles = self.client.vehicles
        vehicles.clear()
        self.assertEqual(len(self.client.vehicles), 1)

    def test_client_update_vehicle_mileage(self):
        self.client.add_vehicle(self.car)
        self.client.update_vehicle_mileage("1234ABC", 60000)
        self.assertEqual(self.car.mileage, 60000)

    def test_client_update_vehicle_mileage_not_found_raises_error(self):
        with self.assertRaises(VehicleNotFoundError):
            self.client.update_vehicle_mileage("9999ZZZ", 60000)

    def test_client_update_vehicle_color(self):
        self.client.add_vehicle(self.car)
        self.client.update_vehicle_color("1234ABC", "Green")
        self.assertEqual(self.car.color, "Green")

    def test_client_update_vehicle_color_not_found_raises_error(self):
        with self.assertRaises(VehicleNotFoundError):
            self.client.update_vehicle_color("9999ZZZ", "Green")

    def test_client_check_next_itv_returns_future_date(self):
        self.client.add_vehicle(self.car)
        itv = self.client.check_next_itv("1234ABC")
        self.assertGreater(itv, date.today())

    def test_client_check_next_itv_not_found_raises_error(self):
        with self.assertRaises(VehicleNotFoundError):
            self.client.check_next_itv("9999ZZZ")

    def test_client_check_next_maintenance_returns_string(self):
        self.client.add_vehicle(self.car)
        result = self.client.check_next_maintenance("1234ABC")
        self.assertIsInstance(result, str)

    def test_client_check_next_maintenance_not_found_raises_error(self):
        with self.assertRaises(VehicleNotFoundError):
            self.client.check_next_maintenance("9999ZZZ")

    def test_client_get_info_contains_id(self):
        self.assertIn("C001", self.client.get_info())

    def test_client_get_info_contains_name(self):
        self.assertIn("Hanna Rathke", self.client.get_info())

    def test_client_get_info_contains_vehicle_plate(self):
        self.client.add_vehicle(self.car)
        self.assertIn("1234ABC", self.client.get_info())

    def test_client_different_vehicle_types(self):
        self.client.add_vehicle(self.car)
        self.client.add_vehicle(self.motorbike)
        self.assertEqual(len(self.client.vehicles), 2)

    def test_admin_role_must_be_text_on_creation(self):
        with self.assertRaises(InvalidRoleError):
            Admin("Lucia Zamora", date(2007, 11, 5), "A003", 123)

    def test_admin_update_role_must_be_text(self):
        with self.assertRaises(InvalidRoleError):
            self.admin.update_role(123)
    
    def test_user_id_none_raises_error(self):
        with self.assertRaises(InvalidIDError):
            Client("Hanna Rathke", date(2006, 1, 27), None)

if __name__ == "__main__":
    unittest.main()