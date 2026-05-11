from datetime import date
from Services.shop_manager import ShopManager

def is_valid_plate(plate):
    plate = plate.strip().upper()
    return len(plate) == 7 and plate[:4].isdigit() and plate[4:].isalpha()

def read_plate(label="License Plate"):
    while True:
        plate = input(f"{label}: ").strip().upper()
        if is_valid_plate(plate):
            return plate
        print("Invalid license plate. Use format: 1234ABC")

def read_date(label):
    while True:
        try:
            print(f"\n{label}")
            year = int(input("Year: "))
            month = int(input("Month: "))
            day = int(input("Day: "))

            if year < 1900 or year > date.today().year:
                print("Invalid year. Please enter a realistic year.")
                continue
            return date(year, month, day)

        except ValueError:
            print("Invalid date. Please enter a valid year, month and day.")

def read_positive_float(label):
    while True:
        try:
            value = float(input(f"{label}: "))
            if value > 0:
                return value
            print(f"{label} must be positive.")
        except ValueError:
            print(f"Invalid {label.lower()}. Please enter a number.")

def read_non_empty_text(label):
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print(f"{label} cannot be empty.")

def read_insurance():
    while True:
        insurance = input("Insurance (basic/premium/full): ").strip().lower()
        if insurance in ["basic", "premium", "full"]:
            return insurance
        print("Invalid insurance. Choose: basic, premium or full.")

def read_role():
    while True:
        role = input("Role (mechanic/rental manager/administrator): ").strip().lower()
        if role in ["mechanic", "rental manager", "administrator"]:
            return role
        print("Invalid role. Choose: mechanic, rental manager or administrator.")

def admin_menu():
    print("\n***** ADMIN MENU *****")
    print("1. Add Vehicle")
    print("2. Add Client")
    print("3. Add Worker")
    print("4. Assign Vehicle to Client")
    print("5. Create Rental")
    print("6. Modify Rental")
    print("7. Add Kms to Rental")
    print("8. View All Vehicles")
    print("9. View All Clients")
    print("10. View All Workers")
    print("11. View All Rentals")
    print("12. View Active Rentals")
    print("13. View Finished Rentals")
    print("14. Save and Exit")
    print("15. Back to User Selection")

def add_vehicle_menu(manager):
    print("\nVehicle Type:")
    print("1. Car")
    print("2. Motorbike")
    print("3. Truck")

    while True:
        vehicle_type = input("Choose vehicle type: ").strip()
        if vehicle_type in ["1", "2", "3"]:
            break
        print("Invalid vehicle type. Please choose 1, 2 or 3.")

    brand = read_non_empty_text("Brand") 
    color = read_non_empty_text("Color")
    plate = read_plate("License Plate")
    model = read_non_empty_text("Model")
    matriculation_date = read_date("Matriculation Date")
    mileage = read_positive_float("Mileage")

    manager.add_vehicle(vehicle_type, brand, color, plate, model, matriculation_date, mileage)

    print("Vehicle added successfully.")

def add_client_menu(manager):
    name = read_non_empty_text("Client name")
    dob = read_date("Birth Date")
    user_id = read_non_empty_text("Client ID")
    manager.add_client(name, dob, user_id)
    print("Client added successfully.")

def add_worker_menu(manager):
    name = read_non_empty_text("Worker name")
    dob = read_date("Birth Date")
    user_id = read_non_empty_text("Worker ID")
    role = read_role()
    manager.add_worker(name, dob, user_id, role)
    print("Worker added successfully.")

def assign_vehicle_menu(manager):
    plate = read_plate("Vehicle plate")
    client_id = read_non_empty_text("Client ID")
    manager.assign_vehicle_to_client(plate, client_id)
    print("Vehicle assigned successfully.")

def create_rental_menu(manager):
    plate = read_plate("Vehicle plate")
    client_id = read_non_empty_text("Client ID")
    start_date = read_date("Start Date")
    end_date = read_date("End Date")
    kms_allowed = read_positive_float("Allowed kms")
    insurance = read_insurance()
    manager.create_rental(plate, client_id, start_date, end_date, kms_allowed,insurance)
    print("Rental created successfully.")

def modify_rental_menu(manager):
    plate = read_plate("Vehicle plate")
    client_id = read_non_empty_text("Client ID")
    start_date = read_date("Original Rental Start Date")

    print("\nNew rental information:")
    new_end_date = read_date("New End Date")
    new_kms_allowed = read_positive_float("New kms allowed")
    new_insurance_type = read_insurance()
    manager.modify_rental(plate, client_id, start_date, new_end_date, new_kms_allowed, new_insurance_type)
    print("Rental modified successfully.")

