import random
import string
import datetime
import csv
import os

# ------------------ CLI MENU ------------------
def cli_menu():
    print("\n" + "*" * 42)
    print("*" + " " * 10+ "WELCOME TO CAR RENTAL" + " " * 9 + "*")
    print("*" * 42)
    print("\n1. Admin Login")
    print("2. Register New Client")
    print("3. Client Login")
    print("0. Exit")
    return input("\nSelect an option: ")

# ------------------ CLIENT DASHBOARD ------------------
def client_dashboard(client):
    while True:
        print("\n" + "=" * 50)
        print(f"WELCOME, {client.first_name.upper()} {client.last_name.upper()}")
        print(f"ADDRESS: {client.address}")
        print("=" * 50)
        print("1. View Available Cars")
        print("2. Rent a Car")
        print("3. Return a Car")
        print("4. View Rental History")
        print("5. Check Balance")
        print("6. Add Balance")
        print("0. Logout")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            print("\n--- Available Cars ---")
            available_cars = [car for car in Car.all_cars if car.is_avail]
            if not available_cars:
                print("No cars available at the moment.")
            for car in available_cars:
                car.show_details()
                
        elif choice == '2':
            if client.rental:
                print("You already have an active rental.")
                continue
                
            print("\n--- Available Cars ---")
            available_cars = [car for car in Car.all_cars if car.is_avail]
            if not available_cars:
                print("No cars available for rent at the moment.")
                continue
                
            for i, car in enumerate(available_cars, 1):
                print(f"{i}. ", end="")
                car.show_details()
                
            try:
                car_choice = int(input("Select car number (0 to cancel): "))
                if car_choice == 0:
                    continue
                days = int(input("Number of days to rent: "))
                if days <= 0:
                    print("Please enter a valid number of days.")
                    continue
                    
                selected_car = available_cars[car_choice - 1]
                rental = Rental(client, selected_car, days)
                
            except (ValueError, IndexError):
                print("Invalid selection.")
                
        elif choice == '3':
            if not client.rental:
                print("You don't have any active rentals.")
                continue
                
            client.rental.return_car()
            client.rental = None
            
        elif choice == '4':
            print("\n--- Rental History ---")
            if not client.rental_history:
                print("No rental history found.")
            for rental in client.rental_history:
                print(f"{rental.car.brand} {rental.car.model} | "
                      f"{rental.days} days | Total: {rental.total_cost} | "
                      f"From: {rental.start_date} To: {rental.end_date}")
                      
        elif choice == '5':
            print(f"\nYour current balance: {client.check_balance()} PKR")
            
        elif choice == '6':
            try:
                amount = int(input("Enter amount to add: "))
                if amount > 0:
                    client.deposit(amount)
                    print(f"Successfully added {amount} PKR to your balance.")
                else:
                    print("Amount must be positive.")
            except ValueError:
                print("Please enter a valid amount.")
                
        elif choice == '0':
            print("Logging out...")
            break
            
        else:
            print("Invalid option. Please try again.")

# ------------------ ADMIN DASHBOARD ------------------
def admin_dashboard(admin):
    while True:
        print("\n=== Admin Dashboard ===")
        print("1. View All Users")
        print("2. View All Clients")
        print("3. Add New Car")
        print("4. Remove Car")
        print("5. View Reserved Cars")
        print("0. Logout")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            admin.view_all_users()
            
        elif choice == '2':
            admin.view_all_clients()
            
        elif choice == '3':
            try:
                brand = input("Car brand: ")
                model = input("Car model: ")
                seats = int(input("Number of seats: "))
                price = int(input("Price per day: "))
                admin.add_car(brand, model, seats, price)
            except ValueError:
                print("Invalid input. Please enter valid numbers for seats and price.")
                
        elif choice == '4':
            car_id = input("Enter car ID to remove: ").strip().upper()
            admin.remove_car(car_id)
            
        elif choice == '5':
            admin.view_reserved_cars()
            
        elif choice == '0':
            print("Logging out...")
            break
            
        else:
            print("Invalid option. Please try again.")

