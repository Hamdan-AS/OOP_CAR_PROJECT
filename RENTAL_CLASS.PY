import random, string
import datetime
import csv
import os

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
                  f"for {self.days} days. Total cost: ${self.total_cost:.2f}")
                  
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