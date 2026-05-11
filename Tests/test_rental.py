import unittest
from datetime import date
from dateutil.relativedelta import relativedelta
from Services.rental import Rental
from Vehicles.car import Car
from Users.client import Client
from Exceptions.exceptions import InvalidRentalPeriodError, RentalAlreadyFinishedError, KmsExceededError, InvalidKmsAllowedError

class TestRental(unittest.TestCase):

    def setUp(self): #creates all the objects and dates that will be reused in the rental tests before each test runs
        self.car = Car("Mercedes", "Black", "1234ABC", "C-Class", date(2015, 1, 1), 50000)
        self.car2 = Car("BMW", "Blue", "5678DEF", "X3", date(2018, 1, 1), 30000)
        self.client = Client("Hanno Schwecke", date(1990, 1, 1), "C001")
        self.today = date.today()
        self.start = self.today - relativedelta(days=5)
        self.end = self.today + relativedelta(days=5)
        self.rental = Rental(self.car, self.client, self.start, self.end, 500, "basic")
        self.finished_rental = Rental(self.car2, self.client, self.today - relativedelta(days=10), self.today - relativedelta(days=1), 500, "basic")

    def test_rental_created_correctly(self):
        self.assertEqual(self.rental.vehicle, self.car)
        self.assertEqual(self.rental.client, self.client)
        self.assertEqual(self.rental.kms_allowed, 500)
        self.assertEqual(self.rental.insurance_type, "basic")

    def test_kms_done_starts_at_zero(self):
        self.assertEqual(self.rental.kms_done, 0.0)

    def test_insurance_stored_lowercase(self):
        rental = Rental(self.car, self.client, self.start, self.end, 500, "PREMIUM")
        self.assertEqual(rental.insurance_type, "premium")

    def test_insurance_stored_stripped(self):
        rental = Rental(self.car, self.client, self.start, self.end, 500, "full")
        self.assertEqual(rental.insurance_type, "full")

    def test_same_start_and_end_date_is_valid(self):
        rental = Rental(self.car, self.client, self.today, self.today, 100, "basic")
        self.assertIsNotNone(rental) #checks that the rental object was successfully created

    def test_end_date_before_start_raises_error(self): #the next line should raise an InvalidRentalPeriodError
        with self.assertRaises(InvalidRentalPeriodError):
            Rental(self.car, self.client, self.end, self.start, 500, "basic")

    def test_negative_kms_raises_error(self):
        with self.assertRaises(InvalidKmsAllowedError):
            Rental(self.car, self.client, self.start, self.end, -100, "basic")

    def test_zero_kms_raises_error(self):
        with self.assertRaises(InvalidKmsAllowedError):
            Rental(self.car, self.client, self.start, self.end, 0, "basic")

    def test_kms_not_number_raises_error(self):
        with self.assertRaises(InvalidKmsAllowedError):
            Rental(self.car, self.client, self.start, self.end, "abc", "basic")

    def test_invalid_insurance_raises_error(self):
        with self.assertRaises(ValueError):
            Rental(self.car, self.client, self.start, self.end, 500, "platinum")

    def test_active_rental(self):
        self.assertTrue(self.rental.is_active())
        self.assertFalse(self.rental.is_finished())
        self.assertFalse(self.rental.is_upcoming())

    def test_finished_rental(self):
        self.assertTrue(self.finished_rental.is_finished())
        self.assertFalse(self.finished_rental.is_active())
        self.assertFalse(self.finished_rental.is_upcoming())

    def test_upcoming_rental(self):
        rental = Rental(self.car, self.client, self.today + relativedelta(days=2), self.today + relativedelta(days=10), 500,"basic")

        self.assertTrue(rental.is_upcoming())
        self.assertFalse(rental.is_active())
        self.assertFalse(rental.is_finished())

    def test_add_kms_done(self):
        self.rental.add_kms_done(100)
        self.assertEqual(self.rental.kms_done, 100)

    def test_add_kms_updates_vehicle_mileage(self):
        self.rental.add_kms_done(100)
        self.assertEqual(self.car.mileage, 50100)

    def test_add_kms_exactly_at_limit(self):
        self.rental.add_kms_done(500)
        self.assertEqual(self.rental.kms_done, 500)

    def test_add_kms_exceeding_limit_raises_error(self):
        with self.assertRaises(KmsExceededError):
            self.rental.add_kms_done(600)

    def test_add_kms_negative_raises_error(self):
        with self.assertRaises(InvalidKmsAllowedError):
            self.rental.add_kms_done(-50)

    def test_add_kms_to_finished_rental_raises_error(self):
        with self.assertRaises(RentalAlreadyFinishedError):
            self.finished_rental.add_kms_done(50)

    def test_kms_remaining_at_start(self):
        self.assertEqual(self.rental.kms_remaining(), 500)

    def test_kms_remaining_after_adding_kms(self):
        self.rental.add_kms_done(200)
        self.assertEqual(self.rental.kms_remaining(), 300)

    def test_modify_end_date(self):
        new_end = self.today + relativedelta(days=10)
        self.rental.modify_rental(new_end_date=new_end)
        self.assertEqual(self.rental.end_date, new_end)

    def test_modify_kms_allowed(self):
        self.rental.modify_rental(new_kms_allowed=1000)
        self.assertEqual(self.rental.kms_allowed, 1000)

    def test_modify_insurance_type(self):
        self.rental.modify_rental(new_insurance_type="full")
        self.assertEqual(self.rental.insurance_type, "full")

    def test_modify_finished_rental_raises_error(self):
        with self.assertRaises(RentalAlreadyFinishedError):
            self.finished_rental.modify_rental(new_kms_allowed=1000)

    def test_modify_end_before_start_raises_error(self):
        with self.assertRaises(InvalidRentalPeriodError):
            self.rental.modify_rental(new_end_date=self.start - relativedelta(days=1))

    def test_modify_kms_below_done_raises_error(self):
        self.rental.add_kms_done(300)

        with self.assertRaises(InvalidKmsAllowedError):
            self.rental.modify_rental(new_kms_allowed=100)

    def test_modify_invalid_insurance_raises_error(self):
        with self.assertRaises(ValueError):
            self.rental.modify_rental(new_insurance_type="platinum")

    def test_set_kms_done_from_csv(self):
        self.rental.set_kms_done_from_csv(200)
        self.assertEqual(self.rental.kms_done, 200)

    def test_set_kms_done_from_csv_exceeds_allowed_raises_error(self):
        with self.assertRaises(KmsExceededError):
            self.rental.set_kms_done_from_csv(600)

    def test_to_csv_row_keys(self):
        row = self.rental.to_csv_row()

        for key in ["vehicle_plate", "client_id", "start_date", "end_date", "kms_allowed", "kms_done", "insurance_type"]:
            self.assertIn(key, row) #checks that each key exists inside the dictionary.

    def test_to_csv_row_vehicle_plate(self):
        self.assertEqual(self.rental.to_csv_row()["vehicle_plate"], "1234ABC")

    def test_to_csv_row_client_id(self):
        self.assertEqual(self.rental.to_csv_row()["client_id"], "C001")

    def test_same_rental_equal(self):
        rental2 = Rental(self.car, self.client, self.start, self.end, 1000, "full")
        self.assertEqual(self.rental, rental2)

    def test_different_vehicle_not_equal(self):
        rental2 = Rental(self.car2, self.client, self.start, self.end, 500, "basic")
        self.assertNotEqual(self.rental, rental2)

    def test_different_client_not_equal(self):
        client2 = Client("Clara Becker", date(1985, 1, 1), "C002")
        rental2 = Rental(self.car, client2, self.start, self.end, 500, "basic")
        self.assertNotEqual(self.rental, rental2)

    def test_rental_not_equal_to_non_rental(self):
        self.assertEqual(self.rental.__eq__("not a rental"), NotImplemented)

    def test_str_active_shows_active(self):
        self.assertIn("ACTIVE", str(self.rental))

    def test_str_finished_shows_finished(self):
        self.assertIn("FINISHED", str(self.finished_rental))

    def test_str_upcoming_shows_upcoming(self):
        rental = Rental(self.car, self.client, self.today + relativedelta(days=2), self.today + relativedelta(days=10), 500, "basic")
        self.assertIn("UPCOMING", str(rental))

    def test_str_contains_plate(self):
        self.assertIn("1234ABC", str(self.rental))

    def test_str_contains_client_id(self):
        self.assertIn("C001", str(self.rental))

    def test_str_contains_insurance_type(self):
        self.assertIn("basic", str(self.rental))
    
    def test_vehicle_must_be_vehicle_object(self):
        with self.assertRaises(TypeError):
            Rental("not vehicle", self.client, self.start, self.end, 500, "basic")

    def test_client_must_be_client_object(self):
        with self.assertRaises(TypeError):
            Rental(self.car, "not client", self.start, self.end, 500,"basic")

    def test_start_and_end_must_be_date_objects(self):
        with self.assertRaises(InvalidRentalPeriodError):
            Rental(self.car, self.client, "2025-01-01", "2025-01-10", 500, "basic")

    def test_insurance_must_be_text_on_creation(self):
        with self.assertRaises(ValueError):
            Rental(self.car, self.client, self.start, self.end, 500,123)

    def test_modify_rental_end_date_must_be_date_object(self):
        with self.assertRaises(InvalidRentalPeriodError):
            self.rental.modify_rental(new_end_date=123)

    def test_modify_rental_kms_must_be_positive_number(self):
        with self.assertRaises(InvalidKmsAllowedError):
            self.rental.modify_rental(new_kms_allowed="abc")

    def test_modify_rental_insurance_must_be_text(self):
        with self.assertRaises(ValueError):
            self.rental.modify_rental(new_insurance_type=123)

    def test_set_kms_done_from_csv_must_be_non_negative_number(self):
        with self.assertRaises(ValueError):
            self.rental.set_kms_done_from_csv("abc")

if __name__ == "__main__":
    unittest.main()