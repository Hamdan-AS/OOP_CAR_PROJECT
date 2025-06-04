import random, string
import datetime
import csv
import os

# All monetary values are in PKR (Pakistani Rupees)

# ------------------ USER CLASSES ------------------
class User:
    def __init__(self, username, password, first_name, last_name, address, balance):
        try:
            if not all([username, password, first_name, last_name, address]):
                raise ValueError("All user details must be provided")
            if not isinstance(balance, (int, float)) or balance < 0:
                raise ValueError("Balance must be a non-negative number")

            self.username = str(username)
            self.__password = str(password)
            self.first_name = str(first_name)
            self.last_name = str(last_name)
            self.address = str(address)
            self.__balance = float(balance)
        except (TypeError, ValueError) as e:
            print(f"Error creating user: {str(e)}")
            raise

    def deposit(self, amount):
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError("Deposit amount cannot be negative")
            self.__balance += amount
            return True
        except (TypeError, ValueError) as e:
            print(f"Error during deposit: {str(e)}")
            return False

    def renting(self, rent):
        try:
            rent = float(rent)
            if rent < 0:
                raise ValueError("Rent amount cannot be negative")
            if self.__balance < rent:
                raise ValueError("Insufficient balance to rent a car")
            self.__balance -= rent
            return True
        except (TypeError, ValueError) as e:
            print(f"Error during rental: {str(e)}")
            return False

    def check_balance(self):
        return self.__balance

    def security_check(self, asking_for_password):
        return self.__password == asking_for_password

    @staticmethod
    def generate_username_tag(base_name):
        suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        return f"{base_name}_{suffix}"

# ------------------ CLIENT ------------------
class Client(User):
    def __init__(self, base_name, password, first_name, last_name, address, balance):
        try:
            if not all([base_name, password, first_name, last_name, address]):
                raise ValueError("All client details must be provided")
            if not isinstance(balance, (int, float)) or balance < 0:
                raise ValueError("Balance must be a non-negative number")

            username = User.generate_username_tag(str(base_name))
            super().__init__(username, password, first_name, last_name, address, balance)
            self.rental = None
            self.rental_history = []
        except Exception as e:
            print(f"Error creating client: {str(e)}")
            raise

# ------------------ ADMIN ------------------
class Administer(User):
    registered_users = []
    all_clients = []

    def __init__(self, username, password, first_name, last_name, address, balance):
        try:
            if not all([username, password, first_name, last_name, address]):
                raise ValueError("All admin details must be provided")
            if not isinstance(balance, (int, float)) or balance < 0:
                raise ValueError("Balance must be a non-negative number")

            super().__init__(username, password, first_name, last_name, address, balance)
        except Exception as e:
            print(f"Error creating admin: {str(e)}")
            raise

    def renting(self, rent):
        try:
            raise PermissionError("Admins are not allowed to rent cars.")
        except PermissionError as e:
            print(str(e))
            return False

    def register_user(self, user_obj):
        try:
            if not isinstance(user_obj, (Client, Administer)):
                raise TypeError("Invalid user type. Must be Client or Administer")

            if not all([user_obj.username, user_obj.first_name, user_obj.last_name]):
                raise ValueError("User object is missing required attributes")

            for user in Administer.registered_users:
                if user.username == user_obj.username:
                    raise ValueError(f"Username '{user_obj.username}' already exists.")

            Administer.registered_users.append(user_obj)
            if isinstance(user_obj, Client):
                Administer.all_clients.append(user_obj)

            # Save the new user to CSV if it's a Client
            if isinstance(user_obj, Client):
                CSVHandler.save_user(user_obj)

            print(f"User '{user_obj.username}' registered successfully.")
            return True

        except Exception as e:
            print(f"Error registering user: {str(e)}")
            return False

    def view_all_users(self):
        print("\n--- Registered Users ---")
        for user in Administer.registered_users:
            print(user.username)

    def view_all_clients(self):
        print("\n--- Clients ---")
        for client in Administer.all_clients:
            print(f"{client.username} | Balance: PKR {client.check_balance():,.2f}")

    def add_car(self, brand, model, seats, price_per_day):
        Car(brand, model, seats, price_per_day)
        print(f"Added new car: {brand} {model}")

    def remove_car(self, car_id):
        for car in Car.all_cars:
            if car.car_id == car_id:
                Car.all_cars.remove(car)
                print(f"Car with ID {car_id} removed.")
                return
        print(f"Car with ID {car_id} not found.")

    def view_reserved_cars(self):
        print("\n--- Reserved Cars ---")
        reserved = [car for car in Car.all_cars if not car.is_avail]
        if not reserved:
            print("No cars are currently reserved.")
        for car in reserved:
            car.show_details()