def add_kms_to_rental_menu(manager):
    plate = read_plate("Vehicle plate")
    client_id = read_non_empty_text("Client ID")
    start_date = read_date("Rental Start Date")
    kms = read_positive_float("Kms to add")
    manager.add_kms_to_rental(plate, client_id, start_date, kms)
    print("Kms added successfully.")

def admin_program(manager):
    while True:
        admin_menu()
        choice = input("\nChoose an option: ").strip()

        try:
            if choice == "1":
                add_vehicle_menu(manager)

            elif choice == "2":
                add_client_menu(manager)

            elif choice == "3":
                add_worker_menu(manager)

            elif choice == "4":
                assign_vehicle_menu(manager)

            elif choice == "5":
                create_rental_menu(manager)

            elif choice == "6":
                modify_rental_menu(manager)

            elif choice == "7":
                add_kms_to_rental_menu(manager)

            elif choice == "8":
                for vehicle in manager.get_all_vehicles():
                    print(vehicle)

            elif choice == "9":
                for client in manager.get_all_clients():
                    print(client)

            elif choice == "10":
                for worker in manager.get_all_workers():
                    print(worker)

            elif choice == "11":
                for rental in manager.get_all_rentals():
                    print(rental)

            elif choice == "12":
                rentals = manager.get_active_rentals()
                if not rentals:
                    print("There are no active rentals.")
                else:
                    for rental in rentals:
                        print(rental)

            elif choice == "13":
                rentals = manager.get_finished_rentals()
                if not rentals:
                    print("There are no finished rentals.")
                else:
                    for rental in rentals:
                        print(rental)
                        
            elif choice == "14":
                manager.save_all()
                print("Data saved successfully.")
                print("Goodbye.")
                return "exit"
            elif choice == "15":
                return "back"
            else:
                print("Invalid option. Please choose a number from 1 to 15.")

        except Exception as error:
            print(f"Error: {error}")

def client_menu(client):
    print(f"\n***** CLIENT MENU: {client.name} *****")
    print("1. View My Information")
    print("2. View My Vehicles")
    print("3. Update Vehicle Mileage")
    print("4. Update Vehicle Color")
    print("5. Check Next ITV")
    print("6. Check Next Maintenance")
    print("7. View My Rentals")
    print("8. Back to User Selection")

def client_login(manager):
    client_id = read_non_empty_text("Client ID")
    return manager.get_client(client_id)

def view_client_rentals(manager, client):
    found = False

    for rental in manager.get_all_rentals():
        if rental.client.user_id == client.user_id:
            print(rental)
            found = True

    if not found:
        print("You have no rentals.")

def client_program(manager):
    try:
        client = client_login(manager)
    except Exception as error:
        print(f"Error: {error}")
        return

    while True:
        client_menu(client)
        choice = input("\nChoose an option: ").strip()

        try:
            if choice == "1":
                print(client.get_info())
                print(f"Age: {client.get_age()}")

            elif choice == "2":
                if not client.vehicles:
                    print("You have no registered vehicles.")
                else:
                    for vehicle in client.vehicles:
                        print(vehicle)

            elif choice == "3":
                plate = read_plate("Vehicle plate")
                mileage = read_positive_float("New mileage")

                client.update_vehicle_mileage(plate, mileage)
                manager.save_vehicles()

                print("Mileage updated successfully.")

            elif choice == "4":
                plate = read_plate("Vehicle plate")
                color = read_non_empty_text("New color")

                client.update_vehicle_color(plate, color)
                manager.save_vehicles()

                print("Color updated successfully.")

            elif choice == "5":
                plate = read_plate("Vehicle plate")
                print(client.check_next_itv(plate))

            elif choice == "6":
                plate = read_plate("Vehicle plate")
                print(client.check_next_maintenance(plate))

            elif choice == "7":
                view_client_rentals(manager, client)

            elif choice == "8":
                return

            else:
                print("Invalid option. Please choose a number from 1 to 8.")

        except Exception as error:
            print(f"Error: {error}")


def user_selection_menu():
    print("\n***** VEHICLE RENTAL SYSTEM *****")
    print("1. Client")
    print("2. Admin")
    print("3. Save and Exit")

def main():
    manager = ShopManager()

    while True:
        user_selection_menu()
        choice = input("\nWho are you? ").strip()

        if choice == "1":
            client_program(manager)

        elif choice == "2":
            result = admin_program(manager)
            if result == "exit":
                break

        elif choice == "3":
            manager.save_all()
            print("Data saved successfully.")
            print("Goodbye.")
            break

        else:
            print("Invalid option. Please choose 1, 2 or 3.")


if __name__ == "__main__":
    main()