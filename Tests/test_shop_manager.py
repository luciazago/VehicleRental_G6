import unittest
from datetime import date
from dateutil.relativedelta import relativedelta
from Services.shop_manager import ShopManager
from Vehicles.car import Car
from Vehicles.motorbike import Motorbike
from Vehicles.truck import Truck
from Users.client import Client
from Users.admin import Admin
from Exceptions.exceptions import DuplicateLicensePlateError, DuplicateIDError, VehicleNotFoundError, UserNotFoundError, RentalNotFoundError, VehicleAlreadyRentedError

class TestShopManager(unittest.TestCase):

    def setUp(self):
        self.shop = ShopManager()
        self.shop._ShopManager__vehicles = [] #start empty for testing
        self.shop._ShopManager__clients = []
        self.shop._ShopManager__workers = []
        self.shop._ShopManager__rentals = []
        self.car = Car("Mercedes", "Black", "1234ABC", "C-Class", date(2015, 1, 1), 50000)
        self.car2 = Car("BMW", "Blue", "5678DEF", "X3", date(2018, 1, 1), 30000)
        self.motorbike = Motorbike("Honda", "Black", "3333CCC", "CBR", date(2019, 1, 1), 10000)
        self.truck = Truck("Volvo", "White", "4444DDD", "FH16", date(2010, 1, 1), 100000)
        self.client = Client("Hanna Rathke", date(2006, 1, 27), "C001")
        self.client2 = Client("Hanno Schwecke", date(2005, 6, 14), "C002")
        self.admin = Admin("Lucia Zamora", date(2007, 11, 5), "A001","mechanic")
        self.today = date.today()
        self.start = self.today - relativedelta(days=3)
        self.end = self.today + relativedelta(days=7)
        self.past_start = self.today - relativedelta(days=10)
        self.past_end = self.today - relativedelta(days=1)
        self.future_start = self.today + relativedelta(days=2)
        self.future_end = self.today + relativedelta(days=10)

    def test_add_vehicle_object(self):
        self.shop.add_vehicle(self.car)
        self.assertIn(self.car, self.shop.get_all_vehicles()) #gets all vehicles from the shop and checks if self.car is inside that list.

    def test_add_multiple_vehicles(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_vehicle(self.car2)
        self.assertEqual(len(self.shop.get_all_vehicles()), 2)

    def test_add_duplicate_vehicle_raises_error(self):
        self.shop.add_vehicle(self.car)

        with self.assertRaises(DuplicateLicensePlateError):
            self.shop.add_vehicle(self.car)

    def test_add_vehicle_from_raw_inputs_car(self): #creates a test to check if the shop can create and add a Car using raw input values instead of an already-created object
        self.shop.add_vehicle("1", "Audi", "Black", "9999AAA", "A4", date(2020, 1, 1), 1000)
        self.assertIsInstance(self.shop.get_vehicle("9999AAA"), Car) #checks that an object belongs to a specific class.

    def test_add_vehicle_from_raw_inputs_motorbike(self):
        self.shop.add_vehicle("2", "Yamaha", "Blue", "8888BBB", "R1", date(2020, 1, 1), 1000)
        self.assertIsInstance(self.shop.get_vehicle("8888BBB"), Motorbike)

    def test_add_vehicle_from_raw_inputs_truck(self):
        self.shop.add_vehicle("3", "MAN", "White", "7777CCC", "TruckX", date(2020, 1, 1), 1000)
        self.assertIsInstance(self.shop.get_vehicle("7777CCC"), Truck)

    def test_add_vehicle_invalid_type_raises_error(self):
        with self.assertRaises(ValueError):
            self.shop.add_vehicle("9", "Audi", "Black", "6666DDD", "A3", date(2020, 1, 1), 1000)

    def test_get_vehicle(self):
        self.shop.add_vehicle(self.car)
        self.assertEqual(self.shop.get_vehicle("1234ABC"), self.car) #searches for the vehicle with that plate, and returns the vehicle

    def test_get_vehicle_case_insensitive(self):
        self.shop.add_vehicle(self.car)
        self.assertEqual(self.shop.get_vehicle("1234abc"), self.car)

    def test_get_vehicle_not_found_raises_error(self):
        with self.assertRaises(VehicleNotFoundError):
            self.shop.get_vehicle("9999ZZZ")

    def test_remove_vehicle(self):
        self.shop.add_vehicle(self.car)
        self.shop.remove_vehicle("1234ABC")
        self.assertNotIn(self.car, self.shop.get_all_vehicles()) #checks that self.car is NOT inside the shop’s vehicle list anymore

    def test_remove_vehicle_not_found_raises_error(self):
        with self.assertRaises(VehicleNotFoundError):
            self.shop.remove_vehicle("9999ZZZ")

    def test_remove_active_rented_vehicle_raises_error(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental("1234ABC", "C001", self.start, self.end, 500, "basic")

        with self.assertRaises(VehicleAlreadyRentedError):
            self.shop.remove_vehicle("1234ABC")

    def test_remove_upcoming_rented_vehicle_raises_error(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental("1234ABC", "C001", self.future_start, self.future_end, 500, "basic")

        with self.assertRaises(VehicleAlreadyRentedError):
            self.shop.remove_vehicle("1234ABC")

    def test_remove_vehicle_with_finished_rental_ok(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental("1234ABC", "C001", self.past_start, self.past_end, 500, "basic")
        self.shop.remove_vehicle("1234ABC")
        self.assertNotIn(self.car, self.shop.get_all_vehicles())

    def test_get_all_vehicles_returns_copy(self):
        self.shop.add_vehicle(self.car)
        vehicles = self.shop.get_all_vehicles()
        vehicles.clear()
        self.assertEqual(len(self.shop.get_all_vehicles()), 1)

    def test_update_vehicle_color(self):
        self.shop.add_vehicle(self.car)
        self.shop.update_vehicle_color("1234ABC", "Green")
        self.assertEqual(self.car.color, "Green")

    def test_update_vehicle_color_not_found_raises_error(self):
        with self.assertRaises(VehicleNotFoundError):
            self.shop.update_vehicle_color("9999ZZZ", "Green")

    def test_update_vehicle_mileage(self):
        self.shop.add_vehicle(self.car)
        self.shop.update_vehicle_mileage("1234ABC", 60000)
        self.assertEqual(self.car.mileage, 60000)

    def test_update_vehicle_mileage_not_found_raises_error(self):
        with self.assertRaises(VehicleNotFoundError):
            self.shop.update_vehicle_mileage("9999ZZZ", 60000)

    def test_check_vehicle_itv(self):
        self.shop.add_vehicle(self.car)
        self.assertGreater(self.shop.check_vehicle_itv("1234ABC"), date.today())

    def test_check_vehicle_maintenance(self):
        self.shop.add_vehicle(self.car)
        self.assertIn("Next maintenance", self.shop.check_vehicle_maintenance("1234ABC"))

    def test_add_client_object(self):
        self.shop.add_client(self.client)
        self.assertIn(self.client, self.shop.get_all_clients())

    def test_add_client_from_raw_inputs(self):
        self.shop.add_client("Hanna Rathke", date(2006, 1, 27), "C010")
        self.assertIsInstance(self.shop.get_client("C010"), Client)

    def test_add_duplicate_client_raises_error(self):
        self.shop.add_client(self.client)

        with self.assertRaises(DuplicateIDError):
            self.shop.add_client(self.client)

    def test_add_client_same_id_as_worker_raises_error(self):
        self.shop.add_worker(self.admin)

        with self.assertRaises(DuplicateIDError):
            self.shop.add_client("Hanno Schwecke", date(2005, 6, 14), "A001")

    def test_get_client(self):
        self.shop.add_client(self.client)
        self.assertEqual(self.shop.get_client("C001"), self.client)

    def test_get_client_not_found_raises_error(self):
        with self.assertRaises(UserNotFoundError):
            self.shop.get_client("C999")

    def test_remove_client(self):
        self.shop.add_client(self.client)
        self.shop.remove_client("C001")
        self.assertNotIn(self.client, self.shop.get_all_clients())
    
    def test_remove_client_with_active_rental_raises_error(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental("1234ABC", "C001", self.start, self.end, 500, "basic")

        with self.assertRaises(VehicleAlreadyRentedError):
            self.shop.remove_client("C001")

    def test_remove_client_with_finished_rental_ok(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental("1234ABC", "C001", self.past_start, self.past_end, 500, "basic")
        self.shop.remove_client("C001")
        self.assertNotIn(self.client, self.shop.get_all_clients())

    def test_remove_client_not_found_raises_error(self):
        with self.assertRaises(UserNotFoundError):
            self.shop.remove_client("C999")

    def test_update_client_name(self):
        self.shop.add_client(self.client)
        self.shop.update_client_name("C001", "Maria")
        self.assertEqual(self.client.name, "Maria")

    def test_get_all_clients_returns_copy(self): #makes sure that clearing the copied list does NOT delete the real clients inside the shop.
        self.shop.add_client(self.client)
        clients = self.shop.get_all_clients()
        clients.clear()
        self.assertEqual(len(self.shop.get_all_clients()), 1)

    def test_add_worker_object(self):
        self.shop.add_worker(self.admin)
        self.assertIn(self.admin, self.shop.get_all_workers())

    def test_add_worker_from_raw_inputs(self):
        self.shop.add_worker("Lucia Zamora", date(2007, 11, 5), "A010", "mechanic")
        self.assertIsInstance(self.shop.get_worker("A010"), Admin)

    def test_add_duplicate_worker_raises_error(self):
        self.shop.add_worker(self.admin)

        with self.assertRaises(DuplicateIDError):
            self.shop.add_worker(self.admin)

    def test_add_worker_same_id_as_client_raises_error(self):
        self.shop.add_client(self.client)

        with self.assertRaises(DuplicateIDError):
            self.shop.add_worker("Lucia Zamora", date(2007, 11, 5), "C001", "mechanic")

    def test_get_worker(self): #check if the shop can correctly find a worker by ID
        self.shop.add_worker(self.admin)
        self.assertEqual(self.shop.get_worker("A001"), self.admin)

    def test_get_worker_not_found_raises_error(self):
        with self.assertRaises(UserNotFoundError):
            self.shop.get_worker("A999")

    def test_remove_worker(self):
        self.shop.add_worker(self.admin)
        self.shop.remove_worker("A001")
        self.assertEqual(len(self.shop.get_all_workers()), 0)

    def test_remove_worker_not_found_raises_error(self):
        with self.assertRaises(UserNotFoundError):
            self.shop.remove_worker("A999")

    def test_update_worker_role(self):
        self.shop.add_worker(self.admin) 
        self.shop.update_worker_role("A001", "administrator")
        self.assertEqual(self.admin.role,"administrator")

    def test_get_all_workers_returns_copy(self): #This test checks that changing the returned workers list does not change the real workers stored in the shop.
        self.shop.add_worker(self.admin) #adds one worker into the shop
        workers = self.shop.get_all_workers() #gets the workers list and stores it in workers.
        workers.clear() #empties the copied list
        self.assertEqual(len(self.shop.get_all_workers()), 1) #checks that the real workers list inside the shop still contains 1 worker

    def test_assign_vehicle_to_client(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.assign_vehicle_to_client("1234ABC", "C001")
        self.assertIn(self.car, self.client.vehicles)

    def test_remove_vehicle_from_client(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.assign_vehicle_to_client("1234ABC", "C001")
        self.shop.remove_vehicle_from_client("1234ABC","C001")
        self.assertNotIn(self.car, self.client.vehicles)

    def test_assign_vehicle_not_found_raises_error(self):
        self.shop.add_client(self.client)

        with self.assertRaises(VehicleNotFoundError):
            self.shop.assign_vehicle_to_client("9999ZZZ", "C001")

    def test_assign_client_not_found_raises_error(self):
        self.shop.add_vehicle(self.car)

        with self.assertRaises(UserNotFoundError):
            self.shop.assign_vehicle_to_client("1234ABC","C999")

    def test_create_rental(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        rental = self.shop.create_rental("1234ABC", "C001", self.start, self.end, 500, "basic")
        self.assertIn(rental, self.shop.get_all_rentals())

    def test_create_rental_vehicle_not_found_raises_error(self):
        self.shop.add_client(self.client)

        with self.assertRaises(VehicleNotFoundError):
            self.shop.create_rental("9999ZZZ", "C001", self.start, self.end, 500, "basic")

    def test_create_rental_client_not_found_raises_error(self):
        self.shop.add_vehicle(self.car)

        with self.assertRaises(UserNotFoundError):
            self.shop.create_rental("1234ABC", "C999", self.start, self.end, 500, "basic")

    def test_create_overlapping_rental_raises_error(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.add_client(self.client2)
        self.shop.create_rental("1234ABC", "C001", self.start, self.end, 500,"basic")

        with self.assertRaises(VehicleAlreadyRentedError):
            self.shop.create_rental("1234ABC", "C002", self.start, self.end, 500,"basic")

    def test_create_non_overlapping_rentals_ok(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.add_client(self.client2)
        self.shop.create_rental("1234ABC", "C001", self.past_start, self.past_end, 500,"basic")
        self.shop.create_rental("1234ABC", "C002", self.future_start, self.future_end, 500, "basic")
        self.assertEqual(len(self.shop.get_all_rentals()), 2)

    def test_get_rental_not_found_raises_error(self):
        with self.assertRaises(RentalNotFoundError):
            self.shop.get_rental("1234ABC", "C001", self.today)

    def test_modify_rental_overlap_raises_error(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.add_client(self.client2)
        self.shop.create_rental("1234ABC", "C001", self.start, self.end, 500,"basic")
        self.shop.create_rental("1234ABC", "C002", self.today + relativedelta(days=20), self.today + relativedelta(days=30),500,"basic")

        with self.assertRaises(VehicleAlreadyRentedError):
            self.shop.modify_rental("1234ABC", "C001", self.start, new_end_date=self.today + relativedelta(days=25))

    def test_get_all_rentals_returns_copy(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental("1234ABC", "C001", self.start, self.end, 500, "basic")
        rentals = self.shop.get_all_rentals()
        rentals.clear()
        self.assertEqual(len(self.shop.get_all_rentals()), 1)

    def test_str(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.add_worker(self.admin)
        result = str(self.shop) #calls the shop’s __str__() method and saves the returned text in result.
        self.assertIn("1 vehicles", result)
        self.assertIn("1 clients", result)
        self.assertIn("1 workers", result)
    
    def test_modify_rental_success_saves_changes(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental("1234ABC", "C001", self.start, self.end, 500, "basic")
        new_end = self.today + relativedelta(days=15)
        self.shop.modify_rental("1234ABC", "C001", self.start, new_end_date=new_end, new_kms_allowed=800, new_insurance_type="premium")
        rental = self.shop.get_rental("1234ABC", "C001", self.start)
        self.assertEqual(rental.end_date, new_end)
        self.assertEqual(rental.kms_allowed, 800)
        self.assertEqual(rental.insurance_type, "premium")

    def test_add_kms_to_rental_saves_kms_and_vehicle(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental("1234ABC", "C001", self.start, self.end, 500, "basic")
        self.shop.add_kms_to_rental("1234ABC", "C001", self.start, 100)
        rental = self.shop.get_rental("1234ABC", "C001", self.start)
        self.assertEqual(rental.kms_done, 100)
        self.assertEqual(self.car.mileage, 50100)

    def test_active_and_finished_rentals_lists(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_vehicle(self.car2)
        self.shop.add_client(self.client)
        self.shop.create_rental("1234ABC", "C001", self.start, self.end, 500, "basic")
        self.shop.create_rental("5678DEF", "C001", self.past_start, self.past_end, 500, "basic")
        self.assertEqual(len(self.shop.get_active_rentals()), 1)
        self.assertEqual(len(self.shop.get_finished_rentals()), 1)

if __name__ == "__main__":
    unittest.main()