# ------------------ CAR ------------------
class Car:
    all_cars = []

    def __init__(self, brand, model, seats, price_per_day):
        try:
            if not all([brand, model]):
                raise ValueError("Brand and model are required")
            if not isinstance(seats, int) or seats <= 0:
                raise ValueError("Seats must be a positive integer")
            if not isinstance(price_per_day, (int, float)) or price_per_day <= 0:
                raise ValueError("Price per day must be a positive number")

            self.car_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            self.brand = str(brand)
            self.model = str(model)
            self.seats = int(seats)
            self.price_per_day = float(price_per_day)
            self.is_avail = True
            Car.all_cars.append(self)

            # Save the new car to CSV
            CSVHandler.save_car(self)

        except Exception as e:
            print(f"Error creating car: {str(e)}")
            raise

    def show_details(self):
        try:
            print(f"Car ID: {self.car_id} | Brand: {self.brand} | Model: {self.model} | "
                  f"Seats: {self.seats} | Price per Day: PKR {self.price_per_day:,.2f} | "
                  f"Available: {'Yes' if self.is_avail else 'No'}")
        except Exception as e:
            print(f"Error showing car details: {str(e)}")

    def car_rented(self):
        try:
            if not self.is_avail:
                raise ValueError(f"{self.brand} {self.model} is already rented")
            self.is_avail = False
            print(f"{self.brand} {self.model} has been marked as rented.")
            return True
        except Exception as e:
            print(f"Error marking car as rented: {str(e)}")
            return False

    def car_returned(self):
        try:
            if self.is_avail:
                raise ValueError(f"{self.brand} {self.model} is already available")
            self.is_avail = True
            print(f"{self.brand} {self.model} is now available for rent again.")
            return True
        except Exception as e:
            print(f"Error marking car as returned: {str(e)}")
            return False

