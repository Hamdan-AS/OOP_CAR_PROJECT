import random, string
import datetime
import csv
import os


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
            print(f"{client.username} | Balance: {client.check_balance()}")

    def add_car(self, brand, model, seats, price_per_day):
        Car(brand, model, seats, price_per_day)
        print(f"Added new car: {brand} {model}")

    def remove_car(self, car_id):
        for car in Car.all_cars:
            if car.car_id == car_id:
                Car.all_cars.remove(car)
                print(f"Removed car {car_id}")
                return
        print(f"Car with ID {car_id} not found.")

    def view_reserved_cars(self):
        print("\n--- Reserved Cars ---")
        reserved = [car for car in Car.all_cars if not car.is_avail]
        if not reserved:
            print("No cars are currently reserved.")
        for car in reserved:
            car.show_details()