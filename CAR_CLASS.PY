import random, string
import datetime
import csv
import os
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
                  f"Seats: {self.seats} | Price per Day: {self.price_per_day:.2f} | "
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