# ------------------ RENTAL ------------------
class Rental:
    def __init__(self, client_obj, car_obj, days):
        try:
            if not all([client_obj, car_obj]):
                raise ValueError("Client and car objects are required")
            if not isinstance(days, int) or days <= 0:
                raise ValueError("Rental days must be a positive integer")

            self.client = client_obj
            self.car = car_obj
            self.days = days
            self.start_date = datetime.date.today()
            self.end_date = self.start_date + datetime.timedelta(days=days)
            self.total_cost = float(car_obj.price_per_day * days)

            # Validate rental conditions
            if not car_obj.is_avail:
                raise ValueError(f"Car {car_obj.car_id} is already rented")

            if client_obj.check_balance() < self.total_cost:
                raise ValueError(f"{client_obj.username} has insufficient balance")

            # Process rental
            if not client_obj.renting(self.total_cost):
                raise ValueError("Failed to process rental payment")

            if not car_obj.car_rented():
                # Refund if car rental fails after payment
                client_obj.deposit(self.total_cost)
                raise RuntimeError("Failed to mark car as rented")

            self.client.rental = self
            self.client.rental_history.append(self)

            # Save updated car status
            CSVHandler.overwrite_all_cars(Car.all_cars)

            print(f"Rental created: {client_obj.username} rented {car_obj.brand} {car_obj.model} "
                  f"for {self.days} days. Total cost: PKR {self.total_cost:,.2f}")

        except Exception as e:
            print(f"Error creating rental: {str(e)}")
            raise

    def return_car(self):
        try:
            if not self.car:
                raise ValueError("No car associated with this rental")

            if self.car.is_avail:
                raise ValueError(f"Car {self.car.car_id} is already available")

            if not self.car.car_returned():
                raise RuntimeError("Failed to mark car as returned")

            # Update car status in CSV
            CSVHandler.overwrite_all_cars(Car.all_cars)

            print(f"{self.client.username} has successfully returned {self.car.brand} {self.car.model}")
            return True

        except Exception as e:
            print(f"Error returning car: {str(e)}")
            return False

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
                      f"{rental.days} days | Total: PKR {rental.total_cost:,.2f} | "
                      f"From: {rental.start_date} To: {rental.end_date}")
                      
        elif choice == '5':
            print(f"\nYour current balance is: PKR {client.check_balance():,.2f}")
            
        elif choice == '6':
            try:
                amount = int(input("Enter amount to add (PKR): "))
                if amount > 0:
                    client.deposit(amount)
                    print(f"Successfully added PKR {amount} to your balance.")
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
                price = int(input("Price per day (PKR): "))
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
    ADMINS_FILE = 'admins.csv'

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
    def save_admin(cls, admin):
        """Save a single admin's details to admins.csv"""
        file_exists = os.path.isfile(cls.ADMINS_FILE)
        with open(cls.ADMINS_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['username', 'password', 'first_name', 'last_name', 'address', 'balance'])
            writer.writerow([
                admin.username,
                admin._User__password,  # Accessing the private password field
                admin.first_name,
                admin.last_name,
                admin.address,
                admin.check_balance()
            ])

    @classmethod
    def load_admins(cls):
        """Load all admins from admins.csv and return as Administer objects"""
        if not os.path.isfile(cls.ADMINS_FILE):
            return []

        admins = []
        with open(cls.ADMINS_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    admin = Administer(
                        username=row['username'],
                        password=row['password'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        address=row['address'],
                        balance=float(row['balance'])
                    )
                    admins.append(admin)
                    Administer.registered_users.append(admin)
                except Exception as e:
                    print(f"Error loading admin {row.get('username', 'unknown')}: {str(e)}")
        return admins

    @classmethod
    def save_user(cls, user):
        """Save a single user's details to the appropriate CSV file"""
        if isinstance(user, Administer):
            return cls.save_admin(user)
            
        file_exists = os.path.isfile(cls.USERS_FILE)
        with open(cls.USERS_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['username', 'password', 'first_name', 'last_name', 'address', 'balance'])
            writer.writerow([
                user.username,
                user._User__password,  # Accessing private member
                user.first_name,
                user.last_name,
                user.address,
                user.check_balance()
            ])

    @classmethod
    def load_users(cls):
        """Load all clients from users.csv and return as Client objects"""
        if not os.path.isfile(cls.USERS_FILE):
            return []

        clients = []
        with open(cls.USERS_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    client = Client(
                        base_name=row['username'].split('_')[0],
                        password=row['password'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        address=row['address'],
                        balance=float(row['balance'])
                    )
                    clients.append(client)
                    Administer.all_clients.append(client)
                except Exception as e:
                    print(f"Error loading client {row.get('username', 'unknown')}: {str(e)}")
        return clients

    @classmethod
    def overwrite_all_users(cls, user_list):
        """Overwrite users.csv and admins.csv with the current lists"""
        # Separate admins and clients
        admins = [u for u in user_list if isinstance(u, Administer)]
        clients = [u for u in user_list if isinstance(u, Client)]
        
        # Save admins
        with open(cls.ADMINS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password', 'first_name', 'last_name', 'address', 'balance'])
            for admin in admins:
                writer.writerow([
                    admin.username,
                    admin._User__password,
                    admin.first_name,
                    admin.last_name,
                    admin.address,
                    admin.check_balance()
                ])
        
        # Save clients
        with open(cls.USERS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password', 'first_name', 'last_name', 'address', 'balance'])
            for client in clients:
                writer.writerow([
                    client.username,
                    client._User__password,
                    client.first_name,
                    client.last_name,
                    client.address,
                    client.check_balance()
                ])

# ------------------ MAIN PROGRAM ------------------
def seed_data():
    # Load existing data
    Car.all_cars = CSVHandler.load_cars()
    admins = CSVHandler.load_admins()
    clients = CSVHandler.load_users()
    
    # Combine all users
    all_users = admins + clients
    
    # Update class variables
    Administer.registered_users = all_users
    Administer.all_clients = clients
    
    # If no admin exists, create a default one
    if not admins:
        admin = Administer(
            username="admin",
            password="admin123",
            first_name="Admin",
            last_name="User",
            address="123 Admin St",
            balance=10000
        )
        admin.register_user(admin)  # This will save to CSV
        return admin
    
    # Return the first admin found
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