# ------------------ CSV HANDLER ------------------
class CSVHandler:
    CARS_FILE = 'cars.csv'
    USERS_FILE = 'users.csv'

    @classmethod
    def save_car(cls, car):
        """Save a single car's details to cars.csv"""
        file_exists = os.path.isfile(cls.CARS_FILE)
        with open(cls.CARS_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['car_id', 'brand', 'model', 'seats', 'price_per_day', 'is_available'])
            writer.writerow([
                car.car_id,
                car.brand,
                car.model,
                car.seats,
                car.price_per_day,
                car.is_avail
            ])

    @classmethod
    def load_cars(cls):
        """Load all cars from cars.csv and return as Car objects"""
        if not os.path.isfile(cls.CARS_FILE):
            return []

        cars = []
        with open(cls.CARS_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                car = Car(
                    brand=row['brand'],
                    model=row['model'],
                    seats=int(row['seats']),
                    price_per_day=float(row['price_per_day'])
                )
                car.car_id = row['car_id']
                car.is_avail = row['is_available'].lower() == 'true'
                cars.append(car)
        return cars

    @classmethod
    def overwrite_all_cars(cls, car_list):
        """Overwrite cars.csv with the current list of cars"""
        with open(cls.CARS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['car_id', 'brand', 'model', 'seats', 'price_per_day', 'is_available'])
            for car in car_list:
                writer.writerow([
                    car.car_id,
                    car.brand,
                    car.model,
                    car.seats,
                    car.price_per_day,
                    car.is_avail
                ])

    @classmethod
    def save_user(cls, user):
        """Save a single user's details to users.csv"""
        file_exists = os.path.isfile(cls.USERS_FILE)
        with open(cls.USERS_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['username', 'password', 'first_name', 'last_name', 'address', 'balance', 'role'])

            role = 'admin' if isinstance(user, Administer) else 'client'
            writer.writerow([
                user.username,
                user._User__password,  # Accessing the private password field
                user.first_name,
                user.last_name,
                user.address,
                user.check_balance(),
                role
            ])

    @classmethod
    def load_users(cls):
        """Load all users from users.csv and return as User objects"""
        if not os.path.isfile(cls.USERS_FILE):
            return [], []

        users = []
        admins = []
        with open(cls.USERS_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['role'] == 'admin':
                    admin = Administer(
                        username=row['username'],
                        password=row['password'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        address=row['address'],
                        balance=float(row['balance'])
                    )
                    admins.append(admin)
                    users.append(admin)
                else:
                    client = Client(
                        base_name=row['username'].split('_')[0],  # Extract base name from username
                        password=row['password'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        address=row['address'],
                        balance=float(row['balance'])
                    )
                    users.append(client)
        return users, admins

    @classmethod
    def overwrite_all_users(cls, user_list):
        """Overwrite users.csv with the current list of users"""
        with open(cls.USERS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password', 'first_name', 'last_name', 'address', 'balance', 'role'])
            for user in user_list:
                role = 'admin' if isinstance(user, Administer) else 'client'
                writer.writerow([
                    user.username,
                    user._User__password,
                    user.first_name,
                    user.last_name,
                    user.address,
                    user.check_balance(),
                    role
                ])

# ------------------ MAIN PROGRAM ------------------
def seed_data():
    # Try to load existing data first
    cars = CSVHandler.load_cars()
    users, admins = CSVHandler.load_users()

    # If no cars exist, create some sample cars
    if not cars:
        car1 = Car("Toyota", "Camry", 5, 50.0)
        car2 = Car("Honda", "Civic", 5, 45.0)
        car3 = Car("Ford", "Explorer", 7, 70.0)
        cars = Car.all_cars
    else:
        Car.all_cars = cars

    # If no admin exists, create a default admin
    if not admins:
        admin = Administer("admin", "admin123", "Admin", "User", "123 Admin St", 1000.0)
        CSVHandler.save_user(admin)
        admins = [admin]

    # Update registered users in Administer class
    Administer.registered_users = users
    Administer.all_clients = [user for user in users if isinstance(user, Client)]

    return admins[0] if admins else None

if __name__ == '__main__':
    try:
        admin = seed_data()
        if not admin:
            print("Error: No admin account found and could not create one.")
            exit(1)

        # Get clients from registered users
        clients = [user for user in Administer.registered_users if isinstance(user, Client)]

        while True:
            option = cli_menu()

            if option == '1':  # Admin Login
                uname = input("Admin Username: ")
                pwd = input("Password: ")
                if uname == admin.username and admin.security_check(pwd):
                    admin_dashboard(admin)
                    # Save any changes made during admin session
                    CSVHandler.overwrite_all_cars(Car.all_cars)
                    CSVHandler.overwrite_all_users(Administer.registered_users)
                else:
                    print("Invalid admin credentials.")

            elif option == '2':  # Register New Client
                base_name = input("Enter base username: ")

                # Check if username already exists
                if any(user.username.startswith(base_name + '_') for user in Administer.registered_users):
                    print(f"Username starting with '{base_name}' already exists. Please choose a different base name.")
                    continue

                password = input("Set your password: ")
                first_name = input("First Name: ")
                last_name = input("Last Name: ")
                address = input("Address: ")
                try:
                    balance = float(input("Initial deposit (PKR): "))
                    if balance < 0:
                        print("Balance cannot be negative.")
                        continue

                    new_client = Client(base_name, password, first_name, last_name, address, balance)
                    admin.register_user(new_client)
                    CSVHandler.save_user(new_client)  # Save new client to CSV
                    clients.append(new_client)
                    print(f"Registration successful! Your username is: {new_client.username}")

                    # Log in the new client
                    client_dashboard(new_client)
                    # Save any changes made during client session
                    CSVHandler.overwrite_all_cars(Car.all_cars)
                    CSVHandler.overwrite_all_users(Administer.registered_users)
                except ValueError:
                    print("Invalid deposit amount. Please enter a valid number.")

            elif option == '3':  # Client Login
                uname = input("Enter your username: ")
                pwd = input("Enter your password: ")

                # Check both registered users and admin
                user_found = None
                for user in Administer.registered_users:
                    if user.username == uname and user.security_check(pwd):
                        user_found = user
                        break

                if user_found:
                    if isinstance(user_found, Client):
                        client_dashboard(user_found)
                        # Save any changes made during client session
                        CSVHandler.overwrite_all_cars(Car.all_cars)
                        CSVHandler.overwrite_all_users(Administer.registered_users)
                    else:
                        print("Please use the Admin Login option to log in as admin.")
                else:
                    print("Invalid username or password.")

            elif option == '0':  # Exit
                # Save all data before exiting
                try:
                    CSVHandler.overwrite_all_cars(Car.all_cars)
                    CSVHandler.overwrite_all_users(Administer.registered_users)
                    print("All data has been saved successfully.")
                except Exception as e:
                    print(f"Warning: Error while saving data: {e}")

                print("Thank you for using the Online Car Rental System. Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        # Try to save data even on keyboard interrupt
        try:
            CSVHandler.overwrite_all_cars(Car.all_cars)
            CSVHandler.overwrite_all_users(Administer.registered_users)
            print("Data has been saved before exit.")
        except Exception as e:
            print(f"Warning: Could not save data before exit: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("The program will now exit.")