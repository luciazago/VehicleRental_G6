import unittest
from datetime import date
from dateutil.relativedelta import relativedelta
from Vehicles.vehicle import Vehicle
from Vehicles.car import Car
from Vehicles.motorbike import Motorbike
from Vehicles.truck import Truck
from Exceptions.exceptions import InvalidLicensePlateError, InvalidMileageError, InvalidDateError

class TestVehicle(unittest.TestCase):

    def setUp(self):
        self.car = Car("Mercedes", "Black", "1234ABC", "C-Class", date(2015, 6, 1), 50000)
        self.motorbike = Motorbike("Yamaha", "Silver", "5678DEF", "MT-07", date(2018, 3, 1), 20000)
        self.truck = Truck("Scania", "Grey", "9999XYZ", "R450", date(2010, 1, 1), 100000)
        self.old_car = Car("BMW", "Blue", "2222BBB", "X3", date(2008, 1, 1), 80000)
        self.old_truck = Truck("MAN", "White", "1111AAA", "TGX", date(2005, 1, 1), 200000)

    def test_cannot_instantiate_vehicle_directly(self): #becasue vehicle is just a template class
        with self.assertRaises(TypeError):
            Vehicle("Audi", "Black", "1234ABC", "A4", date(2015, 1, 1), 0)

    def test_car_created_correctly(self):
        self.assertEqual(self.car.brand, "Mercedes")
        self.assertEqual(self.car.color, "Black")
        self.assertEqual(self.car.license_plate, "1234ABC")
        self.assertEqual(self.car.model, "C-Class")
        self.assertEqual(self.car.mileage, 50000)

    def test_motorbike_and_truck_created_correctly(self):
        self.assertEqual(self.motorbike.brand, "Yamaha")
        self.assertEqual(self.motorbike.license_plate, "5678DEF")
        self.assertEqual(self.truck.brand, "Scania")
        self.assertEqual(self.truck.license_plate, "9999XYZ")

    def test_plate_stored_uppercase_and_stripped(self):
        car = Car("Porsche", "White", " 1234abc ", "Macan", date(2015, 6, 1), 0)
        self.assertEqual(car.license_plate, "1234ABC")

    def test_text_fields_stripped_on_creation(self):
        car = Car("  Tesla  ", "  Red  ", "4444DDD", "  Model 3  ", date(2015, 1, 1), 0)
        self.assertEqual(car.brand, "Tesla")
        self.assertEqual(car.color, "Red")
        self.assertEqual(car.model, "Model 3")

    def test_mileage_stored_as_float(self):
        car = Car("Volkswagen", "Grey", "3333CCC", "Golf", date(2015, 1, 1), 1000)
        self.assertIsInstance(car.mileage, float)

    def test_invalid_plates_raise_error(self):
        invalid_plates = ["123ABC", "12345ABC", "ABC1234", "1234AB!", "1234ÄÖÜ", 1234567]

        for plate in invalid_plates:
            with self.assertRaises(InvalidLicensePlateError):
                Car("Audi", "Black", plate, "A3", date(2015, 1, 1), 0)

    def test_invalid_mileage_raises_error(self):
        with self.assertRaises(InvalidMileageError):
            Car("Seat", "Yellow", "5555EEE", "Ibiza", date(2015, 1, 1), -1)

        with self.assertRaises(InvalidMileageError):
            Car("Seat", "Yellow", "5555EEE", "Ibiza", date(2015, 1, 1), "abc")

    def test_zero_mileage_is_valid(self):
        car = Car("Seat", "Yellow", "5555EEE", "Ibiza", date(2015, 1, 1), 0)
        self.assertEqual(car.mileage, 0)

    def test_invalid_dates_raise_error(self):
        with self.assertRaises(InvalidDateError):
            Car("Cupra", "Green", "6666FFF", "Formentor", date.today() + relativedelta(days=1), 0)

        with self.assertRaises(InvalidDateError):
            Car("Cupra", "Green", "6666FFF", "Formentor", "2015-01-01", 0)

    def test_today_matriculation_date_is_valid(self):
        car = Car("Cupra", "Green", "6666FFF", "Formentor", date.today(), 0)
        self.assertEqual(car.matriculation_date, date.today())

    def test_invalid_text_fields_raise_error(self):
        invalid_values = ["", "   ", 123]

        for value in invalid_values:
            with self.assertRaises(ValueError):
                Car(value, "Black", "1234ABC", "C-Class", date(2015, 1, 1), 0)
            with self.assertRaises(ValueError):
                Car("Mercedes", value, "1234ABC", "C-Class", date(2015, 1, 1), 0)
            with self.assertRaises(ValueError):
                Car("Mercedes", "Black", "1234ABC", value, date(2015, 1, 1), 0)

    def test_update_brand_color_model(self):
        self.car.update_brand("  Audi  ")
        self.car.update_color("  Dark Blue  ")
        self.car.update_model("  A6  ")

        self.assertEqual(self.car.brand, "Audi")
        self.assertEqual(self.car.color, "Dark Blue")
        self.assertEqual(self.car.model, "A6")

    def test_update_text_fields_empty_raise_error(self):
        with self.assertRaises(ValueError):
            self.car.update_brand("")

        with self.assertRaises(ValueError):
            self.car.update_color("")

        with self.assertRaises(ValueError):
            self.car.update_model("")

    def test_update_mileage(self):
        self.car.update_mileage(60000) #checks from 50000 --> 60000
        self.assertEqual(self.car.mileage, 60000)
        self.car.update_mileage(60000) #chacks from 60000 --> 60000
        self.assertEqual(self.car.mileage, 60000)

    def test_update_mileage_invalid_raises_error(self):
        with self.assertRaises(InvalidMileageError):
            self.car.update_mileage(10000)
        with self.assertRaises(InvalidMileageError):
            self.car.update_mileage("abc")

    def test_years_since_matriculation(self):
        new_car = Car("Mini", "Pink", "7777GGG", "Cooper", date.today(), 0)
        self.assertEqual(new_car.years_since_matriculation(), 0)
        self.assertGreaterEqual(self.old_car.years_since_matriculation(), 10)

    def test_vehicle_equality(self):
        car1 = Car("Mercedes", "Black", "7777GGG", "E-Class", date(2015, 1, 1), 0)
        car2 = Car("BMW", "Blue", "7777GGG", "Series 5", date(2018, 1, 1), 0)
        car3 = Car("BMW", "Blue", "8888HHH", "Series 5", date(2018, 1, 1), 0)

        self.assertEqual(car1, car2) #considers two cars with the same lisence plate are equal (defined in vehicles)
        self.assertNotEqual(car1, car3)
        self.assertEqual(self.car.__eq__("not a vehicle"), NotImplemented)

    def test_to_csv_row(self):
        row = self.car.to_csv_row() #calls the to_csv_row() method and stores the returned dictionary in row

        self.assertEqual(row["type"], "Car")
        self.assertEqual(row["brand"], "Mercedes")
        self.assertEqual(row["color"], "Black")
        self.assertEqual(row["license_plate"], "1234ABC")
        self.assertEqual(row["model"], "C-Class")
        self.assertEqual(row["matriculation_date"], "2015-06-01")
        self.assertEqual(row["mileage"], 50000)
        self.assertEqual(self.motorbike.to_csv_row()["type"], "Motorbike")
        self.assertEqual(self.truck.to_csv_row()["type"], "Truck")

    def test_str_contains_important_information(self):
        text = str(self.car)

        self.assertIn("Car", text)
        self.assertIn("Mercedes", text)
        self.assertIn("C-Class", text)
        self.assertIn("1234ABC", text)
        self.assertIn("50000", text)

    def test_car_itv_and_maintenance(self):
        self.assertGreater(self.car.next_itv(), date.today()) #checks that the next ITV date of self.car is later than today.
        self.assertGreater(self.old_car.next_itv(), date.today())
        self.assertIn("Next maintenance", self.car.next_maintenance()) #self.car.next_maintenance() returns a string --> checks if the words: "Next maintenance", appear inside that text

        young_car_date = date.today() - relativedelta(years=2) #creates a date from 2 years ago.
        young_car = Car("Nissan", "Beige", "9090DDD", "Qashqai", young_car_date, 0) #creates a new car matriculated 2 years ago.
        self.assertEqual(young_car.next_itv(), young_car_date + relativedelta(years=4)) #checks that the ITV date is exactly matriculation date plus 4 years

    def test_motorbike_itv_and_maintenance(self):
        self.assertGreater(self.motorbike.next_itv(), date.today())
        self.assertIn("km", self.motorbike.next_maintenance())

        young_motorbike_date = date.today() - relativedelta(years=1)
        young_motorbike = Motorbike("Ducati", "Red", "1010EEE", "Monster", young_motorbike_date, 0)
        self.assertEqual(young_motorbike.next_itv(), young_motorbike_date + relativedelta(years=4))

        motorbike = Motorbike("Kawasaki", "Green", "1212III", "Ninja", date(2019, 1, 1), 5000)
        self.assertIn("6000", motorbike.next_maintenance())

    def test_truck_itv_and_maintenance(self):
        self.assertGreater(self.truck.next_itv(), date.today())
        self.assertGreater(self.old_truck.next_itv(), date.today())
        self.assertIn("km", self.truck.next_maintenance())

        truck = Truck("DAF", "Orange", "3434JJJ", "XF", date(2010, 1, 1), 5000)
        self.assertIn("6000", truck.next_maintenance())


if __name__ == "__main__":
    unittest.main()