import unittest
import csv
import tempfile
from Data.csv_handler import CSVHandler

class TestCSVHandler(unittest.TestCase):

    def setUp(self): #Creates a CSVHandler object before each test runs
        self.handler = CSVHandler()

    def test_load_vehicles_file_not_found(self): #Checks that if the file doesne't exist, it returns an empty list
        result = self.handler.load_vehicles("missing_vehicles.csv")
        self.assertEqual(result, [])

    def test_load_clients_file_not_found(self):
        result = self.handler.load_clients("missing_clients.csv", [])
        self.assertEqual(result, [])

    def test_load_workers_file_not_found(self):
        result = self.handler.load_workers("missing_workers.csv")
        self.assertEqual(result, [])

    def test_load_rentals_file_not_found(self):
        result = self.handler.load_rentals("missing_rentals.csv", [], [])
        self.assertEqual(result, [])

    def test_load_truck_vehicle(self): #Create a fake CSV file with one truck, load it, and check that the truck was correctly created
        with tempfile.NamedTemporaryFile(mode="w+", newline="") as file: #creates a temporary file.
            writer = csv.DictWriter( 
                file,
                fieldnames=[
                    "type",
                    "brand",
                    "color",
                    "license_plate",
                    "model",
                    "matriculation_date",
                    "mileage"]) #creates the CSV writer object

            writer.writeheader() #writes the column names into the file

            writer.writerow({
                "type": "Truck",
                "brand": "Scania",
                "color": "Grey",
                "license_plate": "4444DDD",
                "model": "R450",
                "matriculation_date": "2010-01-01",
                "mileage": "100000"}) #writes one row of data into the CSV file
            
            file.flush() #saves file

            vehicles = self.handler.load_vehicles(file.name) #load_vehicles() function reads the temporary CSV file.
            self.assertEqual(len(vehicles), 1) #Checks that exactly one object exists in the list.
            self.assertEqual(vehicles[0].license_plate, "4444DDD") #Check that the correct truck was loaded

    def test_unknown_vehicle_type_is_skipped(self): #This test checks that invalid vehicle types are ignored when loading the CSV file
        with tempfile.NamedTemporaryFile(mode="w+", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "type",
                    "brand",
                    "color",
                    "license_plate",
                    "model",
                    "matriculation_date",
                    "mileage"])

            writer.writeheader()

            writer.writerow({
                "type": "Plane",
                "brand": "Boeing",
                "color": "White",
                "license_plate": "9999ZZZ",
                "model": "747",
                "matriculation_date": "2010-01-01",
                "mileage": "10000"}) #writes one invalid row into the CSV file (it creates a plane)

            file.flush()

            vehicles = self.handler.load_vehicles(file.name) #tries to upload the file --> but passes 
            self.assertEqual(vehicles, []) #checks no file has actually been uploaded

if __name__ == "__main__":
    unittest.main()